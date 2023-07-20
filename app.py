# -- import modules start --
import streamlit as st
import extra_streamlit_components as stx
from streamlit_folium import st_folium
from streamlit_echarts import st_echarts
from st_pages import Page, add_page_title, show_pages

import folium

# requests data
import json
import requests

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# customized modules
from recommend import jaccard
from recommend import region as r
from recommend import company as corp

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

    '''
    with st.sidebar:
        if st.button('이력서를 통한 직업 추천'):
          router.route('/')
        elif st.button('직장 선택'):
            if 'clicked_regionCd' not in st.session_state or st.session_state.clicked_regionCd == None:
                st.error('직업 추천을 먼저 해주세요')
            else:
                router.route('/view')
        elif st.button('인프라 확인'):
            if 'company' not in st.session_state or st.session_state.company == None:
                st.error('직장 선택을 먼저 해주세요')
            else:
                router.route('/map')
                '''

if __name__ == "__main__":
    set_variable()
    router = initRouter()
    router.show_route_view()
    main()
