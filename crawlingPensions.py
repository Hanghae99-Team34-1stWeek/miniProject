# ----- 스크래핑 : selenium -----#
from urllib.parse import urlencode, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
import time

# ----- 스크래핑 : requests, BeautifulSoup -----#
import requests
from bs4 import BeautifulSoup

# ----- DB : 연결 및 저장 -----#
from pymongo import MongoClient
import uuid

client = MongoClient('localhost', 27017)
dbMopen = client.mopen
colPensionInfo = dbMopen.pensionInfo
colUser = dbMopen.mopenUser

# ----- init selenium -----#
# cd = ChromeDriverManager().install()  # install chrome driver if there's not right chrome update model
# driver = webdriver.Chrome(cd)  # for chrome driver

print('[Connecting...]')
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(5)

# ----- 지역별 url -----#
urlSeoul = "https://www.yanolja.com/pension/r-900270?advert=AREA&region=900270"
urlBusan = "https://www.yanolja.com/pension/r-900272?advert=AREA&region=900272"
urlUlsan = "https://www.yanolja.com/pension/r-900575?advert=AREA&region=900575"
urlIncheon = "https://www.yanolja.com/pension/r-900594?advert=AREA&region=900594"
urlGg = "https://www.yanolja.com/pension/r-900591/pkey-pension?advert=AREA&rentType=1&stayType=1&region=900591"
urlGw = "https://www.yanolja.com/pension/r-900592/pkey-pension?advert=AREA&rentType=1&stayType=1&region=900592"
urlCb = "https://www.yanolja.com/pension/r-900596/pkey-pension?advert=AREA&rentType=1&stayType=1&region=900596"
urlCn = "https://www.yanolja.com/pension/r-900595/pkey-pension?advert=AREA&rentType=1&stayType=1&region=900595"
urlGb = "https://www.yanolja.com/pension/r-900598/pkey-pension?advert=AREA&rentType=1&stayType=1&region=900598"
urlGn = "https://www.yanolja.com/pension/r-910224/pkey-pension?advert=AREA&rentType=1&stayType=1&region=910224"
urlJb = "https://www.yanolja.com/pension/r-900600/pkey-pension?advert=AREA&rentType=1&stayType=1&region=900600"
urlJn = "https://www.yanolja.com/pension/r-900599/pkey-pension?advert=AREA&rentType=1&stayType=1&region=900599"
urlJj = "https://www.yanolja.com/pension/r-900593/pkey-pension?advert=AREA&rentType=1&stayType=1&region=900593"


# ----- 각 지역별 리스트 가져오기 -----#
# 가격 콤마 제거
def remove_comma(x):
    return x.replace(',', '')


# ----- insertPensionInfo('가져올 url', '지역명') -----#
def insertPensionInfo(arg_UrlToGet, arg_LocationCategory):
    driver.get(arg_UrlToGet)

    for i in range(1, 50):
        name = driver.find_element_by_css_selector(
            f'#__next > div.StyleComponent_container__1jS9A.list_listContainer__2kL99.list_bottomPadding__xvWzu > section.PlaceListBody_placeListBodyContainer__1u70R > div:nth-child(2) > div > div:nth-child({i}) > a > div.PlaceListItemBanner_contents__1oW8G > div:nth-child(1) > div.PlaceListTitle_container__qe7XH > strong')
        pensionLocation = name.text.split(' ')[0]
        pensionName = name.text.split(' ')[1].split('(')[0]
        rate = driver.find_element_by_css_selector(
            f'#__next > div.StyleComponent_container__1jS9A.list_listContainer__2kL99.list_bottomPadding__xvWzu > section.PlaceListBody_placeListBodyContainer__1u70R > div:nth-child(2) > div > div:nth-child({i}) > a > div.PlaceListItemBanner_contents__1oW8G > div:nth-child(1) > div.PlaceListScore_container__2-JXJ.PlaceListItemBanner_score__3HHN5 > span')
        pensionNumRate = rate.text
        price = driver.find_element_by_css_selector(
            f'#__next > div.StyleComponent_container__1jS9A.list_listContainer__2kL99.list_bottomPadding__xvWzu > section.PlaceListBody_placeListBodyContainer__1u70R > div:nth-child(2) > div > div:nth-child({i}) > a > div.PlaceListItemBanner_contents__1oW8G > div.PlaceListItemBanner_prices__5aywq > div > div.PlacePriceInfo_priceInfo__H0DLi > span.PlacePriceInfo_salePrice__28VZD').text
        if price == '예약마감':
            pensionPrice = 89000
        else:
            price = price.split('원')[0]
            pensionPrice = int(remove_comma(price))
        img = driver.find_element_by_css_selector(
            f'#__next > div.StyleComponent_container__1jS9A.list_listContainer__2kL99.list_bottomPadding__xvWzu > section.PlaceListBody_placeListBodyContainer__1u70R > div:nth-child(2) > div > div:nth-child({i}) > a > div.PlaceListItemBanner_image__1-YJA > div.PlaceListImage_container__t-mGF > div.PlaceListImage_imageSmall__1NuLT')
        pensionImgUrl = img.get_attribute("style").split('"')[1]

        print(arg_LocationCategory, ":", pensionLocation, ":", pensionName, ":", pensionNumRate, ":", pensionPrice, ":",
              pensionImgUrl)

        dict = {
            '_id': uuid.uuid4().hex,
            'img': pensionImgUrl,
            'location': pensionLocation,
            'locationCategory': arg_LocationCategory,
            'name': pensionName,
            'rate': pensionNumRate,
            'price': pensionPrice,
        }

        colPensionInfo.insert_one(dict)

    print('저장 성공')

    time.sleep(3)

    driver.close()
    driver.quit()


# ----- 충북 -----#
def insertPensionInfo_Cb(arg_UrlToGet, arg_LocationCategory):
    driver.get(arg_UrlToGet)

    for i in range(1, 50):
        name = driver.find_element_by_css_selector(
            f'#__next > div.StyleComponent_container__1jS9A.list_listContainer__2kL99.list_bottomPadding__xvWzu > section.PlaceListBody_placeListBodyContainer__1u70R > div:nth-child(2) > div > div:nth-child({i}) > a > div > div.PlaceListItemText_contents__2GR73.place-content.PlaceListItemText_singlePrice__1aj9I > div.PlaceListTitle_container__qe7XH > strong')
        pensionLocation = name.text.split(' ')[0]
        pensionName = name.text.split(' ')[1].split('(')[0]
        rate = driver.find_element_by_css_selector(
            f'#__next > div.StyleComponent_container__1jS9A.list_listContainer__2kL99.list_bottomPadding__xvWzu > section.PlaceListBody_placeListBodyContainer__1u70R > div:nth-child(2) > div > div:nth-child({i}) > a > div > div.PlaceListItemText_contents__2GR73.place-content.PlaceListItemText_singlePrice__1aj9I > div.PlaceListItemText_extraInfos__3Bp2B> div > span')
        pensionNumRate = rate.text
        price = driver.find_element_by_css_selector(
            f'#__next > div.StyleComponent_container__1jS9A.list_listContainer__2kL99.list_bottomPadding__xvWzu > section.PlaceListBody_placeListBodyContainer__1u70R > div:nth-child(2) > div > div:nth-child({i}) > a > div.PlaceListItemBanner_contents__1oW8G > div.PlaceListItemBanner_prices__5aywq > div > div.PlacePriceInfo_priceInfo__H0DLi > span.PlacePriceInfo_salePrice__28VZD')
        if price.text == '예약마감':
            pensionPrice = 89000
        else:
            price = price.text.strip('"')
            pensionPrice = int(remove_comma(price))
        img = driver.find_element_by_css_selector(
            f'#__next > div.StyleComponent_container__1jS9A.list_listContainer__2kL99.list_bottomPadding__xvWzu > section.PlaceListBody_placeListBodyContainer__1u70R > div:nth-child(2) > div > div:nth-child({i}) > a > div > div.PlaceListItemText_image__2mlnK.place-image > div.PlaceListImage_container__t-mGF > div.PlaceListImage_imageText__2XEMn')
        pensionImgUrl = img.get_attribute("style").split('"')[1]

        print(arg_LocationCategory, ":", pensionLocation, ":", pensionName, ":", pensionNumRate, ":", pensionPrice, ":",
              pensionImgUrl)

        dict = {
            '_id': uuid.uuid4().hex,
            'img': pensionImgUrl,
            'location': pensionLocation,
            'locationCategory': arg_LocationCategory,
            'name': pensionName,
            'rate': pensionNumRate,
            'price': pensionPrice,
        }

        colPensionInfo.insert_one(dict)

    print('저장 성공')

    time.sleep(3)

    driver.close()
    driver.quit()


# 기존 db내 데이터 있을 경우 삭제
# colPensionInfo.drop()

# ----- 작동 잘 됨 -----#
# ----- 한 줄 씩 작동시키면 됩니다! -----#
# insertPensionInfo(urlGg, '경기')
# insertPensionInfo(urlGw, '강원')
# insertPensionInfo(urlCn, '충남')
# insertPensionInfo(urlGb, '경북')
# insertPensionInfo(urlGn, '경남')
# insertPensionInfo(urlJb, '전북')
# insertPensionInfo(urlJn, '전남')
insertPensionInfo(urlJj, '제주')
# insertPensionInfo_Cb(urlCb, '충북')
