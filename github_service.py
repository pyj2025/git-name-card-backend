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

    async def get_repo_count(self, github_id: str):
        try:
            data = await self._get_github_api(github_id)
            return {"repos": data.get("public_repos", 0)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_followers(self, github_id: str):
        try:
            data = await self._get_github_api(github_id)
            return {"followers": data.get("followers", 0)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_name(self, github_id: str):
        try:
            soup = await self._get_github_page(github_id)
            name_element = soup.find('span', {
                'itemprop': 'name'
            })
            
            if name_element:
                return {"name": name_element.text.strip()}
            return {"name": "Name not found"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 