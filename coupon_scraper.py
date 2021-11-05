import json
import requests
from lxml import html

class ComidocScraper:
    def __init__(self):
        self.json_url = 'https://comidoc.net/_next/data/YVdpchpGwXm8Bo0vIAEa3{course_name}.json'
        self.url = 'https://comidoc.net/'
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    
    def get_recent_courses(self):
        res = requests.get(self.url, headers=self.headers)
        tree = html.fromstring(res.text)
        courses = tree.xpath('//div[contains(@class, "w-[307px]")]')
        for course in courses:
            course_name = course.xpath('.//a//@href')[-1]
            json_url = self.json_url.format(course_name=course_name)
            data = self.handle_json_url(json_url)
            yield data
    
    def handle_json_url(self, url):
        res = requests.get(url, headers=self.headers)
        data = json.loads(res.text).get('pageProps')
        topics = ', '.join([i['title'] for i in data['course']['topic']])
        instructors = ', '.join([i['name'] for i in data['course']['instructor']])
        return {
            'url': self.get_course_url(data['course']['cleanUrl']),
            'coupon': data['course']['code'],
            'topics': topics,
            'instructor': instructors,
            'valid': data['course']['codeIsValid'],
        }
    
    def get_course_url(self, course_name):
        return f'https://udemy.com/course{course_name}'