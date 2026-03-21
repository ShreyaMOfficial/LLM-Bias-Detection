# app.py

import streamlit as st
import plotly.graph_objects as go
from text_generator import generate_text
from modules.bias_detector import detect_bias
from modules.llm_analyzer import analyze_bias_with_llm

st.set_page_config(
    page_title="Bias Lens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400;1,700&family=Source+Serif+4:ital,wght@0,300;0,400;0,600;1,300;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --ink:       #1a1410;
    --paper:     #f5f0e8;
    --cream:     #ede8dc;
    --warm-mid:  #c8bfaa;
    --rule:      #2a2018;
    --red:       #c0392b;
    --amber:     #d4860a;
    --green:     #2d6a4f;
    --blue:      #1a3a5c;
    --muted:     #6b6050;
    --highlight: #fff3cd;
}

* { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Source Serif 4', Georgia, serif !important;
    background-color: var(--paper) !important;
    color: var(--ink) !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem !important; max-width: 1100px !important; }

/* ── MASTHEAD ── */
.masthead {
    border-top: 4px solid var(--rule);
    border-bottom: 1px solid var(--rule);
    padding: 1.2rem 0 1rem 0;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
}
.masthead-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.8rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    color: var(--ink);
    line-height: 1;
}
.masthead-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--muted);
    text-align: right;
    line-height: 1.6;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.masthead-rule {
    border: none;
    border-top: 3px double var(--rule);
    margin: 0.4rem 0 1.5rem 0;
}

/* ── DECK / SUBTITLE ── */
.deck {
    font-family: 'Source Serif 4', serif;
    font-size: 1.05rem;
    font-style: italic;
    font-weight: 300;
    color: var(--muted);
    margin-bottom: 1.8rem;
    border-left: 3px solid var(--warm-mid);
    padding-left: 0.8rem;
    line-height: 1.5;
}

/* ── INPUT AREA ── */
.input-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-bottom: 0.3rem;
}
div[data-testid="stTextInput"] input {
    background: white !important;
    border: 1.5px solid var(--rule) !important;
    border-radius: 0 !important;
    color: var(--ink) !important;
    font-family: 'Source Serif 4', serif !important;
    font-size: 1rem !important;
    padding: 0.6rem 0.9rem !important;
    box-shadow: 2px 2px 0 var(--warm-mid) !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--red) !important;
    box-shadow: 2px 2px 0 var(--red) !important;
    outline: none !important;
}
div[data-testid="stButton"] button {
    background: var(--ink) !important;
    color: var(--paper) !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 1rem !important;
    width: 100% !important;
    transition: background 0.15s !important;
}
div[data-testid="stButton"] button:hover {
    background: var(--red) !important;
}

/* ── SECTION RULES ── */
.section-rule {
    border: none;
    border-top: 2px solid var(--ink);
    margin: 1.8rem 0 0.6rem 0;
}
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--muted);
    margin-bottom: 0.8rem;
}
.section-headline {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 0.6rem;
    line-height: 1.2;
}

/* ── GENERATED TEXT ── */
.article-body {
    font-family: 'Source Serif 4', serif;
    font-size: 0.97rem;
    line-height: 1.8;
    color: var(--ink);
    background: white;
    border: 1px solid var(--warm-mid);
    padding: 1.4rem 1.6rem;
    border-left: 4px solid var(--ink);
    box-shadow: 3px 3px 0 var(--cream);
    margin-bottom: 1rem;
}

/* ── VERDICT STRIP ── */
.verdict-strip {
    display: flex;
    gap: 0;
    border: 1.5px solid var(--ink);
    margin: 1.4rem 0;
    box-shadow: 3px 3px 0 var(--warm-mid);
}
.verdict-cell {
    flex: 1;
    padding: 0.9rem 1rem;
    border-right: 1px solid var(--warm-mid);
    background: white;
    text-align: center;
}
.verdict-cell:last-child { border-right: none; }
.verdict-num {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 900;
    line-height: 1;
    color: var(--ink);
}
.verdict-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-top: 0.2rem;
}

/* ── SEVERITY PILL ── */
.sev-none   { display:inline-block;padding:.2rem .7rem;font-family:'JetBrains Mono',monospace;font-size:.72rem;font-weight:500;letter-spacing:.06em;text-transform:uppercase;background:#e8f5e9;color:var(--green);border:1.5px solid var(--green); }
.sev-low    { display:inline-block;padding:.2rem .7rem;font-family:'JetBrains Mono',monospace;font-size:.72rem;font-weight:500;letter-spacing:.06em;text-transform:uppercase;background:#fff8e1;color:var(--amber);border:1.5px solid var(--amber); }
.sev-medium { display:inline-block;padding:.2rem .7rem;font-family:'JetBrains Mono',monospace;font-size:.72rem;font-weight:500;letter-spacing:.06em;text-transform:uppercase;background:#fff3e0;color:#e65100;border:1.5px solid #e65100; }
.sev-high   { display:inline-block;padding:.2rem .7rem;font-family:'JetBrains Mono',monospace;font-size:.72rem;font-weight:500;letter-spacing:.06em;text-transform:uppercase;background:#ffebee;color:var(--red);border:1.5px solid var(--red); }

/* ── NO BIAS ── */
.clean-verdict {
    background: #f0f7f4;
    border: 1.5px solid var(--green);
    border-left: 5px solid var(--green);
    padding: 1.2rem 1.5rem;
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-style: italic;
    color: var(--green);
    margin: 1rem 0;
}

/* ── LAYER HEADERS ── */
.layer-head {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 1.6rem 0 0.4rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--warm-mid);
}
.layer-num {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 900;
    color: var(--ink);
    line-height: 1;
}
.layer-title {
    font-family: 'Source Serif 4', serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--ink);
}
.layer-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.15rem 0.5rem;
    border: 1px solid var(--warm-mid);
    color: var(--muted);
    background: var(--cream);
}
.layer-desc {
    font-family: 'Source Serif 4', serif;
    font-size: 0.82rem;
    font-style: italic;
    color: var(--muted);
    margin-bottom: 0.8rem;
    line-height: 1.5;
}

/* ── FINDING CARDS ── */
.finding {
    background: white;
    border: 1px solid var(--warm-mid);
    border-left: 4px solid var(--ink);
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 2px 2px 0 var(--cream);
}
.finding-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.4rem;
}
.finding-type {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    background: var(--cream);
    border: 1px solid var(--warm-mid);
    padding: 0.1rem 0.5rem;
}
.finding-title {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 0.3rem;
    font-style: italic;
}
.finding-quote {
    font-family: 'Source Serif 4', serif;
    font-size: 0.85rem;
    font-style: italic;
    color: var(--blue);
    background: #f0f4f8;
    border-left: 3px solid var(--blue);
    padding: 0.4rem 0.7rem;
    margin: 0.4rem 0;
    line-height: 1.5;
}
.finding-body {
    font-family: 'Source Serif 4', serif;
    font-size: 0.87rem;
    color: #3a3028;
    line-height: 1.6;
    margin-top: 0.4rem;
}
.finding-context {
    font-family: 'Source Serif 4', serif;
    font-size: 0.78rem;
    font-style: italic;
    color: var(--muted);
    margin-top: 0.5rem;
    border-top: 1px solid var(--cream);
    padding-top: 0.4rem;
}

/* ── ASSESSMENT BOX ── */
.assessment {
    background: var(--highlight);
    border: 1px solid #e6c84a;
    border-left: 4px solid var(--amber);
    padding: 0.9rem 1.2rem;
    font-family: 'Source Serif 4', serif;
    font-size: 0.9rem;
    font-style: italic;
    color: var(--ink);
    line-height: 1.6;
    margin-bottom: 1rem;
}

/* ── EMPTY STATE ── */
.empty-layer {
    font-family: 'Source Serif 4', serif;
    font-size: 0.88rem;
    font-style: italic;
    color: var(--muted);
    padding: 0.7rem 1rem;
    background: var(--cream);
    border: 1px solid var(--warm-mid);
}

/* ── REASONING LOG ── */
.log-row {
    display: flex;
    gap: 0.8rem;
    padding: 0.45rem 0;
    border-bottom: 1px solid var(--cream);
    font-size: 0.83rem;
    line-height: 1.5;
}
.log-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--warm-mid);
    min-width: 1.5rem;
    padding-top: 0.1rem;
}
.log-text { color: var(--muted); font-family: 'Source Serif 4', serif; font-style: italic; }

/* ── FOOTER ── */
.footer-rule {
    border: none;
    border-top: 3px double var(--rule);
    margin: 3rem 0 0.6rem 0;
}
.footer-txt {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: var(--warm-mid);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    text-align: center;
}

/* Plotly transparent bg */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── MASTHEAD ────────────────────────────────────────────────
import datetime
today = datetime.date.today().strftime("%B %d, %Y").upper()

st.markdown(f"""
<div class="masthead">
    <div class="masthead-title">Bias Lens</div>
    <div class="masthead-meta">
        Gender & Age Bias Detection<br>
        Dual-Layer Analysis System<br>
        {today}
    </div>
</div>
<hr class="masthead-rule">
<div class="deck">
    An investigative tool that generates text from any prompt and examines it for gender and age bias —
    using a trained ML classifier alongside AI contextual reasoning.
</div>
""", unsafe_allow_html=True)

# ── INPUT ────────────────────────────────────────────────────
st.markdown('<div class="input-label">Enter a topic or question to analyze</div>', unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])
with col_input:
    prompt = st.text_input(
        label="prompt",
        placeholder='e.g.  "Why do men make better leaders than women?"',
        label_visibility="collapsed"
    )
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("Run Analysis")

def sev_class(sev):
    return {"None":"sev-none","Low":"sev-low","Medium":"sev-medium","High":"sev-high"}.get(sev,"sev-none")

# ── MAIN LOGIC ───────────────────────────────────────────────
if run:
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating text…"):
            try:
                generated_text = generate_text(prompt)
            except Exception as e:
                st.error(f"Text generation failed: {e}")
                st.stop()

        if not generated_text:
            st.error("The model returned empty text. Try a different prompt.")
            st.stop()

        with st.spinner("Running ML bias classifier…"):
            try:
                rule_result = detect_bias(generated_text)
            except Exception as e:
                st.error(f"Rule-based detection failed: {e}")
                st.stop()

        with st.spinner("Running AI contextual analysis…"):
            try:
                llm_result = analyze_bias_with_llm(generated_text)
            except Exception as e:
                llm_result = {"biases_found":[],"overall_assessment":f"Unavailable: {e}","overall_severity":"None"}

        # ── GENERATED TEXT ───────────────────────────────────
        st.markdown('<hr class="section-rule">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Generated Text</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="article-body">{generated_text}</div>', unsafe_allow_html=True)

        # ── VERDICT STRIP ────────────────────────────────────
        all_bias_types = list(set(
            rule_result["bias_types"] +
            [b["bias_type"] for b in llm_result.get("biases_found",[])]
        ))
        sev_order = {"None":0,"Low":1,"Medium":2,"High":3}
        combined_sev = max(
            rule_result["severity"],
            llm_result.get("overall_severity","None"),
            key=lambda s: sev_order.get(s,0)
        )
        total_llm = len(llm_result.get("biases_found",[]))

        st.markdown(f"""
        <div class="verdict-strip">
            <div class="verdict-cell">
                <div class="verdict-num">{rule_result["bias_score"]}</div>
                <div class="verdict-lbl">ML Score</div>
            </div>
            <div class="verdict-cell">
                <div class="verdict-num">{total_llm}</div>
                <div class="verdict-lbl">AI Findings</div>
            </div>
            <div class="verdict-cell">
                <div class="verdict-num" style="font-size:1.1rem;padding-top:.5rem;">
                    <span class="{sev_class(combined_sev)}">{combined_sev}</span>
                </div>
                <div class="verdict-lbl">Overall Severity</div>
            </div>
            <div class="verdict-cell">
                <div class="verdict-num">{len(all_bias_types)}</div>
                <div class="verdict-lbl">Bias Types</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── NO BIAS ───────────────────────────────────────────
        if not rule_result["bias_detected"] and total_llm == 0:
            st.markdown("""
            <div class="clean-verdict">
                ✓ &nbsp; No significant gender or age bias detected in this text.
            </div>""", unsafe_allow_html=True)

        else:
            # ── CHARTS ───────────────────────────────────────
            st.markdown('<hr class="section-rule">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Visual Summary</div>', unsafe_allow_html=True)

            ch_left, ch_right = st.columns(2)

            with ch_left:
                if all_bias_types:
                    colors = ["#1a3a5c","#c0392b","#d4860a","#2d6a4f","#6b3fa0","#7a5230"]
                    fig_pie = go.Figure(go.Pie(
                        labels=all_bias_types,
                        values=[1]*len(all_bias_types),
                        hole=0.5,
                        marker=dict(colors=colors[:len(all_bias_types)],
                                    line=dict(color="#f5f0e8", width=3)),
                        textfont=dict(color="white", size=10, family="JetBrains Mono"),
                        hovertemplate="%{label}<extra></extra>"
                    ))
                    fig_pie.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#6b6050", family="Source Serif 4"),
                        margin=dict(l=10,r=10,t=30,b=10), height=230,
                        title=dict(text="Bias Categories", font=dict(family="Playfair Display", size=13, color="#1a1410"), x=0),
                        legend=dict(font=dict(color="#3a3028",size=10,family="Source Serif 4"), bgcolor="rgba(0,0,0,0)")
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

            with ch_right:
                gauge_color = {"None":"#2d6a4f","Low":"#d4860a","Medium":"#e65100","High":"#c0392b"}.get(combined_sev,"#1a3a5c")
                max_score = max(rule_result["bias_score"], 10)
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=rule_result["bias_score"],
                    number={"font":{"color":"#1a1410","family":"Playfair Display","size":30}},
                    title={"text":"ML Bias Score","font":{"family":"Playfair Display","size":13,"color":"#1a1410"}},
                    gauge={
                        "axis":{"range":[0,max_score+2],"tickwidth":1,"tickcolor":"#c8bfaa",
                                "tickfont":{"color":"#6b6050","size":9,"family":"JetBrains Mono"}},
                        "bar":{"color":gauge_color,"thickness":0.3},
                        "bgcolor":"white","borderwidth":1,"bordercolor":"#c8bfaa",
                        "steps":[
                            {"range":[0,2],"color":"#f0f7f4"},
                            {"range":[2,5],"color":"#fff8e1"},
                            {"range":[5,max_score+2],"color":"#fff0f0"}
                        ],
                        "threshold":{"line":{"color":gauge_color,"width":2},"thickness":0.8,"value":rule_result["bias_score"]}
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=20,r=20,t=40,b=10), height=230
                )
                st.plotly_chart(fig_gauge, use_container_width=True)

            # ── LAYER 1 ───────────────────────────────────────
            st.markdown("""
            <div class="layer-head">
                <div class="layer-num">I</div>
                <div>
                    <div class="layer-title">ML Classifier &nbsp;<span class="layer-tag">RoBERTa + ModernBERT</span></div>
                </div>
            </div>
            <div class="layer-desc">
                Sentence-level detection using two fine-tuned transformer models.
                himel7/bias-detector (92% accuracy) flags biased sentences;
                cirimus/modernbert classifies gender vs. age type.
            </div>
            """, unsafe_allow_html=True)

            if not rule_result["bias_detected"]:
                st.markdown('<div class="empty-layer">No explicit bias patterns flagged by the ML classifier.</div>', unsafe_allow_html=True)
            else:
                for e in rule_result["evidence"]:
                    conf = e.get("confidence","")
                    conf_html = f'<span style="font-family:JetBrains Mono,monospace;font-size:.65rem;color:var(--muted);">{conf}% confidence</span>' if conf else ""
                    sent_html = f'<div class="finding-context">Sentence: "{e.get("sentence","")}"</div>' if e.get("sentence") else ""
                    st.markdown(f"""
                    <div class="finding">
                        <div class="finding-top">
                            <span class="finding-type">{e.get("type","Bias")}</span>
                            {conf_html}
                        </div>
                        <div class="finding-quote">{e.get("text","")}</div>
                        <div class="finding-body">{e.get("explanation","")}</div>
                        {sent_html}
                    </div>""", unsafe_allow_html=True)

                st.markdown('<div class="section-label" style="margin-top:1rem;">Classifier Log</div>', unsafe_allow_html=True)
                for i, r in enumerate(rule_result["reasons"],1):
                    st.markdown(f'<div class="log-row"><span class="log-num">{i:02d}</span><span class="log-text">{r}</span></div>', unsafe_allow_html=True)

            # ── LAYER 2 ───────────────────────────────────────
            st.markdown("""
            <div class="layer-head">
                <div class="layer-num">II</div>
                <div>
                    <div class="layer-title">AI Contextual Analysis &nbsp;<span class="layer-tag">Llama 3.3 70B</span></div>
                </div>
            </div>
            <div class="layer-desc">
                Deep contextual reasoning — catches occupational gender coding, name-role stereotyping,
                implicit age framing, invisibility bias, double standards, and trait essentialism.
            </div>
            """, unsafe_allow_html=True)

            if llm_result.get("overall_assessment"):
                st.markdown(f'<div class="assessment">"{llm_result["overall_assessment"]}"</div>', unsafe_allow_html=True)

            if not llm_result.get("biases_found"):
                st.markdown('<div class="empty-layer">No subtle contextual biases detected by AI analysis.</div>', unsafe_allow_html=True)
            else:
                sev_colors = {"Low":("#fff8e1","#d4860a"),"Medium":("#fff3e0","#e65100"),"High":("#ffebee","#c0392b"),"None":("#f0f7f4","#2d6a4f")}
                for b in llm_result["biases_found"]:
                    b_sev = b.get("severity","Low")
                    bg, fg = sev_colors.get(b_sev,("#fff8e1","#d4860a"))
                    st.markdown(f"""
                    <div class="finding" style="border-left-color:{fg};">
                        <div class="finding-top">
                            <span class="finding-type">{b.get("bias_type","Bias")}</span>
                            <span style="font-family:JetBrains Mono,monospace;font-size:.65rem;
                                         background:{bg};color:{fg};padding:.1rem .5rem;
                                         border:1px solid {fg};">{b_sev}</span>
                        </div>
                        <div class="finding-title">{b.get("title","")}</div>
                        <div class="finding-quote">{b.get("evidence","")}</div>
                        <div class="finding-body">{b.get("explanation","")}</div>
                    </div>""", unsafe_allow_html=True)

# ── FOOTER ──────────────────────────────────────────────────
st.markdown("""
<hr class="footer-rule">
<div class="footer-txt">
    Bias Lens &nbsp;·&nbsp; Gender & Age Bias Detection
    &nbsp;·&nbsp; RoBERTa + ModernBERT + Llama 3.3 70B &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)