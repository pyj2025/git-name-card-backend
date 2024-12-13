import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

class GitHubService:
    def __init__(self):
        self.base_url = "https://github.com"
        self.api_url = "https://api.github.com/users"

    async def _get_github_page(self, github_id: str):
        url = f"{self.base_url}/{github_id}"
        response = requests.get(url)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="GitHub profile not found")
        return BeautifulSoup(response.text, 'html.parser')

    async def _get_github_api(self, github_id: str):
        url = f"{self.api_url}/{github_id}"
        response = requests.get(url)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="GitHub profile not found")
        return response.json()

    async def get_email(self, github_id: str):
        try:
            soup = await self._get_github_page(github_id)
            email_element = soup.select_one('a[href^="mailto:"]')
            return {"email": email_element['href'].replace('mailto:', '') if email_element else "Email not found"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_website(self, github_id: str):
        try:
            soup = await self._get_github_page(github_id)
            website_element = soup.select_one('a[href^="http"]')
            return {"website": website_element['href'] if website_element else "Website not found"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_repo_count(self, github_id: str):
        try:
            data = await self._get_github_api(github_id)
            return {"repos": data.get("public_repos", 0)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_linkedin(self, github_id: str):
        try:
            soup = await self._get_github_page(github_id)
            linkedin_element = soup.select_one('a[href*="linkedin.com"]')
            return {"linkedin": linkedin_element['href'] if linkedin_element else "LinkedIn profile not found"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_followers(self, github_id: str):
        try:
            data = await self._get_github_api(github_id)
            return {"followers": data.get("followers", 0)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 