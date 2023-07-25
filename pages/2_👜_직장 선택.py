import streamlit as st
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages
from streamlit_extras.switch_page_button import switch_page

# data analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import matplotlib as mpl
import math

import json
import requests

import sys
import base64
from pathlib import Path

from recommend import company as corp
from recommend import jaccard

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def get_progress_score():
    st.session_state.barScore = 0
    if st.session_state.selectJob or st.session_state.selectRegion:
        st.session_state.barScore = 25
        if st.session_state.selectJob and st.session_state.selectRegion:
            st.session_state.barScore = 50
            if st.session_state.selectCompany:
                st.session_state.barScore = 75
                if st.session_state.selectWLB:
                    st.session_state.barScore = 100

def set_csv():
  st.session_state.df_subway = pd.read_csv('csv/subway.csv')
  st.session_state.df_bus = pd.read_csv('csv/bus.csv')
  st.session_state.df_hospital = pd.read_csv('csv/hospital.csv')
  st.session_state.df_museum = pd.read_csv('csv/museum.csv')
  st.session_state.df_starbucks = pd.read_csv('csv/starbucks_busan.csv')
  st.session_state.df_exercise = pd.read_csv('csv/exercise.csv')
  st.session_state.df_oliveyoung = pd.read_csv('csv/oliveyoung.csv')

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

def eval_infra(score_list):
    eval_list = list()
    if (score_list[0] + score_list[1]) == 0 : #대중교통
        eval_list.append("없음")
    elif (score_list[0] + score_list[1]) > 200:
        eval_list.append("혼잡")
    else :
        eval_list.append("보통")

    if score_list[2] == 0: #병원
        eval_list.append("없음")
    elif score_list[2] >= 1 and score_list[2] <= 2:
        eval_list.append("보통")
    else:
        eval_list.append("여유")
    
    if score_list[3] == 0: #문화시설
        eval_list.append("없음")
    elif score_list[3] >= 1 and score_list[3] <= 2:
        eval_list.append("보통")
    else:
        eval_list.append("여유")
    
    if score_list[4] == 0: #스벽
        eval_list.append("없음")
    elif score_list[4] >= 1 and score_list[4] <= 2:
        eval_list.append("보통")
    else:
        eval_list.append("여유")
    
    if score_list[5] == 0: #운동
        eval_list.append("없음")
    elif score_list[5] >= 100 :
        eval_list.append("여유")
    else :
        eval_list.append("보통")
    
    if score_list[6] == 0: #올영
        eval_list.append("없음")
    elif score_list[6] >= 1 and score_list[6] <= 2:
        eval_list.append("보통")
    else:
        eval_list.append("여유")
    return eval_list

# EventListener: Button(Show More)
def on_more_click(show_more, idx):
    show_more[idx] = True
    st.session_state.show_more = show_more

def on_less_click(show_more, idx):
    show_more[idx] = False
    st.session_state.show_more = show_more

# func: calculate score of company
def make_score(company_name,address,busisize,isShow=False): # 점수 계산
    set_csv()
    center_xy = list(addr_to_lat_lon(address))

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
    col_name = ['subway','bus','hospital','museum','starbucks','exercise','oliveyoung']
    score_list = list()
    score = 0
    for name in col_name:
        tp_score = 0
        for i in range(3):
            tp_score = tp_score + df_graph.loc[i][name]
        score_list.append(tp_score)
        if tp_score >= 100:
            if tp_score >= 1000:
                tp_score = tp_score * 0.02
            else :
                tp_score = tp_score * 0.2
        
        score = score + tp_score
        
    if busisize == '강소기업':
        score = int(score*1.2)
    st.session_state.score = int(score)
    
    eval_list = eval_infra(score_list)
    query = f"""
    현재 회사 근처에 대중교통 {eval_list[0]}, 병원 {eval_list[1]}, 박물관 {eval_list[2]}, 커피숍 {eval_list[3]}, 운동시설 {eval_list[4]}, 화장품샵 {eval_list[5]} 인데 회사 주변의 인프라를 평가해줘.
    """
    
    if busisize == '강소기업':
        score = int(score*1.2)
    st.session_state.score = int(score)

    st.session_state.query = query
    if isShow:
        st.session_state.query = query
        st.session_state.infra = jaccard.getInfra_to_GPT(st.session_state.query,st.secrets.KEY.INFRA_GPT_KEY)
        st.session_state.eval_list = eval_list
    return int(score)

def all_score():
    li = list()
    for idx,row in st.session_state.companys.iterrows():
        score = make_score(row['기업명'], row['기업위치'], row['기업규모'])
        li.append(score)
    df = pd.DataFrame(li, columns=['score'])
    st.session_state.companys['score'] = li
    st.session_state.companys['score'].sort_values(ascending=False) # 내림차순



htmlTitle = """
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
    
    <div class="container header" style="font-weight:600;"><p class="h3">👜기업의 직업/지역 선택</p></div>
    <div class="container">
        <ol class="c-stepper">
            <li class="c-stepper-item completed" id="c-item1">
                <p class="c-stepper-title">이력서 파일 입력</p>
            </li>
            <li class="c-stepper-item completed" id="c-item2">
                <p class="c-stepper-title">개인 맞춤 직무 추천</p>
            </li>
            <li class="c-stepper-item completed" id="c-item3">
                <p class="c-stepper-title">기업의 직업/지역 선택</p>
            </li>
            <li class="c-stepper-item" id="c-item4">
                <p class="c-stepper-title">기업 인프라 평가 + ELEI 차트</p>
            </li>
        </ol>
    </div>
    <style type="text/css">
        @font-face {
            font-family: 'Pretendard-Regular';
            src: url('https://cdn.jsdelivr.net/gh/Project-Noonnu/noonfonts_2107@1.1/Pretendard-Regular.woff') format('woff');
            font-weight: 400;
            font-style: normal;
        }
        .container {
            font-family: 'Pretendard-Regular';
        }

        .c-stepper {
            display: flex;
            flex-wrap: wrap;
            margin: 0;
            padding: 0;
        }

        .c-stepper-title {
            margin-top:5px;
            font-size: small;
        }
        
        .c-stepper-item {
            flex: 1;
            display: flex;
            flex-direction: column;
            text-align: center;
        }
        
        .c-stepper-item:before {
            --size: 3rem;
            content: '';
            position: relative;
            z-index: 1;
            display: block;
            width: var(--size);
            height: var(--size);
            border-radius: 50%;
            border: 0.5px solid #0E3E89;
            margin: 0 auto;
            background-color: #ffffff;
        }
        .c-stepper-item:not(:last-child):after {
            content: '';
            position: relative;
            top: 1.5rem;
            left: 50%;
            height: 1.5px;
            background-color: #D1D1D1;
            order: -1;
        }
        .c-stepper-item.completed:before {
            --size: 3rem;
            content: '';
            position: relative;
            z-index: 1;
            display: block;
            width: var(--size);
            height: var(--size);
            border-radius: 50%;
            border: 0.5px solid #0E3E89;
            margin: 0 auto;
            background-color: #0E3E89
        }
    </style>
    """
st.markdown(htmlTitle, unsafe_allow_html=True)
with st.sidebar:
    htmlSide=f"""
        <br/>
        <ul>
        <li>현재 채용중인 기업정보에 대하여 확인이 가능해요.</li>
        <li>버튼을 누른 뒤, 마음에 드는 회사를 선택해봐요.</li>
        <li>인프라 확인 버튼을 누르면 인프라를 확인할수 있어요!</li>
        </ul>
    """
    st.markdown(htmlSide, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    bar = st.progress(st.session_state.barScore, text= f"진행률 {st.session_state.barScore}%")
    
if 'clicked_regionCd' not in st.session_state:
    st.error('직업 추천을 먼저 진행해주세요')
    if st.button("< Prev"):
        switch_page("이력서를_통한_직업_추천")
elif st.session_state.clicked_regionCd != None and st.session_state.clicked_regionNm != None and st.session_state.clicked_jobCd != None and st.session_state.clicked_jobNm != None:
    st.session_state.gangso, st.session_state.recommend_company = corp.find_company(st.session_state.clicked_regionCd, st.session_state.clicked_jobCd, st.secrets.KEY.MONGO_KEY)
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
                
        cols = st.columns(3)
        rows = ['기업명', '더보기', '라이프 밸런스 점수']
    
        # table header
        for col, field in zip(cols, rows):
            col.write("**"+field+"**")
        all_score()
        # table rows
        for idx, row in st.session_state.companys.iterrows():
          col1, col2,col3 = st.columns(3)
          col1.write(row['기업명'])
          placeholder = col2.empty()
          if show_more[int(idx)]:
              placeholder.button(
                  "less", key=str(idx) + "_", on_click=on_less_click, args=[show_more, idx]
              )
              make_score(row['기업명'], row['기업위치'], row['기업규모'], isShow= True)
                    
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
                      st.session_state.selectCompany = True
                      get_progress_score()
                      bar.progress(st.session_state.barScore, text= f"진행률 {st.session_state.barScore}%")
                      st.session_state.company = row
                      switch_page("직장_라이프_밸런스_확인")
                  
              st.write("---")
          else:
                placeholder.button(
                  "more",
                  key=idx,
                  on_click=on_more_click,
                  args=[show_more, idx],
                  type="primary",
                )
          col3.write(f"{row['score']}점")
