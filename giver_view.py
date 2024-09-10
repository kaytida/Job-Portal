import streamlit as st
import mysql.connector
import pandas as pd
from io import BytesIO
import twilio_helper

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

def view_jobs(user_info):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        user_id = user_info[0]
        query = "SELECT jobId, company, role, jobDescription, skillsrequired, jobtype, ctc FROM JobsGroup4 WHERE createdBy = %s"
        cursor.execute(query, (user_id,))
        jobs = cursor.fetchall()

        if not jobs:
            st.warning("No jobs found.")
            return

        cols = st.columns(3)
        for index, job in enumerate(jobs):
            with cols[index % 3]:
                st.markdown(f"### **{job[2]}** at **{job[1]}**")
                st.markdown(f"**Description:** {job[3]}")
                st.markdown(f"**Skills Required:** {job[4]}")
                st.markdown(f"**Job Type:** {job[5]}")
                st.markdown(f"**CTC:** ₹{job[6]:,}")
                
                if st.button(f"View Applicants", key=f"view_{job[0]}"):
                    st.session_state['selected_job_id'] = job[0]
                    view_applicants(job[0])
                st.markdown("---")

    except mysql.connector.Error as err:
        st.error(f"Failed to retrieve jobs: {err}")
    finally:
        if conn:
            conn.close()

def view_applicants(job_id):
    conn = None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
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

        # Store applicants and job ID in session state
        st.session_state['applicants'] = users
        st.session_state['selected_job_id'] = job_id

        df = pd.DataFrame(users, columns=["User ID", "Name", "Email", "Phone", "Skills", "Location"])

        st.markdown(f"## Applicants for Job ID: {job_id}")
        st.table(df)
        export_to_csv(df, f"job_{job_id}_applicants.csv")

        # Initialize message and sending status
        if 'message' not in st.session_state:
            st.session_state['message'] = ""
        if 'sending_status' not in st.session_state:
            st.session_state['sending_status'] = False

        # Text input for message
        message = "joker"
        send_messages_to_applicants(users, message)

       
    except mysql.connector.Error as err:
        st.error(f"Failed to retrieve applicants: {err}")
    finally:
        if conn:
            conn.close()

def send_messages_to_applicants(users, message):
    if not message:
        st.error("Please enter a message before sending.")
        return

    phone_numbers = [user[3] for user in users]
    for number in phone_numbers:
        try:
            sid = twilio_helper.send_whatsapp_message(number, message)
            st.write(f"Message sent to {number}. SID: {sid}")
        except Exception as e:
            st.error(f"Failed to send message to {number}: {e}")

    st.success("Messages sent to all applicants!")


# def view_applicants(job_id):
#     conn = None
#     try:
#         conn = connect_to_db()
#         cursor = conn.cursor()
#         query = """
#         SELECT userId, fullname, email, contact, skills, address
#         FROM UserGroup4 
#         WHERE FIND_IN_SET(%s, JobTrackerIds) > 0
#         """
#         cursor.execute(query, (job_id,))
#         users = cursor.fetchall()

#         if not users:
#             st.warning("No users have applied for this job.")
#             return

#         st.session_state['applicants'] = users
#         df = pd.DataFrame(users, columns=["User ID", "Name", "Email", "Phone", "Skills", "Location"])

#         st.markdown(f"## Applicants for Job ID: {job_id}")
#         st.table(df)
#         export_to_csv(df, f"job_{job_id}_applicants.csv")

#         if 'message' not in st.session_state:
#             st.session_state['message'] = "hi"

#         message = st.text_input("Enter your message to send to applicants:", value=st.session_state['message'])

#         if st.button("Send Message to Applicants"):
#             if message:
#                 send_messages_to_applicants(users, message)
#                 # Update the session state
#                 st.session_state['message'] = message
#             else:
#                 st.error("Please enter a message before sending.")

#     except mysql.connector.Error as err:
#         st.error(f"Failed to retrieve applicants: {err}")
#     finally:
#         if conn:
#             conn.close()

# def send_messages_to_applicants(users, message):
#     if not message:
#         st.error("Please enter a message before sending.")
#         return
    
#     phone_numbers = [user[3] for user in users]
#     for number in phone_numbers:
#         try:
#             sid = twilio_helper.send_whatsapp_message(number, message)
#             st.write(f"Message sent to {number}. SID: {sid}")
#         except Exception as e:
#             st.error(f"Failed to send message to {number}: {e}")
    
#     st.success("Messages sent to all applicants!")

if __name__ == "__main__":
    user_info = [1]  # Dummy user info

    if 'selected_job_id' in st.session_state and 'applicants' in st.session_state:
        view_applicants(st.session_state['selected_job_id'])
    else:
        view_jobs(user_info)
