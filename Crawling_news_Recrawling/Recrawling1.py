import sys
import requests
from bs4 import BeautifulSoup
from konlpy.tag  import Okt



####################################################################################################################################


KEYWORD = input("키워드를 입력해주세요. : ")
PAGE = int(input("Crawiling을 진행할 page 수를 입력해주세요. : "))

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}

def create_soup(url) :
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

sys.stdout = open('크롤링.txt', 'w')

def scrape_1page() :
    url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="+ KEYWORD+"&sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1"  

    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"list_news"}).find_all("li", attrs={"class":"bx"})
    for index , news in enumerate(news_list) :
        title = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["title"]

        press = []
        for press_pick in news.find("div", attrs={"class":"news_area"}).find("div", attrs={"class":"news_info"}).find("div", attrs={"class":"info_group"}).find("a", attrs={"class":"info press"}).stripped_strings :
            press.append(press_pick)

        print(title)
      

def scrape_news() :
    print()

    if PAGE == 1 :
        scrape_1page() 
    elif PAGE > 1 :
        scrape_1page()

        page_index = 10

        for i in range(1, PAGE) :
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + KEYWORD + "&sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=" + str(i) + "1"
            
            soup = create_soup(url)
            news_list = soup.find("ul", attrs={"class":"list_news"}).find_all("li", attrs={"class":"bx"})   
            for index , news in enumerate(news_list) :
                title = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["title"]
            
                
                press = []
                for press_pick in news.find("div", attrs={"class":"news_area"}).find("div", attrs={"class":"news_info"}).find("div", attrs={"class":"info_group"}).find("a", attrs={"class":"info press"}).stripped_strings :
                    press.append(press_pick)

                page_index = page_index + 1

                print(title)
                

if __name__ == "__main__" :
    scrape_news() 

sys.stdout.close()


####################################################################################################################################


okt=Okt()
word_dic={}
f=open("크롤링.txt", 'r')
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
