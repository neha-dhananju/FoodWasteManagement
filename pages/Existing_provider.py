import streamlit as st
import db  # your db.py
import pandas as pd

st.set_page_config(page_title="Provider Portal", layout="wide")

# --- SESSION STATE INIT ---
if "page" not in st.session_state:
    st.session_state.page = "login"  # default
if "provider" not in st.session_state:
    st.session_state.provider = None

# --- NAVIGATION HANDLER ---
def go_to(page):
    st.session_state.page = page
    st.rerun()   # 🔑 ensures no double-click needed

# --- LOGIN PAGE ---
if st.session_state.page == "login":
    st.title("🔑 Provider Login")

    provider_id = st.text_input("Provider ID")
    contact = st.text_input("Contact Number")

    if st.button("Login"):
        provider = db.get_provider(provider_id)
        if provider is None:
            st.error("❌ Invalid Provider ID")
        elif str(provider["Contact"]) != str(contact):
            st.error("❌ Contact does not match")
        else:
            st.session_state.provider = provider
            go_to("dashboard")

# --- DASHBOARD ---
elif st.session_state.page == "dashboard":
    provider = st.session_state.provider
    st.title(f"👋 Welcome {provider['Name']}")

    st.write("### Choose an action:")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📦 Food Listings"):
            go_to("food_listings")
    with col2:
        if st.button("🙋 Receivers"):
            go_to("receivers")
    with col3:
        if st.button("⚙️ Account Settings"):
            go_to("account")

    # 👇 Back/Logout button positioned at bottom-left
    st.markdown("---")
    if st.button("⬅️ Logout", use_container_width=False):
        st.session_state.provider = None
        go_to("login")

# --- FOOD LISTINGS PAGE ---

elif st.session_state.page == "food_listings":
    provider = st.session_state.provider
    st.subheader("📦 Your Food & Claims")

    foods = db.get_food_with_claims(provider["Provider_ID"])
    if foods:
        from collections import defaultdict
        grouped = defaultdict(list)

        # Group by Food_ID
        for f in foods:
            grouped[f["Food_ID"]].append(f)

        for food_id, items in grouped.items():
            food = items[0]  # main food info (same for all claims of this food)

            # --- Food details ---
            clean_data = {
                k: (v if v is not None else "-")
                for k, v in food.items()
                if k not in ["Claim_ID", "Receiver_ID", "Status", "Timestamp"]
            }
            df = pd.DataFrame([clean_data]).T
            df.columns = ["Details"]

            with st.expander(f"🍲 {food['Food_Name']} (ID: {food_id})"):
                st.table(df)

                # --- Claims (if any) ---
                claims_data = []
                for f in items:
                    if f.get("Claim_ID"):
                        claims_data.append({
                            "Receiver": f.get("Receiver_ID", "-"),
                            "Status": f.get("Status", "-"),
                            "Time": f.get("Timestamp", "-")
                        })

                if claims_data:
                    st.write("📋 Claims:")
                    st.table(pd.DataFrame(claims_data))

    else:
        st.info("No food listed yet.")

    st.markdown("---")
    if st.button("⬅️ Back to Dashboard", use_container_width=False):
        st.session_state.page = "dashboard"
        st.rerun()

# --- RECEIVERS PAGE ---
elif st.session_state.page == "receivers":
    provider = st.session_state.provider
    st.subheader("🙋 Receivers who claimed food")

    receivers = db.get_receivers_by_provider(provider["Provider_ID"])
    if receivers:
        for r in receivers:
            st.write(
                f"👤 {r['Receiver_Name']} | ID: {r['Receiver_ID']} | Contact: {r['Contact']} | Type: {r['Type']} | Location: {r['Location']}"
            )
    else:
        st.info("No claims yet.")

    st.markdown("---")
    if st.button("⬅️ Back to Dashboard"):
        go_to("dashboard")

# --- ACCOUNT PAGE ---
elif st.session_state.page == "account":
    provider = st.session_state.provider
    st.subheader("⚙️ Account Settings")

    st.write(f"Name: {provider['Name']}")
    st.write(f"Type: {provider['Type']}")
    st.write(f"Address: {provider['Address']}")
    st.write(f"City: {provider['City']}")
    st.write(f"Contact: {provider['Contact']}")

    if st.button("❌ Delete My Account"):
        db.delete_provider(provider["Provider_ID"])
        st.success("✅ Account deleted")
        st.session_state.provider = None
        go_to("login")

    st.markdown("---")
    if st.button("⬅️ Back to Dashboard"):
        go_to("dashboard")
