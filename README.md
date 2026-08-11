# Undercoat

**The invisible layer that keeps AI-built interfaces from looking AI-built.**

You know the look. Purple gradient, Inter, three cards in a row, Get Started. Your agent
writes it every time because it's the average of everything it learned. Undercoat catches
it at the write and refuses — so the file never lands.

It won't make your app beautiful. It'll stop it looking machine-made.

---

## Install

```bash
git clone https://github.com/jnemargut/undercoat
./undercoat/install.sh /path/to/your/project
```

That's it. The script prints every action, backs up your settings first, and
`./undercoat/uninstall.sh` reverses all of it.

**Scope.** Two modes.

*Opt-in (default).* The hook is registered once in `~/.claude/settings.json` but only acts
on projects containing `UNDERCOAT.md` or `.undercoat.patterns.json`. Every other repo is
untouched. Run `install.sh` once per project.

*Global.* `./undercoat/install.sh --global` covers every project on the machine with no
per-project setup — the right mode if you want a new idea protected from the first file.
Disarm any project with `touch .undercoat.off`, which wins in both modes.

A project can also ship its own `.undercoat.patterns.json`, and the hook will use that
instead of the installed rule set.

Guidance only, no enforcement:

```bash
./undercoat/install.sh /path/to/your/project --no-hook
```

## What it does

Two halves.

**The portable half** is `AGENTS.md` — a plain markdown file read on task start by 28+
agent tools (Claude Code, Codex, Cursor, Aider, Copilot, Gemini CLI, Windsurf, Zed,
Amazon Q). It teaches the rules. It works everywhere and enforces nothing.

**The enforcement half** is a `PreToolUse` hook for Claude Code. It inspects the content
of every Write, Edit, MultiEdit and NotebookEdit before it lands, and refuses on a match:

```
REFUSED  undercoat/ai-purple
FILE  src/Hero.tsx
MATCH  'from-purple-600'
WHY  The purple-to-violet gradient is the single strongest tell of machine-made UI.
     Models reach for it because it sits under thousands of SaaS landing pages in
     the training data.
CONSTRAINT  One flat colour chosen for this project. If you want depth, use spacing
            and type weight, not a gradient.
DO NOT  ask the user to approve this. Choose a direction and rewrite the file.
```

The agent reads that and tries again. You are not interrupted.

It also watches `Bash`, because blocking the Write tool alone does not stop an agent
writing the file — `cat > file`, a heredoc, `sed -i` and `tee` all bypass it, and
[a Write-tool guard has been reported pushing models into the heredoc route](https://github.com/anthropics/claude-code/issues/40517).
Undercoat refuses the *route* and points the agent back at the Write tool.

## The rules

56 rules: **20 block, 36 advise.**

Severity comes from risk, not popularity. A rule refuses a write only if both are true:

- **`unambiguous`** — the match means one thing, not a proxy that also catches real code
- **`rarely_legitimate`** — almost nobody wants this pattern on purpose

Everything else advises, and carries a `risk_note` saying which test it failed. That is
deliberate: how many catalogs name a pattern tells you how *contested* it is, not whether
refusing it will ever be *wrong*. A hot-linked Unsplash URL is named by one source and is
almost never right — safe to block. "Three equal cards" is named by four and is legitimate
constantly — not safe to block. Catalog counts are still recorded, as provenance only.

Undercoat matches text. It cannot see composition, and it does not try to. Contrast
ratios and line length need computed layout and are deliberately not shipped — that is a
post-hoc auditor's job. Undercoat is built to compose with one, not replace it.

**Known false alarm: writing about the patterns.** A style guide, design doc or blog post
that quotes `from-purple-600` or "Lorem ipsum" trips the rule describing it. Undercoat
cannot tell use from mention. Disarm those projects with `.undercoat.off` — this repo
carries one for exactly that reason.

## When a rule is wrong

```json
// .undercoat.local.json — local, gitignored
{ "off": ["ai-purple"] }
```

Per-rule, per-project. There is no per-line escape hatch on purpose: an agent could write
one and grant itself permission, which turns enforcement back into advice.

A blocking rule that refuses the same file three times stops and hands the decision to
you rather than letting the agent loop.

## Adding rules

Edit `patterns.json`, then:

```bash
python3 build.py            # regenerate AGENTS.md
python3 build.py --check    # CI: fail if AGENTS.md is stale
```

`patterns.json` is the original. `AGENTS.md` is generated and committed, so nobody
installing Undercoat ever runs a build step. Never edit `AGENTS.md` by hand.

`patterns.schema.json` enforces the severity model: a rule cannot be `block` unless both
risk flags are true, and a `warn` rule must carry a `risk_note`.

## Status

Early. Two honest caveats. The `catalogs` counts are reconstructed from published
descriptions, not verified against source rule files — they are provenance only and no
longer drive severity, which lowers the cost of that gap. And the `rarely_legitimate`
calls are **judgments, not measurements**. They are the first thing to audit if a block
ever fires on code you wanted.

**Validated against real code.** The rules were run over shadcn/ui, tailwindcss.com and
cal.com — 4,722 files of well-regarded hand-written UI. The first run refused **32.7% of
tailwindcss.com**, which exposed three wrong `rarely_legitimate` calls and five rules that
had to be demoted or rescoped. After those fixes:

| corpus | before | after |
|---|---|---|
| shadcn/ui | 9.6% | **0.03%** |
| tailwindcss.com | 32.7% | **3.27%** |
| cal.com | 4.5% | **0.68%** |

Detection was re-checked afterwards so the improvement isn't just a weaker tool: a generic
landing page still trips seven blocking rules at once.

Known residue: `buzzword-copy` can fire on prose inside code comments, and Tailwind's own
site legitimately demos purple swatches. Both are rare and both are wrong-block risks.

Requires `python3` (present on macOS and most Linux). No npm package, no account, no key.

## Credit

The pattern vocabulary in this space was largely established by others. Undercoat's rules
are assembled from patterns independently named by
[impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0),
[Taste Skill](https://www.tasteskill.dev/), web-taste, and Anthropic's frontend-design
skill. See `NOTICE`.

Undercoat's contribution is not the list. It's the moment — refusing at the write, before
the file exists.

## Licence

Apache-2.0. See `LICENSE` and `NOTICE`.
