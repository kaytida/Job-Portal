import streamlit as st
import mysql.connector

# Function to connect to the database and fetch job tracker details
def fetch_tracker_details(tracker_id):
    conn = mysql.connector.connect(
        host="dataserver.gramener.com",
        user="learnr",
        password="n&KZs6wa",
        database="campus_training"
    )
    cursor = conn.cursor()
    query = "SELECT jobId, status FROM JobTrackerGroup4 WHERE JobTrackerIds = %s"
    cursor.execute(query, (tracker_id,))
    result = cursor.fetchone()
    conn.close()
    return result

# Function to fetch job details based on jobId
def fetch_job_details(job_id):
    conn = mysql.connector.connect(
        host="dataserver.gramener.com",
        user="learnr",
        password="n&KZs6wa",
        database="campus_training"
    )
    cursor = conn.cursor()
    query = "SELECT jobId, company, role,jobDescription,ctc FROM JobsGroup4 WHERE jobId = %s"
    cursor.execute(query, (job_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def main(user_info):
    st.header("Job Tracker")
    
    # Assuming user_info[14] contains a comma-separated list of tracker IDs
    tracker_ids = user_info[14].split(',')

    for tracker_id in tracker_ids:
        tracker_id = tracker_id.strip()  # Remove any extra spaces
        
        # Fetch tracker details
        tracker_details = fetch_tracker_details(tracker_id)
        
        if tracker_details:
            job_id, status = tracker_details
            
            # Fetch job details based on job_id
            job_details = fetch_job_details(job_id)
            
            if job_details:
                job_id, company,role,jobDescription,ctc = job_details
                st.write(f"**Job Title:** {job_id}")
                st.write(f"**Company:** {company}")
                st.write(f"**Role:** {role}")
                st.write(f"**Status:** {status}")
                st.write(f"**jobDescription:** {jobDescription}")
                st.write(f"**ctc:** {ctc}")

                st.write("---")  # Divider between each job entry
            else:
                st.write(f"No job details found for Job ID: {job_id}")
        else:
            st.write(f"No tracker details found for Tracker ID: {tracker_id}")

if __name__ == "__main__":
    # Replace this with actual user info in your application
    main()
