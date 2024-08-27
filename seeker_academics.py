import streamlit as st
import mysql.connector

# Function to connect to the database and fetch education details
def fetch_education_details(education_id):
    try:
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
        return result
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Function to insert new education details into the database
def add_education(degree, grade, institution, start_year, end_year):
    try:
        conn = mysql.connector.connect(
            host="dataserver.gramener.com",
            user="learnr",
            password="n&KZs6wa",
            database="campus_training"
        )
        cursor = conn.cursor()
        query = """
        INSERT INTO EducationGroup4 (degree, grade, institution, startYear, endYear) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (degree, grade, institution, start_year.strftime('%Y-%m-%d'), end_year.strftime('%Y-%m-%d')))
        conn.commit()

        # Retrieve the last inserted educationId
        new_education_id = cursor.lastrowid

        st.success("Education added successfully!")
        return new_education_id
    except mysql.connector.Error as err:
        st.error(f"Failed to insert record: {err}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Function to update educationIds field in UserGroup4
def update_education_ids(user_id, new_education_id):
    try:
        conn = mysql.connector.connect(
            host="dataserver.gramener.com",
            user="learnr",
            password="n&KZs6wa",
            database="campus_training"
        )
        cursor = conn.cursor()
        query = "SELECT educationIds FROM UserGroup4 WHERE userId = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            education_ids = result[0]
            if education_ids:
                education_ids = f"{education_ids},{new_education_id}"
            else:
                education_ids = str(new_education_id)
            update_query = "UPDATE UserGroup4 SET educationIds = %s WHERE userId = %s"
            cursor.execute(update_query, (education_ids, user_id))
            conn.commit()
            st.success("Education IDs updated successfully!")
        else:
            st.error("User not found.")
    except mysql.connector.Error as err:
        st.error(f"Failed to update Education IDs: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

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

    # Add Education Section
    st.header("Add Education")
    with st.form("add_education_form"):
        degree = st.text_input("Degree")
        grade = st.number_input("Grade", min_value=0.0, max_value=4.0, step=0.01)
        institution = st.text_input("Institution")
        start_year = st.date_input("Start Year")
        end_year = st.date_input("End Year")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if degree and institution and start_year and end_year:  # Check for required fields
                new_education_id = add_education(degree, grade, institution, start_year, end_year)
                if new_education_id:
                    # Assuming user_info[0] contains the user ID
                    update_education_ids(user_info[0], new_education_id)
            else:
                st.error("Please fill in all required fields.")

if __name__ == "__main__":
    # Replace this with actual user info in your application
    user_info = ["1", "John Doe", "1,2,3,4"]  # Example user info with user ID and education IDs
    main(user_info)
