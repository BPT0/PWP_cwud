from flask import Flask, request, render_template
import requests
import openai
import pandas as pd
import glob
import os

app = Flask(__name__)

openai.api_key = "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"

@app.route('/')
def index():
    musics = glob.glob("*.xlsx");     # 음악들 데이터로 초기화
    print(musics)   
    return render_template("listmusic.html",  musics = musics)


@app.route('/make')
def musicList() :
    role = request.args.get("role", "")
    
    mon = request.args.get("mon", "")
    tue = request.args.get("tue", "")
    wes = request.args.get("wes", "")
    thu = request.args.get("thu", "")
    fri = request.args.get("fri", "")
    sat = request.args.get("sat", "")
    sun = request.args.get("sun", "")

    jenre = request.args.get("jenre", "")
    feel = request.args.get("feel", "")
    weather = request.args.get("weather", "")
    
    num = int(request.args.get("num", 5))

    playlistName = request.args.get("playlistName", "")
    
    prompt  = f"""
    당신은 {role} DJ 입니다.
    이번주 월요일엔 {mon}, 화요일엔 {tue}, 수요일엔 {wes}, 목요일엔 {thu}, 
    금요일엔 {fri}, 토요일엔 {sat}, 일요일엔, {sun} 음악을 들은 사람에게
    {jenre}이고 {feel}감정일때 {weather}에 적절한 음악을 들으려고 합니다.
    추천하는 음악과 유튜브 링크를 표시하려 합니다
    please generate python code to write excel file using dataframe in table format with 7 columns.
    please save the excel file as {playlistName}.xlsx.
    python 코드만 작성하고 설명이나 주석없이 코드만 알려주세요
    
    column 1 : 월, column 2 : 화, column 3 : 수, column 4 : 목,  column 5 : 금,  column 6 : 토,  column 7 : 일,
    """
    
    print(prompt)
    messages = []
    messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    res = completion.choices[0].message['content']
    print(res)
    exec(res)    
    return  "code : <br/>" + res.replace("\n", "<br/>").replace(" "," &nbsp;")


@app.route('/readmusic/<file>')
def readmusic(file) :
    df = pd.read_excel(file)     
    return render_template("readmusic.html", data=df.to_dict('record'))
   
if __name__ == '__main__':
	app.run(debug=True)