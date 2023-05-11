# Dipak Subramaniam
# CS 590 SBN Final Project

import networkx as nx
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import matplotlib

DRIVER_PATH = r'C:\Users\dipak\AppData\Local\Google\Web Driver\chromedriver'
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

G = nx.DiGraph()

top31 = [  # top 31 subreddits of 2022, source: https://blog.oneupapp.io/biggest-subreddits/
    {"Rank": 1, "name": "announcements", "subs": 153972327},
    {"Rank": 2, "name": "funny", "subs": 40442903},
    {"Rank": 3, "name": "AskReddit", "subs": 35787366},
    {"Rank": 4, "name": "gaming", "subs": 32799784},
    {"Rank": 5, "name": "aww", "subs": 31092097},
    {"Rank": 6, "name": "Music", "subs": 29758361},
    {"Rank": 7, "name": "pics", "subs": 28482511},
    {"Rank": 8, "name": "science", "subs": 27820102},
    {"Rank": 9, "name": "worldnews", "subs": 27609819},
    {"Rank": 10, "name": "videos", "subs": 26642802},
    {"Rank": 11, "name": "todayilearned", "subs": 26500738},
    {"Rank": 12, "name": "movies", "subs": 26414252},
    {"Rank": 13, "name": "news", "subs": 24551097},
    {"Rank": 14, "name": "Showerthoughts", "subs": 24622523},
    {"Rank": 15, "name": "EarthPorn", "subs": 21815057},
    {"Rank": 16, "name": "gifs", "subs": 21707631},
    {"Rank": 17, "name": "IAmA", "subs": 21696773},
    {"Rank": 18, "name": "food", "subs": 21631790},
    {"Rank": 19, "name": "askscience", "subs": 21217290},
    {"Rank": 20, "name": "Jokes", "subs": 20882857},
    {"Rank": 21, "name": "LifeProTips", "subs": 20733482},
    {"Rank": 22, "name": "explainlikeimfive", "subs": 20605576},
    {"Rank": 23, "name": "Art", "subs": 20491054},
    {"Rank": 24, "name": "books", "subs": 20347275},
    {"Rank": 25, "name": "mildlyinteresting", "subs": 19479815},
    {"Rank": 26, "name": "nottheonion", "subs": 19481767},
    {"Rank": 27, "name": "DIY", "subs": 19416881},
    {"Rank": 28, "name": "sports", "subs": 19383761},
    {"Rank": 29, "name": "blog", "subs": 18983596},
    {"Rank": 30, "name": "space", "subs": 18856839},
    {"Rank": 31, "name": "gadgets", "subs": 17795689}
]

# node list
top31names = []
for elm in top31:
    top31names.append(elm["name"])

# adding nodes
first = 0
for elm in top31:
    sub_weight = elm["subs"]/1000000
    print(elm["name"])
    print(sub_weight)
    G.add_node(elm["name"], weight=sub_weight)

    base_url = "https://subredditstats.com/subreddit-user-overlaps/"
    stats_url = "https://subredditstats.com/r/"
    driver.get(base_url + elm["name"])
    time.sleep(4)
    pre = driver.find_element_by_xpath("//*[@id='outputEl']")
    divs = pre.find_elements_by_tag_name("div")

    similar = []
    ite = 0
    if first != 0:
        for ch in divs:
            col = ch.text.split(" ", 1)
            col[1] = "".join(col[1].split())
            if col[1] in top31names:
                G.add_edge(elm["name"], col[1], weight=float(col[0]))
    first = first + 1

    nx.write_gml(G, "top31subreddits.gml")

    # similar[col[1]] = float(col[0])
    # print(pre.text)
    # print(pre.tag_name)
    # print(pre.parent)
    # print(pre.location)
    # print(pre.size)
    # /html/body/div[4]/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[1]
    # reqs = requests.get(base_url + elm["name"])
    #
    # soup = BeautifulSoup(reqs.text, 'html.parser')
    # //*[@id="outputEl"]/div[1]
    # similarities = {}
    # pre = soup.find_all("a")
    # print(pre)
    # all_children_by_xpath = pre.find_elements_by_xpath(".//*")
    # print('len(all_children_by_xpath): ' + str(len(all_children_by_xpath)))

    #    if float(col[0]) >= 2.00 and ite < 21:
    #     driver.get(stats_url + col[1])
    #     time.sleep(10)
    #     blocks = driver.find_elements_by_class_name("property-value")
    #     print(blocks)
    #     # td = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[1]/div/div[1]/table/tbody/tr[2]/td[1]')
    #     # # td = driver.find_element_by_xpath("//html//body//div[4]//div[2]//div[1]//div//div[1]//table//tbody//tr[2]//td[1]").text
    #     # sim_weight = float(td.replace(",", ""))/1000000
    #     # G.add_node(col[1], weight=sim_weight)
    #     # G.add_edge(elm["name"], col[1], weight=float(col[0]))
    #     ite = ite + 1
