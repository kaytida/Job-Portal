import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file
file_path = 'synthetic_rural_ap_job_data.csv'
df = pd.read_csv(file_path)

def plot_age_distribution():
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Age'], bins=20, kde=True, color='blue')
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    st.pyplot(plt)

def plot_education_distribution():
    plt.figure(figsize=(10, 6))
    sns.countplot(y=df['Education'], order=df['Education'].value_counts().index, palette='viridis')
    plt.title('Education Levels Distribution')
    plt.xlabel('Count')
    plt.ylabel('Education Level')
    st.pyplot(plt)

def plot_job_roles_distribution():
    plt.figure(figsize=(10, 6))
    sns.countplot(y=df['Applied Job Role'], order=df['Applied Job Role'].value_counts().index, palette='magma')
    plt.title('Applied Job Roles Distribution')
    plt.xlabel('Count')
    plt.ylabel('Job Role')
    st.pyplot(plt)

def plot_skills_distribution():
    df['Skills'] = df['Skills'].str.split(', ')
    skills_series = df['Skills'].explode()

    plt.figure(figsize=(12, 6))
    sns.countplot(y=skills_series, order=skills_series.value_counts().index, palette='coolwarm')
    plt.title('Skills Distribution')
    plt.xlabel('Count')
    plt.ylabel('Skills')
    st.pyplot(plt)

def plot_location_distribution():
    plt.figure(figsize=(10, 6))
    sns.countplot(y=df['Location'], order=df['Location'].value_counts().index, palette='Set2')
    plt.title('Location Distribution')
    plt.xlabel('Count')
    plt.ylabel('Location')
    st.pyplot(plt)

def plot_application_status_distribution():
    plt.figure(figsize=(10, 6))
    sns.countplot(x=df['Status of Job Application'], order=df['Status of Job Application'].value_counts().index, palette='Set1')
    plt.title('Status of Job Application Distribution')
    plt.xlabel('Application Status')
    plt.ylabel('Count')
    st.pyplot(plt)

def plot_experience_distribution():
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Experience'], bins=20, kde=True, color='green')
    plt.title('Experience Distribution')
    plt.xlabel('Years of Experience')
    plt.ylabel('Frequency')
    st.pyplot(plt)

def plot_education_job_roles_correlation():
    plt.figure(figsize=(12, 8))
    sns.countplot(y='Applied Job Role', hue='Education', data=df, palette='muted', order=df['Applied Job Role'].value_counts().index)
    plt.title('Correlation between Education and Applied Job Roles')
    plt.xlabel('Count')
    plt.ylabel('Applied Job Role')
    plt.legend(title='Education Level')
    st.pyplot(plt)

def plot_skills_success_rate():
    # Apply the success rate calculation
    df['Accepted'] = df['Status of Job Application'].apply(lambda x: 1 if x == 'Accepted' else 0)
    skills_success = df.explode('Skills').groupby('Skills')['Accepted'].mean().sort_values(ascending=False)

    # Plot the success rate by skills
    plt.figure(figsize=(12, 6))
    skills_success.plot(kind='bar', color='teal')
    plt.title('Success Rate by Skills')
    plt.xlabel('Skills')
    plt.ylabel('Success Rate')
    st.pyplot(plt)

def main(user_info):
    st.title("Analysis")
    # st.write("This is the companies page.")
    # st.write("Here you can browse and view information about various companies.")

    # Add analysis options
    st.header("Data Analytics")
    analysis_option = st.selectbox("Choose Analysis", [
        "Age Distribution",
        "Education Levels Distribution",
        "Applied Job Roles Distribution",
        "Skills Distribution",
        "Location Distribution",
        "Application Status Distribution",
        "Experience Distribution",
        "Correlation between Education and Applied Job Roles",
        "Success Rate by Skills"
    ])

    if analysis_option == "Age Distribution":
        plot_age_distribution()
    elif analysis_option == "Education Levels Distribution":
        plot_education_distribution()
    elif analysis_option == "Applied Job Roles Distribution":
        plot_job_roles_distribution()
    elif analysis_option == "Skills Distribution":
        plot_skills_distribution()
    elif analysis_option == "Location Distribution":
        plot_location_distribution()
    elif analysis_option == "Application Status Distribution":
        plot_application_status_distribution()
    elif analysis_option == "Experience Distribution":
        plot_experience_distribution()
    elif analysis_option == "Correlation between Education and Applied Job Roles":
        plot_education_job_roles_correlation()
    elif analysis_option == "Success Rate by Skills":
        plot_skills_success_rate()

if __name__ == "__main__":
    main()
