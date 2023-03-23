from fastapi import FastAPI, Request
import uvicorn
import time

from src.routes import contacts, auth, groups, user


app = FastAPI()


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
    uvicorn.run(app, host="0.0.0.0", port=8000)