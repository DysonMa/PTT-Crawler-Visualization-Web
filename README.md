# PTT Crawler Visualization Web

* 這是一個用 Flask, Bootstrap, SQLite, D3.js 架設並部署在 Azure 的 Ptt 爬蟲資料視覺化網站。
* DB資料來源: [PTT-Crawler爬蟲程式碼](https://github.com/DysonMa/PTT-Crawler)

![home](./static/img/3.PNG)
![demo](./static/img/4.gif)

## 功能:
* 使用者登入功能(Flask-login)
* 響應式(RWD)網站設計
* 目前DB共有五個板名，HatePolitics(政黑板)、Beauty(表特板)、Soft_Job(軟體板)、NBA、Stock(股票板)、Tech_Job(科技板)
* 選擇其中一個板名，按下查詢，從後台SQLite資料庫查詢
* 列出各個欄位，ex: 編號、文章ID、推噓數量、作者、標題、日期、內文...
* 換頁功能與跳轉頁碼(Flask-Paginate)
* 將各板的推噓數量級距做資料視覺化(D3.js)
* 部署到 Azure web services (目前因金錢原因取消部署)
* Jieba斷詞與文字雲(wordcloud)顯示 (因速度效能遇到障礙而取消)

## 使用技術與工具
* 前端:
    - HTML5
    - CSS3
    - jquery
    - [Bootstrap(4.5.2)](https://getbootstrap.com/)
* 後端:
    - [Flask](https://flask.palletsprojects.com/en/1.1.x/)
        - Flask_paginate
        - Flask-login
        - login_required
        - jieba斷詞
        - wordcloud文字雲
* 資料庫:
    - [SQLite](https://www.sqlite.org/index.html)
* 部署:
    - [Azure](https://azure.microsoft.com/zh-tw/)

## 演示步驟與展示圖片

* 尚未有帳號密碼，所以導至登入頁面
<img src='./static/img/1.PNG' width='750px'>

* 登入成功後，進到首頁
<img src='./static/img/2.PNG' width='750px'>

* 選擇板名，並按下搜尋，列出DB爬蟲的資料
<img src='./static/img/3.PNG' width='750px'>

* 點選上方導覽列的 `DATA VISUALIZATION`，看到各板推噓數量的級距分配圖
<img src='./static/img/4.gif' width='750px'>

