import time
from uuid import getnode as get_mac
def getUrl():
    str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    tiny = ''
    id = int(round(time.time() * 1000))
    while (id > 0):
        tiny += str[int(id % 62)]
        id = int(id / 62)
    return tiny
def getMacAddress():
    mac = get_mac()
    return str(mac)

