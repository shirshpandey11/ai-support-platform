import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Support Dashboard")

st.title("AI-Powered Support Insights Dashboard")

uploaded = st.file_uploader(
    "Upload support tickets CSV",
    type=["csv"]
)

if uploaded:

    res = requests.post(
        "https://ai-support-platform-reku.onrender.com/upload",
        files={"file": uploaded}
    )

    st.success("Uploaded successfully!")

if st.button("Retrieve Insights"):

    data = requests.get(
        "https://ai-support-platform-reku.onrender.com/insights/"
    ).json()

    st.subheader("Top Issues")
    st.json(data["top_issues"])

    st.subheader("Sentiment Trends")
    st.json(data["sentiment_trend"])

    st.subheader("Average Order Value")
    st.write(data["avg_order_value"])

    st.subheader("Total Tickets")
    st.write(data["ticket_count"])

    st.subheader("Recent Tickets")

    recent_df = pd.DataFrame(data["recent_tickets"])

    st.dataframe(recent_df)

    st.subheader("Top Issues Chart")

    issue_df = pd.DataFrame(
        list(data["top_issues"].items()),
        columns=["Issue", "Count"]
    )

    st.bar_chart(issue_df.set_index("Issue"))

# Reset database button
if st.button("Reset Database"):

    response = requests.delete(
        "https://ai-support-platform-reku.onrender.com/reset/"
    )

    if response.status_code == 200:
        st.success("Database reset successful!")

    else:
        st.error("Failed to reset database")