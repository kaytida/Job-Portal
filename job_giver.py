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

# Function to add a new job posting
def post_job(company, role, job_description, skills_required, job_type, ctc):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = """
        INSERT INTO JobsGroup4 (company, role, jobDescription, skillsrequired, jobtype, ctc) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (company, role, job_description, skills_required, job_type, ctc))
        conn.commit()
        st.success("Job posted successfully!")
    except mysql.connector.Error as err:
        st.error(f"Failed to post job: {err}")
    finally:
        conn.close()

def main():
    st.header("Job Giver Dashboard")
    st.write("Here you can post jobs, manage applications, etc.")

    # Logout Button
    if st.button("Logout"):
        st.session_state['role'] = None
        st.experimental_rerun()

    # Post a Job Section
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
            if company and role and job_description and skills_required and job_type and ctc:  # Check for required fields
                post_job(company, role, job_description, skills_required, job_type, ctc)
            else:
                st.error("Please fill in all fields.")

if __name__ == "__main__":
    main()
