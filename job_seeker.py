import streamlit as st
import mysql.connector
import seeker_profile
import seeker_languages
import seeker_skills
import seeker_academics
import seeker_experience
import seeker_calendar
import seeker_notices
import seeker_analytics
import seeker_tracker
import seeker_chatbot

# Function to connect to the database
def connect_to_db():
    return mysql.connector.connect(
        host="dataserver.gramener.com",
        user="learnr",
        password="n&KZs6wa",
        database="campus_training"
    )

# Function to fetch all job listings from the database
def fetch_job_listings():
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM JobsGroup4"
    cursor.execute(query)
    jobs = cursor.fetchall()
    conn.close()
    return jobs

# Function to update JobTrackerIds for the user
def apply_for_job(user_id, job_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch the current JobTrackerIds for the user
    query = "SELECT JobTrackerIds FROM UserGroup4 WHERE userId = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    if result:
        job_tracker_ids = result[0]
        # Convert the current JobTrackerIds into a list, add the new jobId if not already present
        if job_tracker_ids:
            job_tracker_list = job_tracker_ids.split(',') if job_tracker_ids else []
            if str(job_id) not in job_tracker_list:
                job_tracker_list.append(str(job_id))
        else:
            job_tracker_list = [str(job_id)]
        
        # Convert list back to a comma-separated string
        updated_job_tracker_ids = ','.join(job_tracker_list)
        
        # Update the JobTrackerIds field in the database
        update_query = "UPDATE UserGroup4 SET JobTrackerIds = %s WHERE userId = %s"
        cursor.execute(update_query, (updated_job_tracker_ids, user_id))
        conn.commit()
        st.success(f"Successfully applied for job ID: {job_id}")

    conn.close()

# Updated display_jobs function with Apply button
def display_jobs(user_info):
    st.title("Job Portal")

    # Fetch all job listings from the database
    jobs = fetch_job_listings()

    # Job Filter options
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.button("All")
    with col2:
        st.button("Internship")
    with col3:
        st.button("Fresher")
    with col4:
        st.button("Entry Level")
    with col5:
        st.button("Internship + Full Time")

    # Display jobs in a grid
    cols = st.columns(4)
    for index, job in enumerate(jobs):
        with cols[index % 4]:
            st.image("https://via.placeholder.com/150", width=150)  # Placeholder image for company logo
            st.markdown(f"**{job[1]}**")  # Company name
            st.markdown(f"*{job[2]}*")  # Job role
            st.markdown(f"{job[5]}")    # Job type
            st.markdown(f"${job[6]:,.2f} per year")  # Salary formatted as currency

            # Apply Button
            if st.button(f"Apply for {job[2]}", key=f"apply_{job[0]}"):
                apply_for_job(user_info[0], job[0])  # Pass the userId and jobId to the apply function

# Main function to display the job portal and other pages
def main(user_info):
    # Initialize session state for navigation if not already set
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'jobs'  # Default to showing jobs

    user_name = user_info[3]
    user_location = "Hyderabad, Telangana"

    # Sidebar
    with st.sidebar:
        st.image("Blank-Profile-Picture-1.webp", width=100)  # Replace with user's profile picture if available
        
        if st.button(f"{user_name}"):
            st.session_state['current_page'] = 'profile'
            st.rerun()

        st.markdown(f"{user_location}")
        
        st.write("")
        if st.button("Jobs"):
            st.session_state['current_page'] = 'jobs'
            st.rerun()

        if st.button("Analysis"):
            st.session_state['current_page'] = 'analytics'
            st.rerun()
        
        st.write("")
        if st.button("Academics"):
            st.session_state['current_page'] = 'academics'
            st.rerun()
        
        if st.button("Skills"):
            st.session_state['current_page'] = 'skills'
            st.rerun()

        if st.button("Work Experience"):
            st.session_state['current_page'] = 'experience'
            st.rerun()

        if st.button("Languages"):
            st.session_state['current_page'] = 'languages'
            st.rerun()
        
        st.write("")
        if st.button("Calendar"):
            st.session_state['current_page'] = 'calendar'
            st.rerun()

        if st.button("Notices"):
            st.session_state['current_page'] = 'notices'
            st.rerun()
        
        if st.button("Tracker"):
            st.session_state['current_page'] = 'job Tracker'
            st.rerun()

        if st.button("Logout"):
            st.session_state['role'] = None
            st.rerun()

    # Main content area
    if st.session_state['current_page'] == 'profile':
        seeker_profile.main(user_info)
    elif st.session_state['current_page'] == 'jobs':
        display_jobs()  # Call a separate function to display the job portal
    elif st.session_state['current_page'] == 'analytics':
        seeker_analytics.main(user_info)
    elif st.session_state['current_page'] == 'academics':
        seeker_academics.main(user_info)
    elif st.session_state['current_page'] == 'skills':
        seeker_skills.main(user_info)
    elif st.session_state['current_page'] == 'experience':
        seeker_experience.main(user_info)
    elif st.session_state['current_page'] == 'languages':
        seeker_languages.main(user_info)
    elif st.session_state['current_page'] == 'calendar':
        seeker_calendar.main(user_info)
    elif st.session_state['current_page'] == 'notices':
        seeker_notices.main(user_info)
    elif st.session_state['current_page'] == 'job Tracker':
        seeker_tracker.main(user_info)
    elif st.session_state['current_page'] == 'chatbot':
        seeker_chatbot.main(user_info)

    # Notifications and Profile (Top-right corner)
    st.markdown("""
        <style>
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header div {
            margin-right: 20px;
        }
        </style>
        <div class="header">
            <div></div>
            <div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Standard Streamlit button for the chatbot
    if st.button("Chat with Chatbot"):
        st.session_state['current_page'] = 'chatbot'
        st.rerun()

# Function to display jobs fetched from the database
def display_jobs():
    st.title("Job Portal")

    # Fetch all job listings from the database
    jobs = fetch_job_listings()

    # Job Filter options
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.button("All")
    with col2:
        st.button("Internship")
    with col3:
        st.button("Fresher")
    with col4:
        st.button("Entry Level")
    with col5:
        st.button("Internship + Full Time")

    # Display jobs in a grid
    cols = st.columns(4)
    for index, job in enumerate(jobs):
        with cols[index % 4]:
            st.image("https://via.placeholder.com/150", width=150)  # Placeholder image for company logo
            st.markdown(f"**{job[1]}**")  # Company name
            st.markdown(f"*{job[2]}*")  # Job role
            st.markdown(f"{job[5]}")    # Job type
            st.markdown(f"${job[6]:,.2f} per year")  # Salary formatted as currency

if __name__ == "__main__":
    # Replace this with actual user info in your application
    user_info = [1, 'johndoe', 'password123', 'John Doe', '1990-01-01', '1234567890', '123 Main St', 'john.doe@example.com', 'Python, SQL', 'English, Spanish', '1,2', '3,4', 'http://example.com/resume.pdf', 'User', '5,6']
    main(user_info)