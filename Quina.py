#### Execução ###
#   python3 -m venv venv
#	source venv/bin/activate
#	cd Aplicativos/Inquiri
#   export FLASK_ENV=development 
#   export FLASK_APP=Quina
###########################################
from flask import Flask, render_template, request, url_for, redirect,jsonify

import pandas as pd

# --------------------------------------------------------#
df = pd.read_excel('data/Quina.xlsx')
df = df.head(5)
# Conver# Converter o DataFrame para JSON
df_json = df.to_json(orient='records', force_ascii=False)



# ----------------------------------------------------------#
app = Flask(__name__)
@app.route('/') 
def index():
    return render_template('index.html',jogos=df_json)

if __name__ == '__main__':
    app.run(debug=True)