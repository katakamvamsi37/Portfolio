import json
import html
from pathlib import Path
import streamlit as st

BASE = Path(__file__).parent
DATA_FILE = BASE / "data" / "portfolio.json"
ASSETS = BASE / "assets"

st.set_page_config(
    page_title="Joel Darla | Data Engineer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_data
def load_data():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

data = load_data()
profile = data["profile"]

def esc(value):
    return html.escape(str(value or ""))

def badges(items):
    return "".join(f'<span class="badge">{esc(x)}</span>' for x in items)

st.markdown(
    """
<style>
:root {--card:rgba(17,31,52,.75);--text:#eef6ff;--muted:#9eb0c6;--accent:#63e6be;--accent2:#74c0fc;--line:rgba(255,255,255,.10)}
html{scroll-behavior:smooth}
[data-testid="stAppViewContainer"]{background:radial-gradient(circle at 12% 8%,rgba(55,178,255,.13),transparent 27rem),radial-gradient(circle at 88% 18%,rgba(99,230,190,.10),transparent 28rem),linear-gradient(180deg,#07111f 0%,#091626 55%,#07111f 100%)}
[data-testid="stHeader"]{background:transparent}[data-testid="stSidebar"]{display:none}.block-container{max-width:1180px;padding-top:2rem;padding-bottom:4rem}p,li{color:var(--muted);line-height:1.7}a{text-decoration:none!important}
.top{display:flex;justify-content:space-between;gap:1rem;align-items:center;padding:.7rem 0 2.1rem}.brand{font-weight:850;letter-spacing:.08em;color:var(--text)}.nav{display:flex;gap:1rem;flex-wrap:wrap}.nav a{color:var(--muted)!important;font-size:.9rem}
.hero{padding:3rem 0 2.3rem}.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:.42rem .72rem;color:var(--accent);background:rgba(99,230,190,.06);font-size:.82rem;font-weight:750}.hero h1{color:var(--text);font-size:clamp(3rem,8vw,6.2rem);line-height:.93;letter-spacing:-.055em;margin:.8rem 0}.role{font-size:clamp(1.4rem,4vw,2.15rem);color:var(--accent2);font-weight:700}.copy{max-width:760px;color:var(--muted);font-size:1.08rem;line-height:1.8;margin-top:.8rem}
.cta-row{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1.4rem}.cta,.plink{display:inline-flex;padding:.72rem 1rem;border-radius:10px;border:1px solid var(--line);font-weight:750}.cta.primary{background:linear-gradient(135deg,var(--accent),#8ce99a);color:#04131a!important;border-color:transparent}.cta.secondary,.plink{color:var(--text)!important;background:rgba(255,255,255,.035)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem;margin:2rem 0}.stat,.card,.project,.about{border:1px solid var(--line);background:var(--card);border-radius:18px}.stat{padding:1.1rem}.sv{font-size:1.45rem;color:var(--text);font-weight:850}.sl{font-size:.78rem;color:var(--muted)}
.space{height:4rem}.k{color:var(--accent);font-size:.77rem;font-weight:850;letter-spacing:.16em;text-transform:uppercase}.h{color:var(--text);font-size:2.05rem;font-weight:850;letter-spacing:-.035em;margin:.3rem 0 1rem}
.about-grid{display:grid;grid-template-columns:1.35fr .65fr;gap:1rem}.about{padding:1.35rem}.quote{color:var(--text);font-size:1.18rem;font-weight:650;line-height:1.65}.mini-label{color:var(--accent2);font-size:.72rem;font-weight:850;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.4rem}
.badge{display:inline-block;padding:.36rem .6rem;margin:.18rem .18rem .18rem 0;border-radius:999px;border:1px solid var(--line);background:rgba(116,192,252,.06);color:#cfe9ff;font-size:.75rem}
.project{padding:1.5rem;margin-bottom:1rem;background:linear-gradient(135deg,rgba(116,192,252,.055),transparent 40%),var(--card)}.phead{display:flex;justify-content:space-between;gap:1rem}.ptitle{color:var(--text);font-size:1.35rem;font-weight:850}.psub{color:var(--accent);font-size:.82rem;margin:.2rem 0 .7rem}.pnum{color:rgba(255,255,255,.23);font-size:2.1rem;font-weight:900}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem}.mini{border:1px solid var(--line);border-radius:13px;padding:.9rem 1rem;background:rgba(255,255,255,.018)}.links{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1rem}.plink{font-size:.82rem;padding:.52rem .72rem}
.card{padding:1.25rem;height:100%;margin-bottom:.8rem}.ctitle{color:var(--text);font-weight:850;margin-bottom:.75rem}.timeline{border-left:1px solid var(--line);margin-left:.45rem;padding-left:1.4rem}.ti{position:relative;padding-bottom:1.4rem}.ti:before{content:'';position:absolute;width:9px;height:9px;border-radius:50%;background:var(--accent);left:-1.68rem;top:.45rem;box-shadow:0 0 0 5px rgba(99,230,190,.08)}.trole{color:var(--text);font-weight:850}.tmeta{color:var(--accent2);font-size:.82rem;margin:.2rem 0 .6rem}
.contact{text-align:center;border:1px solid var(--line);border-radius:24px;padding:3rem 1.3rem;background:radial-gradient(circle at 50% 0%,rgba(99,230,190,.11),transparent 18rem),rgba(22,39,64,.92)}.contact h2{color:var(--text);font-size:2.3rem;margin:.4rem 0}.footer{text-align:center;color:#718399;font-size:.78rem;margin-top:3rem}
@media(max-width:800px){.stats{grid-template-columns:repeat(2,1fr)}.grid2,.about-grid{grid-template-columns:1fr}.top{align-items:flex-start;flex-direction:column}.hero{padding-top:2rem}}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="top"><div class="brand">{esc(profile["name"]).upper()} · DATA</div><div class="nav"><a href="#about">About</a><a href="#projects">Projects</a><a href="#skills">Skills</a><a href="#experience">Experience</a><a href="#contact">Contact</a></div></div>',
    unsafe_allow_html=True,
)

hero_buttons = ['<a class="cta primary" href="#projects">Explore my work ↓</a>']
if profile.get("github"):
    hero_buttons.append(f'<a class="cta secondary" href="{esc(profile["github"])}" target="_blank">GitHub ↗</a>')
if profile.get("linkedin"):
    hero_buttons.append(f'<a class="cta secondary" href="{esc(profile["linkedin"])}" target="_blank">LinkedIn ↗</a>')

st.markdown(
    f'<div class="hero"><div class="pill">● {esc(profile["availability"])}</div><h1>{esc(profile["name"])}</h1><div class="role">{esc(profile["role"])}</div><div class="copy">{esc(profile["tagline"])}</div><div class="cta-row">{"".join(hero_buttons)}</div></div>',
    unsafe_allow_html=True,
)

stats_html = "".join(
    f'<div class="stat"><div class="sv">{esc(item["value"])}</div><div class="sl">{esc(item["label"])}</div></div>'
    for item in data["stats"]
)
st.markdown(f'<div class="stats">{stats_html}</div>', unsafe_allow_html=True)

st.markdown('<div id="about" class="space"></div><div class="k">About</div><div class="h">Engineering data that people can trust.</div>', unsafe_allow_html=True)
focus = sum(data["skills"].values(), [])[:7]
st.markdown(
    f'<div class="about-grid"><div class="about"><div class="quote">{esc(profile["summary"])}</div></div><div class="about"><div class="mini-label">Current focus</div>{badges(focus)}<div class="mini-label" style="margin-top:1rem">Location</div><div style="color:var(--text);font-weight:750">{esc(profile["location"])}</div></div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div id="projects" class="space"></div><div class="k">Selected work</div><div class="h">Projects built around real data problems.</div><p>These are example projects. Replace them later by editing <code>data/portfolio.json</code>.</p>', unsafe_allow_html=True)
for project in data["projects"]:
    impact = "".join(f'<li>{esc(value)}</li>' for value in project["impact"])
    links = []
    if project.get("github"):
        links.append(f'<a class="plink" href="{esc(project["github"])}" target="_blank">Source code ↗</a>')
    if project.get("demo"):
        links.append(f'<a class="plink" href="{esc(project["demo"])}" target="_blank">Live demo ↗</a>')
    st.markdown(
        f'<div class="project"><div class="phead"><div><div class="ptitle">{esc(project["title"])}</div><div class="psub">{esc(project["subtitle"])}</div></div><div class="pnum">{esc(project["number"])}</div></div><p>{esc(project["description"])}</p>{badges(project["technologies"])}<div class="grid2"><div class="mini"><div class="mini-label">Problem</div><div style="color:var(--muted)">{esc(project["problem"])}</div></div><div class="mini"><div class="mini-label">Solution</div><div style="color:var(--muted)">{esc(project["solution"])}</div></div></div><div class="mini" style="margin-top:1rem"><div class="mini-label">Outcome</div><ul>{impact}</ul></div><div class="links">{"".join(links)}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown('<div id="skills" class="space"></div><div class="k">Technical toolkit</div><div class="h">Tools I use to move data from source to insight.</div>', unsafe_allow_html=True)
skill_groups = list(data["skills"].items())
for i in range(0, len(skill_groups), 2):
    cols = st.columns(2)
    for j, (name, items) in enumerate(skill_groups[i:i+2]):
        with cols[j]:
            st.markdown(f'<div class="card"><div class="ctitle">{esc(name)}</div>{badges(items)}</div>', unsafe_allow_html=True)

st.markdown('<div id="experience" class="space"></div><div class="k">Experience</div><div class="h">Where I have applied my skills.</div>', unsafe_allow_html=True)
experience_html = []
for exp in data["experience"]:
    bullets = "".join(f'<li>{esc(value)}</li>' for value in exp["highlights"])
    experience_html.append(f'<div class="ti"><div class="trole">{esc(exp["role"])} · {esc(exp["company"])}</div><div class="tmeta">{esc(exp["period"])} · {esc(exp["location"])}</div><ul>{bullets}</ul></div>')
st.markdown(f'<div class="timeline">{"".join(experience_html)}</div>', unsafe_allow_html=True)

st.markdown('<div class="space"></div>', unsafe_allow_html=True)
left, right = st.columns(2)
with left:
    st.markdown('<div class="k">Certifications</div><div class="h" style="font-size:1.55rem">Continuous learning</div>', unsafe_allow_html=True)
    for cert in data["certifications"]:
        st.markdown(f'<div class="card"><div class="ctitle">{esc(cert["name"])}</div><div style="color:var(--muted)">{esc(cert["issuer"])} · {esc(cert["year"])}</div></div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="k">Education</div><div class="h" style="font-size:1.55rem">Academic foundation</div>', unsafe_allow_html=True)
    for edu in data["education"]:
        st.markdown(f'<div class="card"><div class="ctitle">{esc(edu["degree"])}</div><div style="color:var(--muted)">{esc(edu["school"])} · {esc(edu["period"])}</div></div>', unsafe_allow_html=True)

st.markdown('<div id="contact" class="space"></div>', unsafe_allow_html=True)
contact_buttons = []
if profile.get("linkedin"):
    contact_buttons.append(f'<a class="cta primary" href="{esc(profile["linkedin"])}" target="_blank">Connect on LinkedIn ↗</a>')
if profile.get("github"):
    contact_buttons.append(f'<a class="cta secondary" href="{esc(profile["github"])}" target="_blank">View GitHub ↗</a>')
if profile.get("email"):
    contact_buttons.append(f'<a class="cta secondary" href="mailto:{esc(profile["email"])}">Email me</a>')

st.markdown(
    f'<div class="contact"><div class="k">Contact</div><h2>Let’s build something useful with data.</h2><p>Interested in data engineering, lakehouse platforms, pipelines, or analytics engineering? Let’s connect.</p><div class="cta-row" style="justify-content:center">{"".join(contact_buttons)}</div></div><div class="footer">Built with Streamlit · Edit content in data/portfolio.json</div>',
    unsafe_allow_html=True,
)

resume_file = str(profile.get("resume_file", "")).strip()
if resume_file and (ASSETS / resume_file).exists():
    st.download_button(
        "Download Resume",
        data=(ASSETS / resume_file).read_bytes(),
        file_name=resume_file,
        mime="application/pdf",
        use_container_width=True,
    )
