from GPS2UTM import GisTransform
import math
import os
import pandas as pd
import csv
import numpy as np

csv_dir = '/home/wyc/0927/2_second_train/train/label/'
un_name = os.listdir(csv_dir)
un_name.sort()
t = np.linspace(0, 5.9, 60)
# print(t)
for name in un_name:
    state = pd.read_csv(csv_dir + name)
    x, y = [], []
    for row in range(1, state.shape[0]):
        x.append(state["x"][row])
        y.append(state["y"][row])
    # print(x)
    px = np.polyfit(t, x, 3)
    py = np.polyfit(t, y, 3)
    fx = np.poly1d(px)
    fy = np.poly1d(py)
    # x_near = fx(t)
    # y_near = fy(t)

    # 存储csv文件
    save_path = '/home/wyc/0927/2_second_train/train/label_near/' + name
    file = open(save_path, 'a+', encoding='utf-8', newline='')
    csv_writer = csv.writer(file)
    csv_writer.writerow([f'x', 'y'])

    for it in t:
        csv_writer.writerow([fx(it), fy(it)])
    # csv_writer.writerow([,])
