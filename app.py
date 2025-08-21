import streamlit as st
from utils import hide_sidebar

# ---- Page Config ----
st.set_page_config(page_title="Food Management System", layout="wide")
hide_sidebar()

# ---- Background Styling ----
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
                url("https://gicgrp.com/sg/website/wp-content/uploads/2021/11/Selection-of-healthy-rich-fiber-sources-vegan-food-for-cooking-812997516_1258x838-1024x683.jpeg");
    background-size: cover;
    background-position: center;
}
.title-text {
    text-align: center;
    color: white;
    font-size: 3.2em;
    font-weight: bold;
    margin-top: 40px;
    text-shadow: 2px 2px 6px #000000;
}
.subtitle-text {
    text-align: center;
    color: #f1f1f1;
    font-size: 2.3em;
    margin-top: 30px;
    margin-bottom: 30px;
}
.role-container {
    display: flex;
    justify-content: center;
    gap: 50px;
    margin-top: 40px;
}
.role-button {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    font-size: 1.2em;
    font-weight: bold;
    border: none;
    background-color: rgba(255, 255, 255, 0.9);
    color: #333;
    cursor: pointer;
    text-decoration: none;
    transition: transform 0.3s ease, background 0.3s ease;
    box-shadow: 0px 6px 15px rgba(0,0,0,0.25);
}
.role-button:hover {
    transform: scale(1.08);
    background-color: #fff;
}
.section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 80px 10%;
    gap: 50px;
}
.section:nth-child(even) {
    flex-direction: row-reverse;  /* alternate layout */
}
.section-text {
    flex: 1;
    color: #333;
    background: rgba(255,255,255,0.95);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
}
.section h2 {
    margin-bottom: 15px;
}
.section-img {
    flex: 1;
}
.section-img img {
    width: 100%;
    border-radius: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.25);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---- Hero Section ----
st.markdown('<div class="title-text">Food Waste Management System</div>', unsafe_allow_html=True)


st.markdown("""
<div class="role-container">
    <a class="role-button" href="/Providers">Provider</a>
    <a class="role-button" href="/Receivers">Receiver</a>
    <a class="role-button" href="/Visualization">Visualization</a>
</div>
""", unsafe_allow_html=True)

# ---- Scrollable Sections ----
st.markdown("""
<div class="section">
    <div class="section-text">
        <h2>🎯 Objective </h2>
        <p>The main goal is to build a transparent and easy-to-use platform where food donations 
        can be listed, claimed, and tracked. By using digital technology, we aim to simplify the 
        process of sharing surplus food and ensure it reaches the right people at the right time.</p>
    </div>
    <div class="section-img">
        <img src="https://cdn-icons-png.flaticon.com/512/747/747310.png" alt="Goal">
    </div>
</div>

<div class="section">
    <div class="section-text">
        <h2>📌 Use Case</h2>
        <p>Every day, tons of edible food goes to waste while many people struggle with hunger. 
        This system connects food providers (restaurants, canteens, households) with receivers 
        (NGOs, individuals, communities) to reduce food wastage and feed the needy.</p>
    </div>
    <div class="section-img">
        <img src="https://cdn-icons-png.flaticon.com/512/3076/3076582.png" alt="Use Case">
    </div>
</div>


<div class="section">
    <div class="section-text">
        <h2>🌍 Social Good</h2>
        <p>This project contributes to the United Nations Sustainable Development Goals (SDGs) 
        by reducing food waste, alleviating hunger, and encouraging community-driven impact. 
        Together, providers and receivers create a sustainable cycle of sharing and caring.</p>
    </div>
    <div class="section-img">
        <img src="https://cdn-icons-png.flaticon.com/512/456/456212.png" alt="Social Good">
    </div>
</div>
""", unsafe_allow_html=True)
