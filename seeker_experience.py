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

    cursor.execute('SELECT * FROM WorkExperienceGroup4 WHERE workexperienceId = %s', (work_experience_id,))
    result = cursor.fetchone()

    conn.close()

    return result

# Function to add new work experience
def add_work_experience(workrole, jobmode, company, start_year, end_year):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = """
        INSERT INTO WorkExperienceGroup4 (workrole, jobmode, company, startYear, endYear) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (workrole, jobmode, company, start_year, end_year))
        conn.commit()

        # Retrieve the last inserted workexperienceId
        new_work_experience_id = cursor.lastrowid

        st.success("Work experience added successfully!")
        return new_work_experience_id
    except mysql.connector.Error as err:
        st.error(f"Failed to insert record: {err}")
        return None
    finally:
        conn.close()

# Function to update workExperienceIds field in UserGroup4
def update_work_experience_ids(user_id, new_work_experience_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "SELECT workExperienceIds FROM UserGroup4 WHERE userId = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            work_experience_ids = result[0]
            if work_experience_ids:
                work_experience_ids = f"{work_experience_ids},{new_work_experience_id}"
            else:
                work_experience_ids = str(new_work_experience_id)
            update_query = "UPDATE UserGroup4 SET workExperienceIds = %s WHERE userId = %s"
            cursor.execute(update_query, (work_experience_ids, user_id))
            conn.commit()
            st.success("Work Experience IDs updated successfully!")
        else:
            st.error("User not found.")
    except mysql.connector.Error as err:
        st.error(f"Failed to update Work Experience IDs: {err}")
    finally:
        conn.close()

def main(user_info):
    st.title("Work Experience")
    st.write("This is the work experience page.")
    st.write("Here you can add or view your work experience.")

    st.header("Professional Information")
    
    work_experience_ids = user_info[11].split(',')  # Assuming work experience IDs are stored as a comma-separated string
    for work_experience_id in work_experience_ids:
        work_experience_details = fetch_work_experience(work_experience_id.strip())
        
        if work_experience_details:
            st.write(f"**Role:** {work_experience_details[1]}")  # workrole
            st.write(f"**Job Mode:** {work_experience_details[2]}")  # jobmode
            st.write(f"**Company:** {work_experience_details[3]}")  # company
            st.write(f"**Start Year:** {work_experience_details[4]}")  # startYear
            st.write(f"**End Year:** {work_experience_details[5]}")  # endYear
            st.write("---")
        else:
            st.write(f"No details found for Work Experience ID: {work_experience_id}")

    st.header("Add Work Experience")
    with st.form("add_work_experience_form"):
        workrole = st.text_input("Role")
        jobmode = st.text_input("Job Mode")
        company = st.text_input("Company")
        start_year = st.date_input("Start Year")
        end_year = st.date_input("End Year")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if workrole and jobmode and company and start_year and end_year:  # Check for required fields
                new_work_experience_id = add_work_experience(workrole, jobmode, company, start_year, end_year)
                if new_work_experience_id:
                    update_work_experience_ids(user_info[0], new_work_experience_id)  # user_info[0] should be user ID
            else:
                st.error("Please fill in all fields.")

    st.header("Resume")
    if user_info[12]:  # Check if a resume URL is available
        st.write(f"[Resume Link]({user_info[12]})")
    else:
        st.write("No resume uploaded.")

if __name__ == "__main__":
    # Replace this with actual user info in your application
    # user_info = ["1", "John Doe", "example@domain.com", "123-456-7890", "address", "city", "state", "country", "skill1,skill2", "English,Spanish", "1,2,3", "resume_url"]  # Example user info
    main()
