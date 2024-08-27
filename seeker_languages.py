import streamlit as st
import mysql.connector

# Function to update languages field in UserGroup4
def update_languages(user_id, new_language):
    try:
        conn = mysql.connector.connect(
            host="dataserver.gramener.com",
            user="learnr",
            password="n&KZs6wa",
            database="campus_training"
        )
        cursor = conn.cursor()
        query = "SELECT languages FROM UserGroup4 WHERE userId = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            languages = result[0]
            if languages:
                languages = f"{languages},{new_language}"
            else:
                languages = new_language
            update_query = "UPDATE UserGroup4 SET languages = %s WHERE userId = %s"
            cursor.execute(update_query, (languages, user_id))
            conn.commit()
            st.success("Language added successfully!")
        else:
            st.error("User not found.")
    except mysql.connector.Error as err:
        st.error(f"Failed to update languages: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def main(user_info):
    st.header("Languages")
    
    # Display existing languages
    languages = user_info[9].split(',')  # Assuming languages are stored as a comma-separated string
    for language in languages:
        st.write(f"- {language.strip()}")

    # Add Language Section
    st.header("Add Language")
    with st.form("add_language_form"):
        new_language = st.text_input("Language")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if new_language:  # Check for required fields
                # Assuming user_info[0] contains the user ID
                update_languages(user_info[0], new_language)
            else:
                st.error("Please enter a language.")

if __name__ == "__main__":
    # Replace this with actual user info in your application
    # user_info = ["1", "John Doe", "example@domain.com", "123-456-7890", "address", "city", "state", "country", "skill1,skill2", "English,Spanish", "education", "1,2,3,4"]  # Example user info
    main()
