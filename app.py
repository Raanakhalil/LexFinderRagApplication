import os
from groq import Groq
import streamlit as st
import pandas as pd

# Set your Groq API key
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Create a mock dataset with more relevant cases
mock_data = [
    {
        "case_title": "Smith v. Jones",
        "summary": "A landmark case that established the principle of duty of care.",
    },
    {
        "case_title": "Doe v. United States",
        "summary": "This case addressed issues related to search and seizure under the Fourth Amendment.",
    },
    {
        "case_title": "Roe v. Wade",
        "summary": "A pivotal Supreme Court case that legalized abortion in the United States.",
    },
    {
        "case_title": "Brown v. Board of Education",
        "summary": "A landmark decision that declared racial segregation in public schools unconstitutional.",
    },
    {
        "case_title": "Loving v. Virginia",
        "summary": "This case struck down laws banning interracial marriage, addressing civil rights.",
    },
    {
        "case_title": "Miranda v. Arizona",
        "summary": "This case established Miranda rights and protections under the Fifth Amendment.",
    },
    {
        "case_title": "Griswold v. Connecticut",
        "summary": "A case that recognized the right to privacy in marital relations and contraceptive use.",
    },
    {
        "case_title": "Tinker v. Des Moines",
        "summary": "A case that affirmed students' rights to free speech in public schools.",
    },
    {
        "case_title": "Furman v. Georgia",
        "summary": "A significant case regarding the death penalty and its application, addressing criminal law.",
    },
    {
        "case_title": "Obergefell v. Hodges",
        "summary": "This case legalized same-sex marriage across the United States, highlighting equal protection.",
    },
]

# Convert mock data to DataFrame for easy querying
mock_df = pd.DataFrame(mock_data)

def get_case_summary(user_query):
    # Search for relevant cases in the mock dataset
    relevant_cases = mock_df[mock_df['case_title'].str.contains(user_query, case=False) | 
                              mock_df['summary'].str.contains(user_query, case=False)]
    
    if not relevant_cases.empty:
        # Take the first relevant case for simplicity
        case_info = relevant_cases.iloc[0]
        case_title = case_info['case_title']
        case_summary = case_info['summary']
        
        # Generate a response using the Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Provide a detailed summary of the following case: {case_title}. Summary: {case_summary}",
                }
            ],
            model="llama3-8b-8192",
        )
        
        return chat_completion.choices[0].message.content
    else:
        return "No relevant cases found."

# Streamlit application
st.title("Legal Research Assistant")

# User input
user_query = st.text_input("Enter a case title or keyword:")

if st.button("Get Case Summary"):
    if user_query:
        summary = get_case_summary(user_query)
        st.write(summary)
    else:
        st.write("Please enter a case title or keyword.")
