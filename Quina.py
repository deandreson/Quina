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
df_records = df.to_dict(orient='records')


print(df.columns)


# ----------------------------------------------------------#
app = Flask(__name__)
@app.route('/') 
def index():
    return render_template('index.html',jogos=df_records)

if __name__ == '__main__':
    app.run(debug=True)