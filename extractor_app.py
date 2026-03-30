import io
import re

import pandas as pd
import streamlit as st

# This looks for 010, 011, 012, or 015 followed by 8 digits
egy_phone_pattern = r"01[0125]\d{8}"

# This looks for standard email formats
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"


def _unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for v in values:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def _to_two_column_df(phones: list[str], emails: list[str]) -> pd.DataFrame:
    n = max(len(phones), len(emails), 1)
    phones_pad = phones + [""] * (n - len(phones))
    emails_pad = emails + [""] * (n - len(emails))
    return pd.DataFrame({"egy_mobile": phones_pad, "email": emails_pad})


st.set_page_config(
    page_title="Smart Contact Extractor",
    page_icon="📇",
    layout="wide",
)

st.markdown(
    """
<style>
  .app-shell {
    padding: 0.25rem 0 0.75rem 0;
  }
  .sales-hero {
    border: 1px solid rgba(49, 51, 63, 0.12);
    border-radius: 16px;
    padding: 18px 18px 14px 18px;
    background: linear-gradient(135deg, rgba(20, 184, 166, 0.10), rgba(59, 130, 246, 0.08));
  }
  .sales-title {
    font-size: 30px;
    font-weight: 750;
    letter-spacing: -0.02em;
    margin: 0 0 6px 0;
  }
  .sales-subtitle {
    color: rgba(49, 51, 63, 0.75);
    margin: 0;
    font-size: 14px;
    line-height: 1.35;
  }
  .sales-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 650;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid rgba(49, 51, 63, 0.16);
    background: rgba(255, 255, 255, 0.65);
  }
  div.stButton > button[kind="primary"] {
    border-radius: 10px !important;
    font-weight: 700 !important;
  }
  div.stDownloadButton > button {
    border-radius: 10px !important;
    font-weight: 650 !important;
  }
</style>
<div class="app-shell">
  <div class="sales-hero">
    <div class="sales-badge">Sales-ready • Clean export</div>
    <div class="sales-title">Smart Contact Extractor</div>
    <p class="sales-subtitle">
      Paste any content (emails, signatures, chat logs, leads). Click <b>Extract Info</b> to capture Egyptian mobile numbers and email addresses.
    </p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

content = st.text_area(
    "Paste content",
    height=260,
    placeholder="Paste your text here… (e.g., customer messages, web page text, email threads, notes)",
)

col_actions_left, col_actions_right = st.columns([1, 2], vertical_alignment="bottom")
with col_actions_left:
    extract_clicked = st.button("Extract Info", type="primary", use_container_width=True)
with col_actions_right:
    st.caption("Tip: extraction runs only when you click the button.")

phones: list[str] = []
emails: list[str] = []

if extract_clicked:
    phones = re.findall(egy_phone_pattern, content or "")
    emails = re.findall(email_pattern, content or "", flags=re.IGNORECASE)

    phones = _unique_preserve_order([p.strip() for p in phones if p.strip()])
    emails = _unique_preserve_order([e.strip() for e in emails if e.strip()])

st.divider()

left, right = st.columns(2, vertical_alignment="top")
with left:
    st.subheader("Egyptian mobile numbers")
    phones_df = pd.DataFrame({"egy_mobile": phones})
    st.dataframe(phones_df, use_container_width=True, hide_index=True)

with right:
    st.subheader("Email addresses")
    emails_df = pd.DataFrame({"email": emails})
    st.dataframe(emails_df, use_container_width=True, hide_index=True)

st.divider()

download_df = _to_two_column_df(phones, emails)
csv_bytes = download_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download results (CSV)",
    data=csv_bytes,
    file_name="smart_contact_extractor_results.csv",
    mime="text/csv",
    use_container_width=True,
    disabled=(len(phones) == 0 and len(emails) == 0),
)

