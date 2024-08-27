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

# Function to delete a job posting
def delete_job(company, role):
    conn = None  # Initialize conn to None
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = "DELETE FROM JobsGroup4 WHERE company = %s AND role = %s"
        cursor.execute(query, (company, role))
        conn.commit()
        
        if cursor.rowcount > 0:
            st.success("Job deleted successfully!")
        else:
            st.warning("No matching job found.")
    except mysql.connector.Error as err:
        st.error(f"Failed to delete job: {err}")
    finally:
        if conn:  # Ensure conn is not None before closing
            conn.close()

def render_delete_job():
    st.header("Delete a Job")
    with st.form("delete_job_form"):
        company = st.text_input("Company")
        role = st.text_input("Role")
        submitted = st.form_submit_button("Delete Job")

        if submitted:
            if company and role:
                delete_job(company, role)
            else:
                st.error("Please fill in both fields.")
