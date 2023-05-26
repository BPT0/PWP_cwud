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
    return render_template("listquiz.html",  musics = musics)


@app.route('/make')
def quiz() :
    role = request.args.get("role", "")
    sel = request.
    subject = request.args.get("subject", "")
    num = int(request.args.get("num", 5))
    prompt  = f"""
    당신은 {role} DJ 입니다.
    월요일엔 {mon}, 화요일엔 {tue}, 수요일엔 {wes}, 목요일엔 {thu}, 
    금요일엔 {fri}, 토요일엔 {sat}, 일요일엔, {sun} 음악을 들은 사람에게
    {subject} 주제를 가진 음악을 추천해주고 음악마다 유튜브 링크를 표시하려 합니다
    please generate python code to write excel file using dataframe in table format with 7 columns.
    please save the excel file as {subject}.xlsx.
    python 코드만 작성하고 설명이나 주석없이 코드만 알려주세요
    
    
    column 1 : 월, column 2 : 화, column 3 : 수, column 4 : 목,  column 5 : 금,  column 6 : 토,  column 7 : 일,
    """
    
    if(sel == subject){
        
    }

    print(prompt)
    messages = []
    messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    res = completion.choices[0].message['content']
    print(res)
    exec(res)    
    return  "code : <br/>" + res.replace("\n", "<br/>").replace(" "," &nbsp;")

@app.route('/readquiz/<file>')
def readquiz(file) :
    df = pd.read_excel(file)     
    return render_template("readquiz.html", data=df.to_dict('record'))
   
if __name__ == '__main__':
	app.run(debug=True)


<div class="form-group col-sm-5">
        <label for="addressKindU">도/특별시 선택</label>
        <select class="form-control" id="addressKindU" name="addressKindU" onchange="addressKindChange(this)">
        <option>주소를 선택하세요</option>
        <option value="a">서울</option>
        <option value="b">경기도</option>
        <option value="c">충청남도</option>
        </select>
    </div>
    <div class="form-group col-sm-4">
        <label for="addressKindD">주소 소분류</label>
        <select class="form-control" id="addressKindD" name="addressKindD">
        <option>선택해주세요.</option>
        </select>
    </div>