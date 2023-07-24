def infra():
    import streamlit as st
    from streamlit_echarts import st_echarts
    from streamlit_folium import st_folium
    from st_pages import add_page_title
    
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
    
    import sys
    import base64
    from pathlib import Path
    
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
    # def set_csv():
    #   st.session_state.df_subway = pd.read_csv('./csv/subway.csv')
    #   st.session_state.df_bus = pd.read_csv('./csv/bus.csv')
    #   st.session_state.df_hospital = pd.read_csv('./csv/hospital.csv')
    #   st.session_state.df_museum = pd.read_csv('./csv/museum.csv')
    #   st.session_state.df_starbucks = pd.read_csv('./csv/starbucks_busan.csv')
    #   st.session_state.df_exercise = pd.read_csv('./csv/exercise.csv')
    #   st.session_state.df_oliveyoung = pd.read_csv('./csv/oliveyoung.csv')
    
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
        options=options, height=725
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
    
    st.title('🌏 직장 라이프 밸런스 확인')
    with st.sidebar:
        htmlSide=f"""
            <br/>
            <ul>
              <li>인프라에 대하여 확인 할 수 있어요!</li>
              <li>다른 직장이 궁금하면 직장 선택을 다시 하면 확인할 수 있어요.</li>
            </ul>
        """
        st.markdown(htmlSide, unsafe_allow_html=True)
        st.sidebar.markdown("---")
        bar = st.progress(st.session_state.barScore, text= f"진행률 {st.session_state.barScore}%")
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
    # set_csv()
    if 'company' in st.session_state:
        st.session_state.selectWLB = True
        get_progress_score()
        bar.progress(st.session_state.barScore, text= f"진행률 {st.session_state.barScore}%")
        company = st.session_state.company
        address = company['기업위치']
        company_name = company['기업명']
        html = f"""
        선택한 채용공고는 <strong>{company_name}</strong>의 채용공고시네요! 해당 회사에 대한 인프라를 알려드릴게요!
        """
        st.markdown(html, unsafe_allow_html=True)
        con1,con2= st.columns([0.5,0.5])
        with con1:
          m = makeMap(address, company_name)
          con1_html = """ 
            <h3 style="text-align:center">생활 편의시설 통계</h3>
            """
          st.markdown(con1_html, unsafe_allow_html=True)
        # html = """<br/>"""
        # st.markdown(html, unsafe_allow_html=True)
        with con2:
          st_folium(m, width=700, returned_objects=[])
          con2_html = """ 
            <h3 style="text-align:center">기업 주변 인프라</h3>
            """
          st.markdown(con2_html, unsafe_allow_html=True)
    else:
       st.error('직장 선택을 먼저 진행해주세요')
