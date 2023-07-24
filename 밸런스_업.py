# -- import modules start --
#streamlit
import streamlit as st
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages

import sys
import base64
from pathlib import Path
import pandas as pd
import folium
from streamlit_echarts import st_echarts
from streamlit_folium import st_folium
import math

# -- import modules end --

# func: setting variable & files
def set_variable():
    st.session_state.selected_region = None
    st.session_state.selected_job = None
    st.session_state.recommend_jobs = None
    st.session_state.similarity_jobs = None
    st.session_state.jobs = None
    st.session_state.pageName = None
    st.session_state.query = None
    st.session_state.infra = None
    if 'score' not in st.session_state:  
      st.session_state.score = None
    if 'selectJob' not in st.session_state:  
      st.session_state.selectJob = False
    if 'selectRegion' not in st.session_state:  
      st.session_state.selectRegion = False
    if 'selectCompany' not in st.session_state:  
      st.session_state.selectCompany = False
    if 'selectWLB' not in st.session_state:  
      st.session_state.selectWLB = False
    if 'barScore' not in st.session_state:
      st.session_state.barScore = False


def set_csv():
  st.session_state.df_subway = pd.read_csv('csv/subway.csv')
  st.session_state.df_bus = pd.read_csv('csv/bus.csv')
  st.session_state.df_hospital = pd.read_csv('csv/hospital.csv')
  st.session_state.df_museum = pd.read_csv('csv/museum.csv')
  st.session_state.df_starbucks = pd.read_csv('csv/starbucks_busan.csv')
  st.session_state.df_exercise = pd.read_csv('csv/exercise.csv')
  st.session_state.df_oliveyoung = pd.read_csv('csv/oliveyoung.csv')

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

# func: 지도 생성
def makeMap(center_xy,corpNm):
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
          {"value": int(df_graph.iloc[1]['museum']), "name": "복합문화공간"},
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
    options=options, height=725
  )
  
  makeMarker(m, df_subway_distance, 'orange', 'train', "대중교통")
  makeMarker(m, df_bus_distance, 'orange', 'bus', "대중교통")
  makeMarker(m, df_hospital_distance, 'red', 'plus', "병원")
  makeMarker(m, df_museum_distance, 'pink', 'institution', "박물관")
  makeMarker(m, df_starbucks_distance, 'green', 'coffee', "스타벅스")
  makeMarker(m, df_exercise_distance, 'black', 'soccer-ball-o', "운동시설")
  makeMarker(m, df_oliveyoung_distance, 'green', 'meteor', "올리브영")
  return m

# func: make Marker in map
def makeMarker(m, df, color, icon, nm):
  for idx, row in df.iterrows():
    loc = row['latlon'][1:-1].split(', ')
    folium.Marker(loc,
                  popup=folium.Popup(row['name'], max_width=300),
                  tooltip= '('+nm+') '+row['name'],
                  icon=(folium.Icon(color=color, icon=icon, prefix='fa'))
                 ).add_to(m)

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def main():
    #side
    with st.sidebar:
        htmlSide=f"""
        <br/>
        <a href="#what-is-balanceup-balanceup" style="text-align:left; text-decoration:center; color:inherit;"><p>✔ What is BalanceUP?</p></a>
        <a href="#how-to-use-balancup" style="text-align:left; text-decoration:center; color:inherit;"><p>🔔 How To Use</p></a>
        <a href="#why-balanceup-balanceup" style="text-align:left; text-decoration:center; color:inherit;"><p>❓ Why BalanceUP?</p></a>
        <a href="#feature-balanceup" style="text-align:left; text-decoration:center; color:inherit;"><p>📝Feature</p></a>
        """
        st.markdown(htmlSide, unsafe_allow_html=True)
        st.sidebar.markdown("---")
        htmlSide2=f"""
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/openai_logo-removebg.png")}" style="width:180px; height:60px;">
            </h5>
        </div>
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/mongodb logo.png")}" style="width:180px; height:60px;">
            </h5>
        </div>
        <div id="logo">
            <h5>
                <span>Powered By  &nbsp; &nbsp; &nbsp;</span>
                <img src="data:image/png;base64,{img_to_bytes("./img/Neo4j-logo_color.png")}" style="width:180px; height:60px;">
            </h5>
        </div>
        """
        st.markdown(htmlSide2, unsafe_allow_html=True)

    #main
    html = f"""
    <!-- Font Awesome -->
    <link
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    rel="stylesheet"/>
    <!-- Google Fonts -->
    <link
    href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
    rel="stylesheet"/>
    <!-- MDB -->
    <link
    href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.0/mdb.min.css"
    rel="stylesheet"/>
    <!-- MDB -->
    <script
    type="text/javascript"
    src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/6.4.0/mdb.min.js"></script>
    <div class="title">
        <div class="row d-flex justify-content-center align-items-center">
            <div class="col-sm-2">
                <img src="data:image/png;base64,{img_to_bytes("./img/balanceup logo.png")}" style="width:100px; height:100px;">
            </div>
            <div class="col-sm-8 align-items-center">
                <h4>밸런스 업</h4>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="subtitle" id="subtitle">
            <p class="h5">이력서만 등록해도 맞춤 포지션 추천과 기업 평가까지!!</p>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

    con1,con2= st.columns([0.5,0.5])
    center_xy = (35.175420857972, 129.12504608504) # 임의 데이터 
    corpNm = "(주)아람커뮤니케이션즈"
    with con1:
        m = makeMap(center_xy, corpNm)
        con1_html = """ 
        <h3 style="text-align:center">생활 편의시설 통계</h3>
        """
        st.markdown(con1_html, unsafe_allow_html=True)
    with con2:
        st_folium(m, width=700, returned_objects=[])
        con2_html = """ 
        <h3 style="text-align:center">기업 주변 인프라</h3>
        """
        st.markdown(con2_html, unsafe_allow_html=True)
    html2 = """
   <hr/>
   <br/>
   <!-- <div class="card" name="whyis"> -->
   <!--     <div class="card-header" id="whyis">-->
            <h5>
                <i class="fas fa-question-circle fa-sm me-2 opacity-70" style="color:skyblue"></i>
                Why
                <span style="color:#DC2D1C">BalanceUP</span>:
                <span>&nbsp; BalanceUP이 만들어진 이유!
            </h5>
     <!--   </div> -->
        <div class="card-body">
            사x인, 잡xx아, 잡xx닛 등과 같은 기존 사이트들의 공통점은 무엇일까요?<br>
            현 구직 세대인 MZ세대의 요구조건인 삶과 일의 균형에 대한 요구조건을 만족시켜주지 못한다는 것입니다.<br>
            우리 사이트는 타사 서비스보다 빠르게 거대언어모델(LLM)의 도입에 성공하였으며, 청년세대의 니즈를 만족시켜주기 위하여 만들어졌습니다.
        </div>
    <!-- </div> -->
    <hr/>
    <br/>
   <!-- <div class="card" name="feature">-->
    <!--    <div class="card-header" id="feature">-->
            <h5>
                <i class="fas fa-question-circle fa-sm me-2 opacity-70" style="color:skyblue"></i>
                Feature: 
                <span style="color:#DC2D1C">&nbsp; BalanceUP</span>만의 특징!
            </h5>
    <!--    </div>-->
        <div class="card-body">
          <ul>
            <li>분기별 모델 업데이트로 빠르게 변화하는 노동시장 대응</li>
            <li>MZ세대의 요구조건을 만족하는 기업 생활 환경 지수 차트 </li>
            <li>최근 관심이 증대한 인공지능 거대언어모델을 적용</li>
          </ul>
        </div>
    <!--</div>-->
    </div>
    """
    st.markdown(html2, unsafe_allow_html=True)
    
    

if __name__ == "__main__":
    set_variable()
    set_csv()
    st.set_page_config(page_title="BalanceUp", layout="wide")
    main()
