#!/usr/bin/env python3
"""Rebuild the README images from one source of truth.

Everything the README shows is generated here so the pictures cannot drift from
the rules. Run it after changing patterns.json:

    python3 assets/src/build_assets.py

Needs headless Chrome and Pillow. Writes into assets/.
"""
import json, pathlib, re, subprocess, sys, importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "assets"
WORK = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("/tmp/undercoat-assets")
WORK.mkdir(parents=True, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# The demo pages are deliberately full of the things Undercoat refuses, so the
# hook must not police the directory it renders them in.
(WORK / ".undercoat.off").write_text("")


# ---------------------------------------------------------------- rule lookup
def rules():
    return json.loads((ROOT / "patterns.json").read_text())["rules"]


def hits_on(path: pathlib.Path):
    """Every rule that actually fires on a file, in patterns.json order."""
    spec = importlib.util.spec_from_file_location("hook", ROOT / "hook.py")
    hook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hook)
    txt = path.read_text()
    out = []
    for r in rules():
        if not hook.rule_applies_to(r, path.name):
            continue
        if re.compile(r["match"]).search(txt):
            out.append((r["id"], r["severity"]))
    return out


# ------------------------------------------------------------- the slop page
FONT = ('<link href="https://fonts.googleapis.com/css2?'
        'family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">')

SLOP_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
.page{font-family:Inter,system-ui,sans-serif;background:#13111c;width:962px}
.hero{position:relative;overflow:hidden;padding:54px 48px 44px;text-align:center;
      background:linear-gradient(135deg,#6366f1 0%,#8b5cf6 48%,#c084fc 100%)}
.orb{position:absolute;width:300px;height:300px;border-radius:9999px;filter:blur(70px);
     background:rgba(255,255,255,.30);top:-130px;left:-70px}
.orb2{position:absolute;width:260px;height:260px;border-radius:9999px;filter:blur(70px);
      background:rgba(217,70,239,.45);bottom:-150px;right:-50px}
.kick{position:relative;font-size:11px;font-weight:700;letter-spacing:.2em;
      text-transform:uppercase;color:rgba(255,255,255,.82);margin-bottom:16px}
.hero h1{position:relative;font-size:44px;font-weight:800;color:#fff;line-height:1.13;
         letter-spacing:-.025em}
.sub{position:relative;font-size:15px;color:rgba(255,255,255,.86);line-height:1.6;
     max-width:520px;margin:16px auto 0}
.btns{position:relative;display:flex;gap:14px;justify-content:center;margin-top:26px}
.cta{background:#a5b4fc;color:#312e81;border:none;border-radius:9999px;padding:12px 24px;
     font-size:14px;font-weight:700;font-family:Inter;box-shadow:0 0 34px rgba(165,180,252,.85)}
.cta2{background:rgba(255,255,255,.20);color:#fff;border:1px solid rgba(255,255,255,.36);
      border-radius:9999px;padding:12px 24px;font-size:14px;font-weight:700;font-family:Inter}
.trustwrap{position:relative;margin-top:34px}
.trust{font-size:10.5px;font-weight:700;letter-spacing:.19em;text-transform:uppercase;
       color:rgba(255,255,255,.72)}
.logos{display:flex;gap:16px;justify-content:center;margin-top:14px}
.logo{width:74px;height:19px;border-radius:5px;background:rgba(255,255,255,.34);display:block}
.cards{display:grid;grid-template-columns:1fr 1fr 1fr;gap:22px;padding:52px 48px}
.card{position:relative;background:rgba(255,255,255,.07);backdrop-filter:blur(18px);
      border:1px solid rgba(255,255,255,.12);border-radius:26px;padding:28px 24px;
      text-align:center;box-shadow:0 26px 52px -14px rgba(0,0,0,.7)}
.ico{width:66px;height:66px;border-radius:9999px;background:linear-gradient(135deg,#8b5cf6,#6366f1);
     display:flex;align-items:center;justify-content:center;font-size:29px;margin:0 auto 16px;
     box-shadow:0 0 30px rgba(139,92,246,.6)}
.card h3{font-size:17px;font-weight:700;color:#fff;margin-bottom:9px}
.card p{font-size:13.5px;color:#94a3b8;line-height:1.65}
.quote{margin:8px 48px 52px;background:rgba(255,255,255,.07);backdrop-filter:blur(18px);
       border:1px solid rgba(255,255,255,.12);border-radius:26px;padding:30px;text-align:center;
       box-shadow:0 26px 52px -14px rgba(0,0,0,.7)}
.quote p{font-size:17px;color:#e2e8f0;font-style:italic;line-height:1.6}
.who{position:relative;display:flex;gap:11px;align-items:center;justify-content:center;margin-top:18px}
.av{width:42px;height:42px;border-radius:9999px;background:linear-gradient(135deg,#a855f7,#6366f1)}
.who b{font-size:13.5px;color:#fff;display:block}
.who span{font-size:12px;color:#94a3b8}
"""

# {a:...} slots take the annotation attributes; empty for the plain slop page.
SLOP_BODY = """
<div class="page">
  <div class="hero"{a_hero}>
    <div class="orb"></div><div class="orb2"></div>
    <div class="kick"{a_kick}>Powered by AI</div>
    <h1{a_h1}>Transform Your Workflow<br>With AI-Powered Insights</h1>
    <p class="sub"{a_sub}>Seamless, cutting-edge collaboration for modern teams. Everything you
       need to take your productivity to the next level.</p>
    <div class="btns"{a_btns}>
      <button class="cta">Get Started &rarr;</button><button class="cta2">Learn More</button>
    </div>
    <div class="trustwrap"{a_trust}>
      <div class="trust">Trusted by teams at</div>
      <div class="logos"><i class="logo"></i><i class="logo"></i><i class="logo"></i><i class="logo"></i></div>
    </div>
  </div>
  <div class="cards">
    <div class="card"><div class="ico"{a_ico}>&#128640;</div><h3>Lightning Fast</h3>
      <p>Blazing fast performance that scales seamlessly with your growing team.</p></div>
    <div class="card"><div class="ico">&#128274;</div><h3>Enterprise Ready</h3>
      <p>Best-in-class security and compliance built in from day one.</p></div>
    <div class="card"{a_glass}><div class="ico">&#10024;</div><h3>AI Powered</h3>
      <p>Revolutionary intelligence that learns how your team actually works.</p></div>
  </div>
  <div class="quote">
    <p>&ldquo;This product completely transformed how our team operates. Game-changing.&rdquo;</p>
    <div class="who"{a_who}><div class="av"></div>
      <div style="text-align:left"><b>Jane Doe</b><span>CEO at Acme Inc</span></div></div>
  </div>
</div>
"""

BLANK = {k: "" for k in ("a_hero", "a_kick", "a_h1", "a_sub", "a_btns", "a_trust",
                         "a_ico", "a_glass", "a_who")}


def write_slop():
    p = WORK / "slop.html"
    p.write_text(f"<!DOCTYPE html><html><head>{FONT}<style>{SLOP_CSS}"
                 "body{margin:0;background:#13111c}</style></head><body>"
                 + SLOP_BODY.format(**BLANK) + "</body></html>")
    return p


# ------------------------------------------------------- the page that passes
CLEAN = """<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Archivo,system-ui,sans-serif;background:#f7f5f0;color:#17161a;width:962px}
.nav{display:flex;align-items:center;padding:17px 40px;border-bottom:1px solid #e4e0d8;background:#f7f5f0}
.brand{font-weight:800;font-size:15.5px}
.nl{margin-left:auto;display:flex;gap:22px;font-size:13.5px;color:#57534b}
.nl b{font-weight:600;color:#17161a}
.hero{padding:52px 40px 44px;background:#f7f5f0}
h1{font-size:52px;font-weight:900;line-height:1.02;letter-spacing:-.035em;max-width:15ch}
.lede{font-size:16px;color:#403d38;line-height:1.65;max-width:52ch;margin-top:20px}
.act{display:flex;gap:18px;align-items:center;margin-top:26px}
.go{background:#17161a;color:#fff;border:none;border-radius:7px;padding:12px 19px;
    font-size:14.5px;font-weight:600;font-family:Archivo}
.alt{font-size:14.5px;font-weight:600;border-bottom:1.5px solid #17161a;padding-bottom:1px}
.fine{font-size:12.5px;color:#78736a;margin-top:11px}
.strip{display:grid;grid-template-columns:1.15fr 1fr 1fr;border-top:1px solid #e4e0d8;background:#fff}
.st{padding:26px 30px;border-right:1px solid #e4e0d8}
.st:last-child{border-right:none}
.lab{font-family:'JetBrains Mono',monospace;font-size:10.5px;color:#8a857c;margin-bottom:12px}
.big{font-size:40px;font-weight:800;letter-spacing:-.03em;line-height:1}
.big s{font-size:17px;font-weight:600;text-decoration:none;color:#57534b}
.st b{font-size:14.5px;display:block;margin-bottom:5px}
.st p{font-size:13px;color:#57534b;line-height:1.6;margin-top:9px}
.quote{background:#17161a;color:#f2efe9;padding:34px 40px}
.quote p{font-size:19px;line-height:1.5;max-width:44ch;font-weight:500}
.quote .who{font-family:'JetBrains Mono',monospace;font-size:11.5px;color:#a5a099;margin-top:16px}
</style></head><body>
<div class="nav"><div class="brand">Meridian</div>
  <div class="nl"><span>How it reads your team</span><b>Pricing</b><b>Sign in</b></div></div>
<div class="hero">
  <h1>Find out what your team already decided</h1>
  <p class="lede">Meridian reads your threads, docs and tickets, then answers one question:
     has anyone settled this already? Usually somebody has.</p>
  <div class="act"><button class="go">Search your last 90 days</button>
    <span class="alt">See a sample report</span></div>
  <div class="fine">Free while it indexes. No card, no call.</div>
</div>
<div class="strip">
  <div class="st"><div class="lab">WHAT IT COSTS YOU NOW</div>
    <div class="big">4.2<s>h</s></div><b>a week, spent re-deciding</b>
    <p>The average across twelve teams we measured before building this. Most of it goes on
       questions with an answer already sitting in a thread from March.</p></div>
  <div class="st"><div class="lab">WHERE IT LOOKS</div>
    <b>Slack, Notion, Linear</b>
    <p>Read-only. It never posts, and it never writes anything back.</p></div>
  <div class="st"><div class="lab">WHAT YOU GET</div>
    <b>The decision, and who made it</b>
    <p>With the thread it came from, so you can argue with the right person.</p></div>
</div>
<div class="quote">
  <p>It found a pricing decision from 2024 that three of us had been quietly contradicting
     all quarter.</p>
  <div class="who">Priya Raman &middot; Head of Platform, Kettle</div>
</div>
</body></html>"""


def write_clean():
    p = WORK / "clean.html"
    p.write_text(CLEAN)
    return p


# ------------------------------------------------------------------- renderer
def trim_bottom(im, bg=(11, 14, 20), pad=18):
    """Drop trailing rows that are all background, so nothing floats in a void."""
    px = im.convert("RGB").load()
    last = im.height - 1
    while last > 0:
        row = range(0, im.width, 7)
        if any(abs(px[x, last][i] - bg[i]) > 8 for x in row for i in range(3)):
            break
        last -= 1
    return im.crop((0, 0, im.width, min(im.height, last + pad)))


def shot(html: pathlib.Path, png: pathlib.Path, w: int, h: int, scale: int = 2):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    f"--screenshot={png}", f"--window-size={w},{h}", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", f"file://{html}"],
                   capture_output=True)
    if not png.exists():
        raise SystemExit(f"chrome produced nothing for {html}")
    return png


# --------------------------------------------------- annotated "what it refuses"
ANNO_CSS = """
body{margin:0;background:#0b0e14;font-family:Inter,system-ui,sans-serif}
.title{padding:20px 24px 14px;display:flex;align-items:baseline;gap:12px}
.title h2{font-size:19px;font-weight:800;color:#fafaf9}
.title span{font-size:13px;color:#8b95a8}
.outer{position:relative}
.frame{margin-left:24px;width:962px;border-radius:14px;overflow:hidden;
       box-shadow:0 30px 70px -20px rgba(0,0,0,.8)}
[data-rule]{position:relative;outline:2px solid #f43f5e;outline-offset:5px;border-radius:3px}
[data-rule]::after{content:attr(data-rule);position:absolute;top:-11px;left:-5px;
  transform:translateY(-100%);font:700 11px 'SF Mono',Menlo,monospace;white-space:nowrap;
  background:#9f1239;color:#fff;padding:3px 8px;border-radius:4px;z-index:9}
[data-rule][data-side="r"]::after{left:auto;right:-5px}
[data-rule][data-side="b"]::after{top:auto;bottom:-11px;transform:translateY(100%)}
[data-rule][data-side="in"]::after{top:10px;left:10px;transform:none}
[data-rule][data-side="br"]::after{top:auto;bottom:-11px;left:auto;right:-5px;transform:translateY(100%)}
[data-note]{position:relative;outline:2px solid #f59e0b;outline-offset:5px;border-radius:3px}
[data-note]::after{content:attr(data-note);position:absolute;top:-11px;right:-5px;
  transform:translateY(-100%);font:700 11px 'SF Mono',Menlo,monospace;white-space:nowrap;
  background:#b45309;color:#fff;padding:3px 8px;border-radius:4px;z-index:9}
[data-note][data-side="b"]::after{top:auto;bottom:-11px;transform:translateY(100%)}
[data-note][data-side="l"]::after{right:auto;left:-5px}
.side{position:absolute;left:1010px;top:0;width:266px}
.tot{font:800 42px Inter;line-height:1;color:#fafaf9}
.tot small{font:600 13px Inter;color:#8b95a8;display:block;margin-top:6px}
.key div{display:flex;align-items:center;gap:8px;font-size:12.5px;color:#c3cddf;margin-bottom:8px}
.sw{width:11px;height:11px;border-radius:3px}
.note{margin-top:18px;font-size:13px;line-height:1.7;color:#8b95a8;border-top:1px solid #263041;padding-top:14px}
.note b{color:#fecdd3}
"""

# Which element carries which rule box. Only rules that actually fire get one.
ANNO = {
    "a_hero":  ' data-rule="ai-purple-hex" data-side="in"',
    "a_kick":  ' data-note="powered-by-ai-copy"',
    "a_h1":    ' data-rule="vague-headline"',
    "a_sub":   ' data-rule="buzzword-copy" data-side="br"',
    "a_btns":  ' data-rule="generic-cta" data-side="b"',
    "a_trust": ' data-note="trusted-by-logos" data-side="b"',
    "a_ico":   ' data-rule="emoji-as-icon"',
    "a_glass": ' data-note="glassmorphism" data-side="b"',
    "a_who":   ' data-rule="fake-testimonial" data-side="br"',
}
# Fires on the file but has nothing to point at in a picture.
INVISIBLE = {"default-sans-inter": "the typeface", "neon-glow": "the glow around that button",
             "eyebrow-label": "the letterspaced caps", "hardcoded-neutral-ramp": "the greys"}


def write_annotated(fired):
    blocks = [i for i, s in fired if s == "block"]
    warns = [i for i, s in fired if s == "warn"]
    shown = {re.search(r'data-(?:rule|note)="([a-z0-9-]+)"', v).group(1) for v in ANNO.values()}
    missing = [i for i, _ in fired if i not in shown]
    unknown = [i for i in missing if i not in INVISIBLE]
    if unknown:
        raise SystemExit(f"rule fires but has no box and no explanation: {unknown}")

    bits = ", ".join(f"<b>{i}</b> for {INVISIBLE[i]}" for i in missing)
    body = SLOP_BODY.format(**ANNO)
    side = f"""<div class="side">
  <div class="tot">{len(blocks)}<small>rules refused this file</small></div>
  <div style="height:18px"></div>
  <div class="tot" style="font-size:28px;color:#fbbf24">{len(warns)}<small>more left a note</small></div>
  <div style="height:22px"></div>
  <div class="key">
    <div><span class="sw" style="background:#f43f5e"></span>Refused. It never gets written.</div>
    <div><span class="sw" style="background:#f59e0b"></span>Noted. Sometimes it's right.</div>
  </div>
  <div class="note">{len(missing)} more caught it that you can't see in a picture: {bits}.</div>
  <div class="note" style="border:none;padding-top:0">Nobody chose any of this. It's what turns
    up when nothing tells the model otherwise.</div>
</div>"""
    p = WORK / "annotated.html"
    p.write_text(f"<!DOCTYPE html><html><head>{FONT}<style>{SLOP_CSS}{ANNO_CSS}</style></head><body>"
                 '<div class="title"><h2>What Undercoat refuses to let your agent write</h2>'
                 '<span>Every box is a rule that actually fired on this file.</span></div>'
                 f'<div class="outer"><div class="frame">{body}</div>{side}</div>'
                 "</body></html>")
    return p


# ------------------------------------------------------------ before and after
def write_ba(n_block):
    word = {7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven"}.get(n_block, str(n_block))
    p = WORK / "ba.html"
    p.write_text(f"""<!DOCTYPE html><html><head>{FONT}<style>
body{{margin:0;background:#0b0e14;font-family:Inter,system-ui,sans-serif;width:1240px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px;padding:22px}}
.head{{display:flex;align-items:center;gap:12px;margin-bottom:12px}}
.head h3{{font-size:15.5px;font-weight:700;color:#fafaf9}}
.tag{{font:700 10.5px 'SF Mono',Menlo,monospace;letter-spacing:.08em;padding:4px 9px;border-radius:5px}}
.tag.no{{background:#4c0519;color:#fecdd3}}
.tag.yes{{background:#052e16;color:#bbf7d0}}
.shot{{border-radius:11px;overflow:hidden;border:1px solid #1e2735}}
.shot img{{display:block;width:100%}}
.cap{{font-size:13px;color:#8b95a8;line-height:1.65;margin-top:12px}}
</style></head><body><div class="grid">
<div><div class="head"><span class="tag no">REFUSED</span><h3>What the agent tried to save</h3></div>
  <div class="shot"><img src="slop.png"></div>
  <div class="cap">{word} rules sent this file back. Nobody chose the purple, the headline,
    the emoji icons or the fake quote. They are just what turns up by default.</div></div>
<div><div class="head"><span class="tag yes">WRITTEN</span><h3>What it saved instead</h3></div>
  <div class="shot"><img src="clean.png"></div>
  <div class="cap">Same product, same brief. Undercoat did not design this. It only refused the
    first version and told the agent which bits to rethink.</div></div>
</div></body></html>""")
    return p


# ------------------------------------------------------------------- diagram
def write_diagram(n_rules):
    p = WORK / "diagram.html"
    p.write_text(f"""<!DOCTYPE html><html><head>{FONT}<style>
*{{box-sizing:border-box}}
body{{margin:0;background:#0b0e14;font-family:Inter,system-ui,sans-serif;width:1000px;padding:22px 30px}}
.box{{border:1.5px solid #d97706;border-radius:11px;background:#1a1206;padding:16px;text-align:center}}
.box .n{{font:700 17px 'SF Mono',Menlo,monospace;color:#fbbf24}}
.box .s{{font-size:13px;color:#8b95a8;margin-top:5px}}
.arrow{{text-align:center;color:#4b5666;font-size:13px;margin:7px 0}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.c{{background:#11161f;border:1px solid #1e2735;border-radius:11px;padding:19px 21px}}
.c .k{{font:700 10.5px Inter;letter-spacing:.12em;color:#8b95a8;margin-bottom:9px}}
.c .t{{font:700 15.5px 'SF Mono',Menlo,monospace;color:#fafaf9;margin-bottom:9px}}
.c p{{font-size:13.5px;color:#c3cddf;line-height:1.6}}
.pill{{display:inline-block;margin-top:13px;font:700 10.5px Inter;letter-spacing:.09em;
      padding:5px 10px;border-radius:5px}}
.pill.a{{border:1px solid #35404f;color:#8b95a8}}
.pill.b{{background:#4c0519;color:#fecdd3}}
.foot{{text-align:center;font-size:13.5px;color:#8b95a8;margin-top:20px;line-height:1.75}}
.foot b{{color:#fbbf24}}
</style></head><body>
<div class="box"><div class="n">patterns.json</div>
  <div class="s">{n_rules} rules. The one file you edit.</div></div>
<div class="arrow">&#9660;</div>
<div class="two">
  <div class="c"><div class="k">THE PORTABLE HALF</div><div class="t">AGENTS.md</div>
    <p>Generated and committed. Plain markdown, read on task start by Claude Code, Codex,
       Cursor, Aider, Copilot, Gemini CLI, Windsurf, Zed and 20 more.</p>
    <span class="pill a">ADVISES &middot; WORKS EVERYWHERE</span></div>
  <div class="c"><div class="k">THE ENFORCEMENT HALF</div><div class="t">hook.py</div>
    <p>A PreToolUse hook. Reads Write, Edit, MultiEdit, NotebookEdit and Bash write routes
       before anything reaches disk.</p>
    <span class="pill b">SENDS BACK &middot; CLAUDE CODE</span></div>
</div>
<div class="foot">Enforcement is the upgrade, not the product.<br>
  On a tool without hooks it <b>falls back to advice rather than breaking</b>.</div>
</body></html>""")
    return p


# ----------------------------------------------------------------------- main
def main():
    from PIL import Image
    n_rules = len(rules())
    slop, clean = write_slop(), write_clean()
    fired = hits_on(slop)
    blocks = [i for i, s in fired if s == "block"]
    warns = [i for i, s in fired if s == "warn"]
    print(f"  slop.html fires {len(blocks)} block + {len(warns)} warn")
    for i, s in fired:
        print(f"     {s:5} {i}")
    if hits_on(clean):
        raise SystemExit(f"clean.html should pass but hits {hits_on(clean)}")
    print("  clean.html passes the floor")

    # what-it-refuses.png
    anno = write_annotated(fired)
    png = shot(anno, WORK / "anno.png", 1300, 1260)
    im = Image.open(png)
    im = trim_bottom(im.resize((1300, im.height // 2), Image.LANCZOS), pad=26)
    im.save(OUT / "what-it-refuses.png")
    print(f"  assets/what-it-refuses.png {im.size}")

    # before-after.png and .gif
    shot(slop, WORK / "slop.png", 962, 1035, 1)
    shot(clean, WORK / "clean.png", 962, 792, 1)
    ba = write_ba(len(blocks))
    png = shot(ba, WORK / "ba.png", 1240, 900)
    im = Image.open(png)
    im = im.resize((1240, im.height // 2), Image.LANCZOS)
    im = trim_bottom(im)
    im.save(OUT / "before-after.png")
    a = Image.open(WORK / "slop.png").convert("P", palette=Image.ADAPTIVE)
    b = Image.open(WORK / "clean.png").convert("P", palette=Image.ADAPTIVE)
    a.save(OUT / "before-after.gif", save_all=True, append_images=[b], duration=[1500, 2200], loop=0)
    print(f"  assets/before-after.png {im.size} and before-after.gif")

    # how-it-works.png
    png = shot(write_diagram(n_rules), WORK / "hiw.png", 1000, 405)
    Image.open(png).resize((1000, 405), Image.LANCZOS).save(OUT / "how-it-works.png")
    print("  assets/how-it-works.png (1000, 405)")
    print(f"\n  done. {n_rules} rules, {len(blocks)} sent this demo back.")


if __name__ == "__main__":
    main()
