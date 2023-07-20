# -- import modules start --
#streamlit
import streamlit as st
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages

# -- import modules end --

# func: setting variable & files
def set_variable():
    st.session_state.selected_region = None
    st.session_state.selected_job = None
    st.session_state.recommend_jobs = None
    st.session_state.similarity_jobs = None
    st.session_state.jobs = None
    st.session_state.score = None

def main():
    show_pages([
        Page("./pages/recom.py", "이력서를 통한 직업 추천"),
        Page("./pages/view.py", "직장 선택"),
        Page("./pages/map.py", "직장 인프라 확인")
    ])

if __name__ == "__main__":
    set_variable()
    main()
