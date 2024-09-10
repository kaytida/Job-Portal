import streamlit as st
import mysql.connector
import pandas as pd
from io import BytesIO
import twilio_helper

# Function to connect to the MySQL database
def connect_to_db():
    connection = mysql.connector.connect(
        host="dataserver.gramener.com",
        user="learnr",
        password="n&KZs6wa",
        database="campus_training"
    )
    return connection

def export_to_csv(df, filename):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    st.download_button(label="Download CSV", data=buffer, file_name=filename, mime="text/csv")

# Function to retrieve and display jobs
def view_jobs(user_info):
    conn = None  # Initialize conn to None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        user_id = user_info[0]  # Assuming user_info contains the logged-in user info and the first element is the user ID
        query = "SELECT jobId, company, role, jobDescription, skillsrequired, jobtype, ctc FROM JobsGroup4 WHERE createdBy = %s"
        cursor.execute(query, (user_id,))
        jobs = cursor.fetchall()

        if not jobs:
            st.warning("No jobs found.")
            return

        # Determine the number of columns to display
        cols = st.columns(3)  # Adjust the number here based on how many jobs you want in each row
        
        # Loop through jobs and display each in its own column
        for index, job in enumerate(jobs):
            with cols[index % 3]:  # Cycle through columns
                st.markdown(f"### **{job[2]}** at **{job[1]}**")
                st.markdown(f"**Description:** {job[3]}")
                st.markdown(f"**Skills Required:** {job[4]}")
                st.markdown(f"**Job Type:** {job[5]}")
                st.markdown(f"**CTC:** ₹{job[6]:,}")
                if st.button(f"View Applicants", key=f"view_{job[0]}"):
                    view_applicants(job[0])  # Pass the jobId to view_applicants function
                st.markdown("---")

    except mysql.connector.Error as err:
        st.error(f"Failed to retrieve jobs: {err}")
    finally:
        if conn:  # Ensure conn is not None before closing
            conn.close()

# Function to display users who have applied for the selected job
def view_applicants(job_id):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        # Fetch users who have applied for this job (jobId in JobTrackerIds)
        query = """
        SELECT userId, fullname, email, contact, skills, address
        FROM UserGroup4 
        WHERE FIND_IN_SET(%s, JobTrackerIds) > 0
        """
        cursor.execute(query, (job_id,))
        users = cursor.fetchall()

        if not users:
            st.warning("No users have applied for this job.")
            return

        # Create a DataFrame for exporting
        df = pd.DataFrame(users, columns=["User ID", "Name", "Email", "Phone", "Skills", "Location"])

        # Display the users in a table
        st.markdown(f"## Applicants for Job ID: {job_id}")
        st.table(df)

        # Export options
        st.write("")
        export_to_csv(df, f"job_{job_id}_applicants.csv")

        st.write("")

        # Initialize the session state for the message and button click
        if "message" not in st.session_state:
            st.session_state["message"] = ""
        if "button_clicked" not in st.session_state:
            st.session_state["button_clicked"] = False

        # Update session state when the text area changes
        st.session_state["message"] = st.text_area("Enter your message to send to applicants:", value=st.session_state["message"])

        # Function to handle the button click
        def handle_click():
            st.session_state["button_clicked"] = True

        # Button for sending messages
        st.button("Contact Me", on_click=handle_click)

        # Send the message only if the button was clicked

        phone_numbers = [user[3] for user in users]  # Extract phone numbers from user data
        message = "hi"
        # Send message to each phone number
        for number in phone_numbers:
            try:
                sid = twilio_helper.send_whatsapp_message(number, message)  # Send to each number
                st.write(f"Message sent to {number}. SID: {sid}")
            except Exception as e:
                st.error(f"Failed to send message to {number}: {e}")
        st.success("Messages sent to all applicants!")
        
        # Reset the button clicked state after sending
        st.session_state["button_clicked"] = False

    except mysql.connector.Error as err:
        st.error(f"Failed to retrieve applicants: {err}")
    finally:
        if conn:  # Ensure conn is not None before closing
            conn.close()
