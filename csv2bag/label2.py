# coding=utf-8
from GPS2UTM import GisTransform
import math
import os
import pandas as pd
import csv
import pathlib

gis = GisTransform('wgs84', 'webMercator')
dfg = pd.read_csv(
    '/home/wyc/0927/envir_1/envir_1/04_1216/gpslog2021-09-27-12-16-47.log-GPS.csv')
dfi = pd.read_csv(
    '/home/wyc/0927/envir_1/envir_1/04_1216/gpslog2021-09-27-12-16-47.log-IMU.csv')

p = pathlib.Path('/home/wyc/0927/test_envir1/Edata/')
H_paths = list(p.glob('E*.png'))
H_paths.sort()
print(H_paths)

# un_name = os.listdir('/home/wyc/0927/0_zero_train/test/data/')
# un_name.sort()

data_index = 5
for rrow in range(dfg.shape[0]):
    tip = dfg['timestamp'][rrow]
    rosftime = 1632672000 + int(tip) // 1000 + int(tip) % 1000 / 1000  # 0927
    rosftime_str = str(rosftime)

    _, train_name = os.path.split(H_paths[data_index])
    train_name = train_name[1:-4]
    # train_name = un_name[data_index]
    # break
    print(train_name)
    if rosftime_str == train_name:
        data_index = data_index + 1 #second train模式，每6张图片一组，1-6,2-7,3-8
        log_path = '/home/wyc/0927/test_envir1/label/' + rosftime_str + '.csv'
        file = open(log_path, 'a+', encoding='utf-8', newline='')
        csv_writer = csv.writer(file)
        csv_writer.writerow([f'x', 'y'])

        latitude = dfg[' latitude'][rrow]   # 维度
        longitude = dfg[' longitude'][rrow]  # 经度
        ord_o = gis.transform_func(longitude, latitude)

        csv_writer.writerow([ord_o[0], ord_o[1]])
        save_x, save_y = 0, 0
        if (rrow + 600) > dfg.shape[0] :
            print("out of lable list : ", train_name)
            break
        for i in range(600):
            row = rrow + i
            heading = dfi[' heading'][row]
            radh = math.radians(heading)
            # print(radh)
            lat = dfg[' latitude'][row]  # 维度
            lon = dfg[' longitude'][row]  # 经度
            g_x, g_y = gis.transform_func(lon, lat)
            # print("gxy: ", g_x, g_y)
            gx = g_x - ord_o[0]
            gy = g_y - ord_o[1]
            # print("xy: ", gx, gy)
            ordx = - gx * math.cos(radh) + gy * math.sin(radh)
            ordy = gy * math.cos(radh) + gx * math.sin(radh)

            if (i + 1) % 10 == 0:
                # csv_writer.writerow([save_x / 10.0, save_y / 10.0])
                csv_writer.writerow([ordx * 2 , ordy / 10.0 ])
                # save_x, save_y = 0, 0
            # else:
                # save_x = save_x + ordx
                # save_y = save_y + ordy
        file.close()
