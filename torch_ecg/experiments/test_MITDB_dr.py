import sys
print(sys.executable)
#%%

from torch_ecg.databases import MITDB
dr = MITDB(db_dir="/tmp/MITDB")
#dr.download()

print(len(dr))

dr.helper("beat")

dr.helper("rhythm")

