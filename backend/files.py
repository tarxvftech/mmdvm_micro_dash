import os
import time
import pathlib

from dataclasses import dataclass
from misc import *
def pathhash(p):
    return hashs(p)[0:10]

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
        sh = hashfile(self.path)[0:16]
        p = pathhash(self.path)
        t = int(time.time())
        s = f"change_{p}_{t}_{sh}"
        return s

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
        p = self.base_path  / hashs(self.path) 
        p.mkdir(parents=True, exist_ok=True)
        fn = p / snapid
        with open(fn, "wb") as fd:
            fd.write(self.read())
        return snapid

    def restore(self, snapid):
        p = self.base_path  / hashs(self.path) / snapid
        self.snapshot( self.gen_filename("prerestore") )
        with open(p, "rb") as fd:
            self.write( fd.read() )
        return snapid

    def ls_snapshots(self):
        p = self.base_path / hashs(self.path)
        if not p.exists():
            return []
        fs = [os.path.basename(x) for x in p.iterdir()]
        fs.sort()
        return fs



class profile_files(dict):
    #list of backup-able files to store snapshots of each file to allow fast switching between profiles
    pass
