import streamlit as st
from pathlib import Path
import pandas as pd
from utils import hide_sidebar



# ---- Page Config ----
st.set_page_config(page_title="Food Management System", layout="wide")
hide_sidebar()

# ---- Background Image ----
page_bg_img = """
<style>
html, body, [data-testid="stAppViewContainer"] {
    height: 100%;
    overflow: hidden; /* Prevent scrolling */
    margin: 0;
}

[data-testid="stAppViewContainer"] {
    background: 
        linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), /* Dark overlay */
        url("https://gicgrp.com/sg/website/wp-content/uploads/2021/11/Selection-of-healthy-rich-fiber-sources-vegan-food-for-cooking-812997516_1258x838-1024x683.jpeg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}


.title-text {
    text-align: center;
    color: white;
    font-size: 3em;
    font-weight: bold;
    margin-top: 50px;
    text-shadow: 2px 2px 4px #000000;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---- Title ----
st.markdown('<div class="title-text">Food Management System</div>', unsafe_allow_html=True)



st.markdown("""
    <style>
    .button-container {
        display: flex;
        justify-content: center;  /* Center horizontally */
        align-items: center;      /* Center vertically if needed */
        gap: 20px;                /* Space between buttons */
        flex-wrap: nowrap;        /* Keep them in a single row */
        margin-top: 30px;
    }
    .circular-button {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 150px;
        height: 150px;
        border-radius: 50%;
        font-size: 1.3em;
        font-weight: bold;
        border: none;
        background-color: rgba(255, 255, 255, 0.85);
        color: black;
        cursor: pointer;
        transition: transform 0.2s ease;
        text-decoration: none; /* Remove link underline if using <a> */
    }
    .circular-button:hover {
        transform: scale(1.1);
        background-color: rgba(255, 255, 255, 1);
    }
    </style>


    <div class="button-container">
        <a class="circular-button" href="/Providers">Providers</a>
        <a class="circular-button" href="/Receivers">Receivers</a>
        <a class="circular-button" href="/Claims">Claims</a>
        <a class="circular-button" href="/Food_Listings">Food Listings</a>
        <a class="circular-button" href="/Visualizing">Visualizing</a>
    </div>
""", unsafe_allow_html=True)
