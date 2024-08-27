import streamlit as st
import mysql.connector
from googletrans import Translator
import job_seeker
import job_giver
import admin

# Function to connect to the MySQL database
def connect_to_db():
    connection = mysql.connector.connect(
        host="dataserver.gramener.com",
        user="learnr",
        password="n&KZs6wa",
        database="campus_training"
    )
    return connection

# Simulate a login function (replaces startswith check with database query)
def authenticate(email, password):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM UserGroup4 WHERE username = %s AND password = %s', (email, password))
    result = cursor.fetchone()

    conn.close()

    return result

# Helper function to translate text
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Main app function
def main():
    # Initialize the translator
    translator = Translator()

    # Language selection
    language_options = {
        "English": "en",
        "Telugu": "te"
    }
    selected_language = st.sidebar.selectbox("Choose Language", list(language_options.keys()))
    selected_language_code = language_options[selected_language]
    
    # Initialize session state for role and language
    if 'role' not in st.session_state:
        st.session_state['role'] = None
    if 'language' not in st.session_state:
        st.session_state['language'] = selected_language_code

    # Update session language if changed
    if selected_language_code != st.session_state['language']:
        st.session_state['language'] = selected_language_code

    # App title
    st.title(translate_text("Job Portal", st.session_state['language']))

    if st.session_state['role'] is None:
        # User input for login
        email_label = translate_text("Enter your Email ID", st.session_state['language'])
        password_label = translate_text("Enter your Password", st.session_state['language'])
        login_button = translate_text("Login", st.session_state['language'])
        
        email = st.text_input(email_label)
        password = st.text_input(password_label, type="password")

        if st.button(login_button):
            result = authenticate(email, password)
            user_role = ''
            if result:
                role = result[13]  # Assuming the role is in the 14th column (index 13)
                if role == 'Employer':
                    user_role = "job_giver"
                elif role == 'User':
                    user_role = "job_seeker"
                elif role == 'Admin':
                    user_role = "admin"

                # If user_role is determined, update the session state
                if user_role:
                    st.session_state['role'] = user_role
                    st.session_state['user_info'] = result  # Store result in session state
                    # Rerun is unnecessary because the UI will update automatically

            else:
                st.error(translate_text("Invalid email or password. Please try again.", st.session_state['language']))
    else:
        # Display the correct page based on role
        if st.session_state['role'] == "job_seeker":
            job_seeker.main(st.session_state['user_info'])
        elif st.session_state['role'] == "job_giver":
            job_giver.main()
        elif st.session_state['role'] == "admin":
            admin.main()

if __name__ == "__main__":
    main()
