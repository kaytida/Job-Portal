import streamlit as st
import mysql.connector

# Function to connect to the MySQL database
def connect_to_db():
    connection = mysql.connector.connect(
        host="dataserver.gramener.com",
        user="learnr",
        password="n&KZs6wa",
        database="campus_training"
    )
    return connection

# Function to retrieve and display jobs
def view_jobs():
    conn = None  # Initialize conn to None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "SELECT company, role, jobDescription, skillsrequired, jobtype, ctc FROM JobsGroup4"
        cursor.execute(query)
        jobs = cursor.fetchall()

        if not jobs:
            st.warning("No jobs found.")
            return

        # Determine the number of columns to display
        cols = st.columns(3)  # Adjust the number here based on how many jobs you want in each row
        
        # Loop through jobs and display each in its own column
        for index, job in enumerate(jobs):
            with cols[index % 3]:  # Cycle through columns
                st.markdown(f"### **{job[1]}** at **{job[0]}**")
                st.markdown(f"**Description:** {job[2]}")
                st.markdown(f"**Skills Required:** {job[3]}")
                st.markdown(f"**Job Type:** {job[4]}")
                st.markdown(f"**CTC:** ₹{job[5]:,}")
                st.markdown("---")

    except mysql.connector.Error as err:
        st.error(f"Failed to retrieve jobs: {err}")
    finally:
        if conn:  # Ensure conn is not None before closing
            conn.close()

