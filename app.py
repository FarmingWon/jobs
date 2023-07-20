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

# data analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import matplotlib as mpl
import math

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

# func: calculate score of company
def make_score(company_name,address,busisize): # 점수 계산
    set_csv()
    center_xy = list(addr_to_lat_lon(address))

    df_subway_distance = calculate_distance(st.session_state.df_subway, center_xy)
    df_bus_distance = calculate_distance(st.session_state.df_bus, center_xy)
    df_hospital_distance = calculate_distance(st.session_state.df_hospital, center_xy)
    df_museum_distance = calculate_distance(st.session_state.df_museum, center_xy)
    df_starbucks_distance = calculate_distance(st.session_state.df_starbucks, center_xy)
    df_exercise_distance = calculate_distance(st.session_state.df_exercise, center_xy)
    df_oliveyoung_distance = calculate_distance(st.session_state.df_oliveyoung, center_xy)

    # df_oliveyoung_distance = df_oliveyoung_distance.astype({'latlon' : 'object'})
    # df_subway_distance = df_subway_distance.astype({'latlon' : 'object'})
    # df_bus_distance = df_bus_distance.astype({'latlon' : 'object'})
    # df_hospital_distance = df_hospital_distance.astype({'latlon' : 'object'})
    # df_museum_distance = df_museum_distance.astype({'latlon' : 'object'})
    # df_starbucks_distance = df_starbucks_distance.astype({'latlon' : 'object'})
    # df_exercise_distance = df_exercise_distance.astype({'latlon' : 'object'})


    df_graph = pd.DataFrame({'distance': ['500m', '1km', '3km']})

    df_graph['subway'] = [len(df_subway_distance.loc[df_subway_distance['distance'] <= 0.5]),
                        len(df_subway_distance.loc[(df_subway_distance['distance'] > 0.5) & (df_subway_distance['distance'] <= 1.0)]),
                        len(df_subway_distance.loc[(df_subway_distance['distance'] > 1.0) & (df_subway_distance['distance'] <= 3.0)])]

    df_graph['bus'] = [len(df_bus_distance.loc[df_bus_distance['distance'] <= 0.5]),
                        len(df_bus_distance.loc[(df_bus_distance['distance'] > 0.5) & (df_bus_distance['distance'] <= 1.0)]),
                        len(df_bus_distance.loc[(df_bus_distance['distance'] > 1.0) & (df_bus_distance['distance'] <= 3.0)])]

    df_graph['hospital'] = [len(df_hospital_distance.loc[df_hospital_distance['distance'] <= 0.5]),
                        len(df_hospital_distance.loc[(df_hospital_distance['distance'] > 0.5) & (df_hospital_distance['distance'] <= 1.0)]),
                        len(df_hospital_distance.loc[(df_hospital_distance['distance'] > 1.0) & (df_hospital_distance['distance'] <= 3.0)])]

    df_graph['museum'] = [len(df_museum_distance.loc[df_museum_distance['distance'] <= 0.5]),
                        len(df_museum_distance.loc[(df_museum_distance['distance'] > 0.5) & (df_museum_distance['distance'] <= 1.0)]),
                        len(df_museum_distance.loc[(df_museum_distance['distance'] > 1.0) & (df_museum_distance['distance'] <= 3.0)])]
    
    df_graph['starbucks'] = [len(df_starbucks_distance.loc[df_starbucks_distance['distance'] <= 0.5]),
                        len(df_starbucks_distance.loc[(df_starbucks_distance['distance'] > 0.5) & (df_starbucks_distance['distance'] <= 1.0)]),
                        len(df_starbucks_distance.loc[(df_starbucks_distance['distance'] > 1.0) & (df_starbucks_distance['distance'] <= 3.0)])]
    
    df_graph['exercise'] = [len(df_exercise_distance.loc[df_exercise_distance['distance'] <= 0.5]),
                        len(df_exercise_distance.loc[(df_exercise_distance['distance'] > 0.5) & (df_exercise_distance['distance'] <= 1.0)]),
                        len(df_exercise_distance.loc[(df_exercise_distance['distance'] > 1.0) & (df_exercise_distance['distance'] <= 3.0)])]

    df_graph['oliveyoung'] = [len(df_oliveyoung_distance.loc[df_oliveyoung_distance['distance'] <= 0.5]),
                        len(df_oliveyoung_distance.loc[(df_oliveyoung_distance['distance'] > 0.5) & (df_oliveyoung_distance['distance'] <= 1.0)]),
                        len(df_oliveyoung_distance.loc[(df_oliveyoung_distance['distance'] > 1.0) & (df_oliveyoung_distance['distance'] <= 3.0)])]
    col_name = ['subway','bus','hospital','museum','starbucks','exercise','oliveyoung']
    score = 0
    for i in range(3):
        for name in col_name:
            score = score + df_graph.loc[i][name]
    if busisize == '강소기업':
        score = int(score*1.2)
    st.session_state.score = score
    

      
# Router: Router initialize
def initRouter():
  return stx.Router({'/': recom, '/map': map, '/view': view})

# EventListener: Button(Show More)
def on_more_click(show_more, idx):
    show_more[idx] = True
    st.session_state.show_more = show_more

def on_less_click(show_more, idx):
    show_more[idx] = False
    st.session_state.show_more = show_more


            
# Router: view information of companies - /view
def view():
    if st.session_state.clicked_regionCd != None and st.session_state.clicked_regionNm != None and st.session_state.clicked_jobCd != None and st.session_state.clicked_jobNm != None:
        st.session_state.gangso, st.session_state.recommend_company = corp.find_company(st.session_state.clicked_regionCd, st.session_state.clicked_jobCd, "mongodb+srv://wonseok:E3kXD7Tta02OWXYT@cluster0.0nbzrz6.mongodb.net/?retryWrites=true&w=majority")
        fields = ['기업명','기업규모','근로계약','기업위치','근무시간' ,'URL']
        st.subheader('기업목록')
        if len(st.session_state.gangso) != 0:
            gangso_df = pd.DataFrame(st.session_state.gangso, columns=fields)
        if len(st.session_state.recommend_company) != 0:
            company_df = pd.DataFrame(st.session_state.recommend_company, columns=fields)
        if len(st.session_state.gangso) == 0 and len(st.session_state.recommend_company) == 0:
            st.write("회사 없음.")
        else:
            if len(st.session_state.gangso) != 0 and len(st.session_state.recommend_company) != 0:
                st.session_state.companys = pd.merge(gangso_df, company_df, how='outer')
            elif len(st.session_state.gangso) == 0:
                st.session_state.companys = company_df
            else:
                st.session_state.companys = gangso_df

            if 'show_more' not in st.session_state or st.session_state.show_more == None or len(st.session_state.show_more) != len(st.session_state.companys):
                st.session_state.show_more = dict.fromkeys([i for i in range(len(st.session_state.companys))], False)
            show_more = st.session_state.show_more
            
            cols = st.columns(2)
            rows = ['기업명', '더보기']

            # table header
            for col, field in zip(cols, rows):
                col.write("**"+field+"**")

            # table rows
            for idx, row in st.session_state.companys.iterrows():
                col1, col2 = st.columns(2)
                col1.write(row['기업명'])
                placeholder = col2.empty()
                if show_more[int(idx)]:
                    placeholder.button(
                        "less", key=str(idx) + "_", on_click=on_less_click, args=[show_more, idx]
                    )
                    make_score(row['기업명'], row['기업위치'], row['기업규모'])
                    
                    st.write('기업규모 : ' + row['기업규모'])
                    st.write('근로계약 : ' + row['근로계약'])
                    st.write('근무시간 : ' + row['근무시간'])
                    url = row['URL']
                    st.write("공고 URL : [%s](%s)" % (url, url))
                    st.write("인프라 점수 : " + str(st.session_state.score))
                    subcol1, subcol2 = st.columns(2)
                    subcol1.write('기업위치 : ' + row['기업위치'])
                    with subcol2:
                        if st.button('기업 주변 인프라 확인'):
                            st.session_state.company = row
                            router.route('/map')
                    st.write("---")
                else:
                    placeholder.button(
                        "more",
                        key=idx,
                        on_click=on_more_click,
                        args=[show_more, idx],
                        type="primary",
                    )

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
