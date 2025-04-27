import os
import csv
import datetime
import streamlit as st
import pandas as pd
import datetime

# Load the dataset
file_path = "college_cutoff_data_updated.csv"
df = pd.read_csv(file_path)
log_file = "recommendation_history.csv"


# Streamlit UI
st.title("College Recommendation System")

# Input from user
score = st.number_input("Enter your CET Percentile:", min_value=0.0, max_value=100.0, step=0.01)
category = st.selectbox("Select your Category:", ["General", "OBC", "SC", "ST"])

# Filter and Recommend Colleges
def recommend_colleges(score, category):
    filtered_df = df[df[category] <= score]  # Filter based on category-wise cutoff
    recommended_colleges = filtered_df.sort_values(by=[category], ascending=False)
    return recommended_colleges[["College", "Program", category]]

if st.button("Find Colleges"):
    recommendations = recommend_colleges(score, category)
    if recommendations.empty:
        st.warning("No colleges available for your percentile and category.")
    else:
        st.write("Recommended Colleges:")
        st.dataframe(recommendations)
    
    # Save to history
    log_file = "recommendation_history.csv"
    if not os.path.exists(log_file):
        with open(log_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["CET Percentile", "Category", "College Name", "recommendation", "Timestamp"])
    
    with open(log_file, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for _, row in recommendations.iterrows():
            csv_writer.writerow([score, category, row["College"], row["Program"], timestamp])

# View previous recommendations
if st.button("Show History"):
    if os.path.exists(log_file):
        try:
            # Read the history CSV file, skipping bad lines if necessary
            history_df = pd.read_csv(log_file, on_bad_lines='skip')
            
            # Check if the DataFrame is empty
            if history_df.empty:
                st.warning("No history available.")
            else:
                st.write(history_df)
        except Exception as e:
            st.error(f"Error reading history: {str(e)}")
    else:
        st.warning("No history available.")


