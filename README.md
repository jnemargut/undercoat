# Undercoat

**Sends your coding agent back to try again when it reaches for the same generic page it builds for everyone else.**

You've seen this page. Everyone has.

![A generated landing page with thirteen Undercoat rules caught on it, eight of which send it back. The labels include a purple gradient, a vague headline, a generic call to action, an emoji standing in for an icon, and an invented testimonial](assets/what-it-refuses.png)

Your agent didn't pick the purple, or the headline, or the button that says Get Started.
None of that was a decision. It's just what comes out when nothing tells the model
otherwise, because it's the average of every landing page it ever read.

You can tell it not to. That works for about forty files, and then it forgets.

Undercoat doesn't ask. It reads each file as the agent goes to save it, and if that stuff is
in there, the save doesn't go through. The agent gets told which rule caught it and what to do
instead, so it writes a different version.

![Undercoat turning a write back, the agent retrying, and the second attempt going through](assets/refusal.gif)

Nothing halts. The agent reads the message, has another go, and carries on with the rest of
the job. You are not asked to approve anything, and you never see the first version.

## Install it

```bash
git clone https://github.com/jnemargut/undercoat
./undercoat/install.sh /path/to/your/project
```

That's the whole setup. The script tells you every change it makes as it makes it, backs up
your settings first, and `./undercoat/uninstall.sh` puts it all back.

If you'd rather have it on for everything you build without setting it up each time:

```bash
./undercoat/install.sh --global
```

Then `touch .undercoat.off` in any project you'd rather it left alone.

There's no account and no API key. It's Python and a couple of markdown files, same as
[decision-kit](https://github.com/jnemargut/decision-kit).

## What actually changes

![The page that got sent back, beside the one that got written, same product and same brief](assets/before-after.png)

Undercoat didn't design the page on the right. It turned back the one on the left and named
the parts to think about again. The agent did the rest.

## How it works

![patterns.json feeding AGENTS.md, which advises everywhere, and hook.py, which turns writes back in Claude Code](assets/how-it-works.png)

You edit one file, `patterns.json`. Both halves come out of it.

**AGENTS.md** is plain markdown that most coding tools read on their own when they start a
task, so it works in Cursor, Codex, Copilot, Aider and a couple of dozen others. It can't
stop anything. It just tells the agent what to steer clear of.

**The hook** is the half with teeth, and it only works in Claude Code. It reads every file the
agent tries to save, before the file exists, and hands back a reason when it turns one down.

You get the advice everywhere and the redirect in Claude Code. If you've only got the first
one, nothing breaks.

It keeps an eye on shell commands too. An agent that can't use the save tool will happily
try `cat > file` instead, so Undercoat turns that down and points it back at the normal way.

## The rules

**76 of them. 35 send the file back to be rewritten, 41 leave a note and let it through.**

<details>
<summary><strong>The 35 that send it back</strong></summary>

**Color**

| Rule | What it catches |
|---|---|
| `ai-purple` | Purple, violet or indigo gradient stops |
| `ai-purple-hex` | The seven hex values models reach for when they mean "primary" |
| `rainbow-gradient` | Gradients with three or more color stops |
| `tinted-shadow` | Colored shadows like shadow-purple-500/50 |
| `gradient-on-root` | A gradient on the page background itself |

**Shadows, blur and shape**

| Rule | What it catches |
|---|---|
| `neon-glow` | Zero-offset box shadows used as a glow |
| `ambient-blur-orb` | The blurred color blob floating behind a hero |
| `gradient-border-trick` | A 1px gradient wrapper faking a glowing border |
| `z-index-nuke` | Four-digit z-index values |

**Type**

| Rule | What it catches |
|---|---|
| `default-sans-inter` | Inter set as the typeface |
| `hero-italic-emphasis` | One italic word inside a hero headline |

**The template page**

| Rule | What it catches |
|---|---|
| `stat-row` | Three or more round, unsourced numbers in a row |
| `marketing-eyebrow` | Section labels like Features, Benefits, How it works |
| `hero-pill-badge` | A small rounded chip sitting above the hero headline |
| `testimonial-triplet` | Three quote cards in a row, each with a circle avatar and a job title |
| `card-icon-tile` | An icon in a tinted rounded square, on a card or above an empty state |
| `pricing-most-popular` | A Most popular badge on a pricing tier |
| `invented-faq` | A Frequently asked questions block |
| `repeated-cta` | The same button wording repeated down the page |
| `min-read-byline` | An X min read estimate in a byline |
| `related-reading` | A Related reading or You might also like block |
| `tip-callout` | A Pro tip or Worth knowing callout box |
| `checkmark-benefit-list` | Three or more identical tick icons beside short benefit lines |
| `setup-checklist` | A numbered Finish setting up checklist card |

**Words on the page**

| Rule | What it catches |
|---|---|
| `generic-cta` | Buttons saying Get Started, Learn More, Click Here |
| `vague-headline` | Headlines like "Transform Your Workflow" |
| `buzzword-copy` | Seamless, cutting-edge, revolutionary, game-changing |
| `lorem-ipsum` | Placeholder latin still sitting in a real component |
| `placeholder-copy` | Your Company, Text goes here, Replace this |
| `fake-testimonial` | John Doe or Acme Inc used as social proof |
| `ai-implementation-comment` | Comments like "// In a real implementation this would" |
| `hardcoded-relative-time` | Three or more X ago timestamps written into the markup |

**Pictures and icons**

| Rule | What it catches |
|---|---|
| `stock-placeholder-image` | Hot-linked Unsplash, placehold.co or picsum URLs |
| `generated-avatar-service` | Procedural avatars from dicebear or ui-avatars |
| `emoji-as-icon` | An emoji doing an icon's job, alone in a tile or beside text in a heading or button |

</details>

<details>
<summary><strong>The 41 it only mentions</strong></summary>

Every one of these is a real tell, but each is also sometimes exactly right, so Undercoat
says something and gets out of your way.

**Color**

| Rule | What it catches |
|---|---|
| `tailwind-default-blue` | bg-blue-500 or bg-blue-600 as the brand color |
| `hardcoded-neutral-ramp` | Tailwind's slate, zinc, gray or stone ramps hardcoded as the palette |
| `default-grey-body` | Light gray body text on a light background |
| `pure-black-on-white` | Pure #000 text |
| `hardcoded-hex-in-markup` | Arbitrary hex values inline in class names |
| `status-stripe-accent` | Two or more cards tagged with different colored left-edge stripes |
| `traffic-light-status` | Green, amber and red all used together as status colors |

**Shadows, blur and shape**

| Rule | What it catches |
|---|---|
| `glassmorphism` | Frosted glass via backdrop-blur |
| `default-heavy-shadow` | shadow-xl and shadow-2xl on ordinary cards |
| `uniform-bubbly-radius` | rounded-3xl on every surface |
| `ring-decoration` | Focus rings used as ornament |
| `border-and-shadow` | A border and a shadow doing the same job |

**Type**

| Rule | What it catches |
|---|---|
| `system-font-only` | The system stack as the only typographic choice |
| `all-bold` | font-bold repeated until nothing stands out |
| `eyebrow-label` | The tiny uppercase letterspaced kicker, in utility classes or plain CSS |
| `giant-hero-text` | text-7xl and above |

**Words on the page**

| Rule | What it catches |
|---|---|
| `danger-zone-heading` | A section headed Danger Zone |
| `exclamation-marketing` | Exclamation marks in interface copy |
| `trusted-by-logos` | A "Trusted by" logo strip |
| `powered-by-ai-copy` | Copy selling the tech instead of the benefit |

**Pictures and icons**

| Rule | What it catches |
|---|---|
| `sparkles-icon` | The sparkle or wand icon standing in for AI |

**Layout and spacing**

| Rule | What it catches |
|---|---|
| `three-card-grid` | Three equal cards as a page's main content |
| `nested-cards` | A card inside a card |
| `everything-centered` | Whole sections center-aligned |
| `hero-icon-circle` | A big circled icon floating above a heading |
| `full-height-hero` | min-h-screen on the first thing anyone sees |
| `default-container-width` | max-w-7xl mx-auto, the width nobody picked |
| `sticky-everything` | More than one sticky element fighting for the screen |
| `status-chip-soup` | Four or more badges in one view |
| `cramped-padding` | p-0 and p-1 where something needed room |
| `magic-spacing` | Arbitrary pixel spacing off the scale |
| `small-touch-target` | Buttons under roughly 44px |
| `placeholder-as-label` | A placeholder doing the job of a label |
| `nothing-here-yet` | A No X yet or Nothing here yet empty state heading |

**Movement**

| Rule | What it catches |
|---|---|
| `uniform-fade-in` | The same entrance animation on everything |
| `bounce-easing` | Overshoot easing on interface motion |
| `decorative-pulse` | animate-pulse on something that isn't loading |
| `slow-transition` | Transitions over half a second |

**Everything else**

| Rule | What it catches |
|---|---|
| `dark-mode-reflex` | A near-black page background by default |
| `inline-style-attribute` | Values set inline, going round the system |
| `important-override` | !important |

</details>

### Why some rules send it back and some only leave a note

Every rule has to pass two tests before it's allowed to stop a file.

**Is there only one explanation for it?** A hot-linked Unsplash URL in shipped code is only
ever one thing. Three cards in a row isn't: sometimes that's a template, and sometimes it's
just three cards.

**Would anyone ever choose it on purpose?** Nobody means to ship a photo that loads off
someone else's server. Plenty of good pages have three cards.

A rule needs a yes to both. Unsplash gets a yes to both, so `stock-placeholder-image` sends
the file back. Three cards gets a no to both, so `three-card-grid` leaves a note and the file
goes through.

Whether the pattern is ugly doesn't come into it. The only thing I ask is whether sending a
file back could ever be the wrong call. If it could, the rule doesn't get to.

## When a rule gets it wrong

Turn it off for that project:

```json
// .undercoat.local.json
{ "off": ["ai-purple"] }
```

That switches off one rule in one project. There's no way to skip a single line, and that's
deliberate: if there were, the agent could write the skip itself and wave its own work through.

If the same rule turns the same file back three times, Undercoat gives up and tells you,
instead of letting the agent loop.

## What it can't do

It reads text, and that's all it reads. So:

- **Layout is invisible to it.** Four identical sections stacked down a page sail straight
  through, and honestly that's where most of the "AI made this" feeling comes from.
- **It can't see color in context.** Gray text is unreadable on white and completely fine
  on black, and the file looks the same either way.
- **It can't tell writing about a pattern from using one.** A style guide that mentions
  `from-purple-600` gets pulled up for it, so turn Undercoat off in those repos.

If you want something that looks at the finished page and tells you it's boring, you want a
design reviewer. Undercoat is built to work alongside one, not replace it.

## Credit

Most of these patterns were worked out by other people first. The rules here describe things
named by [impeccable](https://github.com/pbakaus/impeccable),
[Taste Skill](https://github.com/Leonxlnx/taste-skill) and
[Anthropic's frontend-design skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design),
plus a handful of write-ups cataloging AI design tells. There's a fuller note in `NOTICE`.

What's different here is when it happens. Other tools tell the agent what to do before it
starts, or check your code once it's finished. This one catches the file on its way to disk
and sends the agent back to write a better one.

## Try it

Point it at whatever you're building next and see what it sends back.

Then tell me what it got wrong. A rule that turns back something you actually wanted is worth
more to me than ten that fire correctly.

Apache-2.0. See `LICENSE` and `NOTICE`.
