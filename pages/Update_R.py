import streamlit as st
from db import   get_table,reciever_exists,update_receiver  # import your backend functions

st.title("Update Provider")
receiver_df = get_table("receivers")
if receiver_df.empty:
    st.warning("No providers found in the database.")

else:

    selected_id = st.selectbox("Select Provider ID to Update", receiver_df["Receiver_ID"].tolist())
    receiver = receiver_df[receiver_df["Receiver_ID"] == selected_id].iloc[0]

    with st.form("update_form"):
        name = st.text_input("Name", receiver["Name"])
        type_ = st.text_input("Type", receiver["Type"])
        city = st.text_input("City", receiver["City"])
        contact = st.text_input("Contact", receiver["Contact"])

        submit = st.form_submit_button("Update")
        if submit:
            if not reciever_exists(selected_id, receiver["Name"], receiver["Type"], receiver["Address"], receiver["City"], receiver["Contact"]):
                st.error("User does not exist!")
            else:
                update_receiver(selected_id, name, type_, city, contact)
                st.success(f"Receiver {selected_id} updated successfully!")
