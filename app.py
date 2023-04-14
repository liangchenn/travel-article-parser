import streamlit as st
from streamlit_option_menu import option_menu

from pages import batch_update_page
from pages import preview_page

# app setups
st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="expanded",  # collapsed",  # Can be "auto", "expanded", "collapsed"
    page_title="Klook 文章分析器",  # String or None.
    page_icon="./asset/klook.png",  # String, anything supported by st.image, or None.
)


st.header("Klook Article Parser")


with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Previewer", "Batch Update"],
        icons=["card-text", "cloud-upload-fill"],
        menu_icon="cast",
        default_index=1,
    )


if selected == "Previewer":
    preview_page()

elif selected == "Batch Update":
    batch_update_page()
