import streamlit as st 
import Libs as glib 
import json

st.set_page_config(page_title="Home")

st.markdown("Create 1 Data-Driven Test Function with Katalon") 
st.markdown("Create 1 test case login page with Katalon") 
st.markdown("Create 1 API Test Function with Katalon") 
st.markdown("Create a selenium test functions for a for list users") 

input_text = st.text_area("Input your question") 
go_button = st.button("Go", type="primary")

if input_text and go_button: 
    response = glib.call_stream(input_text)
    st.write_stream(response)

    



    
   