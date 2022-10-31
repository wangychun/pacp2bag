# coding=utf-8
import math


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