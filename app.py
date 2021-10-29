import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

app = dash.Dash(__name__)
server = app.server
################################# 데이터 로드 #################################

time = pd.read_csv('data/Time.csv')
timeAge = pd.read_csv('data/TimeAge.csv')
timeGender = pd.read_csv('data/TimeGender.csv')
timeProvince = pd.read_csv('data/TimeProvince.csv')

Gender_Date = timeGender.pivot_table(index = ['date'],columns=['sex'], aggfunc=sum)
Gender_Confirmed = Gender_Date['confirmed']
Gender_Deceased = Gender_Date['deceased']

################################# 레이아웃 세팅 #################################

cnf, dth, rec, act = '#393e46', '#ff2e63', '#21bf73', '#fe9801' 
DEFAULT_PLOTLY_COLORS=['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                       'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                       'rgb(148, 103, 189)', 'rgb(140, 86, 75)',
                       'rgb(227, 119, 194)', 'rgb(127, 127, 127)',
                       'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

# 기본 세팅 설정(font 등)
layout_setting = {'font':dict(size=20, color='#60606e', family='Franklin Gothic' )}

################################# 시간에 따른 확진자 추이 fig 객체 생성 #################################

fig_time = go.Figure()
fig_time.add_trace(go.Scatter(x=time['date'],y=time['released'],  mode='lines+markers', name='released'))
fig_time.add_trace(go.Scatter(x=time['date'],y=time['confirmed'], mode='lines+markers', name='confirmed'))
fig_time.add_trace(go.Scatter(x=time['date'],y=time['deceased'],  mode='lines+markers', name='deceased'))
fig_time.update_layout(title='<b>시간에 따른 확진자 추이</b>', **layout_setting)


################################# 남녀 확진자&사망자 fig 객체 생성 #################################

# subplots 그리기
fig_gender = make_subplots(rows=1, cols=2, horizontal_spacing= 0.15, subplot_titles=('<b>남여 확진자 수</b>','<b>남여 사망자 수</b>'))

fig_gender.add_trace(go.Scatter(x=Gender_Confirmed.index, y=Gender_Confirmed['male'], mode='lines', name="Male", line=dict(color='#3370ff')), row=1, col=1)
fig_gender.add_trace(go.Scatter(x=Gender_Confirmed.index, y=Gender_Confirmed['female'], mode='lines', name="Female", line=dict(color='#ff0d5f')), row=1, col=1)
fig_gender.add_trace(go.Scatter(x=Gender_Deceased.index, y=Gender_Deceased['male'], mode='lines', name="Male", showlegend=False, line=dict(color='#3370ff')), row=1, col=2)
fig_gender.add_trace(go.Scatter(x=Gender_Deceased.index, y=Gender_Deceased['female'], mode='lines', name="Female", showlegend=False, line=dict(color='#ff0d5f')), row=1, col=2)

fig_gender.update_layout(title='<b>성별 확진자 및 사망자 수</b>', font = layout_setting['font'], showlegend=True)

fig_gender.update_xaxes(title_text="월", row=1, col=1)
fig_gender.update_xaxes(title_text="월", row=1, col=2)
fig_gender.update_yaxes(title_text="명수", row=1, col=1)
fig_gender.update_yaxes(title_text="명수", row=1, col=2)

for i in fig_gender['layout']['annotations']:
    i['font'] = dict(size=25)

################################# 연령별 확진자 추이 fig 객체 생성 #################################

fig_age_confirm = px.bar(timeAge, x='date', y='confirmed', hover_data=['age'], color='age', )
fig_age_confirm.update_layout(title='<b>연령별 확진자 추이</b>', **layout_setting)

################################# 웹 페이지에 띄우기 #################################

app.layout = html.Div(children=[
    html.H1(children='코로나 그래프'),
    html.Div(children='Desined by Dash'),

    dcc.Graph(
        id='fig_time',
        figure=fig_time
    ),
    
    dcc.Graph(
        id='fig_gender',
        figure=fig_gender
    ),
    dcc.Graph(
        id='fig_age_confirm',
        figure=fig_age_confirm
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

