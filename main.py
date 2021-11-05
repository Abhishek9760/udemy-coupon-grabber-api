from fastapi import FastAPI
from coupon_scraper import ComidocScraper

app = FastAPI()

@app.get('/')
async def home():
    scraper_obj  = ComidocScraper()
    g = scraper_obj.get_recent_courses()
    data = []
    for i in range(10):
        data.append(next(g))
    return data
