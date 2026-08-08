"""
India Pharma & Healthcare Stock Tracker
Comprehensive AI-powered analysis dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from company_data import COMPANIES, SECTOR_TYPES, get_company_data

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Pharma & Healthcare Tracker",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #0f3460 0%, #16213e 50%, #0f3460 100%);
        padding: 24px 32px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .main-header h1 { margin: 0; font-size: 2.0rem; font-weight: 700; }
    .main-header p { margin: 6px 0 0; opacity: 0.82; font-size: 0.95rem; }

    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border-left: 4px solid #0f3460;
        height: 100%;
    }
    .metric-label { font-size: 0.78rem; color: #888; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 1.55rem; font-weight: 700; color: #0f3460; margin: 4px 0 0; }
    .metric-sub { font-size: 0.8rem; color: #555; margin-top: 2px; }

    /* Section headers */
    .section-header {
        background: #f0f4ff;
        border-left: 4px solid #0f3460;
        padding: 10px 16px;
        border-radius: 0 8px 8px 0;
        margin: 20px 0 14px;
        font-weight: 700;
        font-size: 1.05rem;
        color: #0f3460;
    }

    /* Score badge */
    .score-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .score-high { background: #d4edda; color: #155724; }
    .score-mid  { background: #fff3cd; color: #856404; }
    .score-low  { background: #f8d7da; color: #721c24; }

    /* Red flag  */
    .red-flag {
        background: #fff5f5;
        border: 1px solid #fed7d7;
        border-left: 4px solid #e53e3e;
        border-radius: 6px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 0.88rem;
        color: #742a2a;
    }

    /* Bull / bear */
    .bull-point {
        background: #f0fff4;
        border-left: 3px solid #38a169;
        border-radius: 0 6px 6px 0;
        padding: 8px 12px;
        margin: 4px 0;
        font-size: 0.87rem;
        color: #276749;
    }
    .bear-point {
        background: #fff5f5;
        border-left: 3px solid #e53e3e;
        border-radius: 0 6px 6px 0;
        padding: 8px 12px;
        margin: 4px 0;
        font-size: 0.87rem;
        color: #742a2a;
    }

    /* Concall card */
    .concall-card {
        background: #f8faff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        margin: 10px 0;
    }
    .concall-header { font-weight: 700; color: #0f3460; font-size: 1.0rem; }
    .guidance-met   { color: #276749; font-weight: 600; }
    .guidance-miss  { color: #742a2a; font-weight: 600; }
    .guidance-prog  { color: #744210; font-weight: 600; }

    /* Pill tags */
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 2px;
    }
    .tag-pharma  { background: #ebf8ff; color: #2b6cb0; }
    .tag-hospital{ background: #fff5f5; color: #c53030; }
    .tag-pipeline{ background: #fffbeb; color: #b7791f; }

    /* Pipeline stage */
    .stage-pill {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 0.76rem;
        font-weight: 700;
    }
    .stage-marketed { background: #c6f6d5; color: #22543d; }
    .stage-ph3      { background: #bee3f8; color: #1a365d; }
    .stage-ph2      { background: #fefcbf; color: #744210; }
    .stage-ph1      { background: #fed7d7; color: #742a2a; }
    .stage-pending  { background: #e9d8fd; color: #44337a; }

    /* Sidebar */
    .sidebar-section {
        background: #f0f4ff;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
    }

    /* Data table styling */
    .stDataFrame { border-radius: 8px; overflow: hidden; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 18px;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        color: #aaa;
        font-size: 0.78rem;
        margin-top: 40px;
        padding: 16px;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)


# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────
def fmt_cr(val):
    if val >= 100000:
        return f"₹{val/100000:.1f}L Cr"
    elif val >= 1000:
        return f"₹{val/1000:.1f}K Cr"
    return f"₹{val:,.0f} Cr"

def get_score_class(score):
    if score >= 8:   return "score-high"
    if score >= 6.5: return "score-mid"
    return "score-low"

def get_stage_class(stage_text):
    s = stage_text.lower()
    if "marketed" in s or "market" in s:     return "stage-marketed"
    if "phase iii" in s or "phase 3" in s:   return "stage-ph3"
    if "phase ii" in s or "phase 2" in s:    return "stage-ph2"
    if "phase i" in s or "phase 1" in s:     return "stage-ph1"
    return "stage-pending"

def pct_change(old, new):
    if old == 0: return 0
    return round((new - old) / old * 100, 1)

def color_metric(val, positive_good=True):
    if val > 0:
        return "🟢" if positive_good else "🔴"
    elif val < 0:
        return "🔴" if positive_good else "🟢"
    return "⚪"


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 18px;'>
        <div style='font-size:2.5rem;'>💊</div>
        <div style='font-size:1.1rem; font-weight:700; color:#0f3460;'>Pharma & Healthcare</div>
        <div style='font-size:0.78rem; color:#888;'>India Listed Stock Tracker</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    sector_filter = st.selectbox(
        "🔍 Filter by Sector",
        ["All", "Pharma / CRDMO", "Hospitals / Healthcare"],
        help="Filter companies by sector type"
    )

    filtered = {}
    for k, v in COMPANIES.items():
        if sector_filter == "All":
            filtered[k] = v
        elif sector_filter == "Pharma / CRDMO" and v["type"] == "pharma":
            filtered[k] = v
        elif sector_filter == "Hospitals / Healthcare" and v["type"] == "hospital":
            filtered[k] = v

    company_options = {k: f"{v['name']} ({k})" for k, v in filtered.items()}
    selected_key = st.selectbox(
        "🏢 Select Company",
        list(company_options.keys()),
        format_func=lambda x: company_options[x],
    )

    co = get_company_data(selected_key)
    st.markdown("---")

    # Quick stats in sidebar
    if co:
        st.markdown(f"""
        <div class='sidebar-section'>
            <div style='font-size:0.78rem; color:#888; font-weight:600;'>QUICK STATS</div>
            <div style='margin-top:8px;'>
                <b>HQ:</b> {co['hq']}<br>
                <b>Type:</b> <span class='tag tag-{"pharma" if co["type"]=="pharma" else "hospital"}'>{co['type'].upper()}</span><br>
                <b>Founded:</b> {co['founded']}<br>
                <b>CMP:</b> ₹{co['cmp']:,}<br>
                <b>Mkt Cap:</b> {fmt_cr(co['market_cap_cr'])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        fy26 = co["financials"]["FY2026"]
        fy25 = co["financials"]["FY2025"]
        rev_growth = pct_change(fy25["revenue"], fy26["revenue"])

        st.markdown(f"""
        <div class='sidebar-section'>
            <div style='font-size:0.78rem; color:#888; font-weight:600;'>FY26 FINANCIALS</div>
            <div style='margin-top:8px; font-size:0.88rem;'>
                <b>Revenue:</b> {fmt_cr(fy26['revenue'])} ({color_metric(rev_growth)}{rev_growth:+.1f}% YoY)<br>
                <b>EBITDA%:</b> {fy26['ebitda_margin']:.1f}%<br>
                <b>PAT:</b> {fmt_cr(fy26['pat'])}<br>
                <b>EPS:</b> ₹{fy26['eps']:.1f}
            </div>
        </div>
        """, unsafe_allow_html=True)

        ai = co["ai_analysis"]
        score = ai["overall_score"]
        sc = get_score_class(score)
        st.markdown(f"""
        <div class='sidebar-section'>
            <div style='font-size:0.78rem; color:#888; font-weight:600;'>AI ASSESSMENT</div>
            <div style='margin-top:8px; text-align:center;'>
                <span class='score-badge {sc}'>{score}/10</span>
                <div style='font-size:0.82rem; margin-top:6px; font-weight:600;'>{ai["recommendation"][:45]}...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#aaa; text-align:center;'>
        Data sourced from public filings, annual reports, investor presentations & earnings calls.<br><br>
        ⚠️ For educational use only. Not investment advice.
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
if not co:
    st.error("Company data not found. Please select a valid company.")
    st.stop()

# Header
st.markdown(f"""
<div class='main-header'>
    <h1>{'💊' if co['type']=='pharma' else '🏥'} {co['name']}</h1>
    <p>
        <span class='tag tag-{"pharma" if co["type"]=="pharma" else "hospital"}' style='background:rgba(255,255,255,0.2); color:white;'>
            {co['type'].upper()}
        </span>
        &nbsp;|&nbsp; {co['hq']}
        &nbsp;|&nbsp; NSE: {selected_key}
        &nbsp;|&nbsp; Founded: {co['founded']}
        &nbsp;|&nbsp; CMP: ₹{co['cmp']:,}
    </p>
</div>
""", unsafe_allow_html=True)

# ── Top-line snapshot ──────────────────────────────────────────────────────────
fy26 = co["financials"]["FY2026"]
fy25 = co["financials"]["FY2025"]
fy24 = co["financials"]["FY2024"]

c1, c2, c3, c4, c5, c6 = st.columns(6)
metrics = [
    ("Market Cap", fmt_cr(co['market_cap_cr']), ""),
    ("FY26 Revenue", fmt_cr(fy26['revenue']), f"{pct_change(fy25['revenue'], fy26['revenue']):+.1f}% YoY"),
    ("EBITDA Margin", f"{fy26['ebitda_margin']:.1f}%", f"{fy26['ebitda_margin']-fy25['ebitda_margin']:+.1f}% YoY"),
    ("PAT", fmt_cr(fy26['pat']), f"{pct_change(fy25['pat'], fy26['pat']):+.1f}% YoY"),
    ("ROE", f"{fy26['roe']:.1f}%", f"FY25: {fy25['roe']:.1f}%"),
    ("Net D/E", f"{max(0, (fy26['gross_debt']-fy26['cash']))/max(1,fy26['pat']*3):.1f}x", "Net Debt / EBITDA"),
]
for col, (label, val, sub) in zip([c1, c2, c3, c4, c5, c6], metrics):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{val}</div>
            <div class='metric-sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🏭 Facilities & Expansion",
    "👔 Board Members",
    "💉 Products & Pipeline",
    "🔗 Supply Chain",
    "📊 Financial Analysis",
    "📈 Revenue Mix",
    "🏥 Hospital Metrics" if co["type"] == "hospital" else "📋 Key Ratios",
    "🎙️ Concall Analysis",
    "🤖 AI Assessment",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — FACILITIES & EXPANSION
# ─────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown("<div class='section-header'>🏭 Operational Facilities</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])

    with col_a:
        # Facility table
        fac_data = co["facilities"]
        df_fac = pd.DataFrame(fac_data)
        df_fac.columns = ["City / Location", "Facility Type", "# Units", "Status"]

        def style_status(val):
            color = "#276749" if val == "Operational" else "#744210"
            bg = "#c6f6d5" if val == "Operational" else "#fefcbf"
            return f"background-color:{bg}; color:{color}; font-weight:600; border-radius:4px; padding:2px 8px;"

        styled_df = df_fac.style.applymap(style_status, subset=["Status"])
        st.dataframe(styled_df, use_container_width=True, height=350)

        # City map chart
        city_counts = df_fac.groupby("City / Location")["# Units"].sum().reset_index()
        fig_fac = px.bar(
            city_counts, x="City / Location", y="# Units",
            color="# Units",
            color_continuous_scale=["#d6e4f7", "#0f3460"],
            title="Manufacturing Units by City",
        )
        fig_fac.update_layout(
            height=300, margin=dict(t=40, b=0, l=0, r=0),
            xaxis_title="", yaxis_title="# Units",
            showlegend=False, coloraxis_showscale=False,
            plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
        )
        fig_fac.update_traces(marker_line_width=0)
        st.plotly_chart(fig_fac, use_container_width=True)

    with col_b:
        # Summary stats
        total_fac = co.get("total_facilities", len(fac_data))
        total_countries = co.get("total_countries", "N/A")
        total_beds = co.get("total_beds", "N/A")

        st.markdown(f"""
        <div style='background:#f0f4ff; border-radius:10px; padding:18px;'>
            <div style='font-weight:700; color:#0f3460; margin-bottom:12px; font-size:1.05rem;'>📊 Facility Summary</div>
            <div style='font-size:0.9rem; line-height:2;'>
                <b>Total Facilities:</b> {total_fac}<br>
                <b>Countries Present:</b> {total_countries}<br>
                {'<b>Total Beds:</b> ' + f'{total_beds:,}' + '<br>' if co['type']=='hospital' else ''}
                <b>Listed Cities:</b> {len(fac_data)}<br>
                <b>HQ:</b> {co['hq']}<br>
                <b>Founded:</b> {co['founded']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Pie by type
        type_counts = df_fac.groupby("Facility Type")["# Units"].sum().reset_index()
        fig_pie = px.pie(type_counts, values="# Units", names="Facility Type",
                         color_discrete_sequence=["#0f3460","#16213e","#1a5276","#2e86c1","#85c1e9"],
                         hole=0.45)
        fig_pie.update_layout(
            height=260, showlegend=True,
            legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
            margin=dict(t=10, b=10, l=0, r=0),
            paper_bgcolor="#f0f4ff",
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Expansion Plans
    st.markdown("<div class='section-header'>🚀 Expansion Plans & Growth Capex</div>", unsafe_allow_html=True)
    plans = co.get("expansion_plans", [])
    cols_exp = st.columns(2)
    for i, plan in enumerate(plans):
        with cols_exp[i % 2]:
            st.markdown(f"""
            <div style='background:white; border:1px solid #e2e8f0; border-left:4px solid #0f3460;
                        border-radius:6px; padding:12px 14px; margin:5px 0; font-size:0.88rem;'>
                🔹 {plan}
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — BOARD MEMBERS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown("<div class='section-header'>👔 Current Board of Directors</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#555; font-size:0.9rem;'>Showing {len(co['board_members'])} board members for {co['name']}.</p>", unsafe_allow_html=True)

    for bm in co["board_members"]:
        joined_org_str  = str(bm["joined_org"]) if bm["joined_org"] else "N/A"
        joined_board_str = str(bm["joined_board"]) if bm["joined_board"] else "N/A"
        tenure_board = (2026 - bm["joined_board"]) if bm["joined_board"] else "N/A"
        tenure_org   = (2026 - bm["joined_org"])   if bm["joined_org"]   else "N/A"

        # Role badge color
        role_bg = "#ebf8ff"
        role_color = "#2b6cb0"
        if "Independent" in bm["role"]:
            role_bg, role_color = "#f0fff4", "#276749"
        elif "MD" in bm["role"] or "CEO" in bm["role"] or "Chairman" in bm["role"] or "CFO" in bm["role"] or "Founder" in bm["role"]:
            role_bg, role_color = "#fff5f5", "#c53030"

        initials = "".join(w[0] for w in bm["name"].split()[:2]).upper()

        st.markdown(f"""
        <div style='background:white; border:1px solid #e2e8f0; border-radius:10px;
                    padding:16px 20px; margin:10px 0; display:flex; align-items:flex-start; gap:16px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.06);'>
            <div style='width:52px; height:52px; background:{role_bg}; border-radius:50%;
                        display:flex; align-items:center; justify-content:center;
                        font-weight:800; font-size:1.1rem; color:{role_color}; flex-shrink:0;'>
                {initials}
            </div>
            <div style='flex:1;'>
                <div style='display:flex; align-items:center; gap:10px; flex-wrap:wrap;'>
                    <span style='font-weight:700; font-size:1.05rem; color:#0f3460;'>{bm['name']}</span>
                    <span style='background:{role_bg}; color:{role_color}; padding:3px 10px;
                                 border-radius:12px; font-size:0.78rem; font-weight:600;'>{bm['role']}</span>
                </div>
                <div style='display:flex; gap:24px; margin-top:6px; font-size:0.82rem; color:#555;'>
                    <span>📅 Joined Board: <b>{joined_board_str}</b> ({tenure_board} yrs tenure)</span>
                    <span>🏢 Joined Org: <b>{joined_org_str}</b>
                        {'('+str(tenure_org)+' yrs with co.)' if tenure_org != 'N/A' else ''}</span>
                </div>
                <div style='margin-top:8px; font-size:0.86rem; color:#444; line-height:1.5;'>
                    {bm['background']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Board composition pie
    st.markdown("<div class='section-header'>📊 Board Composition Analysis</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    roles_cat = []
    for bm in co["board_members"]:
        if "Independent" in bm["role"]: roles_cat.append("Independent")
        elif "MD" in bm["role"] or "CEO" in bm["role"] or "Founder" in bm["role"]: roles_cat.append("Executive (Promoter/CEO)")
        elif "CFO" in bm["role"] or "Whole-time" in bm["role"]: roles_cat.append("Executive (Mgmt)")
        else: roles_cat.append("Non-Executive")

    from collections import Counter
    role_counts = dict(Counter(roles_cat))

    with col1:
        fig_board = px.pie(
            values=list(role_counts.values()), names=list(role_counts.keys()),
            title="Board Role Mix",
            color_discrete_sequence=["#0f3460","#2e86c1","#85c1e9","#d6eaf8"],
            hole=0.4,
        )
        fig_board.update_layout(height=280, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_board, use_container_width=True)

    with col2:
        tenures = [(2026 - bm["joined_board"]) for bm in co["board_members"] if bm["joined_board"]]
        avg_tenure = np.mean(tenures) if tenures else 0
        st.metric("Avg Board Tenure", f"{avg_tenure:.1f} yrs")
        st.metric("Total Board Members", len(co["board_members"]))
        ind_count = sum(1 for c in roles_cat if c == "Independent")
        st.metric("Independent Directors", f"{ind_count} / {len(co['board_members'])}")

    with col3:
        st.markdown("""
        <div style='background:#f8faff; border-radius:8px; padding:14px; font-size:0.85rem;'>
            <b style='color:#0f3460;'>🏛️ Governance Assessment</b><br><br>
        """, unsafe_allow_html=True)
        ind_pct = ind_count / len(co["board_members"]) * 100
        sebi_ok = ind_pct >= 33
        status = "✅ SEBI compliant" if sebi_ok else "⚠️ Below SEBI minimum"
        st.markdown(f"""
            <div style='font-size:0.84rem; line-height:2;'>
                Independent Directors: <b>{ind_pct:.0f}%</b><br>
                SEBI Requirement (33%+): <b>{status}</b><br>
                Promoter/Executive Mix: <b>{100-ind_pct:.0f}%</b>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — PRODUCTS & PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    prod = co["products"]
    st.markdown("<div class='section-header'>🔬 Product Portfolio & Pipeline</div>", unsafe_allow_html=True)

    # Categories
    cat_html = "".join(f"<span class='tag tag-pharma' style='margin:3px;'>{c}</span>" for c in prod["categories"])
    st.markdown(f"<p><b>Segments / Categories:</b> {cat_html}</p>", unsafe_allow_html=True)

    if co["type"] == "pharma":
        # Drug pipeline
        st.markdown("<div class='section-header'>💊 Key Drugs & Approval Status</div>", unsafe_allow_html=True)

        drugs = prod.get("key_drugs", [])
        for drug in drugs:
            stage_class = get_stage_class(drug["stage"])
            revenue_color = {"Very High":"#276749","High":"#2b6cb0","Growing":"#744210","Moderate":"#555","Pipeline":"#888"}.get(drug.get("revenue_contribution",""), "#555")

            st.markdown(f"""
            <div style='background:white; border:1px solid #e2e8f0; border-radius:8px;
                        padding:12px 16px; margin:6px 0; display:flex; align-items:center; gap:14px;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05);'>
                <div style='flex:0 0 220px;'>
                    <div style='font-weight:700; color:#0f3460; font-size:0.92rem;'>{drug['name']}</div>
                    <div style='font-size:0.78rem; color:#888; margin-top:2px;'>{drug['segment']}</div>
                </div>
                <div style='flex:1;'>
                    <span style='font-size:0.8rem; color:#555;'>🔏 {drug['patent_status']}</span>
                </div>
                <div style='flex:0 0 160px; text-align:center;'>
                    <span class='stage-pill {stage_class}'>{drug['stage']}</span>
                </div>
                <div style='flex:0 0 120px; text-align:right;'>
                    <span style='font-size:0.8rem; font-weight:600; color:{revenue_color};'>
                        {'💰 ' if drug.get("revenue_contribution","") not in ["Pipeline"] else '🔬 '}{drug.get('revenue_contribution','')}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Patents pending
        if prod.get("pending_patents"):
            st.markdown("<div class='section-header'>📋 Patents Pending / Filed</div>", unsafe_allow_html=True)
            for pat in prod["pending_patents"]:
                st.markdown(f"""
                <div style='background:#fffbeb; border-left:3px solid #d69e2e; border-radius:6px;
                            padding:8px 14px; margin:5px 0; font-size:0.87rem; color:#744210;'>
                    📄 {pat}
                </div>
                """, unsafe_allow_html=True)

        # Pipeline summary
        if prod.get("pipeline_summary"):
            st.info(f"**Pipeline Overview:** {prod['pipeline_summary']}")

        # Pipeline funnel chart
        st.markdown("<div class='section-header'>📊 Pipeline Stage Distribution</div>", unsafe_allow_html=True)
        stages = {"Marketed": 0, "Phase III": 0, "Phase II": 0, "Phase I": 0, "Filing/Pending": 0}
        for drug in drugs:
            s = drug["stage"].lower()
            if "marketed" in s or "market" in s: stages["Marketed"] += 1
            elif "phase iii" in s or "phase 3" in s: stages["Phase III"] += 1
            elif "phase ii" in s or "phase 2" in s: stages["Phase II"] += 1
            elif "phase i" in s or "phase 1" in s: stages["Phase I"] += 1
            else: stages["Filing/Pending"] += 1

        colors = ["#276749","#2b6cb0","#744210","#742a2a","#553c9a"]
        fig_stage = go.Figure(go.Bar(
            y=list(stages.keys()),
            x=list(stages.values()),
            orientation="h",
            marker_color=colors,
            text=list(stages.values()),
            textposition="outside",
        ))
        fig_stage.update_layout(
            height=280, margin=dict(t=10, b=10, l=0, r=60),
            xaxis_title="# Products", yaxis_title="",
            plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
            xaxis=dict(showgrid=True, gridcolor="#eee"),
        )
        st.plotly_chart(fig_stage, use_container_width=True)

    else:
        # Hospital services
        st.markdown("<div class='section-header'>🏥 Clinical Programs & Services</div>", unsafe_allow_html=True)
        services = prod.get("key_services", [])
        for svc in services:
            rc = svc.get("revenue_contribution", "")
            rc_color = {"Highest":"#276749","Very High":"#2b6cb0","High":"#744210","Growing":"#553c9a","Moderate":"#555"}.get(rc, "#555")
            st.markdown(f"""
            <div style='background:white; border:1px solid #e2e8f0; border-radius:8px;
                        padding:12px 16px; margin:6px 0; display:flex; align-items:center;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05);'>
                <div style='flex:1; font-weight:700; color:#0f3460;'>🏥 {svc['name']}</div>
                <div style='flex:0 0 160px; color:#555; font-size:0.85rem;'>{svc['segment']}</div>
                <div style='flex:0 0 140px; text-align:right; font-weight:600; color:{rc_color}; font-size:0.88rem;'>
                    {rc}
                </div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — SUPPLY CHAIN
# ─────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    sc = co["supply_chain"]
    st.markdown("<div class='section-header'>🔗 Supply Chain Overview</div>", unsafe_allow_html=True)

    col_sc1, col_sc2 = st.columns(2)

    with col_sc1:
        fields = [
            ("🏭 API / Material Sourcing", sc.get("api_sourcing", "N/A")),
            ("📦 Key Raw Materials", ", ".join(sc.get("key_raw_materials", []))),
            ("🚚 Logistics & Distribution", sc.get("logistics", "N/A")),
            ("🌐 China Exposure", sc.get("china_exposure", "N/A")),
        ]
        for label, val in fields:
            st.markdown(f"""
            <div style='background:white; border:1px solid #e2e8f0; border-radius:8px;
                        padding:14px 16px; margin:8px 0; box-shadow:0 1px 4px rgba(0,0,0,0.04);'>
                <div style='font-weight:700; color:#0f3460; margin-bottom:5px;'>{label}</div>
                <div style='font-size:0.88rem; color:#444;'>{val}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_sc2:
        # Revenue by market — pie chart
        markets = sc.get("key_markets", [])
        if markets:
            mkt_labels, mkt_vals = [], []
            for m in markets:
                try:
                    parts = m.rsplit("(", 1)
                    label = parts[0].strip()
                    pct   = float(parts[1].replace(")", "").replace("%", "").strip())
                    mkt_labels.append(label)
                    mkt_vals.append(pct)
                except:
                    pass

            if mkt_labels and mkt_vals:
                fig_mkt = px.pie(
                    values=mkt_vals, names=mkt_labels,
                    title="Geographic Revenue Split",
                    color_discrete_sequence=["#0f3460","#1a5276","#2e86c1","#5dade2","#85c1e9","#d6eaf8"],
                    hole=0.42,
                )
                fig_mkt.update_layout(
                    height=340, margin=dict(t=40, b=0, l=0, r=0),
                    legend=dict(orientation="v", x=0.85, y=0.5, font=dict(size=10)),
                )
                fig_mkt.update_traces(textinfo='percent+label', textposition='inside')
                st.plotly_chart(fig_mkt, use_container_width=True)

        # China exposure assessment
        china_text = sc.get("china_exposure", "")
        china_color = "#276749"
        china_bg    = "#f0fff4"
        if "HIGH" in china_text.upper() or "high" in china_text.lower():
            china_color, china_bg = "#742a2a", "#fff5f5"
        elif "Moderate" in china_text or "moderate" in china_text:
            china_color, china_bg = "#744210", "#fffbeb"

        st.markdown(f"""
        <div style='background:{china_bg}; border:1px solid; border-color:{china_color}40;
                    border-radius:8px; padding:14px; margin-top:8px;'>
            <div style='font-weight:700; color:{china_color}; margin-bottom:6px;'>🇨🇳 China Supply Risk</div>
            <div style='font-size:0.87rem; color:{china_color};'>{china_text}</div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — FINANCIAL ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    fin = co["financials"]
    years = ["FY2024", "FY2025", "FY2026"]
    revenues  = [fin[y]["revenue"]       for y in years]
    ebitdas   = [fin[y]["ebitda"]        for y in years]
    pats      = [fin[y]["pat"]           for y in years]
    emgns     = [fin[y]["ebitda_margin"] for y in years]
    pmgns     = [fin[y]["pat_margin"]    for y in years]
    roes      = [fin[y]["roe"]           for y in years]
    roces     = [fin[y]["roce"]          for y in years]
    gross_d   = [fin[y]["gross_debt"]    for y in years]
    cash_vals = [fin[y]["cash"]          for y in years]
    net_debt  = [g - c for g, c in zip(gross_d, cash_vals)]

    # ── Revenue & Profitability ────────────────────────────────────────────────
    st.markdown("<div class='section-header'>📊 Revenue & Profitability Trend</div>", unsafe_allow_html=True)

    fig_rev = make_subplots(specs=[[{"secondary_y": True}]])
    fig_rev.add_trace(go.Bar(name="Revenue (₹ Cr)", x=years, y=revenues,
                              marker_color=["#d6e4f7","#7fb3d6","#0f3460"], text=revenues,
                              texttemplate="₹%{y:,.0f}", textposition="outside"), secondary_y=False)
    fig_rev.add_trace(go.Bar(name="EBITDA (₹ Cr)", x=years, y=ebitdas,
                              marker_color=["#cfffc8","#7dda7d","#276749"], opacity=0.85), secondary_y=False)
    fig_rev.add_trace(go.Bar(name="PAT (₹ Cr)", x=years, y=pats,
                              marker_color=["#ffc9c9","#ff8080","#c53030"], opacity=0.85), secondary_y=False)
    fig_rev.add_trace(go.Scatter(name="EBITDA Margin%", x=years, y=emgns,
                                  mode="lines+markers+text", line=dict(color="#e67e22", width=2.5),
                                  marker=dict(size=9), text=[f"{v:.1f}%" for v in emgns],
                                  textposition="top center"), secondary_y=True)
    fig_rev.add_trace(go.Scatter(name="PAT Margin%", x=years, y=pmgns,
                                  mode="lines+markers+text", line=dict(color="#8e44ad", width=2, dash="dot"),
                                  marker=dict(size=9), text=[f"{v:.1f}%" for v in pmgns],
                                  textposition="bottom center"), secondary_y=True)
    fig_rev.update_layout(
        height=400, barmode="group",
        plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
        legend=dict(orientation="h", y=-0.15),
        margin=dict(t=20, b=0, l=0, r=0),
        yaxis=dict(title="₹ Crores"),
        yaxis2=dict(title="Margin %", ticksuffix="%"),
    )
    st.plotly_chart(fig_rev, use_container_width=True)

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        # ROE / ROCE
        st.markdown("<div class='section-header'>📈 Return Ratios</div>", unsafe_allow_html=True)
        fig_ret = go.Figure()
        fig_ret.add_trace(go.Scatter(x=years, y=roes, mode="lines+markers+text",
                                      name="ROE %", line=dict(color="#0f3460", width=3),
                                      marker=dict(size=10), text=[f"{v:.1f}%" for v in roes],
                                      textposition="top center"))
        fig_ret.add_trace(go.Scatter(x=years, y=roces, mode="lines+markers+text",
                                      name="ROCE %", line=dict(color="#2e86c1", width=3, dash="dot"),
                                      marker=dict(size=10), text=[f"{v:.1f}%" for v in roces],
                                      textposition="bottom center"))
        fig_ret.update_layout(
            height=280, plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
            legend=dict(orientation="h", y=-0.2),
            margin=dict(t=10, b=0, l=0, r=0), yaxis=dict(ticksuffix="%"),
        )
        st.plotly_chart(fig_ret, use_container_width=True)

    with col_f2:
        # Debt profile
        st.markdown("<div class='section-header'>💰 Debt & Cash Profile</div>", unsafe_allow_html=True)
        fig_debt = go.Figure()
        fig_debt.add_trace(go.Bar(x=years, y=gross_d, name="Gross Debt",
                                   marker_color=["#ffc9c9","#ff8080","#c53030"]))
        fig_debt.add_trace(go.Bar(x=years, y=cash_vals, name="Cash & Investments",
                                   marker_color=["#cfffc8","#7dda7d","#276749"]))
        fig_debt.add_trace(go.Scatter(x=years, y=net_debt, name="Net Debt",
                                       mode="lines+markers", line=dict(color="#e67e22", width=2.5, dash="dash"),
                                       marker=dict(size=9)))
        fig_debt.update_layout(
            height=280, barmode="group", plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
            legend=dict(orientation="h", y=-0.2),
            margin=dict(t=10, b=0, l=0, r=0), yaxis=dict(title="₹ Cr"),
        )
        st.plotly_chart(fig_debt, use_container_width=True)

    # ── Detailed Financials Table ──────────────────────────────────────────────
    st.markdown("<div class='section-header'>📋 Comprehensive Financial Statement</div>", unsafe_allow_html=True)
    data_rows = {
        "📊 Revenue (₹ Cr)":      [f"₹{fin[y]['revenue']:,.0f}" for y in years],
        "📊 EBITDA (₹ Cr)":       [f"₹{fin[y]['ebitda']:,.0f}" for y in years],
        "📊 PAT (₹ Cr)":          [f"₹{fin[y]['pat']:,.0f}" for y in years],
        "📊 EPS (₹)":             [f"₹{fin[y]['eps']:.1f}" for y in years],
        "📈 EBITDA Margin":       [f"{fin[y]['ebitda_margin']:.1f}%" for y in years],
        "📈 PAT Margin":          [f"{fin[y]['pat_margin']:.1f}%" for y in years],
        "📈 ROE":                 [f"{fin[y]['roe']:.1f}%" for y in years],
        "📈 ROCE":                [f"{fin[y]['roce']:.1f}%" for y in years],
        "🏦 Gross Debt (₹ Cr)":  [f"₹{fin[y]['gross_debt']:,.0f}" for y in years],
        "🏦 Cash (₹ Cr)":        [f"₹{fin[y]['cash']:,.0f}" for y in years],
        "🏦 Net Debt (₹ Cr)":    [f"₹{max(0, fin[y]['gross_debt']-fin[y]['cash']):,.0f}" if fin[y]['gross_debt']>fin[y]['cash'] else f"Net Cash ₹{fin[y]['cash']-fin[y]['gross_debt']:,.0f}" for y in years],
    }
    # Add YoY growth
    rev_chg = ["-",
                f"{pct_change(fin['FY2024']['revenue'], fin['FY2025']['revenue']):+.1f}%",
                f"{pct_change(fin['FY2025']['revenue'], fin['FY2026']['revenue']):+.1f}%"]
    pat_chg = ["-",
                f"{pct_change(fin['FY2024']['pat'], fin['FY2025']['pat']):+.1f}%",
                f"{pct_change(fin['FY2025']['pat'], fin['FY2026']['pat']):+.1f}%"]
    data_rows["🔺 Revenue YoY Growth"] = rev_chg
    data_rows["🔺 PAT YoY Growth"]     = pat_chg

    df_fin = pd.DataFrame(data_rows, index=years).T
    df_fin.index.name = "Metric"
    st.dataframe(df_fin.style.set_properties(**{"background-color":"#f8faff","font-size":"0.88rem"}),
                 use_container_width=True)

    # ── Key Highlights ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🔍 Financial Statement Analysis</div>", unsafe_allow_html=True)
    # AI-generated analysis
    rev_3yr_cagr = (revenues[2]/revenues[0])**0.5 - 1
    pat_3yr_cagr = (pats[2]/pats[0])**0.5 - 1 if pats[0] > 0 else 0
    margin_trend = emgns[2] - emgns[0]
    debt_trend   = net_debt[2] - net_debt[0]

    analyses = []
    analyses.append(f"**Revenue CAGR (FY24–FY26):** {rev_3yr_cagr*100:.1f}% — "
                    + ("Strong outperformer. Growth consistently above sector average." if rev_3yr_cagr > 0.15
                       else "Moderate growth. Company growing inline with sector." if rev_3yr_cagr > 0.05
                       else "Sluggish growth — watch for business headwinds."))
    analyses.append(f"**PAT CAGR (FY24–FY26):** {pat_3yr_cagr*100:.1f}% — "
                    + ("Exceptional earnings growth — operating leverage kicking in." if pat_3yr_cagr > 0.25
                       else "Steady earnings growth. Margins stabilizing." if pat_3yr_cagr > 0.10
                       else "PAT growth lagging revenue — check margin pressures."))
    analyses.append(f"**Margin Trend:** EBITDA margin moved {margin_trend:+.1f}% over 3 years — "
                    + ("Significant margin expansion; business scaling efficiently." if margin_trend > 3
                       else "Stable margins — cost management effective." if margin_trend > 0
                       else "Margin compression — cost inflation or pricing pressure."))
    net_d26 = net_debt[2]
    analyses.append(f"**Debt Position FY26:** {'Net Debt ₹'+str(net_d26)+' Cr — leverage manageable.' if net_d26 > 0 else 'Net Cash company — excellent balance sheet strength.'}")
    analyses.append(f"**ROE Trajectory:** {roes[0]:.1f}% → {roes[2]:.1f}% — "
                    + ("Improving capital efficiency — value-accretive growth." if roes[2] > roes[0] else "Declining capital efficiency — watch asset turnover."))

    for analysis in analyses:
        st.markdown(f"- {analysis}")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — REVENUE MIX
# ─────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    rmix = co["revenue_mix"]
    years_r = list(rmix.keys())
    segments = list(rmix[years_r[0]].keys())

    st.markdown("<div class='section-header'>📊 Revenue Mix — 3-Year Comparison</div>", unsafe_allow_html=True)

    # Stacked bar
    fig_mix = go.Figure()
    colors_mix = ["#0f3460","#1a5276","#2e86c1","#5dade2","#85c1e9","#d6eaf8","#aed6f1","#7fb3d6"]
    for i, seg in enumerate(segments):
        vals = [rmix[y].get(seg, 0) for y in years_r]
        fig_mix.add_trace(go.Bar(
            x=years_r, y=vals, name=seg,
            marker_color=colors_mix[i % len(colors_mix)],
            text=[f"{v:.0f}%" for v in vals], textposition="inside",
        ))
    fig_mix.update_layout(
        barmode="stack", height=380,
        yaxis=dict(title="% of Revenue", ticksuffix="%", range=[0, 115]),
        plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
        legend=dict(orientation="h", y=-0.2),
        margin=dict(t=20, b=0, l=0, r=0),
    )
    st.plotly_chart(fig_mix, use_container_width=True)

    # Side-by-side pie for each year
    col_yr = st.columns(len(years_r))
    for i, yr in enumerate(years_r):
        with col_yr[i]:
            fig_pie = px.pie(
                values=list(rmix[yr].values()),
                names=list(rmix[yr].keys()),
                title=yr,
                color_discrete_sequence=colors_mix,
                hole=0.38,
            )
            fig_pie.update_layout(
                height=300, margin=dict(t=30, b=0, l=0, r=0),
                legend=dict(orientation="v", x=0.7, y=0.5, font=dict(size=10)),
                showlegend=(i == len(years_r) - 1),
            )
            fig_pie.update_traces(textinfo='percent', textposition='inside')
            st.plotly_chart(fig_pie, use_container_width=True)

    # Segment shift table
    st.markdown("<div class='section-header'>📋 Segment Share Shift Analysis</div>", unsafe_allow_html=True)
    shift_data = {"Segment": segments}
    for yr in years_r:
        shift_data[yr] = [f"{rmix[yr].get(s, 0):.0f}%" for s in segments]

    if len(years_r) >= 2:
        shift_data["3Y Change"] = [
            f"{rmix[years_r[-1]].get(s, 0) - rmix[years_r[0]].get(s, 0):+.0f}%" for s in segments
        ]

    df_shift = pd.DataFrame(shift_data)
    st.dataframe(df_shift.style.set_properties(**{"text-align": "center"}), use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 — HOSPITAL METRICS / KEY RATIOS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[6]:
    if co["type"] == "hospital":
        hr = co.get("hospital_ratios", {})
        yrs_h = [y for y in ["FY2024","FY2025","FY2026"] if y in hr]

        st.markdown("<div class='section-header'>🏥 Hospital Operating Metrics — 3-Year Trend</div>", unsafe_allow_html=True)

        # Top KPIs
        if yrs_h:
            latest = hr[yrs_h[-1]]
            prev   = hr[yrs_h[-2]] if len(yrs_h) >= 2 else latest

            kpi_cards = [
                ("🛏️ Occupancy Rate",   f"{latest['occupancy_rate']:.1f}%",
                 f"{pct_change(prev['occupancy_rate'], latest['occupancy_rate']):+.1f}% YoY"),
                ("💰 ARPOB / Day",       f"₹{latest['arpob_per_day']:,.0f}",
                 f"{pct_change(prev['arpob_per_day'], latest['arpob_per_day']):+.1f}% YoY"),
                ("⏱️ ALOS (days)",       f"{latest['alos_days']:.1f}d",
                 "Average Length of Stay"),
                ("🛏️ Operational Beds",  f"{latest['beds_operational']:,}",
                 f"{latest['beds_operational'] - prev.get('beds_operational',latest['beds_operational']):+,} vs PY"),
                ("👥 IP Volume",         f"{latest['inpatient_volume']:,.0f}",
                 f"{pct_change(prev['inpatient_volume'], latest['inpatient_volume']):+.1f}% YoY"),
                ("🚶 OP Volume",         f"{latest['outpatient_volume']:,.0f}",
                 f"{pct_change(prev['outpatient_volume'], latest['outpatient_volume']):+.1f}% YoY"),
            ]
            cols_h = st.columns(3)
            for i, (label, val, sub) in enumerate(kpi_cards):
                with cols_h[i % 3]:
                    st.markdown(f"""
                    <div class='metric-card' style='margin-bottom:12px;'>
                        <div class='metric-label'>{label}</div>
                        <div class='metric-value' style='font-size:1.3rem;'>{val}</div>
                        <div class='metric-sub'>{sub}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Charts
            col_h1, col_h2 = st.columns(2)

            with col_h1:
                # Occupancy trend
                occ  = [hr[y]["occupancy_rate"] for y in yrs_h]
                fig_occ = go.Figure()
                fig_occ.add_trace(go.Bar(x=yrs_h, y=occ, name="Occupancy %",
                                          marker_color=["#d6e4f7","#5dade2","#0f3460"],
                                          text=[f"{v:.1f}%" for v in occ], textposition="outside"))
                fig_occ.add_hline(y=70, line_dash="dot", line_color="#276749",
                                  annotation_text="Target 70%", annotation_position="right")
                fig_occ.update_layout(
                    title="Occupancy Rate (%)", height=280,
                    plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
                    yaxis=dict(ticksuffix="%", range=[50, 90]),
                    margin=dict(t=40, b=0, l=0, r=0),
                )
                st.plotly_chart(fig_occ, use_container_width=True)

            with col_h2:
                # ARPOB trend
                arpob = [hr[y]["arpob_per_day"] for y in yrs_h]
                fig_ar = go.Figure()
                fig_ar.add_trace(go.Scatter(x=yrs_h, y=arpob, mode="lines+markers+text",
                                             name="ARPOB/day",
                                             line=dict(color="#0f3460", width=3),
                                             marker=dict(size=11, color="#0f3460"),
                                             text=[f"₹{v:,.0f}" for v in arpob],
                                             textposition="top center"))
                fig_ar.update_layout(
                    title="ARPOB per Day (₹)", height=280,
                    plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
                    yaxis=dict(tickprefix="₹"),
                    margin=dict(t=40, b=0, l=0, r=0),
                )
                st.plotly_chart(fig_ar, use_container_width=True)

            col_h3, col_h4 = st.columns(2)

            with col_h3:
                # Beds trend
                beds = [hr[y]["beds_operational"] for y in yrs_h]
                fig_beds = go.Figure(go.Bar(x=yrs_h, y=beds, marker_color=["#fefcbf","#fdd835","#f9a825"],
                                             text=beds, textposition="outside"))
                fig_beds.update_layout(
                    title="Operational Beds", height=260,
                    plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
                    margin=dict(t=40, b=0, l=0, r=0),
                )
                st.plotly_chart(fig_beds, use_container_width=True)

            with col_h4:
                # Revenue per bed
                rpb = [hr[y]["revenue_per_bed_cr"] for y in yrs_h]
                ebitda_pb = [hr[y]["ebitda_per_bed_lakh"] for y in yrs_h]
                fig_rpb = go.Figure()
                fig_rpb.add_trace(go.Bar(x=yrs_h, y=rpb, name="Rev/Bed (₹ Cr)",
                                          marker_color=["#d6f5f5","#5dade2","#0f3460"]))
                fig_rpb.add_trace(go.Scatter(x=yrs_h, y=ebitda_pb, name="EBITDA/Bed (₹L)",
                                              mode="lines+markers", yaxis="y2",
                                              line=dict(color="#e67e22", width=2.5), marker=dict(size=9)))
                fig_rpb.update_layout(
                    title="Revenue & EBITDA per Bed", height=260,
                    plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
                    yaxis=dict(title="₹ Crore"),
                    yaxis2=dict(title="₹ Lakh", overlaying="y", side="right"),
                    legend=dict(orientation="h", y=-0.25),
                    margin=dict(t=40, b=0, l=0, r=0),
                )
                st.plotly_chart(fig_rpb, use_container_width=True)

            # Hospital detailed table
            st.markdown("<div class='section-header'>📋 Hospital Metrics — Detailed Table</div>", unsafe_allow_html=True)
            metrics_rows = {
                "Occupancy Rate (%)":       [f"{hr[y]['occupancy_rate']:.1f}%" for y in yrs_h],
                "ARPOB / Day (₹)":         [f"₹{hr[y]['arpob_per_day']:,.0f}" for y in yrs_h],
                "Avg Length of Stay (d)":   [f"{hr[y]['alos_days']:.1f}" for y in yrs_h],
                "Operational Beds":         [f"{hr[y]['beds_operational']:,}" for y in yrs_h],
                "Inpatient Volume":         [f"{hr[y]['inpatient_volume']:,.0f}" for y in yrs_h],
                "Outpatient Volume":        [f"{hr[y]['outpatient_volume']:,.0f}" for y in yrs_h],
                "Revenue / Bed (₹ Cr)":    [f"₹{hr[y]['revenue_per_bed_cr']:.3f}" for y in yrs_h],
                "EBITDA / Bed (₹ Lakh)":   [f"₹{hr[y]['ebitda_per_bed_lakh']:.1f}" for y in yrs_h],
                "Doctor Count":             [f"{hr[y]['doctor_count']:,}" for y in yrs_h],
                "Nurse-to-Bed Ratio":       [f"{hr[y]['nursing_ratio']:.1f}x" for y in yrs_h],
            }
            df_hr = pd.DataFrame(metrics_rows, index=yrs_h).T
            st.dataframe(df_hr, use_container_width=True)

    else:
        # For pharma — show key operational ratios
        st.markdown("<div class='section-header'>📋 Key Operational Metrics (Pharma)</div>", unsafe_allow_html=True)
        fin_data = co["financials"]
        phm_ratios = {
            "Metric": ["R&D / Revenue%", "Gross Profit% (est.)", "Asset Turnover", "Interest Coverage",
                       "Net Debt/EBITDA", "Debt / Equity (est.)", "EPS Growth"],
            "FY2024": [
                "~7–9%",
                f"{((fin_data['FY2024']['revenue']-fin_data['FY2024']['revenue']*0.35)/fin_data['FY2024']['revenue']*100):.1f}%",
                f"{fin_data['FY2024']['revenue']/(fin_data['FY2024']['gross_debt']+fin_data['FY2024']['cash']):.2f}x",
                f"{fin_data['FY2024']['ebitda']/(fin_data['FY2024']['gross_debt']*0.08 + 1):.1f}x",
                f"{max(0, fin_data['FY2024']['gross_debt']-fin_data['FY2024']['cash'])/fin_data['FY2024']['ebitda']:.1f}x",
                f"{fin_data['FY2024']['gross_debt']/(fin_data['FY2024']['pat']*6):.2f}x",
                "—",
            ],
            "FY2025": [
                "~7–9%",
                f"{((fin_data['FY2025']['revenue']-fin_data['FY2025']['revenue']*0.33)/fin_data['FY2025']['revenue']*100):.1f}%",
                f"{fin_data['FY2025']['revenue']/(fin_data['FY2025']['gross_debt']+fin_data['FY2025']['cash']):.2f}x",
                f"{fin_data['FY2025']['ebitda']/(fin_data['FY2025']['gross_debt']*0.08 + 1):.1f}x",
                f"{max(0, fin_data['FY2025']['gross_debt']-fin_data['FY2025']['cash'])/fin_data['FY2025']['ebitda']:.1f}x",
                f"{fin_data['FY2025']['gross_debt']/(fin_data['FY2025']['pat']*6):.2f}x",
                f"{pct_change(fin_data['FY2024']['eps'], fin_data['FY2025']['eps']):+.1f}%",
            ],
            "FY2026": [
                "~7–9%",
                f"{((fin_data['FY2026']['revenue']-fin_data['FY2026']['revenue']*0.30)/fin_data['FY2026']['revenue']*100):.1f}%",
                f"{fin_data['FY2026']['revenue']/(fin_data['FY2026']['gross_debt']+fin_data['FY2026']['cash']):.2f}x",
                f"{fin_data['FY2026']['ebitda']/(fin_data['FY2026']['gross_debt']*0.08 + 1):.1f}x",
                f"{max(0, fin_data['FY2026']['gross_debt']-fin_data['FY2026']['cash'])/fin_data['FY2026']['ebitda']:.1f}x",
                f"{fin_data['FY2026']['gross_debt']/(fin_data['FY2026']['pat']*6):.2f}x",
                f"{pct_change(fin_data['FY2025']['eps'], fin_data['FY2026']['eps']):+.1f}%",
            ],
        }
        st.dataframe(pd.DataFrame(phm_ratios), use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 8 — CONCALL ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[7]:
    concalls = co.get("concalls", [])

    st.markdown("<div class='section-header'>🎙️ Earnings Call Analysis — Last 4 Quarters</div>", unsafe_allow_html=True)

    # Guidance hit/miss scorecard
    st.markdown("#### 📊 Management Guidance Scorecard")
    score_data = []
    guidance_all = []
    for cc in concalls:
        status = cc["guidance_status"].lower()
        if "met" in status or "exceeded" in status:
            hit = "✅ Met"
            clr = "#276749"
        elif "partially" in status:
            hit = "⚠️ Partial"
            clr = "#744210"
        elif "ongoing" in status or "in progress" in status or "tracking" in status:
            hit = "🔵 In Progress"
            clr = "#1a5276"
        else:
            hit = "❌ Missed"
            clr = "#742a2a"
        score_data.append({"Quarter": cc["quarter"], "Date": cc["date"],
                           "Status": hit, "Color": clr})
        guidance_all.append(cc["guidance_status"])

    sc_cols = st.columns(len(score_data))
    for i, sc_item in enumerate(score_data):
        with sc_cols[i]:
            st.markdown(f"""
            <div style='background:white; border-radius:8px; padding:14px; text-align:center;
                        box-shadow:0 2px 8px rgba(0,0,0,0.08); border-top:4px solid {sc_item["Color"]};'>
                <div style='font-weight:700; color:#0f3460; font-size:0.9rem;'>{sc_item["Quarter"]}</div>
                <div style='font-size:0.78rem; color:#888; margin:3px 0;'>{sc_item["Date"]}</div>
                <div style='font-size:1.2rem; margin-top:8px;'>{sc_item["Status"]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Full concall cards
    for cc in concalls:
        status = cc["guidance_status"].lower()
        if "met" in status or "exceeded" in status:
            status_class = "guidance-met"
            status_icon = "✅"
        elif "partially" in status:
            status_class = "guidance-miss"
            status_icon = "⚠️"
        elif "ongoing" in status or "in progress" in status or "tracking" in status:
            status_class = "guidance-prog"
            status_icon = "🔵"
        else:
            status_class = "guidance-miss"
            status_icon = "❌"

        with st.expander(f"📞 {cc['quarter']} ({cc['date']}) — {status_icon} {cc['guidance_status'][:60]}..."):
            col_cc1, col_cc2 = st.columns([1, 1])

            with col_cc1:
                st.markdown("**📢 Guidance Given:**")
                for g in cc["guidance_given"]:
                    st.markdown(f"- {g}")

                st.markdown("**📊 Guidance Status:**")
                st.markdown(f"<span class='{status_class}'>{status_icon} {cc['guidance_status']}</span>",
                           unsafe_allow_html=True)

            with col_cc2:
                st.markdown("**🔑 Key Notes from the Call:**")
                for note in cc["key_notes"]:
                    st.markdown(f"""
                    <div class='bull-point'>📌 {note}</div>
                    """, unsafe_allow_html=True)

            if cc.get("red_flags_raised"):
                st.markdown("**🚩 Red Flags Raised in This Call:**")
                for flag in cc["red_flags_raised"]:
                    st.markdown(f"<div class='red-flag'>🚩 {flag}</div>", unsafe_allow_html=True)

    # Guidance trend chart
    st.markdown("<div class='section-header'>📊 Guidance Reliability Chart</div>", unsafe_allow_html=True)
    reliability_map = {"✅ Met": 1, "🔵 In Progress": 0.5, "⚠️ Partial": 0.3, "❌ Missed": 0}
    quarters = [sd["Quarter"] for sd in score_data]
    reliability_scores = [reliability_map.get(sd["Status"], 0.5) for sd in score_data]

    fig_rel = go.Figure()
    fig_rel.add_trace(go.Bar(
        x=quarters[::-1], y=reliability_scores[::-1],
        marker_color=["#276749" if s >= 0.8 else "#744210" if s >= 0.3 else "#742a2a" for s in reliability_scores[::-1]],
        text=[f"{s*100:.0f}%" for s in reliability_scores[::-1]],
        textposition="outside",
    ))
    fig_rel.update_layout(
        height=220, yaxis=dict(range=[0, 1.3], tickvals=[0, 0.3, 0.5, 1.0],
                                ticktext=["Missed", "Partial", "In Progress", "Met"]),
        plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
        margin=dict(t=10, b=0, l=0, r=0),
    )
    st.plotly_chart(fig_rel, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 9 — AI ASSESSMENT
# ─────────────────────────────────────────────────────────────────────────────
with tabs[8]:
    ai = co["ai_analysis"]
    fin_d = co["financials"]

    st.markdown("<div class='section-header'>🤖 AI-Powered Fundamental Assessment</div>", unsafe_allow_html=True)

    # Overall score
    score = ai["overall_score"]
    sc_class = get_score_class(score)
    col_ai1, col_ai2 = st.columns([1, 2])

    with col_ai1:
        gauge_color = "#276749" if score >= 8 else "#744210" if score >= 6.5 else "#742a2a"
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Overall Score", "font": {"size": 16}},
            delta={"reference": 7, "increasing": {"color": "#276749"}, "decreasing": {"color": "#742a2a"}},
            gauge={
                "axis": {"range": [0, 10], "tickwidth": 1, "tickcolor": "#aaa"},
                "bar": {"color": gauge_color},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#e2e8f0",
                "steps": [
                    {"range": [0, 5],   "color": "#fff5f5"},
                    {"range": [5, 7],   "color": "#fffbeb"},
                    {"range": [7, 10],  "color": "#f0fff4"},
                ],
                "threshold": {
                    "line": {"color": "#0f3460", "width": 4},
                    "thickness": 0.75, "value": 7.5,
                },
            },
        ))
        fig_gauge.update_layout(height=280, margin=dict(t=30, b=0, l=20, r=20), paper_bgcolor="#f8faff")
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown(f"""
        <div style='text-align:center; padding:10px;'>
            <div style='font-size:0.85rem; color:#555; font-weight:600; margin-bottom:8px;'>ANALYST VIEW</div>
            <div style='background:#f0f4ff; border-radius:8px; padding:12px; font-size:0.9rem;
                        font-weight:600; color:#0f3460; line-height:1.4;'>
                💡 {ai["recommendation"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_ai2:
        # Bull vs Bear
        st.markdown("**🐂 Bull Factors (Strengths)**")
        for b in ai["bull_factors"]:
            st.markdown(f"<div class='bull-point'>🟢 {b}</div>", unsafe_allow_html=True)

        st.markdown("<br>**🐻 Bear Factors (Risks)**")
        for b in ai["bear_factors"]:
            st.markdown(f"<div class='bear-point'>🔴 {b}</div>", unsafe_allow_html=True)

    # Red Flags
    st.markdown("<div class='section-header'>🚩 Red Flags & Watch Items</div>", unsafe_allow_html=True)
    rf_cols = st.columns(2)
    for i, rf in enumerate(ai["red_flags"]):
        with rf_cols[i % 2]:
            st.markdown(f"<div class='red-flag'>🚩 {rf}</div>", unsafe_allow_html=True)

    if not ai["red_flags"]:
        st.success("✅ No significant red flags identified for this company at present.")

    # Quantitative scorecards
    st.markdown("<div class='section-header'>📊 Quantitative Scorecard</div>", unsafe_allow_html=True)

    # Calculate scores
    f26 = fin_d["FY2026"]
    f25 = fin_d["FY2025"]
    f24 = fin_d["FY2024"]

    rev_cagr   = (f26["revenue"]/f24["revenue"])**0.5 - 1
    pat_cagr   = (f26["pat"]/max(f24["pat"],1))**0.5 - 1
    mgn_change = f26["ebitda_margin"] - f24["ebitda_margin"]
    net_d_ebitda = max(0, f26["gross_debt"]-f26["cash"]) / max(1, f26["ebitda"])

    def score_metric(val, thresholds, labels=None):
        """Return a score 1-5 based on thresholds."""
        if val >= thresholds[0]: return 5
        if val >= thresholds[1]: return 4
        if val >= thresholds[2]: return 3
        if val >= thresholds[3]: return 2
        return 1

    quant_scores = {
        "Revenue CAGR (3Y)":     (f"{rev_cagr*100:.1f}%",   score_metric(rev_cagr*100, [20,15,10,5])),
        "PAT CAGR (3Y)":         (f"{pat_cagr*100:.1f}%",   score_metric(pat_cagr*100, [25,18,10,5])),
        "EBITDA Margin":         (f"{f26['ebitda_margin']:.1f}%", score_metric(f26['ebitda_margin'], [30,24,18,12])),
        "Margin Expansion (3Y)": (f"{mgn_change:+.1f}%",    score_metric(mgn_change, [4,2,0,-2])),
        "ROE":                   (f"{f26['roe']:.1f}%",      score_metric(f26['roe'], [25,18,12,8])),
        "ROCE":                  (f"{f26['roce']:.1f}%",     score_metric(f26['roce'], [25,18,12,8])),
        "Net Debt/EBITDA":       (f"{net_d_ebitda:.1f}x",   score_metric(2.5-net_d_ebitda, [2.5,2,1.5,1])),
    }

    score_labels = {1: ("❌ Poor", "#742a2a"), 2: ("⚠️ Below Avg", "#744210"),
                    3: ("⚪ Average", "#555"), 4: ("✅ Good", "#276749"), 5: ("⭐ Excellent", "#0f3460")}

    df_qs_data = {"Parameter": [], "Value": [], "Score": [], "Rating": []}
    for param, (val, sc) in quant_scores.items():
        label, _ = score_labels[sc]
        df_qs_data["Parameter"].append(param)
        df_qs_data["Value"].append(val)
        df_qs_data["Score"].append(f"{sc}/5")
        df_qs_data["Rating"].append(label)

    df_qs = pd.DataFrame(df_qs_data)
    st.dataframe(df_qs, use_container_width=True)

    # Radar chart
    cats  = list(quant_scores.keys())
    vals  = [quant_scores[c][1] for c in cats]
    cats_closed = cats + [cats[0]]
    vals_closed = vals + [vals[0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=vals_closed, theta=cats_closed, fill="toself",
        fillcolor="rgba(15, 52, 96, 0.15)",
        line=dict(color="#0f3460", width=2.5),
        name=co["name"]
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5], tickvals=[1,2,3,4,5])),
        showlegend=False, height=380,
        margin=dict(t=20, b=20, l=40, r=40), paper_bgcolor="#f8faff",
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Peer comparison
    st.markdown("<div class='section-header'>📊 Cross-Company Comparison</div>", unsafe_allow_html=True)
    same_type = {k: v for k, v in COMPANIES.items() if v["type"] == co["type"]}
    if len(same_type) > 1:
        comp_data = []
        for ck, cv in same_type.items():
            cf = cv["financials"]["FY2026"]
            comp_data.append({
                "Company": cv["name"][:30],
                "Revenue (₹ Cr)": cf["revenue"],
                "EBITDA Margin": f"{cf['ebitda_margin']:.1f}%",
                "PAT Margin": f"{cf['pat_margin']:.1f}%",
                "ROE": f"{cf['roe']:.1f}%",
                "AI Score": cv["ai_analysis"]["overall_score"],
                "Rating": cv["ai_analysis"]["recommendation"][:40],
            })
        df_comp = pd.DataFrame(comp_data).sort_values("Revenue (₹ Cr)", ascending=False)
        st.dataframe(df_comp.style.highlight_max(subset=["Revenue (₹ Cr)","AI Score"], color="#c6f6d5")
                                  .highlight_min(subset=["AI Score"], color="#fed7d7"),
                     use_container_width=True)

        # Revenue comparison bar
        fig_comp = px.bar(
            df_comp, x="Company", y="Revenue (₹ Cr)",
            color="AI Score", color_continuous_scale="Blues",
            title="Peer Revenue Comparison (FY2026)",
            text="Revenue (₹ Cr)", labels={"Revenue (₹ Cr)":"Revenue (₹ Cr)"}
        )
        fig_comp.update_layout(height=320, plot_bgcolor="#f8faff", paper_bgcolor="#f8faff",
                                margin=dict(t=40, b=0, l=0, r=0),
                                coloraxis_colorbar=dict(title="AI Score"))
        fig_comp.update_traces(texttemplate="₹%{y:,.0f}", textposition="outside")
        st.plotly_chart(fig_comp, use_container_width=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='app-footer'>
    💊 India Pharma & Healthcare Tracker | Data sourced from public filings, annual reports, BSE/NSE disclosures & earnings calls.<br>
    ⚠️ For educational and research purposes only. Not investment advice. Always verify with primary sources.<br>
    Built with Streamlit + Plotly | August 2026
</div>
""", unsafe_allow_html=True)
