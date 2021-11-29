import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}"


def extract_indeed_pages():

    result = requests.get(URL)

    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("span", title=True).string
    company = html.find("span", {"class": "companyName"}).string
    location = html.find("div", {"class": "companyLocation"}).string
    job_href = html["href"]
    return {f"공고: {title} 모집회사: {company} 회사위치: {location} 모집링크: {job_href}"}


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("a", {"class": "tapItem"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs
