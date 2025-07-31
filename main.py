from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Route GET /ping
@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return PlainTextResponse(content="pong", status_code=200)

# Route GET /home
@app.get("/home", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content="<html><body><h1>Welcome home!</h1></body></html>", status_code=200)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return HTMLResponse(content="<html><body><h1>404 NOT FOUND</h1></body></html>", status_code=404)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})