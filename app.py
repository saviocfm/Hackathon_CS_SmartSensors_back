from flask import Flask,request
import sqlite3
from flask_cors import CORS

from importlib_metadata import re

conn = sqlite3.connect('hackathon.db',check_same_thread=False)
cursor = conn.cursor()

def createTable():
    cursor.execute("""CREATE TABLE IF NOT EXISTS hackathon(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cidade TEXT,
        bairro TEXT,
        estado TEXT,
        rua TEXT,
        distancia TEXT,
        perda NUMERIC,
        latitude TEXT,
        longitude TEXT,
        mapa TEXT
    )""")
    conn.commit()


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/add', methods=['POST'])
def add():
    cidade = request.json['cidade']
    bairro = request.json['bairro']
    estado = request.json['estado']
    rua = request.json['rua']
    distancia = request.json['distancia']
    perda = request.json['perda']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    mapa = request.json['mapa']
    cursor.execute("""INSERT INTO hackathon(cidade,bairro,estado,rua,distancia,perda,latitude,longitude,mapa)
    VALUES(?,?,?,?,?,?,?,?,?)""",(cidade,bairro,estado,rua,distancia,perda,latitude,longitude,mapa))
    conn.commit()
    return 'Dados inseridos com sucesso!'

@app.route('/get', methods=['GET'])
def get():
    cursor.execute('''SELECT
    case 
        when perda < 0.01  then 'rompido'
        else 'normal'
    end as status,
    id,
    cidade,
    bairro,
    estado,
    rua,
    distancia,
    perda,
    latitude,
    longitude,
    mapa
    FROM hackathon''')
    rows = cursor.fetchall()
    ret = []
    for i in rows:
        ret.append({
            'status': i[0],
            'id': i[1],
            'cidade': i[2],
            'bairro': i[3],
            'estado': i[4],
            'rua': i[5],
            'distancia': i[6],
            'perda': i[7],
            'latitude': i[8],
            'longitude': i[9],
            'mapa': i[10]
        }) 
    return {
        "dados": ret
    }

@app.route('/delete', methods=['DELETE'])
def delete():
    id = request.form['id']
    cursor.execute("DELETE FROM hackathon WHERE id = ?", (id,))
    conn.commit()
    return 'Dados deletados com sucesso!'

@app.route('/update', methods=['PUT'])
def update():
    id = request.json['id']
    cidade = request.json['cidade']
    bairro = request.json['bairro']
    estado = request.json['estado']
    rua = request.json['rua']
    distancia = request.json['distancia']
    perda = request.json['perda']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    mapa = request.json['mapa']
    cursor.execute("""UPDATE hackathon SET cidade = ?,bairro = ?,estado = ?,rua = ?,distancia = ?,perda = ?,latitude = ?,longitude = ?,mapa = ? WHERE id = ?""",(cidade,bairro,estado,rua,distancia,perda,latitude,longitude,mapa,id))    
    conn.commit()
    return 'Dados atualizados com sucesso!'

def main():
    createTable()
    app.run(debug=True)

main()
