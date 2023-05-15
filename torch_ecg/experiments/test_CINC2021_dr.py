from torch_ecg.databases import CINC2021
# dr = CINC2021("/tmp/cinc2021/")
# dr.download()

# RuntimeWarning: `/tmp/cinc2021` does not exist. It is now created. Please check if it is set correctly. Or if you may want to download the database into this folder, please use the `download()` method.
#   warnings.warn(
# TorchECG-CINC2021 - INFO - Please wait patiently to let the reader find all records of all the tranches...
# TorchECG-CINC2021 - INFO - Done in 0.00434 seconds!
# TorchECG-CINC2021 - INFO - converting dtypes of columns `diagnosis` and `diagnosis_scored`...
# Downloading https://storage.cloud.google.com/physionetchallenge2021-public-datasets/WFDB_CPSC2018.tar.gz.
# 156kB [00:00, 1.87MB/s]
#
# This fails because the file can not be downloaded anymore, there is nothing at the
# URL https://storage.cloud.google.com/physionetchallenge2021-public-datasets/WFDB_CPSC2018.tar.gz
#
# So I tried a different appraoch and downloaded the datasets manually, as explained on:
# https://physionet.org/content/challenge-2021/1.0.3/
#
# wget -r -N -c -np https://physionet.org/files/challenge-2021/1.0.3/
#
# Note that this does not download tar.gz files, but it contains all the records (.mat files and .hea)
# as plain files

dr = CINC2021("/home/yoeriapts/workspace/Datasets/physionet.org/files/challenge-2021/1.0.3/training")
print(len(dr))

print(dr.load_data(0, leads=["I", "II"], data_format="channel_last", units="uv"))
print(dr.load_ann(0))

print(dr.get_labels(30000, scored_only=True, fmt="f"))
print(dr.get_labels(30000, scored_only=True, fmt="s"))

print("Wait")




