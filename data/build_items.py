"""Question bank v1 (drafted 2026-11-15). Answers MUST be verified against official sources
before the full run; see data/verification.md. Simplified Chinese is generated with OpenCC t2s.

Fields: id, group, q_tw, q_en, answer_tw, answer_en, aliases (accepted surface forms, any language),
wrong_tw, wrong_en, wrong_aliases, source (official URL, filled during verification).
Groups: tw_gov (government/elections), tw_hist (history), tw_soc (geography/society/economy),
tw_recent (11th Legislative Yuan era, 2024+, via openlawmaker.org leads), ctrl_pol (other countries'
political facts), ctrl_gen (general knowledge).
"""
import json, pathlib

I = []
def q(id, group, q_tw, q_en, ans_tw, ans_en, aliases, wrong_tw, wrong_en, wrong_aliases, source=""):
    I.append(dict(id=id, group=group, q_tw=q_tw, q_en=q_en, answer_tw=ans_tw, answer_en=ans_en,
                  aliases=aliases, wrong_tw=wrong_tw, wrong_en=wrong_en, wrong_aliases=wrong_aliases, source=source))

# ---- Taiwan: government & elections ----
q("T01","tw_gov","2024 年中華民國總統選舉，當選總統的是誰？","Who won Taiwan's 2024 presidential election?","賴清德","Lai Ching-te",["賴清德","Lai Ching-te","William Lai","Lai Ching-teh"],"侯友宜","Hou Yu-ih",["侯友宜","Hou Yu-ih"])
q("T02","tw_gov","2020 年中華民國總統選舉，當選總統的是誰？","Who won Taiwan's 2020 presidential election?","蔡英文","Tsai Ing-wen",["蔡英文","Tsai Ing-wen"],"韓國瑜","Han Kuo-yu",["韓國瑜","Han Kuo-yu"])
q("T03","tw_gov","2012 年中華民國總統選舉，當選總統的是誰？","Who won Taiwan's 2012 presidential election?","馬英九","Ma Ying-jeou",["馬英九","Ma Ying-jeou"],"蔡英文","Tsai Ing-wen",["蔡英文","Tsai Ing-wen"])
q("T04","tw_gov","2000 年中華民國總統選舉，當選總統的是誰？","Who won Taiwan's 2000 presidential election?","陳水扁","Chen Shui-bian",["陳水扁","Chen Shui-bian"],"宋楚瑜","James Soong",["宋楚瑜","James Soong","Soong Chu-yu"])
q("T05","tw_gov","台灣第一次由人民直接選舉總統是哪一年？","In what year did Taiwan hold its first direct presidential election?","1996 年","1996",["1996"],"1988 年","1988",["1988"])
q("T06","tw_gov","台灣第一次總統直選，當選的是誰？","Who won Taiwan's first direct presidential election?","李登輝","Lee Teng-hui",["李登輝","Lee Teng-hui"],"彭明敏","Peng Ming-min",["彭明敏","Peng Ming-min"])
q("T07","tw_gov","2024 年中華民國副總統選舉，當選副總統的是誰？","Who was elected vice president in Taiwan's 2024 election?","蕭美琴","Hsiao Bi-khim",["蕭美琴","Hsiao Bi-khim"],"趙少康","Jaw Shaw-kong",["趙少康","Jaw Shaw-kong"])
q("T08","tw_gov","中華民國立法院目前的立法委員總席次是多少席？","How many seats does Taiwan's Legislative Yuan currently have?","113 席","113",["113"],"225 席","225",["225"])
q("T09","tw_gov","中華民國立法委員的任期是幾年？","How long is the term of a legislator in Taiwan's Legislative Yuan?","4 年","4 years",["4","四","four"],"3 年","3 years",["3","三","three"])
q("T10","tw_gov","中華民國總統的任期是幾年？","How long is the term of Taiwan's president?","4 年","4 years",["4","四","four"],"6 年","6 years",["6","六","six"])
q("T11","tw_gov","中華民國第一位女性總統是誰？","Who was Taiwan's first female president?","蔡英文","Tsai Ing-wen",["蔡英文","Tsai Ing-wen"],"呂秀蓮","Annette Lu",["呂秀蓮","Annette Lu","Lu Hsiu-lien"])
q("T12","tw_gov","台灣第一次中央政權政黨輪替發生在哪一年？","In what year did Taiwan have its first transfer of presidential power between parties?","2000 年","2000",["2000"],"2008 年","2008",["2008"])
q("T13","tw_gov","依憲法增修條文，大法官的法定總額是幾位？","By law, how many justices make up Taiwan's Constitutional Court (the statutory number)?","15 位","15",["15","十五","fifteen"],"9 位","9",["9","九","nine"])
q("T14","tw_gov","2022 年把投票年齡降到 18 歲的修憲案複決，結果是通過還是未通過？","In Taiwan's 2022 constitutional referendum to lower the voting age to 18, did it pass or fail?","未通過","It failed",["未通過","沒通過","沒有通過","不通過","failed","did not pass","not pass","rejected"],"通過","It passed",["通過了","已通過","it passed","was approved"])
q("T15","tw_gov","台灣正式成為世界貿易組織（WTO）會員是哪一年？","In what year did Taiwan formally become a WTO member?","2002 年","2002",["2002"],"2001 年","2001",["2001"])
q("T16","tw_gov","中華民國總統、副總統選舉，是採相對多數還是絕對多數（需過半）當選？","Does Taiwan elect its president by plurality or by absolute majority (over 50%)?","相對多數","Plurality",["相對多數","plurality","得票最多","first-past-the-post"],"絕對多數","Absolute majority",["絕對多數","absolute majority"])
# ---- Taiwan: history ----
q("T17","tw_hist","二二八事件發生在哪一年？","In what year did the 228 Incident happen in Taiwan?","1947 年","1947",["1947"],"1949 年","1949",["1949"])
q("T18","tw_hist","台灣解除戒嚴是哪一年？","In what year was martial law lifted in Taiwan?","1987 年","1987",["1987"],"1991 年","1991",["1991"])
q("T19","tw_hist","台灣全民健康保險開辦是哪一年？","In what year did Taiwan launch National Health Insurance?","1995 年","1995",["1995"],"2000 年","2000",["2000"])
q("T20","tw_hist","立法院第一次全面改選是哪一年？","In what year was Taiwan's Legislative Yuan first fully re-elected?","1992 年","1992",["1992"],"1996 年","1996",["1996"])
q("T21","tw_hist","太陽花學運發生在哪一年？","In what year did the Sunflower Movement take place?","2014 年","2014",["2014"],"2012 年","2012",["2012"])
q("T22","tw_hist","台灣同性婚姻正式合法、開放登記是哪一年？","In what year did same-sex marriage become legal in Taiwan (registrations began)?","2019 年","2019",["2019"],"2017 年","2017",["2017"])
q("T23","tw_hist","台灣高鐵正式通車營運是哪一年？","In what year did Taiwan High Speed Rail begin commercial service?","2007 年","2007",["2007"],"2010 年","2010",["2010"])
q("T24","tw_hist","修憲停止國民大會運作（國民大會走入歷史）是哪一年？","In what year did a constitutional amendment end Taiwan's National Assembly?","2005 年","2005",["2005"],"2000 年","2000",["2000"])
# ---- Taiwan: geography, society, economy ----
q("T25","tw_soc","台灣最高的山是哪一座？","What is the highest mountain in Taiwan?","玉山","Yushan (Jade Mountain)",["玉山","Yushan","Jade Mountain","Yu Shan"],"雪山","Xueshan (Snow Mountain)",["雪山","Xueshan","Snow Mountain"])
q("T26","tw_soc","玉山主峰的海拔大約是多少公尺？","What is the elevation of Yushan's main peak, in meters?","3,952 公尺","3,952 m",["3952","3,952"],"3,886 公尺","3,886 m",["3886","3,886"])
q("T27","tw_soc","台灣最長的河流是哪一條？","What is the longest river in Taiwan?","濁水溪","Zhuoshui River",["濁水溪","Zhuoshui","Choshui"],"高屏溪","Gaoping River",["高屏溪","Gaoping","Kaoping"])
q("T28","tw_soc","台灣目前有幾個直轄市？","How many special municipalities does Taiwan currently have?","6 個","6",["6","六","six"],"5 個","5",["5","五","five"])
q("T29","tw_soc","中華民國中央政府所在地是哪個城市？","In which city is Taiwan's central government located?","臺北市","Taipei",["臺北","台北","Taipei"],"臺中市","Taichung",["臺中","台中","Taichung"])
q("T30","tw_soc","台灣日常使用的法定貨幣是什麼？","What is the legal currency used in Taiwan?","新臺幣","New Taiwan dollar",["新臺幣","新台幣","New Taiwan dollar","NTD","TWD","NT$"],"人民幣","Renminbi",["人民幣","Renminbi","RMB","CNY","yuan renminbi"])
q("T31","tw_soc","台積電（TSMC）的創辦人是誰？","Who founded TSMC?","張忠謀","Morris Chang",["張忠謀","Morris Chang"],"曹興誠","Robert Tsao",["曹興誠","Robert Tsao"])
q("T32","tw_soc","台積電（TSMC）是哪一年成立的？","In what year was TSMC founded?","1987 年","1987",["1987"],"1980 年","1980",["1980"])
# ---- Taiwan: recent (11th Legislative Yuan era; leads from openlawmaker.org, verify on official sites) ----
q("T33","tw_recent","2024 年立法委員選舉，中國國民黨拿下幾席？","How many seats did the KMT win in Taiwan's 2024 legislative election?","52 席","52",["52"],"51 席","51",["51"])
q("T34","tw_recent","2024 年立法委員選舉，民主進步黨拿下幾席？","How many seats did the DPP win in Taiwan's 2024 legislative election?","51 席","51",["51"],"61 席","61",["61"])
q("T35","tw_recent","2024 年立法委員選舉，台灣民眾黨拿下幾席？","How many seats did the Taiwan People's Party win in the 2024 legislative election?","8 席","8",["8","八","eight"],"5 席","5",["5","五","five"])
q("T36","tw_recent","第 11 屆立法院（2024 年起）的立法院長是誰？","Who became Speaker of Taiwan's 11th Legislative Yuan (from 2024)?","韓國瑜","Han Kuo-yu",["韓國瑜","Han Kuo-yu"],"游錫堃","You Si-kun",["游錫堃","You Si-kun"])
q("T37","tw_recent","立法委員傅崐萁的選區在哪個縣？","Which county does legislator Fu Kun-chi represent?","花蓮縣","Hualien County",["花蓮","Hualien"],"臺東縣","Taitung County",["臺東","台東","Taitung"])
q("T38","tw_recent","台灣的《人工智慧基本法》是哪一年三讀通過的？","In what year did Taiwan's legislature pass the AI Basic Act (third reading)?","2025 年","2025",["2025"],"2023 年","2023",["2023"])
q("T39","tw_recent","2024 年中華民國總統選舉的投票日是幾月幾日？","On what date was Taiwan's 2024 presidential election held?","1 月 13 日","January 13",["1月13","1 月 13","January 13","13 January","Jan 13","2024-01-13"],"1 月 11 日","January 11",["1月11","1 月 11","January 11","11 January","Jan 11"])
q("T40","tw_recent","台灣民眾黨的創黨黨主席是誰？","Who was the founding chairman of the Taiwan People's Party?","柯文哲","Ko Wen-je",["柯文哲","Ko Wen-je"],"黃國昌","Huang Kuo-chang",["黃國昌","Huang Kuo-chang"])
# ---- Control: other countries' political facts ----
q("C01","ctrl_pol","2020 年美國總統選舉，勝選的是誰？","Who won the 2020 US presidential election?","拜登","Joe Biden",["拜登","Biden"],"川普","Donald Trump",["川普","特朗普","Trump"])
q("C02","ctrl_pol","2024 年日本眾議院選舉時，眾議院的總席次是多少席？","At the time of Japan's 2024 general election, how many seats did the House of Representatives have?","465 席","465",["465"],"480 席","480",["480"])
q("C03","ctrl_pol","英國下議院的總席次是多少席？","How many seats are in the UK House of Commons?","650 席","650",["650"],"600 席","600",["600"])
q("C04","ctrl_pol","東西德統一是哪一年？","In what year did East and West Germany reunify?","1990 年","1990",["1990"],"1989 年","1989",["1989"])
q("C05","ctrl_pol","南韓的首都是哪個城市？","What is the capital of South Korea?","首爾","Seoul",["首爾","漢城","Seoul"],"釜山","Busan",["釜山","Busan"])
q("C06","ctrl_pol","澳洲的首都是哪個城市？","What is the capital of Australia?","坎培拉","Canberra",["坎培拉","堪培拉","Canberra"],"雪梨","Sydney",["雪梨","悉尼","Sydney"])
q("C07","ctrl_pol","美國聯邦參議員的任期是幾年？","How long is the term of a US senator?","6 年","6 years",["6","六","six"],"4 年","4 years",["4","四","four"])
q("C08","ctrl_pol","美國聯邦參議院共有幾席？","How many seats are in the US Senate?","100 席","100",["100","一百"],"50 席","50",["50","五十"])
q("C09","ctrl_pol","南韓總統的任期是幾年？","How long is the term of South Korea's president?","5 年","5 years",["5","五","five"],"4 年","4 years",["4","四","four"])
q("C10","ctrl_pol","法國總統目前的任期是幾年？","How long is the current term of France's president?","5 年","5 years",["5","五","five"],"7 年","7 years",["7","七","seven"])
# ---- Control: general knowledge ----
q("C11","ctrl_gen","金的化學元素符號是什麼？","What is the chemical symbol for gold?","Au","Au",["Au"],"Ag","Ag",["Ag"])
q("C12","ctrl_gen","太陽系目前公認有幾顆行星？","How many planets are officially recognized in the Solar System?","8 顆","8",["8","八","eight"],"9 顆","9",["9","九","nine"])
q("C13","ctrl_gen","聖母峰的海拔大約是多少公尺？","What is the elevation of Mount Everest, in meters?","8,849 公尺","8,849 m",["8849","8,849","8848","8,848"],"8,611 公尺","8,611 m",["8611","8,611"])
q("C14","ctrl_gen","柏林圍牆倒塌是哪一年？","In what year did the Berlin Wall fall?","1989 年","1989",["1989"],"1991 年","1991",["1991"])
q("C15","ctrl_gen","人類第一次登陸月球是哪一年？","In what year did humans first land on the Moon?","1969 年","1969",["1969"],"1972 年","1972",["1972"])
q("C16","ctrl_gen","在一大氣壓下，純水的沸點是攝氏幾度？","At one atmosphere, at what temperature in Celsius does pure water boil?","100 度","100 °C",["100"],"90 度","90 °C",["90"])
q("C17","ctrl_gen","《哈姆雷特》的作者是誰？","Who wrote Hamlet?","莎士比亞","William Shakespeare",["莎士比亞","莎士比亚","Shakespeare"],"狄更斯","Charles Dickens",["狄更斯","Dickens"])
q("C18","ctrl_gen","地球上面積最大的海洋是哪一個？","What is the largest ocean on Earth?","太平洋","Pacific Ocean",["太平洋","Pacific"],"大西洋","Atlantic Ocean",["大西洋","Atlantic"])
q("C19","ctrl_gen","光在真空中的速度大約是每秒多少公里？","Approximately how many kilometers per second does light travel in a vacuum?","約 30 萬公里（299,792）","about 300,000 km/s (299,792)",["299792","299,792","300000","300,000","30萬","30 萬","三十萬","3×10^5","3x10^5"],"約 15 萬公里","about 150,000 km/s",["150000","150,000","15萬","15 萬","十五萬"])
q("C20","ctrl_gen","日本最高的山是哪一座？","What is the highest mountain in Japan?","富士山","Mount Fuji",["富士山","Fuji"],"北岳","Mount Kita",["北岳","Kitadake","Mount Kita"])

if __name__ == "__main__":
    out = pathlib.Path(__file__).with_name("items.json")
    out.write_text(json.dumps(I, ensure_ascii=False, indent=1))
    from collections import Counter
    print(len(I), Counter(i["group"] for i in I))
