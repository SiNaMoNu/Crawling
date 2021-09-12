import requests
from bs4 import BeautifulSoup
import tkinter.ttk as ttk
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
# url을 통해 html이 비정상적으로 불러오는 것을 막으면서 제작자가 진행하는 Crawling 환경을 공개

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
        elif(sid2 == ("국회" or "정당" or "국회/정당")) :
            sid2_code = str(265)
        elif(sid2 == "북한") :
            sid2_code = str(268)
        elif(sid2 == "행정") :
            sid2_code = str(266)
        elif(sid2 == ("국방" or "외교" or "국방/외교")) :
            sid2_code = str(267)
        elif(sid2 == ("정치일반" or "정치 일반")) :
            sid2_code = str(269)
        else :
            warn_sid2()
    elif(sid1 == "경제") :
        sid1_code = str(101)

        if(sid2 == "금융") :
            sid2_code = str(259)
        elif(sid2 == "증권") :
            sid2_code = str(258)
        elif(sid2 == ("산업재계")) :
            sid2_code = str(261)
        elif(sid2 == ("중기벤처")) :
            sid2_code = str(771)
        elif(sid2 == "부동산") :
            sid2_code = str(260)
        elif(sid2 == ("글로벌경제")) :
            sid2_code = str(262)
        elif(sid2 == "생활경제") :
            sid2_code = str(310)
        elif(sid2 == ("경제일반")) :
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
        elif(sid2 == ("인권복지")) :
            sid2_code = "59b"
        elif(sid2 == ("식품의료")) :
            sid2_code = str(255)
        elif(sid2 == "지역") :
            sid2_code = str(256)
        elif(sid2 == "인물") :
            sid2_code = str(276)
        elif(sid2 == ("사회일반")) :
            sid2_code = str(257)
        else :
            warn_sid2()
    elif(sid1 == ("생활문화")) :
        sid1_code = str(103)

        if(sid2 == "건강정보") :
            sid2_code = str(241)
        elif(sid2 == ("자동차시승기")) :
            sid2_code = str(239)
        elif(sid2 == ("도로교통")) :
            sid2_code = str(240)
        elif(sid2 == ("여행레저")) :
            sid2_code = str(237)
        elif(sid2 == ("음식맛집")) :
            sid2_code = str(238)
        elif(sid2 == ("패션뷰티")) :
            sid2_code = str(376)
        elif(sid2 == ("공연전시")) :
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

        if(sid2 == ("아시아호주")) :
            sid2_code = str(231)
        elif(sid2 == ("미국중남미")) :
            sid2_code = str(232)
        elif(sid2 == "유럽") :
            sid2_code = str(233)
        elif(sid2 == ("중동아프리카")) :
            sid2_code = str(234)
        elif(sid2 == "세계 일반") :
            sid2_code = str(322)
        else :
            warn_sid2()
    elif(sid1 == ("IT과학")) :
        sid1_code = str(105)

        if(sid2 == "모바일") :
            sid2_code = str(731)
        elif(sid2 == ("인터넷SNS")) :
            sid2_code = str(226)
        elif(sid2 == ("통신뉴미디어")) :
            sid2_code = str(227)
        elif(sid2 == "IT 일반") :
            sid2_code = str(230)
        elif(sid2 == ("보안해킹")) :
            sid2_code = str(732)
        elif(sid2 == "컴퓨터") :
            sid2_code = str(283)
        elif(sid2 == ("게임리뷰")) :
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
                    img = news1.find("img") # 뉴스 정보를 담고 있는 "li" 태그에 이미지가 있을 경우 "img" 태그는 하나만 존재하므로 다음과 같이 작성했다. 
                    if img :
                        a_img = 1   # img 태그가 있으면 1번째 a 태그의 정보를 사용

                    a_tag1 = news1.find_all("a")[a_img]
                    title = a_tag1.get_text().strip()   # strip() : 불필요한 공백 제거
                    link = a_tag1["href"]
                    press = news1.find("span", attrs={"class":"writing"}).get_text()

                    page_index_1 = page_index_1 + 1
                    file.write("{}. {}".format(page_index_1, title)+"\n"+"   링크 : {}".format(link) + "\n" + "   언론사 : {}".format(press) + "\n")

                page_index_1 = page_index_1 + index + 1     # 2page 이상 스크랩할 경우 이후 출력하는 index가 1부터 시작하지 않고 이어갈 수 있게함.

                if(soup.find("ul", attrs={"class":"type06"})) :     # 해당 페이지의 기사가 10개 이하일 경우 "class":"type06" 가 없기 때문에 if문이 없다면 에러코드가 뜬다. 이를 없애기 위해 if문으로 "class":"type06" 가 있는지 확인한다.
                    news_list2 = soup.find("ul", attrs={"class":"type06"}).find_all("li")       # 해당 페이지가 기사가 11개 이상일 경우 기사들의 정보가 "class":"type06_headline"이 아닌 "class":"type06"에 있다.
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

                    page_index_2 = page_index_2 + index + 1     # 182 line 과 동일

    page_number = 1
    paging_url = "https://news.naver.com/main/list.naver?mode=LS2D&sid2=" + sid2_code + "&sid1=" + sid1_code + "&mid=shm&date=" + date + "&page=" + str(page_number)
    paging_soup = create_paging_soup(paging_url)
    page_start = paging_soup.find("div", attrs={"class":"paging"}).find("strong").get_text()    # 해당 기사의 시작 페이지를 찾는다. 당연하게 1page 부터 시작하겠지만, 상식을 벗어나는 일이 발생하는 것을 방지하기 위해 시작 페이지를 확인한다. 

    if(paging_soup.find("div", attrs={"class":"paging"}).find("a")) :       # 해당 기사 페이지가 1page만 있는 경우 a 태그가 없기 때문에 오류가 뜨면서 page_end 값을 지정할 수 없다. 해당 기사가 1page만 있는지 확인한다.
        page = paging_soup.find("div", attrs={"class":"paging"}).find_all("a")[-1]      # a 태그의 마지막 값
        page_end = page.get_text()
    else :
        page_end = page_start

    if(page_end == "다음") :        # page_end 값을 지정하는 url이 1page를 기준으로 되어 있다. 해당 기사 페이지가 11page 이상인 경우 page_end에 할당되는 값은 '다음'이다. while문을 통해 page_end가 '다음'이 아닌 마지막 페이지를 할당받을 때까지 반복한다. 
        while(page_end == "다음") :
            page_number = page_number + 10      # 1page, 11page, 21page ... 에서 page_end가 '다음' 값을 할당받는지 확인한다.
            paging_url = "https://news.naver.com/main/list.naver?mode=LS2D&sid2=" + sid2_code + "&sid1=" + sid1_code + "&mid=shm&date=" + date + "&page=" + str(page_number)
            paging_soup = create_paging_soup(paging_url)
            page = paging_soup.find("div", attrs={"class":"paging"}).find_all("a")[-1]
            page_end = page.get_text()

            if(page_end != "다음") :
                if(page_end == "이전") :        # 11page 이상인 기사에서 마지막 페이지의 일의 자리가 1인 경우 a 태그가 없어 page_end에 '이전' 값을 할당한다. 이 경우 strong 태그의 값을 page_end에 할당하여 해결한다.
                    page_end = paging_soup.find("div", attrs={"class":"paging"}).find("strong").get_text()
                    scrape()        # 오류를 수정하다보니 scrape을 위한 긴 코드가 여러번 반복되어 함수로 처리하였다. (158 line) 
                else :
                    scrape()
    elif(page_end != "다음") :
        scrape()
                
 

    print("내가 입력한 상위 주제 : {}   code : {}".format(sid1, sid1_code))
    print("내가 입력한 하위 주제 : {}   code : {}".format(sid2, sid2_code))
    print("내가 입력한 날짜 : {}".format(date))
    print("Crawling을 진행한 page 수 : {}".format(page_end))









