/*
 * withimu.h
 *
 *  Created on: 2022年10月25日
 *      Author: wyc
 */

#ifndef SRC_WITHIMU_H_
#define SRC_WITHIMU_H_

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
#include <pcl/ModelCoefficients.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>
//math
#include <math.h>
#include <vector>
#include <Eigen/Dense>
#define pi 3.14159265

void howcalib(pcl::PointCloud<pcl::PointXYZ>::Ptr cloud)
{
		std::vector<int> gdlist;

		for(int i = 0; i < cloud->size(); i++)
		{
			if(
					// 俯仰角
//					cloud->points[i].x > 3 or cloud->points[i].x < -3 or
//					cloud->points[i].y > 15 or cloud->points[i].y < 0)
					//left-right
					cloud->points[i].y > 3 or cloud->points[i].y < -3 or
					cloud->points[i].x > 0 or cloud->points[i].x < -15)
				continue;
			gdlist.push_back(i);
		}

		pcl::PointCloud<pcl::PointXYZ>::Ptr gdCloud(new pcl::PointCloud<pcl::PointXYZ>);
		pcl::copyPointCloud(*cloud, gdlist, *gdCloud);
		pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients);
		pcl::PointIndices::Ptr inliers (new pcl::PointIndices);
		//创建分割对象
		  pcl::SACSegmentation<pcl::PointXYZ> seg;
		 //可选设置
		  seg.setOptimizeCoefficients (true);
		//必须设置
		seg.setModelType (pcl::SACMODEL_PLANE);
		seg.setMethodType (pcl::SAC_RANSAC);
		seg.setDistanceThreshold (0.2);//inline distance is 0.5 m.
		seg.setInputCloud (gdCloud->makeShared ());
		seg.segment (*inliers, *coefficients);// acquire the value of coefficients
		double a = coefficients->values[0];
		double b = coefficients->values[1];
		double c = coefficients->values[2];


		double plrx = atan(b/c);
		double plry = atan(a/c);
		double plrx2, plry2;
		plrx2 = plrx * 180 / pi;
		plry2 = plry * 180 / pi;
//		std::cout << "plrx, plry:" << plrx << ", " << plry << std::endl;
		std::cout << "plrx2, plry2:" << plrx2 << ", " << plry2 << std::endl;
//		std::cout << "drx, dry:" << plrx - ry_msg << ", " << plry - rx_msg<< std::endl;
}


#endif /* SRC_WITHIMU_H_ */
