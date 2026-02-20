from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from playwright.sync_api import sync_playwright

app = FastAPI(title='WP Headless Render Service', version='0.1.0')

class RenderIn(BaseModel):
url: HttpUrl
wait_ms: int = 2500

@app.get('/health')
def health():
return {'ok': True}

@app.post('/render')
def render(payload: RenderIn):
try:
with sync_playwright() as p:
browser = p.chromium.launch(headless=True)
page = browser.new_page()
page.goto(str(payload.url), wait_until='domcontentloaded', timeout=60000)
page.wait_for_timeout(max(0, min(payload.wait_ms, 15000)))
html = page.content()
final_url = page.url
browser.close()
return {'ok': True, 'url': str(payload.url), 'final_url': final_url, 'html': html}
except Exception as e:
raise HTTPException(status_code=400, detail=str(e))
