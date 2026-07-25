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
# MOBILE-FIRST CSS
# ============================================================
st.markdown("""
<style>
 html, body, [class*="css"] {
 font-size: 16.5px !important;
 line-height: 1.5 !important;
 }
 h1 { font-size: 1.9rem !important; margin-bottom: 0.4rem !important; }
 h2 { font-size: 1.5rem !important; margin-top: 1.8rem !important; }
 h3 { font-size: 1.3rem !important; margin-top: 1.3rem !important; }
 
 .block-container {
 padding-top: 1rem !important;
 padding-bottom: 4rem !important; /* extra space for phone browser bars */
 padding-left: 0.8rem !important;
 padding-right: 0.8rem !important;
 }
 
 @media (max-width: 600px) {
 html, body, [class*="css"] { font-size: 15.5px !important; }
 h1 { font-size: 1.7rem !important; }
 h2 { font-size: 1.35rem !important; }
 }
</style>
""", unsafe_allow_html=True)

st.title("🇮🇪 Ireland + 🇬🇧 United Kingdom")
st.caption(f"Common Travel Area • Absolute numbers | {datetime.now().strftime('%Y-%m-%d')}")

st.warning(
 "Census data are the best official figures but are not perfect "
 "(non-response and undercounting occur). Religion questions are voluntary in some UK areas."
)

# ============================================================
# BASE NUMBERS (correct census figures)
# ============================================================
IE_POP = 5_149_139
UK_POP = 67_000_000
COMBINED = IE_POP + UK_POP

# ============================================================
# 1. COMBINED POPULATION
# ============================================================
st.header("1. Combined Population")

st.markdown(f"""
Citizens of Ireland and the United Kingdom can move freely under the **Common Travel Area**. 
Together they form one free-movement area of **{COMBINED:,}** people.
""")

pop_df = pd.DataFrame({
 "Part": ["Ireland", "United Kingdom"],
 "People": [IE_POP, UK_POP]
})

fig1 = px.pie(
 pop_df, values="People", names="Part",
 title="Where people live",
 color="Part",
 color_discrete_map={"Ireland": "#169B62", "United Kingdom": "#012169"},
 hole=0.4
)
fig1.update_traces(textinfo="percent", textfont_size=18)
fig1.update_layout(
 height=480,
 margin=dict(t=50, b=100, l=10, r=10),
 showlegend=True,
 legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(size=15))
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown(f"""
- **Ireland**: {IE_POP:,} 
- **United Kingdom**: {UK_POP:,} 
- **Combined**: {COMBINED:,}
""")
st.caption("Source: CSO Census 2022 (5,149,139) + ONS / Scotland / NISRA 2021–22 (UK rounded).")

# ============================================================
# 2. PLACE OF BIRTH
# ============================================================
st.header("2. Place of Birth")

ie_born_ie = int(IE_POP * 0.80)
ie_born_out = IE_POP - ie_born_ie
uk_born_uk = int(UK_POP * 0.84)
uk_born_out = UK_POP - uk_born_uk

birth_df = pd.DataFrame({
 "Category": ["Born Ireland", "Born outside Ireland", "Born UK", "Born outside UK"],
 "People": [ie_born_ie, ie_born_out, uk_born_uk, uk_born_out]
})

fig2 = px.pie(
 birth_df, values="People", names="Category",
 title="Place of Birth",
 hole=0.35
)
fig2.update_traces(textinfo="percent", textfont_size=16)
fig2.update_layout(
 height=520,
 margin=dict(t=50, b=120, l=10, r=10),
 showlegend=True,
 legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center", font=dict(size=14))
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown(f"""
**Ireland** 
- Born in Ireland: **{ie_born_ie:,}** 
- Born outside: **{ie_born_out:,}**

**United Kingdom** 
- Born in UK: **{uk_born_uk:,}** 
- Born outside: **{uk_born_out:,}**
""")
st.caption("Source: CSO 2022 (≈80% Irish-born) • ONS Census period (≈16% foreign-born).")

# ============================================================
# 3. RELIGION
# ============================================================
st.header("3. Religion")

# Correct Ireland figures (CSO 2022)
ie_catholic = 3_515_861 # 69%
ie_none = 736_210
ie_muslim = 81_930
ie_hindu = 33_043 
ie_sikh = 2_000

# UK figures
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
 title="Religion in Ireland (CSO 2022)",
 color_discrete_sequence=px.colors.sequential.Greens
)
fig_ie.update_traces(textinfo="percent", textfont_size=16)
fig_ie.update_layout(
 height=500,
 margin=dict(t=50, b=110, l=10, r=10),
 showlegend=True,
 legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", font=dict(size=14))
)
st.plotly_chart(fig_ie, use_container_width=True)

st.markdown(f"""
- Catholic: **{ie_catholic:,}** (69%) 
- No religion: **{ie_none:,}** 
- Muslim: **{ie_muslim:,}** 
- Hindu: **{ie_hindu:,}** 
- Sikh: **{ie_sikh:,}**
""")
st.caption("Source: CSO Census 2022 Profile 5 – Religion.")

# --- United Kingdom (Catholics separate) ---
st.subheader("In the United Kingdom")
uk_rel = pd.DataFrame({
 "Religion": ["Catholic", "Christian other", "No religion", "Muslim", "Hindu", "Sikh"],
 "People": [uk_catholic, uk_other_christian, uk_none, uk_muslim, uk_hindu, uk_sikh]
})
fig_uk = px.pie(
 uk_rel, values="People", names="Religion",
 title="Religion in the UK (Catholics separate)",
 color_discrete_sequence=px.colors.sequential.Blues
)
fig_uk.update_traces(textinfo="percent", textfont_size=15)
fig_uk.update_layout(
 height=540,
 margin=dict(t=50, b=130, l=10, r=10),
 showlegend=True,
 legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center", font=dict(size=14))
)
st.plotly_chart(fig_uk, use_container_width=True)

st.markdown(f"""
- Catholic: **{uk_catholic:,}** (≈8%) 
- Christian other: **{uk_other_christian:,}** 
- No religion: **{uk_none:,}** 
- Muslim: **{uk_muslim:,}** 
- Hindu: **{uk_hindu:,}** 
- Sikh: **{uk_sikh:,}**
""")
st.caption("Source: ONS 2021 + Scotland 2022 + NISRA 2021. Catholic share ≈8%.")

# --- Combined ---
st.subheader("Common Travel Area Combined")
combined_catholic = ie_catholic + uk_catholic
combined_other = uk_other_christian
combined_none = ie_none + uk_none
combined_muslim = ie_muslim + uk_muslim
combined_hindu = ie_hindu + uk_hindu
combined_sikh = ie_sikh + uk_sikh

comb_rel = pd.DataFrame({
 "Religion": ["Catholic", "Christian other", "No religion", "Muslim", "Hindu", "Sikh"],
 "People": [combined_catholic, combined_other, combined_none, combined_muslim, combined_hindu, combined_sikh]
})
fig_comb = px.pie(
 comb_rel, values="People", names="Religion",
 title="Whole Common Travel Area (Catholics & Muslims combined)",
 hole=0.35
)
fig_comb.update_traces(textinfo="percent", textfont_size=15)
fig_comb.update_layout(
 height=560,
 margin=dict(t=60, b=140, l=10, r=10),
 showlegend=True,
 legend=dict(orientation="h", y=-0.28, x=0.5, xanchor="center", font=dict(size=14))
)
st.plotly_chart(fig_comb, use_container_width=True)

st.markdown(f"""
- Catholic: **{combined_catholic:,}** 
- Christian other: **{combined_other:,}** 
- No religion: **{combined_none:,}** 
- Muslim: **{combined_muslim:,}** 
- Hindu: **{combined_hindu:,}** 
- Sikh: **{combined_sikh:,}**
""")
st.caption("Catholics from both countries combined. Muslims from both countries combined.")

# ============================================================
# 4. PLACES OF WORSHIP
# ============================================================
st.header("4. Places of Worship (Estimates)")

st.markdown("""
**Ireland** 
- Catholic churches ≈ 2,500 
- Mosques ≈ 50 

**United Kingdom** 
- Christian churches ≈ 40,000 
- Mosques ≈ 1,900 
""")

worship = pd.DataFrame({
 "Category": ["Catholic churches (IE)", "Mosques (IE)", "Christian churches (UK)", "Mosques (UK)"],
 "Number": [2500, 50, 40000, 1900]
})
fig4 = px.pie(
 worship, values="Number", names="Category",
 title="Places of Worship (Estimates)",
 color_discrete_sequence=["#169B62", "#169B62", "#012169", "#012169"],
 hole=0.35
)
fig4.update_traces(textinfo="percent", textfont_size=15)
fig4.update_layout(
 height=520,
 margin=dict(t=50, b=120, l=10, r=10),
 showlegend=True,
 legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center", font=dict(size=14))
)
st.plotly_chart(fig4, use_container_width=True)

st.caption("All figures are estimates only (no single official register).")

# ============================================================
# 5. CROSS-BORDER + SUMMARY
# ============================================================
st.header("5. Cross-Border Movement")
st.markdown("""
Under the **Common Travel Area** there are no routine immigration controls between Ireland and the UK. 
Movement of citizens has been two-way for decades.
""")
st.caption("Source: Irish Department of Justice / UK Home Office.")

st.header("Summary")
st.markdown(f"""
- Combined population: **{COMBINED:,}** 
- Ireland: {IE_POP:,} (69% Catholic) 
- United Kingdom: {UK_POP:,} (≈46% Christian, ≈6% Muslim) 
- Free movement continues both ways
""")

st.divider()
st.caption("Primary sources: CSO Census 2022 • ONS 2021 • Scotland Census 2022 • NISRA 2021")
