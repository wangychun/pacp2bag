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
//math
#include <math.h>
#include <vector>
#include <Eigen/Dense>
#define pi 3.14159265
//write
//#include "pretreat.h"

class SubscribeAndPublish {
public:
	SubscribeAndPublish(ros::NodeHandle nh, std::string lidar_topic_name);

	void callback(const sensor_msgs::PointCloud2ConstPtr& cloudmsg) {
		pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
		pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_mark(new pcl::PointCloud<pcl::PointXYZRGB>);
		pcl::fromROSMsg(*cloudmsg, *cloud);

		//坐标转换, y为车辆行驶方向
	   double dx,dy,dz; //距离矫正
	   double rx,ry,rz;  //方向矫正
	   double de_rz;//其他参数直接写在程序中，只调整dz，直接在roslaunch中调整
	   ros::param::get("~de_rz",de_rz);

	   dx = 0; dy = 1.12; dz = 2.46;
	   rx = 0; ry = 0; rz = pi*de_rz/180;
//	   std::cout<<"rz:"<<rz<<std::endl;
//	   std::cout<<"de_rz:"<<de_rz<<std::endl;

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
};

SubscribeAndPublish::SubscribeAndPublish(ros::NodeHandle nh,
		std::string lidar_topic_name)
{
	//Topic you want to publish

	pub_ = nh.advertise < sensor_msgs::PointCloud2 > ("/lidarcalib", 10);
	sub_ = n_.subscribe(lidar_topic_name, 10, &SubscribeAndPublish::callback, this);

}

int main(int argc, char **argv)
{

	ros::init(argc, argv, "calib_node");
	SubscribeAndPublish SAPObject(ros::NodeHandle(), "/velodyne_points");

	ROS_INFO("waiting for data!");
	ros::spin();

    return 0;
}
