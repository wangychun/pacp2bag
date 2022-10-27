from sensor_msgs.msg import NavSatFix
import rosbag
import rospy
import time
import math

import pandas as pd
dfg = pd.read_csv(
    '/home/wyc/0927/envir_1/02_1206/gpslog2021-09-27-12-06-12.log-GPS.csv')
dfi = pd.read_csv(
    '/home/wyc/0927/envir_1/02_1206/gpslog2021-09-27-12-06-12.log-IMU.csv')
# for row in range(df.shape[0]):
#     print(df['timestamp'][row])

with rosbag.Bag('try.bag', 'w') as bag:
    for row in range(dfg.shape[0]):
        tip = dfg['timestamp'][row]
        # print(dfg['timestamp'][row])
        lcsec = int(tip) // 1000
        lcnsec = int(tip) % 1000 / 1000
        rosftime = 1632672000 + lcsec + lcnsec

        # y, mo, d, h, mi, s = 2021, 9, 27, lcsec // 3600, (lcsec %
        #                                                   3600) // 60, (lcsec % 3600) % 60
        # lcrostime = time.strptime(
        #     str(y) + "-" + str(mo) + "-" + str(d) + "-" + str(h) + "-" + str(mi) + "-" + str(s),
        #     "%Y-%m-%d-%H-%M-%S")
        # print(lcrostime)
        # rosftime = time.mktime(lcrostime)
        # rosftime = lcnsec + rosftime
        # print(rosftime)


        timestamp = rospy.Time.from_seconds(rosftime)
        # print(timestamp)
        gps_msg = NavSatFix()
        gps_msg.header.stamp = timestamp
        gps_msg.latitude = dfg[' latitude'][row]
        gps_msg.longitude = dfg[' longitude'][row]

        # 用高度存速度
        vx = dfi[' V-east'][row]
        vy = dfi[' V-north'][row]
        v = math.sqrt(vx * vx + vy * vy)
        gps_msg.altitude = v
        # print(df['roll'][row])

        # Populate the data elements for IMU
        # e.g. imu_msg.angular_velocity.x = df['a_v_x'][row]

        bag.write("/gps", gps_msg, timestamp)
        # break
        # gps_msg = NavSatFix()
        # gps_msg.header.stamp = timestamp

        # Populate the data elements for GPS

        # bag.write("/gps", gpu_msg, timestamp)
