# flask
from flask import Flask
from flask import request, render_template, url_for, redirect, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_paginate import Pagination, get_page_parameter, get_page_args

from matplotlib import pyplot as plt
from wordcloud import WordCloud
# from PIL import Image
# from collections import Counter
import jieba
# import io
# import os
import urllib, base64
import pandas as pd

import sqlite3 as DB

app = Flask(__name__)

#連接資料庫
def get_DB():
    conndb = DB.connect(sqlite_path) # 若有則讀取，沒有則建立
    curr = conndb.cursor()  
    return [conndb,curr]

def queryData(webName):
    # global sqlite_path
    [conndb,curr] = get_DB()
    try:
        results = curr.execute("SELECT * FROM {} ORDER BY Date DESC;".format(webName))
    except DB.OperationalError:
        return 'No Such Table'
    return results

def queryDataCnt(boardName):
    # global sqlite_path
    [conndb,curr] = get_DB()
    try:
        cnt = []
        for webName in boardName:
            results = curr.execute(f'SELECT count(*) FROM {webName};')
            cnt.append(results.fetchall()[0][0])
    except DB.OperationalError:
        return 'No Such Table'
    return cnt

def queryBoardName():
    # global sqlite_path
    [conndb,curr] = get_DB()
    boardList = []
    try:
        results = curr.execute("SELECT name FROM sqlite_master")
        for row in results:
            boardList.append(row[0])
    except DB.OperationalError:
        return 'No Tables'
    return boardList


#抓取部分資料
def fetch_data(datas, offset=0, per_page=10):
    return datas[offset: offset + per_page]

#創造分頁
def make_pagination():

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    # per_page = PER_PAGE
    # offset = PER_PAGE
    
    print(page, per_page, offset)

    # 用fetch_data這個函式來抓取分段的資料
    page_datas = fetch_data(datas, offset=offset, per_page=per_page)
    
    # 設定分頁
    pagination = Pagination(page=page, per_page=per_page, total=len(datas), css_framework='bootstrap4', record_name='review')

    return page_datas, pagination

# 畫文字雲
# def plt_WordCloud(word_freq):
#     height, width  = 600, 800

#     # print(stop_words)
#     # stop_words = ["https", "com", "/", 'imgur', 'jpg','jpghttps','jpghttp']+stop_words
#     wc = WordCloud(font_path="simsun.ttc", 
#                 height=height, 
#                 width=width
#                 ).generate_from_frequencies(dict(word_freq))
#     # plt.figure(figsize=(width/96.,height/96.)) #pixel to inch
#     plt.imshow(wc)
#     plt.axis("off")
#     # wc.to_file("wordcloud.png")

#     image = io.BytesIO()
#     plt.tight_layout()
#     plt.savefig(image, format='png')
#     image.seek(0)  # rewind the data
#     string = base64.b64encode(image.read())
#     image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
#     return image_64

#定義資料庫位置
sqlite_path = 'ptt.db'
[conndb,curr] = get_DB()


# 設定密碼
secret_key = 'ptt_test'

# os.urandom(16).hex()

app = Flask(__name__)
app.secret_key = secret_key

#初始化Flask-Login
login_manager = LoginManager()

#將flask與flask-login綁定
login_manager.init_app(app)

#預設是'basic'，這行可寫可不寫
# login_manager.session_protection = "strong"

#當未登入的使用者請求了一個需要權限的網頁時，就將他送到代表login()的位址去，login()是函式
login_manager.login_view = 'login'

#當未登入的使用者被送到login_view所指定的位址時，會一併跳出的訊息
login_manager.login_message = '請輸入帳號密碼已登入，此為demo，帳號為Madi，密碼為0168'

#繼承Flask-login裏頭的UserMixin
class User(UserMixin):
    pass

#驗證使用者是否存在在合法清單內
@login_manager.user_loader
def user_loader(loginUser):
    if loginUser not in users:
        return
    user = User()
    user.id = loginUser
    return user

#驗證使用者的密碼是否正確
@login_manager.request_loader
def request_loader(request):
    loginUser = request.form.get('user_id')
    if loginUser not in users:
        return
    user = User()
    user.id = loginUser
    return user

#建立一個使用者清單
users = {'Madi': {'password': '0168'}}

# 設定成global才不換頁就沒資料
datas = ''
webName = ''
# pagination = ''
boardName = ''

# 首頁
@app.route('/', methods=['GET','POST'])
@login_required #指定該頁面一定要登入才能查看
def home():
    global datas, webName, pagination, boardName
    boardName = queryBoardName()
    if request.method == 'GET':
        # 第一次登入
        if datas == '':
            return render_template('index.html', boardName=boardName)
        # 已經有datas，代表有post過表單，但換頁的pagination是用GET方式傳送，所以要寫在這
        else:
            page_datas, pagination = make_pagination()
            # page, per_page, offset = get_page_args(page_parameter='page',
            #                                        per_page_parameter='per_page')
            # # per_page = 5
            # print(page, per_page, offset)

            # # 用fetch_data這個函式來抓取分段的資料
            # page_datas = fetch_data(datas, offset=offset, per_page=per_page)
            
            # # 設定分頁
            # pagination = Pagination(page=page, per_page=per_page, total=len(datas), css_framework='bootstrap4', record_name='review')
            
            return render_template('index.html', datas=page_datas, 
                                                webName=webName, 
                                                boardName=boardName,
                                                pagination=pagination)

    elif request.method == 'POST':
        webName = request.form.get('webName')
        results = queryData(webName)
        datas = results.fetchall()
        # review = ','.join([data[5] for data in datas])
        # review = (review)
        # segments = jieba.cut(review, cut_all=False)
        # stop_words = []
        # with open("./static/stopwords.txt",'r', encoding='utf-8-sig') as f:
        #     for line in f.readlines():
        #         line = line.strip()
        #         stop_words.append(line)
        # segments= [segment for segment in segments if segment not in stop_words]
        # word_freq = Counter(segments)
        # print(word_freq.most_common(20))


        
        
        # wordcloud = plt_WordCloud(word_freq)

        if datas != 'No Such Table':
            page_datas, pagination = make_pagination()
            # page, per_page, offset = get_page_args(page_parameter='page',
            #                                        per_page_parameter='per_page')
            # # per_page = 5
            # print(page, per_page, offset)
            # page_datas = fetch_data(datas, offset=offset, per_page=per_page)
            # pagination = Pagination(page=page, per_page=per_page, total=len(datas), css_framework='bootstrap4', record_name='review')
            
            return render_template('index.html', datas=page_datas, 
                                                webName=webName, 
                                                boardName=boardName,
                                                pagination=pagination)
        
        # else:
        #     datas = []
        #     return render_template('index.html', datas=datas, webName='No Such Table')
        
#登入
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    loginUser = request.form['user_id']
    if (loginUser in users) and (request.form['password'] == users[loginUser]['password']):
        user = User()
        user.id = loginUser
        login_user(user)
        # flash(f'{loginUser}！歡迎登入！')
        return redirect(url_for('home'))

    flash('登入失敗了...')
    return render_template('login.html')

#登出
@app.route('/logout')
def logout():
    loginUser = current_user.get_id()
    logout_user()
    flash(f'{loginUser}！歡迎下次再來！')
    return render_template('login.html')


#繪圖
@app.route('/visualization')
@login_required #指定該頁面一定要登入才能查看
def plot():
    boardName = queryBoardName()
    cnt = queryDataCnt(boardName)
    print(boardName)

    return render_template('visualization.html', cnt=cnt, boardName=boardName)

# pie chart資料
@app.route('/get_piechart_data')
def get_piechart_data():
    boardName = queryBoardName()
    cnt = queryDataCnt(boardName)
    pieChartData = []
    for index, item in enumerate(cnt):
        eachData = {}
        eachData['category'] = boardName[index]
        eachData['measure'] =  item
        pieChartData.append(eachData)
        print(pieChartData)

    return jsonify(pieChartData)

# bar chart資料
@app.route('/get_barchart_data')
def get_barchart_data():
    boardList = queryBoardName()
    [conndb,curr] = get_DB()
    cnt_labels = ['0-99', '100-199', '200-299', '300-399', '400-499', '500-599', '600-699', '700-799', '800-899', '900-999']
    barChartData = []
    for each in boardList:
        df = pd.read_sql(con=conndb, sql=f'select ArticleID,Comment_PushTag from {each}')
        df['cnt'] = df.Comment_PushTag.str.split('⟴').str.len()
        df['cnt_group'] = pd.cut(df.cnt, range(0, 1100,100), right=False, labels=cnt_labels)
        percent = (df.groupby('cnt_group').size().values/df.ArticleID.count())*100
        for index ,item in enumerate(percent):
            eachBarChart = {}
            eachBarChart['group'] = each
            eachBarChart['category'] = cnt_labels[index]
            eachBarChart['measure'] = round(item,1)
            barChartData.append(eachBarChart)

    
    return jsonify(barChartData)

if __name__=="__main__":
    app.run(debug=True, port="5000")
