import streamlit as st
import extra_streamlit_components as stx
from st_pages import Page, add_page_title, show_pages

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

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

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

def set_csv():
    st.session_state.df_subway = pd.read_csv('./csv/subway.csv')
    st.session_state.df_bus = pd.read_csv('./csv/bus.csv')
    st.session_state.df_hospital = pd.read_csv('./csv/hospital.csv')
    st.session_state.df_museum = pd.read_csv('./csv/museum.csv')
    st.session_state.df_starbucks = pd.read_csv('./csv/starbucks_busan.csv')
    st.session_state.df_exercise = pd.read_csv('./csv/exercise.csv')
    st.session_state.df_oliveyoung = pd.read_csv('./csv/oliveyoung.csv')

# EventListener: Button(Show More)
def on_more_click(show_more, idx):
    show_more[idx] = True
    st.session_state.show_more = show_more

def on_less_click(show_more, idx):
    show_more[idx] = False
    st.session_state.show_more = show_more

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
    
st.title('👜직장 선택')
with st.sidebar:
    htmlSide=f"""
        <br/>
        <p>1</p>
        <p>2</p>
        <p>3</p>
        <p>4</p>
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

if 'clicked_regionCd' not in st.session_state:
    st.error('직업 추천을 먼저 진행해주세요')
elif st.session_state.clicked_regionCd != None and st.session_state.clicked_regionNm != None and st.session_state.clicked_jobCd != None and st.session_state.clicked_jobNm != None:
  bar = st.progress(50, text="진행률")
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
                      bar.progress(75, text="진행률")
                      st.success('왼쪽 메뉴에서 직장 주변 인프라 확인을 눌러주세요!')
                      #router.route('/map')
              st.write("---")
          else:
                placeholder.button(
                  "more",
                  key=idx,
                  on_click=on_more_click,
                  args=[show_more, idx],
                  type="primary",
                )
