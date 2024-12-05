from dataclasses import dataclass
import subprocess

from misc import *
class system_services(dict):
    def __getattr__(self, name):
        return callable_dict({each.name:getattr(each,name) for each in self.values()})


# result = subprocess.run(["python", "-c", "print(subprocess)"], capture_output=True, text=True, timeout=5)

service_verbs = ["restart","stop","status","start","enable","disable"]
@dataclass
class system_service:
    name: str
    timeout: int = 10
    def __getattr__(self, name):
        if name in service_verbs:
            if hasattr(self,name+"cmd"):
                def fn():
                    cmd = getattr(self, name+"cmd")
                    ret = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout)
                    return ret
                return fn
            else:
                raise(NotImplementedError)

class rcd_service(system_service):
    @property
    def statuscmd(self):
        return ["rc-service", self.name, "status"]
    @property
    def startcmd(self):
        return ["rc-service", self.name, "start"]
    @property
    def restartcmd(self):
        return ["rc-service", self.name, "restart"]
    @property
    def stopcmd(self):
        return ["rc-service", self.name, "stop" ]
    @property
    def enablecmd(self):
        return ["rc-update", "add", self.name]
    @property
    def disablecmd(self):
        return ["rc-update", "del", self.name]

class systemd_service(system_service):
    @property
    def statuscmd(self):
        return ["systemctl", "status", self.name]
    @property
    def startcmd(self):
        return ["systemctl", "start", self.name]
    @property
    def restartcmd(self):
        return ["systemctl", "restart", self.name]
    @property
    def stopcmd(self):
        return ["systemctl", "stop", self.name]
    @property
    def enablecmd(self):
        return ["systemctl", "enable", self.name]
    @property
    def disablecmd(self):
        return ["systemctl", "disable", self.name]



