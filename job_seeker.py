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

# Function to fetch all job listings from the database
def fetch_job_listings():
    conn = mysql.connector.connect(
        host="dataserver.gramener.com",
        user="learnr",
        password="n&KZs6wa",
        database="campus_training"
    )
    cursor = conn.cursor()
    query = "SELECT * FROM JobsGroup4"
    cursor.execute(query)
    jobs = cursor.fetchall()
    conn.close()
    return jobs

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
            st.experimental_rerun()

        st.markdown(f"{user_location}")
        
        st.write("")
        if st.button("Jobs"):
            st.session_state['current_page'] = 'jobs'
            st.experimental_rerun()

        if st.button("Analysis"):
            st.session_state['current_page'] = 'analytics'
            st.experimental_rerun()
        
        st.write("")
        if st.button("Academics"):
            st.session_state['current_page'] = 'academics'
            st.experimental_rerun()
        
        if st.button("Skills"):
            st.session_state['current_page'] = 'skills'
            st.experimental_rerun()

        if st.button("Work Experience"):
            st.session_state['current_page'] = 'experience'
            st.experimental_rerun()

        if st.button("Languages"):
            st.session_state['current_page'] = 'languages'
            st.experimental_rerun()
        
        st.write("")
        if st.button("Calendar"):
            st.session_state['current_page'] = 'calendar'
            st.experimental_rerun()

        if st.button("Notices"):
            st.session_state['current_page'] = 'notices'
            st.experimental_rerun()
        
        if st.button("Tracker"):
            st.session_state['current_page'] = 'job Tracker'
            st.experimental_rerun()

        if st.button("Logout"):
            st.session_state['role'] = None
            st.experimental_rerun()
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