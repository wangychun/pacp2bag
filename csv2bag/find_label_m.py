# coding=utf-8
from GPS2UTM import GisTransform
import math
import os
import pandas as pd
import csv
import pathlib

# 注意： 对label进行归一化 max and min:  tensor(68.9906) ;  tensor(-23.5500)
# sum/2 = 22.725, diff/2 = 46.275( half sum = hsum; hdiff;
# value = (value - hsum) / hdiff
hsum = 22.725
hdiff = 46.275

gis = GisTransform('wgs84', 'webMercator')
dfg = pd.read_csv(
    '/home/wyc/0927/envir_2/gpslog2021-09-27-14-49-45.log-GPS.csv')
dfi = pd.read_csv(
    '/home/wyc/0927/envir_2/gpslog2021-09-27-14-49-45.log-IMU.csv')

# p = pathlib.Path('/home/wyc/0927/2_second_train/train/data')
# H_paths = list(p.glob('E*.png'))
# H_paths.sort()
un_name = os.listdir('/home/wyc/0927/2_second_train/train/data')
un_name.sort()

minx, maxx = 100, -100
miny, maxy = 100, -100

data_index = 5
for rrow in range(dfg.shape[0]):
    tip = dfg['timestamp'][rrow]
    rosftime = 1632672000 + int(tip) // 1000 + int(tip) % 1000 / 1000  # 0927
    rosftime_str = str(rosftime)

    # _, train_name = os.path.split(un_name[data_index])
    # train_name = train_name[1:-4]
    if data_index > len(un_name): break
    train_name = un_name[data_index]
    train_name = train_name[:-4]
    # break
    # print(train_name)
    if rosftime_str == train_name:
        # data_index = data_index + 1 #second train模式，每6张图片一组，1-6,2-7,3-8
        data_index = data_index + 6  # second eval/test模式，6张图片各一组，1-6,7-12
        # log_path = '/home/wyc/0927/2_second_train/train/label/' + rosftime_str + '.csv'
        # file = open(log_path, 'a+', encoding='utf-8', newline='')
        # csv_writer = csv.writer(file)
        # csv_writer.writerow([f'x', 'y'])

        latitude = dfg[' latitude'][rrow]   # 维度
        longitude = dfg[' longitude'][rrow]  # 经度
        ord_o = gis.transform_func(longitude, latitude)

        # csv_writer.writerow([ord_o[0], ord_o[1]])
        # save_x, save_y = 0, 0
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

            # find min and max
            if minx > ordx:
                minx = ordx
                print("minx is update to : ", minx)
            if maxx < ordx:
                maxx = ordx
                print("maxx is update to : ", maxx)
            if miny > ordy:
                miny = ordy
                print("miny is update to : ", miny)
            if maxy < ordy:
                maxy = ordy
                print("maxy is update to : ", maxy)

            # 归一化
            # ordx = (ordx - hsum) / hdiff
            # ordy = (ordy - hsum) / hdiff

        #     if (i + 1) % 10 == 0:
        #         csv_writer.writerow([ordx, ordy])
        # file.close()
print("final minx, maxx, miny, maxy: ",minx, "; ", maxx, "; ", miny, "; ", maxy)
# final minx, maxx, miny, maxy:
# -21.403584356714035 ;  19.246502543986114 ;  -8.179473070857545 ;  68.96927579900175
# minx = -20, maxx = 20, miny = 0, maxy = 80