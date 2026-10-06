"""Joel's single-page Streamlit portfolio.

Run: streamlit run streamlit_app.py
Requires Streamlit 1.65+. This file also works without the data/ folder.
Edit DEFAULT_DATA below, or use data/portfolio.json (takes precedence).
Export a standalone preview: python streamlit_app.py --export-html preview.html
All project data and pipeline runs are illustrative, local browser simulations.
"""

from __future__ import annotations

import argparse
import base64
import copy
import html
import json
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parent

# ── YOUR CONTENT: update these values; no layout changes are needed. ──────────
DEFAULT_DATA = {
    "schema_version": 2,
    "profile": {
        "name": "Joel Darla",
        "role": "Data Engineer",
        "location": "India",
        "availability": "Open to Data Engineering opportunities",
        "headline": ["From raw data.", "To real decisions."],
        "tagline": "I connect data sources, shape reliable datasets, and turn complex information into clear business insights.",
        "summary": "Data Engineer focused on Microsoft Fabric, Azure Data Factory, Azure Databricks, SQL, PySpark, and Power BI. I enjoy turning raw data into well-governed, reliable data products that help teams make faster decisions.",
        "email": "",
        "linkedin": "",
        "github": "",
        "resume_file": "",
    },
    "experience": [{
        "role": "Data Engineer",
        "company": "Ingenius Technologies and Consulting",
        "period": "June 2025 — Present",
        "location": "India · Hybrid",
        "highlights": [
            "Build and support data workflows for ingestion, transformation, validation, and analytics.",
            "Work with SQL, modern data platforms, pipeline orchestration, and reporting solutions.",
            "Translate data requirements into reliable datasets and repeatable engineering workflows.",
        ],
    }],
    "education": [{"degree": "B.Sc. Computer Science", "school": "Acharya Nagarjuna University", "period": "2019 — 2022"}],
    # Only add completed certifications with accurate titles and credential URLs.
    "certifications": [],
    "skills": {
        "Ingest & orchestrate": ["Azure Data Factory", "Microsoft Fabric", "ETL / ELT", "Data Pipelines"],
        "Transform & model": ["Azure Databricks", "PySpark", "Python", "SQL", "Delta Lake"],
        "Analyze & communicate": ["Power BI", "DAX", "Data Modelling", "Data Quality"],
        "Build & collaborate": ["Azure", "OneLake", "Git", "GitHub"],
    },
    "projects": [
        {
            "id": "powerbi", "number": "01", "category": "Business intelligence",
            "platform": "Power BI", "title": "Retail performance, in focus.",
            "summary": "A sales and margin reporting concept that brings scattered retail data into one consistent view for business teams.",
            "audience": "Sales leaders & business analysts",
            "problem": "Which regions drive revenue, and where is margin under pressure? Separate spreadsheets make that question difficult to answer consistently.",
            "approach": "Prepare source data, model sales at order-line level, and define reusable measures before building the report.",
            "value": "A shared view of sales and profit, with clear filters and consistent KPI definitions.",
            "tags": ["Power Query", "Star schema", "DAX", "Power BI"],
            "status": "Example architecture", "github": "", "demo": "",
            "stages": [
                {"title": "Source data", "subtitle": "Sales · costs · products", "icon": "database", "input": "SQL sales records and product / region reference files.", "action": "Bring together the records needed to explain sales and profitability.", "output": "Source tables with documented keys and reporting grain."},
                {"title": "Power Query", "subtitle": "Clean & standardize", "icon": "filter", "input": "Source tables with inconsistent types and labels.", "action": "Set data types, normalize labels, and resolve missing or invalid records.", "output": "Clean tables ready for relationships and measures."},
                {"title": "Star schema", "subtitle": "Facts + dimensions", "icon": "model", "input": "Clean sales, dates, regions, and products.", "action": "Connect SalesFact at order-line grain to Date, Region, and Product dimensions using one-to-many relationships.", "output": "A semantic model with unambiguous filtering paths."},
                {"title": "DAX measures", "subtitle": "Sales · profit · margin", "icon": "code", "input": "A validated semantic model.", "action": "Define Sales and Profit as sums; calculate Margin as Profit divided by Sales so totals remain correct.", "output": "Reusable measures evaluated in the current filter context."},
                {"title": "Power BI", "subtitle": "Explore & decide", "icon": "chart", "input": "The semantic model and business measures.", "action": "Publish a report with regional filtering and trends; configure access and refresh for the intended audience.", "output": "An interactive business view. The preview below uses synthetic data."},
            ],
            "controls": ["Validate relationships", "Reconcile KPI totals", "Configure refresh & access"],
            "reference": "https://learn.microsoft.com/en-us/power-bi/guidance/star-schema",
        },
        {
            "id": "databricks", "number": "02", "category": "Lakehouse engineering",
            "platform": "Azure Databricks", "title": "Raw events. Refined intelligence.",
            "summary": "An e-commerce lakehouse concept that separates original records, validated data, and business-ready aggregates.",
            "audience": "Data teams & downstream analysts",
            "problem": "Order files contain duplicate updates and incomplete records. Analysts need consistent, traceable tables they can trust.",
            "approach": "Organize Delta tables into Bronze, Silver, and Gold layers, with explicit quality rules and a quarantine path.",
            "value": "Traceable transformations, reusable business tables, and a clear place to investigate rejected records.",
            "tags": ["PySpark", "Delta Lake", "ADLS Gen2", "Unity Catalog"],
            "status": "Example architecture", "github": "", "demo": "",
            "stages": [
                {"title": "ADLS Gen2", "subtitle": "Order landing zone", "icon": "cloud", "input": "E-commerce order extracts arriving as JSON or CSV.", "action": "Land original files in a controlled storage location; capture file provenance during ingestion.", "output": "Source files ready for Databricks ingestion."},
                {"title": "Bronze", "subtitle": "Preserve raw records", "icon": "layers", "input": "New files from the landing zone.", "action": "Ingest into Delta tables and retain original fields plus ingestion metadata for replay and audit.", "output": "Raw history, including duplicates and records needing validation."},
                {"title": "Silver", "subtitle": "Validate & deduplicate", "icon": "shield", "input": "Raw Bronze records.", "action": "Keep the latest version of each order, cast types, and require an order ID, customer ID, and non-negative amount. Route invalid records to quarantine.", "output": "Validated order-level Delta data plus a quarantine table."},
                {"title": "Gold", "subtitle": "Model business tables", "icon": "model", "input": "Validated Silver records.", "action": "Aggregate order count and revenue by region for this sample. In a full build, publish business-grain facts and dimensions.", "output": "Curated datasets with consistent business definitions."},
                {"title": "SQL → BI", "subtitle": "Serve trusted data", "icon": "chart", "input": "Gold tables registered in the catalog.", "action": "Query through Databricks SQL and connect the curated dataset to Power BI or other analytics consumers.", "output": "Governed analytical access, subject to configured permissions."},
            ],
            "controls": ["Unity Catalog permissions", "Job monitoring", "Reject → quarantine"],
            "reference": "https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion",
        },
        {
            "id": "adf", "number": "03", "category": "Pipeline orchestration",
            "platform": "Azure Data Factory", "title": "Every load, under control.",
            "summary": "An incremental ingestion concept that copies changed records, validates the load, and advances its checkpoint only after success.",
            "audience": "Data platform & operations teams",
            "problem": "Repeated full loads waste work, while failed runs can leave the destination out of sync with the source.",
            "approach": "Capture a fixed old/new watermark window, copy the delta, then validate and merge it before committing the new checkpoint.",
            "value": "A repeatable load boundary, visible failures, and a safer retry path without skipping unprocessed data.",
            "tags": ["ADF pipelines", "Azure SQL", "ADLS Gen2", "Databricks"],
            "status": "Example architecture", "github": "", "demo": "",
            "stages": [
                {"title": "Azure SQL", "subtitle": "Read changed rows", "icon": "database", "input": "Source rows and the previous successful watermark.", "action": "Capture a new upper bound and select old < modified_at ≤ new. The source must reliably update modified_at; deletes need a separate strategy.", "output": "A bounded set of new and updated records."},
                {"title": "ADF Copy", "subtitle": "Parameterized activity", "icon": "workflow", "input": "The captured source window and dataset parameters.", "action": "Copy the selected records using linked services and the appropriate integration runtime.", "output": "A copy result with row counts and a run identifier."},
                {"title": "ADLS staging", "subtitle": "Isolate each run", "icon": "cloud", "input": "Rows copied for this run.", "action": "Persist the extraction in a run-specific path so that retries and validation have a stable input.", "output": "Staged data ready for validation and merge."},
                {"title": "Validate & merge", "subtitle": "Databricks task", "icon": "shield", "input": "The staged delta and target Delta table.", "action": "Check required keys and reconcile counts; merge by business key with deterministic deduplication. Abort on a failed validation.", "output": "An updated target only after successful validation and merge."},
                {"title": "Commit checkpoint", "subtitle": "Control-table update", "icon": "check", "input": "Successful downstream completion.", "action": "Update the stored watermark to the captured upper bound. On failure, retain the old watermark, log the run, and alert the owner.", "output": "The next run starts from the last successful boundary."},
            ],
            "controls": ["Schedule & parameters", "Managed identity / Key Vault", "Failure → log & alert"],
            "reference": "https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-overview",
        },
    ],
}

def esc(value):
    return html.escape(str(value or ""), quote=True)


def valid_link(value):
    """Allow real profile/project URLs, never generic placeholder homepages."""
    value = str(value or "").strip()
    parsed = urlparse(value)
    if parsed.scheme not in ("https", "http") or not parsed.netloc:
        return ""
    if parsed.netloc.lower().removeprefix("www.") in ("github.com", "linkedin.com") and parsed.path.strip("/") == "":
        return ""
    return value


def load_data():
    data = copy.deepcopy(DEFAULT_DATA)
    config = BASE / "data" / "portfolio.json"
    if config.exists():
        saved = json.loads(config.read_text(encoding="utf-8"))
        if not isinstance(saved, dict):
            raise ValueError("data/portfolio.json must contain a JSON object.")
        data["profile"].update(saved.get("profile", {}))
        for key in ("experience", "education", "certifications", "skills"):
            if key in saved:
                data[key] = saved[key]
        # Old version-1 profiles still load, with the three new example projects.
        if saved.get("schema_version") == 2 and "projects" in saved:
            data["projects"] = saved["projects"]
        if saved.get("schema_version") != 2:
            data["certifications"] = [c for c in data["certifications"] if not str(c.get("name", "")).lower().startswith("add your")]
    return data


ICONS = {
    "database": '<ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v14c0 4 14 4 14 0V5M5 12c0 4 14 4 14 0"/>',
    "cloud": '<path d="M7 18H5a4 4 0 0 1-1-7.9A7 7 0 0 1 17.5 8a5 5 0 0 1 1.5 10h-2M12 12v9m-3-3 3 3 3-3"/>',
    "layers": '<path d="m12 3 10 5-10 5L2 8Zm-9 10 9 5 9-5M3 18l9 5 9-5"/>',
    "workflow": '<rect x="2" y="8" width="6" height="8" rx="1"/><rect x="16" y="2" width="6" height="6" rx="1"/><rect x="16" y="16" width="6" height="6" rx="1"/><path d="M8 12h4V5h4m-4 7v7h4"/>',
    "chart": '<path d="M3 3v18h19M7 17v-5m5 5V7m5 10V3"/>',
    "filter": '<path d="M3 5h18l-7 8v7l-4-2v-5Z"/>',
    "code": '<path d="m8 6-6 6 6 6m8-12 6 6-6 6M14 3l-4 18"/>',
    "model": '<rect x="8" y="8" width="8" height="8" rx="1"/><path d="M12 2v6m0 8v6M2 12h6m8 0h6"/><circle cx="12" cy="2" r="1"/><circle cx="12" cy="22" r="1"/><circle cx="2" cy="12" r="1"/><circle cx="22" cy="12" r="1"/>',
    "shield": '<path d="m12 2 9 4v6c0 5-9 10-9 10S3 17 3 12V6Zm-4 10 3 3 5-6"/>',
    "check": '<path d="m5 12 4 4L20 5"/><path d="M21 12v8H3V3h12"/>',
    "arrow": '<path d="M5 12h14m-5-5 5 5-5 5"/>',
    "up": '<path d="M5 19 19 5M5 5h14v14"/>',
    "play": '<path d="m8 4 12 8-12 8Z"/>',
    "pause": '<path d="M8 4v16M16 4v16"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m3 5 9 8 9-8"/>',
    "download": '<path d="M12 3v12m-5-5 5 5 5-5M3 16v5h18v-5"/>',
}


def icon(name, cls=""):
    return f'<svg class="icon {esc(cls)}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS.get(name, ICONS["code"])}</svg>'


def chips(items):
    return "".join(f'<span class="chip">{esc(x)}</span>' for x in items)


def external_button(label, url, primary=False):
    url = valid_link(url)
    if not url:
        return ""
    return f'<a class="button {"primary" if primary else "secondary"}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}{icon("up")}</a>'


def resume_button(profile):
    name = str(profile.get("resume_file", "")).strip()
    if not name:
        return ""
    assets = (BASE / "assets").resolve()
    path = (assets / name).resolve()
    if not path.is_relative_to(assets) or not path.is_file() or path.suffix.lower() != ".pdf":
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'<a class="button secondary" download="{esc(path.name)}" href="data:application/pdf;base64,{encoded}">Download resume{icon("download")}</a>'


def hero_visual():
    return f'''<div class="hero-canvas" aria-label="Illustrative pipeline from source data through Azure Data Factory and Databricks to Power BI">
      <div class="canvas-heading"><span><span class="status-dot"></span> THE DATA JOURNEY</span><span class="mono">SOURCE → INSIGHT</span></div>
      <svg class="hero-wires" viewBox="0 0 500 370" aria-hidden="true"><defs><linearGradient id="wire"><stop stop-color="#95e6c5"/><stop offset="1" stop-color="#66b9e8"/></linearGradient></defs>
        <path class="hero-path" d="M145 70V115Q145 132 163 132H248V171M355 70V115Q355 132 337 132H248M248 218V267M248 311V350"/>
        <path class="hero-signal" d="M145 70V115Q145 132 163 132H248V171M355 70V115Q355 132 337 132H248M248 218V267M248 311V350"/>
      </svg>
      <div class="source-pair"><div class="source-tile">{icon("database")}<span>SQL records</span></div><div class="source-tile">{icon("cloud")}<span>Files & APIs</span></div></div>
      <div class="journey-node ingest"><span class="journey-icon azure">{icon("workflow")}</span><div><b>Azure Data Factory</b><small>Ingest & orchestrate</small></div><span class="node-order">01</span></div>
      <div class="journey-node transform"><span class="journey-icon coral">{icon("layers")}</span><div><b>Azure Databricks</b><small>Transform & validate</small></div><span class="node-order">02</span></div>
      <div class="journey-node insight"><span class="journey-icon yellow">{icon("chart")}</span><div><b>Power BI</b><small>Model & explore</small></div><span class="node-order">03</span></div>
      <div class="canvas-foot"><span><i></i>Connected by design</span><span>Illustrative flow</span></div>
    </div>'''


def output_preview(project_id):
    if project_id == "powerbi":
        return '''<div class="output-preview bi-preview">
          <div class="preview-heading"><div><span class="eyebrow">THE BUSINESS VIEW</span><h4>Sales performance</h4></div><label class="select-label">Region<select class="region-filter" aria-label="Filter sample sales by region"><option>All regions</option><option>North</option><option>South</option><option>West</option></select></label></div>
          <div class="bi-layout"><div class="sample-metrics"><div><span>Sales</span><strong class="sales-value"></strong></div><div><span>Profit</span><strong class="profit-value"></strong></div><div><span>Margin</span><strong class="margin-value"></strong></div></div><div class="chart-wrap"><div class="chart-label"><span>Monthly sales</span><span>₹ thousands · synthetic</span></div><div class="sample-chart" role="img" aria-label="Synthetic monthly sales, January through June"></div></div></div>
          <p class="sample-note">Interactive report illustration · synthetic data · not an embedded Power BI report</p>
        </div>'''
    if project_id == "databricks":
        return '''<div class="output-preview lake-preview">
          <div class="preview-heading"><div><span class="eyebrow">FOLLOW THE RECORDS</span><h4>Quality improves at every layer.</h4></div><div class="layer-picker" role="group" aria-label="Choose a sample data layer"><button type="button" data-layer="bronze" class="active" aria-pressed="true">Bronze</button><button type="button" data-layer="silver" aria-pressed="false">Silver</button><button type="button" data-layer="gold" aria-pressed="false">Gold</button></div></div>
          <div class="sample-table-wrap"><table class="sample-table"><thead></thead><tbody></tbody></table></div><p class="sample-note layer-note" aria-live="polite"></p>
        </div>'''
    if project_id == "adf":
        return '''<div class="output-preview adf-preview">
          <div class="preview-heading"><div><span class="eyebrow">RELIABILITY BY DESIGN</span><h4>A checkpoint you can trust.</h4></div><label class="select-label">Run scenario<select class="scenario-filter" aria-label="Choose sample pipeline scenario"><option value="success">Successful load</option><option value="failure">Validation failure</option></select></label></div>
          <div class="run-ledger"><div><span>Previous checkpoint</span><strong class="mono">14 Jan · 00:00</strong></div><div class="ledger-arrow">→</div><div><span>Candidate checkpoint</span><strong class="mono">15 Jan · 00:00</strong></div><div><span>Stored checkpoint</span><strong class="mono watermark">14 Jan · 00:00</strong></div></div>
          <p class="ledger-status" aria-live="polite">Choose a scenario, then select “Run data flow” above.</p><p class="sample-note">Illustrative run window · 2026 UTC · each replay resets this local simulation</p>
        </div>'''
    return ""


def project_card(project):
    pid = project["id"]
    stages = "".join(
        f'<button type="button" class="stage {"selected" if i == 0 else ""}" data-stage="{i}" aria-pressed="{"true" if i == 0 else "false"}" aria-controls="{esc(pid)}-detail"><span class="stage-top"><span class="stage-icon">{icon(s["icon"])}</span><span class="stage-index">0{i+1}</span></span><strong>{esc(s["title"])}</strong><small>{esc(s["subtitle"])}</small></button>'
        for i, s in enumerate(project["stages"])
    )
    controls = "".join(f'<span>{icon("check")}{esc(t)}</span>' for t in project["controls"])
    first = project["stages"][0]
    links = external_button("Source code", project.get("github")) + external_button("Live project", project.get("demo"))
    branch = ""
    if pid == "databricks":
        branch = f'<div class="branch quarantine-branch">{icon("shield")}Invalid rows → quarantine table</div>'
    elif pid == "adf":
        branch = f'<div class="branch failure-branch">{icon("shield")}Failure → log & alert · retain checkpoint</div>'
    return f'''<article class="project-card {esc(pid)}" id="{esc(pid)}" data-project="{esc(pid)}">
      <div class="project-header"><div class="project-number">{esc(project["number"])}</div><div class="project-title"><div class="project-kicker"><span>{esc(project["platform"])}</span><span class="tiny-separator">/</span>{esc(project["category"])}</div><h3>{esc(project["title"])}</h3><p>{esc(project["summary"])}</p></div><span class="example-label">{esc(project["status"])}</span></div>
      <div class="project-brief"><div><span class="eyebrow">THE QUESTION</span><p>{esc(project["problem"])}</p></div><div><span class="eyebrow">THE APPROACH</span><p>{esc(project["approach"])}</p></div><div><span class="eyebrow">THE INTENDED VALUE</span><p>{esc(project["value"])}</p></div></div>
      <div class="architecture"><div class="architecture-heading"><div><span class="architecture-label">{icon("workflow")}High-level architecture</span><span class="architecture-hint">Select a stage to see what happens.</span></div><button type="button" class="flow-button">{icon("play")}<span>Run data flow</span></button></div>
        <div class="pipeline-canvas"><svg class="pipeline-edges" aria-hidden="true"></svg><div class="stages">{stages}</div>{branch}</div>
        <div class="flow-status" role="status"><span class="status-dot"></span><span class="flow-status-text">Interactive concept · ready to explore</span></div>
        <div class="stage-detail" id="{esc(pid)}-detail"><div class="detail-heading"><span class="detail-number">01</span><strong class="detail-title">{esc(first["title"])}</strong></div><div class="detail-grid"><div><span class="eyebrow">INPUT</span><p class="detail-input">{esc(first["input"])}</p></div><div><span class="eyebrow">WHAT HAPPENS</span><p class="detail-action">{esc(first["action"])}</p></div><div><span class="eyebrow">OUTPUT</span><p class="detail-output">{esc(first["output"])}</p></div></div></div>
        <div class="controls-line">{controls}</div>
      </div>
      {output_preview(pid)}
      <div class="project-bottom"><div class="chips">{chips(project["tags"])}</div><div class="project-links">{links}<a class="reference-link" href="{esc(valid_link(project["reference"]))}" target="_blank" rel="noopener noreferrer">Architecture reference {icon("up")}</a></div></div>
    </article>'''


def render_page(data):
    p = data["profile"]
    name = p["name"]
    initials = "".join(w[0] for w in name.split()[:2]).upper()
    headline = p.get("headline", DEFAULT_DATA["profile"]["headline"])
    resume = resume_button(p)
    social = external_button("LinkedIn", p.get("linkedin")) + external_button("GitHub", p.get("github"))
    email = str(p.get("email", "")).strip()
    contact = ""
    if email and "@" in email and not any(ch in email for ch in "\r\n?&# "):
        contact = f'<a class="button primary" href="mailto:{esc(email)}">Let’s talk{icon("mail")}</a>'
    contact += social
    if not contact:
        contact = '<p class="contact-pending">Direct contact details will be added soon.</p>'
    exp_html = ""
    for e in data["experience"]:
        points = "".join(f'<li>{esc(x)}</li>' for x in e["highlights"])
        exp_html += f'<div class="experience-item"><span class="timeline-dot"></span><span class="eyebrow">{esc(e["period"])}</span><h4>{esc(e["role"])}</h4><p class="company">{esc(e["company"])}</p><p class="location">{esc(e.get("location", ""))}</p><ul>{points}</ul></div>'
    education = "".join(f'<div class="education-item"><span class="eyebrow">EDUCATION · {esc(e["period"])}</span><h4>{esc(e["degree"])}</h4><p>{esc(e["school"])}</p></div>' for e in data["education"])
    certs = "".join(f'<div class="education-item"><span class="eyebrow">CERTIFICATION · {esc(c.get("year", ""))}</span><h4>{esc(c["name"])}</h4><p>{esc(c.get("issuer", ""))}</p>{external_button("View credential", c.get("url"))}</div>' for c in data["certifications"])
    skill_icons = ["workflow", "layers", "chart", "code"]
    skill_html = "".join(f'<div class="skill-card"><div class="skill-icon">{icon(skill_icons[i % 4])}</div><h4>{esc(k)}</h4><div class="chips">{chips(v)}</div></div>' for i, (k, v) in enumerate(data["skills"].items()))
    jump_links = "".join(f'<a href="#{esc(q["id"])}"><span>{esc(q["number"])}</span>{esc(q["platform"])}{icon("arrow")}</a>' for q in data["projects"])
    projects = "".join(project_card(q) for q in data["projects"])
    payload = base64.b64encode(json.dumps(data["projects"]).encode("utf-8")).decode("ascii")
    return f'''<div id="joel-portfolio" data-projects="{payload}">
      <a class="skip-link" href="#work">Skip to projects</a>
      <header class="site-header"><a class="brand" href="#home" aria-label="{esc(name)} home"><span class="monogram">{esc(initials)}</span><span>{esc(name)}<small>{esc(p["role"])}</small></span></a><nav aria-label="Main navigation"><a href="#work">Work</a><a href="#expertise">Expertise</a><a href="#about">About</a><a href="#contact">Contact</a></nav><button type="button" class="motion-toggle" aria-pressed="false" aria-label="Pause animations">{icon("pause")}<span>Pause motion</span></button></header>
      <main><section class="hero section-width" id="home"><div class="hero-copy"><span class="availability"><span class="status-dot"></span>{esc(p["availability"])}</span><p class="hero-intro">{esc(name)} <span>/</span> {esc(p["role"])}</p><h1>{esc(headline[0])}<br><span>{esc(headline[1])}</span></h1><p class="hero-description">{esc(p["tagline"])}</p><div class="hero-actions"><a class="button primary" href="#work">Explore my work{icon("arrow")}</a>{resume or '<a class="button text-button" href="#about">A little about me ↗</a>'}</div><div class="hero-location"><span>{esc(p["location"])}</span><span class="tiny-separator">/</span><span>Data engineering · Analytics</span></div></div>{hero_visual()}</section>
      <div class="focus-strip section-width"><div><span class="focus-index">01</span><div><strong>Ingest reliably.</strong><p>Connect sources. Control the flow.</p></div></div><div><span class="focus-index">02</span><div><strong>Transform with purpose.</strong><p>Build quality into every layer.</p></div></div><div><span class="focus-index">03</span><div><strong>Make data useful.</strong><p>Deliver insights people can act on.</p></div></div></div>
      <section class="work section-width" id="work"><div class="section-heading"><div><span class="eyebrow accent">SELECTED CONCEPTS / 01—03</span><h2>See the thinking.<br><span>Follow the data.</span></h2></div><p>Three example projects, from ingestion to insight. Explore the architecture and see how each stage connects to the next.</p></div><div class="project-jumps">{jump_links}</div><p class="examples-note">{icon("code")}Sample architectures and synthetic previews · designed to demonstrate an approach, with no production results claimed.</p>{projects}</section>
      <section class="expertise section-width" id="expertise"><div class="section-heading"><div><span class="eyebrow accent">THE TOOLKIT</span><h2>Built across the<br><span>data lifecycle.</span></h2></div><p>The tools I focus on, organized around the work they help me do.</p></div><div class="skills-grid">{skill_html}</div></section>
      <section class="about section-width" id="about"><div class="about-intro"><span class="eyebrow accent">BEHIND THE PIPELINES</span><h2>Curious about data.<br><span>Careful with detail.</span></h2><p>{esc(p["summary"])}</p><div class="about-links">{social}{resume}</div>{education}{certs}</div><div class="experience"><span class="eyebrow">EXPERIENCE</span>{exp_html}</div></section>
      <section class="contact section-width" id="contact"><div><span class="eyebrow accent">LET’S CONNECT</span><h2>Good data starts with<br>a good conversation.</h2><p>Let’s talk about data engineering, analytics, and the next useful thing to build.</p></div><div class="contact-actions">{contact}</div></section></main>
      <footer class="site-footer section-width"><span>{esc(name)} <span class="footer-sep">/</span> {esc(p["role"])}</span><span>Built with care. Powered by Streamlit.</span><a href="#home">Back to top ↑</a></footer>
    </div>'''


# ── PRESENTATION: scoped styles avoid affecting unrelated Streamlit widgets. ──
CSS = r'''
<style>
html{scroll-behavior:smooth}body{margin:0;background:#0b1015}
[data-testid="stAppViewContainer"],.stApp{background:#0b1015!important}
[data-testid="stHeader"],[data-testid="stToolbar"]{display:none!important}
[data-testid="stSidebar"],[data-testid="stMainMenu"]{display:none}
.stMainBlockContainer,.block-container{max-width:none!important;padding:0!important}
[data-testid="stVerticalBlock"]{gap:0!important}
#joel-portfolio{--bg:#0b1015;--card:#11181e;--panel:#151d25;--border:#29343e;--text:#f2f4f5;--muted:#a5b1bd;--mint:#a8efd2;--accent:#a8efd2;color:var(--text);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;font-size:15px;line-height:1.6;overflow:hidden;background:radial-gradient(ellipse at 87% 4%,#17312944,transparent 24%),var(--bg);text-rendering:optimizeLegibility}
#joel-portfolio *{box-sizing:border-box}#joel-portfolio a{color:inherit;text-decoration:none}#joel-portfolio button,#joel-portfolio select{font:inherit}#joel-portfolio button{cursor:pointer}#joel-portfolio h1,#joel-portfolio h2,#joel-portfolio h3,#joel-portfolio h4,#joel-portfolio p{margin:0;padding:0;font-family:inherit;color:inherit}#joel-portfolio h1,#joel-portfolio h2,#joel-portfolio h3{font-weight:600;letter-spacing:-.048em}#joel-portfolio p{color:var(--muted)}#joel-portfolio .icon{width:20px;height:20px;flex:none;vertical-align:middle}#joel-portfolio a:focus-visible,#joel-portfolio button:focus-visible,#joel-portfolio select:focus-visible{outline:2px solid var(--mint);outline-offset:5px}#joel-portfolio section,#joel-portfolio article{scroll-margin-top:34px}
#joel-portfolio .section-width{width:min(1200px,calc(100% - 96px));margin-inline:auto}#joel-portfolio .eyebrow{font-size:10px;letter-spacing:.15em;font-weight:600;color:#9aa9b7;display:block}#joel-portfolio .eyebrow.accent{color:var(--mint)}#joel-portfolio .mono{font-family:"SFMono-Regular",Consolas,monospace}#joel-portfolio .status-dot{width:6px;height:6px;border-radius:100%;background:var(--mint);display:inline-block;box-shadow:0 0 12px #a8efd22b;flex:none}#joel-portfolio .tiny-separator{opacity:.35}#joel-portfolio .button{display:inline-flex;align-items:center;justify-content:center;gap:14px;min-height:46px;padding:12px 20px;font-size:13px;font-weight:600;border-radius:7px;transition:background .18s,transform .18s;border:1px solid transparent}#joel-portfolio .button:hover{transform:translateY(-2px)}#joel-portfolio .primary{background:var(--mint);color:#11251d}#joel-portfolio .primary:hover{background:#c6ffe7}#joel-portfolio .secondary{border-color:var(--border);background:#152029;color:#e6edf1}#joel-portfolio .text-button{color:#bac6cd;padding-inline:10px}#joel-portfolio .button .icon{width:17px;height:17px}#joel-portfolio .skip-link{position:absolute;top:-80px;left:12px;z-index:30;padding:12px;background:var(--mint);color:#0b1015}#joel-portfolio .skip-link:focus{top:12px}
#joel-portfolio .site-header{width:min(1320px,calc(100% - 80px));margin:auto;display:flex;align-items:center;justify-content:space-between;padding:30px 0 26px;border-bottom:1px solid #22303b80;gap:24px}#joel-portfolio .brand{display:flex;gap:12px;align-items:center;font-size:14px;font-weight:600;line-height:1.35;min-width:205px}#joel-portfolio .brand small{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#91a2af;display:block;margin-top:4px;font-weight:400}#joel-portfolio .monogram{height:40px;width:40px;border:1px solid #88c6ad55;border-radius:10px;display:grid;place-items:center;color:var(--mint);font-size:14px;background:#19302755}#joel-portfolio nav{display:flex;gap:32px}#joel-portfolio nav a{font-size:13px;color:#b9c4cd;transition:color .15s}#joel-portfolio nav a:hover{color:var(--mint)}#joel-portfolio .motion-toggle{background:transparent;color:#a9b7c0;display:flex;align-items:center;justify-content:end;gap:8px;border:0;font-size:11px;min-width:205px}#joel-portfolio .motion-toggle .icon{width:13px;height:13px}
#joel-portfolio .hero{display:grid;grid-template-columns:1.15fr 1fr;align-items:center;gap:56px;padding-block:75px 64px}#joel-portfolio .availability{font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:#b8ebd5;display:inline-flex;align-items:center;gap:8px;border:1px solid #74ac9540;border-radius:30px;padding:6px 10px;background:#203d2e2b}#joel-portfolio .hero-intro{font-size:13px;color:#b8c4cd;margin:27px 0 14px}#joel-portfolio .hero-intro span{color:#617382;margin:0 6px}#joel-portfolio h1{font-size:clamp(43px,4.75vw,69px);line-height:1.04;white-space:nowrap}#joel-portfolio h1 span{color:var(--mint)}#joel-portfolio .hero-description{font-size:15px;line-height:1.8;max-width:460px;margin-top:24px}#joel-portfolio .hero-actions{display:flex;flex-wrap:wrap;gap:13px;margin-top:27px}#joel-portfolio .hero-location{display:flex;align-items:center;gap:12px;font-size:11px;color:#8a9caa;margin-top:30px}
#joel-portfolio .hero-canvas{height:424px;position:relative;background:radial-gradient(circle at 50% 70%,#a8efd20b,transparent 75%),radial-gradient(#4c687637 1px,transparent 1px),#10181e;background-size:auto,18px 18px,auto;border:1px solid #31433d;border-radius:14px;box-shadow:0 24px 90px #0003;overflow:hidden}#joel-portfolio .canvas-heading{position:absolute;top:21px;left:23px;right:23px;display:flex;align-items:center;justify-content:space-between;font-size:8px;font-weight:600;letter-spacing:.13em;color:#bccbc8;gap:8px}#joel-portfolio .canvas-heading .status-dot{margin-right:6px;width:5px;height:5px}#joel-portfolio .canvas-heading .mono{font-size:8px;color:#7e9990}#joel-portfolio .hero-wires{position:absolute;top:35px;width:100%;height:340px;overflow:visible}#joel-portfolio .hero-path{stroke:#547b69;stroke-width:1;fill:none}#joel-portfolio .hero-signal{stroke:url(#wire);stroke-width:2;fill:none;stroke-dasharray:10 44;animation:signal 7s linear infinite}#joel-portfolio .source-pair{position:absolute;top:68px;left:10%;width:80%;display:flex;justify-content:space-between;gap:20px}#joel-portfolio .source-tile{display:flex;align-items:center;gap:10px;padding:13px 14px;background:#17242b;border:1px solid #3b4a51;border-radius:7px;font-size:11px;width:46%;justify-content:center;color:#c8d4dc}#joel-portfolio .source-tile .icon{color:#8fafb1;width:17px;height:17px}#joel-portfolio .journey-node{position:absolute;left:20%;width:60%;display:flex;gap:13px;align-items:center;padding:14px;background:#15222a;border:1px solid #35434c;border-radius:9px;box-shadow:0 6px 15px #0002}#joel-portfolio .journey-node b{font-size:12px;font-weight:600;display:block;line-height:1.4}#joel-portfolio .journey-node small{font-size:10px;color:#91a5b3;display:block;margin-top:2px}#joel-portfolio .journey-node.ingest{top:152px}#joel-portfolio .journey-node.transform{top:237px}#joel-portfolio .journey-node.insight{top:321px;border-color:#55614a}#joel-portfolio .journey-icon{width:33px;height:33px;display:grid;place-items:center;border-radius:7px;flex:none}#joel-portfolio .journey-icon.azure{color:#85c7ed;background:#25465a}#joel-portfolio .journey-icon.coral{color:#fba495;background:#47322f}#joel-portfolio .journey-icon.yellow{color:#e8d57e;background:#45422c}#joel-portfolio .node-order{font-size:8px;color:#657d89;margin-left:auto;font-family:monospace}#joel-portfolio .canvas-foot{position:absolute;bottom:9px;left:22px;right:22px;display:flex;justify-content:space-between;font-size:8px;color:#7f968e}#joel-portfolio .canvas-foot i{display:inline-block;width:4px;height:4px;background:#8bc5a7;border-radius:50%;margin-right:6px}
#joel-portfolio .focus-strip{border-top:1px solid var(--border);border-bottom:1px solid var(--border);display:grid;grid-template-columns:repeat(3,1fr);padding:25px 0;gap:30px}#joel-portfolio .focus-strip>div{display:flex;align-items:flex-start;gap:16px}#joel-portfolio .focus-index{font-size:10px;color:#81948f;padding-top:4px;font-family:monospace}#joel-portfolio .focus-strip strong{font-size:13px;font-weight:500}#joel-portfolio .focus-strip p{font-size:11px;margin-top:3px;color:#8c9aa6}
#joel-portfolio .work{padding-top:77px}#joel-portfolio .section-heading{display:flex;align-items:end;justify-content:space-between;gap:60px;margin-bottom:28px}#joel-portfolio h2{font-size:43px;line-height:1.15;margin-top:13px}#joel-portfolio h2 span{color:#8fa2af}#joel-portfolio .section-heading>p{font-size:13px;line-height:1.8;max-width:355px;padding-bottom:6px}#joel-portfolio .project-jumps{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--border);border-radius:9px;overflow:hidden;margin-top:33px}#joel-portfolio .project-jumps a{display:flex;align-items:center;gap:13px;padding:17px 20px;font-size:12px;color:#d5dfe4;border-right:1px solid var(--border);background:#131c2350}#joel-portfolio .project-jumps a:last-child{border-right:0}#joel-portfolio .project-jumps a:hover{background:#20312b}#joel-portfolio .project-jumps a span{font:10px monospace;color:#9fcbb9}#joel-portfolio .project-jumps .icon{margin-left:auto;width:15px;height:15px;color:var(--mint)}#joel-portfolio .examples-note{font-size:10px;margin:15px 0 26px;display:flex;align-items:center;gap:8px;line-height:1.7}#joel-portfolio .examples-note .icon{width:13px;height:13px;color:#809487}
#joel-portfolio .project-card{border:1px solid var(--border);border-radius:14px;background:var(--card);margin-bottom:25px;overflow:hidden;--accent:#e6d080;--tint:#e6d0800b}#joel-portfolio .project-card.databricks{--accent:#f2a291;--tint:#f2a2910b}#joel-portfolio .project-card.adf{--accent:#8bc9ee;--tint:#8bc9ee0b}#joel-portfolio .project-header{display:flex;gap:21px;align-items:flex-start;padding:31px 32px 22px;background:linear-gradient(120deg,var(--tint),transparent 70%)}#joel-portfolio .project-number{height:39px;width:39px;display:grid;place-items:center;color:var(--accent);border:1px solid var(--border);border-radius:9px;font-size:13px;font-family:monospace;flex:none}#joel-portfolio .project-title{flex:1}#joel-portfolio .project-kicker{font-size:10px;color:#94a5b2;display:flex;gap:10px;align-items:center}#joel-portfolio .project-kicker>span:first-child{color:var(--accent);font-weight:600}#joel-portfolio h3{font-size:29px;line-height:1.25;margin-top:9px}#joel-portfolio .project-title>p{font-size:12px;max-width:660px;line-height:1.8;margin-top:10px}#joel-portfolio .example-label{font-size:9px;border:1px solid #3c4b51;padding:4px 8px;white-space:nowrap;border-radius:5px;color:#a9b8c2;margin-top:1px}#joel-portfolio .project-brief{display:grid;grid-template-columns:1fr 1fr 1fr;gap:27px;padding:0 32px 26px}#joel-portfolio .project-brief .eyebrow{font-size:8px;color:#7f94a4}#joel-portfolio .project-brief p{font-size:11px;line-height:1.8;margin-top:7px}
#joel-portfolio .architecture{margin:0 20px;border:1px solid #293741;border-radius:9px;background:#0e151b}#joel-portfolio .architecture-heading{display:flex;justify-content:space-between;align-items:center;gap:18px;padding:17px 18px;border-bottom:1px solid #26343e}#joel-portfolio .architecture-heading>div{display:flex;align-items:center;gap:18px}#joel-portfolio .architecture-label{display:flex;align-items:center;gap:8px;font-size:11px;font-weight:500}#joel-portfolio .architecture-label .icon{width:15px;height:15px;color:var(--accent)}#joel-portfolio .architecture-hint{color:#8496a3;font-size:9px}#joel-portfolio .flow-button{display:flex;gap:7px;align-items:center;justify-content:center;border:1px solid #42545c;background:#1d2c34;color:#e2e9ed;padding:7px 11px;border-radius:5px;white-space:nowrap;font-size:10px;transition:border-color .2s}#joel-portfolio .flow-button:hover{border-color:var(--accent)}#joel-portfolio .flow-button .icon{width:12px;height:12px}#joel-portfolio .pipeline-canvas{position:relative;background:radial-gradient(#728b9a29 .7px,transparent .7px);background-size:14px 14px;padding:28px 20px 20px;overflow:hidden}#joel-portfolio .stages{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:24px;position:relative;z-index:1}#joel-portfolio .stage{min-width:0;display:flex;flex-direction:column;text-align:left;background:#15212a;color:#e0e8ed;border:1px solid #33434f;border-radius:8px;padding:13px 12px;transition:border-color .18s,background .18s,box-shadow .18s;min-height:108px}#joel-portfolio .stage:hover{background:#1c2e37;border-color:#678075}#joel-portfolio .stage.selected{border-color:var(--accent);background:#1e2a30;box-shadow:0 0 0 1px color-mix(in srgb,var(--accent) 10%,transparent)}#joel-portfolio .stage.running{box-shadow:0 0 22px color-mix(in srgb,var(--accent) 15%,transparent);border-color:var(--accent)}#joel-portfolio .stage.complete .stage-index{color:var(--mint)}#joel-portfolio .stage.failed{border-color:#ed928d}#joel-portfolio .stage-top{display:flex;justify-content:space-between;align-items:center;width:100%;margin-bottom:10px}#joel-portfolio .stage-icon{color:var(--accent)}#joel-portfolio .stage-icon .icon{width:21px;height:21px}#joel-portfolio .stage-index{font:8px monospace;color:#7a919e}#joel-portfolio .stage strong{font-size:11px;font-weight:600;letter-spacing:-.01em;line-height:1.4}#joel-portfolio .stage small{font-size:8px;color:#8fa4b2;margin-top:3px;line-height:1.4}#joel-portfolio .pipeline-edges{position:absolute;inset:0;width:100%;height:100%;z-index:0;overflow:visible}#joel-portfolio .edge{fill:none;stroke:#536b76;stroke-width:1.3}#joel-portfolio .edge.active{stroke:var(--accent);stroke-width:2;stroke-dasharray:5 4;animation:signal 1s linear infinite}#joel-portfolio .edge-arrow{fill:#82989f}#joel-portfolio .edge.branch-edge{stroke:#798889;stroke-dasharray:3 4}#joel-portfolio .branch{position:relative;z-index:1;background:#1c2226;color:#a9b7be;border:1px dashed #576067;border-radius:5px;width:max-content;max-width:100%;padding:6px 12px;font-size:9px;margin-top:26px;line-height:1.6}#joel-portfolio .quarantine-branch{margin-left:43%}#joel-portfolio .failure-branch{margin-left:auto;margin-right:0}#joel-portfolio .branch .icon{width:12px;height:12px;margin-right:6px;color:var(--accent)}#joel-portfolio .flow-status{display:flex;align-items:center;gap:7px;padding:0 20px 14px;color:#92a8b5;font-size:9px;min-height:24px}#joel-portfolio .flow-status .status-dot{width:4px;height:4px;background:var(--accent)}#joel-portfolio .stage-detail{margin:0 14px 14px;border:1px solid #2c3a43;background:#152029;border-radius:6px;padding:14px 17px}#joel-portfolio .detail-heading{display:flex;align-items:center;gap:8px;margin-bottom:9px}#joel-portfolio .detail-number{font:8px monospace;color:var(--accent)}#joel-portfolio .detail-title{font-size:11px;font-weight:500}#joel-portfolio .detail-grid{display:grid;grid-template-columns:1fr 1.4fr 1fr;gap:24px}#joel-portfolio .detail-grid .eyebrow{font-size:7px;letter-spacing:.11em;color:#8197a6}#joel-portfolio .detail-grid p{font-size:10px;line-height:1.75;margin-top:4px;min-height:53px}#joel-portfolio .controls-line{padding:11px 18px;border-top:1px solid #25333d;display:flex;flex-wrap:wrap;gap:20px}#joel-portfolio .controls-line>span{font-size:9px;color:#8fa2ad;display:flex;align-items:center;gap:5px}#joel-portfolio .controls-line .icon{width:11px;height:11px;color:#9ec7b4}
#joel-portfolio .output-preview{margin:20px 20px 0;border-radius:8px;background:#151e26;border:1px solid #2b3842;padding:19px}#joel-portfolio .preview-heading{display:flex;justify-content:space-between;gap:18px;align-items:center;margin-bottom:16px}#joel-portfolio .preview-heading .eyebrow{font-size:7px;color:var(--accent);letter-spacing:.13em}#joel-portfolio h4{font-size:15px;font-weight:500;line-height:1.5}#joel-portfolio .preview-heading h4{margin-top:3px}#joel-portfolio .select-label{display:flex;gap:8px;align-items:center;font-size:8px;color:#a3b3c0}#joel-portfolio select{color:#d9e3e9;background:#172630;border:1px solid #3c505c;padding:7px 25px 7px 9px;border-radius:5px;font-size:9px;cursor:pointer;color-scheme:dark;max-width:180px}#joel-portfolio .bi-layout{display:grid;grid-template-columns:.85fr 1.15fr;gap:35px;align-items:center}#joel-portfolio .sample-metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}#joel-portfolio .sample-metrics span{font-size:9px;display:block;color:#96a9b8}#joel-portfolio .sample-metrics strong{font-size:25px;letter-spacing:-.035em;font-weight:500;margin-top:3px;display:block;line-height:1.4}#joel-portfolio .sample-metrics>div:last-child strong{color:var(--accent)}#joel-portfolio .chart-label{display:flex;justify-content:space-between;font-size:8px;color:#95a5b0;margin-bottom:9px}#joel-portfolio .sample-chart{display:flex;gap:13px;align-items:end;height:77px;border-bottom:1px solid #40535f;padding:0 6px 16px}#joel-portfolio .chart-column{flex:1;position:relative;display:flex;align-items:end;height:100%;min-width:0}#joel-portfolio .chart-bar{width:100%;min-height:4px;background:linear-gradient(180deg,#e4ce81,#817651);border-radius:3px 3px 0 0;position:relative;transition:height .3s}#joel-portfolio .chart-column:nth-last-child(-n+2) .chart-bar{background:linear-gradient(180deg,#acedd0,#548d79)}#joel-portfolio .chart-month{position:absolute;bottom:-15px;left:0;right:0;text-align:center;font-size:7px;color:#879caa}#joel-portfolio .chart-value{position:absolute;top:-14px;width:100%;text-align:center;font-size:7px;color:#c9d8dc}#joel-portfolio .sample-note{font-size:8px;color:#899eac;margin-top:15px;line-height:1.6}#joel-portfolio .layer-picker{display:flex;gap:3px;background:#0f171e;border:1px solid #344451;border-radius:6px;padding:3px}#joel-portfolio .layer-picker button{font-size:9px;padding:5px 11px;color:#9ab0bf;border:0;border-radius:4px;background:transparent}#joel-portfolio .layer-picker button.active{color:#f8d7cc;background:#42352f}#joel-portfolio .sample-table-wrap{overflow-x:auto}#joel-portfolio .sample-table{width:100%;border-collapse:collapse;font-size:9px;text-align:left;white-space:nowrap;margin:0;color:#b5c5d0}#joel-portfolio .sample-table th{font-size:8px;font-weight:400;text-transform:uppercase;letter-spacing:.07em;color:#8ba0af;background:#1b2933;border:0;padding:8px 12px}#joel-portfolio .sample-table td{padding:7px 12px;border:0;border-bottom:1px solid #29384266;line-height:1.45;font-family:"SFMono-Regular",Consolas,monospace}#joel-portfolio .sample-table td:last-child{color:#cfb395}#joel-portfolio .sample-table tr:last-child td{border-bottom:0}#joel-portfolio .run-ledger{display:grid;grid-template-columns:1fr auto 1fr 1.1fr;align-items:center;gap:20px;background:#111b23;padding:16px;border:1px solid #2b3c48;border-radius:6px}#joel-portfolio .run-ledger span{font-size:8px;color:#96a9b7;display:block}#joel-portfolio .run-ledger strong{font-size:12px;color:#cfdee7;display:block;font-weight:400;margin-top:5px}#joel-portfolio .run-ledger>div:last-child{border-left:1px solid #374f5d;padding-left:20px}#joel-portfolio .run-ledger>div:last-child strong{color:var(--accent)}#joel-portfolio .ledger-arrow{color:#749cad}#joel-portfolio .ledger-status{font-size:9px;margin-top:12px;color:#b1c2cf}#joel-portfolio .ledger-status.failed{color:#efa5a0}
#joel-portfolio .project-bottom{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:21px 25px;flex-wrap:wrap}#joel-portfolio .chips{display:flex;flex-wrap:wrap;gap:5px}#joel-portfolio .chip{font-size:9px;line-height:1.6;padding:4px 8px;color:#aebfcb;border:1px solid #30414d;background:#19232b;border-radius:4px;display:inline-block}#joel-portfolio .project-links{display:flex;gap:10px;align-items:center;flex-wrap:wrap}#joel-portfolio .project-links .button{font-size:10px;padding:7px 9px;min-height:30px}#joel-portfolio .reference-link{font-size:9px;color:#91a7b6}#joel-portfolio .reference-link .icon{width:12px;height:12px;margin-left:3px}#joel-portfolio .reference-link:hover{color:var(--accent)}
#joel-portfolio .expertise{padding-block:68px 73px}#joel-portfolio .skills-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:31px}#joel-portfolio .skill-card{border-top:1px solid #355045;padding:24px 18px;background:linear-gradient(180deg,#18251e55,transparent)}#joel-portfolio .skill-icon{color:#acdfc9;margin-bottom:14px}#joel-portfolio .skill-card h4{font-size:12px;margin-bottom:16px}#joel-portfolio .skill-card .chip{font-size:9px;background:#151e24;border-color:#273b40}#joel-portfolio .about{display:grid;grid-template-columns:1fr 1fr;gap:100px;border-top:1px solid var(--border);padding-block:72px}#joel-portfolio .about h2{font-size:35px;margin-bottom:22px}#joel-portfolio .about-intro>p{font-size:13px;line-height:1.9;max-width:440px}#joel-portfolio .about-links{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}#joel-portfolio .education-item{padding:23px 0 0;margin-top:24px;border-top:1px solid var(--border)}#joel-portfolio .education-item .eyebrow{font-size:8px}#joel-portfolio .education-item h4{font-size:13px;margin-top:9px}#joel-portfolio .education-item p{font-size:11px;margin-top:4px}#joel-portfolio .experience{padding-top:2px}#joel-portfolio .experience-item{position:relative;padding:0 0 7px 22px;margin-top:31px;border-left:1px solid #355145}#joel-portfolio .timeline-dot{position:absolute;left:-4px;top:4px;width:7px;height:7px;background:var(--mint);border-radius:50%;box-shadow:0 0 0 4px #a8efd20d}#joel-portfolio .experience-item .eyebrow{color:#8cb7a4;font-size:9px}#joel-portfolio .experience-item h4{font-size:19px;margin-top:10px}#joel-portfolio .experience-item .company{font-size:12px;color:#ccd8df;margin-top:4px}#joel-portfolio .experience-item .location{font-size:10px;margin-top:4px}#joel-portfolio .experience-item ul{margin:19px 0 0;padding-left:14px;line-height:1.85;color:#9fadb8;font-size:11px}#joel-portfolio .experience-item li{padding-left:3px;margin-bottom:10px}#joel-portfolio .experience-item li::marker{color:#70a68f}#joel-portfolio .contact{display:flex;justify-content:space-between;align-items:center;gap:40px;padding:42px 40px;background:radial-gradient(ellipse at 0 0,#244b373b,transparent 80%),#14201c;border:1px solid #335345;border-radius:12px}#joel-portfolio .contact h2{font-size:37px;margin-top:12px}#joel-portfolio .contact p{font-size:12px;max-width:420px;margin-top:16px;line-height:1.8}#joel-portfolio .contact-actions{display:flex;gap:10px;flex-wrap:wrap;justify-content:end;max-width:320px}#joel-portfolio .contact-pending{color:#9bb5a7!important;font-size:11px!important;max-width:220px!important}#joel-portfolio .site-footer{display:flex;align-items:center;justify-content:space-between;gap:25px;padding-block:30px;font-size:9px;color:#879daa}#joel-portfolio .footer-sep{margin:0 6px;color:#486256}#joel-portfolio .site-footer a{color:#bfd2c8}
/* Keep technical explanations readable at a normal browser zoom. */
#joel-portfolio .project-title>p,#joel-portfolio .project-brief p{font-size:13px}
#joel-portfolio .project-brief .eyebrow,#joel-portfolio .detail-grid .eyebrow{font-size:9px}
#joel-portfolio .stage strong{font-size:12px}#joel-portfolio .stage small{font-size:10px}
#joel-portfolio .detail-grid p{font-size:12px}#joel-portfolio .detail-title{font-size:12px}
#joel-portfolio .controls-line>span,#joel-portfolio .sample-note,#joel-portfolio .reference-link{font-size:10px}
#joel-portfolio .sample-table{font-size:11px}#joel-portfolio .sample-table th{font-size:9px}
#joel-portfolio .ledger-status{font-size:11px}
@keyframes signal{to{stroke-dashoffset:-108}}
#joel-portfolio.motion-off *,#joel-portfolio.motion-off *::before,#joel-portfolio.motion-off *::after{animation:none!important;transition:none!important}
@media(min-width:1500px){#joel-portfolio .hero{padding-block:88px 76px}}
@media(max-width:1000px){#joel-portfolio .section-width{width:calc(100% - 56px)}#joel-portfolio .site-header{width:calc(100% - 56px)}#joel-portfolio .hero{gap:25px;grid-template-columns:1.08fr 1fr}#joel-portfolio h1{font-size:clamp(38px,5vw,52px)}#joel-portfolio .hero-canvas{height:408px}#joel-portfolio .journey-node{left:12%;width:76%}#joel-portfolio .motion-toggle{min-width:auto}#joel-portfolio .brand{min-width:auto}#joel-portfolio nav{gap:22px}#joel-portfolio .architecture-hint{display:none}#joel-portfolio .stages{gap:17px}#joel-portfolio .stage{padding:11px 8px}#joel-portfolio .stage strong{font-size:10px}#joel-portfolio .stage small{font-size:8px}#joel-portfolio .project-header{gap:16px;padding:26px 24px 20px}#joel-portfolio .example-label{display:none}#joel-portfolio .project-brief{padding-inline:24px;gap:20px}#joel-portfolio .bi-layout{grid-template-columns:1fr 1fr;gap:25px}#joel-portfolio .sample-metrics strong{font-size:21px}#joel-portfolio .about{gap:55px}#joel-portfolio .contact h2{font-size:31px}#joel-portfolio .skills-grid{grid-template-columns:repeat(2,1fr)}#joel-portfolio .hero-description{font-size:13px}#joel-portfolio .hero-location{font-size:9px}}
@media(max-width:700px){#joel-portfolio .section-width{width:calc(100% - 36px)}#joel-portfolio .site-header{width:calc(100% - 36px);padding-block:19px 17px;gap:10px;flex-wrap:wrap}#joel-portfolio .brand{font-size:12px}#joel-portfolio .brand small{font-size:8px}#joel-portfolio .monogram{width:34px;height:34px}#joel-portfolio nav{order:3;width:100%;justify-content:space-between;gap:15px;padding-top:12px}#joel-portfolio nav a{font-size:12px}#joel-portfolio .motion-toggle{font-size:10px}#joel-portfolio .hero{grid-template-columns:1fr;gap:31px;padding-block:36px 30px}#joel-portfolio .availability{font-size:8px}#joel-portfolio .hero-intro{font-size:11px;margin-top:23px}#joel-portfolio h1{font-size:clamp(35px,9.1vw,60px);letter-spacing:-.05em}#joel-portfolio .hero-description{font-size:13px;margin-top:18px;max-width:420px}#joel-portfolio .hero-actions{gap:6px;margin-top:21px}#joel-portfolio .button{font-size:11px;padding:11px 14px;gap:9px}#joel-portfolio .hero-location{margin-top:20px;font-size:9px}#joel-portfolio .hero-canvas{height:417px;max-width:470px;width:100%;margin:auto}#joel-portfolio .journey-node{left:18%;width:64%}#joel-portfolio .source-pair{left:8%;width:84%;gap:14px}#joel-portfolio .source-tile{font-size:10px;padding:12px 8px}#joel-portfolio .focus-strip{gap:17px;padding-block:20px}#joel-portfolio .focus-strip>div{display:block}#joel-portfolio .focus-index{font-size:9px;display:block;margin-bottom:6px}#joel-portfolio .focus-strip strong{font-size:10px;line-height:1.5;display:block}#joel-portfolio .focus-strip p{font-size:8px;line-height:1.8;margin-top:6px}#joel-portfolio .work{padding-top:43px}#joel-portfolio h2{font-size:32px}#joel-portfolio .section-heading{display:block;margin-bottom:23px}#joel-portfolio .section-heading>p{margin-top:17px;max-width:450px;font-size:12px}#joel-portfolio .project-jumps{grid-template-columns:1fr;margin-top:22px}#joel-portfolio .project-jumps a{padding:11px 14px;border-right:0;border-bottom:1px solid var(--border);font-size:11px}#joel-portfolio .project-jumps a:last-child{border-bottom:0}#joel-portfolio .examples-note{align-items:flex-start;font-size:9px;margin-block:13px 22px}#joel-portfolio .examples-note .icon{margin-top:3px}#joel-portfolio .project-header{padding:21px 18px 18px;gap:12px}#joel-portfolio .project-number{width:28px;height:28px;border-radius:6px;font-size:10px}#joel-portfolio .project-kicker{font-size:8px;gap:6px;flex-wrap:wrap}#joel-portfolio h3{font-size:23px;margin-top:8px}#joel-portfolio .project-title>p{font-size:11px}#joel-portfolio .project-brief{grid-template-columns:1fr;gap:15px;padding:0 19px 21px}#joel-portfolio .project-brief p{font-size:11px;margin-top:4px}#joel-portfolio .architecture{margin:0 10px}#joel-portfolio .architecture-heading{padding:12px 11px;gap:9px}#joel-portfolio .architecture-label{font-size:9px;gap:5px}#joel-portfolio .architecture-label .icon{width:12px;height:12px}#joel-portfolio .flow-button{font-size:9px;padding:6px 8px;gap:4px}#joel-portfolio .stages{grid-template-columns:1fr;gap:23px;width:100%;padding-right:0}#joel-portfolio .stage{min-height:71px;padding:12px 13px;position:relative;padding-left:58px;justify-content:center}#joel-portfolio .stage-top{position:absolute;left:15px;top:24px;width:auto;margin:0}#joel-portfolio .stage-index{position:absolute;left:calc(100vw - 136px);top:-13px}#joel-portfolio .stage strong{font-size:12px}#joel-portfolio .stage small{font-size:9px;margin-top:3px}#joel-portfolio .pipeline-canvas{padding:18px 14px}#joel-portfolio .branch{margin:25px 0 0 auto;font-size:8px;padding:6px 8px;max-width:100%;width:fit-content}#joel-portfolio .flow-status{font-size:8px;padding-inline:14px;padding-bottom:12px;align-items:flex-start;min-height:20px}#joel-portfolio .flow-status .status-dot{margin-top:5px}#joel-portfolio .stage-detail{padding:13px;margin:0 10px 10px}#joel-portfolio .detail-grid{grid-template-columns:1fr;gap:10px}#joel-portfolio .detail-grid p{font-size:10px;min-height:0}#joel-portfolio .detail-grid .eyebrow{font-size:7px}#joel-portfolio .controls-line{gap:9px;padding:10px 12px}#joel-portfolio .controls-line>span{font-size:8px}#joel-portfolio .output-preview{margin:12px 10px 0;padding:14px}#joel-portfolio .preview-heading{align-items:flex-start;flex-wrap:wrap;gap:11px;margin-bottom:16px}#joel-portfolio .preview-heading h4{font-size:13px}#joel-portfolio .select-label{font-size:8px}#joel-portfolio .select-label select{font-size:9px;padding:6px 9px}#joel-portfolio .bi-layout{grid-template-columns:1fr;gap:25px}#joel-portfolio .sample-metrics strong{font-size:23px}#joel-portfolio .sample-chart{height:90px}#joel-portfolio .sample-note{font-size:8px}#joel-portfolio .run-ledger{grid-template-columns:1fr;gap:12px;padding:12px}#joel-portfolio .run-ledger>div:last-child{border-left:0;border-top:1px solid #304652;padding:12px 0 0}#joel-portfolio .ledger-arrow{display:none}#joel-portfolio .run-ledger strong{font-size:12px;margin-top:3px}#joel-portfolio .project-bottom{padding:16px;gap:14px}#joel-portfolio .chip{font-size:8px}#joel-portfolio .expertise{padding-block:33px 38px}#joel-portfolio .skills-grid{gap:10px;margin-top:20px}#joel-portfolio .skill-card{padding:17px 10px}#joel-portfolio .skill-card h4{font-size:10px}#joel-portfolio .skill-card .chip{font-size:8px;padding:3px 5px}#joel-portfolio .about{grid-template-columns:1fr;gap:36px;padding-block:39px}#joel-portfolio .about h2{font-size:29px}#joel-portfolio .about-intro>p{font-size:12px}#joel-portfolio .experience-item{margin-top:22px}#joel-portfolio .contact{display:block;padding:27px 22px}#joel-portfolio .contact h2{font-size:28px}#joel-portfolio .contact p{font-size:11px}#joel-portfolio .contact-actions{justify-content:start;margin-top:24px}#joel-portfolio .site-footer{flex-wrap:wrap;gap:12px;font-size:8px;padding-block:23px}#joel-portfolio .site-footer>span:nth-child(2){order:3;width:100%}#joel-portfolio .site-footer a{margin-left:auto}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}#joel-portfolio *{animation:none!important;transition:none!important}}
@media print{#joel-portfolio .motion-toggle,#joel-portfolio .flow-button,#joel-portfolio .project-jumps,#joel-portfolio nav{display:none}#joel-portfolio .project-card{break-inside:avoid}#joel-portfolio{print-color-adjust:exact;-webkit-print-color-adjust:exact}}
</style>
'''


JS = r'''
<script>
(()=>{
  const root=document.getElementById('joel-portfolio');
  if(!root || root.dataset.initialized==='true')return;
  root.dataset.initialized='true';
  const cleanups=[];
  // The HTML is authored here; user-editable content is escaped in Python.
  const projects=JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(root.dataset.projects),c=>c.charCodeAt(0))));
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  let motionOff=reduced.matches;
  const motionButton=root.querySelector('.motion-toggle');
  function updateMotion(){
    root.classList.toggle('motion-off',motionOff);
    motionButton.setAttribute('aria-pressed',String(motionOff));
    motionButton.setAttribute('aria-label',motionOff?'Resume animations':'Pause animations');
    motionButton.querySelector('span').textContent=motionOff?'Resume motion':'Pause motion';
  }
  updateMotion();
  motionButton.addEventListener('click',()=>{motionOff=!motionOff;updateMotion()});
  const reducedHandler=()=>{motionOff=reduced.matches;updateMotion()};
  reduced.addEventListener('change',reducedHandler);
  cleanups.push(()=>reduced.removeEventListener('change',reducedHandler));
  const escapeHtml=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  root.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',event=>{
    const target=root.querySelector(a.getAttribute('href'));
    if(target){event.preventDefault();target.scrollIntoView({behavior:motionOff?'instant':'smooth',block:'start'});target.setAttribute('tabindex','-1');target.focus({preventScroll:true});}
  }));
  // Connect actual node bounds so the hero's wires remain aligned at every width.
  const hero=root.querySelector('.hero-canvas');
  function drawHero(){
    if(!root.isConnected)return;
    const bounds=hero.getBoundingClientRect();
    const svg=hero.querySelector('.hero-wires');
    svg.style.top='0';svg.style.height='100%';
    svg.setAttribute('viewBox',`0 0 ${bounds.width} ${bounds.height}`);
    const nodes=Array.from(hero.querySelectorAll('.journey-node'));
    const first=nodes[0].getBoundingClientRect();
    let d='';
    hero.querySelectorAll('.source-tile').forEach(source=>{
      const rect=source.getBoundingClientRect();
      const sx=rect.left+rect.width/2-bounds.left,sy=rect.bottom-bounds.top;
      const tx=first.left+first.width/2-bounds.left,ty=first.top-bounds.top;
      d+=`M${sx} ${sy}V${(sy+ty)/2}H${tx}V${ty}`;
    });
    nodes.slice(0,-1).forEach((node,i)=>{
      const a=node.getBoundingClientRect(),b=nodes[i+1].getBoundingClientRect();
      d+=`M${a.left+a.width/2-bounds.left} ${a.bottom-bounds.top}L${b.left+b.width/2-bounds.left} ${b.top-bounds.top}`;
    });
    hero.querySelector('.hero-path').setAttribute('d',d);
    hero.querySelector('.hero-signal').setAttribute('d',d);
  }
  const heroObserver=new ResizeObserver(()=>requestAnimationFrame(drawHero));
  heroObserver.observe(hero);cleanups.push(()=>heroObserver.disconnect());
  requestAnimationFrame(drawHero);
  // Synthetic sales values in thousands of INR. Margin is a weighted ratio.
  const monthly={North:[38,43,39,51,57,63],South:[31,36,42,41,48,53],West:[24,27,29,36,38,45]};
  const profitRates={North:.24,South:.28,West:.21};
  const region=root.querySelector('.region-filter');
  function updateSales(){
    if(!region)return;
    const groups=region.value==='All regions'?Object.keys(monthly):[region.value];
    const values=Array.from({length:6},(_,i)=>groups.reduce((s,g)=>s+monthly[g][i],0));
    const total=values.reduce((s,x)=>s+x,0);
    const profit=groups.reduce((s,g)=>s+monthly[g].reduce((a,v)=>a+v,0)*profitRates[g],0);
    const preview=root.querySelector('.bi-preview');
    const format=k=>'₹'+(k/100).toFixed(2)+'L';
    preview.querySelector('.sales-value').textContent=format(total);
    preview.querySelector('.profit-value').textContent=format(profit);
    preview.querySelector('.margin-value').textContent=(profit/total*100).toFixed(1)+'%';
    const months=['Jan','Feb','Mar','Apr','May','Jun'];
    preview.querySelector('.sample-chart').innerHTML=values.map((v,i)=>`<div class="chart-column"><div class="chart-bar" style="height:${v/Math.max(...values)*82}%" title="${months[i]}: ₹${v},000"><span class="chart-value">${v}</span></div><span class="chart-month">${months[i]}</span></div>`).join('');
    preview.querySelector('.sample-chart').setAttribute('aria-label',region.value+' synthetic sales: '+values.map((v,i)=>months[i]+' '+v+' thousand rupees').join(', '));
  }
  region?.addEventListener('change',updateSales);updateSales();
  // These local transformations make the Bronze/Silver/Gold preview consistent.
  const bronze=[
    {id:'1001',customer:'C01',region:'North',amount:1200,updated:'09:00'},
    {id:'1002',customer:'C02',region:'South',amount:1800,updated:'09:00'},
    {id:'1002',customer:'C02',region:'South',amount:2000,updated:'10:00'},
    {id:'1003',customer:'C03',region:'North',amount:800,updated:'09:10'},
    {id:'1004',customer:'C04',region:'West',amount:1500,updated:'09:20'},
    {id:'1005',customer:'',region:'South',amount:600,updated:'09:30'},
  ];
  const latest=new Map();
  bronze.forEach(row=>{if(!latest.has(row.id)||latest.get(row.id).updated<row.updated)latest.set(row.id,row)});
  const valid=row=>!!row.id&&!!row.customer&&Number.isFinite(row.amount)&&row.amount>=0;
  const silver=Array.from(latest.values()).filter(valid);
  const gold=Object.values(silver.reduce((result,r)=>{const row=result[r.region]??={region:r.region,orders:0,revenue:0};row.orders++;row.revenue+=r.amount;return result},{}));
  function updateLayer(layer){
    const preview=root.querySelector('.lake-preview');if(!preview)return;
    preview.querySelectorAll('[data-layer]').forEach(b=>{b.classList.toggle('active',b.dataset.layer===layer);b.setAttribute('aria-pressed',String(b.dataset.layer===layer))});
    let headers,rows,note;
    if(layer==='gold'){
      headers=['Region','Orders','Revenue (₹)'];rows=gold.map(r=>[r.region,r.orders,r.revenue.toLocaleString('en-IN')]);
      note='Gold · 3 region aggregates · 4 orders · ₹5,500 revenue. Aggregated from the validated Silver layer.';
    }else{
      headers=['Order ID','Customer','Region','Amount (₹)','Updated'];
      rows=(layer==='bronze'?bronze:silver).map(r=>[r.id,r.customer||'NULL',r.region,r.amount.toLocaleString('en-IN'),r.updated]);
      note=layer==='bronze'?'Bronze · 6 synthetic records. Order 1002 has two versions; order 1005 has no customer ID.':'Silver · 4 valid orders. The latest 1002 record is kept; 1005 is quarantined. One older duplicate is removed.';
    }
    preview.querySelector('thead').innerHTML='<tr>'+headers.map(h=>'<th scope="col">'+escapeHtml(h)+'</th>').join('')+'</tr>';
    preview.querySelector('tbody').innerHTML=rows.map(row=>'<tr>'+row.map(x=>'<td>'+escapeHtml(x)+'</td>').join('')+'</tr>').join('');
    preview.querySelector('.layer-note').textContent=note+' Browser illustration; no Databricks connection.';
  }
  root.querySelectorAll('[data-layer]').forEach(b=>b.addEventListener('click',()=>updateLayer(b.dataset.layer)));updateLayer('bronze');

  const ns='http://www.w3.org/2000/svg';
  projects.forEach(project=>{
    const card=Array.from(root.querySelectorAll('[data-project]')).find(c=>c.dataset.project===project.id);if(!card)return;
    const stages=Array.from(card.querySelectorAll('.stage'));
    const svg=card.querySelector('.pipeline-edges');const canvas=card.querySelector('.pipeline-canvas');
    let active=0,timer=null,running=false,runIndex=0;
    function selectStage(index){
      active=index;const s=project.stages[index];
      stages.forEach((b,i)=>{b.classList.toggle('selected',i===index);b.setAttribute('aria-pressed',String(i===index))});
      card.querySelector('.detail-number').textContent=String(index+1).padStart(2,'0');
      card.querySelector('.detail-title').textContent=s.title;
      card.querySelector('.detail-input').textContent=s.input;
      card.querySelector('.detail-action').textContent=s.action;
      card.querySelector('.detail-output').textContent=s.output;
    }
    function path(d,cls,index){const p=document.createElementNS(ns,'path');p.setAttribute('d',d);p.setAttribute('class',cls);if(index!==undefined)p.dataset.edge=String(index);svg.appendChild(p);return p}
    function drawEdges(){
      if(!root.isConnected){observer.disconnect();return}
      const bounds=canvas.getBoundingClientRect();svg.setAttribute('viewBox',`0 0 ${bounds.width} ${bounds.height}`);svg.replaceChildren();
      const vertical=window.innerWidth<=700;
      stages.slice(0,-1).forEach((node,i)=>{
        const a=node.getBoundingClientRect(),b=stages[i+1].getBoundingClientRect();
        let x1,y1,x2,y2;
        if(vertical){x1=a.left+a.width/2-bounds.left;y1=a.bottom-bounds.top;x2=b.left+b.width/2-bounds.left;y2=b.top-bounds.top;}
        else{x1=a.right-bounds.left;y1=a.top+a.height/2-bounds.top;x2=b.left-bounds.left;y2=b.top+b.height/2-bounds.top;}
        path(`M${x1} ${y1}L${x2} ${y2}`,'edge'+(running&&i<runIndex?' active':''),i);
        path(vertical?`M${x2-3} ${y2-5}L${x2} ${y2}L${x2+3} ${y2-5}Z`:`M${x2-5} ${y2-3}L${x2} ${y2}L${x2-5} ${y2+3}Z`,'edge-arrow');
      });
      const branch=card.querySelector('.branch');
      if(branch){
        const origin=stages[project.id==='databricks'?2:3].getBoundingClientRect(),dest=branch.getBoundingClientRect();
        const tx=dest.left+dest.width*.5-bounds.left,ty=dest.top-bounds.top;
        if(vertical){const sx=origin.left-bounds.left,sy=origin.top+origin.height/2-bounds.top;path(`M${sx} ${sy}H5V${ty-10}H${tx}V${ty}`,'edge branch-edge');}
        else{const sx=origin.left+origin.width/2-bounds.left,sy=origin.bottom-bounds.top;path(`M${sx} ${sy}V${ty-12}H${tx}V${ty}`,'edge branch-edge');}
      }
    }
    const observer=new ResizeObserver(()=>requestAnimationFrame(drawEdges));observer.observe(canvas);
    cleanups.push(()=>{clearTimeout(timer);observer.disconnect()});
    stages.forEach((node,i)=>node.addEventListener('click',()=>{if(running)stopRun('Paused · select a stage or run again.');selectStage(i)}));
    function status(text){card.querySelector('.flow-status-text').textContent=text}
    const runButton=card.querySelector('.flow-button');
    const scenario=card.querySelector('.scenario-filter');
    function stopRun(message){
      clearTimeout(timer);timer=null;running=false;stages.forEach(s=>s.classList.remove('running'));runButton.querySelector('span').textContent='Run data flow';if(scenario)scenario.disabled=false;
      if(message)status(message);drawEdges();
    }
    function finish(){
      stopRun('Simulation complete · source → trusted output.');
      stages.forEach(s=>s.classList.add('complete'));
      if(project.id==='adf'){
        card.querySelector('.watermark').textContent='15 Jan · 00:00';
        card.querySelector('.ledger-status').textContent='Success: validation and merge completed. The stored checkpoint advances to 15 Jan.';
      }
    }
    function step(){
      if(!root.isConnected){clearTimeout(timer);observer.disconnect();return}
      selectStage(runIndex);stages.forEach((s,i)=>{s.classList.toggle('running',i===runIndex);s.classList.toggle('complete',i<runIndex)});
      status(`Simulating ${runIndex+1}/${stages.length} · ${project.stages[runIndex].title}`);drawEdges();
      timer=setTimeout(()=>{
        if(project.id==='adf'&&scenario.value==='failure'&&runIndex===3){
          stages[3].classList.add('failed');stopRun('Validation failed · target merge and checkpoint update are skipped.');
          const note=card.querySelector('.ledger-status');note.classList.add('failed');note.textContent='Validation failed: keep 14 Jan as the stored checkpoint. Log and alert, then retry the same bounded window after correction.';return;
        }
        if(runIndex===stages.length-1)finish();else{runIndex++;step()}
      },motionOff?180:1100);
    }
    function resetCheckpoint(){
      if(project.id==='adf'){card.querySelector('.watermark').textContent='14 Jan · 00:00';const note=card.querySelector('.ledger-status');note.classList.remove('failed');note.textContent='Simulation reset. The old checkpoint is retained until validation and merge succeed.';}
    }
    runButton.addEventListener('click',()=>{
      if(running){stopRun('Simulation stopped · run again to replay.');return;}
      stages.forEach(s=>s.classList.remove('complete','failed'));resetCheckpoint();
      running=true;runIndex=0;runButton.querySelector('span').textContent='Stop flow';if(scenario)scenario.disabled=true;step();
    });
    scenario?.addEventListener('change',()=>{stopRun('Scenario changed · run the data flow to explore.');stages.forEach(s=>s.classList.remove('complete','failed'));resetCheckpoint()});
    selectStage(0);requestAnimationFrame(drawEdges);
  });
  return ()=>cleanups.forEach(cleanup=>cleanup());
})();
</script>
'''


def build_html(data=None, standalone=False):
    data = load_data() if data is None else data
    fragment = CSS + render_page(data) + JS
    if not standalone:
        return fragment
    title = esc(data["profile"]["name"] + " | " + data["profile"]["role"])
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>{title}</title></head><body>{fragment}</body></html>'


def main():
    import streamlit as st
    try:
        data = load_data()
        content = render_page(data)
    except (ValueError, TypeError, KeyError) as exc:
        st.error(f"Please check data/portfolio.json: {exc}")
        st.stop()
    st.set_page_config(page_title=data["profile"]["name"] + " | " + data["profile"]["role"], page_icon="✦", layout="wide", initial_sidebar_state="collapsed")
    # V2 preserves interactive SVGs and uses a single document scroll.
    # All layout and JavaScript are owned code. Editable text is escaped above.
    component_js = JS.replace("<script>", "").replace("</script>", "").strip()
    component_js = component_js.replace("(()=>{", '''export default function(component){
      const mount=component.parentElement.querySelector('.portfolio-mount');
      mount.innerHTML=component.data;
    ''', 1).replace("document.getElementById('joel-portfolio')", "mount.querySelector('#joel-portfolio')", 1)
    component_js = component_js.removesuffix("})();") + "}"
    portfolio = st.components.v2.component(
        "joel_portfolio",
        html='<div class="portfolio-mount"></div>',
        css=CSS.replace("<style>", "").replace("</style>", ""),
        js=component_js,
        isolate_styles=False,
    )
    portfolio(data=content, key="joel_portfolio_view", width="stretch", height="content")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--export-html", type=Path)
    args, _ = parser.parse_known_args()
    if args.export_html:
        args.export_html.write_text(build_html(standalone=True), encoding="utf-8")
        print(f"Preview saved: {args.export_html}")
    else:
        main()
