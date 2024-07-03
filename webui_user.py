import streamlit as st
from webui_pages.utils import *
from streamlit_option_menu import option_menu
from webui_pages.dialogue.dialogue import dialogue_page, chat_box
from webui_pages.main.main import main_page
import os
import sys
from configs import VERSION
from server.utils import api_address

api = ApiRequest(base_url=api_address())

if __name__ == "__main__":
    is_lite = "lite" in sys.argv

    st.set_page_config(
        "Langchain-Chatchat WebUI",
        os.path.join("img","logo.png"),
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/chatchat-space/Langchain-Chatchat',
            'Report a bug': "https://github.com/chatchat-space/Langchain-Chatchat/issues",
            'About': f"""欢迎使用 Yan-Chai WebUI {VERSION}！"""
        }
    )

    pages = {
        "首页": {
            "icon": "main",
            "func": main_page,
        },
        "对话": {
            "icon": "dialogue",
            "func": dialogue_page,
        },
    }

    page_container = st.container()
    with st.sidebar:
        st.image(
            os.path.join("img", "logo.png"),
            use_column_width=True
        )
        st.caption(
            f"""<p align="right">当前版本：{VERSION}</p>""",
            unsafe_allow_html=True,
        )
        options = list(pages)
        icons = [x["icon"] for x in pages.values()]

        default_index = 0
        selected_page = option_menu(
            "",
            options=options,
            icons=icons,
            # menu_icon="chat-quote",
            default_index=default_index,
        )

    if selected_page in pages:
        if selected_page == '首页':
            pages[selected_page]["func"](container=page_container)
        elif selected_page == '对话':
            pages[selected_page]["func"](api=api, is_lite=is_lite, initial_message="")
