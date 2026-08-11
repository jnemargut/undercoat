# Undercoat

**Stops your coding agent from writing the same generic-looking page every time.**

You have seen it. Purple gradient, three cards in a row, a button that says Get Started.

Your agent writes that page because it is the most common page in everything it learned.
Telling it not to works for a while, then it forgets.

Undercoat does not ask. It reads the file while the agent is saving it, and if the file has
that stuff in it, the save fails.

![Undercoat refusing a write, then the agent retrying and getting it right](assets/refusal.gif)

The agent reads the message and tries again. You are not interrupted, and you never see the
first version.

## Install it

```bash
git clone https://github.com/jnemargut/undercoat
./undercoat/install.sh /path/to/your/project
```

That is the whole setup. The script prints every change it makes, backs up your settings
first, and `./undercoat/uninstall.sh` puts everything back.

If you want it on for everything you build, without setting it up each time:

```bash
./undercoat/install.sh --global
```

Then turn it off for any single project with `touch .undercoat.off`.

No account, no API key, no npm package. Just Python and markdown files, the same as
[decision-kit](https://github.com/jnemargut/decision-kit).

## How it works

![patterns.json feeds two halves: AGENTS.md which advises everywhere, and hook.py which refuses in Claude Code](assets/how-it-works.png)

You edit one file, `patterns.json`. Everything else comes from it.

**AGENTS.md** is a plain markdown file that most coding tools read automatically when they
start a task. It tells the agent what to avoid. It works in Cursor, Codex, Copilot, Aider
and about two dozen others. It cannot stop anything, it can only advise.

**The hook** is the part that actually refuses. It works in Claude Code, and it checks every
file the agent tries to save before the file exists.

You get the advice everywhere. You get the refusal in Claude Code. Nothing breaks if you
only have the first one.

It also watches shell commands, because an agent that cannot use the save tool will often
try `cat > file` instead. Undercoat blocks that route and points it back at the normal tool.

## What it catches

**56 rules. 20 refuse the file, 36 leave a note and let it through.**

<details>
<summary><strong>The 20 it refuses</strong></summary>

**Colour**

| Rule | What it catches |
|---|---|
| `ai-purple` | Purple, violet or indigo gradient stops |
| `ai-purple-hex` | The seven hex values models pick for "primary" |
| `rainbow-gradient` | Gradients with three or more colour stops |
| `tinted-shadow` | Coloured shadows like shadow-purple-500/50 |
| `gradient-on-root` | A gradient applied to the page background itself |

**Shadows, blur and shape**

| Rule | What it catches |
|---|---|
| `neon-glow` | Zero-offset box shadows used as a glow |
| `ambient-blur-orb` | The blurred colour blob floating behind a hero |
| `gradient-border-trick` | A 1px gradient wrapper faking a glowing border |
| `z-index-nuke` | Four-digit z-index values |

**Type**

| Rule | What it catches |
|---|---|
| `default-sans-inter` | Inter declared as the typeface |

**Words on the page**

| Rule | What it catches |
|---|---|
| `generic-cta` | Buttons that say Get Started, Learn More, Click Here |
| `vague-headline` | Headlines like "Transform your workflow" |
| `buzzword-copy` | Seamless, cutting-edge, revolutionary, game-changing |
| `lorem-ipsum` | Placeholder latin left in a real component |
| `placeholder-copy` | Your Company, Text goes here, Replace this |
| `fake-testimonial` | John Doe or Acme Inc shown as social proof |
| `ai-implementation-comment` | Comments like "// In a real implementation this would" |

**Pictures and icons**

| Rule | What it catches |
|---|---|
| `stock-placeholder-image` | Hot-linked Unsplash, placehold.co or picsum URLs |
| `generated-avatar-service` | Procedural avatars from dicebear or ui-avatars |
| `emoji-as-icon` | Emoji used as an icon inside a heading or button |

</details>

<details>
<summary><strong>The 36 it only mentions</strong></summary>

These are real tells, but each one is sometimes the right call, so Undercoat says something
and gets out of the way.

**Colour**

| Rule | What it catches |
|---|---|
| `tailwind-default-blue` | bg-blue-500 or bg-blue-600 as the brand colour |
| `default-grey-body` | Light grey body text on a light background |
| `pure-black-on-white` | Pure #000 text |
| `hardcoded-hex-in-markup` | Arbitrary hex values inline in class names |

**Shadows, blur and shape**

| Rule | What it catches |
|---|---|
| `glassmorphism` | Frosted glass via backdrop-blur |
| `default-heavy-shadow` | shadow-xl and shadow-2xl on ordinary cards |
| `uniform-bubbly-radius` | rounded-3xl applied to every surface |
| `ring-decoration` | Focus rings used as ornament |
| `border-and-shadow` | A border and a shadow doing the same job |

**Type**

| Rule | What it catches |
|---|---|
| `system-font-only` | The system font stack as the only typographic choice |
| `all-bold` | font-bold repeated until nothing stands out |
| `eyebrow-label` | The tiny uppercase letterspaced kicker above a heading |
| `giant-hero-text` | text-7xl and above |

**Words on the page**

| Rule | What it catches |
|---|---|
| `exclamation-marketing` | Exclamation marks in interface copy |
| `trusted-by-logos` | A "Trusted by" logo strip |
| `powered-by-ai-copy` | Copy that sells the tech rather than the benefit |

**Pictures and icons**

| Rule | What it catches |
|---|---|
| `sparkles-icon` | The sparkle or wand icon as shorthand for AI |

**Layout and spacing**

| Rule | What it catches |
|---|---|
| `three-card-grid` | Three equal cards as a page's main content |
| `nested-cards` | A card inside a card |
| `everything-centered` | Whole sections centre-aligned |
| `hero-icon-circle` | A large circled icon floating above a heading |
| `full-height-hero` | min-h-screen on the first thing a reader sees |
| `default-container-width` | max-w-7xl mx-auto, the width nobody chose |
| `sticky-everything` | More than one sticky element fighting for the screen |
| `status-chip-soup` | Four or more badges in one view |
| `cramped-padding` | p-0 and p-1 where breathing room was needed |
| `magic-spacing` | Arbitrary pixel spacing off the scale |
| `small-touch-target` | Buttons under roughly 44px |
| `placeholder-as-label` | A placeholder used as the only label |

**Movement**

| Rule | What it catches |
|---|---|
| `uniform-fade-in` | The same entrance animation on everything |
| `bounce-easing` | Overshoot easing on interface motion |
| `decorative-pulse` | animate-pulse on something that is not loading |
| `slow-transition` | Transitions over half a second |

**Everything else**

| Rule | What it catches |
|---|---|
| `dark-mode-reflex` | A near-black page background as the default |
| `inline-style-attribute` | Values set inline, bypassing the system |
| `important-override` | !important |

</details>

### Why some refuse and some do not

A rule only refuses a file if two things are true: the thing it looks for means one thing
and nothing else, and almost nobody would want it on purpose.

A hot-linked Unsplash photo in shipped code is basically never right, so that one refuses.
Three cards in a row is a real tell, but plenty of pages legitimately have three cards, so
that one just leaves a note.

That is the whole rule for deciding. It is not about how many people agree the pattern is
bad. It is about whether stopping you would ever be the wrong call.

## When a rule gets it wrong

Turn it off for that project:

```json
// .undercoat.local.json
{ "off": ["ai-purple"] }
```

One rule at a time, one project at a time. There is no way to skip a single line, on
purpose. If there were, the agent could write that skip itself and let its own work through.

If a rule refuses the same file three times, Undercoat stops and hands the problem to you
instead of letting the agent spin.

## What it cannot do

It reads text. That is the whole mechanism, and it has real limits:

- **It cannot see layout.** Four identical sections stacked down the page will pass
  everything. That is where "looks AI-made" really lives.
- **It cannot see colour in context.** Grey text is unreadable on white and fine on black.
  Same words in the file, opposite answer.
- **It cannot tell writing about a pattern from using one.** A style guide that mentions
  `from-purple-600` gets flagged for it. Turn Undercoat off in those repos.

For anything needing to actually look at the rendered page, use a design reviewer. Undercoat
is meant to sit alongside one, not replace it.

## Does it get in the way?

It was tested against shadcn/ui, tailwindcss.com and cal.com, about 4,700 files of good
hand-written code. It now refuses **0.3% of them**, and the ones it still catches are mostly
fair. The first version refused a third of tailwindcss.com, which is how five rules got
demoted and several got narrowed.

The rules that refuse are judgment calls about what nobody would want on purpose. If one of
them stops code you meant to write, that judgment was wrong and worth telling me about.

## Credit

Other people worked out most of these patterns first. Undercoat's rules describe things
named by [impeccable](https://github.com/pbakaus/impeccable), [Taste Skill](https://github.com/Leonxlnx/taste-skill), and
[Anthropic's frontend-design skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design), plus a
handful of independent write-ups on AI design tells. See `NOTICE`.

The list is not the interesting part. The interesting part is when it happens: at the save,
before the file exists.

## Try it

Install it, point it at whatever you build next, and see what it stops.

Then tell me what it got wrong. A rule that refuses something you wanted is worth more than
ten that fire correctly.

Apache-2.0. See `LICENSE` and `NOTICE`.
