import uvicorn
from os import environ as env
from vulndb.fastapi import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(env["PORT"]))
