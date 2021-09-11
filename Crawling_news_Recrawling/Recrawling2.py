
import requests
from bs4 import BeautifulSoup
import re
import time


with open("결과값.txt",'r') as f:
    text = f.read()
    b = re.compile('[가-힣]+')
    m = b.findall("alpha".join (text.split('\n')[0:2]))
    a=' '.join(m)
    f.close()


###################################################################################################################################


keyword = a

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
PAGE = int(input("Crawiling을 진행할 page 수를 입력해주세요. : "))

time = time.localtime()

def create_soup(url) :
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def scrape_1page() :
    url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + keyword + "&sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1"  

    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"list_news"}).find_all("li", attrs={"class":"bx"})
    for index , news in enumerate(news_list) :
        title = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["title"]
        link = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["href"]
        
        press = []
        for press_pick in news.find("div", attrs={"class":"news_area"}).find("div", attrs={"class":"news_info"}).find("div", attrs={"class":"info_group"}).find("a", attrs={"class":"info press"}).stripped_strings :
            press.append(press_pick)

        print("{}. {}".format(index+1, title))
        print("   링크 : {}".format(link))
        print("   언론사 : {}".format(press[0]))

def scrape_news() :
    print("[뉴스 정보]")
    print("Crawiling을 진행한 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    print()

    if PAGE == 1 :
        scrape_1page() 
    elif PAGE > 1 :
        scrape_1page()

        page_index = 10

        for i in range(1, PAGE) :
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + keyword + "&sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=" + str(i) + "1"
            
            soup = create_soup(url)
            news_list = soup.find("ul", attrs={"class":"list_news"}).find_all("li", attrs={"class":"bx"})   
            for index , news in enumerate(news_list) :
                title = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["title"]
                link = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["href"]
                
                press = []
                for press_pick in news.find("div", attrs={"class":"news_area"}).find("div", attrs={"class":"news_info"}).find("div", attrs={"class":"info_group"}).find("a", attrs={"class":"info press"}).stripped_strings :
                    press.append(press_pick)

                page_index = page_index + 1

                print("{}. {}".format(page_index, title))
                print("   링크 : {}".format(link))
                print("   언론사 : {}".format(press[0]))

if __name__ == "__main__" :
    scrape_news()   
