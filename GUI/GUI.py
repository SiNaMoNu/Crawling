import time
import tkinter.ttk as ttk
from tkinter import *
import os
import tkinter.messagebox as msgbox
import platform
import re
from Crawling_Theme import * 
from Crawling_Keyword import *
from Recrawling import *
from Crawling_Excel import *
from Crawling_Visualization import * 

root = Tk()
root.title("CRAWLING GUI") 
root.geometry("640x740+700+200")
root.resizable(False, False) # 너비, 높이 값 변경 불가 -> 창 크기 변경 불가, 최소화도 안됨

filename = "keyword.txt"

def fin():
    msgbox.showinfo("알림", "크롤링이 끝났습니다.")

def clear():
    mylist = root.pack_slaves()
    for i in mylist:
        i.destroy()

def initial_state():
    def change():
        time_label.config(text = "크롤링을 진행한 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    first_frame = LabelFrame(root, height=20)
    first_frame.pack(fill="x",  padx=10, pady=10)

    first_label = Label(first_frame, text="기능을 선택해주십시오", height=20, font=20)
    first_label.pack()
    initial_button()
    change()

def initial_button():
    btn_frame1 = LabelFrame(root, text="심화")
    btn_frame1.pack(side= "bottom", fill="x",padx=10, pady=1)

    btn1 = Button(btn_frame1, text="연관 검색어", height=5, width=20, command=btn1cmd)
    btn1.pack(side="left", padx=27)

    btn2 = Button(btn_frame1, text="엑셀로 저장", height=5, width=20, command=btn2cmd)
    btn2.pack(side="left", padx=27)

    btn2 = Button(btn_frame1, text="시각화", height=5, width=20, command=btn3cmd)
    btn2.pack(side="left", padx=27)

    btn_frame2 = LabelFrame(root, text="기초")
    btn_frame2.pack(side= "bottom", fill="x",padx=10, pady=1)

    btn1 = Button(btn_frame2, text="주제 크롤링", height=5, width=20, command=btn4cmd)
    btn1.pack(side="left", padx=27)

    btn2 = Button(btn_frame2, text="키워드 크롤링", height=5, width=20, command=btn5cmd)
    btn2.pack(side="right", padx=27)

def btn1cmd():
    clear()
    initial_button()
    time_label = Label(root, text = "현재 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    time_label.pack()
    def change():
        time_label.config(text = "크롤링을 진행한 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    
    txt_frame = Frame(root)
    txt_frame.pack(fill="x", padx=10, pady=10)

    scrollbar = Scrollbar(txt_frame)
    scrollbar.pack(side="right", fill="y")

    txt_file= Text(txt_frame, height=15, yscrollcommand=scrollbar.set)
    txt_file.pack(side="left",  expand=True, fill="both")
    scrollbar.config(command=txt_file.yview)
    txt_file.insert(END," \n\n\n\n 원하는 키워드를 입력하시고 크롤링 버튼을 눌러주시면 1차 크롤링이 진행됩니다. \n\n 크롤링된 기사들의 제목을 바탕으로 연관된 추천키워드를 제시합니다. \n\n 재크롤링 버튼을 눌러주시면 추천키워드로 재크롤링이 진행됩니다.")
    
    def open_file():
        if os.path.isfile(filename): # 파일 있으면 True, 없으면 False
             with open(filename, "r", encoding="utf8") as file:
                 txt_file.delete("1.0", END) # 텍스트 위젯 본문 삭제
                 txt_file.insert(END, file.read())
    Label(root, text="<연관 키워드 추출 후 재크롤링>").pack()

    input_frame = LabelFrame(root)
    input_frame.pack(fill="x", padx=7, pady=10)

    output_frame = Frame(root)
    output_frame.pack(fill="x", padx=7, pady=10)

    # 키워드 텍스트
    keyword_label = Label(input_frame, text="키워드", width=8)
    keyword_label.pack(side="left", padx=25, pady=5)

    keyword_txt = Entry(input_frame, width=30)
    keyword_txt.pack(side="left", padx=25, pady=5)
    keyword_txt.insert(0, "키워드를 입력하시오")

    # 크롤링 페이지 수
    page_label = Label(input_frame, text="크롤링 페이지 수")
    page_label.pack(side="left", padx=25, pady=5)

    page_values = [int(i) for i in range(1,16)] 

    page_combobox = ttk.Combobox(input_frame,width=5 , height=5, values=page_values,state="readonly")
    page_combobox.current(0)
    page_combobox.pack(side="left",padx=25, pady=5)

    # 추천 키워드
    keyword_label = Label(output_frame, text="추천 키워드", width=8)
    keyword_label.pack( padx=7, pady=5)

    rekeyword_txt = Entry(output_frame, width=40)
    rekeyword_txt.pack()
    
    def btncmd():
        KEYWORD = keyword_txt.get()
        PAGE = int(page_combobox.get())
        change()
        if __name__ == "__main__" :
            rescrape_news_keyword(KEYWORD, PAGE)   #뉴스 정보 가져오기
            fin()
        okt=Okt()
        word_dic={}
        f=open(filename, 'r', encoding="utf8")
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
        f = open("결과값.txt", 'w', encoding="utf8")
        f.write(a)
        f.close()
        with open("결과값.txt",'r', encoding="utf8") as f:
            text = f.read()
            b = re.compile('[가-힣]+')
            m = b.findall("alpha".join (text.split('\n')[0:2]))
            a=' '.join(m) 
            f.close()
        rekeyword_txt.insert(END, a)
        open_file() 


    def rebtncmd():
        KEYWORD = rekeyword_txt.get()
        PAGE = int(page_combobox.get())
        change()
        if __name__ == "__main__" :
            scrape_news_keyword(KEYWORD, PAGE)   #뉴스 정보 가져오기
            open_file()
            fin()

    # 크롤링 버튼
    btn_frame = Frame(root)
    btn_frame.pack(fill="x", padx=7, pady=10)

    #1차 크롤링 버튼
    btn1 = Button(btn_frame, text="크롤링",height=5, width=15, command=btncmd)
    btn1.pack(side="left", padx=27)

    #2차 크롤링 버튼
    btn2 = Button(btn_frame, text="재 크롤링",height=5, width=15, command=rebtncmd)
    btn2.pack(side="right", padx=27)

def btn2cmd():
    clear()
    initial_button()
    time_label = Label(root, text = "현재 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    time_label.pack()
    def change():
        time_label.config(text = "크롤링을 진행한 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    txt_frame = Frame(root)
    txt_frame.pack(fill="x", padx=10, pady=10)

    scrollbar = Scrollbar(txt_frame)
    scrollbar.pack(side="right", fill="y")

    txt_file= Text(txt_frame, height=15, yscrollcommand=scrollbar.set)
    txt_file.pack(side="left",  expand=True, fill="both")
    scrollbar.config(command=txt_file.yview)
    txt_file.insert(END, " \n\n\n\n\n\n 원하시는 날짜를 설정해주시고 크롤링 버튼을 눌러주세요. \n\n 해당 날짜의 모든 뉴스들을 주제별로 나누어 엑셀 파일로 저장합니다. ")    
    
    Label(root, text="<선택 날짜의 모든 뉴스 제목, 언론사, 링크 엑셀파일로 저장>").pack()

    input_frame = LabelFrame(root, text="엑셀로 저장")
    input_frame.pack(fill="x", padx=7, pady=5)

    # 크롤링 날짜
    year_values = [int(i) for i in range(1991,2022)] 
    month_values = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    day_values = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

    year_combobox = ttk.Combobox(input_frame,width=15 ,height=5, values=year_values,state="readonly")
    year_combobox.current(30)
    year_combobox.pack(side="left",padx=10, pady=5)

    year_label = Label(input_frame, text="년도", width=8)
    year_label.pack(side="left", padx=5, pady=5)

    month_combobox = ttk.Combobox(input_frame,width=15 , height=5, values=month_values,state="readonly")
    month_combobox.current(8)
    month_combobox.pack(side="left",padx=10, pady=5)

    month_label = Label(input_frame, text="월", width=8)
    month_label.pack(side="left", padx=5, pady=5)

    day_combobox = ttk.Combobox(input_frame,width=15 , height=5, values=day_values,state="readonly")
    day_combobox.current(0)
    day_combobox.pack(side="left",padx=10, pady=5)

    day_label = Label(input_frame, text="일", width=8)
    day_label.pack(side="left", padx=5, pady=5)

    frame_progress = LabelFrame(root, text="진행상황")
    frame_progress.pack( fill="x", padx=5, pady=5, ipady=5)

    p_var = DoubleVar()
    progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
    progress_bar.pack(fill="x", padx=5, pady=5)

    def btncmd():
        change()
        date = str(year_combobox.get()) + month_combobox.get() + day_combobox.get()
        if __name__ == "__main__" :
            scrape_news_excel(date) # 뉴스 정보 가져오기
            fin()
    # 크롤링 버튼
    btn_frame = Frame(root)
    btn_frame.pack(fill="x", padx=7, pady=10)
    
    #1차 크롤링 버튼
    btn1 = Button(btn_frame, text="크롤링",height=5, width=15, command=btncmd)
    btn1.pack()

def btn3cmd():
    clear()
    initial_button()
    time_label = Label(root, text = "현재 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    time_label.pack()
    def change():
        time_label.config(text = "크롤링을 진행한 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    txt_frame = Frame(root)
    txt_frame.pack(fill="x", padx=10, pady=10)

    scrollbar = Scrollbar(txt_frame)
    scrollbar.pack(side="right", fill="y")

    txt_file= Text(txt_frame, height=15, yscrollcommand=scrollbar.set)
    txt_file.pack(side="left",  expand=True, fill="both")
    scrollbar.config(command=txt_file.yview)
    txt_file.insert(END, " \n\n\n\n\n\n 키워드를 입력해주시고 크롤링을 시작할 페이지와 마지막 페이지를 설정해주세요. \n\n <크롤링 & 시각화> 버튼을 누르면 크롤링을 진행 후 언론사의 비율을 시각화해서 나타내줍니다.")    

    Label(root, text="< 크롤링 후 언론사별 시각화 >").pack()

    input_frame = LabelFrame(root, text="언론사 시각화")
    input_frame.pack(fill="x", padx=7, pady=5)

    # 키워드 텍스트
    keyword_label = Label(input_frame, text="키워드", width=8)
    keyword_label.pack(side="left", padx=7, pady=5)

    keyword_txt = Entry(input_frame, width=20)
    keyword_txt.pack(side="left")
    keyword_txt.insert(0, "키워드를 입력하시오")

    # 크롤링 페이지1
    page_label1 = Label(input_frame, text="크롤링 첫 페이지")
    page_label1.pack(side="left", padx=7, pady=5)

    page_values = [int(i) for i in range(1,16)] 

    page_combobox = ttk.Combobox(input_frame,width=2 , height=5, values=page_values,state="readonly")
    page_combobox.current(0)
    page_combobox.pack(side="left",padx=7, pady=5)

    # 크롤링 페이지2
    page_label2 = Label(input_frame, text="크롤링 마지막 페이지")
    page_label2.pack(side="left", padx=7, pady=5)

    page_values = [int(i) for i in range(1,16)] 

    page_combobox2 = ttk.Combobox(input_frame,width=2 , height=5, values=page_values,state="readonly")
    page_combobox2.current(0)
    page_combobox2.pack(side="left",padx=7, pady=5)

    def btncmd():
        query = keyword_txt.get()
        page1 = int(page_combobox.get()) 
        page2 = int(page_combobox2.get())
        if platform.system() == 'Windows':
            plt.rc('font', family='Malgun Gothic') 
            plt.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결

        elif platform.system() == 'Darwin': #맥
            plt.rc('font', family='AppleGothic') 
            plt.rcParams['axes.unicode_minus'] = False #한글 폰트 사용시 마이너스 폰트 깨짐 해결
        firstlastscrape(query,page1 ,page2)

    # 크롤링 버튼
    btn_frame = Frame(root)
    btn_frame.pack(fill="x", padx=7, pady=10)
    
    #1차 크롤링 버튼
    btn1 = Button(btn_frame, text="크롤링 & 시각화",height=5, width=15, command=btncmd)
    btn1.pack(pady= 70)

def btn4cmd():
    clear()
    initial_button()
    time_label = Label(root, text = "현재 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    time_label.pack()
    def change():
        time_label.config(text = "크롤링을 진행한 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    txt_frame = Frame(root)
    txt_frame.pack(fill="x", padx=10, pady=10)

    scrollbar = Scrollbar(txt_frame)
    scrollbar.pack(side="right", fill="y")

    txt_file= Text(txt_frame, height=15, yscrollcommand=scrollbar.set)
    txt_file.pack(side="left",  expand=True, fill="both")
    scrollbar.config(command=txt_file.yview)
    txt_file.insert(END, "\n\n\n\n\n 상위 주제를 선택하시고 <상위 주제 결정> 버튼을 눌러주세요. \n\n 추가된 하위 주제와 날짜를 설정하시고 아래에 크롤링 버튼을 눌러주세요 \n\n 해당하는 기사들을 크롤링해옵니다. \n\n 새로운 상위주제로 크롤링 하고 싶다면 <주제 크롤링> 버튼을 눌러주세요")    
    
    def open_file():
        if os.path.isfile(filename): # 파일 있으면 True, 없으면 False
             with open(filename, "r", encoding="utf8") as file:
                 txt_file.delete("1.0", END) # 텍스트 위젯 본문 삭제
                 txt_file.insert(END, file.read())
    
    Label(root, text="< 상위 주제와 하위 주제를 선택후 크롤링 >").pack()
    # 주제 크롤링 프레임
    sid_frame = LabelFrame(root, text="주제 크롤링")
    sid_frame.pack(fill="x", padx=7, pady=5)

    sid1_label = Label(sid_frame, text="상위주제", width=15)
    sid1_label.pack(side="left", padx=7, pady=5)

    sid1_values = ["정치", "경제", "사회", "생활/문화", "세계", "IT/과학"]
    정치_values = ["청와대", "국회/정당", "북한", "행정", "국방/외교", "정치 일반"]
    경제_values = ["금융", "증권", "산업/재계", "중기/벤처", "부동산", "글로벌 경제", "생활 경제", "경제 일반"]
    사회_values = ["사건사고", "교육", "노동", "언론", "환경", "인권/복지", "식품/의료", "지역", "인물", "사회 일반"]
    생활문화_values = ["건강정보", "자동차/시승기", "도로/교통", "여행/레저", "음식/맛집", "패션/뷰티", "공연/전시", "책", "종교", "날씨", "생활문화 일반"]
    세계_values = ["아시아/호주", "미국/중남미", "유럽", "중동/아프리카", "세계 일반"]
    IT과학_values = ["모바일", "인터넷/SNS", "통신/뉴미디어", "IT 일반", "보안/해킹", "컴퓨터", "게임/리뷰", "과학 일반"]

    sid1_combobox = ttk.Combobox(sid_frame,width=15 ,height=5, values=sid1_values,state="readonly")
    sid1_combobox.pack(side="left", padx=7, pady=5)
    
    def sidcmd():
        sid2_label = Label(sid_frame, text="하위주제", width=15)
        sid2_label.pack(side="left", padx=7, pady=5)
        if sid1_combobox.get() == "정치":
            VALUES = 정치_values
            sid2_combobox = ttk.Combobox(sid_frame,width=15 ,height=5, values=VALUES,state="readonly")
            sid2_combobox.pack(side="left", padx=7, pady=5)

        elif sid1_combobox.get() == "경제":
            VALUES = 경제_values
            sid2_combobox = ttk.Combobox(sid_frame,width=15 ,height=5, values=VALUES,state="readonly")
            sid2_combobox.pack(side="left", padx=7, pady=5)
        elif sid1_combobox.get() == "사회":
            VALUES = 사회_values
            sid2_combobox = ttk.Combobox(sid_frame,width=15 ,height=5, values=VALUES,state="readonly")
            sid2_combobox.pack(side="left", padx=7, pady=5)
        elif sid1_combobox.get() == "생활/문화":
            VALUES = 생활문화_values
            sid2_combobox = ttk.Combobox(sid_frame,width=15 ,height=5, values=VALUES,state="readonly")
            sid2_combobox.pack(side="left", padx=7, pady=5)
        elif sid1_combobox.get() == "세계":
            VALUES = 세계_values
            sid2_combobox = ttk.Combobox(sid_frame,width=15 ,height=5, values=VALUES,state="readonly")
            sid2_combobox.pack(side="left", padx=7, pady=5)
        elif sid1_combobox.get() == "IT/과학":
            VALUES = IT과학_values
            sid2_combobox = ttk.Combobox(sid_frame,width=15 ,height=5, values=VALUES,state="readonly")
            sid2_combobox.pack(side="left", padx=7, pady=5)
        
        def btncmd():
            sid1 = sid1_combobox.get()
            sid2 = sid2_combobox.get()
            date = str(year_combobox.get()) + month_combobox.get() + day_combobox.get()
            change()
            if __name__ == "__main__" :
                scrape_news(sid1, sid2, date)   #뉴스 정보 가져오기
                open_file()
                fin()
            
        input_frame = LabelFrame(root)
        input_frame.pack(fill="x", padx=7, pady=5)

        year_values = [int(i) for i in range(1991,2022)] 
        month_values = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        day_values = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]

        year_combobox = ttk.Combobox(input_frame,width=15 ,height=5, values=year_values,state="readonly")
        year_combobox.current(30)
        year_combobox.pack(side="left",padx=10, pady=5)

        year_label = Label(input_frame, text="년도", width=8)
        year_label.pack(side="left", padx=5, pady=5)

        month_combobox = ttk.Combobox(input_frame,width=15 , height=5, values=month_values,state="readonly")
        month_combobox.current(8)
        month_combobox.pack(side="left",padx=10, pady=5)

        month_label = Label(input_frame, text="월", width=8)
        month_label.pack(side="left", padx=5, pady=5)

        day_combobox = ttk.Combobox(input_frame,width=15 , height=5, values=day_values,state="readonly")
        day_combobox.current(0)
        day_combobox.pack(side="left",padx=10, pady=5)

        day_label = Label(input_frame, text="일", width=8)
        day_label.pack(side="left", padx=5, pady=5)

        # 크롤링 버튼
        btn_frame = Frame(root)
        btn_frame.pack(fill="x", padx=7, pady=10)
                
        #1차 크롤링 버튼
        btn1 = Button(btn_frame, text="크롤링",height=5, width=15, command=btncmd)
        btn1.pack()
        
    sid_btn = Button(sid_frame, text="상위 주제 결정", command=sidcmd)
    sid_btn.pack(side="left")

def btn5cmd():
    clear()
    initial_button()
    time_label = Label(root, text = "현재 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    time_label.pack()

    def change():
        time_label.config(text = "크롤링을 진행한 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
    txt_frame = Frame(root)
    txt_frame.pack(fill="x", padx=10, pady=10)

    scrollbar = Scrollbar(txt_frame)
    scrollbar.pack(side="right", fill="y")

    txt_file= Text(txt_frame, height=15, yscrollcommand=scrollbar.set)
    txt_file.pack(side="left",  expand=True, fill="both")
    scrollbar.config(command=txt_file.yview)
    txt_file.insert(END, " \n\n\n\n\n 크롤링을 원하는 키워드와 페이지 수를 입력해 주세요. \n\n 크롤링 버튼을 누르시면 위 텍스트 창에 기사 제목, 링크, 언론사가 출력됩니다. ")    
    
    def open_file():
        if os.path.isfile(filename): # 파일 있으면 True, 없으면 False
             with open(filename, "r", encoding="utf8") as file:
                 txt_file.delete("1.0", END) # 텍스트 위젯 본문 삭제
                 txt_file.insert(END, file.read())
    Label(root, text="< 키워드를 입력받고 크롤링 >").pack()

    input_frame = LabelFrame(root)
    input_frame.pack(fill="x", padx=7, pady=10)

    output_frame = Frame(root)
    output_frame.pack(fill="x", padx=7, pady=10)

    # 키워드 텍스트
    keyword_label = Label(input_frame, text="키워드", width=8)
    keyword_label.pack(side="left", padx=25, pady=5)

    keyword_txt = Entry(input_frame, width=30)
    keyword_txt.pack(side="left", padx=25, pady=5)
    keyword_txt.insert(0, "키워드를 입력하시오")

    # 크롤링 페이지 수
    page_label = Label(input_frame, text="크롤링 페이지 수")
    page_label.pack(side="left", padx=25, pady=5)

    page_values = [int(i) for i in range(1,16)] 

    page_combobox = ttk.Combobox(input_frame,width=5 , height=5, values=page_values,state="readonly")
    page_combobox.current(0)
    page_combobox.pack(side="left",padx=25, pady=5)

    def btncmd():
        KEYWORD = keyword_txt.get()
        PAGE = int(page_combobox.get())
        change()
        if __name__ == "__main__" :
            scrape_news_keyword(KEYWORD, PAGE)   #뉴스 정보 가져오기
            open_file()
            fin()
         
    # 크롤링 버튼
    btn_frame = Frame(root)
    btn_frame.pack(fill="x", padx=7, pady=10)
    
    #1차 크롤링 버튼
    btn1 = Button(btn_frame, text="크롤링",height=5, width=15, command=btncmd)
    btn1.pack()

# 현재 시간 레이블
time_label = Label(root, text = "현재 시각 {}.{}.{} {}:{}:{}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec))
time_label.pack()

# 처음 화면 구성 
initial_state()

root.mainloop()
