# 💊 India Pharma & Healthcare Stock Tracker

A comprehensive AI-powered Streamlit dashboard for tracking listed pharma and healthcare stocks on Indian exchanges (NSE/BSE).

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📊 Features

### For All Companies:
- **Facilities & Expansion**: City-wise plants, hospitals, R&D centers with expansion plans
- **Board Members**: Current board with tenure, background, and governance scoring
- **Products & Pipeline**: Drug pipeline, patent status, approval stages (Pharma) | Clinical programs (Hospital)
- **Supply Chain**: Raw materials, logistics, geographic exposure, China risk
- **Financial Analysis**: 3-year Income Statement, Balance Sheet, Return Ratios, Debt profile
- **Revenue Mix**: Segment-wise 3-year revenue breakdown with charts
- **Concall Analysis**: Last 4 quarters — guidance given, management guidance tracking, key notes
- **AI Assessment**: Overall score (1-10), Bull/Bear factors, Red flags, Peer comparison

### Pharma-Specific:
- Drug pipeline with approval stages (Marketed → Phase III → Phase II → Phase I → Filing)
- Patent status and pending patent filings
- ANDA pipeline count and first-to-file opportunities

### Hospital-Specific:
- **ARPOB** (Average Revenue Per Occupied Bed per day)
- **Occupancy Rate** (%) — 3-year trend
- **ALOS** (Average Length of Stay)
- Bed count, inpatient/outpatient volumes
- Revenue per bed, EBITDA per bed, doctor count, nursing ratios

## 🏢 Companies Covered

### 💊 Pharmaceuticals / CRDMO:
- **SUNPHARMA** — Sun Pharmaceutical Industries Ltd
- **DRREDDY** — Dr. Reddy's Laboratories Ltd
- **CIPLA** — Cipla Limited
- **DIVISLAB** — Divi's Laboratories Limited (API / BIOSECURE Act)
- **LAURUS** — Laurus Labs Limited (ARV/CDMO)

### 🏥 Hospitals / Healthcare:
- **APOLLOHOSP** — Apollo Hospitals Enterprise Ltd
- **MAXHEALTH** — Max Healthcare Institute Ltd
- **FORTIS** — Fortis Healthcare Limited

## 🤖 AI Assessment Engine

The AI assessment is rule-based and considers:
1. Revenue CAGR (3-year)
2. PAT CAGR (3-year)
3. EBITDA margin trend
4. Return ratios (ROE, ROCE)
5. Leverage (Net Debt/EBITDA)
6. Management guidance reliability (from last 4 concalls)
7. Structural moats and industry position

**Scoring: 1–10** | >8: Strong Buy/Buy | 7–8: Accumulate | 6–7: Hold | <6: Caution

## 📋 Data Sources

All data is sourced from publicly available information:
- BSE/NSE quarterly filings
- Company annual reports (FY2024, FY2025, FY2026)
- SEBI disclosures
- Earnings call transcripts
- Investor presentations
- Industry reports (BCG, IQVIA, CRISIL)

⚠️ **Disclaimer**: This app is for educational and research purposes only. It does not constitute investment advice. Always verify with primary sources before making investment decisions.

## 🔧 Extending the App

To add a new company, edit `company_data.py` and follow the existing data structure:

```python
COMPANIES["NEWCOMPANY"] = {
    "name": "Company Name",
    "ticker": "TICKER.NS",
    "type": "pharma",  # or "hospital"
    "hq": "City, State",
    "facilities": [...],
    "board_members": [...],
    "products": {...},
    "supply_chain": {...},
    "revenue_mix": {...},
    "financials": {...},
    "concalls": [...],
    "ai_analysis": {...},
    # For hospitals also add:
    "hospital_ratios": {...},
}
```
