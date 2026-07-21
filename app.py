from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
RESOURCE_DIR = APP_DIR / "resources"


@st.cache_data
def load_json(name: str) -> Any:
    with (DATA_DIR / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


PROGRAM = load_json("program.json")
TOOL_RESEARCH = load_json("tool_research.json")
CASE_EXPANSIONS = {item["id"]: item for item in load_json("case_expansions.json")}
CASES = {item["id"]: item for item in PROGRAM["cases"]}
PROMPTS = {item["id"]: item for item in PROGRAM["prompts"]}
TOOLS = TOOL_RESEARCH["tools"]


st.set_page_config(
    page_title="Patient-Centric Healthcare 5.0",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:wght@600;700&display=swap');
:root {
  --navy:#082638; --navy2:#123e55; --teal:#087e78; --mint:#ddf2ee;
  --coral:#e8694a; --blush:#fbe7df; --blue:#2f6f9f; --sky:#e2eef7;
  --gold:#c59028; --sand:#f5eacd; --cream:#f7f3eb; --ink:#183340;
  --muted:#63747c; --line:#d3ddde; --white:#ffffff;
}
html, body, [class*="css"] { font-family:'Inter', sans-serif; color:var(--ink); }
.stApp { background:linear-gradient(180deg,#fbfaf7 0%,#f7f3eb 100%); }
[data-testid="stSidebar"] { background:var(--navy); }
[data-testid="stSidebar"] * { color:#eef7f6; }
[data-testid="stSidebar"] [data-baseweb="radio"] label { padding:.34rem .42rem; border-radius:10px; }
[data-testid="stSidebar"] [data-baseweb="radio"] label:hover { background:rgba(255,255,255,.08); }
h1,h2,h3 { font-family:'Source Serif 4',serif; color:var(--navy); letter-spacing:-.02em; }
h1 { font-size:2.65rem !important; line-height:1.05 !important; }
h2 { font-size:1.8rem !important; }
.block-container { max-width:1480px; padding-top:1.6rem; padding-bottom:4rem; }
.hero { background:linear-gradient(135deg,var(--navy) 0%,var(--navy2) 58%,var(--teal) 100%); border-radius:26px; padding:2.2rem 2.4rem; color:white; box-shadow:0 18px 50px rgba(8,38,56,.18); margin-bottom:1.2rem; }
.hero h1 { color:white !important; margin:0 0 .5rem 0; font-size:3rem !important; }
.hero p { color:#dbe9eb; font-size:1.08rem; max-width:900px; margin:.35rem 0; }
.eyebrow { display:inline-flex; align-items:center; gap:.45rem; text-transform:uppercase; letter-spacing:.11em; font-size:.72rem; font-weight:800; padding:.42rem .7rem; border-radius:999px; background:rgba(255,255,255,.12); color:white; margin-bottom:.8rem; }
.hero-grid { display:grid; grid-template-columns:repeat(4,minmax(120px,1fr)); gap:.65rem; margin-top:1.35rem; }
.hero-stat { background:rgba(255,255,255,.1); border:1px solid rgba(255,255,255,.16); border-radius:16px; padding:.75rem .9rem; }
.hero-stat strong { display:block; color:white; font-size:1.35rem; }
.hero-stat span { color:#dbe9eb; font-size:.76rem; }
.callout { border-radius:16px; padding:1rem 1.1rem; margin:.65rem 0 1rem; border:1px solid var(--line); background:white; }
.callout.teal { background:var(--mint); border-color:#9fcfc8; }
.callout.coral { background:var(--blush); border-color:#f2b5a4; }
.callout.gold { background:var(--sand); border-color:#e0c679; }
.callout.blue { background:var(--sky); border-color:#aac9dd; }
.callout strong { color:var(--navy); }
.metric-row { display:grid; grid-template-columns:repeat(4,1fr); gap:.8rem; margin:.8rem 0 1.1rem; }
.metric-card { background:white; border:1px solid var(--line); border-radius:18px; padding:1rem; box-shadow:0 8px 25px rgba(8,38,56,.06); }
.metric-card span { display:block; color:var(--muted); font-size:.75rem; text-transform:uppercase; letter-spacing:.08em; font-weight:700; }
.metric-card strong { display:block; color:var(--navy); font-size:1.75rem; margin-top:.2rem; }
.section-card { background:white; border:1px solid var(--line); border-radius:20px; padding:1rem 1.1rem; height:100%; box-shadow:0 8px 24px rgba(8,38,56,.05); }
.section-card h3 { margin-top:.2rem; }
.tag { display:inline-block; padding:.28rem .55rem; border-radius:999px; font-weight:800; font-size:.68rem; letter-spacing:.06em; text-transform:uppercase; margin:0 .25rem .25rem 0; }
.tag.teal { background:var(--mint); color:var(--teal); }
.tag.coral { background:var(--blush); color:#b7433d; }
.tag.gold { background:var(--sand); color:#8b6317; }
.tag.blue { background:var(--sky); color:var(--blue); }
.timeline { position:relative; margin:.5rem 0 1rem; }
.timeline-item { display:grid; grid-template-columns:86px 1fr; gap:.75rem; padding:.65rem 0; border-bottom:1px solid var(--line); }
.timeline-time { color:var(--teal); font-weight:800; font-size:.86rem; }
.timeline-title { color:var(--navy); font-weight:700; }
.timeline-copy { color:var(--muted); font-size:.87rem; margin-top:.15rem; }
.evidence-box { border-left:5px solid var(--coral); background:var(--blush); border-radius:12px; padding:.9rem 1rem; }
.checkpoint { border-left:5px solid var(--teal); background:var(--mint); border-radius:12px; padding:.9rem 1rem; }
.step { display:grid; grid-template-columns:38px 1fr; gap:.65rem; align-items:start; margin:.55rem 0; }
.step-num { width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; background:var(--teal); font-weight:800; }
.step-copy { padding-top:.3rem; }
.source-link { font-size:.8rem; color:var(--blue); overflow-wrap:anywhere; }
.small { font-size:.8rem; color:var(--muted); }
.footer { margin-top:2rem; padding-top:1rem; border-top:1px solid var(--line); color:var(--muted); font-size:.78rem; text-align:center; }
div[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:16px; overflow:hidden; }
.stButton > button, .stDownloadButton > button, a[data-testid="stLinkButton"] { border-radius:12px !important; font-weight:700 !important; }
@media (max-width:900px) { .hero-grid,.metric-row { grid-template-columns:repeat(2,1fr); } .hero h1 { font-size:2.35rem !important; } }
@media (max-width:600px) { .hero-grid,.metric-row { grid-template-columns:1fr; } .hero { padding:1.5rem; } .timeline-item { grid-template-columns:68px 1fr; } }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


THEORY_TIMELINE = [
    ("00–05", "Opening and patient-purpose contract", "Identify where technology steals attention or delays a safe decision."),
    ("05–12", "Capabilities + P-A-T-I-E-N-T", "Own projection, research, diagnostic support and continuity under seven safeguards."),
    ("12–24", "Operational value and alert design", "Serbia EHR and SepsisLab: workflow ownership, uncertainty and actionability."),
    ("24–34", "Trust and adoption", "Qatar perceptions and ambient scribes: consent, accountability, review work and stop rules."),
    ("34–46", "Learning and future readiness", "China teaching and Trinity foresight: efficiency without deleting productive struggle or values."),
    ("46–54", "Explainability and due diligence", "Explanations support scrutiny but do not prove correctness or benefit."),
    ("54–60", "Cross-case synthesis + India guardrails", "Evidence labels, DPDP/ICMR/CDSCO/UCPMP orientation and transition to the lab."),
]


STATIONS = [
    {
        "id": 1,
        "title": "Consultation continuity",
        "minutes": 18,
        "specialised": ["Heidi Health", "Nabla", "Abridge"],
        "prompts": [1, 6],
        "input": "Mrs A, 52: type 2 diabetes and hypertension; missed medicines twice this week; low health literacy; prefers Hindi; tingling feet; believes insulin means failure. No acute red flags are supplied.",
        "outcome": "A reviewed draft encounter summary, patient explanation, teach-back questions and a controlled ambient-scribe pilot plan.",
        "steps": [
            "Label the case synthetic and explain the consent/notice script.",
            "Enter the prepared transcript into the approved ambient tool or use saved screenshots.",
            "Generate the draft note and patient summary.",
            "Run ChatGPT Prompt 1 with the same input.",
            "Compare facts, omissions, inventions, medicine questions and escalation.",
            "Edit, approve or reject; then use Prompt 6 for pilot governance."
        ],
        "checkpoint": "No content enters a record or reaches a patient until a clinician/designated reviewer corrects and signs it.",
        "stop_rule": "Stop if an invented diagnosis, medicine, dose, allergy or red-flag disposition passes review unnoticed.",
        "debrief": "What attention did the tool return—and what new verification work did it create?",
    },
    {
        "id": 2,
        "title": "Diagnostic support + medication safety",
        "minutes": 23,
        "specialised": ["DxGPT", "Medscape AI", "ClinicalKey AI", "VisualDx", "iatroX", "MDCalc", "Epocrates"],
        "prompts": [2, 3],
        "input": "Mr R, 58: progressive breathlessness and ankle swelling; BP 164/96, pulse 104, SpO₂ 93%; diabetes, hypertension and smoking history; raised BNP and basal crepitations; medicine and ECG information incomplete.",
        "outcome": "A structured uncertainty map, source-verification record and medicine-reconciliation checklist—never a final diagnosis or prescription.",
        "steps": [
            "Ask which information changes urgency before it changes the differential.",
            "Run the problem representation in DxGPT or a prepared specialised-tool demo.",
            "Run ChatGPT Prompt 2 using exactly the same synthetic facts.",
            "Check one claim in Medscape AI/ClinicalKey AI and open the cited source.",
            "Demonstrate one bounded MDCalc input or medicine-reference verification.",
            "Record agreement, conflict, local-protocol fit and the clinician-owned decision."
        ],
        "checkpoint": "A licensed clinician owns urgency, diagnosis and disposition; a prescriber/pharmacist verifies medicines and approved sources.",
        "stop_rule": "Stop if the workflow delays urgent escalation, invents a finding or turns a hypothesis into a diagnosis.",
        "debrief": "Did the tools widen attention or create noise? Which claim remained unverified?",
    },
    {
        "id": 3,
        "title": "Patient + pharma communication",
        "minutes": 19,
        "specialised": ["Canva Magic Studio", "Gamma", "Bhashini", "Approved MI/PV workflow"],
        "prompts": [4, 7, 10],
        "input": "Approved public source excerpt for a class 6–8 patient handout, plus a separate synthetic unsolicited medical-information interaction containing a possible adverse event and an off-label question.",
        "outcome": "A reviewed patient asset, an MI/PV/PQC/MLR routing plan and an ethical professional-projection draft.",
        "steps": [
            "Use Prompt 4 to draft a one-page patient handout from the approved source only.",
            "Review meaning, red flags, teach-back and unsupported [REVIEW] statements.",
            "Use Canva/Gamma for design and Bhashini only as a draft language aid.",
            "Run Prompt 7 on the synthetic pharma inquiry and separate MI, off-label, PV/PQC and MLR responsibilities.",
            "Use Prompt 10 to create a useful, evidence-bounded professional asset.",
            "Apply the named clinical, bilingual and regulatory release gates."
        ],
        "checkpoint": "Nothing reaches a patient or external audience until the appropriate clinical, bilingual, MI/PV and MLR reviewers approve it.",
        "stop_rule": "Stop for unsupported claims, mistranslated clinical meaning, promotional drift or delayed adverse-event/product-quality escalation.",
        "debrief": "Can the patient act safely, and is every professional boundary visible?",
    },
    {
        "id": 4,
        "title": "Research + Socratic teaching",
        "minutes": 15,
        "specialised": ["PubMed", "Elicit", "ResearchRabbit", "Scite"],
        "prompts": [11, 9],
        "input": "PICO: ambient documentation versus usual documentation; outcomes include after-hours EHR time, note errors and patient experience. Use one verified seed source.",
        "outcome": "A transparent starting evidence map, uncertainty log and staged Socratic teaching script—not a fabricated systematic review.",
        "steps": [
            "Write the PICO and the decision it will inform.",
            "Build and record a PubMed query, date, filters and result count.",
            "Use Elicit to structure candidate evidence and verify fields in the original records.",
            "Use ResearchRabbit for adjacency and Scite for citation context—not as quality verdicts.",
            "Run Prompt 11 to create an evidence-map template and uncertainty log.",
            "Run Prompt 9 to turn the case into a commit–challenge–verify–revise dialogue."
        ],
        "checkpoint": "Open every source; verify design, population, outcome and limitation; faculty protects learner reasoning and originality.",
        "stop_rule": "Stop when a citation cannot be opened, a design is mislabelled or an AI summary outruns the source.",
        "debrief": "What is the defensible deliverable—and what remains outside this rapid workflow?",
    },
]


QUIZ = [
    {
        "q": "What is the first question before selecting a healthcare AI tool?",
        "options": ["Which model is newest?", "Will this improve patient attention, understanding, safety or continuity?", "Can it replace a professional?", "Is the demo visually impressive?"],
        "answer": 1,
        "why": "Patient value and the accountable decision come before brand or novelty."
    },
    {
        "q": "Which evidence label correctly describes the Qatar case?",
        "options": ["Randomised clinical trial", "Cross-sectional perception survey", "Prospective diagnostic validation", "Systematic review"],
        "answer": 1,
        "why": "The study captures perceptions; it does not establish clinical effectiveness."
    },
    {
        "q": "What is the safest role for an AI-generated differential?",
        "options": ["Final diagnosis", "Treatment order", "Hypothesis and missing-information aid", "Emergency reassurance"],
        "answer": 2,
        "why": "A licensed clinician owns diagnosis, urgency and disposition."
    },
    {
        "q": "What must overlap before accepting a clinical claim?",
        "options": ["Two AI tools", "AI output, opened evidence and local context", "A citation and a heatmap", "Vendor approval and user confidence"],
        "answer": 1,
        "why": "Citation presence alone is insufficient; the original evidence and local applicability must be checked."
    },
    {
        "q": "What does an ambient scribe create in addition to a draft note?",
        "options": ["No additional work", "A new review, consent and audit workflow", "A final diagnosis", "Automatic patient consent"],
        "answer": 1,
        "why": "Time saved at the keyboard creates verification, correction and governance responsibilities."
    },
    {
        "q": "What does an explainability heatmap prove?",
        "options": ["Clinical benefit", "Regulatory approval", "Nothing by itself about accuracy or benefit", "Fairness across groups"],
        "answer": 2,
        "why": "Explanations can support scrutiny but still be unstable or clinically irrelevant."
    },
    {
        "q": "Which rapid-research claim is honest?",
        "options": ["Systematic review completed in 15 minutes", "All citations are automatically verified", "A transparent starting map and uncertainty log", "Citation context is a quality verdict"],
        "answer": 2,
        "why": "Rapid discovery supports planning; it does not replace full search, selection, appraisal and synthesis."
    },
    {
        "q": "Which pharma interaction requires immediate escalation?",
        "options": ["A formatting request", "Possible adverse event or product-quality complaint", "A general literature question", "A request for a slide template"],
        "answer": 1,
        "why": "Safety and product-quality information must follow the approved SOP without delay."
    },
    {
        "q": "Which two POPLE dimensions are minimum gates in this programme?",
        "options": ["Ease and cost", "Patient value and effort", "Ownership and privacy", "Local fit and design"],
        "answer": 2,
        "why": "A high total score cannot compensate for missing accountability or unacceptable data governance."
    },
    {
        "q": "What should happen when a live specialised-tool demo fails?",
        "options": ["Cancel the station", "Use real patient data in another tool", "Use the prepared output, paired ChatGPT prompt and same checkpoint", "Skip the debrief"],
        "answer": 2,
        "why": "The learning objective is the workflow, comparison and human decision—not product theatre."
    },
]


def hero(title: str, subtitle: str, eyebrow: str = "Patient-Centric Healthcare 5.0") -> None:
    st.markdown(
        f"""
        <div class="hero">
          <div class="eyebrow">🩺 {eyebrow}</div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
          <div class="hero-grid">
            <div class="hero-stat"><strong>60 min</strong><span>Evidence-labelled theory</span></div>
            <div class="hero-stat"><strong>90 min</strong><span>Four-station workshop</span></div>
            <div class="hero-stat"><strong>7 cases</strong><span>Complete teaching chapters</span></div>
            <div class="hero-stat"><strong>11 prompts</strong><span>ChatGPT practice cards</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def safety_banner() -> None:
    st.markdown(
        """
        <div class="callout coral"><strong>Educational safety boundary.</strong>
        Use only synthetic/de-identified or approved public information. This app does not diagnose, prescribe,
        replace urgent care, release patient advice, or substitute for professional, organisational, legal or regulatory review.</div>
        """,
        unsafe_allow_html=True,
    )


def render_steps(steps: list[str]) -> None:
    for index, item in enumerate(steps, start=1):
        st.markdown(
            f'<div class="step"><div class="step-num">{index}</div><div class="step-copy">{item}</div></div>',
            unsafe_allow_html=True,
        )


def resource_download(file_name: str, label: str, key: str) -> None:
    file_path = RESOURCE_DIR / file_name
    if not file_path.exists():
        st.caption(f"{label}: add `{file_name}` to the resources folder.")
        return
    mime = {
        ".pdf": "application/pdf",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".zip": "application/zip",
    }.get(file_path.suffix.lower(), "application/octet-stream")
    st.download_button(label, data=file_path.read_bytes(), file_name=file_path.name, mime=mime, key=key, width="stretch")


def page_overview() -> None:
    hero("Patient-Centric Healthcare 5.0", "An interactive management-development programme for doctors and pharmaceutical professionals—connecting patient centricity, diagnostic support, research, professional projection and governed AI adoption.")
    safety_banner()
    st.markdown(
        """
        <div class="metric-row">
          <div class="metric-card"><span>Tool landscape</span><strong>93</strong></div>
          <div class="metric-card"><span>Sample-deck tools</span><strong>58</strong></div>
          <div class="metric-card"><span>Workshop shortlist</span><strong>18</strong></div>
          <div class="metric-card"><span>Total duration</span><strong>150 min</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.18, 0.82], gap="large")
    with left:
        st.subheader("Programme journey")
        st.markdown(
            """
            <div class="timeline">
              <div class="timeline-item"><div class="timeline-time">THEORY</div><div><div class="timeline-title">Seven cases → one operating question</div><div class="timeline-copy">Where does AI return attention or insight—and where must human ownership become stronger?</div></div></div>
              <div class="timeline-item"><div class="timeline-time">LAB 1</div><div><div class="timeline-title">Consultation continuity</div><div class="timeline-copy">Ambient documentation versus a structured ChatGPT draft.</div></div></div>
              <div class="timeline-item"><div class="timeline-time">LAB 2</div><div><div class="timeline-title">Diagnostic support + medicines</div><div class="timeline-copy">Hypotheses, missing information, evidence, calculators and references.</div></div></div>
              <div class="timeline-item"><div class="timeline-time">LAB 3</div><div><div class="timeline-title">Patient + pharma communication</div><div class="timeline-copy">Approved evidence, accessible design, MI/PV routing and professional projection.</div></div></div>
              <div class="timeline-item"><div class="timeline-time">LAB 4</div><div><div class="timeline-title">Research + teaching</div><div class="timeline-copy">Transparent evidence discovery and Socratic reasoning.</div></div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.subheader("Learning outcomes")
        st.markdown(
            """
            <div class="callout teal"><strong>Patient continuity</strong><br>Return attention, clarity, teach-back and follow-up to care.</div>
            <div class="callout blue"><strong>Diagnostic support</strong><br>Expose hypotheses, urgency and missing evidence without outsourcing diagnosis.</div>
            <div class="callout gold"><strong>Research</strong><br>Produce a transparent starting evidence map and uncertainty log.</div>
            <div class="callout coral"><strong>Own projection</strong><br>Build useful professional visibility without promotion or overclaiming.</div>
            """,
            unsafe_allow_html=True,
        )
    st.subheader("P-A-T-I-E-N-T operating system")
    framework = [
        ("P", "Protect privacy"), ("A", "Assess accuracy"), ("T", "Trace sources"),
        ("I", "Inform + consent"), ("E", "Examine equity"),
        ("N", "Never replace judgement"), ("T", "Take responsibility"),
    ]
    columns = st.columns(7)
    for column, (letter, label) in zip(columns, framework):
        with column:
            st.markdown(f'<div class="section-card" style="text-align:center"><h2 style="color:#e8694a">{letter}</h2><div class="small">{label}</div></div>', unsafe_allow_html=True)


def page_theory() -> None:
    hero("60-minute theory class", "A case-based sequence that keeps evidence design, limitations and human checkpoints visible.", "Exactly 60 minutes")
    safety_banner()
    st.subheader("Facilitator clock")
    for time, title, copy in THEORY_TIMELINE:
        st.markdown(f'<div class="timeline-item"><div class="timeline-time">{time}</div><div><div class="timeline-title">{title}</div><div class="timeline-copy">{copy}</div></div></div>', unsafe_allow_html=True)
    total = sum(int(item[0].split("–")[1]) - int(item[0].split("–")[0]) for item in THEORY_TIMELINE)
    st.success(f"Timing check: {total} minutes")
    st.subheader("Seven-case teaching matrix")
    rows = []
    for case in PROGRAM["cases"]:
        rows.append({
            "Case": case["short"], "Evidence design": case["evidence"],
            "Useful lesson": case["lesson"], "Do not overclaim": case["limitation"]
        })
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True, height=370)
    st.markdown('<div class="callout gold"><strong>Facilitation rule:</strong> every result must be spoken with its evidence label and limitation. A survey is not an effectiveness trial; a prototype is not an outcome study; an explanation is not proof.</div>', unsafe_allow_html=True)


def page_cases() -> None:
    hero("Complete case library", "Seven detailed teaching cases with management dilemmas, evidence appraisal, patient-centric risks, discussion guidance and matching workshop demonstrations.")
    safety_banner()
    labels = {case_id: f"Case {case_id}: {CASES[case_id]['short']}" for case_id in sorted(CASES)}
    selected_id = st.selectbox("Choose a case", options=list(labels), format_func=lambda item: labels[item])
    case = CASES[selected_id]
    extended = CASE_EXPANSIONS[selected_id]
    st.markdown(f"<span class='tag coral'>Case {case['id']}</span><span class='tag teal'>{case['evidence']}</span>", unsafe_allow_html=True)
    st.title(case["title"])
    st.markdown(f"**Management dilemma:** {extended['management_dilemma']}")
    overview, evidence, teaching, demo = st.tabs(["Case narrative", "Evidence + risks", "Discussion guide", "Workshop bridge"])
    with overview:
        st.markdown(f'<div class="callout blue"><strong>Context.</strong> {extended["case_context"]}</div>', unsafe_allow_html=True)
        for paragraph in extended["narrative"]:
            st.write(paragraph)
        st.markdown("#### Key facts")
        for item in extended["key_facts"]:
            st.markdown(f"- {item}")
        st.markdown("#### Stakeholders")
        st.write(" • ".join(extended["stakeholders"]))
    with evidence:
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown("#### Reported signal")
            st.info(case["result"])
            st.markdown("#### Evidence design")
            st.write(case["evidence"])
        with right:
            st.markdown("#### Limitation")
            st.markdown(f'<div class="evidence-box">{case["limitation"]}</div>', unsafe_allow_html=True)
            st.markdown("#### Human checkpoint")
            st.markdown(f'<div class="checkpoint">{case["human"]}</div>', unsafe_allow_html=True)
        st.markdown("#### Patient-centric risks")
        for risk in extended["patient_centric_risks"]:
            st.markdown(f"- {risk}")
        st.markdown(f"Source: [{case['url']}]({case['url']})")
    with teaching:
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown("#### Discussion questions")
            for index, question in enumerate(extended["discussion_questions"], start=1):
                st.markdown(f"**{index}.** {question}")
        with right:
            st.markdown("#### Suggested discussion direction")
            for item in extended["suggested_discussion"]:
                st.markdown(f"- {item}")
        st.markdown(f'<div class="callout gold"><strong>Transfer assignment.</strong> {extended["assignment"]}</div>', unsafe_allow_html=True)
    with demo:
        bridge = extended["demo_bridge"]
        st.markdown(f"### {bridge['title']}")
        st.markdown(f"<span class='tag blue'>{bridge['tools']}</span><span class='tag coral'>Prompt {bridge['prompt_id']}</span>", unsafe_allow_html=True)
        render_steps(bridge["steps"])
        st.markdown(f'<div class="callout teal"><strong>Expected output.</strong> {bridge["output"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="callout coral"><strong>Human checkpoint.</strong> {bridge["checkpoint"]}</div>', unsafe_allow_html=True)


def page_lab() -> None:
    hero("90-minute demonstration workshop", "Four timed stations pair purpose-built or specialised tools with ChatGPT practice so every participant can work—even when a premium account is facilitator-only.", "Exactly 90 minutes")
    safety_banner()
    totals = sum(station["minutes"] for station in STATIONS) + 8 + 7
    st.markdown(f'<div class="callout teal"><strong>Timing check.</strong> 8-minute launch + 75 minutes across four stations + 7-minute synthesis = {totals} minutes.</div>', unsafe_allow_html=True)
    station_id = st.selectbox("Open a station", [item["id"] for item in STATIONS], format_func=lambda value: f"Station {value}: {STATIONS[value-1]['title']} ({STATIONS[value-1]['minutes']} min)")
    station = STATIONS[station_id - 1]
    st.markdown(f"<span class='tag teal'>Station {station['id']}</span><span class='tag gold'>{station['minutes']} minutes</span>", unsafe_allow_html=True)
    st.header(station["title"])
    left, right = st.columns([1.15, .85], gap="large")
    with left:
        st.markdown("#### Specialised tools")
        tool_index = {item["name"]: item for item in TOOLS}
        for name in station["specialised"]:
            tool = tool_index.get(name)
            if tool:
                url = tool.get("demo_url") or tool.get("url")
                st.markdown(f"- **{name}** — {tool['access']} — [open tool/demo]({url})")
            else:
                st.markdown(f"- **{name}** — institutional/approved workflow")
        st.markdown("#### Synthetic/approved input")
        st.info(station["input"])
        st.markdown("#### Live demonstration sequence")
        render_steps(station["steps"])
    with right:
        st.markdown("#### ChatGPT practice")
        for prompt_id in station["prompts"]:
            prompt = PROMPTS[prompt_id]
            with st.expander(f"Prompt {prompt_id}: {prompt['title']}", expanded=prompt_id == station["prompts"][0]):
                st.code(PROGRAM["universal_wrapper"] + "\n\nTASK\n" + prompt["prompt"], language=None, wrap_lines=True)
                st.caption(f"Expected: {prompt['expected']}")
        st.markdown(f'<div class="checkpoint"><strong>Human checkpoint.</strong><br>{station["checkpoint"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="evidence-box" style="margin-top:.7rem"><strong>Stop rule.</strong><br>{station["stop_rule"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="callout gold"><strong>Debrief.</strong> {station["debrief"]}</div>', unsafe_allow_html=True)
    st.markdown(f"#### Participant output\n{station['outcome']}")
    st.text_area("Record the group's final human decision and verification evidence", key=f"lab_notes_{station_id}", height=130)


def page_prompts() -> None:
    hero("ChatGPT medical discussion studio", "Eleven copy-ready prompts for patient communication, diagnostic reasoning, medicines, governance, pharma safety, professional projection, research and teaching.")
    safety_banner()
    st.markdown("#### Universal safety wrapper")
    st.code(PROGRAM["universal_wrapper"], language=None, wrap_lines=True)
    prompt_id = st.selectbox("Choose a prompt", sorted(PROMPTS), format_func=lambda value: f"P{value}: {PROMPTS[value]['title']}")
    prompt = PROMPTS[prompt_id]
    left, right = st.columns([1.2, .8], gap="large")
    with left:
        st.markdown(f"### P{prompt_id} — {prompt['title']}")
        st.caption(prompt["purpose"])
        combined = PROGRAM["universal_wrapper"] + "\n\nTASK\n" + prompt["prompt"]
        st.code(combined, language=None, wrap_lines=True)
        st.download_button("Download this prompt", combined.encode("utf-8"), file_name=f"P{prompt_id}_{prompt['title'].replace(' ','_')}.txt", mime="text/plain", width="stretch")
    with right:
        st.markdown(f'<div class="callout teal"><strong>Expected output.</strong><br>{prompt["expected"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="callout coral"><strong>Human checkpoint.</strong><br>{prompt["checkpoint"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="callout gold"><strong>Failure to discuss.</strong><br>{prompt["failure"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="callout blue"><strong>Debrief.</strong><br>{prompt["discussion"]}</div>', unsafe_allow_html=True)
    st.markdown("#### Prompt-use checklist")
    checklist = ["Input is synthetic/de-identified or approved", "No diagnosis/prescribing request", "Unknowns and assumptions are separated", "Original sources will be opened", "Named professional will review", "Urgent escalation remains active"]
    columns = st.columns(2)
    for index, item in enumerate(checklist):
        columns[index % 2].checkbox(item, key=f"prompt_check_{prompt_id}_{index}")


def access_group(access: str) -> str:
    lower = access.lower()
    if "free" in lower and not any(word in lower for word in ["trial only"]):
        return "Free / free-tier"
    if any(word in lower for word in ["institutional", "enterprise", "paid", "demo", "trial"]):
        return "Paid / trial / institutional"
    return "Access varies"


def page_tools() -> None:
    hero("Medical AI tool explorer", "Filter the 93-tool research landscape, inspect the 58 tools found in the supplied sample deck, and focus on the 18-tool workshop shortlist.")
    safety_banner()
    frame = pd.DataFrame(TOOLS)
    frame["Access group"] = frame["access"].map(access_group)
    categories = sorted(frame["category"].dropna().unique())
    tiers = sorted(frame["tier"].dropna().unique())
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        selected_categories = st.multiselect("Category", categories)
    with c2:
        selected_access = st.multiselect("Access", sorted(frame["Access group"].unique()))
    with c3:
        selected_tiers = st.multiselect("Recommendation", tiers)
    with c4:
        sample_only = st.checkbox("Only tools from sample PPT")
    query = st.text_input("Search tool, use case or user group")
    filtered = frame.copy()
    if selected_categories:
        filtered = filtered[filtered["category"].isin(selected_categories)]
    if selected_access:
        filtered = filtered[filtered["Access group"].isin(selected_access)]
    if selected_tiers:
        filtered = filtered[filtered["tier"].isin(selected_tiers)]
    if sample_only:
        filtered = filtered[filtered["sample"] == "Yes"]
    if query:
        mask = filtered[["name", "use_case", "users", "category"]].fillna("").apply(lambda col: col.str.contains(query, case=False, regex=False)).any(axis=1)
        filtered = filtered[mask]
    st.caption(f"Showing {len(filtered)} of {len(frame)} researched tools")
    display = filtered[["name", "category", "use_case", "access", "india", "tier", "sample", "url", "demo_url"]].rename(columns={
        "name": "Tool", "category": "Category", "use_case": "Primary use", "access": "Access",
        "india": "India note", "tier": "Recommendation", "sample": "Sample PPT", "url": "Official URL", "demo_url": "Demo/sign-up"
    })
    st.dataframe(display, width="stretch", hide_index=True, height=480)
    csv = display.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered tool list", csv, "filtered_medical_ai_tools.csv", "text/csv")
    st.subheader("Access distribution")
    counts = frame.groupby("Access group").size().rename("Tools")
    st.bar_chart(counts, color="#087E78")
    st.markdown('<div class="callout gold"><strong>Interpretation.</strong> “Free” can still involve registration, professional verification, geographic limits or restricted features. Recheck pricing, intended use, data controls and regulatory status before delivery or procurement.</div>', unsafe_allow_html=True)


def page_readiness() -> None:
    hero("Demo readiness control room", "Turn an impressive tool list into a reliable workshop: accounts, privacy checks, synthetic inputs, fallbacks and human checkpoints.")
    safety_banner()
    shortlist = ["Heidi Health", "Nabla", "Abridge", "Medscape AI", "ClinicalKey AI", "VisualDx", "DxGPT", "iatroX", "MDCalc", "Epocrates", "ChatGPT", "Canva Magic Studio", "Gamma", "Bhashini", "PubMed", "Elicit", "ResearchRabbit", "Scite"]
    tool_index = {item["name"]: item for item in TOOLS}
    ready_count = 0
    for index, name in enumerate(shortlist):
        tool = tool_index.get(name, {})
        with st.expander(f"{name} — {tool.get('access','Access varies')}"):
            c1, c2, c3, c4 = st.columns(4)
            account = c1.checkbox("Account/login tested", key=f"ready_account_{index}")
            privacy = c2.checkbox("Privacy check passed", key=f"ready_privacy_{index}")
            synthetic = c3.checkbox("Synthetic input ready", value=True, key=f"ready_input_{index}")
            fallback = c4.checkbox("Screenshot fallback ready", value=True, key=f"ready_fallback_{index}")
            if account and privacy and synthetic and fallback:
                ready_count += 1
            url = tool.get("demo_url") or tool.get("url")
            st.caption(f"India/access note: {tool.get('india','Verify current access')} | {url}")
    completion = ready_count / len(shortlist)
    st.progress(completion, text=f"{ready_count}/{len(shortlist)} tools fully ready")
    if ready_count == len(shortlist):
        st.success("All tool-level readiness gates are complete. Perform the final room/network test.")
    else:
        st.warning("Pending items are normal during preparation. A tool without access or privacy approval must use the prepared fallback.")
    st.subheader("Final go/no-go gates")
    gates = ["No identifiable patient data", "Named reviewer", "Urgent escalation path", "Official URL opens", "Account/region verified", "Synthetic label visible", "Fallback opens", "Expected output known", "Stop rule announced"]
    gate_cols = st.columns(3)
    for index, gate in enumerate(gates):
        gate_cols[index % 3].checkbox(gate, key=f"final_gate_{index}")


def page_assessment() -> None:
    hero("Knowledge check", "Ten questions assess evidence labelling, clinical boundaries, pharma escalation, research integrity and demo resilience.")
    safety_banner()
    with st.form("assessment_form"):
        responses = []
        for index, item in enumerate(QUIZ, start=1):
            st.markdown(f"**{index}. {item['q']}**")
            response = st.radio("Choose one", options=range(len(item["options"])), format_func=lambda option, choices=item["options"]: choices[option], key=f"quiz_{index}", index=None)
            responses.append(response)
        submitted = st.form_submit_button("Submit assessment", width="stretch")
    if submitted:
        score = sum(response == item["answer"] for response, item in zip(responses, QUIZ))
        st.markdown(f'<div class="metric-card"><span>Assessment score</span><strong>{score}/10</strong></div>', unsafe_allow_html=True)
        if score >= 8:
            st.success("Strong readiness. Use the case discussion and workshop to deepen transfer.")
        elif score >= 6:
            st.warning("Good foundation. Revisit evidence labels, human checkpoints and escalation rules.")
        else:
            st.error("Revisit the theory and prompt-studio sections before facilitating or applying the workflows.")
        for index, (response, item) in enumerate(zip(responses, QUIZ), start=1):
            if response == item["answer"]:
                st.markdown(f"**{index}. Correct.** {item['why']}")
            else:
                correct = item["options"][item["answer"]]
                st.markdown(f"**{index}. Review.** Correct answer: *{correct}*. {item['why']}")


def page_downloads() -> None:
    hero("Programme downloads", "Use the editable files for delivery and the PDFs for distribution. The deployment package contains this app and its supporting data.")
    cols = st.columns(3)
    resources = [
        ("Patient_Centricity_Healthcare_5_0_150min.pptx", "Download presentation", "pptx"),
        ("Patient_Centricity_Healthcare_5_0_150min.pdf", "Download presentation PDF", "pdf"),
        ("Patient_Centricity_Complete_Handbook.docx", "Download handbook DOCX", "handbook_docx"),
        ("Patient_Centricity_Complete_Handbook.pdf", "Download handbook PDF", "handbook_pdf"),
        ("Facilitator_Guide_150min.docx", "Download facilitator guide", "fac"),
        ("Participant_Workbook_150min.docx", "Download participant workbook", "part"),
        ("ChatGPT_Medical_Discussion_Prompt_Cards.pdf", "Download prompt cards", "prompts"),
        ("Medical_AI_Tool_Matrix_Workshop.xlsx", "Download tool matrix", "tools"),
        ("Verified_URLs_Cases_and_References.xlsx", "Download verified URLs", "refs"),
        ("Demo_Readiness_Checklist.xlsx", "Download readiness checklist", "ready"),
    ]
    for index, item in enumerate(resources):
        with cols[index % 3]:
            resource_download(*item)
    st.markdown("#### Deployment")
    st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")
    st.caption("For Streamlit Community Cloud, push this folder to GitHub and select app.py as the entry point.")


def page_about() -> None:
    hero("About the programme", "Designed and facilitated by Dr. Alok Tiwari, Assistant Professor – Big Data Analytics, Goa Institute of Management.")
    st.markdown(
        """
        ### Design philosophy

        The programme treats patient centricity as an operating discipline: technology should return attention,
        strengthen understanding, expose uncertainty, support continuity and preserve accountable human decisions.

        ### Audience

        - Doctors, clinical leaders and healthcare managers
        - Pharmaceutical medical, evidence, safety, patient-engagement and learning professionals
        - Faculty and researchers working with healthcare AI

        ### App characteristics

        - No API key required
        - No patient-data storage or clinical inference
        - All exercises use synthetic or approved information
        - Tool access and pricing must be rechecked before delivery
        """
    )
    st.markdown('<div class="callout teal"><strong>Programme principle.</strong> AI assists. Professionals decide. Patients remain the purpose.</div>', unsafe_allow_html=True)


PAGES = {
    "Overview": page_overview,
    "60-min Theory": page_theory,
    "Complete Cases": page_cases,
    "90-min Workshop": page_lab,
    "Prompt Studio": page_prompts,
    "Medical Tool Explorer": page_tools,
    "Demo Readiness": page_readiness,
    "Assessment": page_assessment,
    "Downloads": page_downloads,
    "About": page_about,
}


with st.sidebar:
    st.markdown("## 🩺 Patient-Centric\n### Healthcare 5.0")
    st.caption("Interactive MDP Learning Studio")
    selected_page = st.radio("Navigate", list(PAGES), label_visibility="collapsed")
    st.divider()
    st.markdown("**Programme clock**")
    st.progress(60 / 150, text="60 min theory")
    st.progress(90 / 150, text="90 min workshop")
    st.caption("Doctors × Pharma Professionals")
    st.caption("Dr. Alok Tiwari • Goa Institute of Management")


PAGES[selected_page]()
st.markdown('<div class="footer">Patient-Centric Healthcare 5.0 • Educational use • Verify current sources, access, policies and professional responsibilities before application</div>', unsafe_allow_html=True)
