import requests
from bs4 import BeautifulSoup
from tkinter import *
import tkinter.messagebox as msgbox

filename = "keyword.txt"

def info():
    msgbox.showinfo("알림", "크롤링을 시작합니다.")

def warn_sid1():
    msgbox.showwarning("경고", "잘못된 상위주제를 입력하셨습니다.")

def warn_sid2():
    msgbox.showwarning("경고", "잘못된 하위주제를 입력하셨습니다.")

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"}

def create_soup(url) :
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def create_paging_soup(paging_url) :
    res = requests.get(paging_url, headers=headers)
    res.raise_for_status()
    paging_soup = BeautifulSoup(res.text, "lxml")
    return paging_soup

def scrape_news(sid1, sid2, date) :

    if(sid1 == "정치") :
        sid1_code = str(100)
        
        if(sid2 == "청와대") :
            sid2_code = str(264)
        elif(sid2 == "국회/정당") :
            sid2_code = str(265)
        elif(sid2 == "북한") :
            sid2_code = str(268)
        elif(sid2 == "행정") :
            sid2_code = str(266)
        elif(sid2 == "국방/외교") :
            sid2_code = str(267)
        elif(sid2 == "정치 일반") :
            sid2_code = str(269)
        else :
            warn_sid2()
    elif(sid1 == "경제") :
        sid1_code = str(101)

        if(sid2 == "금융") :
            sid2_code = str(259)
        elif(sid2 == "증권") :
            sid2_code = str(258)
        elif(sid2 == "산업/재계") :
            sid2_code = str(261)
        elif(sid2 == "중기/벤처") :
            sid2_code = str(771)
        elif(sid2 == "부동산") :
            sid2_code = str(260)
        elif(sid2 == "글로벌 경제") :
            sid2_code = str(262)
        elif(sid2 == "생활 경제") :
            sid2_code = str(310)
        elif(sid2 == "경제 일반") :
            sid2_code = str(263)
        else :
            warn_sid2()
    elif(sid1 == "사회") :
        sid1_code = str(102)

        if(sid2 == "사건사고") :
            sid2_code = str(249)
        elif(sid2 == "교육") :
            sid2_code = str(250)
        elif(sid2 == "노동") :
            sid2_code = str(251)
        elif(sid2 == "언론") :
            sid2_code = str(254)
        elif(sid2 == "환경") :
            sid2_code = str(252)
        elif(sid2 == "인권/복지") :
            sid2_code = "59b"
        elif(sid2 == "식품/의료") :
            sid2_code = str(255)
        elif(sid2 == "지역") :
            sid2_code = str(256)
        elif(sid2 == "인물") :
            sid2_code = str(276)
        elif(sid2 == "사회 일반") :
            sid2_code = str(257)
        else :
            warn_sid2()
    elif(sid1 == "생활/문화") :
        sid1_code = str(103)

        if(sid2 == "건강정보") :
            sid2_code = str(241)
        elif(sid2 == "자동차/시승기") :
            sid2_code = str(239)
        elif(sid2 == "도로/교통") :
            sid2_code = str(240)
        elif(sid2 == "여행/레저") :
            sid2_code = str(237)
        elif(sid2 == "음식/맛집") :
            sid2_code = str(238)
        elif(sid2 == "패션/뷰티") :
            sid2_code = str(376)
        elif(sid2 == "공연/전시") :
            sid2_code = str(242)
        elif(sid2 == "책") :
            sid2_code = str(243)
        elif(sid2 == "종교") :
            sid2_code = str(244)
        elif(sid2 == "날씨") :
            sid2_code = str(248)
        elif(sid2 == "생활문화 일반") :
            sid2_code = str(245)
        else :
            warn_sid2()
    elif(sid1 == "세계") :
        sid1_code = str(104)

        if(sid2 == "아시아/호주") :
            sid2_code = str(231)
        elif(sid2 == "미국/중남미") :
            sid2_code = str(232)
        elif(sid2 == "유럽") :
            sid2_code = str(233)
        elif(sid2 == "중동/아프리카") :
            sid2_code = str(234)
        elif(sid2 == "세계 일반") :
            sid2_code = str(322)
        else :
            warn_sid2()
    elif(sid1 == "IT/과학") :
        sid1_code = str(105)

        if(sid2 == "모바일") :
            sid2_code = str(731)
        elif(sid2 == "인터넷/SNS") :
            sid2_code = str(226)
        elif(sid2 == "통신/뉴미디어") :
            sid2_code = str(227)
        elif(sid2 == "IT 일반") :
            sid2_code = str(230)
        elif(sid2 == "보안/해킹") :
            sid2_code = str(732)
        elif(sid2 == "컴퓨터") :
            sid2_code = str(283)
        elif(sid2 == "게임/리뷰") :
            sid2_code = str(229)
        elif(sid2 == "과학 일반") :
            sid2_code = str(228)
        else :
            warn_sid2()
    else :
            warn_sid1()

    def scrape() :
        page_index_1 = 0
        page_index_2 = 10
        with open(filename, "w", encoding="utf8") as file:
            for i in range(int(page_start), int(page_end)+1) :
                url = "https://news.naver.com/main/list.naver?mode=LS2D&sid2=" + sid2_code + "&sid1=" + sid1_code + "&mid=shm&date=" + date + "&page=" + str(i)
                i = i + 1 
                
                soup = create_soup(url)
                news_list1 = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li")
                for index, news1 in enumerate(news_list1) :
                    
                    a_img = 0
                    img = news1.find("img")
                    if img :
                        a_img = 1

                    a_tag1 = news1.find_all("a")[a_img]
                    title = a_tag1.get_text().strip()
                    link = a_tag1["href"]
                    press = news1.find("span", attrs={"class":"writing"}).get_text()

                    page_index_1 = page_index_1 + 1
                    file.write("{}. {}".format(page_index_1, title)+"\n"+"   링크 : {}".format(link) + "\n" + "   언론사 : {}".format(press) + "\n")

                page_index_1 = page_index_1 + index + 1

                if(soup.find("ul", attrs={"class":"type06"})) :
                    news_list2 = soup.find("ul", attrs={"class":"type06"}).find_all("li")
                    for index, news2 in enumerate(news_list2) :
                            a_img = 0
                            img = news2.find("img")
                            if img :
                                    a_img = 1

                            a_tag2 = news2.find_all("a")[a_img]
                            title = a_tag2.get_text().strip()
                            link = a_tag2["href"]
                            press = news2.find("span", attrs={"class":"writing"}).get_text()

                            page_index_2 = page_index_2 + 1

                            file.write("{}. {}".format(page_index_2, title)+"\n"+"   링크 : {}".format(link) + "\n" + "   언론사 : {}".format(press) + "\n")

                    page_index_2 = page_index_2 + index + 1

    page_number = 1
    paging_url = "https://news.naver.com/main/list.naver?mode=LS2D&sid2=" + sid2_code + "&sid1=" + sid1_code + "&mid=shm&date=" + date + "&page=" + str(page_number)
    paging_soup = create_paging_soup(paging_url)
    page_start = paging_soup.find("div", attrs={"class":"paging"}).find("strong").get_text()

    if(paging_soup.find("div", attrs={"class":"paging"}).find("a")) :
        page = paging_soup.find("div", attrs={"class":"paging"}).find_all("a")[-1]
        page_end = page.get_text()
    else :
        page_end = page_start

    if(page_end == "다음") :
        while(page_end == "다음") :
            page_number = page_number + 10
            paging_url = "https://news.naver.com/main/list.naver?mode=LS2D&sid2=" + sid2_code + "&sid1=" + sid1_code + "&mid=shm&date=" + date + "&page=" + str(page_number)
            paging_soup = create_paging_soup(paging_url)
            page = paging_soup.find("div", attrs={"class":"paging"}).find_all("a")[-1]
            page_end = page.get_text()

            if(page_end != "다음") :
                if(page_end == "이전") :
                    page_end = paging_soup.find("div", attrs={"class":"paging"}).find("strong").get_text()
                    scrape()
                else :
                    scrape()
    elif(page_end != "다음") :
        scrape()             
 
    print("내가 입력한 상위 주제 : {}   code : {}".format(sid1, sid1_code))
    print("내가 입력한 하위 주제 : {}   code : {}".format(sid2, sid2_code))
    print("내가 입력한 날짜 : {}".format(date))
    print("Crawling을 진행한 page 수 : {}".format(page_end))
