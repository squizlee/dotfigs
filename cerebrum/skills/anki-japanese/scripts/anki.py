#!/usr/bin/env python3
"""AnkiConnect helper for the Japanese deck. Stdlib only; Anki must be open.

  anki.py check              is AnkiConnect reachable? deck/model present?
  anki.py setup              create deck, note type, options (idempotent)
  anki.py add < notes.json   add notes; skips duplicates, never overwrites
  anki.py find <query>       list notes matching an Anki search
"""
import json
import os
import sys
import urllib.request

URL = "http://127.0.0.1:8765"
DECK = "Japanese"
MODEL = "JP Sentence"
CONFIG = "Japanese"
FIELDS = ["Japanese", "English", "Reading", "Audio", "Swap", "Notes", "AddListen"]

# Speak-card and Listen-card audio: real clip if present, else macOS TTS.
AUDIO = ("{{#Audio}}{{Audio}}{{/Audio}}"
         "{{^Audio}}{{tts ja_JP voices=Kyoko:Japanese}}{{/Audio}}")
DETAILS = """
<div class="jp">{{Japanese}}</div>
{{#Reading}}<div class="reading">{{Reading}}</div>{{/Reading}}
{{#Notes}}<div class="notes">{{Notes}}</div>{{/Notes}}
{{#Swap}}<div class="swap">Swap: {{Swap}}</div>{{/Swap}}
"""
TEMPLATES = [
    {
        "Name": "Speak",
        "Front": '<div class="en">{{English}}</div>\n<div class="hint">Say it aloud</div>',
        "Back": '{{FrontSide}}\n<hr id="answer">' + DETAILS + AUDIO,
    },
    {
        # Generated only when AddListen is non-empty.
        "Name": "Listen",
        "Front": '{{#AddListen}}<div class="hint">What does this mean?</div>\n'
        + AUDIO + "{{/AddListen}}",
        "Back": '{{FrontSide}}\n<hr id="answer">\n<div class="en">{{English}}</div>' + DETAILS,
    },
]
CSS = """.card { font-family: -apple-system, "Hiragino Sans", sans-serif; font-size: 22px;
  text-align: center; color: #222; background: #fafafa; }
.nightMode.card { color: #eee; background: #1e1e1e; }
.en { font-size: 26px; }
.jp { font-size: 34px; margin: 8px 0; }
.reading { font-size: 18px; opacity: .7; }
.notes, .swap { font-size: 16px; opacity: .8; margin-top: 10px; }
.hint { font-size: 14px; opacity: .5; margin-top: 6px; }
"""
OPTIONS = {"new": {"perDay": 8}, "rev": {"perDay": 150},
           "lapse": {"leechFails": 6, "leechAction": 1},  # 1 = tag only
           "desiredRetention": 0.9}


def call(action, **params):
    req = urllib.request.Request(
        URL, json.dumps({"action": action, "version": 6, "params": params}).encode())
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = json.load(r)
    except OSError as e:
        sys.exit(f"AnkiConnect unreachable at {URL} ({e}). Is Anki open?")
    if resp.get("error"):
        raise RuntimeError(f"{action}: {resp['error']}")
    return resp["result"]


def check():
    print(json.dumps({
        "ankiconnect": call("version"),
        "deck": DECK in call("deckNames"),
        "model": MODEL in call("modelNames"),
    }))


def setup():
    done = []
    if DECK not in call("deckNames"):
        call("createDeck", deck=DECK)
        done.append(f"created deck {DECK}")
    if MODEL not in call("modelNames"):
        call("createModel", modelName=MODEL,
             inOrderFields=FIELDS, css=CSS, cardTemplates=TEMPLATES)
        done.append(f"created note type {MODEL}")
    else:
        missing = [f for f in FIELDS if f not in call("modelFieldNames", modelName=MODEL)]
        if missing:
            sys.exit(f"note type {MODEL} exists but lacks fields {missing}; fix by hand")
        want = {t["Name"]: {"Front": t["Front"], "Back": t["Back"]} for t in TEMPLATES}
        if call("modelTemplates", modelName=MODEL) != want:
            call("updateModelTemplates", model={"name": MODEL, "templates": want})
            done.append("updated card templates")
        if call("modelStyling", modelName=MODEL)["css"] != CSS:
            call("updateModelStyling", model={"name": MODEL, "css": CSS})
            done.append("updated styling")

    conf = call("getDeckConfig", deck=DECK)
    if conf["name"] != CONFIG:  # don't edit the shared Default preset
        new_id = call("cloneDeckConfigId", name=CONFIG, cloneFrom=conf["id"])
        call("setDeckConfigId", decks=[DECK], configId=new_id)
        conf = call("getDeckConfig", deck=DECK)
        done.append(f"created options preset {CONFIG}")
    changed = False
    for key, val in OPTIONS.items():
        if isinstance(val, dict):
            for k, v in val.items():
                changed |= conf[key].get(k) != v
                conf[key][k] = v
        else:
            changed |= conf.get(key) != val
            conf[key] = val
    if changed:
        call("saveDeckConfig", config=conf)
        done.append("applied options " + json.dumps(OPTIONS))
    print("\n".join(done) or "already set up; nothing to do")


def add():
    notes = json.load(sys.stdin)
    if isinstance(notes, dict):
        notes = [notes]
    added, skipped, failed = [], [], []
    for n in notes:
        jp = n.get("Japanese", "").strip()
        en = n.get("English", "").strip()
        if not jp or not en:
            failed.append({"note": n, "error": "Japanese and English are required"})
            continue
        fields = {f: str(n.get(f, "")).strip() for f in FIELDS if f != "Audio"}
        fields["AddListen"] = "y" if n.get("AddListen") else ""
        note = {"deckName": DECK, "modelName": MODEL, "fields": fields,
                "tags": n.get("tags", []),
                "options": {"allowDuplicate": False, "duplicateScope": "deck"}}
        if n.get("audio_path"):
            p = os.path.expanduser(n["audio_path"])
            note["audio"] = [{"path": p, "filename": os.path.basename(p),
                              "fields": ["Audio"]}]
        try:
            added.append({"id": call("addNote", note=note), "Japanese": jp})
        except RuntimeError as e:
            (skipped if "duplicate" in str(e) else failed).append(
                {"Japanese": jp, "error": str(e)})
    print(json.dumps({"added": added, "skipped": skipped, "failed": failed},
                     ensure_ascii=False, indent=1))


def find(query):
    ids = call("findNotes", query=f'deck:"{DECK}" {query}')
    out = [{"id": i["noteId"], "Japanese": i["fields"]["Japanese"]["value"],
            "English": i["fields"]["English"]["value"], "tags": i["tags"]}
           for i in call("notesInfo", notes=ids[:200])]
    print(json.dumps({"total": len(ids), "notes": out}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "check":
        check()
    elif cmd == "setup":
        setup()
    elif cmd == "add":
        add()
    elif cmd == "find":
        find(" ".join(sys.argv[2:]))
    else:
        sys.exit(__doc__)
