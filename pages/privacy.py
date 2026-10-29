import streamlit as st

from app_helpers import page_header

page_header(
    "Understand / privacy", "Privacy and project scope.",
    "What this local student application uses, stores and leaves outside its scope."
)
st.subheader("Race data")
st.write(
    "This project uses historical race timing data accessed through FastF1 for an educational "
    "comparison of forecasting methods. The interface displays driver abbreviations, race details, "
    "lap times and model outputs. Driver abbreviations and race numbers can identify drivers; "
    "they are not anonymisation. No private contact details or sensitive profiles are added."
)

st.subheader("Using this local app")
st.markdown(
    "- There are no accounts, contact forms, uploads, advertising or custom visitor analytics.\n"
    "- The application does not write your selections to a database or modify the race data.\n"
    "- Forecasts are read from a local file and cached in the running Python process. "
    "Stopping that process clears this in-memory cache; the saved files remain on disk.\n"
    "- Streamlit usage statistics are disabled in the project configuration. "
    "Streamlit may use technical session/security mechanisms.\n"
    "- The server is configured for this computer only (127.0.0.1). "
    "Changing its hosting or configuration can change who can access it.\n"
    "- Source links open external websites, whose own privacy terms apply."
)

st.subheader("GDPR responsibilities")
st.write(
    "Identifiable driver data needs an appropriate basis and purpose for processing. "
    "Public availability alone is not proof of GDPR compliance. This page describes the "
    "current local implementation; it is not a completed legal assessment."
)
st.write(
    "Before sharing a hosted version, the project owner and institution need to record the "
    "responsible organisation/contact, lawful basis, retention period, hosting recipients and "
    "any international transfers, and the route for access, correction, deletion or objection requests. "
    "These details have not yet been established for a public deployment."
)
st.markdown(
    "Official references: [European Commission GDPR principles]"
    "(https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en) "
    "and [personal data definitions]"
    "(https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/application-gdpr_en)."
)

st.subheader("Responsible interpretation")
st.write(
    "This is a historical forecasting study, not a live race feed or a tool for making consequential "
    "decisions about drivers. A small overall error does not guarantee an accurate individual lap. "
    "Fallbacks and unavailable forecasts are shown openly. The app does not predict driving paths "
    "or corner speeds, and it is not affiliated with Formula 1 or its teams."
)
