import streamlit as st 
import Libs as glib 
from PyPDF2 import PdfReader
import Libs as glib 

st.set_page_config(page_title="To create STAR Report")

input_text = st.text_area("Input your whole or apart of your essay") 
if input_text: 
    response = glib.create_STAR_Report(input_text) 
    st.write_stream(response)
    