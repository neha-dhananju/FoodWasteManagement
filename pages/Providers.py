import streamlit as st

# ---- Page Config ----
st.set_page_config(page_title="Provider Access", layout="wide")

# ---- Background Styling ----
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: 
        linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
        url("https://images.unsplash.com/photo-1525610553991-2bede1a236e2") no-repeat center center fixed;
    background-size: cover;
}

.title-text {
    text-align: center;
    color: white;
    font-size: 2.5em;
    font-weight: bold;
    margin-top: 50px;
    text-shadow: 2px 2px 6px #000000;
}

.button-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    margin-top: 50px;
}

.round-button {
    width: 250px;
    padding: 15px;
    font-size: 1.2em;
    font-weight: bold;
    border-radius: 30px;
    border: none;
    background-color: rgba(255, 255, 255, 0.9);
    color: black;
    cursor: pointer;
    transition: transform 0.2s ease, background-color 0.3s ease;
    text-align: center;
}

.round-button:hover {
    transform: scale(1.05);
    background-color: white;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---- Title ----
st.markdown('<div class="title-text">Provider Access</div>', unsafe_allow_html=True)

# ---- Buttons ----
st.markdown(
    """
    <div class="button-container">
        <a class="round-button" href=/New_provider>🆕 New Provider</a>
        <a class="round-button" href="Existing_provider">🔑 Existing Provider</a>
        <a class="round-button" href="/app">⬅️ Back to Home</a>
    </div>
    """,
    unsafe_allow_html=True,
)
