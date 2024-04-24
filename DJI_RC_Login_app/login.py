import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()
public_ip = "10.89.40.97"


@app.get("/login")
async def pilot_login():
    file_path = "./login.html"
    with open(file_path, "r") as file:
        file_content = file.read()
    return HTMLResponse(file_content)


if __name__ == "__main__":
    uvicorn.run(app, host=public_ip, port=5172)
