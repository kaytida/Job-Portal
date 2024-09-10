import streamlit as st
from giver_view import view_jobs  # Import the view_jobs function from giver_view.py
from giver_delete import render_delete_job  # Import the delete job function from giver_delete.py
import mysql.connector
import twilio_helper  # Ensure this module has the function to send WhatsApp messages

# Function to connect to the MySQL database
def connect_to_db():
    connection = mysql.connector.connect(
        host="dataserver.gramener.com",
        user="learnr",
        password="n&KZs6wa",
        database="campus_training"
    )
    return connection

def send_notifications(job_details):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        
        # Fetch all user contacts
        query = "SELECT contact FROM UserGroup4"
        cursor.execute(query)
        users = cursor.fetchall()
        
        # Create a message for the new job
        message = f"A new job has been posted!\n\nJob Details:\nCompany: {job_details['company']}\nRole: {job_details['role']}\nDescription: {job_details['job_description']}\nSkills Required: {job_details['skills_required']}\nJob Type: {job_details['job_type']}\nCTC: ₹{job_details['ctc']:,}\n\nPlease apply if interested."
        
        # Send the message to all users
        for user in users:
            phone_number = user[0]
            try:
                sid = twilio_helper.send_whatsapp_message(phone_number, message)  # Ensure this function is defined in twilio_helper
                st.write(f"Notification sent to {phone_number}. SID: {sid}")
            except Exception as e:
                st.error(f"Failed to send message to {phone_number}: {e}")

        st.success("Notifications sent to all users!")

    except mysql.connector.Error as err:
        st.error(f"Failed to retrieve users or send notifications: {err}")
    finally:
        if conn:
            conn.close()

# Function to add a new job posting
def post_job(user_id, company, role, job_description, skills_required, job_type, ctc):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = """
        INSERT INTO JobsGroup4 (company, role, jobDescription, skillsrequired, jobtype, ctc, createdBy) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (company, role, job_description, skills_required, job_type, ctc, user_id))
        conn.commit()
        st.success("Job posted successfully!")

        # Send notifications to users
        job_details = {
            'company': company,
            'role': role,
            'job_description': job_description,
            'skills_required': skills_required,
            'job_type': job_type,
            'ctc': ctc
        }
        send_notifications(job_details)

    except mysql.connector.Error as err:
        st.error(f"Failed to post job: {err}")
    finally:
        if conn:
            conn.close()

def main(user_info):
    st.sidebar.title("Job Giver Dashboard")
    
    if st.sidebar.button("Post a Job"):
        st.session_state.page = "post_job"
    if st.sidebar.button("View Jobs"):
        st.session_state.page = "view_jobs"
    if st.sidebar.button("Delete a Job"):
        st.session_state.page = "delete_job"
    
    if st.sidebar.button("Logout"):
        st.session_state['role'] = None
        st.rerun()

    if 'page' not in st.session_state:
        st.session_state.page = "post_job"

    if st.session_state.page == "post_job":
        st.header("Post a Job")
        with st.form("post_job_form"):
            company = st.text_input("Company")
            role = st.text_input("Role")
            job_description = st.text_area("Job Description")
            skills_required = st.text_input("Skills Required")
            job_type = st.selectbox("Job Type", ['Full-time', 'Part-time', 'Internship', 'Remote'])
            ctc = st.number_input("CTC", min_value=0, step=1000)
            submitted = st.form_submit_button("Post Job")

            if submitted:
                if company and role and job_description and skills_required and job_type and ctc:
                    user_id = user_info[0]
                    post_job(user_id, company, role, job_description, skills_required, job_type, ctc)
                else:
                    st.error("Please fill in all fields.")

    elif st.session_state.page == "view_jobs":
        st.header("View Jobs")
        view_jobs(user_info)

    elif st.session_state.page == "delete_job":
        render_delete_job()

if __name__ == "__main__":
    main()
