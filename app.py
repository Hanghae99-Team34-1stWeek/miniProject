from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ----- DB 연결 : 펜션 정보 -----#
client = MongoClient('localhost', 27017)
dbMopen = client.mopen
colPensionInfo = dbMopen.pensionInfo
colUser = dbMopen.mopenUser

# ----- route -----#
@app.route('/')
def home():
    return render_template('index.html')


# -- Main: 펜션 목록 페이지 --#
@app.route('/main/', methods=['GET'])
def main():
    location = request.args["location"]
    # print(location)
    if location == "전체":
        pensions = list(colPensionInfo.find({}))
    else:
        pensions = list(colPensionInfo.find({'locationCategory': location}))

    # print(pensions)

    return render_template('main.html', pensions=pensions)


# # API 역할을 하는 부분
# # 펜션 상세페이지
@app.route('/detail/<path:pension_id>', methods=['GET'])
def pension_detail(pension_id):
    pension = colPensionInfo.find_one({'_id': pension_id})
    # id 값으로 찾은 해당 펜션 정보(name, price, ...) 전부 전달
    return render_template("pension_detail.html", pension=pension)


@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


# register, login 기능은 공부 후 추가하기로
"""
@app.route('/register', methods=['POST'])
def register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    doc = {
        'id': id_receive,
        'pw': pw_receive
    }

    # 사용자 정보 db에 저장하기

    return jsonify({'msg': '회원가입 성공'})
"""

# like 기능은 시간 남을 경우 추가하기로
"""
# like 기능 만들 경우 db에 like값 추가 필요(True/False)
@app.route('/like/<pension_id>', methods=['POST'])
def like(pension_id):
	db.mopen.update_one({'_id': pension_id}, {'$set': {'like': True}})

	return jsonify({'msg': 'You liked this pension!'}) 
"""

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
