#include <iostream>
//PCL
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/visualization/cloud_viewer.h>
//ROS
#include <ros/ros.h>
#include <pcl_ros/transforms.h>
#include <pcl_conversions/pcl_conversions.h>
#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/approximate_time.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <sensor_msgs/Imu.h>
//math
#include <math.h>
#include <vector>
#include <Eigen/Dense>
#define pi 3.14159265

class SubscribeAndPublish {
public:
//	SubscribeAndPublish(ros::NodeHandle nh, std::string lidar_topic_name);
	SubscribeAndPublish(ros::NodeHandle nh, std::string lidar_topic_name, std::string imudata_topic_name );
	void callback(const sensor_msgs::PointCloud2ConstPtr& cloudmsg,
			const sensor_msgs::ImuConstPtr& imudata_msg){
		pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
		pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_mark(new pcl::PointCloud<pcl::PointXYZ>);
		pcl::fromROSMsg(*cloudmsg, *cloud);

		double rx_msg = imudata_msg->orientation.x ;
		double ry_msg = imudata_msg->orientation.y ;

		//坐标转换, y为车辆行驶方向
	   double dx,dy,dz; //距离矫正
	   double rx,ry,rz;  //方向矫正
	   dx = 0; dy = 1.12; dz = 2.46;

	   double de_rx = -0.954;	rx_msg += de_rx;
	   double de_ry = 1.433;	ry_msg += de_ry;
	   double de_rz = -17;

	   rx = pi*(-ry_msg)/180;
	   ry = pi*rx_msg/180;
	   rz = pi*de_rz/180;

	   Eigen::Vector3d T; //列向量，如果要初始化行向量，用:Eigen::RowVectorXd
	   Eigen::Matrix3d Rx, Ry, Rz, R;
	   T << dx, dy, dz;
	   Rx <<   1, 0, 0,
			   0, cos(rx), -sin(rx),
			   0, sin(rx), cos(rx);
	   Ry << cos(ry), 0, sin(ry),
			   0, 1, 0,
			   -sin(ry), 0, cos(ry);
	   Rz << cos(rz), -sin(rz), 0,
			   sin(rz), cos(rz), 0,
			   0, 0, 1;
	   R = Rx * Ry * Rz;


	   for(int i = 0; i < cloud->points.size(); i++ )
		{

		   Eigen::Vector3d originP,newP;
		   originP << cloud->points[i].x, cloud->points[i].y, cloud->points[i].z;
		   newP = R * originP + T;

			cloud->points[i].x = newP[0];
			cloud->points[i].y = newP[1];
			cloud->points[i].z = newP[2];
		}

		sensor_msgs::PointCloud2 ros_cloud;
		pcl::toROSMsg(*cloud, ros_cloud);

		ros_cloud.header.frame_id = "car";
		ros_cloud.header.stamp = cloudmsg->header.stamp;
		pub_.publish(ros_cloud);

	}

private:
	ros::NodeHandle n_;
	ros::Publisher pub_;
	ros::Subscriber sub_;
	message_filters::Subscriber<sensor_msgs::PointCloud2> Sub_Lidar;
	message_filters::Subscriber<sensor_msgs::Imu> Sub_Imu;

	typedef message_filters::sync_policies::ApproximateTime<sensor_msgs::PointCloud2,sensor_msgs::Imu> MySyncPolicy;
	message_filters::Synchronizer<MySyncPolicy> sync;
};

SubscribeAndPublish::SubscribeAndPublish(ros::NodeHandle nh,
		std::string lidar_topic_name, std::string imudata_topic_name ):
        n_(nh), Sub_Lidar(nh, lidar_topic_name, 1000), Sub_Imu(nh, imudata_topic_name,1000),
		sync(MySyncPolicy(30), Sub_Lidar, Sub_Imu)
{
	//Topic you want to publish

	pub_ = nh.advertise < sensor_msgs::PointCloud2 > ("/lidar_calibed", 10);
	sync.registerCallback(boost::bind(&SubscribeAndPublish::callback, this, _1, _2));
}

int main(int argc, char **argv)
{

	ros::init(argc, argv, "calib_node");
	SubscribeAndPublish SAPObject(ros::NodeHandle(), "velodyne_points","/imu");

	ROS_INFO("waiting for data!");
	ros::spin();

    return 0;
}
