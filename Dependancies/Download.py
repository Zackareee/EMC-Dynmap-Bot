import requests
from os import path, makedirs, getcwd
from datetime import datetime
import os

if os.name == 'nt':
    s = "#"
else:
    s = "-"
def MarkerDownload(Server):

    print(F"{str(getcwd())}/JSON/{str(Server)}/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}.json")
    Headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    if not path.exists(F"{str(getcwd())}/JSON/{str(Server)}/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}.json"):
        if Server == "Towny":
            DownloadedFile = requests.get('https://earthmc.net/map/nova/standalone/MySQL_markers.php?marker=_markers_/marker_earth.json', headers=Headers)
        elif Server == "Aurora":
            DownloadedFile = requests.get('https://earthmc.net/map/aurora/standalone/MySQL_markers.php?marker=_markers_/marker_earth.json', headers=Headers)

        if b'502: Bad gateway' in DownloadedFile.content:
            print("502: Bad gateway")
            MarkerDownload(Server)
        else:
            makedirs(F"{str(getcwd())}/JSON/{str(Server)}/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}/")
            open(F"{str(getcwd())}/JSON/{str(Server)}/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}.json", 'wb').write(DownloadedFile.content)
            print("File Downloaded")
        return True
    else:
        print("file exists")
        return False