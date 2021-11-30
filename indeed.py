import requests
from bs4 import BeautifulSoup

LIMIT = 50


def extract_indeed_pages(url):

    result = requests.get(url)

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
    job_id = html["data-jk"]
    return {'title': title, 'company': company, 'location': location, 'apply_link': f"https://kr.indeed.com/viewjob?jk={job_id}"}


def extract_indeed_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed page: {page+1}")
        result = requests.get(f"{url}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("a", {"class": "tapItem"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={word}&limit={LIMIT}"
    last_pages = extract_indeed_pages(url)
    jobs = extract_indeed_jobs(last_pages, url)
    return jobs
