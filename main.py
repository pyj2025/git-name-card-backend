from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from github_service import GitHubService

app = FastAPI()
github_service = GitHubService()

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
    return {"name": "Joon Park"}

@app.get("/get_name/{github_id}")
async def get_name(github_id: str):
    return await github_service.get_name(github_id)

@app.get("/get_email/{github_id}")
async def get_github_email(github_id: str):
    return await github_service.get_email(github_id)

@app.get("/get_website/{github_id}")
async def get_github_website(github_id: str):
    return await github_service.get_website(github_id)

@app.get("/get_repos/{github_id}")
async def get_repo_count(github_id: str):
    return await github_service.get_repo_count(github_id)

@app.get("/get_linkedin/{github_id}")
async def get_linkedin(github_id: str):
    return await github_service.get_linkedin(github_id)

@app.get("/get_followers/{github_id}")
async def get_followers(github_id: str):
    return await github_service.get_followers(github_id)