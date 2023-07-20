# -- import modules start --
import streamlit as st
import extra_streamlit_components as stx
from streamlit_folium import st_folium
from streamlit_echarts import st_echarts

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
    st.session_state.company = None

def set_csv():
    st.session_state.df_subway = pd.read_csv('./csv/subway.csv')
    st.session_state.df_bus = pd.read_csv('./csv/bus.csv')
    st.session_state.df_hospital = pd.read_csv('./csv/hospital.csv')
    st.session_state.df_museum = pd.read_csv('./csv/museum.csv')
    st.session_state.df_starbucks = pd.read_csv('./csv/starbucks_busan.csv')
    st.session_state.df_exercise = pd.read_csv('./csv/exercise.csv')
    st.session_state.df_oliveyoung = pd.read_csv('./csv/oliveyoung.csv')

# func: UI for Select Region
def showRegion(regions):
    regionsNm = [reg[1] for reg in regions]
    st.session_state.selected_region = st.radio(label = '', options= regionsNm)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# func: UI for Select Job
def showJob(recommend_jobs, similarity_jobs):
    st.session_state.jobs = [[recommend_jobs[0]['occupation3'], recommend_jobs[0]['occupation3Nm']]]
    tmp2 = [[job[0]['occupation3'],job[0]['occupation3Nm']] for job in similarity_jobs]
    st.session_state.jobs.extend(tmp2)
    jobsNm = [job[1] for job in st.session_state.jobs]
    st.session_state.selected_job= st.radio(label='',options=jobsNm)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
 
# func: save pdf file
def save_upload_file(dir, file):
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(os.path.join(dir, file.name), 'wb') as f:
        f.write(file.getbuffer())

# func: address to lat, lon
def addr_to_lat_lon(addr):
  url = f"https://dapi.kakao.com/v2/local/search/address.json?query={addr}"
  headers = {"Authorization": "KakaoAK " + st.secrets.KEY.KAKAO_KEY}
  result = json.loads(str(requests.get(url, headers=headers).text))
  match_first = result['documents'][0]['address']
  return float(match_first['y']), float(match_first['x'])

# func: calculator distance
def calculate_distance(df, center_xy):
  df_distance = pd.DataFrame()
  distance_list = []
  for i in df['latlon']:
    if i != None or i != '':
      if type(i) == str:
        i = i[1:-1].split(', ')
        y = abs(float(center_xy[0]) - float(i[0])) * 111
        x = (math.cos(float(center_xy[0])) * 6400 * 2 * 3.14 / 360) * abs(float(center_xy[1]) - float(i[1]))
        distance = math.sqrt(x*x + y*y)
        if distance <= 3.0:
          df_distance = pd.concat([df_distance, df[df['latlon'] == ('(' + i[0] + ', ' + i[1] + ')')]])
          distance_list.append(distance)

  df_distance = df_distance.drop_duplicates()
  df_distance['distance'] = distance_list

  return df_distance # 만들어진 데이터프레임 리턴

# func: calculate score of company
def make_score(company_name,address,busisize): # 점수 계산
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
    
# func: 지도 생성
def makeMap(address,corpNm):
  center_xy = list(addr_to_lat_lon(address))
  m = folium.Map(location=center_xy, zoom_start=16)
  folium.Marker(center_xy, 
                popup=corpNm,
                tooltip=corpNm,
                icon=(folium.Icon(color='blue', icon='building', prefix='fa'))
                ).add_to(m)
  
  df_subway_distance = calculate_distance(st.session_state.df_subway, center_xy)
  df_bus_distance = calculate_distance(st.session_state.df_bus, center_xy)
  df_hospital_distance = calculate_distance(st.session_state.df_hospital, center_xy)
  df_museum_distance = calculate_distance(st.session_state.df_museum, center_xy)
  df_starbucks_distance = calculate_distance(st.session_state.df_starbucks, center_xy)
  df_exercise_distance = calculate_distance(st.session_state.df_exercise, center_xy)
  df_oliveyoung_distance = calculate_distance(st.session_state.df_oliveyoung, center_xy)

#   df_subway_distance = df_subway_distance.astype({'latlon' : 'object'})
#   df_bus_distance = df_bus_distance.astype({'latlon' : 'object'})
#   df_hospital_distance = df_hospital_distance.astype({'latlon' : 'object'})
#   df_museum_distance = df_museum_distance.astype({'latlon' : 'object'})
#   df_starbucks_distance = df_starbucks_distance.astype({'latlon' : 'object'})
#   df_exercise_distance = df_exercise_distance.astype({'latlon' : 'object'})
#   df_oliveyoung_distance = df_oliveyoung_distance.astype({'latlon' : 'object'})

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

  options = {
    "tooltip": {"trigger": "item"},
    "legend": {"top": "0%", "left": "center",},
    "series": [
      {
        "name": "500m",
        "type": "pie",
        "radius": ["20%", "40%"],
        "avoidLabelOverlap": False,
        "itemStyle": {
          "borderRadius": 10,
          "borderColor": "#fff",
          "borderWidth": 2,
        },
        "label": {"show": False, "position": "center"},
        "emphasis": {
          "label": {"show": True, "fontSize": "20", "fontWeight": "bold"}
        },
        "labelLine": {"show": False},
        "data": [
          {"value": int(df_graph.iloc[0]['subway']), "name": "지하철역"},
          {"value": int(df_graph.iloc[0]['bus']), "name": "버스정류장"},
          {"value": int(df_graph.iloc[0]['hospital']), "name": "병원"},
          {"value": int(df_graph.iloc[0]['museum']), "name": "박물관/미술관"},
          {"value": int(df_graph.iloc[0]['starbucks']), "name": "스타벅스"},
          {"value": int(df_graph.iloc[0]['exercise']), "name": "체육시설"},
          {"value": int(df_graph.iloc[0]['oliveyoung']), "name": "올리브영"},
        ],
      },
      {
        "name": "1km",
        "type": "pie",
        "radius": ["40%", "60%"],
        "avoidLabelOverlap": False,
        "itemStyle": {
          "borderRadius": 15,
          "borderColor": "#fff",
          "borderWidth": 2,
        },
        "label": {"show": False, "position": "center"},
        "emphasis": {
          "label": {"show": True, "fontSize": "20", "fontWeight": "bold"}
        },
        "labelLine": {"show": False},
        "data": [
          {"value": int(df_graph.iloc[1]['subway']), "name": "지하철역"},
          {"value": int(df_graph.iloc[1]['bus']), "name": "버스정류장"},
          {"value": int(df_graph.iloc[1]['hospital']), "name": "병원"},
          {"value": int(df_graph.iloc[1]['museum']), "name": "박물관/미술관"},
          {"value": int(df_graph.iloc[1]['starbucks']), "name": "스타벅스"},
          {"value": int(df_graph.iloc[1]['exercise']), "name": "체육시설"},
          {"value": int(df_graph.iloc[1]['oliveyoung']), "name": "올리브영"},
        ],
      },
      {
        "name": "3km",
        "type": "pie",
        "radius": ["60%", "80%"],
        "avoidLabelOverlap": False,
        "itemStyle": {
          "borderRadius": 20,
          "borderColor": "#fff",
          "borderWidth": 2,
        },
        "label": {"show": False, "position": "center"},
        "emphasis": {
          "label": {"show": True, "fontSize": "20", "fontWeight": "bold"}
        },
        "labelLine": {"show": False},
        "data": [
          {"value": int(df_graph.iloc[2]['subway']), "name": "지하철역"},
          {"value": int(df_graph.iloc[2]['bus']), "name": "버스정류장"},
          {"value": int(df_graph.iloc[2]['hospital']), "name": "병원"},
          {"value": int(df_graph.iloc[2]['museum']), "name": "박물관/미술관"},
          {"value": int(df_graph.iloc[2]['starbucks']), "name": "스타벅스"},
          {"value": int(df_graph.iloc[2]['exercise']), "name": "체육시설"},
          {"value": int(df_graph.iloc[2]['oliveyoung']), "name": "올리브영"},
        ],
      },
    ],
  }
  st_echarts(
    options=options, height=500
  )
  
  makeMarker(m, df_subway_distance, 'orange', 'train')
  makeMarker(m, df_bus_distance, 'orange', 'bus')
  makeMarker(m, df_hospital_distance, 'red', 'plus')
  makeMarker(m, df_museum_distance, 'pink', 'institution')
  makeMarker(m, df_starbucks_distance, 'green', 'coffee')
  makeMarker(m, df_exercise_distance, 'black', 'soccer-ball-o')
  makeMarker(m, df_oliveyoung_distance, 'green', 'meteor')
  return m

# func: make Marker in map
def makeMarker(m, df, color, icon):
  for idx, row in df.iterrows():
    loc = row['latlon'][1:-1].split(', ')
    folium.Marker(loc,
                  popup=folium.Popup(row['name'], max_width=300),
                  tooltip=row['name'],
                  icon=(folium.Icon(color=color, icon=icon, prefix='fa'))
                 ).add_to(m)
      
# Router: Router initialize
def initRouter():
  return stx.Router({'/': recom, '/map': map, '/view': view})

# EventListener: Button(Show More)
def on_more_click(show_more, idx):
    show_more[idx] = True

def on_less_click(show_more, idx):
    show_more[idx] = False
    st.session_state.show_more = show_more

# Router: Recommend - /
def recom():
    st.title("이력서 PDF파일을 통한 직업 추천")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    st.session_state.regions = r.getRegion()

    if uploaded_file:
        if st.session_state.recommend_jobs is None:
            save_upload_file('_pdf', uploaded_file)
            GPT_KEY = st.secrets.KEY.GPT_KEY
            st.session_state.recommend_jobs = jaccard.recommend_job(uploaded_file, GPT_KEY)
        if st.session_state.recommend_jobs :
            recommend_jobs = st.session_state.recommend_jobs
            if st.session_state.similarity_jobs is None:
                st.session_state.similarity_jobs = jaccard.recommend_similarity_job(recommend_jobs)
            st.write(f"추천 직업 : {recommend_jobs[0]['occupation3Nm']}")
        if st.session_state.selected_region is None:
            with st.expander(label="지역 선택", expanded=True):
                regions = st.session_state.regions
                showRegion(regions)
                if st.session_state.selected_region is not None:
                    print("get region")
        if st.session_state.selected_job is None:
            with st.expander(label = '직업 선택', expanded=True):
                if st.session_state.recommend_jobs is not None and st.session_state.similarity_jobs is not None:
                    recommend_jobs = st.session_state.recommend_jobs
                    similarity_jobs = st.session_state.similarity_jobs
                    showJob(st.session_state.recommend_jobs, st.session_state.similarity_jobs)
        regionBtn_clicked = st.button("선택")
        if regionBtn_clicked:
            st.session_state.clicked_regionCd = None
            st.session_state.clicked_regionNm = None
            st.session_state.clicked_jobCd = None
            st.session_state.clicked_jobNm = None
            for region in st.session_state.regions:
                if st.session_state.selected_region == region[1]:
                    st.session_state.clicked_regionCd = region[0]
                    st.session_state.clicked_regionNm = region[1]
                    break
            if st.session_state.jobs is not None:
                for job in st.session_state.jobs:
                    if st.session_state.selected_job == job[1]:
                        st.session_state.clicked_jobCd = job[0]
                        st.session_state.clicked_jobNm = job[1]
                        break
            router.route('/view')
# Router: view information of companies            
def view():
    if st.session_state.clicked_regionCd != None and st.session_state.clicked_regionNm != None and st.session_state.clicked_jobCd != None and st.session_state.clicked_jobNm != None:
        st.session_state.gangso, st.session_state.recommend_company = corp.find_company(st.session_state.clicked_regionCd, st.session_state.clicked_jobCd, "mongodb+srv://wonseok:E3kXD7Tta02OWXYT@cluster0.0nbzrz6.mongodb.net/?retryWrites=true&w=majority")
        fields = ['기업명','기업규모','근로계약','기업위치','근무시간' ,'URL']
        st.subheader('기업 기업목록')
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

            if not st.session_state.show_more or len(st.session_state.show_more) != len(st.session_state.companys):
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
                    for i in show_more:
                        if i != idx:
                            on_less_click(show_more, i)
                    
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

# Router: Map - /map
def map():
    set_csv()
    st.title('주변 인프라')
    company = st.session_state.company
    #row = companys.shape[0]
    #for i in range(row):
        #ad = companys.loc[i]['기업위치'].strip()
        #ad = ad.replace(',', " ")
        #ad = ad.strip()
        #ad = ad.split(" ")
        #addr = ""
        #for s in ad[1:6]:
            #addr = addr + " " + s
        #print(addr)
        #make_score(companys.loc[i]['기업명'], addr, companys.loc[i]['기업규모'])
    #sorted_data = sorted(st.session_state.score, key=lambda x: x[2], reverse=True)
    #address = sorted_data[0][1]
    address = company['기업위치']
    company_name = company['기업명']
    m = makeMap(address, company_name)
    st_folium(m, width=725, returned_objects=[])

def main():
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

if __name__ == "__main__":
    set_variable()
    router = initRouter()
    router.show_route_view()
    main()
