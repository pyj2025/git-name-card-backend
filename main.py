from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from fastapi.responses import Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/favicon.ico')
async def favicon():
    return Response(status_code=204)

@app.get("/getName")
async def get_name():
    return {"name": "홍길동"}

@app.get("/get_email/{github_id}")
async def get_github_email(github_id: str):
    try:
        url = f"https://github.com/{github_id}"
        response = requests.get(url)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="GitHub profile not found")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        email_element = soup.select_one('a[href^="mailto:"]')
        
        if email_element:
            email = email_element['href'].replace('mailto:', '')
            return {"email": email}
        else:
            return {"email": "Email not found"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_website/{github_id}")
async def get_github_website(github_id: str):
    try:
        url = f"https://github.com/{github_id}"
        response = requests.get(url)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="GitHub profile not found")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        website_element = soup.select_one('a[href^="http"]')
        
        if website_element:
            website = website_element['href']
            return {"website": website}
        else:
            return {"website": "Website not found"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_repos/{github_id}")
async def get_repo_count(github_id: str):
    try:
        url = f"https://api.github.com/users/{github_id}"
        response = requests.get(url)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="GitHub profile not found")
            
        data = response.json()
        return {"repos": data.get("public_repos", 0)}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_linkedin/{github_id}")
async def get_linkedin(github_id: str):
    try:
        url = f"https://github.com/{github_id}"
        response = requests.get(url)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="GitHub profile not found")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        linkedin_element = soup.select_one('a[href*="linkedin.com"]')
        
        if linkedin_element:
            linkedin = linkedin_element['href']
            return {"linkedin": linkedin}
        else:
            return {"linkedin": "LinkedIn profile not found"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_followers/{github_id}")
async def get_followers(github_id: str):
    try:
        url = f"https://api.github.com/users/{github_id}"
        response = requests.get(url)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="GitHub profile not found")
            
        data = response.json()
        return {"followers": data.get("followers", 0)}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))