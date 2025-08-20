import streamlit as st
import pandas as pd
import db  # our database file
from datetime import datetime

st.set_page_config(page_title="Receivers Portal", page_icon="🥗", layout="wide")

if "receiver" not in st.session_state:
    st.session_state.receiver = None

# ---------------- REGISTER ----------------
def register_receiver():
    st.subheader("📝 Register as Receiver")
    receiver_id = st.text_input("Receiver ID")
    name = st.text_input("Receiver Name")
    r_type = st.selectbox("Receiver Type", ["NGO", "Individual", "Orphanage", "Other"])
    city = st.text_input("City")
    contact = st.text_input("Contact Number")

    if st.button("Register ✅"):
        if receiver_id.strip() == "" or name.strip() == "" or contact.strip() == "":
            st.error("⚠️ Please fill all required fields!")
        else:
            result = db.add_receiver(receiver_id, name, r_type, city, contact)
            if result["success"]:
                st.success("🎉 Registered successfully! Please login now.")
            else:
                st.error(result["error"])

# ---------------- LOGIN ----------------
def login_receiver():
    st.subheader("🔐 Receiver Login")
    receiver_id = st.text_input("Receiver ID")
    contact = st.text_input("Contact Number")

    if st.button("Login 🔑"):
        receiver = db.login_receiver(receiver_id, contact)
        if receiver:
            st.session_state.receiver = receiver
            st.success(f"Welcome, {receiver['Name']}! 🎉")
            st.rerun()
        else:
            st.error("❌ Invalid Receiver ID or Contact Number!")

# ---------------- BROWSE FOOD ----------------
def browse_food():
    st.subheader("🍽️ Available Food Listings")

    food_list = db.get_available_food()
    if not food_list:
        st.info("No food available right now.")
        return

    df = pd.DataFrame(food_list)

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        food_name_filter = st.text_input("🔍 Search by Food Name")
    with col2:
        location_filter = st.text_input("📍 Filter by Location")
    with col3:
        food_type_filter = st.selectbox("🥗 Filter by Food Type", ["All"] + list(df["Food_Type"].unique()))

    # Apply filters
    filtered_df = df.copy()
    if food_name_filter:
        filtered_df = filtered_df[filtered_df["Food_Name"].str.contains(food_name_filter, case=False)]
    if location_filter:
        filtered_df = filtered_df[filtered_df["Location"].str.contains(location_filter, case=False)]
    if food_type_filter != "All":
        filtered_df = filtered_df[filtered_df["Food_Type"] == food_type_filter]

    st.dataframe(filtered_df, use_container_width=True)

    # Select food to claim
    selected_food_ids = st.multiselect("✅ Select Food to Claim", filtered_df["Food_ID"])
    claimed_qty = st.number_input("Enter Claimed Quantity", min_value=1, step=1)

    if st.button("Claim Food 🍴"):
        if not selected_food_ids:
            st.error("⚠️ Please select at least one food item!")
        else:
            for food_id in selected_food_ids:
                result = db.claim_food(food_id, st.session_state.receiver["Receiver_ID"], claimed_qty)
                if result["success"]:
                    st.success(f"🎉 Successfully claimed {claimed_qty} units! Claim ID: {result['claim_id']}")
                else:
                    st.error(result["error"])
            st.rerun()

# ---------------- CLAIM HISTORY ----------------
def claim_history():
    st.subheader("📜 My Claim History")
    claims = db.get_claim_history(st.session_state.receiver["Receiver_ID"])
    if claims:
        st.dataframe(pd.DataFrame(claims), use_container_width=True)
    else:
        st.info("No claims yet.")

# ---------------- MAIN ----------------
st.title("🥗 Receivers Portal")

if st.session_state.receiver:
    st.sidebar.success(f"Logged in as: {st.session_state.receiver['Name']}")
    page = st.sidebar.radio("Navigation", ["Browse Food", "Claim History", "Logout"])

    if page == "Browse Food":
        browse_food()
    elif page == "Claim History":
        claim_history()
    elif page == "Logout":
        st.session_state.receiver = None
        st.success("🔒 Logged out successfully!")
        st.rerun()
else:
    auth_tab = st.radio("Choose Option", ["Login", "Register"])
    if auth_tab == "Login":
        login_receiver()
    else:
        register_receiver()
