---
name: code-review
description: Review working-tree or branch changes against repo standards and the agreed plan. Use when the user requests a code review.
---

## Select the changes

Honor the requested scope. For a pre-commit review, run `git status --short --untracked-files=all`, `git diff --cached`, and `git diff`. Inspect relevant untracked files directly. Check staged and unstaged changes separately so an unstaged fix cannot hide a defect in the staged version. For a branch review against a named base, use `git diff <base>...HEAD`. State which changes you reviewed.

## Identify the spec

Use the user’s requested issue, spec, or agreed chat plan. If the intended behavior is unclear, flag the specific assumption that affects a finding. If no spec is available, say so and complete the standards review.

## Identify the standards sources

Search the repo for every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

## Report

Use the same set of changes for two independent passes. Report each pass under its own heading.

- **Standards.** Cite the applicable repo rule for each violation. For a code smell, identify the changed lines and explain the maintenance cost in this particular case.
- **Spec.** For each missing, incorrect, or out-of-scope behavior, cite the requirement or agreed chat decision. Trace the affected caller and give a concrete example of the mismatch.

Run relevant checks when practical.

Under each heading, lead with the most consequential finding, its file and line, the scenario that triggers it, and the smallest useful correction. If an axis is clear, say so. List checks run and any material verification gap. Leave fixes and commits to the user unless they request a fix.

Adapted from Matt Pocock’s code-review skill.
