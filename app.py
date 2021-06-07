from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/mypage')
def mypage():
    return render_template('mypage.html')


@app.route('/detail')
def detail():
    return render_template('pension_detail.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_list():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)

    return jsonify({'msg': 'list 연결되었습니다!'})


@app.route('/api/like', methods=['POST'])
def modify_list():
    sample_receive = request.form['sample_give']
    print(sample_receive)

    return jsonify({'msg': 'like 연결되었습니다!'})


@app.route('/api/delete', methods=['POST'])
def delete_list():
    sample_receive = request.form['sample_give']
    print(sample_receive)

    return jsonify({'msg': 'delete 연결되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
