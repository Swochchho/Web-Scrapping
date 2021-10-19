from bs4 import BeautifulSoup
import requests
import time
import csv

def find_jobs():
    source = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=').text

    soup = BeautifulSoup(source, 'lxml')
    jobs = soup.find_all('li', class_= 'clearfix job-bx wht-shd-bx')

    csv_file = open('wscrape.csv', 'w')

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['company Name', 'Required skill','Job Link'])

    for job in jobs:
        published_date = job.find('span', 'sim-posted').span.text
        if 'few' in published_date:
            company = job.find('h3', class_= 'joblist-comp-name').text.replace('  ', '')
            skill = job.find('span', 'srp-skills').text.replace('  ', '')
            link = job.header.h2.a['href']
    
            print(f"Company name: {company.strip()}")
            print(f"Required skills: {skill.strip()}")
            print(f"Job Link: {link.strip()}")
            print(' ')
    
        csv_writer.writerow([company, skill, link])

    csv_file.close()


if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
