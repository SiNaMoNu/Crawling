import requests
from bs4 import BeautifulSoup

filename = "keyword.txt"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"}

def create_soup(url) :
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def scrape_news_keyword(KEYWORD, PAGE):
    with open(filename, "w", encoding="utf8") as file:
        def scrape_1page(KEYWORD) :
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + KEYWORD + "&sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=1"  

            soup = create_soup(url)
            news_list = soup.find("ul", attrs={"class":"list_news"}).find_all("li", attrs={"class":"bx"})
            for index , news in enumerate(news_list) :
                title = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["title"]
                link = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["href"]
                
                press = []
                for press_pick in news.find("div", attrs={"class":"news_area"}).find("div", attrs={"class":"news_info"}).find("div", attrs={"class":"info_group"}).find("a", attrs={"class":"info press"}).stripped_strings :
                    press.append(press_pick)
                
                file.write("{}. {}".format(index+1, title)+"\n"+"   링크 : {}".format(link) + "\n" + "   언론사 : {}".format(press[0]) + "\n")
        
        if PAGE == 1 :
            scrape_1page(KEYWORD)
        elif PAGE > 1 :
            scrape_1page(KEYWORD)

            page_index = 10
                
            for i in range(1, PAGE) :
                url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + KEYWORD + "&sort=0&photo=0&field=0&pd=0&ds=&de=&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=" + str(i) + "1"
                
                soup = create_soup(url)
                news_list = soup.find("ul", attrs={"class":"list_news"}).find_all("li", attrs={"class":"bx"})
                for news in news_list :
                    title = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["title"]
                    link = news.find("div", attrs={"class":"news_area"}).find("a", attrs={"class":"news_tit"})["href"]
                    
                    press = []
                    for press_pick in news.find("div", attrs={"class":"news_area"}).find("div", attrs={"class":"news_info"}).find("div", attrs={"class":"info_group"}).find("a", attrs={"class":"info press"}).stripped_strings :
                        press.append(press_pick)

                    page_index = page_index + 1

                    file.write("{}. {}".format(page_index, title)+"\n"+"   링크 : {}".format(link) + "\n" + "   언론사 : {}".format(press[0]) + "\n")
