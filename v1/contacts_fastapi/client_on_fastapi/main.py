from pathlib import Path
import requests

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn


app_dir = Path(__file__).parent

app = FastAPI()

templates = Jinja2Templates(directory=app_dir / "templates")

@app.get('/')
def hello(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "abagalamaga"})

# @app.get("/")
# def kuku():
#     return {"kuku": "hello"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # response = requests.get("https://SilentDismalSweepsoftware.olieksandrkond3.repl.co/healthchecker")
    # print(response)