import os
import csv
import math
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

#구인 링크 페이지에서 paging의 최대값을 반환하는 함수
def extract_MaxPages(link):
    print(f"현재 추출할 링크: {link}")
    result = requests.get(link)
    soup = BeautifulSoup(result.text, 'html.parser')
    job = soup.find("p", {"class":["jobCount", "listCount"]})
    jobCount = job.find("strong").text
    jobCount = jobCount.replace(',', '')
    maxpage = math.ceil(float(jobCount)/50)
    return int(maxpage)

#최대 페이지와 구인 링크를 받으면 근무지, 공고제목, 근무시간, 급여, 등록일을 반환하는 함수
def extract_jobs(last_page, link):
    jobs = []
    for page in range(last_page):
        print(f"{page+1}페이지 스크랩중입니`다.")
        result = requests.get(f"{link}?page={page+1}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("tr", {"class": ["", "divide"]})
        for res in results:
            local = res.find_all("td", {"class": "local"})
            title = res.find_all("span", {"class": "title"})
            time = res.find_all("td", {"class": "data"})
            pay = res.find_all("td", {"class": "pay"})
            regdate = res.find_all("td", {"class": "regDate"})
            for i in range(len(pay)):
                job = {'local': local[i].text, 'title': title[i].text, 'time': time[i].text, 'pay': pay[i].text, 'regdate': regdate[i].text}
                jobs.append(job)
    return jobs

# 회사이름과 주소를 dict형태로 links에 저장하는 함수
def extract_superbrand_links(url):
    result = requests.get(url)

    soup = BeautifulSoup(result.text, 'html.parser')

    info = soup.find("div", {"id": "MainSuperBrand"})
    box = info.find_all("a", {"class": "goodsBox-info"})
    link_count = len(box)
    links = {}

    for i in range(link_count):
        company = box[i].find("span", {"class": "company"}).string
        links[company] = box[i]["href"]
    return links

links = extract_superbrand_links(alba_url)
ic = ['\\', '/', ':' ,'*' ,'?' ,'"' ,'<', '>', '|', '.', '%']
for company, link in links.items():
    lastPage = extract_MaxPages(link)
    for c in ic:
        if c in company:
            company = company.replace(c, ' ')
    file = open(company+'.csv', mode="w")
    writer = csv.writer(file)
    writer.writerow(["place", "title", "time", "pay", "date"])
    print(f"{company}의 구인정보 추출을 시작합니다.")
    jobs = extract_jobs(lastPage, link)
    for job in jobs:
        writer.writerow(list(job.values()))
print("모든 정보 추출을 마쳤습니다.")
    