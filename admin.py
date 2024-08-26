import streamlit as st

def main():
    st.header("Admin Dashboard")
    st.write("Here you can manage users, view reports, etc.")
    if st.button("Logout"):
        st.session_state['role'] = None
        st.experimental_rerun()

if __name__ == "__main__":
    main()
