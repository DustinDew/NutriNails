from typing import Union
import uvicorn
from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pathlib as pathlib
import os as os

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q:Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/takeImg")
def take_image():
    return {"Image": "taken"}

if __name__ == "__main__":
    uvicorn.run("main_ip:app", host="0.0.0.0", port=8000, reload=True, ssl_keyfile="key.pem", ssl_certfile="cert.pem")