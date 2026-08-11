# Undercoat

**Your agent writes the slop. Undercoat refuses it. You never see the file.**

You know the look. Purple gradient, Inter, three cards in a row, Get Started.

Your agent writes it every time — not because it's careless, but because that page is the
average of everything it learned. Slop isn't a bug. It's the mean.

Undercoat catches it at the write and refuses. The file never lands.

It won't make your app beautiful. It'll stop it looking machine-made.

*This is the opposite of cleaning up afterwards.*

---

## So what is it doing?

Every design tool for AI agents is a document. The agent reads it, agrees with it, and has
forgotten it by file forty. Undercoat isn't a document — it sits on the write and says no.

```
● Write(src/Hero.tsx)
  ✗ Blocked — undercoat/ai-purple

REFUSED  undercoat/ai-purple
FILE  src/Hero.tsx
MATCH  'from-purple-600'
WHY  The purple-to-violet gradient is the single strongest tell of machine-made UI.
     Models reach for it because it sits under thousands of SaaS landing pages.
CONSTRAINT  One flat colour chosen for this project. If you want depth, use spacing
            and type weight, not a gradient.
DO NOT  ask the user to approve this. Choose a direction and rewrite the file.

● Write(src/Hero.tsx) — retry
  ✓ written
```

The agent reads that and tries again. **You are never interrupted.**

## Start here in 2 minutes

```bash
git clone https://github.com/jnemargut/undercoat
./undercoat/install.sh /path/to/your/project
```

That's it. The script prints every action it takes, backs up your settings first, and
`./undercoat/uninstall.sh` puts everything back.

Want it everywhere, with no per-project setup?

```bash
./undercoat/install.sh --global
```

Every project is covered from the first file. Disarm any one of them with
`touch .undercoat.off`.

No account. No API key. No npm package. Plain Python and plain markdown — the same
install model as [decision-kit](https://github.com/jnemargut/decision-kit).

## How it works

**Two halves, and only one of them needs a hook.**

1. **`AGENTS.md`** — the portable half. Plain markdown, read on task start by 28+ agent
   tools: Claude Code, Codex, Cursor, Aider, Copilot, Gemini CLI, Windsurf, Zed, Amazon Q.
   It teaches the rules. It enforces nothing, and it works everywhere.

2. **The hook** — the enforcement half. A `PreToolUse` hook for Claude Code that reads the
   content of every Write, Edit, MultiEdit and NotebookEdit *before it lands*, and refuses
   on a match.

Enforcement is the upgrade, not the product. On a tool without hooks, Undercoat degrades to
guidance rather than breaking.

It watches `Bash` too. Blocking the Write tool alone doesn't stop an agent writing the file
— `cat > file`, a heredoc, `sed -i` and `tee` all walk straight past it, and
[a Write-tool guard has been reported *pushing* models into the heredoc route](https://github.com/anthropics/claude-code/issues/40517).
Undercoat refuses the route and points the agent back at the Write tool.

## How it compares

| | Undercoat | Taste skills | Post-hoc auditors | Linters |
|---|---|---|---|---|
| When it acts | At the write | Before, as advice | After the file exists | At commit or CI |
| Can it refuse? | **Yes** | No | No | Yes, later |
| Survives file 40 | **Yes** | Drifts | n/a | Yes |
| Needs a design system | No | Sometimes | Sometimes | n/a |
| What it promises | A floor | A ceiling | A cleanup | Correctness |

Undercoat is a **floor, not a ceiling**. Everyone else sells you beautiful. This one
guarantees *not embarrassing*. That's a smaller promise, and it's one a write-time rule can
actually keep.

It composes rather than competes. Run a taste skill for the ceiling. Run Undercoat so the
floor holds while you do.

## The rules

**56 rules — 20 refuse, 36 advise.**

<details>
<summary><strong>Refused</strong> — 20 rules</summary>

**Colour** — `ai-purple` · `ai-purple-hex` (the seven exact hexes models pick for "primary")
· `rainbow-gradient` · `tinted-shadow` · `gradient-on-root`

**Surface** — `neon-glow` · `ambient-blur-orb` (the blurred blob behind every generated hero)
· `gradient-border-trick` · `z-index-nuke`

**Type** — `default-sans-inter`

**Copy** — `generic-cta` · `vague-headline` · `buzzword-copy` · `lorem-ipsum` ·
`placeholder-copy` · `fake-testimonial` · `ai-implementation-comment`

**Assets** — `stock-placeholder-image` · `generated-avatar-service` · `emoji-as-icon`

</details>

<details>
<summary><strong>Advised</strong> — 36 rules</summary>

`three-card-grid` · `nested-cards` · `everything-centered` · `hero-icon-circle` ·
`full-height-hero` · `default-container-width` · `sticky-everything` · `status-chip-soup` ·
`glassmorphism` · `default-heavy-shadow` · `uniform-bubbly-radius` · `tailwind-default-blue` ·
`default-grey-body` · `pure-black-on-white` · `eyebrow-label` · `giant-hero-text` ·
`all-bold` · `system-font-only` · `sparkles-icon` · `trusted-by-logos` ·
`powered-by-ai-copy` · `exclamation-marketing` · `dark-mode-reflex` · `uniform-fade-in` ·
`bounce-easing` · `decorative-pulse` · `slow-transition` · `cramped-padding` ·
`magic-spacing` · `small-touch-target` · `ring-decoration` · `border-and-shadow` ·
`inline-style-attribute` · `important-override` · `hardcoded-hex-in-markup` ·
`placeholder-as-label`

</details>

Severity comes from **risk, not popularity**. A rule refuses only if both are true:

- `unambiguous` — the match means one thing, not a proxy that also catches real code
- `rarely_legitimate` — almost nobody wants this pattern on purpose

Everything else advises, and says why in a `risk_note`.

That distinction is the whole design. How many catalogs name a pattern tells you how
*contested* it is — not whether refusing it will ever be *wrong*. A hot-linked Unsplash URL
is named by one source and is almost never right: safe to refuse. "Three equal cards" is
named by four and is legitimate constantly: not safe to refuse.

## When a rule is wrong

```json
// .undercoat.local.json — local, gitignored
{ "off": ["ai-purple"] }
```

Per-rule, per-project. There's deliberately **no per-line escape hatch** — an agent could
write one and grant itself permission, and enforcement would quietly become advice again.

A rule that refuses the same file three times stops and hands the decision to you rather
than letting the agent loop.

## Adding rules

```bash
python3 build.py            # regenerate AGENTS.md from patterns.json
python3 build.py --check    # CI: fail if AGENTS.md is stale
```

`patterns.json` is the original. `AGENTS.md` is generated *and committed*, so nobody
installing Undercoat ever runs a build step. Never edit `AGENTS.md` by hand.

`patterns.schema.json` enforces the model: a rule can't refuse unless both risk flags are
true, and an advising rule must say which test it failed.

## What it can't do

Undercoat matches text. That's the whole mechanism, and it has edges worth knowing.

**It can't see composition.** Four identical card sections stacked vertically with no
hierarchy will pass every rule. That's where "looks machine-made" really lives, and a regex
can't reach it.

**It can't see the background.** `text-gray-400` is washed out on white and perfectly
readable on near-black. Same string, opposite verdict.

**It can't tell use from mention.** A style guide that quotes `from-purple-600` trips the
rule describing it. Disarm those projects with `.undercoat.off` — this repo carries one.

**Contrast ratios and line length aren't shipped at all.** They need computed layout. That's
an auditor's job, and Undercoat is built to sit alongside one.

## Validated against real code

The rules were run over **shadcn/ui, tailwindcss.com and cal.com** — 4,722 files of
well-regarded hand-written UI. The first pass refused **32.7% of tailwindcss.com**.

That exposed three judgment calls that were simply wrong: `dark:text-gray-400` is correct
dark-mode code, `backdrop-blur` on a sticky nav is standard practice, and
`placeholder="John Doe"` is a name-format hint rather than a fake testimonial. Five rules
were demoted and several rescoped.

| corpus | before | after |
|---|---|---|
| shadcn/ui | 9.6% | **0.03%** |
| tailwindcss.com | 32.7% | **3.27%** |
| cal.com | 4.5% | **0.68%** |

Detection was re-checked afterwards, so the improvement isn't just a weaker tool — a generic
landing page still trips **seven** refusing rules at once.

Still true: the `rarely_legitimate` calls are judgments, not measurements. They're the first
thing to audit if a rule ever refuses code you wanted. And `buzzword-copy` can still fire on
prose inside a code comment.

## Credit

The vocabulary in this space was established by other people. Undercoat's rules describe
patterns named by [impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0),
[Taste Skill](https://www.tasteskill.dev/), web-taste, and Anthropic's frontend-design
skill. See `NOTICE`.

Undercoat's contribution isn't the list. It's the moment — refusing at the write, before the
file exists.

## Try it

Install it, point it at your next idea, and watch what it stops.

Then tell me what it got wrong. A rule that refuses code you wanted is worth more than ten
that fire correctly — it's the only way the floor gets honest.

Apache-2.0. See `LICENSE` and `NOTICE`.
