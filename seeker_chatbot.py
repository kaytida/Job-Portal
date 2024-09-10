import requests
import streamlit as st

# Your LLM Foundry API token (keep this secure in production environments)
API_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkaXR5YS5rb25kYWlAc3RyYWl2ZS5jb20ifQ.QCKo1y1pkKxzAcrNPO96cMfVOXnRZOqVlQzWgXB9c2M"
API_URL = "https://llmfoundry.straive.com/openai/v1/chat/completions"

# Function to get chatbot response from LLM Foundry API
def chatbot_response(user_input):
    try:
        # Make the request to the LLM Foundry API
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_TOKEN}:my-test-project"},
            json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": user_input}]}
        )

        # Parse the response from the API
        if response.status_code == 200:
            data = response.json()
            # Extract the chatbot's response from the API result
            return data['choices'][0]['message']['content']
        else:
            return "Sorry, I am currently unable to process your request."

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main function to create the chatbot UI
def main(user_info):
    st.title("Job Portal Chatbot")

    # Initialize session state for chat history and input field
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ""

    # Custom CSS for alignment
    st.markdown("""
        <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            width: 100%;
            max-width: 600px;
            margin: auto;
        }
        .user-message {
            align-self: flex-end;
            background-color: #008080;
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
            max-width: 80%;
        }
        .chatbot-message {
            align-self: flex-start;
            background-color: #002F4C;
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
            max-width: 80%;
        }
        </style>
    """, unsafe_allow_html=True)

    # Display chat history
    st.write("### Chat History")
    chat_container = st.empty()  # Create an empty container for the chat

    with chat_container:
        chat_html = '<div class="chat-container">'
        for chat in st.session_state['chat_history']:
            if chat['role'] == 'user':
                chat_html += f'<div class="user-message">{chat["message"]}</div>'
            else:
                chat_html += f'<div class="chatbot-message">{chat["message"]}</div>'
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

    # User input
    user_input = st.text_input("Ask me something:", value=st.session_state['user_input'])
    
    if st.button("Send"):
        if user_input:
            # Append user input to the chat history
            st.session_state['chat_history'].append({"role": "user", "message": user_input})

            # Get chatbot response from the API and append it to the chat history
            response = chatbot_response(user_input)
            st.session_state['chat_history'].append({"role": "chatbot", "message": response})

            # Clear the input field by setting the session state value to an empty string
            st.session_state['user_input'] = ""
            st.rerun()  # Use experimental_rerun instead of rerun for better compatibility

if __name__ == "__main__":
    # Example user_info, modify as needed
    user_info = ["1", "John Doe", "john@example.com"]
    main(user_info)
