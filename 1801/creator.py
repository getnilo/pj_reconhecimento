import os
import shutil

arc = os.listdir("C:\\Users\\escolascre01\\Desktop\\pj\\1801\\")

for i in arc:
    if i.endswith(".csv") or i.endswith('.py') or i.endswith("(oculos).jpg"):
        pass
    else:
        ab_ = i.replace(".jpg",'')
        os.makedirs(ab_)
        os.system(f'move "{i}" "{ab_}"')
        