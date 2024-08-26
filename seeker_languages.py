import streamlit as st

def main(user_info):
    st.header("Languages")
    
    languages = user_info[9].split(',')  # Assuming languages are stored as a comma-separated string
    for language in languages:
        st.write(f"- {language.strip()}")

if __name__ == "__main__":
    main()
