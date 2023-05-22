import os
import glob
import json
import time
import pathlib
import operator
import itertools
import functools
import subprocess
import hashlib
from typing import Annotated
from dataclasses import dataclass
from typing import Union
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware


import pprint
pp=pprint.pprint

app = FastAPI()

def flatten(itr):
    """https://stackoverflow.com/a/63316751"""
    for x in itr:
        try:
            yield from flatten(x)
        except TypeError:
            yield x
def hashfile(fn):
    m = hashlib.sha256()
    with open(fn,"rb") as fd:
        m.update(fd.read())
    return m.hexdigest()

def hash(s):
    m = hashlib.sha256()
    m.update(s.encode("utf-8"))
    m.update(b"micro_web_file_editor")
    return m.hexdigest()
def pathhash(p):
    return hash(p)[0:10]
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

class system_services(dict):
    def __getattr__(self, name):
        return [getattr(each,name) for each in self.values()]

# result = subprocess.run(["python", "-c", "print(subprocess)"], capture_output=True, text=True, timeout=5)

@dataclass
class system_service:
    name: str
    timeout: int = 10
    def restart(self):
        ret = subprocess.run(self.restartcmd(self.name), capture_output=True, text=True, timeout=self.timeout)
        return ret
    @property
    def status(self):
        ret = subprocess.run(self.statuscmd(self.name), capture_output=True, text=True, timeout=self.timeout)
        #args option: input = "test1234\n"
        return ret

class systemd_service(system_service):
    def statuscmd(self, name):
        return ["systemctl", "status", name]
    def restartcmd(self, name):
        return ["systemctl", "restart", name]

@dataclass
class editable_file:
    path: pathlib.Path
    base_path: pathlib.Path
    pathhash: str
    def read(self):
        fd = open(self.path,"rb")
        contents = fd.read()
        fd.close()
        return contents

    def gen_filename(self, description):
        return "change_%s_%d"%(hashfile(self.path)[0:10],time.time())

    def backup_and_write(self, bs:bytes):
        self.snapshot(snapid=self.gen_filename("change"))
        self.write(bs)

    def write(self, bs:bytes):
        fd = open(self.path,"wb")
        res = fd.write(bs)
        fd.close()
        return res

    def snapshot(self, snapid=None):
        if snapid is None:
            snapid = self.gen_filename("default")
        p = self.base_path  / hash(self.path) 
        p.mkdir(parents=True, exist_ok=True)
        fn = p / snapid
        with open(fn, "wb") as fd:
            fd.write(self.read())
        return snapid

    def restore(self, snapid):
        p = self.base_path  / hash(self.path) / snapid
        self.snapshot( self.gen_filename("prerestore") )
        with open(p, "rb") as fd:
            self.write( fd.read() )
        return snapid

    def ls_snapshots(self):
        p = self.base_path / hash(self.path)
        if not p.exists():
            return []
        fs = [os.path.basename(x) for x in p.iterdir()]
        return fs



class profile_files(dict):
    #list of backup-able files to store snapshots of each file to allow fast switching between profiles
    pass

allowed_services = [
        "mmdvmhost",
        "m17gateway",
        ]
allowed_paths = [
        "/etc/mosquitto/mosquitto.conf",
        "/etc/MMDVMHost",
        "/etc/M17Gateway",
        "/home/mike/projects/mmdvm_micro_dash/mmdvm_micro_dash/static/main.css",
        ]
backups_base_path = pathlib.Path("/tmp/backups/")


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
def write_file(h, contents: Annotated[bytes, File()]):
    print("h:",h)
    if h in files:
        p = files[h]
        print("p:", p)
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
        return svcs.status
    else:
        if svc in svcs:
            return svcs[svc].status
        else:
            return HTTPException(status_code=404)


@app.post("/services/{svc}/restart")
def restart_service(svc="all"):
    return svcs.restart()

@app.get("/")
def read_root():
    return {"interactive_docs_paths": ["/docs", "/redoc"]}

