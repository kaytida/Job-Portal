import streamlit as st
import mysql.connector

# Function to update skills field in UserGroup4
def update_skills(user_id, new_skill):
    try:
        conn = mysql.connector.connect(
            host="dataserver.gramener.com",
            user="learnr",
            password="n&KZs6wa",
            database="campus_training"
        )
        cursor = conn.cursor()
        query = "SELECT skills FROM UserGroup4 WHERE userId = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            skills = result[0]
            if skills:
                skills = f"{skills},{new_skill}"
            else:
                skills = new_skill
            update_query = "UPDATE UserGroup4 SET skills = %s WHERE userId = %s"
            cursor.execute(update_query, (skills, user_id))
            conn.commit()
            st.success("Skill added successfully!")
        else:
            st.error("User not found.")
    except mysql.connector.Error as err:
        st.error(f"Failed to update skills: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def main(user_info):
    st.header("Skills")
    
    # Display existing skills
    skills = user_info[8].split(',')  # Assuming skills are stored as a comma-separated string
    for skill in skills:
        st.write(f"- {skill.strip()}")

    # Add Skill Section
    st.header("Add Skill")
    with st.form("add_skill_form"):
        new_skill = st.text_input("Skill")
        submitted = st.form_submit_button("Submit")

        if submitted:
            if new_skill:  # Check for required fields
                # Assuming user_info[0] contains the user ID
                update_skills(user_info[0], new_skill)
            else:
                st.error("Please enter a skill.")

if __name__ == "__main__":
    # Replace this with actual user info in your application
    main()
