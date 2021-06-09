import uuid
import requests
from bs4 import BeautifulSoup
import uuid

from pymongo import MongoClient

#----- DB 연결 : 펜션 정보 -----#
client = MongoClient('localhost', 27017)
dbMopen = client.mopen
colPensionInfo = dbMopen.pensionInfo

#-----  bs4 parsing -----#
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.yanolja.com/pension', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# 펜션 리스트 가져오기
pensionList = soup.select('body > div#__next > div > div > main > section.SubhomeList_container__1WIAh > div > a')

# 기존 동일컬렉션 삭제 후 새 데이터 저장
def insertPensionInfo():
	colPensionInfo.drop()

	for pension in pensionList:
		pensionImgUrl = pension.select_one('div.ListItem_image__nEbnK')['style'].split('url(')[1].split(')')[0]
		pensionLocation = pension.select_one('div.ListItem_body__3V5K3 > div.ListItem_title__1-j89').text.split(' ')[0]
		pensionName = pension.select_one('div.ListItem_body__3V5K3 > div.ListItem_title__1-j89').text.split(' ')[1].split('(')[0]
		pensionNumScore = float(pension.select_one('div.PlaceListScore_container__2-JXJ > span.PlaceListScore_rating__3Glxf').text)
		pensionPrice = pension.select_one('div.ListItem_body__3V5K3 > div.ListItem_priceContainer__2Asmo').text.split('원')[0]

		dict = {
			'_id' : uuid.uuid4().hex,
			'img' : pensionImgUrl,
			'location' : pensionLocation,
			'name' : pensionName,
			'score' : pensionNumScore,
			'price' : pensionPrice,
		}

		colPensionInfo.insert_one(dict)

	print('저장 성공')

insertPensionInfo()


