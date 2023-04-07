import time
from math import ceil
from typing import Callable

from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import uvicorn
import redis.asyncio as redis

from src.routes import contacts, auth, groups, user
from src.conf.config import settings

app = FastAPI()

async def callback(request: Request, response: Response, pexpire: int):
    """
    default callback when too many requests
    :param request:
    :param pexpire: The remaining milliseconds
    :param response:
    :return:
    """
    expire = ceil(pexpire / 1000)

    raise HTTPException(
       status.HTTP_429_TOO_MANY_REQUESTS, "Too many requests. Please wait 1 minute", headers={"Retry-After": str(expire)}
    )


@app.on_event("startup")
async def startup():
  r = await redis.Redis(host=settings.redis_host,
                        port=settings.redis_port,
                        password=settings.redis_password,
                        encoding="utf-8",
                        decode_responses=True)
  await FastAPILimiter.init(r, http_callback=callback)


origins = [
  "https://SilentDismalSweepsoftware.olieksandrkond3.repl.co",
  "http://localhost:5500",
  "http://127.0.0.1:5500",
  "http://localhost:8000",
  "http://95.134.189.14:5500",
  "https://172.31.128.1:5500",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
  start_time = time.time()
  response = await call_next(request)
  process_time = time.time() - start_time
  response.headers["Process-Time"] = str(process_time)
  return response


app.include_router(contacts.router, prefix="/api")
app.include_router(groups.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")


@app.get("/healthchecker")
def read_root():
  return {"message": "Auuuuuuuu"}


if __name__ == "__main__":
  # print(settings)
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
