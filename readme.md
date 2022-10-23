# velodyne的pcap包数据解析和坐标变换
## 1.先安装velodyne提供的drive
    sudo apt-get install ros-melodic-velodyne*
其中"-melodic-"是可以替换成ros的对应版本名，如”ros-noetic-velodyne*“
## 2.然后对采集的calib的数据集进行数据解析和标定
### <u>1）calib数据解析（1_Trans.launch）</u>
#### a.  修改文件中”pcap“的“value”值
切记改成绝对文件路径
#### b.  修改node "rosbag" 的“args”
其中“-O”是大写的字母o，此时bag的命名要有后缀文件类型，路径要写绝对路径，/velodyne_points是录的包的话题。如果全录，则可使用-a
#### c.  rviz的config文件要绝对路径
可以先不开这个节点，先rviz调整好，再保存config文件
#### d.  执行1_Trans.launch文件
解析pcap文件至rosbag文件
    roslaunch /launch/1_Trans.launch
### <u>2)  标定（2_Calib.launch,src)</u>
#### a.  先建立ros工作空间，把src文件放进去
    mkdir calib
    cd calib
    catkin_make
    source devel/setup.bash
#### b.  修改src中的main.cpp
直接在文件中找到dx,dy,dz,rx,ry,rz的赋值代码段，除了rz，其他参数都直接给出（dx,dy,dz）是量的，以车辆行驶方向为y轴。修改后记得编译。
    catkin_make
#### c.  修改2_Calib.launch
修改rosbag节点（node)的arg,改成1）b中bag存储的文件路径
修改"de_rz"的value值，微调最终实现较为精确的标定
rviz的修改类似1）d
#### d.  通过修改launch中的de_rz值，并观察rviz中点云的状态，直到微调的标定结果达到要求，记录de_rz值
## 3. 从pcap生成标定后的rosbag包
### <u>1）用2中标定的de_rz值替换3_TransCalib.launch中de_rz值</u>
### <u>2）修改pcap的路径为需要解析的pcap</u>

*注意：如果2,3的launch报错，在calib文件夹再执行一次`source devel/setup.bash`*
