import streamlit as st
from model import LoanModel
import pandas as pd

data_path = "/home/greatness-within/Documents/data.csv"
obj = LoanModel(data_path)


# Define the questions
questions = [
    {"id": "work_experience", "text": "1) What is your work experience?", "type": "number","min_value": 0, "max_value": 10, "step":1},
    {"id": "google_maps", "text": "2) Is your shop visible on Google Maps?", "type": "options", "options": ["Yes", "No"]},
    {"id": "google_rating", "text": "2a) What is your rating on Google Maps?", "type": "number","min_value": 0, "max_value": 5, "step":0.5},
    {"id": "population_size", "text": "2b) What is the average estimated size of the population in the city where your shop is located?", "type": "number","min_value": 0,"step":1},
    {"id": "raw_material_cost", "text": "3) What is your raw material cost on a daily basis?", "type": "number","min_value": 0,"step":1},
    {"id": "monthly_income", "text": "4) What is your monthly income?", "type": "number","min_value": 0,"step":1},
    {"id": "monthly_expenditure", "text": "5) What is your monthly expenditure?", "type": "number","min_value": 0,"step":1},
    {"id": "CF_Rating", "text": "6) What is your average consumer feedback ?", "type": "number","min_value": 0,"max_value": 5,"step":1},
    {"id": "shop_open_days", "text": "7) How many days is your shop open in a week?", "type": "number","min_value": 0,"max_value": 7,"step":1},
]

# Initialize session state
if "responses" not in st.session_state:
    st.session_state.responses = {q["id"]: None for q in questions}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Reset the form
def reset_form():
    st.session_state.responses = {q["id"]: None for q in questions}
    st.session_state.submitted = False

# Submit the form
def submit_form():
    st.session_state.submitted = True

# Convert responses to JSON format
def format_responses_to_json():
    # Map the responses to the expected JSON structure
    data = {
        "Work_Experience": [st.session_state.responses["work_experience"]],
        "Google_Maps_Presence": [1 if st.session_state.responses["google_maps"] == "Yes" else 0],
        "Google_Maps_Rating": [st.session_state.responses["google_rating"]],
        "Population_in_Area_scaled": [st.session_state.responses["population_size"]],  # Scale population
          # Example: Replace with actual input if needed
        "Raw_Material_Cost": [st.session_state.responses["raw_material_cost"]],
        "Monthly_Income": [st.session_state.responses["monthly_income"]],
        "Monthly_Expenditure": [st.session_state.responses["monthly_expenditure"]],
        "CF_Rating": [st.session_state.responses["CF_Rating"]],  # Example value, replace as required
        "Consistency": [st.session_state.responses["shop_open_days"]],  # Example value, replace as required  # Example value, replace as required
    }
    return data

# Main interface
st.title("Interactive Questionnaire")

if not st.session_state.submitted:
    # Display each question
    for question in questions:
        st.write(f"### {question['text']}")

        if question["type"] == "options":
            st.session_state.responses[question["id"]] = st.radio(
                label="", options=question["options"], key=question["id"]
            )
        elif question["type"] == "number":
            st.session_state.responses[question["id"]] = st.number_input(
                label="", step=1.0, key=question["id"]
            )

        # Conditional visibility for dependent questions
        if (
            question["id"] == "google_maps"
            and st.session_state.responses["google_maps"] == "No"
        ):
            # Skip Google-related questions
            st.session_state.responses["google_rating"] = None
            st.session_state.responses["population_size"] = None

    # Submit and Retake buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit"):

            submit_form()
    with col2:
        if st.button("Retake"):
            reset_form()
else:
    # Display submitted responses
    st.success("Responses sent successfully!")
    st.write("### Your Responses in JSON Format:")
    json_data = format_responses_to_json()
    for question in questions:
        st.write(f"- **{question['text']}**: {st.session_state.responses[question['id']]}")

    # Option to save JSON to a file
    if st.button("Analyze JSON"):
        ans = obj.adjust_loan(pd.DataFrame(json_data))
        print(ans[0])
        st.write(f"He can be give a loan upto", ans[0])
        # st.json(json_file)
        # st.download_button("Download JSON File", json_file, "responses.json", "application/json")

    # Option to retake the questionnaire
    if st.button("Retake"):
        reset_form()
