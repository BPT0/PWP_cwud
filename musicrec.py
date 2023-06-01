import os
import openai
import re
import glob
import pandas as pd
from flask import Flask, request, redirect, render_template

# api_key = os.environ["api_key"]
# openai.api_key = api_key 
openai.api_key = "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"

app = Flask(__name__)

messages = []

# /(루트) 요청이 들어왔을때
@app.route('/')
def index():
    files = glob.glob("*.xlsx") # 모든 엑셀파일을 조회해서 files에 저장
    print(files)
    # file에 저장된 내용을 listmusic.html에 fieles 변수에 표시
    return render_template('listmusic.html', files = files)

# /에서 submit 버튼을 눌러 /gpt 로 결과 요청시
@app.route('/gpt')
def gpt():    
    global messages
    # listmusic.html 에서 입력받은 "변수" 선언 그리고
    # 1. 값이 있을때 입력받은 변수 값으로 초기화
    # 2."값이 없을때 "디폴트값" 으로 초기화
    
    # 월, 화 수, 목, 금, 토, 일 노래와
    myMusicMon = request.args.get("myMusicMon", "In The Stars - BensonBoone")    
    myMusicTue = request.args.get("myMusicTue", "In The Stars - BensonBoone")
    myMusicWed = request.args.get("myMusicWed", "In The Stars - BensonBoone")
    myMusicThu = request.args.get("myMusicThu", "In The Stars - BensonBoone")
    myMusicFri = request.args.get("myMusicFri", "In The Stars - BensonBoone")
    myMusicSat = request.args.get("myMusicSat", "In The Stars - BensonBoone")
    myMusicSun = request.args.get("myMusicSun", "In The Stars - BensonBoone")
    # 장르, 기분, 날씨에 따라 입력 받음
    genre = request.args.get("genre", "랜덤하게")    
    feeling = request.args.get("feeling", "랜덤하게")       
    weather = request.args.get("weather", "관계없이")       
    
    #프롬프트에 입력 내용
    prompt = f"""
    다음은 이번주 요일별 들은 노래입니다. 
    월: {myMusicMon}
    화: {myMusicTue}
    수: {myMusicWed}
    목: {myMusicThu}
    금: {myMusicFri}
    토: {myMusicSat}
    일: {myMusicSun}
    당신은 DJ입니다. 장르는 {genre}, 기분은 {feeling}, 그리고 날씨는 {weather}의 조건에 모두 만족하고
    이번주 들은 요일별 노래의 느낌에 맞도록 다음주의 월,화,수,목,금,토,일에 들으면 좋을 노래를 
    "노래제목-가수이름", "연결가능한 유튜브 URL"과 함께 추천해주세요.
    """
    messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  messages=messages)    

    # 입력받은 결과에 \n(줄바꿈)을 <br/>태그로 변경
    # " "(공백)을 &nbsp; 공백 특수문자로 변경
    res = completion.choices[0].message['content'].replace("\n", "<br/>").replace(" "," &nbsp;" )
    messages.append({"role": 'assistant', "content": res}  )
    print(res)

    # 리턴할 html에 답변한 res와 장르, 기분, 날씨 표시
    html = f"""
    <html>
	<head><title>추천 받은 음악</title>
</head>
<body id="wrapper">
	<h1>음악 추천 사이트</h1>
	<hr>
	<div>다음 주 추천 받은 음악</div>
	<div>장르: {genre}, 기분: {feeling}, 날씨: {weather} 의 조건으로 설정했습니다.</div>
	<br>
    <form action=/playlist> 
    {res}
    <hr>
    <div> 추천 받은 플레이리스트를 저장하고 싶으면 이름을 설정하고, "저장하기"를 눌러주세요.<div>
    <div> 
        다음주 플레이리스트 이름 설정
        <input id="playlist" type="text" name="playlist">
     </div>
     <input type=submit value=저장하기>
    </form>
</body>
</html>   
    """ 
    return html

# /gpt에서 처리된 화면에서 
# 파일명 입력후 저장버튼 클릭시 실행
@app.route('/playlist')
def playlist():   
    global messages
    playlist_name = request.args.get("playlist", "music")
    
    # 프롬프트에 입력받은 노래 리스트를 엑셀로 만들어 저장
    prompt = f"""
    추천 받은 노래-가수와 URL을
    please generate  python code to write excel file using dataframe in table format with 2 columns and 7rows.
    when saving as excel file, use df.to_excel() only.
    please save the excel file as {playlist_name}.xlsx.
    I don't need any explanations. please give me only code. 

    column 1 : '요일', column 2: '노래-가수', column 3: 'URL'
    """    

    print(prompt)
    messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  messages=messages)    

    res = completion.choices[0].message['content'].replace("```", "")
    print(res)
    # 결과 실행후 /(루트)로 돌아감
    exec(res)    
    return redirect('/')

# 저장하고 다시 돌아온 /(루트)에서
# 생성된 엑셀파일 링크 클릭시
# 엑셀파일을 가공해 데이터를 표시한 readmusic.html 에 데이터 표시 
@app.route('/readmusic/<file>')
def readquiz(file) :     
    # 파일을 가져와서 읽고
    df = pd.read_excel(file)
    # data 변수에 엑셀에 담긴 값을  전달     
    return render_template("readmusic.html", data=df.to_dict('record'))

if __name__ == '__main__':
	app.run(debug=True)