import time
import os
import pathlib

path = pathlib.Path().resolve()
csp = str(path)
while True:
    dirs = os.listdir( path )
    for file in dirs:
        if file == "autosave.v2":
            try:
                os.rename(csp+'/autosave.v2',csp+"/"+str(len(dirs))+".v2")
            except:
                pass
    time.sleep(2) # Sleep X numbers of seconds
    print(dirs)
