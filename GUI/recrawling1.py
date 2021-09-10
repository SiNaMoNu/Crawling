from konlpy.tag  import Okt
import requests
from bs4 import BeautifulSoup

filename = "keyword.txt"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"}

def create_soup(url) :
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def create_soup(url) :
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup    

def rescrape_news_keyword(KEYWORD, PAGE):
    with open(filename, "w", encoding="utf8") as file:
        if PAGE == 1 :
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + KEYWORD + "&sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1"  

            soup = create_soup(url)
            news_list = soup.find("ul", attrs={"class":"list_news"}).find_all("li", attrs={"class":"bx"})
            with open(filename, "w", encoding="utf8") as file:
                for index , news in enumerate(news_list) :
                    title = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["title"]

                    file.write("{}".format(title) + "\n")
        elif PAGE > 1 :
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + KEYWORD + "&sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1"  

            soup = create_soup(url)
            news_list = soup.find("ul", attrs={"class":"list_news"}).find_all("li", attrs={"class":"bx"})
            for index , news in enumerate(news_list) :
                title = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["title"]

                file.write("{}".format(title) + "\n")
                
            for i in range(1, PAGE) :
                soup = create_soup(url)
                news_list = soup.find("ul", attrs={"class":"list_news"}).find_all("li", attrs={"class":"bx"})   # 관련 기사가 있을 경우 <li class="sub_bx"> 가 존재하므로 attrs={"class":"bx"} 를 추가하여 메인 기사의 정보가 담겨있는 li 태그만 찾도록 하였다.
                for index , news in enumerate(news_list) :
                    title = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["title"]

                    file.write("{}".format(title) + "\n")
                
def morpheme():
    okt=Okt()
    word_dic={}
    f=open(filename, 'r')
    g=''
    while True:
        line = f.readline()
        line = line.replace(line.split(' ')[0]+' ','')
        if not line: break
        g+=line
    f.close()

    g = okt.pos(g)
    for taeso, pumsa in g:
        if pumsa == "Noun":
            if not (taeso in word_dic):
                word_dic[taeso] = 0
            word_dic[taeso]+=1

    a, number = '', 1
    keys = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)
    for word, count in keys[:50]:
        a += "{0}. {1}({2})\n".format(number,word, count)
        number+=1
    f = open("결과값.txt", 'w')
    f.write(a)
    f.close()
