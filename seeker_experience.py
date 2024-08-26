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

# Function to fetch work experience details
def fetch_work_experience(work_experience_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Query to fetch details for the given work experience ID
    cursor.execute('SELECT * FROM WorkExperienceGroup4 WHERE workExperienceId = %s', (work_experience_id,))
    result = cursor.fetchone()

    conn.close()

    return result

def main(user_info):
    st.title("Work Experience")
    st.write("This is the work experience page.")
    st.write("Here you can add or view your work experience.")

    st.header("Professional Information")
    
    # Loop through each work experience ID
    work_experience_ids = user_info[11].split(',')  # Assuming work experience IDs are stored as a comma-separated string
    for work_experience_id in work_experience_ids:
        work_experience_details = fetch_work_experience(work_experience_id.strip())  # Fetch work experience details
        
        if work_experience_details:
            # Display work experience details
            st.write(f"**Company:** {work_experience_details[1]}")  # Assuming column 1 is the company name
            st.write(f"**Role:** {work_experience_details[2]}")  # Assuming column 2 is the role
            st.write(f"**Duration:** {work_experience_details[3]}")  # Assuming column 3 is the duration
            st.write(f"**Description:** {work_experience_details[4]}")  # Assuming column 4 is the description
            st.write("---")
        else:
            st.write(f"No details found for Work Experience ID: {work_experience_id}")

    st.header("Resume")
    if user_info[12]:  # Check if a resume URL is available
        st.write(f"[Resume Link]({user_info[12]})")
    else:
        st.write("No resume uploaded.")

if __name__ == "__main__":
    main()
