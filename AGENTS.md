<!-- Generated from patterns.json by build.py. Do not edit by hand. -->

# Undercoat

The invisible layer that keeps AI-built interfaces from looking AI-built.

This file is the floor. It will not make an interface beautiful. It exists to stop one
looking machine-made. Every rule below is a documented tell of machine-made
interfaces. A rule refuses a write only when its match means one thing and almost
nobody wants that thing on purpose; everything else advises.

On tools that support hooks, the `block` rules are enforced at the write and the file
never lands. Everywhere else, this file is all there is, so read it and honour it.

## Do not write these

Patterns that mean one thing and that almost nobody wants on purpose. On Claude Code these are refused at the write, and the file will not be created until they are gone.

### ai-purple

The purple-to-violet gradient is the single strongest tell of machine-made UI. Models reach for it because it sits under thousands of SaaS landing pages in the training data.

**Instead:** One flat color chosen for this project. If you want depth, use spacing and type weight, not a gradient.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`, `**/*.css`, `**/*.scss`*

### ai-purple-hex

These are the exact hex values models default to for 'primary'. Seeing one hardcoded means the color was inherited, not chosen.

**Instead:** Define your own value. Any deliberate hue beats the one that arrived by default.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`, `**/*.css`, `**/*.scss`*

### rainbow-gradient

A three-stop gradient is decoration with no informational job. It is the 'make it look exciting' reflex.

**Instead:** One color, or a two-stop gradient with a reason. Excitement comes from contrast, not from hue count.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### tinted-shadow

A colored shadow is a glow with extra steps. It is the most-copied way to make a button look special without deciding anything.

**Instead:** Neutral shadow, or none. If the element needs to stand out, change its size, weight or position.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### gradient-on-root

A gradient across the whole page background is the default 'premium' move and it fights every piece of content placed on it.

**Instead:** A flat background. Let the content carry the interest.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### default-sans-inter

Inter is the default of defaults. It is not a bad typeface; it is the one chosen when nobody chose.

**Instead:** Pick a face with a point of view and commit to it. Name it in the project's own styles.

*Applies to: `**/*.css`, `**/*.scss`, `**/*.tsx`, `**/*.jsx`, `**/*.html`*

### neon-glow

A zero-offset glow is decoration standing in for hierarchy. Neon-on-dark with glowing borders is the v0 and Cursor signature.

**Instead:** Offset shadows describe light and depth. If the element needs emphasis, give it size, weight or space.

*Applies to: `**/*.css`, `**/*.html`, `**/*.jsx`, `**/*.scss`, `**/*.svelte`, `**/*.tsx`, `**/*.vue`*

### ambient-blur-orb

The giant blurred color blob floating behind the hero is pure decoration, and it is in every generated landing page written since 2023.

**Instead:** Delete it. If the background needs interest, use a real edge, a rule, or a change of surface.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### gradient-border-trick

The one-pixel gradient wrapper faking a glowing border is a copied trick, not a design decision.

**Instead:** A real border in one color. If the edge needs emphasis, change the surface inside it.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### z-index-nuke

A four-digit z-index means the stacking order was never designed, only fought with.

**Instead:** Fix the stacking context. If two things overlap, one of them is in the wrong place in the tree.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`, `**/*.css`, `**/*.scss`*

### generic-cta

A call to action that says nothing about what happens next is the same button on ten thousand pages.

**Instead:** Name the action in the user's words. 'Start a 14-day trial', 'See it running', 'Read the first chapter'.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### vague-headline

A headline that could sit on any product's page tells the reader nothing and wastes the only line they are guaranteed to read.

**Instead:** Say what this specific thing does for this specific person, in their words.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### buzzword-copy

Marketing vocabulary with no referent. These words survive because they are hard to disagree with, which is exactly why they persuade nobody.

**Instead:** Replace the adjective with the fact underneath it. 'Seamless' usually means 'no configuration'. Say that.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### lorem-ipsum

Placeholder copy in a real component means the content question was skipped, and skipped content is where generic layouts come from.

**Instead:** Write the actual sentence, even badly. Real copy changes the layout you need.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`, `**/*.md`*

### placeholder-copy

Template scaffolding that shipped. It signals that nobody read the page after it was generated.

**Instead:** Write the real thing, or delete the element until you have it.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### fake-testimonial

Invented social proof is worse than none. Placeholder names rendered as testimonial text are the clearest sign the section was generated wholesale.

**Instead:** Real quotes with real names, or remove the section until you have them.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### ai-implementation-comment

A comment apologising for the code being a sketch. It is the most direct evidence possible that generated output shipped unread.

**Instead:** Either finish it or delete the branch. A comment is not a substitute for a decision.

*Applies to: `**/*.html`, `**/*.js`, `**/*.jsx`, `**/*.svelte`, `**/*.ts`, `**/*.tsx`, `**/*.vue`*

### stock-placeholder-image

Hot-linked stock photography is a placeholder that ships. It breaks offline, leaks referrers, and guarantees someone else's site looks identical.

**Instead:** A real asset in the repo, or an honest empty state. A blank space beats a stranger's photograph.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`, `**/*.css`, `**/*.scss`*

### generated-avatar-service

Procedurally generated avatars are the visual equivalent of Lorem ipsum, and they make every user look like a placeholder.

**Instead:** Initials on a flat background, or the user's real image. Both beat a robot face.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### emoji-as-icon

The rocket, the lock, the sparkles. An emoji standing in for an icon system is one of the most legible tells there is, and it renders differently on every platform your reader might be on.

**Instead:** A real icon set, or no icon. If the label needs an emoji to carry meaning, the label needs rewriting.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### hero-italic-emphasis

One word of the headline set in italic, usually in a different color, is a template move. It is emphasis applied because the layout felt flat, not because that word carries more weight than the others. Checked against 4,516 files of hand-written UI from shadcn/ui, tailwindcss.com and cal.com: it appears zero times.

**Instead:** Let the sentence do it. If a word matters more, the headline probably needs rewriting rather than restyling.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### stat-row

The wall of impressive figures. 12,000+ / 99.9% / 40+ with no source and no date, sitting in a row because the section looked empty without them. Measured against 4,722 files of hand-written UI from shadcn/ui, tailwindcss.com and cal.com: 0 hits.

**Instead:** One number you can stand behind, with where it came from. If you cannot source it, the section is better without it.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### marketing-eyebrow

A one-word label above a centered heading above a centered sentence. It is the same block repeated down the page, and the label never tells the reader anything the heading did not. Measured against 4,722 files of hand-written UI from shadcn/ui, tailwindcss.com and cal.com: 1 hit.

**Instead:** Delete the label. If the heading needs a preamble to make sense, rewrite the heading.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### hero-pill-badge

The little pill announcing a feature nobody asked about yet. It is the default way to fill the space above a headline. Measured against 4,722 files of hand-written UI from shadcn/ui, tailwindcss.com and cal.com: 0 hits.

**Instead:** Start with the headline. If the announcement matters, it deserves more than a chip.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### testimonial-triplet

Three testimonials of near-identical length, side by side, each with a gray circle where a face should be. Real praise does not arrive in matching sizes. Measured against 4,722 files of hand-written UI from shadcn/ui, tailwindcss.com and cal.com: 0 hits.

**Instead:** One real quote you can attribute, or none. Three invented ones read as three invented ones.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### card-icon-tile

The tinted rounded tile with an outline icon in it, once per feature card. It is decoration standing in for a picture nobody had. Measured across 4,722 files: 2 hits.

**Instead:** Drop the tile. An icon can sit inline at text size, or the card can lead with its heading.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### pricing-most-popular

The badge on the middle tier, almost always the one you want sold. It is a template slot rather than an observation about what people actually buy. Measured against 4,722 files of hand-written UI from shadcn/ui, tailwindcss.com and cal.com: 0 hits.

**Instead:** If a plan genuinely suits most teams, say who it suits and why, in words.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### invented-faq

Four questions nobody asked, written to fill a section. A real FAQ comes from support tickets and reads nothing like this. Measured against 4,722 files of hand-written UI from shadcn/ui, tailwindcss.com and cal.com: 1 hit.

**Instead:** Answer the questions people actually send you, and put them where they get asked.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### repeated-cta

The identical call to action at the top and again at the bottom. Saying it twice in the same words does not make it more persuasive, it makes the page feel padded. Measured against 4,722 files of hand-written UI from shadcn/ui, tailwindcss.com and cal.com: 0 hits.

**Instead:** If the second one is worth having, it should offer something the first did not.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### min-read-byline

The reading time under the headline. It arrived with content marketing and it tells the reader how long to feel guilty for, not whether the piece is worth their time. Measured across 5,739 files of hand-written code: 0 hits.

**Instead:** Nothing. If the piece is long, the scrollbar already says so.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`, `**/*.md`, `**/*.mdx`*

### related-reading

The block of things you did not ask for at the bottom of the thing you did. It exists to raise time on page rather than to help. Measured across 5,739 files of hand-written code: 0 hits.

**Instead:** Link the one piece that genuinely follows on, in the sentence where it belongs.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### tip-callout

A gray box with a friendly label, holding a sentence that was not important enough for the paragraph above it. Measured across 5,739 files of hand-written code: 0 hits.

**Instead:** Put it in the prose, or cut it. A box is not an argument for keeping something.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`, `**/*.md`, `**/*.mdx`*

### checkmark-benefit-list

The lucide check, repeated down a list of things that are all equally good. It is what fills a card when nobody ranked the features. Measured across 5,739 files of hand-written code: 0 hits.

**Instead:** Drop the ticks. A plain list reads faster, and the ones that matter can be said in a sentence.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

### setup-checklist

The onboarding checklist with the first item already ticked, so the bar looks like progress. It is a gamified to-do list bolted onto a screen that had nothing to show. Measured across 4,722 files of hand-written code: 0 hits.

**Instead:** Put the single next action where the empty content would have been, and drop the rest until it matters.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

## Think twice about these

Real tells that fail one of the two blocking tests. Either the match is a proxy that also catches legitimate code, or the pattern is sometimes wanted deliberately. These do not block anything.

### tailwind-default-blue

Tailwind's mid-blue as the primary brand color is the framework default wearing a brand's clothes.

**Instead:** Define one project color and use it. Any deliberate hue beats the palette you got for free.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Plenty of real products deliberately use a mid-blue, and Tailwind's is a reasonable one.*

### default-grey-body

Light gray body text is the most common accessibility failure in generated UI, and it reads as washed out rather than subtle. Dark-mode variants are excluded, since dark:text-gray-400 is correct.

**Instead:** Body copy at full strength. If something should recede, reduce its size or weight, not its contrast.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Correct on dark surfaces. tailwindcss.com pairs text-gray-400 with text-white, and a regex cannot see the background color, so this advises.*

### pure-black-on-white

Pure black on pure white is harsher than print ever was and reads as untuned.

**Instead:** Near-black around #14141a. The eye reads it as black and it stops vibrating.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`, `**/*.css`, `**/*.scss`*

*Advises rather than blocks: Legitimate in high-contrast and print-like designs, so it advises rather than refuses.*

### hardcoded-hex-in-markup

Arbitrary hex values scattered through markup means there is no palette. Every color was decided separately and none of them relate.

**Instead:** Put the value in your theme and use the token. If it is worth using twice it is worth naming.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: One-off arbitrary colors are sometimes correct, so this advises.*

### system-font-only

The system stack alone is the absence of a typographic decision. It is fine for a tool and wrong for anything with a voice.

**Instead:** Choose a face for headings at least. One deliberate typeface changes the whole impression.

*Applies to: `**/*.css`, `**/*.scss`*

*Advises rather than blocks: The system stack is a legitimate choice for utilities and docs, so this advises.*

### all-bold

When everything is bold nothing is. Uniform heavy weight is what happens when hierarchy was never decided.

**Instead:** One or two weights doing different jobs. Let size and space carry the rest.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: Counting occurrences in a window is a proxy, and a dense component can trip it legitimately.*

### eyebrow-label

The tiny uppercase letterspaced kicker above every heading is a template convention, repeated until it means nothing.

**Instead:** Say it in the heading, or drop it. A label that adds no information is decoration.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Genuinely correct in editorial layouts, so it advises rather than refuses.*

### giant-hero-text

Enormous hero type is how generated pages signal importance without earning it. At this size the words usually say less than the space they take.

**Instead:** Drop a step or two and give the line something worth reading.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Deliberate editorial and display work uses these sizes properly.*

### default-heavy-shadow

The default heavy drop shadow on every card is how generated UI signals 'this is a component'. Real interfaces use shadow sparingly and at one or two depths.

**Instead:** A hairline border, or a shadow one or two steps lighter. Reserve the heaviest depth for things that actually float.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: shadow-xl is the right depth for modals, popovers and dropdowns that genuinely float.*

### glassmorphism

Frosted glass on everything is the current default for 'make it look premium'. Applied without a reason it flattens hierarchy and wrecks contrast.

**Instead:** Solid surfaces. If you want separation, use a different background value or real spacing.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`, `**/*.css`, `**/*.scss`*

*Advises rather than blocks: Correct for translucent navs, modal scrims and overlays. Observed on sticky headers in cal.com; blocking it would break standard practice.*

### uniform-bubbly-radius

Oversized rounding on every surface is a named tell. When cards, buttons and inputs share one bubbly radius, nothing reads as a different kind of thing.

**Instead:** Pick one radius for the project and vary it deliberately: tighter on inputs, looser on containers.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: rounded-3xl is a legitimate deliberate choice for soft design systems.*

### ring-decoration

Rings used as decoration rather than focus states dilute the one signal keyboard users depend on.

**Instead:** Keep ring for focus. For emphasis use a border or a background change.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Rings have legitimate decorative uses, and the focus-state exclusion here is a rough proxy.*

### border-and-shadow

A border and a shadow on the same element is two solutions to one problem, applied because neither was chosen.

**Instead:** Pick one. Borders suit dense interfaces, shadows suit floating things.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Some design systems legitimately use both together.*

### exclamation-marketing

Exclamation marks in interface copy are enthusiasm applied to a reader who did not ask for it.

**Instead:** Say it flat. If the news is good the reader will supply the feeling.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Genuine exclamations exist and this cannot tell them apart.*

### trusted-by-logos

The logo strip is a template slot. When it appears before there are real customers, it is a slot filled rather than a claim made.

**Instead:** Only if the logos are real and you have permission. Otherwise the space is better empty.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Entirely legitimate once the logos are real.*

### powered-by-ai-copy

Saying it is AI-powered describes the implementation, not the benefit. It is the first thing generated copy reaches for.

**Instead:** Say what it does for the reader. They do not care what is behind it.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Correct and necessary for products where the AI is the point.*

### sparkles-icon

The sparkle icon is the universal shorthand for 'this bit is AI'. It arrived with the first wave of AI products and has meant nothing since.

**Instead:** An icon that describes the action. If the action is 'generate', draw generating.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: A legitimate choice for genuinely magical actions, so it advises.*

### three-card-grid

Three equal-weight cards in a row is the default answer to 'show some features', repeated for every section. It gives every item the same importance, which usually means none were ranked.

**Instead:** Decide which one matters most and let the layout say so.

*Applies to: `**/page.tsx`, `**/page.jsx`, `**/index.html`, `**/App.tsx`*

*Advises rather than blocks: Named by four catalogs, but grid-cols-3 fires constantly on legitimate tables and galleries.*

### default-container-width

Every generated page is 1280px centered. It is not wrong, it is the width nobody chose, and it makes unrelated products feel like the same site.

**Instead:** Pick a measure from your type. Long-form reading wants far narrower; a dashboard usually wants wider.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: A perfectly reasonable width that many real projects pick deliberately.*

### everything-centered

Centered everything is the layout equivalent of a shrug. Centered text is hard to read in paragraphs and removes the left edge the eye scans against.

**Instead:** Left-align body copy. Center only short, deliberate lines.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Centered sections are correct for short hero content.*

### nested-cards

Everything wrapped in a card, then cards inside cards. Three levels of container, because hierarchy was never decided.

**Instead:** One container. Use spacing to group what is inside it.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: Requires structural nesting analysis; this regex is a shallow proxy that will miss most real cases.*

### hero-icon-circle

The big circled icon floating above a centered heading is a named tell. The decoration is sized larger than the message it introduces.

**Instead:** Lose the circle. If the icon earns its place, let it sit inline at text scale.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: Needs relative sizing and position to detect properly; also fires on large avatars.*

### full-height-hero

A hero that fills the viewport before saying anything is the template default. It costs the reader a scroll to learn nothing.

**Instead:** Size the section to its content. Let the next thing peek above the fold.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: Legitimate for genuine full-screen experiences.*

### sticky-everything

More than one sticky element and the viewport belongs to the chrome rather than the content.

**Instead:** One sticky thing at most. Everything else can scroll away.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: Counting in a window is a proxy and can trip on legitimate layouts.*

### status-chip-soup

Badges everywhere is what happens when nothing was prioritized. Every state gets a chip and none of them read.

**Instead:** Keep the one or two states a user acts on. Put the rest in text.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: Detection requires counting chips per view; one Badge is fine, nine is the problem.*

### cramped-padding

Interfaces generated without a spacing decision default to too tight. Padding is the cheapest quality signal there is.

**Instead:** Start generous and remove. If it looks empty, the type is probably too small.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: p-0 and p-1 are correct constantly in dense and nested layouts.*

### magic-spacing

Arbitrary pixel values mean there is no spacing scale. Every gap was decided in isolation.

**Instead:** Use the scale. If nothing on the scale fits, the scale is wrong and should change.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: One-off values are sometimes exactly right.*

### small-touch-target

A button under about 44px is hard to hit and reads as an afterthought.

**Instead:** Give interactive targets room. Pad the hit area even when the icon stays small.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: Small buttons inside dense toolbars are a legitimate pattern.*

### uniform-fade-in

The same fade-in on every element is motion applied as a finish rather than to show a relationship. It delays everything and explains nothing.

**Instead:** Animate what changes meaning: a thing arriving, a state flipping. Leave the rest still.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: A single deliberate entrance animation is fine; this cannot tell one from forty.*

### bounce-easing

Overshoot easing on interface motion reads as playful once and cheap thereafter.

**Instead:** Ease-out for things entering, ease-in for things leaving. No overshoot on anything a user waits for.

*Applies to: `**/*.css`, `**/*.scss`, `**/*.tsx`, `**/*.jsx`*

*Advises rather than blocks: Correct for genuinely playful products and for attention-seeking affordances like scroll cues.*

### decorative-pulse

A pulsing element that is not loading anything is an animation looking for a job.

**Instead:** Keep pulse for skeletons and live indicators. Everything else can hold still.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: Entirely correct for loading skeletons, which is where most matches will be.*

### slow-transition

Transitions over about half a second stop reading as responsive and start reading as lag.

**Instead:** 150ms to 300ms for most interface motion. Reserve longer for things genuinely traveling a distance.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: Long durations are right for deliberate, large movements.*

### dark-mode-reflex

Dark by default is the most common reflex in generated interfaces. Dark is a real choice for some products and a costume for most.

**Instead:** Decide. If the product is used in daylight by people reading text, light is probably right.

*Applies to: `**/layout.tsx`, `**/App.tsx`, `**/index.html`, `**/*.css`, `**/*.scss`*

*Advises rather than blocks: Whether dark is a reflex or a decision cannot be read from a class name.*

### inline-style-attribute

Inline styles bypass whatever system exists, which means the value was chosen locally and relates to nothing.

**Instead:** Put it in the stylesheet or the theme. If it is truly dynamic, that is the exception, not the habit.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: Genuinely dynamic values must be inline.*

### important-override

An !important is a note saying the cascade was lost. It is usually a symptom of a system that was never designed.

**Instead:** Fix the specificity. If you are overriding a third-party style, scope it instead.

*Applies to: `**/*.css`, `**/*.scss`, `**/*.tsx`, `**/*.jsx`, `**/*.ts`, `**/*.js`, `**/*.vue`, `**/*.svelte`*

*Advises rather than blocks: Overriding third-party CSS sometimes leaves no alternative.*

### placeholder-as-label

A placeholder used as the only label disappears the moment someone types, and takes the field's meaning with it.

**Instead:** A real label above the field. Placeholders are for examples, not names.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: The negative lookaheads are a crude proxy for 'has a label' and will misfire on wrapped components.*

### hardcoded-neutral-ramp

The reflex you fall into once the obvious colors are closed off. Close one default gray and a model reaches for the next, which is how you can tell nobody picked it.

**Instead:** Choose a neutral and say why. A gray with a little warmth or a little blue in it reads as a decision; the stock ramp reads as none.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`, `**/*.css`, `**/*.scss`*

*Advises rather than blocks: Hardcoding these hexes is common in real code: 20 hits across 4,722 files, spread through production views rather than one palette file. It advises instead of refusing. Note this supersedes the old hardcoded-slate rule, which blocked only because slate happened to be rarer in the sample.*

### nothing-here-yet

The heading that states the obvious. The screen is already empty; saying so uses the one line where you could have said what to do instead.

**Instead:** Lead with the action or the reason. 'Connect a repository to see releases' does the same job and moves someone along.

*Applies to: `**/*.tsx`, `**/*.jsx`, `**/*.vue`, `**/*.svelte`, `**/*.html`*

*Advises rather than blocks: 6 hits across 4,722 files. Real apps do write 'No results found', and sometimes that is the honest thing to say, so it advises rather than refuses.*

## When a rule is wrong

Some projects genuinely need a banned pattern. A brand really is purple, a client
really did specify that face. Mute the rule for the project rather than working around
it:

```json
// .undercoat.local.json  (local, not committed)
{ "off": ["ai-purple"] }
```

Muting is per-rule and per-project on purpose. There is no per-line escape hatch,
because an agent could write one and grant itself permission.
