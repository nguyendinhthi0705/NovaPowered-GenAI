import streamlit as st 
import Libs as glib 
import json

st.set_page_config(page_title="Home")

st.markdown("Create 1 Data-Driven Test Function with Katalon") 
st.markdown("Create 1 test case login page with Katalon") 
st.markdown("Create 1 API Test Function with Katalon") 
st.markdown("Create a selenium test functions for a for list users") 

image_bytes = ""
st.subheader("Select an Image") 
uploaded_file = st.file_uploader("Select an image", type=['png', 'jpeg'], label_visibility="collapsed")
input_text = st.text_area("Input your question") 

if uploaded_file:
    uploaded_image_preview = glib.get_bytesio_from_bytes(uploaded_file.getvalue())
    image_bytes = uploaded_file.getvalue()

    st.image(uploaded_image_preview)

    go_button = st.button("Go", type="primary")

    if input_text and go_button: 
        response = glib.call_stream(input_text, image_bytes)
        st.write_stream(response)

    



    
   