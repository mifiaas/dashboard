#!/usr/bin/env python3
# /mnt/data/dashboard_app.py
# Dash app to visualize survey results for Simulado de Catástrofe
import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output, State
import plotly.express as px

DATA_PATH = "/mnt/data/processed_survey.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    df['mean'] = pd.to_numeric(df['mean'], errors='coerce')
    return df

app = Dash(__name__)
server = app.server

df = load_data()
stages = ['All'] + sorted(df['stage'].dropna().unique().tolist())

app.layout = html.Div([
    html.H2('Dashboard - Simulado de Catástrofe (Enfermagem)'),
    html.Div([
        html.Label('Selecione a etapa:'),
        dcc.Dropdown(id='stage-filter', options=[{'label':s,'value':s} for s in stages], value='All', clearable=False)
    ], style={'width':'30%'}),
    html.Br(),
    dcc.Graph(id='mean-bar'),
    html.Br(),
    dash_table.DataTable(
        id='table',
        columns=[{'name':'Etapa','id':'stage'}, {'name':'Pergunta (exemplo variável)','id':'question_var_example'}, {'name':'Label','id':'label'}, {'name':'Média','id':'mean'}, {'name':'Observações','id':'observations'}],
        data=df.to_dict('records'),
        page_size=20,
        style_cell={'textAlign':'left','whiteSpace':'normal','height':'auto'},
        style_table={'overflowX':'auto'}
    )
])

@app.callback(
    Output('table','data'),
    Output('mean-bar','figure'),
    Input('stage-filter','value')
)
def update(stage):
    dff = df.copy()
    if stage and stage!='All':
        dff = dff[dff['stage']==stage]
    fig = px.bar(dff, x='q_num', y='mean', hover_data=['label','observations'], labels={'q_num':'Pergunta','mean':'Média'})
    dff2 = dff.copy()
    dff2['observations'] = dff2['observations'].fillna('')
    return dff2.to_dict('records'), fig

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
