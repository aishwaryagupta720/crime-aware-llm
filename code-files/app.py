import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title("California Violent Crime Rate (2000-2013)")

# Load Dataset
@st.cache_data
def load_data():
    file_path = r'C:\Users\ankit\Downloads\crime_ca_2000-2013.xlsx'
    data = pd.read_excel(file_path)
    return data

data = load_data()

# Display the data
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(data)

# Verify column names
st.write(data.columns)

# Filter by Year
st.subheader("Filter Data by Year")
if 'reportyear' in data.columns:
    years = st.slider("Select Year Range", min_value=2000, max_value=2013, value=(2000, 2013))
    filtered_data = data[(data['reportyear'] >= years[0]) & (data['reportyear'] <= years[1])]
    st.write(filtered_data)

    # Line Chart
    st.subheader("Violent Crime Rate Over Time")
    fig, ax = plt.subplots()
    sns.lineplot(data=filtered_data, x='reportyear', y='rate', ax=ax)
    st.pyplot(fig)

    # Bar Chart
    st.subheader("Violent Crime Rate by Year")
    fig, ax = plt.subplots()
    sns.barplot(data=filtered_data, x='reportyear', y='rate', ax=ax)
    st.pyplot(fig)
else:
    st.error("The 'reportyear' column is not in the dataset.")
