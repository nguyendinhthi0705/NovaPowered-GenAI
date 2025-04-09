# app.py
import streamlit as st
from NovaPoweredApp import NovaPoweredApp

def main():
    st.set_page_config(page_title="Nova Powered App")
    app = NovaPoweredApp()
    app.run()

if __name__ == "__main__":
    main()
