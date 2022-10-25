#include "withimu.h"

class SubscribeAndPublish {
public:
//	SubscribeAndPublish(ros::NodeHandle nh, std::string lidar_topic_name);
	SubscribeAndPublish(ros::NodeHandle nh, std::string lidar_topic_name, std::string imudata_topic_name );
	void callback(const sensor_msgs::PointCloud2ConstPtr& cloudmsg,
			const sensor_msgs::ImuConstPtr& imudata_msg){
		pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
		pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_mark(new pcl::PointCloud<pcl::PointXYZ>);
		pcl::fromROSMsg(*cloudmsg, *cloud);

		std::vector<int> front;
//		//只是看一下效果，即可注销
//		for(int i = 0; i < cloud->size(); i++)
//		{
//			if(
//					cloud->points[i].x > 3 or cloud->points[i].x < -3 or
//					cloud->points[i].y > 15 or cloud->points[i].y < 0)
//				continue;
//			front.push_back(i);
//		}
//		pcl::copyPointCloud(*cloud, front, *cloud_mark);
//		pcl::copyPointCloud(*cloud_mark,*cloud);



		//坐标转换, y为车辆行驶方向
	   double dx,dy,dz; //距离矫正
	   double rx,ry,rz;  //方向矫正

	   double rx_msg = imudata_msg->orientation.x ;
	   double ry_msg = imudata_msg->orientation.y ;
		//矫正前：
		std::cout << "before calib:";
		howcalib(cloud);
	   std::cout<<"rx_msg, ry_msg:"<<rx_msg<< ", "
	            <<ry_msg<<std::endl;



	   dx = 0; dy = 0; dz = 0;
	   rx = pi*(-ry_msg)/180;
	   ry = pi*rx_msg/180;
	   rz = 0;

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

		//矫正后：
		std::cout << "after calib:";
		howcalib(cloud);
		std::cout << "-------------------------------------------"<< std::endl;

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

//void callback(const sensor_msgs::PointCloud2ConstPtr& cloudmsg,
//			const sensor_msgs::ImuConstPtr& imudata_msg);

SubscribeAndPublish::SubscribeAndPublish(ros::NodeHandle nh,
		std::string lidar_topic_name, std::string imudata_topic_name ):
        n_(nh), Sub_Lidar(nh, lidar_topic_name, 100), Sub_Imu(nh, imudata_topic_name,100),
		sync(MySyncPolicy(30), Sub_Lidar, Sub_Imu)
{
	//Topic you want to publish

	pub_ = nh.advertise < sensor_msgs::PointCloud2 > ("/lidarimu", 10);
	sync.registerCallback(boost::bind(&SubscribeAndPublish::callback, this, _1, _2));
}

int main(int argc, char **argv)
{

	ros::init(argc, argv, "calib_node");
	SubscribeAndPublish SAPObject(ros::NodeHandle(), "/lidarcalib","/imu");

	ROS_INFO("waiting for data!");
	ros::spin();

    return 0;
}
