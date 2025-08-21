import streamlit as st
import pandas as pd
import db  # our database file
from datetime import datetime

st.set_page_config(page_title="Receivers Portal", page_icon="🥗", layout="wide")

if "receiver" not in st.session_state:
    st.session_state.receiver = None
if "active_page" not in st.session_state:
    st.session_state.active_page = None  # No page selected initially

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
        /* Center-align button container */
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 20px;
        }

        /* Style for vertical buttons */
        .stButton>button {
            width: 220px !important;
            padding: 8px 0;
            font-size: 15px !important;
            border-radius: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            margin: 6px 0;
            cursor: pointer;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.03);
        }
    </style>
""", unsafe_allow_html=True)

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
            st.session_state.active_page = None
            st.rerun()
        else:
            st.error("❌ Invalid Receiver ID or Contact Number!")

# ---------------- BROWSE FOOD ----------------
def browse_food():
    st.subheader("🍽️ Available Food Listings")

    # If claim was successful, show message and hide table
    if st.session_state.get("claim_success", False):
        st.success("🎉 Food claimed successfully!")
        # Reset after showing success
        if st.button("⬅️ Back to Food Listings"):
            st.session_state.claim_success = False
            st.rerun()
        return

    # Get food list
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

    # Show available food table
    st.dataframe(filtered_df, use_container_width=True)

    # Select food to claim
    selected_food_ids = st.multiselect("✅ Select Food to Claim", filtered_df["Food_ID"])
    claimed_qty = st.number_input("Enter Claimed Quantity", min_value=1, step=1)

    # Claim button logic
    if st.button("Claim Food 🍴"):
        if not selected_food_ids:
            st.error("⚠️ Please select at least one food item!")
        else:
            all_success = True
            for food_id in selected_food_ids:
                result = db.claim_food(food_id, st.session_state.receiver["Receiver_ID"], claimed_qty)
                if not result.get("success", False):
                    st.error(result.get("error", "⚠️ Something went wrong."))
                    all_success = False
                    break
            if all_success:
                # Set flag to hide table and show success
                st.session_state.claim_success = True
                st.rerun()


# ---------------- CLAIM HISTORY ----------------
def claim_history():
    st.subheader("📜 My Claim History")
    claims = db.get_claim_history(st.session_state.receiver["Receiver_ID"])
    if claims:
        st.dataframe(pd.DataFrame(claims), use_container_width=True)
    else:
        st.info("No claims yet.")


#------------------Account Section-----------------
def account_section():
    st.subheader("👤 My Account")

    # Fetch claim history
    claims = db.get_claim_history(st.session_state.receiver["Receiver_ID"])
    if claims:
        df = pd.DataFrame(claims)
        st.dataframe(df, use_container_width=True)

        # Filter pending claims only
        pending_claims = df[df["Status"].str.lower() == "pending"]

        if not pending_claims.empty:
            st.subheader("🗑️ Delete Pending Claims")
            claim_to_delete = st.multiselect(
                "Select Pending Claims to Delete",
                pending_claims["Claim_ID"]
            )

            if st.button("Delete Selected Claims"):
                if not claim_to_delete:
                    st.error("⚠️ Please select at least one pending claim to delete!")
                else:
                    for claim_id in claim_to_delete:
                        result = db.delete_claim(claim_id)
                        if not result.get("success", False):
                            st.error(f"❌ Failed to delete claim {claim_id}")
                            break
                    else:
                        st.success("✅ Selected pending claims deleted successfully!")
                        st.rerun()
        else:
            st.info("No pending claims to delete.")
    else:
        st.info("You haven't made any claims yet.")

    st.markdown("---")
    st.subheader("⚠️ Danger Zone")
    if st.button("🗑️ Delete My Receiver Account"):
        result = db.delete_receiver(st.session_state.receiver["Receiver_ID"])
        if result.get("success", False):
            st.success("✅ Your account has been deleted successfully!")
            st.session_state.receiver = None
            st.session_state.active_page = None
            st.rerun()
        else:
            st.error(result.get("error", "⚠️ Failed to delete your account."))



# ---------------- MAIN ----------------
st.title("🥗 Receivers Portal")

if st.session_state.receiver:
    st.success(f"Logged in as: {st.session_state.receiver['Name']}")

    # If no page selected, show centered buttons
    if st.session_state.active_page is None:
        st.markdown('<div class="center-container">', unsafe_allow_html=True)

        if st.button("🍽️ Browse Food"):
            st.session_state.active_page = "Browse Food"
            st.rerun()

        if st.button("📜 Claim History"):
            st.session_state.active_page = "Claim History"
            st.rerun()

        if st.button("👤 Account"):
            st.session_state.active_page = "Account"
            st.rerun()

        if st.button("🔒 Logout"):
            st.session_state.receiver = None
            st.session_state.active_page = None
            st.success("Logged out successfully!")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Show selected page content
        if st.session_state.active_page == "Browse Food":
            browse_food()
        elif st.session_state.active_page == "Claim History":
            claim_history()
        elif st.session_state.active_page == "Account":
            account_section()


        # Back button to go to menu
        if st.button("⬅️ Back to Menu"):
            st.session_state.active_page = None
            st.rerun()

else:
    # Login/Register Section
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.auth_tab = "Login"
    with col2:
        if st.button("📝 Register", use_container_width=True):
            st.session_state.auth_tab = "Register"
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")  # Navigate back to home page

    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "Login"

    if st.session_state.auth_tab == "Login":
        login_receiver()
    else:
        register_receiver()
