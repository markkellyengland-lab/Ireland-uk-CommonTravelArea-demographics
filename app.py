# ============================================================
# IMPORTS
# ============================================================
# Import the Streamlit library – this is the framework that turns the script into an interactive web app
import streamlit as st

# Import pandas – used to create and manipulate tabular data (DataFrames) for the charts
import pandas as pd

# Import Plotly Express – high-level interface for creating interactive pie charts
import plotly.express as px

# Import datetime so we can display the current date in the caption
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
# Configure the overall page: title that appears in the browser tab, favicon, wide layout, sidebar starts collapsed
st.set_page_config(
    page_title="Ireland & UK – Common Travel Area",
    page_icon="🇮🇪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS – Larger text + better mobile responsiveness
# ============================================================
st.markdown("""
<style>
    /* Base font size – larger and readable on all devices */
    html, body, [class*="css"] {
        font-size: 18px !important;
        line-height: 1.5 !important;
    }

    /* Main title */
    h1 {
        font-size: 2.4rem !important;
        margin-bottom: 0.4rem !important;
    }

    /* Section headers */
    h2 {
        font-size: 1.8rem !important;
        margin-top: 2.2rem !important;
        margin-bottom: 0.8rem !important;
    }

    /* Sub-headers */
    h3 {
        font-size: 1.45rem !important;
        margin-top: 1.5rem !important;
    }

    /* Captions and source notes */
    .stCaption, .caption {
        font-size: 0.95rem !important;
        line-height: 1.4 !important;
    }

    /* Make markdown text more readable */
    p, li {
        font-size: 1.05rem !important;
    }

    /* Better spacing on mobile */
    @media (max-width: 768px) {
        html, body, [class*="css"] {
            font-size: 16.5px !important;
        }
        h1 { font-size: 1.9rem !important; }
        h2 { font-size: 1.5rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# Display the main page title with flags
st.title("🇮🇪 Ireland + 🇬🇧 United Kingdom")

# Show a small caption under the title with the generation date
st.caption(f"Common Travel Area view • Absolute numbers | {datetime.now().strftime('%Y-%m-%d')}")

# Warning box reminding users that census data, while official, still has limitations
st.warning(
    "Census data are the best official figures but are not perfect "
    "(non-response, undercounting and definition differences occur). "
    "Religion questions are voluntary in some UK jurisdictions."
)

# ============================================================
# BASE NUMBERS (census-period)
# ============================================================
# Ireland total population – exact figure from CSO Census 2022
IE_POP = 5_149_139

# United Kingdom total – rounded figure representing the 2021–22 census period
# (England & Wales 59.6 m + Scotland ≈5.4 m + Northern Ireland ≈1.9 m)
UK_POP = 67_000_000

# Simple arithmetic sum of the two populations = Common Travel Area total
COMBINED = IE_POP + UK_POP

# ============================================================
# 1. COMBINED SCALE
# ============================================================
st.header("1. Combined Population (Common Travel Area)")

st.markdown(f"""
Citizens of Ireland and the United Kingdom can move freely under the **Common Travel Area**.  
Together they form one practical free-movement area of **{COMBINED:,}** people.
""")

pop_pie = pd.DataFrame({
    "Part": ["In Ireland", "In the United Kingdom"],
    "People": [IE_POP, UK_POP]
})

fig_pop = px.pie(
    pop_pie, values="People", names="Part",
    title="Combined Population – Where people live",
    color="Part",
    color_discrete_map={"In Ireland": "#169B62", "In the United Kingdom": "#012169"},
    hole=0.35
)

# Bigger chart + better label handling so nothing is cut off
fig_pop.update_traces(
    textinfo="percent+label",
    textfont_size=16,
    textposition="outside",
    pull=[0.02, 0.02]
)
fig_pop.update_layout(
    height=560,
    font=dict(size=16),
    margin=dict(t=80, b=80, l=40, r=40),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
)
st.plotly_chart(fig_pop, use_container_width=True)

st.markdown(f"""
- **In Ireland**: {IE_POP:,} people  
- **In the United Kingdom**: {UK_POP:,} people (approx. around census period)  
- **Combined Common Travel Area**: {COMBINED:,} people
""")
st.caption(
    "Sources: CSO Census of Population 2022 Summary Results "
    "(https://www.cso.ie/en/releasesandpublications/ep/p-cpsr/censusofpopulation2022-summaryresults/) – "
    "5,149,139 usual residents on 3 April 2022. "
    "UK: ONS Census 2021 England & Wales (59,597,300) + Scotland Census 2022 + Northern Ireland Census 2021 "
    "(combined UK figure rounded for the period)."
)

# ============================================================
# 2. PLACE OF BIRTH
# ============================================================
st.header("2. Place of Birth")

ie_born_ie = int(IE_POP * 0.80)
ie_born_out = IE_POP - ie_born_ie
uk_born_uk = int(UK_POP * 0.84)
uk_born_out = UK_POP - uk_born_uk

birth_df = pd.DataFrame({
    "Category": [
        "Born in Ireland (living in Ireland)",
        "Born outside Ireland (living in Ireland)",
        "Born in the UK (living in the UK)",
        "Born outside the UK (living in the UK)"
    ],
    "People": [ie_born_ie, ie_born_out, uk_born_uk, uk_born_out]
})

fig_birth = px.pie(
    birth_df, values="People", names="Category",
    title="Place of Birth across the Common Travel Area",
    hole=0.3
)
fig_birth.update_traces(
    textinfo="percent+label",
    textfont_size=14,
    textposition="outside"
)
fig_birth.update_layout(
    height=620,
    font=dict(size=15),
    margin=dict(t=90, b=120, l=40, r=40),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
)
st.plotly_chart(fig_birth, use_container_width=True)

st.markdown(f"""
**In Ireland**  
- Born in Ireland: **{ie_born_ie:,}**  
- Born outside Ireland: **{ie_born_out:,}**

**In the United Kingdom**  
- Born in the UK: **{uk_born_uk:,}**  
- Born outside the UK: **{uk_born_out:,}**
""")
st.caption(
    "Sources: CSO Census 2022 (≈80% of population born in Ireland). "
    "ONS Census 2021 England & Wales and equivalent UK data (foreign-born share ≈16% around the census period)."
)

# ============================================================
# 3. RELIGION – IRELAND, UK, AND COMBINED
# ============================================================
st.header("3. Religion")

# Ireland absolute numbers (CSO 2022)
ie_catholic = 3_515_861
ie_none = 736_210
ie_muslim = 81_930
ie_hindu = 33_043
ie_sikh = 2_000

# UK absolute numbers
uk_christian = int(UK_POP * 0.462)
uk_none = int(UK_POP * 0.37)
uk_muslim = int(UK_POP * 0.06)
uk_hindu = int(UK_POP * 0.017)
uk_sikh = int(UK_POP * 0.009)
uk_catholic = int(UK_POP * 0.08)
uk_other_christian = uk_christian - uk_catholic

# --- Ireland pie ---
st.subheader("In Ireland")
ie_rel = pd.DataFrame({
    "Religion": ["Catholic", "No religion", "Muslim", "Hindu", "Sikh"],
    "People": [ie_catholic, ie_none, ie_muslim, ie_hindu, ie_sikh]
})
fig_ie = px.pie(
    ie_rel, values="People", names="Religion",
    title="Religion in Ireland (CSO Census 2022)",
    color_discrete_sequence=px.colors.sequential.Greens
)
fig_ie.update_traces(
    textinfo="percent+label",
    textfont_size=15,
    textposition="outside"
)
fig_ie.update_layout(
    height=560,
    font=dict(size=15),
    margin=dict(t=80, b=100, l=30, r=30),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
)
st.plotly_chart(fig_ie, use_container_width=True)

st.markdown(f"""
**In Ireland**  
- Catholic: **{ie_catholic:,}** (69%)  
- No religion: **{ie_none:,}** (≈14%)  
- Muslim: **{ie_muslim:,}**  
- Hindu: **{ie_hindu:,}**  
- Sikh: **{ie_sikh:,}** (small / approximate)
""")
st.caption(
    "Source: CSO Census of Population 2022 Profile 5 – Religion "
    "(https://www.cso.ie/en/releasesandpublications/ep/p-cpp5/censusofpopulation2022profile5-diversitymigrationethnicityirishtravellersreligion/religion/). "
    "Roman Catholic >3.5 million (69%); No religion 736,210; Muslim figures ≈81,930–83,300; Hindu 33,043."
)

# --- UK pie (Catholics shown separately) ---
st.subheader("In the United Kingdom")
uk_rel = pd.DataFrame({
    "Religion": [
        "Catholic",
        "Christian – other",
        "No religion",
        "Muslim",
        "Hindu",
        "Sikh"
    ],
    "People": [
        uk_catholic,
        uk_other_christian,
        uk_none,
        uk_muslim,
        uk_hindu,
        uk_sikh
    ]
})
fig_uk = px.pie(
    uk_rel, values="People", names="Religion",
    title="Religion in the United Kingdom (Census 2021–22) – Catholics shown separately",
    color_discrete_sequence=px.colors.sequential.Blues
)
fig_uk.update_traces(
    textinfo="percent+label",
    textfont_size=14,
    textposition="outside"
)
fig_uk.update_layout(
    height=600,
    font=dict(size=15),
    margin=dict(t=90, b=120, l=30, r=30),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5)
)
st.plotly_chart(fig_uk, use_container_width=True)

st.markdown(f"""
**In the United Kingdom**  
- Catholic: **{uk_catholic:,}** (approximate UK-wide share ≈8%)  
- Christian – other: **{uk_other_christian:,}**  
- No religion: **{uk_none:,}** (≈37%)  
- Muslim: **{uk_muslim:,}** (≈6%)  
- Hindu: **{uk_hindu:,}** (≈1.7%)  
- Sikh: **{uk_sikh:,}** (≈0.9%)
""")
st.caption(
    "Sources: ONS Religion, England and Wales: Census 2021 "
    "(https://www.ons.gov.uk/peoplepopulationandcommunity/culturalidentity/religion/bulletins/religionenglandandwales/census2021). "
    "Scotland Census 2022 + Northern Ireland Census 2021. "
    "UK Catholic share is an approximation (≈8%) and is shown as its own category."
)

# --- Combined CTA pie ---
st.subheader("Common Travel Area Combined View")

combined_catholic = ie_catholic + uk_catholic
combined_other_christian = uk_other_christian
combined_none = ie_none + uk_none
combined_muslim = ie_muslim + uk_muslim
combined_hindu = ie_hindu + uk_hindu
combined_sikh = ie_sikh + uk_sikh

combined_rel = pd.DataFrame({
    "Religion": [
        "Catholic",
        "Christian – other (mainly UK non-Catholic)",
        "No religion",
        "Muslim",
        "Hindu",
        "Sikh"
    ],
    "People": [
        combined_catholic,
        combined_other_christian,
        combined_none,
        combined_muslim,
        combined_hindu,
        combined_sikh
    ]
})

fig_comb = px.pie(
    combined_rel, values="People", names="Religion",
    title="Religion across the whole Common Travel Area "
          "(Catholics combined; Muslims combined; other groups distinct)",
    hole=0.3
)
fig_comb.update_traces(
    textinfo="percent+label",
    textfont_size=14,
    textposition="outside"
)
fig_comb.update_layout(
    height=640,
    font=dict(size=15),
    margin=dict(t=90, b=130, l=30, r=30),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
)
st.plotly_chart(fig_comb, use_container_width=True)

st.markdown(f"""
**Combined Common Travel Area**  
(Catholics treated as one group regardless of country of residence; Muslims as one group; each other demographic kept separate):  
- Catholic: **{combined_catholic:,}**  
- Christian – other (mainly UK non-Catholic): **{combined_other_christian:,}**  
- No religion: **{combined_none:,}**  
- Muslim: **{combined_muslim:,}**  
- Hindu: **{combined_hindu:,}**  
- Sikh: **{combined_sikh:,}**
""")
st.caption(
    "Sources as above for Ireland (CSO 2022) and UK (ONS 2021 + Scotland 2022 + NISRA 2021). "
    "No residual “Other” category mixes distinct religions."
)

# ============================================================
# 4. PLACES OF WORSHIP (PIE CHART)
# ============================================================
st.header("4. Places of Worship (Estimates)")

st.markdown("""
**In Ireland** (approximate)  
- Catholic churches / churches & mass centres ≈ 2,500–2,650  
- Mosques / prayer centres ≈ 50  

**In the United Kingdom** (approximate)  
- Christian churches ≈ 40,000  
- Mosques ≈ 1,800–2,000  
""")

worship = pd.DataFrame({
    "Category": [
        "Catholic churches in Ireland",
        "Mosques in Ireland",
        "Christian churches in the UK",
        "Mosques in the UK"
    ],
    "Estimated Number": [2500, 50, 40000, 1900]
})

fig_w = px.pie(
    worship,
    values="Estimated Number",
    names="Category",
    title="Places of Worship (Estimates) across the Common Travel Area",
    color="Category",
    color_discrete_sequence=["#169B62", "#169B62", "#012169", "#012169"],
    hole=0.3
)
fig_w.update_traces(
    textinfo="percent+label",
    textfont_size=15,
    textposition="outside"
)
fig_w.update_layout(
    height=580,
    font=dict(size=15),
    margin=dict(t=80, b=110, l=30, r=30),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
)
st.plotly_chart(fig_w, use_container_width=True)

st.caption(
    "All place-of-worship figures are estimates only — there is no single official national register. "
    "Ireland Catholic churches ≈2,500 (Republic). Ireland mosques ≈50. "
    "UK mosques commonly ≈1,800–1,900. Christian churches ≈40,000."
)

# ============================================================
# 5. CROSS-BORDER MOVEMENT
# ============================================================
st.header("5. Cross-Border Movement")

st.markdown("""
Under the **Common Travel Area**, citizens of Ireland and the United Kingdom move freely.  
There are no routine immigration controls on citizen movement between the two countries.

Large numbers of people born in Ireland live in the United Kingdom, and significant numbers of people born in the United Kingdom live in Ireland.  
Movement has been two-way for decades.

**Limitation:** Official year-by-year totals and any breakdown by religion are not published as a single series.
""")
st.caption(
    "Source: Common Travel Area arrangements (Irish Department of Justice / UK Home Office). "
    "Census birthplace data (CSO 2022 and ONS) confirm substantial cross-border resident populations."
)

# ============================================================
# SUMMARY
# ============================================================
st.header("Summary")

st.markdown(f"""
- **Combined Common Travel Area**: {COMBINED:,} people  
- **In Ireland**: {IE_POP:,} people (≈80% born in Ireland, 69% Catholic, ≈82,000 Muslim)  
- **In the United Kingdom**: {UK_POP:,} people (≈16% foreign-born at Census, Christian ≈46%, Muslim ≈6%)  
- Free movement of citizens continues both ways  
""")

st.divider()
st.caption(
    "Primary sources: "
    "CSO Census of Population 2022 (Summary Results + Profile 5 Religion); "
    "ONS Religion England and Wales Census 2021; "
    "National Records of Scotland Census 2022; "
    "NISRA Northern Ireland Census 2021; "
    "public estimates of places of worship. "
    "All absolute numbers are census-period or clearly marked estimates."
)
