# 检查数据是否连续
import os

un_name = os.listdir('/home/wyc/0927/0_zero_train/train/data/')
un_name.sort()

# 1632725394.009--1632728102.359
# first, end = 1632725394, 1632728102


# print("list len: ", len(un_name))
for name_index in range(len(un_name) - 1):
    # print("wrong: ", un_name[name_index][: -8])
    # break
    front = int(un_name[name_index][:-8])
    after = int(un_name[name_index + 1][:-8])
    if after - front > 1:
        print("wrong: ", un_name[name_index])
