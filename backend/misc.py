import hashlib

class callable_dict(dict):
    def __call__(self, *args, **kwargs):
        return {name:fn(*args,**kwargs) for name,fn in self.items()}

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

def hashs(s):
    m = hashlib.sha256()
    m.update(s.encode("utf-8"))
    #salt
    m.update(b"micro_web_file_editor")
    return m.hexdigest()
