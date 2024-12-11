from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/getName")
async def get_name():
    return {"name": "홍길동"}

@app.get("/get_email/{github_id}")
async def get_github_email(github_id: str):
    try:
        url = f"https://github.com/{github_id}"
        
        response = requests.get(url)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Cannot find email GitHub profile")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        email_element = soup.select_one('a[href^="mailto:"]')
        
        if email_element:
            email = email_element['href'].replace('mailto:', '')
            return {"email": email}
        else:
            return {"email": "Cannot find email"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))