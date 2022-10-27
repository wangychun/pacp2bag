# coding=utf-8
import math
# import re
import pandas as pd
import csv

dfg = pd.read_csv(
    '/home/wyc/0918/envir/1527_none/gpslog2021-09-18-15-27-39.log-GPS.csv')
dfi = pd.read_csv(
    '/home/wyc/0918/envir/1527_none/gpslog2021-09-18-15-27-39.log-IMU.csv')

class GisTransform(object):
    """gis坐标转换类"""

    def __init__(self, old_gis_name, new_gis_name):
        """
        经纬度(谷歌高德):'wgs84'/  墨卡托:'webMercator'
        """
        self.pi = 3.1415926535897932384626  # π   精度比math.pi 还高一些
        self.ee = 0.00669342162296594323  # 偏心率平方
        self.a = 6378245.0  # 长半轴

        func_name = old_gis_name + '_to_' + new_gis_name
        if hasattr(self, func_name):
            self.transform_func = getattr(self, func_name)



    def _transformlat(self, lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
            0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * self.pi) + 40.0 *
                math.sin(lat / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * self.pi) + 320 *
                math.sin(lat * self.pi / 30.0)) * 2.0 / 3.0
        return ret

    def _transformlng(self, lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
            0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * self.pi) + 20.0 *
                math.sin(2.0 * lng * self.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * self.pi) + 40.0 *
                math.sin(lng / 3.0 * self.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * self.pi) + 300.0 *
                math.sin(lng / 30.0 * self.pi)) * 2.0 / 3.0
        return ret

    def wgs84_to_webMercator(self, lon, lat):
        """wgs84坐标 转 墨卡托坐标"""
        x = lon * 20037508.342789 / 180
        y = math.log(math.tan((90 + lat) * self.pi / 360)) / (self.pi / 180)
        y = y * 20037508.34789 / 180
        return x, y


    def webMercator_to_wgs84(self, x, y):
        """墨卡托坐标 转 wgs84坐标"""
        lon = x / 20037508.34 * 180
        lat = y / 20037508.34 * 180
        lat = 180 / self.pi * \
            (2 * math.atan(math.exp(lat * self.pi / 180)) - self.pi / 2)
        return lon, lat


if __name__ == '__main__':
    # 经纬度: wgs84 墨卡托: webMercator 国测局: gcj02
    rrow = 0
    gis = GisTransform('wgs84', 'webMercator')

    while rrow < dfg.shape[0] - 60:
        tip = dfg['timestamp'][rrow]
        # rosftime = 1632672000 + int(tip) // 1000 + int(tip) % 1000 / 1000 #0927
        rosftime = 1631894400 + int(tip) // 1000 + int(tip) % 1000 / 1000
        log_path = 'ord_0918/ord'+ str(rosftime) + '.csv'
        file = open(log_path, 'a+', encoding='utf-8', newline='')
        csv_writer = csv.writer(file)
        csv_writer.writerow([f'x', 'y'])

        # timestamp = rospy.Time.from_seconds(rosftime)
        latitude = dfg[' latitude'][rrow]   # 维度
        longitude = dfg[' longitude'][rrow] # 经度
        ord_o = gis.transform_func(longitude, latitude)
        print("ord: ",ord_o)
        csv_writer.writerow([ord_o[0], ord_o[1]])
        for i in range(60):
            row = rrow + i
            heading = dfi[' heading'][row]
            radh = math.radians(heading)
            # print(radh)
            lat = dfg[' latitude'][row]  # 维度
            lon = dfg[' longitude'][ row] # 经度
            g_x, g_y = gis.transform_func(lon, lat)
            print("gxy: ",g_x, g_y)
            gx = g_x - ord_o[0]
            gy = g_y - ord_o[1]
            print("xy: ", gx,gy)
            ordx = gx * math.cos(radh) - gy * math.sin(radh)
            ordy = gy * math.cos(radh) + gx * math.sin(radh)
            csv_writer.writerow([ordx, ordy])
        # print(gis.transform_func(114.09538, 22.62663))
        rrow = rrow + 60

    file.close()