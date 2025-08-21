import streamlit as st
from datetime import date
from utils import hide_sidebar
import db
import re
# ---- Page Config ----
st.set_page_config(page_title="New Provider", layout="wide")
hide_sidebar()

# ---- Plain White Background + Card ----
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #ffffff !important; }
.form-card {
  max-width: 760px; margin: 2.5rem auto; padding: 2rem;
  background: #fff; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,.08);
}
.form-actions { display:flex; gap:12px; justify-content: space-between; }
.step { color:#666; font-weight:600; margin-bottom:.25rem; }
h1, h2, h3 { margin-top: 0; }
.note { color:#444; }
hr { border: none; border-top: 1px solid #eee; margin: 1rem 0 1.25rem; }
button[kind="secondary"] { background:#f6f6f6; }
</style>
""", unsafe_allow_html=True)

# ---- Session State ----
if "provider_step" not in st.session_state:
    st.session_state.provider_step = "provider"   # provider -> food -> thankyou
if "provider_data" not in st.session_state:
    st.session_state.provider_data = {}

# ---- Navigation helpers ----
def go_providers_home():
    """Back to Providers landing page."""
    try:
        # adjust path if your file name differs (e.g., "pages/Providers.py")
        st.switch_page("pages/Providers.py")
    except Exception:
        # Fallback: show a link if switch_page cannot resolve
        st.info("Use the sidebar to open **Providers**.")

def go_existing_login():
    try:
        st.switch_page("pages/Existing_provider.py")
    except Exception:
        st.info("Use the sidebar to open **Existing Provider**.")

# =========================================
# STEP 1 — PROVIDER DETAILS (Required)
# =========================================
if st.session_state.provider_step == "provider":
    with st.container():
        
        st.markdown('<div class="step">Step 1 of 2</div>', unsafe_allow_html=True)
        st.header("📝 Provider Details")
        st.caption("All fields are required.")

        with st.form("provider_form", clear_on_submit=False):
            col_a, col_b = st.columns(2)
            with col_a:
                if "provider_id_input" not in st.session_state:
                    st.session_state.provider_id_input = st.session_state.provider_data.get("provider_id", "")
                provider_id = st.text_input("Provider ID *",
                    value=re.sub(r'\D', '', st.session_state.provider_id_input),key="provider_id_input",
                    placeholder="Digits only (0–9)")
                provider_id_error = bool(provider_id and not provider_id.isdigit())
                if provider_id_error:
                    st.error("Please enter digits only (0–9).")

                name = st.text_input("Name *",
                    value=st.session_state.provider_data.get("name", ""))
                p_type = st.selectbox(
                    "Provider Type *",
                    ["Restaurant", "Supermarket", "Grocery Store", "Catering Service", "Other"],
                    index=(
                        ["Restaurant","Supermarket","Grocery Store","Catering Service","Other"]
                        .index(st.session_state.provider_data.get("p_type","Restaurant"))
                        if st.session_state.provider_data.get("p_type") else 0
                    ),
                )
                other_type = ""
                if p_type == "Other":
                    other_type = st.text_input("Please specify provider type *")
           
            with col_b:
                address = st.text_area("Address *",
                    value=st.session_state.provider_data.get("address", ""))
                city = st.text_input("City *",
                    value=st.session_state.provider_data.get("city", ""))
                contact = st.text_input("Contact Number *",
                    value=st.session_state.provider_data.get("contact", ""))

            c1, c2 = st.columns(2)
            back = c1.form_submit_button("⬅️ Back")
            next_btn = c2.form_submit_button("➡️ Next")

        # Handle actions after form exits
        if back:
            go_providers_home()

        if next_btn:
            # Required-field check
            provider_id = st.session_state.provider_id_input

            if not provider_id.isdigit():
                st.error("⚠️ Provider ID must contain digits only!")
            elif not all([provider_id.strip(), name.strip(), p_type.strip(),
                address.strip(), city.strip(), contact.strip()]):
                st.error("⚠️ Please fill all required fields (*)")
            elif p_type == "Other" and not other_type.strip():
                st.error("⚠️ Please specify the provider type when selecting 'Other'.")
            elif db.provider_id_exists(provider_id):
                st.error("⚠️ Provider ID already exists. Choose another.")
            else:
                final_p_type = other_type if p_type == "Other" else p_type
                st.session_state.provider_data = {
                "provider_id": provider_id,
                "name": name,
                "p_type": final_p_type,
                "address": address,
                "city": city,
                "contact": contact,
                }
                st.session_state.provider_step = "food"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# STEP 2 — FOOD LISTING (Optional)
# =========================================
elif st.session_state.provider_step == "food":
    with st.container():
        st.markdown('<div class="step">Step 2 of 2</div>', unsafe_allow_html=True)
        st.header("🍽 Optional Food Listing")
        st.caption("You can skip this step and submit only the provider details.")

        with st.form("food_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                food_id = st.text_input("Food ID (optional)")
                food_name = st.text_input("Food Name (optional)")
                quantity = st.number_input("Quantity (servings)", min_value=0, step=1, value=0)
                expiry = st.date_input("Expiry Date", value=date.today())
            with col2:
                food_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan", "Other"])
                meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
                location = st.text_input("Pickup Location (optional)")

            c1, c2 = st.columns(2)
            back = c1.form_submit_button("⬅️ Back")
            submit = c2.form_submit_button("✅ Submit")

        # Handle actions after form exits
        if back:
            st.session_state.provider_step = "provider"
            st.rerun()

        if submit:
            pd = st.session_state.provider_data

            # 1) Save provider (only if not already saved)
            if not db.provider_id_exists(pd["provider_id"]):
                db.add_provider(pd["provider_id"], pd["name"], pd["p_type"],
                                pd["address"], pd["city"], pd["contact"])
            

            # 2) Optionally save food if minimal fields provided
            if food_id or food_name:
                if not food_id:
                    st.error("⚠️ Please provide a Food ID.")
                    st.stop()  # stop submission
                elif not food_id.isdigit():
                    st.error("⚠️ Food ID must contain digits only!")
                    st.stop()
                elif db.food_id_exists(food_id):
                    st.error("Food ID already exists — skipping food save.")
                    st.stop()
                elif not food_name.strip():
                    st.error("⚠️ Food Name cannot be empty!")
                    st.stop()
                else:
                    db.add_food(
                        food_id, food_name, quantity, expiry,
                        pd["provider_id"], pd["p_type"], location, food_type, meal_type
                    )
            elif not food_id and not food_name:
                st.info("ℹ️ No food added. Only provider details submitted.")

            st.session_state.provider_step = "thankyou"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# STEP 3 — THANK YOU
# =========================================
elif st.session_state.provider_step == "thankyou":
    st.success("🎉 Thank you for filling the form!")
    st.write("You can **view or update** your information by logging in.")

    col1, col2 = st.columns(2)
    if col1.button("🔑 Go to Login"):
        go_existing_login()
    if col2.button("⬅️ Back to Providers"):
        go_providers_home()

    st.markdown('</div>', unsafe_allow_html=True)
