import streamlit as st

def main(user_info):
    st.title(f"Profile Page for {user_info[3]}")

    st.markdown("---")  # Horizontal line separator

    # Personal Information Section
    st.subheader("Personal Information")
    st.markdown(f"""
    - **User ID:** `{user_info[0]}`
    - **Username:** `{user_info[1]}`
    - **Full Name:** `{user_info[3]}`
    - **Date of Birth:** `{user_info[4]}`
    - **Contact:** `{user_info[5]}`
    - **Address:** `{user_info[6]}`
    - **Email:** `{user_info[7]}`
    """)

    st.markdown("---")

    # Toggle Password Visibility
    st.subheader("Account Information")
    
    if "show_password" not in st.session_state:
        st.session_state["show_password"] = False

    if st.button("Show Password" if not st.session_state["show_password"] else "Hide Password"):
        st.session_state["show_password"] = not st.session_state["show_password"]

    password_display = user_info[2] if st.session_state["show_password"] else "********"
    st.markdown(f"- **Password:** `{password_display}`")

if __name__ == "__main__":
    user_info = ()
