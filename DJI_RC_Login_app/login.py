import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get("/login")
async def pilot_login():
    file_path = "./login.html"
    with open(file_path, "r") as file:
        file_content = file.read()
    # file_content.replace("hostnamehere", host_addr)
    # file_content.replace("userloginhere", username)
    # file_content.replace("userpasswordhere", password)
    return HTMLResponse(file_content)


if __name__ == "__main__":
    uvicorn.run(app, host="10.89.40.97", port=5172)
