import time

import pandas as pd
df = pd.read_csv('/home/wyc/0918/envir/1527_none/gpslog2021-09-18-15-27-39.log-IMU-novelo.csv')
# for row in range(df.shape[0]):
#     print(df['timestamp'][row])
import rospy
import rosbag
from sensor_msgs.msg import Imu

with rosbag.Bag('output.bag', 'w') as bag:
    for row in range(df.shape[0]):
        tip = df['timestamp'][row]
        # print(df['timestamp'][row])
        lcsec = int(tip) // 1000
        lcnsec = int(tip) % 1000 / 1000
        y, mo,d, h, mi, s = 2021, 9, 18, lcsec // 3600, (lcsec % 3600) // 60, (lcsec % 3600) % 60
        lcrostime  = time.strptime(str(y)+"-"+str(mo)+"-"+str(d)+"-"+str(h)+"-"+str(mi)+"-"+str(s),
                      "%Y-%m-%d-%H-%M-%S")

        rosftime = time.mktime(lcrostime)
        rosftime = lcnsec + rosftime
        # print(rosftime)
        timestamp = rospy.Time.from_seconds(rosftime)
        # print(timestamp)
        imu_msg = Imu()
        imu_msg.header.stamp = timestamp
        imu_msg.orientation.x = df[' roll'][row]
        imu_msg.orientation.y = df[' pitch'][row]
        imu_msg.orientation.z = df[' heading'][row]
        # print(df['roll'][row])

        # Populate the data elements for IMU
        # e.g. imu_msg.angular_velocity.x = df['a_v_x'][row]

        bag.write("/imu", imu_msg, timestamp)
        # break

        # gps_msg = NavSatFix()
        # gps_msg.header.stamp = timestamp

        # Populate the data elements for GPS

        # bag.write("/gps", gpu_msg, timestamp)