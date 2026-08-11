---
name: undercoat
description: Inspect, explain, mute and extend the Undercoat visual floor . The rules that stop AI-built interfaces looking AI-built. Use when a write was refused and the user wants to know why, when they want to turn a rule off for a project, or when they want to add a rule. Triggers on "why was that blocked", "undercoat", "mute that rule", "turn off ai-purple", "add a rule".
---

# Undercoat

Undercoat is a floor, not a ceiling. It does not make an interface good; it stops one
looking machine-made. When it refuses a write, the refusal is doing its job.

Undercoat runs in one of two modes. In the default opt-in mode it only acts on projects
containing `UNDERCOAT.md` or `.undercoat.patterns.json`. In global mode
(`~/.claude/undercoat/global` exists) it acts everywhere except projects containing
`.undercoat.off`. If the user says it is not firing, check the mode first.

If a project is mostly *writing about* design patterns, a style guide, documentation, a
blog, expect false alarms, because the rules cannot tell use from mention. Suggest
`.undercoat.off` for those rather than muting rules one by one.

Rules live in `patterns.json`, or in the project's own `.undercoat.patterns.json` if it
has one. Each has an `id`, a `severity`, a scope, a `because` and
an `instead`. `block` rules are refused at the write on tools that support hooks;
`warn` rules attach a note and let the write through.

## When the user asks why something was blocked

Read `patterns.json`, find the rule by id, and give them the `because` and the
`instead` in plain language. Do not soften it and do not apologise for the rule, say
what the pattern is a tell of, and what to do instead.

If the rule has a `risk_note`, mention it: that rule advises instead of blocking because
its match is a proxy, or because the pattern is sometimes wanted deliberately.

## When the user wants to mute a rule

Write or update `.undercoat.local.json` in the project root:

```json
{ "off": ["ai-purple"] }
```

This is local and gitignored. Before doing it, ask once whether the pattern is
genuinely wanted here, a brand that really is purple is a good reason; "it keeps
stopping me" usually means the retry needs a different idea, not that the rule is
wrong. Ask once, then respect the answer.

There is deliberately no per-line escape hatch. An agent could write one and grant
itself permission, which would turn enforcement back into advice.

## When the user wants to add a rule

Add it to `patterns.json`, then run `python3 build.py` to regenerate `AGENTS.md`.
Never edit `AGENTS.md` directly, it is generated and will be overwritten.

Set `severity` from risk, never from how many people agree:

- `block`, only if **both** `unambiguous` (the regex means one thing) and
  `rarely_legitimate` (almost nobody wants this on purpose) are true.
- `warn`, everything else. Set `risk_note` saying which of the two tests it failed.

Popularity is not safety. A pattern every catalog names can still be legitimate constantly,
and a pattern only one names can still be almost never wanted. Judge the second question.

Every rule needs a scope. The `in`/`not_in` globs are the main defense against false
alarms, and a false alarm costs far more than a missed pattern, a wrong block breaks
a build, a miss only lets a gradient through.

## When the user asks what the floor covers

Summarize from `patterns.json`: how many block, how many warn, and what categories.
Be straight about the limits. Undercoat matches text, so it catches banned tokens and
cannot see composition. "This layout is boring" is outside what it can do, by design.
For that, a post-hoc auditor is the right tool and Undercoat is meant to compose with
one, not replace it.
