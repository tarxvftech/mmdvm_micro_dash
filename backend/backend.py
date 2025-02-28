import json
import pprint
pp=pprint.pprint
import pathlib
import configparser

from fastapi import Request, FastAPI, HTTPException, File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware

import asyncio
from typing import Dict, List
from collections import deque


from misc import *
from files import *
from logs import LogMonitor
from services import *

app = FastAPI()

origins = [
    "*",
    "pim17.local"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


with open("config.ini","r") as fd:
    config = json.load(fd)
allowed_services = config["services"]
allowed_paths = config["editable"]
backups_base_path = pathlib.Path(config["backups"])
log_files = config["logs"]

lm = LogMonitor(log_files)

pp(allowed_paths)
files = profile_files({ pathhash(p):editable_file(p, backups_base_path, pathhash(p)) for p in allowed_paths })
svcs = system_services( {name:systemd_service(name) for name in allowed_services})

"""
TODO: 
    allowed_paths should be a bunch of settings - like read-only.
    files should not generate pathhash twice. I can stop use the automatic stuff for that class I guess.
    add some kind of authentication for a single user
"""

@app.get("/files/")
def list_files():
    return files

@app.get("/files/{h}")
def get_file(h):
    print("h:",h)
    if h in files:
        p = files[h]
        return p
    else:
        return HTTPException(status_code=404)

@app.get("/files/{h}/read")
def read_file(h):
    print("h:",h)
    if h in files:
        p = files[h]
        return p.read()
    else:
        return HTTPException(status_code=404)

@app.put("/files/{h}/write")
async def write_file(h: str, request: Request):
    print("h:",h)
    if h in files:
        p = files[h]
        print("p:", p)
        contents = await request.body()
        return p.backup_and_write(contents)
    else:
        return HTTPException(status_code=404)

@app.get("/files/{h}/backups")
def list_backups(h):
    print("h:",h)
    if h in files:
        p = files[h]
        return p.ls_snapshots()
    else:
        return HTTPException(status_code=404)

@app.post("/files/{h}/backups")
def backup_file(h):
    print("h:",h)
    if h in files:
        p = files[h]
        name = p.gen_filename("apicall")
        return p.snapshot(name)
    else:
        return HTTPException(status_code=404)

@app.post("/files/{h}/backups/{bid}/restore")
def restore_backup(h,bid):
    print("h:",h)
    if h in files:
        p = files[h]
        p.restore(bid)
    else:
        return HTTPException(status_code=404)







@app.get("/services/")
def list_services():
    return svcs

@app.get("/services/{svc}")
def get_service(svc="all"):
    if svc == "all":
        return svcs
    else:
        if svc in svcs:
            return svcs[svc]
        else:
            return HTTPException(status_code=404)

@app.get("/services/{svc}/status")
def status_service(svc="all"):
    if svc == "all":
        return svcs.status()
    else:
        if svc in svcs:
            return svcs[svc].status()
        else:
            return HTTPException(status_code=404)


@app.post("/services/{svc}/{verb}")
def verb_service(svc="all",verb=""):
    if svc in svcs:
        if verb in service_verbs:
            try:
                return getattr(svcs[svc], verb)()
            except NotImplementedError as e:
                print(svc,verb,e)
    else:
        return HTTPException(status_code=404)


@app.on_event("startup")
async def startup():
    asyncio.create_task(lm.run())

@app.get("/logs/")
def list_logs():
    return {n:lm.history[n] for n in log_files}

clients = []
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            # data = await websocket.receive_text()
            await asyncio.sleep(0.1)
    except:
        clients.remove(websocket)



@app.get("/")
def read_root():
    return {"interactive_docs_paths": ["/docs", "/redoc"]}
