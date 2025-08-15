import streamlit as st
from db import   get_table,provider_exists,update_provider  # import your backend functions

st.title("Update Provider")
providers_df = get_table("providers")
if providers_df.empty:
    st.warning("No providers found in the database.")

else:

    selected_id = st.selectbox("Select Provider ID to Update", providers_df["Provider_ID"].tolist())
    provider = providers_df[providers_df["Provider_ID"] == selected_id].iloc[0]

    with st.form("update_form"):
        name = st.text_input("Name", provider["Name"])
        type_ = st.text_input("Type", provider["Type"])
        address = st.text_input("Address", provider["Address"])
        city = st.text_input("City", provider["City"])
        contact = st.text_input("Contact", provider["Contact"])

        submit = st.form_submit_button("Update")
        if submit:
            if not provider_exists(selected_id, provider["Name"], provider["Type"], provider["Address"], provider["City"], provider["Contact"]):
                st.error("User does not exist!")
            else:
                update_provider(selected_id, name, type_, address, city, contact)
                st.success(f"Provider {selected_id} updated successfully!")
