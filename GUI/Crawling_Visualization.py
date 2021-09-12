import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import collections




# user agent를 입력해야 함
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.229 Whale/2.10.123.42 Safari/537.36"}


# 크롤링 과정, 기사는 최신순으로 정렬되어 있음
def firstlastscrape(query,page1 ,page2):
    office_list = []
    for first in range(page1, page2+1): # 첫 페이지부터 끝 페이지까지 돌리기
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={query}&sort=1&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:all,a:all&start={first*10-9}"

        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        
        news_area = soup.find_all("div", attrs={"class":"news_area"})
        for i in news_area:
            press = i.find("a", attrs={"class":"info press"}).stripped_strings
            
            for k in press:
                if k == "언론사 선정":
                    continue
                elif k != "언론사 선정":
                    m = k
            office_list.append(m)

    # 여기서부터는 시각화 과정
    dict1 = {}
    dict1 = collections.Counter(office_list)


    office_name = list(dict1)
    office_value = list(dict1.values())


    plt.pie(office_value, labels=office_name, autopct='%.1f%%')
    plt.legend(office_name, loc =(1.15, 0.0))
    plt.title(f"검색어 '{query}' 입력 시 언론사 비율 ")
    plt.show()
