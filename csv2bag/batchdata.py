import shutil

import os
from shutil import copyfile

un_name = os.listdir('/home/wyc/0927/second_train/train/data/')
un_name.sort()
fromdir = '/home/wyc/0927/second_train/train/data/'
outputdir = '/home/wyc/0927/second_train/train/data_batch/'
for i in range(len(un_name) - 6):
    fromname = fromdir + un_name[i]
    outdir = outputdir + str(un_name[i + 5][:-4])
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for j in range(6):
        outname = outdir + '/' + str(un_name[i + j])
        shutil.copyfile(fromname,outname)
    # break