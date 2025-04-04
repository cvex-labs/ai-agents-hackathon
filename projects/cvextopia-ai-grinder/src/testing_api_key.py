import streamlit as st
from config_loader import load_config

config = load_config()
st.write(f"Loaded API Key: {config['cvex_api_key']}")

