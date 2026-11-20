---
name: anki-japanese
description: Use when the user wants to add, draft, or look up Japanese flashcards in Anki — e.g. "add these to anki", "make cards from this Irodori lesson", "cards from my tutor session", "/anki-japanese コーヒーをください". Drafts sentence cards for the "Japanese" deck, previews them, and adds them via AnkiConnect.
---

# Anki Japanese

Turn whatever I give you (a phrase, a list, a pasted Irodori dialogue, tutor notes) into cards in my `Japanese` deck. Goal: practical spoken Japanese for a Japan trip starting **2 Feb 2027**, so cards train **meaning → spoken Japanese**.

Helper: `scripts/anki.py` next to this file (stdlib Python, talks to AnkiConnect on `127.0.0.1:8765`). Anki must be open.

## Workflow

1. **Check**: `python3 <skill>/scripts/anki.py check`. If unreachable, tell me to open Anki and stop. If deck or model is `false`, run `setup` (idempotent) and say what it created.
2. **Draft** cards per the rules below.
3. **Preview** as a compact table (Japanese · English · tags · Listen?) and wait for my OK or edits. Skip the preview only if I said "just add".
4. **Add**: pipe a JSON array to `python3 <skill>/scripts/anki.py add`. Report added / skipped (duplicates) / failed counts. Never edit or delete existing notes unless I ask.

## Card rules

- **Chunks, not lone words.** Prefer a usable sentence or phrase (`コーヒーをください。`) over a dictionary word. A lone word is fine only for high-value nouns (駅, トイレ) and then the English cue says so.
- **Polite です/ます form** by default; casual only if I ask or the source is casual.
- **Unambiguous English cue.** If several Japanese answers would fit, add context in parentheses: `Excuse me (to get a waiter's attention)`.
- **Japanese**: natural kanji + kana as a native would write it. **Reading**: hiragana reading only if the Japanese contains kanji.
- **Swap**: 2–4 substitutions that fit the pattern (`水 / お茶 / ビール`), when the sentence is a reusable frame.
- **Notes**: one short line on the pattern or nuance. Leave empty if obvious.
- **AddListen: true** for things I'll mostly *hear* rather than say (staff questions, announcements, common replies). Otherwise false.
- **Audio**: TTS plays automatically. If I give an audio file (e.g. an Irodori mp3), set `audio_path`.
- One idea per card. Split long dialogue lines into the reusable parts.
- Batches: flag it if a batch exceeds ~25 notes; the deck releases 8 new cards/day, so big batches queue for days. Put trip-critical cards first.

## Tags (hierarchical, always set src + topic)

- `src::irodori::A1-L03` (course level + lesson), `src::tutor::YYYY-MM-DD`, or `src::manual`
- `topic::food|transport|hotel|shopping|directions|help|intro|smalltalk|time|numbers` — plus `topic::trip` on anything I'll need in Japan
- `phase::1`–`phase::4` by grammar level: 1 = basics/questions/です・ます present; 2 = past, negative, locations, requests; 3 = て-form, permission, want, reasons; 4 = discourse/clarifying/extending
- `core::repair` for conversation-repair phrases (もう一度お願いします etc.)

## JSON shape

```json
[{"Japanese": "コーヒーをください。", "English": "Coffee, please.", "Reading": "",
  "Swap": "水 / お茶 / ビール", "Notes": "Xをください = please give me X",
  "AddListen": false, "tags": ["src::manual", "topic::food", "topic::trip", "phase::1"]}]
```

Optional: `"audio_path": "~/Downloads/irodori_L03_02.mp3"`.

## Irodori audio clips

Irodori A1 audio lives in `~/read/irodori_japanese_a1_audio/`, named by the textbook's track number (page `00-04` → `X_[00-04]_*.mp3`). Tracks are whole sections, so cut per-phrase clips:

1. Find phrase boundaries: `ffmpeg -i <track> -af silencedetect=noise=-35dB:d=0.4 -f null - 2>&1 | grep silence_`. Speech = from one `silence_end` to the next `silence_start`. Match segments to the page's lines in order; some tracks also read out item letters (a, b, c…) as short ~0.3 s segments between phrases.
2. Cut with ~0.15 s padding into the scratchpad: `ffmpeg -i <track> -ss <start> -to <end> -c:a libmp3lame -q:a 4 irodori_A1-L00_<romaji>.mp3`.
3. Pass each clip as `audio_path`; Anki copies it into its media folder. Cards with no recording fall back to TTS (Kyoko).

## Lookups

`anki.py find '<anki search>'` lists notes, e.g. `find tag:topic::food`, `find "Japanese:*ください*"`. Use it to check before adding near-duplicates or when I ask "what do I have on X".

## Deck setup (done by `setup`)

Deck `Japanese`; note type `JP Sentence` (fields: Japanese, English, Reading, Audio, Swap, Notes, AddListen; cards: Speak always, Listen when AddListen set); own options preset: 8 new/day, 150 reviews/day, leech at 6 lapses → tag only, desired retention 0.90. FSRS itself is a global toggle that AnkiConnect can't set — remind me to enable it in Deck Options once.
