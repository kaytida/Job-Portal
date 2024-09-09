import streamlit as st
import mysql.connector
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

# Main app function
def main():

    # Initialize session state for role
    if 'role' not in st.session_state:
        st.session_state['role'] = None

    # App title
    st.title("Job Portal")
    
    if st.session_state['role'] is None:
        # User input for login
        email = st.text_input("Enter your Email ID")
        password = st.text_input("Enter your Password", type="password")

        if st.button("Login"):
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
                st.error("Invalid email or password. Please try again.")
    else:
        # Display the correct page based on role
        if st.session_state['role'] == "job_seeker":
            job_seeker.main(st.session_state['user_info'])
        elif st.session_state['role'] == "job_giver":
            job_giver.main(st.session_state['user_info'])
        elif st.session_state['role'] == "admin":
            admin.main()

if __name__ == "__main__":
    main()
