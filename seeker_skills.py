import streamlit as st

def main(user_info):
    st.header("Skills")
    
    skills = user_info[8].split(',')  # Assuming skills are stored as a comma-separated string
    for skill in skills:
        st.write(f"- {skill.strip()}")

if __name__ == "__main__":
    main()
