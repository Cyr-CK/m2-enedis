import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    data = pd.read_csv('data_/neufs.csv')  # Make sure this path is correct
    return data

st.title('DPE en Bretagne')

data = load_data()  # Load the data

# Debugging: Check if data is loaded
if st.checkbox('show data: '):
    st.write("Data loaded successfully!")
    st.write(data.shape)  # Show shape of the DataFrame
    st.write(data.head())  # Preview the first few rows

