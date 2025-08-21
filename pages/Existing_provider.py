import streamlit as st
import db  # your db.py
import pandas as pd
from datetime import datetime
import time
from utils import hide_sidebar

st.set_page_config(page_title="Provider Portal", layout="wide")
hide_sidebar()

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

    if st.button("⬅️ Back to Home"):
        st.switch_page("pages/Providers.py")  # replace with the actual page name


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

    # Fetch receivers and their claimed food details
    receivers = db.get_receivers_by_provider(provider["Provider_ID"])

    if receivers:
        # Convert to DataFrame for better table representation
        df = pd.DataFrame(receivers)

        # Rename columns for better readability if needed
        df = df.rename(columns={
            "Receiver_Name": "Receiver Name",
            "Receiver_ID": "Receiver ID",
            "Contact": "Contact",
            "Type": "Type",
            "Location": "Location",
            "Food_ID": "Food ID",
            "Food_Name": "Food Name",
            "Status": "Claim Status",
            "Timestamp": "Timestamp"
        })

        st.dataframe(df, use_container_width=True)

        st.markdown("### ✏️ Edit Claim Status")

        # Loop through each receiver to allow status editing if pending
        for r in receivers:
            if r["Status"].lower() == "pending":
                with st.expander(f"Edit Status for Claim ID: {r['Claim_ID']}"):
                    new_status = st.selectbox(
                        f"Select new status for {r['Receiver_Name']} (Claim ID: {r['Claim_ID']})",
                        options=["Pending", "Completed", "Cancelled"],
                        index=["Pending", "Completed", "Cancelled"].index(r["Status"])
                    )
                    if st.button(f"Update Status - Claim ID {r['Claim_ID']}"):
                        # Update claim status and timestamp in DB
                        db.update_claim_status(
                            claim_id=r["Claim_ID"],
                            new_status=new_status,
                            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        st.success(f"✅ Claim ID {r['Claim_ID']} updated to {new_status}")
                        st.rerun()
            else:
                st.info(f"Claim ID {r['Claim_ID']} is already '{r['Status']}' and cannot be edited.")

    else:
        st.info("No claims yet.")

    st.markdown("---")
    if st.button("⬅️ Back to Dashboard"):
        go_to("dashboard")


# --- ACCOUNT PAGE ---
elif st.session_state.page == "account":
    provider = st.session_state.provider
    st.subheader("⚙️ Account Settings")

    # ------------------------
    # Show & Update Provider Details
    # ------------------------
    st.write("### 🏢 Provider Details")
    with st.expander("✏️ Update Provider Details", expanded=False):
        new_name = st.text_input("Name", provider["Name"])
        # --- Provider Type selectbox with "Other" handling ---
        provider_types = ["Restaurant", "Supermarket", "Grocery Store", "Catering Service", "Other"]
        saved_type = provider["Type"]

        if saved_type in provider_types:
            type_index = provider_types.index(saved_type)
            other_value = ""
        else:
            type_index = provider_types.index("Other")
            other_value = saved_type  # prefill text input

        new_type = st.selectbox("Type", provider_types, index=type_index)

# Show text input only if "Other" is selected
        if new_type == "Other":
            other_type_input = st.text_input("If Other, please specify", value=other_value)
            final_type = other_type_input.strip() if other_type_input else "Other"
        else:
            final_type = new_type

        
        new_address = st.text_input("Address", provider["Address"])
        new_city = st.text_input("City", provider["City"])
        new_contact = st.text_input("Contact", provider["Contact"])

        if st.button("💾 Save Provider Changes"):
            db.update_provider(provider["Provider_ID"], new_name, final_type, new_address, new_city, new_contact)
            st.success("✅ Provider details updated successfully!")
            provider.update({
                "Name": new_name,
                "Type": new_type,
                "Address": new_address,
                "City": new_city,
                "Contact": new_contact
            })
            st.session_state.provider = provider

    st.markdown("---")

    # ------------------------
    # Add New Food Listing (Google Form Style)
    # ------------------------
    st.write("### ➕ Add New Food Listing")
    with st.expander("📝 Add Food", expanded=False):
        food_id=st.text_input("Food ID")
        food_name = st.text_input("Food Name")
        food_quantity = st.number_input("Quantity", min_value=1, step=1)
        expiry_date = st.date_input("Expiry Date")
        location = st.text_input("Location", provider["City"])
        food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan", "Other"])
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])

        if st.button("✅ Add Food"):
            if food_name.strip() == "":
                st.error("⚠️ Food Name cannot be empty!")
            elif not food_id.isdigit():
                    st.error("⚠️ Food ID must contain digits only!")
                    st.stop()
            else:
                result=db.add_food_listing(food_id, food_name, food_quantity, expiry_date, location, food_type, meal_type,provider["Provider_ID"],)
                if result["success"]:
                    st.success(f"🍽️ '{food_name}' added successfully!")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error(result["error"])
            
    st.markdown("---")

    # ------------------------
    # Show Existing Food Listings
    # ------------------------
    st.write("### 🍽️ Your Food Listings")
    food_listings = db.get_food_by_provider(provider["Provider_ID"])

    if not food_listings:
        st.info("You haven't added any food listings yet.")
    else:
        for food in food_listings:
            with st.expander(f"📌 {food['Food_Name']} ({food['Quantity']} items)"):
                # Show food details

                # Update existing food details
                st.write("#### ✏️ Update Food Details")
                updated_food_id = st.number_input("Food ID", food["Food_ID"], key=f"fid_{food['Food_ID']}")
                updated_food_name = st.text_input("Food Name", food["Food_Name"], key=f"name_{food['Food_ID']}")
                updated_quantity = st.number_input("Quantity", min_value=0, step=1, value=food["Quantity"], key=f"qty_{food['Food_ID']}")
                updated_expiry = st.date_input("Expiry Date", food["Expiry_Date"], key=f"expiry_{food['Food_ID']}")
                updated_location = st.text_input("Location", food["Location"], key=f"loc_{food['Food_ID']}")
                updated_food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan", "Other"],
                                                 index=["Vegetarian", "Non-Vegetarian", "Vegan", "Other"].index(food["Food_Type"]),
                                                 key=f"type_{food['Food_ID']}")
                updated_meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"],
                                                index=["Breakfast", "Lunch", "Dinner", "Snack"].index(food["Meal_Type"]),
                                                key=f"meal_{food['Food_ID']}")

                # Save updated food details
                if st.button(f"💾 Save {food['Food_Name']} Changes", key=f"save_{food['Food_ID']}"):
                    db.update_food_listing(food["Food_ID"], updated_food_name, updated_quantity, updated_expiry,
                                           updated_location, updated_food_type, updated_meal_type)
                    st.success(f"✅ '{updated_food_name}' updated successfully!")
                    st.rerun()

                # Delete food listing
                if st.button(f"🗑️ Delete {food['Food_Name']}", key=f"del_{food['Food_ID']}"):
                    db.delete_food(food["Food_ID"])
                    st.success(f"✅ '{food['Food_Name']}' deleted successfully!")
                    st.rerun()

    st.markdown("---")

    # ------------------------
    # Delete Provider Account
    # ------------------------
    if st.button("❌ Delete My Account"):
        db.delete_provider(provider["Provider_ID"])
        st.success("✅ Account deleted successfully!")
        st.session_state.provider = None
        go_to("login")

    st.markdown("---")
    if st.button("⬅️ Back to Dashboard"):
        go_to("dashboard")
