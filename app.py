from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, url_for

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

app = Flask(__name__)

# ----- DB 연결 : 펜션 정보 -----#
# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@3.34.124.31', 27017)

dbMopen = client.mopen
colPensionInfo = dbMopen.pensionInfo
colUser = dbMopen.mopenUser


# ----- route ----- #
@app.route('/')
def home():
	return render_template('index.html')


# -- Main: 펜션 목록 페이지 --#
@app.route('/main', methods=['GET'])
def main():
	token_receive = request.cookies.get('mytoken')
	location = request.args["location"]
	sorting = "1"

	try:
		sorting = request.args["sort"]
	except:
		sorting = "1"

	base = "name"
	asordes = -1

	print(location, type(sorting))

	if sorting == "1":
		base = "name"
		asordes = -1
	elif sorting == "2":
		base = "price"
		asordes = -1
	elif sorting == "3":
		base = "price"
		asordes = 1
	elif sorting == "4":
		base = "rate"
		asordes = -1
	elif sorting == "5":
		base = "rate"
		asordes = 1

	print(base, asordes)

	try:
		payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
		user_info = colUser.find_one({"id": payload['id']})

		if location == "전체":
			pensions = list(colPensionInfo.find({}).sort(base, asordes))
		else:
			pensions = list(colPensionInfo.find({'locationCategory': location}).sort(base, asordes))

		print("go to main")

		return render_template("main.html", pensions=pensions, nickname=user_info["id"])
	except jwt.ExpiredSignatureError:
		return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))

	except jwt.exceptions.DecodeError:
		return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))



# # API 역할을 하는 부분
# # 펜션 상세페이지
@app.route('/detail/<path:pension_id>', methods=['GET'])
def pension_detail(pension_id):
	pension = colPensionInfo.find_one({'_id': pension_id})
	# id 값으로 찾은 해당 펜션 정보(name, price, ...) 전부 전달
	return render_template("pension_detail.html", pension=pension)


@app.route('/mypage')
def mypage():
	token_receive = request.cookies.get('mytoken')

	try:
		payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
		user_info = colUser.find_one({"id": payload['id']})

		return render_template('mypage.html', nickname=user_info["id"])
	except jwt.ExpiredSignatureError:
		return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))

	except jwt.exceptions.DecodeError:
		return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))




@app.route('/register')
def register():
	return render_template('register.html')


@app.route('/login')
def login():
	msg = request.args.get("msg")
	return render_template('login.html', msg=msg)


#################################
##  로그인을 위한 API            ##
#################################


@app.route('/api/register', methods=['POST'])
def api_register():
	id_receive = request.form['id_give']
	pw_receive = request.form['pw_give']


	pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

	doc = {'id': id_receive, 'pw': pw_hash}
	colUser.insert_one(doc)


	return jsonify({'result': 'success'})

# 아이디 중복 확인 API
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
	username_receive = request.form['username_give']
	# bool=>값이 있느 문자열 리스트 등을 true, 값이 없는건 false
	exists = bool(colUser.find_one({"id": username_receive}))

	return jsonify({'result': 'success', 'exists': exists})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
	id_receive = request.form['id_give']
	pw_receive = request.form['pw_give']

	# 회원가입 때와 같은 방법으로 pw를 암호화합니다.
	pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

	# id, 암호화된pw을 가지고 해당 유저를 찾습니다.
	result = colUser.find_one({'id': id_receive, 'pw': pw_hash})

	# 찾으면 JWT 토큰을 만들어 발급합니다.
	if result is not None:
		payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
		token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

		# token을 줍니다.
		return jsonify({'result': 'success', 'token': token})
	# 찾지 못하면
	else:
		return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.

@app.route('/api/nick', methods=['GET'])
def api_valid():
	token_receive = request.cookies.get('mytoken')

	try:
		payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
		print(payload)

		userinfo = colUser.find_one({'id': payload['id']}, {'_id': 0})
		return jsonify({'result': 'success', 'nickname': userinfo['nick']})
	except jwt.ExpiredSignatureError:
		return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
	except jwt.exceptions.DecodeError:
		return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


if __name__ == '__main__':
	app.run('0.0.0.0', port=5000, debug=True)
