import streamlit as st

def main():
    st.header("Job Giver Dashboard")
    st.write("Here you can post jobs, manage applications, etc.")
    if st.button("Logout"):
        st.session_state['role'] = None
        st.experimental_rerun()

if __name__ == "__main__":
    main()
