#__________________________________________________________
#### Execução ###
#   python3 -m venv venv
#	source venv/bin/activate
#	cd Aplicativos/Inquiri
#   export FLASK_ENV=development 
#   export FLASK_APP=Quina
#__________________________________________________________
from flask import Flask, render_template, request, url_for, redirect,jsonify
import pandas as pd
import json 
import plotly
import plotly.graph_objs as go
import numpy as np

def unir_grafico(df, desc_x, desc_y,desc_x_i, desc_y_i, legendas, desc_soma):
    # Gráfico principal
    df['descritivo'] = 'Soma: ' + df[desc_soma].astype(str) +'<br>Bola 1: ' + df['Bola1'].astype(str) + '<br>Bola 2: ' + df['Bola2'].astype(str) +'<br>Bola 3: ' + df['Bola3'].astype(str) + '<br>Bola 4: ' + df['Bola4'].astype(str)+ '<br>Bola 5: ' +df['Bola5'].astype(str)

    trace_principal = go.Scatter(
        x=df[desc_x],
        y=df[desc_y],
        text=df['descritivo'],
        mode='markers',
        marker=dict(size=10, color='blue', opacity=0.7),
        name=legendas[0],
        hovertemplate='%{text}<extra></extra>', 
    )

    # Dados a serem destacados (pode deixar como vazio para alterar via JS)
    trace_destaque = go.Scatter(
        x=df[desc_x_i],
        y=df[desc_y_i],
        text=df['descritivo'],
        mode='markers',
        marker=dict(size=10, color='green', opacity=0.7),
        name='Destaques',  # Placeholder, será alterado no JS
        hovertemplate='%{text}<extra></extra>', 
    )

    data = [trace_principal, trace_destaque]
    layout = go.Layout(
        title=legendas[1],
        xaxis=dict(title=legendas[1]),
        yaxis=dict(title=legendas[2]),
        showlegend=True
    )

    fig = go.Figure(data=data, layout=layout)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
##__________________________________________________________
def criar_grafico(df,desc_x,desc_y,lengedas,desc_soma):
    x=[]
    y=[]
    df['descritivo'] = 'Soma: ' + df[desc_soma].astype(str) +'<br>Bola 1: ' + df['Bola1'].astype(str) + '<br>Bola 2: ' + df['Bola2'].astype(str) +'<br>Bola 3: ' + df['Bola3'].astype(str) + '<br>Bola 4: ' + df['Bola4'].astype(str)+ '<br>Bola 5: ' +df['Bola5'].astype(str)
    viz = [
            go.Scatter(
            x=df[desc_x],
            y=df[desc_y],
            text=df['descritivo'],
            mode='markers',  # 'markers' para pontos, 'lines' para linhas, 'lines+markers' para ambos
            marker=dict(size=5, color='green', symbol='circle', opacity=0.7),
            hovertemplate='%{text}<extra></extra>', 
        )
    ]
    # Layout do gráfico
    layout = go.Layout(
        title=lengedas[0],
        xaxis=dict(title=lengedas[1]),  # Rótulo para o eixo X
        yaxis=dict(title=lengedas[2]),    # Rótulo para o eixo Y
    )
    
    # Criação da figura
    fig = go.Figure(data=viz, layout=layout)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
#__________________________________________________________
def criar_distribuicao_normal(df):
        # Usando a coluna 'soma_total_numeros'
    trace = go.Histogram(
        x=df['Bola4'],
        nbinsx=10,  # Número de bins (intervalos) no histograma
        opacity=0.75,
        name='Distribuição de soma_total_numeros'
    )

    # Configurar o layout do gráfico
    layout = go.Layout(
        title='Distribuição Normal de soma_total_numeros',
        xaxis=dict(title='Soma Total de Números'),
        yaxis=dict(title='Frequência'),
        showlegend=True
    )

    # Criar a figura com os dados e layout
    fig = go.Figure(data=[trace], layout=layout)

    # Converter a figura em JSON para enviar ao front-end
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
#__________________________________________________________
df = pd.read_excel('data/Quina.xlsx')
df['Data Sorteio'] = pd.to_datetime(df['Data Sorteio'], format='%d/%m/%Y', errors='coerce')
df['Data Sorteio']=df['Data Sorteio'].dt.strftime('%d/%m/%Y')
df=df.sort_values(by=['Concurso'],ascending=False)

df['soma_prime_segun']=df['Bola1']+df['Bola2']
df['soma_quart_quint']=df['Bola4']+df['Bola5']
df['soma_total']=df['soma_prime_segun']+df['Bola3']+df['soma_quart_quint']

df['soma_segun_quart']=df['Bola2']+df['Bola4']
df['soma_prime_terce']=df['Bola1']+df['Bola3']
df['soma_terce_quint']=df['Bola3']+df['Bola5']
df['soma_prime_quint']=df['Bola1']+df['Bola5']

df['soma_prime_quart']=df['Bola1']+df['Bola4']
df['soma_segun_quint']=df['Bola2']+df['Bola5']

df['soma_seg_ter_qua']=df['soma_segun_quart']+df['Bola3']

df['soma_pri_seg_ter']=df['soma_prime_segun']+df['Bola3']
df['soma_ter_qua_qui']=df['soma_terce_quint']+df['Bola4']

df['soma_prim_ao_qua']=df['soma_segun_quart']+df['soma_quart_quint']
#__________________________________________________________


app = Flask(__name__)
@app.route('/') 
def index():
    desc_x='soma_total'
    desc_y='Bola1'
    desc_x_i='soma_total'
    desc_y_i='Bola5'
    legendas=['teste','Bola 1','Bola 5']
    desc_soma='soma_total'
    grafico=unir_grafico(df, desc_x, desc_y,desc_x_i, desc_y_i, legendas, desc_soma)
    return render_template('index.html',jogos=df.to_dict(orient='records'),grafico=grafico)

@app.route('/infonografico') 
def infonografico():
    desc_soma='soma_prime_segun'
    desc_x='soma_prime_segun'
    desc_y='soma_quart_quint'
    lengedas=['Gráfico de Dispersão por Soma',
              'Soma de B1 e B2',
              'Soma de B4 e B5']
    grafico_i=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)

    desc_soma='soma_total'
    desc_x='soma_total'
    desc_y='soma_prime_segun'
    lengedas=['Gráfico do Total',
              'Soma de B1, B2, B3, B4 e B5 ',
              'Soma de B1 e B2']
    grafico_ii=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)

    desc_soma='soma_total'
    desc_x='soma_total'
    desc_y='soma_quart_quint'
    lengedas=['Gráfico de Dispersão dos Jogos da Quina',
              'Soma de B1, B2, B3, B4 e B5',
              'Soma de B4 e B5' ]
    grafico_iii=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)

    desc_soma='soma_pri_seg_ter'
    desc_x='soma_pri_seg_ter'
    desc_y='soma_ter_qua_qui'
    lengedas=['Gráfico de Dispersão dos Jogos da Quina',
              'Soma de B1, B2 e B3',
              'Soma de B3, B4 e B5' ]
    grafico_iv=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)

    desc_soma='soma_seg_ter_qua'
    desc_x='soma_seg_ter_qua'
    desc_y='soma_prime_quint'
    lengedas=['Gráfico de Soma',
              'Soma B2, B3 e B4 ',
              'Soma B1 e B5' ]
    grafico_v=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)

    desc_soma='soma_prime_quart'
    desc_x='soma_prime_quart'
    desc_y='soma_segun_quint'
    lengedas=['Gráfico de Soma',
              'Soma B1 e B4 ',
              'Soma B2 e B5' ]
    grafico_vi=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)
    return render_template('infonografico.html',grafico_i=grafico_i,grafico_ii=grafico_ii,grafico_iii=grafico_iii,grafico_iv=grafico_iv,grafico_v=grafico_v,grafico_vi=grafico_vi)
#__________________________________________________________

@app.route('/analise') 
def analise():
    desc_soma='soma_total'
    desc_x='Bola1'
    desc_y='soma_total'
    lengedas=['B1 versus Soma Total',
              'B1',
              'Soma B1,B2,B3,B4 e B5']
    grafico_i_a=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)
    
    desc_soma='soma_total'
    desc_x='soma_total'
    desc_y='Bola1'
    lengedas=['Soma Total versus B1',
              'Soma B1,B2,B3,B4 e B5',
              ' B1']
    grafico_i_b=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)
#__________________________________________________________

    desc_soma='soma_total'
    desc_x='Bola2'
    desc_y='soma_total'
    lengedas=['B2 versus Soma Total',
              'B2 ',
              'Soma B1,B2,B3,B4 e B5']
    grafico_ii_a=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)

    desc_soma='soma_total'
    desc_x='soma_total'
    desc_y='Bola2'
    lengedas=['Soma Total versus B2',
              'Soma B1,B2,B3,B4 e B5',
              'B2']
    grafico_ii_b=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)
#__________________________________________________________

    desc_soma='soma_total'
    desc_x='Bola3'
    desc_y='soma_total'
    lengedas=['B3 versus Soma Total',
              'B3',
              'Soma B1,B2,B3,B4 e B5' ]
    grafico_iii_a=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)

    desc_soma='soma_total'
    desc_x='soma_total'
    desc_y='Bola3'
    lengedas=['Soma Total versus B3',
              'Soma B1,B2,B3,B4 e B5',
              'B3']
    grafico_iii_b=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)
#__________________________________________________________

    desc_soma='soma_total'
    desc_x='Bola4'
    desc_y='soma_total'
    lengedas=['B4 versus Soma Total',
              'B4',
              'Soma B1,B2,B3,B4 e B5' ]
    grafico_iv_a=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)

    desc_soma='soma_total'
    desc_x='soma_total'
    desc_y='Bola4'
    lengedas=['Soma Total versus B4',
              'Soma de B1, B2 e B3',
              'B4' ]
    grafico_iv_b=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)
#__________________________________________________________
    desc_soma='soma_total'
    desc_x='Bola5'
    desc_y='soma_total'
    lengedas=['B5 versus Soma Total',
              'B5',
              'Soma B1,B2,B3,B4 e B5' ]
    grafico_v_a=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)

    desc_soma='soma_total'
    desc_x='soma_total'
    desc_y='Bola5'
    lengedas=['Soma Total versus B5',
              'Soma B1,B2,B3,B4 e B5',
              'B5' ]
    grafico_v_b=criar_grafico(df,desc_x,desc_y,lengedas,desc_soma)
    return render_template('analise.html',grafico_i_a=grafico_i_a,grafico_i_b=grafico_i_b,
                           grafico_ii_a=grafico_ii_a,grafico_ii_b=grafico_ii_b,
                            grafico_iii_a=grafico_iii_a,grafico_iii_b=grafico_iii_b,
                            grafico_iv_a=grafico_iv_a,grafico_iv_b=grafico_iv_b,
                            grafico_v_a=grafico_v_a,grafico_v_b=grafico_v_b)
#__________________________________________________________

if __name__ == '__main__':
    app.run(debug=True)