# helpdesk_support_bot.py

import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
#client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Call Type Categories
call_types = """
### 📞 Call Types

1. General Inquiry
2. Pricing & Discounts
3. Course Schedule
4. Registration Assistance
5. Change / Cancel Enrollment
6. Technical Support (Online Learning)
7. Certificate Request
8. Placement Test Request
9. Trial Class Booking
10. Course Format Inquiry
11. Teacher Info
12. Language Availability
13. Payment Issues
14. Children's Courses
15. Referral / Gift Questions
"""

# Build system prompt
system_prompt = f"""
You are a helpful support agent for a language learning center.

You can handle the following call types:

{call_types}

Instructions:

1. First, classify the user's question into one of the call types above.
2. Then, provide a helpful, friendly and professional response to the user.
3. Respond in the following format:

Call Type: <call type>
Response: <your helpful answer>

If the question does not fit any call type, say:
Call Type: Unknown
Response: I'm sorry, I cannot assist with this request. Please contact our support team.

Now process the following question.
"""

# Streamlit App Config
st.set_page_config(page_title="Helpdesk Support Bot", page_icon="🤖")
st.title("📞 Helpdesk Support Bot")
st.write("Ask your question about language courses — the bot will assist you!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# Display chat messages so far
for msg in st.session_state.messages[1:]:  # skip system prompt
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Append to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages,
                    max_tokens=500,
                    temperature=0.3,
                )
                assistant_reply = response.choices[0].message.content
                st.markdown(assistant_reply)

                # Append assistant reply to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

            except Exception as e:
                st.error(f"An error occurred: {e}")
