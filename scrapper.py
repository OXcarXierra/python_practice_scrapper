import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q="

def get_last_page(word):
    result = requests.get(f"{URL}{word}")
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_jobs(last_page,word):
    job_list = []
    for page in range(last_page): 
        print(f"Extracting from page {page+1}")
        result = requests.get(f"{URL}{word}&pg={page+1}") 
        soup = BeautifulSoup(result.text,"html.parser")
        jobs = soup.find_all("div",{"class":"-job"})
        for job in jobs:
            job_list.append(extract_data(job))
    return job_list

def extract_data(html):
    title = html.find("h2",{"class":"mb4"}).find("a")["title"]
    company, location = html.find("h3",{"class":"fc-black-700"}).find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html['data-jobid']
    return {'title':title, "company":company, "location":location, "apply_link": f"https://stackoverflow.com/jobs/{job_id}/"}

def get_jobs(word):
    last_page = get_last_page(word)
    jobs = extract_jobs(last_page, word)
    return jobs
