#PARA CORRER LA APLICACION
# python app.py

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_daq as daq
from dash.dependencies import Input, Output
from datetime import datetime
import os

#LEE ARCHIVO BASE
csv_files_path = os.path.join("data/INVENTARIOS.csv")
df = pd.read_csv(csv_files_path) 
#DATOS FILTRADOS 
df_TK1 = df[df['TANQUE']=='TK1']
df_TK2 = df[df['TANQUE']=='TK2']
df_TK3 = df[df['TANQUE']=='TK3']
df_TK4 = df[df['TANQUE']=='TK4']
df_TK5 = df[df['TANQUE']=='TK5']

df_TK800 = df[df['TANQUE']=='TK 800']
df_TK500 = df[df['TANQUE']=='TK 500']
df_TK60 = df[df['TANQUE']=='TK 60']

df_N1 = df[df['TANQUE']=='N1']

df_N2 = df[df['TANQUE']=='N2']

df_TK370 = df[df['TANQUE']=='TK 370']

df_CRISTA1TPF = df[df['TANQUE']=='CRISTA 1'][df[df['TANQUE']=='CRISTA 1']['PRODUCTO']=='PALMA RBD']
df_CRISTA2TPF = df[df['TANQUE']=='CRISTA 2'][df[df['TANQUE']=='CRISTA 2']['PRODUCTO']=='PALMA RBD']
df_TOLVA = df[df['TANQUE']=='TOLVA ']
df_OLEINA_LAVADO = df[df['TANQUE']=='OLEINA LAVADO']
df_TK40 = df[df['TANQUE']=='TK40 RECEPCION ']
df_TK150 = df[df['TANQUE']=='TK150 ']
df_TKEMPAQUE = df[df['TANQUE']=='TK EMPAQUE  ']
df_OLEINA_ENVASADA = df[df['TANQUE']=='OLEINA ENVASADA']

df_CRISTA1TPI = df[df['TANQUE']=='CRISTA 1'][df[df['TANQUE']=='CRISTA 1']['PRODUCTO'].isnull()]
df_CRISTA2TPI = df[df['TANQUE']=='CRISTA 2'][df[df['TANQUE']=='CRISTA 2']['PRODUCTO'].isnull()]
df_TOLVA1 = df[df['TANQUE']=='TOLVA 1']
df_TOLVA2 = df[df['TANQUE']=='TOLVA 2']

#ESTILOS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config["suppress_callback_exceptions"] = True

#COLORES
colors = {
    'background': '#f7f7f7',
    'text': '#00a99e',
    'title': '#99b9b7',
    'subtitle': '#99b9b7',
    'Graph': '#d4d4d4',
    'text1' : '#080909',
    'GraphLine' : '#f4d44d',
    'Alto' : '#99e699',
    'Medio' : '#aae2fb',
    'Bajo' : '#ff9999'
        }
#DEFINICION FUNCIONES 

def elaboracion_encabezado():
    return [
                html.Div(
                [
            html.H1(children='CONTROL DE INVENTARIOS',
                    style={'margin-left': '20px','margin-top': '50px','textAlign': 'left','color': colors['text']},
                     className="nine columns"),
            html.Img(src= app.get_asset_url('logo1.png'),
                     className="three columns",
                     style={'height': '15%','width': '15%','float': 'right','position':'relative'}),
                 ],className="row"),
        ]

def titulo_graficos(titulo1,titulo2):
    return html.Div([
            html.H5(children=titulo1,
                    style={'textAlign': 'left','color': colors['text']},
                     className="six columns"),
            html.H5(children=titulo2,
                    style={'textAlign': 'left','color': colors['text']},
                     className="six columns"),
                    ],className="row")

def colortanq(Altura,Contenido_Actual):
    if Contenido_Actual/Altura>0.66:
        return colors['Alto']
    if Contenido_Actual/Altura>0.33:
        return colors['Medio']
    if Contenido_Actual/Altura<=0.33:
        return colors['Bajo']  
    
def diasdedatos():
    return (datetime.strptime(max(df['FECHA']), "%Y-%m-%d").timestamp()-datetime.strptime(min(df['FECHA']), "%Y-%m-%d").timestamp())/86400
    

def filtros():
    return [
            html.Label('FILTRO RANGO DE FECHAS'),
                dcc.RangeSlider(
                    id='day-slider',
                    count=1,
                    min= 0,
                    max= diasdedatos(),
                    step=1,
                    value= [0,diasdedatos()]
                )
        ]

def grafica_tanque_historico(variable1,variable2,altura):
   return html.Div([ 
                html.Div(
                    children=[
                    daq.Tank(
                    value = round(variable2.iloc[-1]),
                    min = 0,
                    max = altura,
                    showCurrentValue=True,
                    units='Kilogramos',
                    width=90,
                    color = colortanq(altura,round(variable2.iloc[-1])),
                    style={'margin-left': '60px'}),
                    ], className="two columns"),
                html.Div(
                children=[
                    dcc.Graph(id='historic-graph',
                    figure={
                        'data': [
                            {'x': variable1, 'y': variable2, "mode": "lines+markers", 'name': 'TK2',"line": {"color": 'GraphLine'}},
                            #{'x': df_TK2['FECHA'], 'y': df_TK2['KG.'], 'type': 'bar', 'name': u'TK2'},
                        ],
                        'layout': {
                            'title' : "Histórico",
                            "margin": dict(l=30, r=30, t=30, b=30, pad=0),
                            'plot_bgcolor': colors['Graph'],
                            'paper_bgcolor': colors['Graph'],
                            'font': {'color': colors['text1']},
                                }
                            },
                            style={"height":200},
                            ),
                        ], className="four columns"),
           ])

def elaboracion_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="TAB1",
                        label="MATERIAS PRIMAS REFINADAS MARGARINAS",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="TAB2",
                        label="MATERIAS PRIMAS REFINERIA",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                     dcc.Tab(
                        id="TAB3",
                        label="MATERIAS PRIMAS CRUDAS",
                        value="tab3",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                     dcc.Tab(
                        id="TAB4",
                        label="MATERIAS PRIMAS BLANQUEADAS",
                        value="tab4",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                     dcc.Tab(
                        id="TAB5",
                        label="TANQUES PLANTA  LURGI",
                        value="tab5",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                     dcc.Tab(
                        id="TAB6",
                        label="TANQUES PLANTA FRACCIONAMIENTO",
                        value="tab6",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                     dcc.Tab(
                        id="TAB7",
                        label="TANQUES PLANTA INTERESTERIFICADO ",
                        value="tab7",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],style={'textAlign': 'center','color': colors['title'], 'font-size': '12px'},
            )
        ],
    )

def elaboracion_tab_1():
    return [
                #TITULO GENERAL1
                html.Div(id='TMPM',children=[
                    #html.H4(children='TANQUES MATERIAS PRIMAS REFINADAS MARGARINAS',
                    #        style={'textAlign': 'center','color': colors['title']},
                    #         className="row"),
            #TITULO TANQUE 1 + TANQUE 2
                    titulo_graficos('TANQUE 1 ESTEARINA  DE PALMA  RBD','TANQUE 2 INTERESTERIFICADO'),
                #TANQUE 1
                    html.Div([
                    grafica_tanque_historico(df_TK1['FECHA'],df_TK1['KG.'],63000),
                #TANQUE 2
                    grafica_tanque_historico(df_TK2['FECHA'],df_TK2['KG.'],63000),
                    ],className="row"),
            #TITULO TANQUE 3 + TANQUE 4
                    titulo_graficos('TANQUE 3 PALMISTE RBD','TANQUE 4 GRASA DURA'),
                #TANQUE 3
                    html.Div([
                    grafica_tanque_historico(df_TK3['FECHA'],df_TK3['KG.'],63000),
                #TANQUE 4
                    grafica_tanque_historico(df_TK4['FECHA'],df_TK4['KG.'],63000),
                    ],className="row"),
            #TITULO TANQUE 5
                    titulo_graficos('TANQUE 5 PALMA RBD',''),
                #TANQUE 5
                    html.Div([
                    grafica_tanque_historico(df_TK5['FECHA'],df_TK5['KG.'],63000),
                    ],className="row"),
                    ]),  
        ]

def elaboracion_tab_2():
    return [
                html.Div(id = 'TMPR',children=[
            #TITULO TANQUE 800 + TANQUE 500
                    titulo_graficos('TANQUE 800 PALMA RBD','TANQUE 500 PALMA RBD'),
                #TANQUE 800
                    html.Div([
                    grafica_tanque_historico(df_TK800['FECHA'],df_TK800['KG.'],816000),
                #TANQUE 500
                    grafica_tanque_historico(df_TK500['FECHA'],df_TK500['KG.'],48100),
                    ],className="row"),
            #TITULO TANQUE 60
                    titulo_graficos('TANQUE 60 ACIDOS GRASOS DE PALMA',''),
                #TANQUE 60
                    html.Div([
                    grafica_tanque_historico(df_TK60['FECHA'],df_TK60['KG.'],62700),
                    ],className="row")
                ])
            ]
                    
def elaboracion_tab_3():
    return [
                html.Div(id = 'TMPC',children=[
            #TITULO TANQUE N1
                    titulo_graficos('TANQUE N1 ACEITE DE PALMA CRUDO (CPO)',''),
                #TANQUE N1
                    html.Div([
                    grafica_tanque_historico(df_N1['FECHA'],df_N1['KG.'],29400),
                    ],className="row")
                ])
            ]

def elaboracion_tab_4():
    return [
                html.Div(id = 'TMPB',children=[
            #TITULO TANQUE N2
                    titulo_graficos('TANQUE N2 ACEITE DE PALMA BLANQUEADO (BPO)',''),
                #TANQUE N2
                    html.Div([
                    grafica_tanque_historico(df_N2['FECHA'],df_N2['KG.'],29400),
                    ],className="row")
                ])
            ]

def elaboracion_tab_5():
    return [
                html.Div(id = 'TPL',children=[
            #TITULO TANQUE N2
                    titulo_graficos('TANQUE 370 PALMISTE CRUDO',''),
                #TANQUE N2
                    html.Div([
                    grafica_tanque_historico(df_TK370['FECHA'],df_TK370['KG.'],353000),
                    ],className="row")
                ])
            ]

def elaboracion_tab_6():
    return [
                html.Div(id='TPF',children=[
            #TITULO CRISTA 1 + CRISTA 2
                    titulo_graficos('CRISTA 1 PALMA RBD','CRISTA 2 PALMA RBD'),
                #CRISTA 1
                    html.Div([
                    grafica_tanque_historico(df_CRISTA1TPF['FECHA'],df_CRISTA1TPF['KG.'],42500),
                #CRISTA 2
                    grafica_tanque_historico(df_CRISTA2TPF['FECHA'],df_CRISTA2TPF['KG.'],42500),
                    ],className="row"),
            #TITULO TOLVA + OLEINA LAVADO
                    titulo_graficos('TOLVA ESTEARINA DE PALMA RBD','OLEINA LAVADO'),
                #TOLVA
                    html.Div([
                    grafica_tanque_historico(df_TOLVA['FECHA'],df_TOLVA['KG.'],20400),
                #OLEINA LAVADO
                    grafica_tanque_historico(df_OLEINA_LAVADO['FECHA'],df_OLEINA_LAVADO['KG.'],5700),
                    ],className="row"),
            #TITULO TK40 RECEPCION  + TK150
                    titulo_graficos('TANQUE 40 RECEPCION OLEINA PROCESO','TANQUE 150 OLEINA DESPACHO'),
                #TK40 RECEPCION 
                    html.Div([
                    grafica_tanque_historico(df_TK40['FECHA'],df_TK40['KG.'],40800),
                #TK150
                    grafica_tanque_historico(df_TK150['FECHA'],df_TK150['KG.'],156000),
                    ],className="row"),
            #TITULO TK EMPAQUE  
                    titulo_graficos('TANQUE EMPAQUE OLEINA',''),
                #TANQUE TK EMPAQUE
                    html.Div([
                    grafica_tanque_historico(df_TKEMPAQUE['FECHA'],df_TKEMPAQUE['KG.'],13500),
                    ],className="row")
                    ]),  
        ]

def elaboracion_tab_7():
    return [
                html.Div(id='TPI',children=[
            #TITULO CRISTA 1 + CRISTA 2
                    titulo_graficos('CRISTA 1','CRISTA 2'),
                #CRISTA 1
                    html.Div([
                    grafica_tanque_historico(df_CRISTA1TPI['FECHA'],df_CRISTA1TPI['KG.'],16700),
                #CRISTA 2
                    grafica_tanque_historico(df_CRISTA2TPI['FECHA'],df_CRISTA2TPI['KG.'],12500),
                    ],className="row"),
            #TITULO TOLVA 1 + TOLVA 1
                    titulo_graficos('TOLVA 1','TOLVA 2'),
                #TOLVA 1
                    html.Div([
                    grafica_tanque_historico(df_TOLVA1['FECHA'],df_TOLVA1['KG.'],5300),
                #TOLVA 2
                    grafica_tanque_historico(df_TOLVA2['FECHA'],df_TOLVA2['KG.'],7400),
                    ],className="row"),
                    ]),  
        ]


app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.Div([
    #ENCABEZADO
        html.Div(elaboracion_encabezado()),
    #TABS
        html.Div(elaboracion_tabs()),
    #FILTROS
        html.Div(filtros()),
          
        html.Div(id = 'secciones',children=[
    #CONTENIDO
              html.Div(id="app-content"),

                ])
        ])
])

@app.callback(
    Output("app-content", "children"),
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return elaboracion_tab_1()
    if tab_switch == "tab2":
        return elaboracion_tab_2()
    if tab_switch == "tab3":
        return elaboracion_tab_3()
    if tab_switch == "tab4":
        return elaboracion_tab_4()
    if tab_switch == "tab5":
        return elaboracion_tab_5()
    if tab_switch == "tab6":
        return elaboracion_tab_6()
    if tab_switch == "tab7":
        return elaboracion_tab_7()


if __name__ == '__main__':
    app.run_server(debug=True)

@app.callback(
    Output('historic-graph', 'figure'),
    [Input('day-slider', 'value')]
   )
def update_figure(selected_date):
    return 