# ============================================================
# IMPORTS
# ============================================================
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Ireland & UK – Common Travel Area",
    page_icon="🇮🇪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# STRONG MOBILE + DESKTOP CSS
# ============================================================
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-size: 17px !important;
        line-height: 1.55 !important;
    }
    h1 { font-size: 2.1rem !important; margin-bottom: 0.3rem !important; }
    h2 { font-size: 1.65rem !important; margin-top: 2rem !important; }
    h3 { font-size: 1.35rem !important; margin-top: 1.4rem !important; }
    .stCaption { font-size: 0.92rem !important; }
    
    /* Extra space so nothing is cut by phone browser bars */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    @media (max-width: 768px) {
        html, body, [class*="css"] { font-size: 16px !important; }
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.4rem !important; }
        .block-container {
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("🇮🇪 Ireland + 🇬🇧 United Kingdom")
st.caption(f"Common Travel Area view • Absolute numbers | {datetime.now().strftime('%Y-%m-%d')}")

st.warning(
    "Census data are the best official figures but are not perfect "
    "(non-response, undercounting and definition differences occur). "
    "Religion questions are voluntary in some UK jurisdictions."
)

# ============================================================
# BASE NUMBERS
# ============================================================
IE_POP = 5_149_139
UK_POP = 67_000_000
COMBINED = IE_POP + UK_POP

# ============================================================
# 1. COMBINED SCALE
# ============================================================
st.header("1. Combined Population (Common Travel Area)")

st.markdown(f"""
Citizens of Ireland and the United Kingdom can move freely under the **Common Travel Area**.  
Together they form one practical free-movement area of **{COMBINED:,}** people.
""")

# SHORT labels for the pie so they never get cut off on phones
pop_pie = pd.DataFrame({
    "Part": ["Ireland", "United Kingdom"],          # ← short names
    "People": [IE_POP, UK_POP]
})

fig_pop = px.pie(
    pop_pie, values="People", names="Part",
    title="Combined Population – Where people live",
    color="Part",
    color_discrete_map={"Ireland": "#169B62", "United Kingdom": "#012169"},
    hole=0.38
)
fig_pop.update_traces(
    textinfo="percent+label",
    textfont_size=18,
    textposition="outside",
    pull=[0.03, 0.03]
)
fig_pop.update_layout(
    height=520,
    font=dict(size=16),
    margin=dict(t=60, b=80, l=20, r=20),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.18,
        xanchor="center",
        x=0.5,
        font=dict(size=15)
    )
)
st.plotly_chart(fig_pop, use_container_width=True)

st.markdown(f"""
- **In Ireland**: {IE_POP:,} people  
- **In the United Kingdom**: {UK_POP:,} people  
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
        "Born in Ireland",
        "Born outside Ireland",
        "Born in the UK",
        "Born outside the UK"
    ],
    "People": [ie_born_ie, ie_born_out, uk_born_uk, uk_born_out]
})

fig_birth = px.pie(
    birth_df, values="People", names="Category",
    title="Place of Birth across the Common Travel Area",
    hole=0.32
)
fig_birth.update_traces(
    textinfo="percent+label",
    textfont_size=15,
    textposition="outside"
)
fig_birth.update_layout(
    height=580,
    font=dict(size=15),
    margin=dict(t=70, b=110, l=15, r=15),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.28,
        xanchor="center",
        x=0.5,
        font=dict(size=14)
    )
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
# 3. RELIGION
# ============================================================
st.header("3. Religion")

ie_catholic = 3_515_861
ie_none = 736_210
ie_muslim = 81_930
ie_hindu = 33_043
ie_sikh = 2_000

uk_christian = int(UK_POP * 0.462)
uk_none = int(UK_POP * 0.37)
uk_muslim = int(UK_POP * 0.06)
uk_hindu = int(UK_POP * 0.017)
uk_sikh = int(UK_POP * 0.009)
uk_catholic = int(UK_POP * 0.08)
uk_other_christian = uk_christian - uk_catholic

# --- Ireland ---
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
fig_ie.update_traces(textinfo="percent+label", textfont_size=16, textposition="outside")
fig_ie.update_layout(
    height=540,
    font=dict(size=15),
    margin=dict(t=70, b=90, l=15, r=15),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=14))
)
st.plotly_chart(fig_ie, use_container_width=True)

st.markdown(f"""
**In Ireland**  
- Catholic: **{ie_catholic:,}** (69%)  
- No religion: **{ie_none:,}** (≈14%)  
- Muslim: **{ie_muslim:,}**  
- Hindu: **{ie_hindu:,}**  
- Sikh: **{ie_sikh:,}**
""")
st.caption(
    "Source: CSO Census of Population 2022 Profile 5 – Religion "
    "(https://www.cso.ie/en/releasesandpublications/ep/p-cpp5/censusofpopulation2022profile5-diversitymigrationethnicityirishtravellersreligion/religion/). "
    "Roman Catholic >3.5 million (69%); No religion 736,210; Muslim ≈81,930–83,300; Hindu 33,043."
)

# --- United Kingdom (Catholics separate) ---
st.subheader("In the United Kingdom")
uk_rel = pd.DataFrame({
    "Religion": ["Catholic", "Christian – other", "No religion", "Muslim", "Hindu", "Sikh"],
    "People": [uk_catholic, uk_other_christian, uk_none, uk_muslim, uk_hindu, uk_sikh]
})
fig_uk = px.pie(
    uk_rel, values="People", names="Religion",
    title="Religion in the United Kingdom – Catholics shown separately",
    color_discrete_sequence=px.colors.sequential.Blues
)
fig_uk.update_traces(textinfo="percent+label", textfont_size=15, textposition="outside")
fig_uk.update_layout(
    height=580,
    font=dict(size=15),
    margin=dict(t=70, b=110, l=15, r=15),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(size=14))
)
st.plotly_chart(fig_uk, use_container_width=True)

st.markdown(f"""
**In the United Kingdom**  
- Catholic: **{uk_catholic:,}** (≈8%)  
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

# --- Combined ---
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
        "Christian – other",
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
    title="Religion across the whole Common Travel Area<br>(Catholics + Muslims each combined)",
    hole=0.32
)
fig_comb.update_traces(textinfo="percent+label", textfont_size=15, textposition="outside")
fig_comb.update_layout(
    height=600,
    font=dict(size=15),
    margin=dict(t=80, b=120, l=15, r=15),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5, font=dict(size=14))
)
st.plotly_chart(fig_comb, use_container_width=True)

st.markdown(f"""
**Combined Common Travel Area**  
- Catholic: **{combined_catholic:,}**  
- Christian – other: **{combined_other_christian:,}**  
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
# 4. PLACES OF WORSHIP
# ============================================================
st.header("4. Places of Worship (Estimates)")

st.markdown("""
**In Ireland** (approximate)  
- Catholic churches ≈ 2,500  
- Mosques ≈ 50  

**In the United Kingdom** (approximate)  
- Christian churches ≈ 40,000  
- Mosques ≈ 1,900  
""")

worship = pd.DataFrame({
    "Category": [
        "Catholic churches (Ireland)",
        "Mosques (Ireland)",
        "Christian churches (UK)",
        "Mosques (UK)"
    ],
    "Estimated Number": [2500, 50, 40000, 1900]
})

fig_w = px.pie(
    worship,
    values="Estimated Number",
    names="Category",
    title="Places of Worship (Estimates)",
    color="Category",
    color_discrete_sequence=["#169B62", "#169B62", "#012169", "#012169"],
    hole=0.32
)
fig_w.update_traces(textinfo="percent+label", textfont_size=15, textposition="outside")
fig_w.update_layout(
    height=560,
    font=dict(size=15),
    margin=dict(t=70, b=100, l=15, r=15),
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5, font=dict(size=14))
)
st.plotly_chart(fig_w, use_container_width=True)

st.caption(
    "All place-of-worship figures are estimates only. "
    "Ireland Catholic churches ≈2,500 • Ireland mosques ≈50 • "
    "UK mosques ≈1,800–1,900 • UK Christian churches ≈40,000."
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
- **In the United Kingdom**: {UK_POP:,} people (≈16% foreign-born, Christian ≈46%, Muslim ≈6%)  
- Free movement of citizens continues both ways  
""")

st.divider()
st.caption(
    "Primary sources: CSO Census 2022 • ONS Census 2021 • Scotland Census 2022 • NISRA 2021 • public estimates of places of worship."
)
