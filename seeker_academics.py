import streamlit as st
import mysql.connector

# Function to connect to the database and fetch education details
def fetch_education_details(education_id):
    conn = mysql.connector.connect(
        host="dataserver.gramener.com",
        user="learnr",
        password="n&KZs6wa",
        database="campus_training"
    )
    cursor = conn.cursor()
    query = "SELECT degree, grade, institution, startYear, endYear FROM EducationGroup4 WHERE educationId = %s"
    cursor.execute(query, (education_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def main(user_info):
    st.title("Academics")
    st.write("This is the academics page.")
    st.write("Here you can add or view academic qualifications.")

    st.header("Academic Information")

    # Assuming user_info[10] contains a comma-separated string of education IDs
    education_ids = user_info[10].split(',')

    for education_id in education_ids:
        education_id = education_id.strip()  # Remove any extra spaces
        education_details = fetch_education_details(education_id)

        if education_details:
            degree, grade, institution, start_year, end_year = education_details
            st.write(f"**Degree:** {degree}")
            st.write(f"**Grade:** {grade}")
            st.write(f"**Institution:** {institution}")
            st.write(f"**Start Year:** {start_year}")
            st.write(f"**End Year:** {end_year}")
            st.write("---")  # Divider between each entry
        else:
            st.write(f"No academic qualifications found for Education ID: {education_id}")

if __name__ == "__main__":
    # Replace this with actual user info in your application
    main()
