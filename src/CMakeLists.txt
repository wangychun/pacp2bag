cmake_minimum_required(VERSION 3.0.2)
project(lidar_calib)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)
add_compile_options(-std=c++14 )
set( CMAKE_CXX_FLAGS "-std=c++11 -O3" )
set(CMAKE_BUILD_TYPE "Release")

set(PACKAGE_DEPENDENCIES
  roscpp
  sensor_msgs
  std_msgs

)



find_package(catkin REQUIRED COMPONENTS 
            ${PACKAGE_DEPENDENCIES}
)       
find_package(PCL 1.8 REQUIRED)  
find_package(OpenCV REQUIRED)

find_package(Eigen3 REQUIRED)

catkin_package(
  CATKIN_DEPENDS ${PACKAGE_DEPENDENCIES}
  DEPENDS EIGEN3 PCL OpenCV
)
include_directories(${catkin_INCLUDE_DIRS} ${PCL_INCLUDE_DIRS} ${OpenCV_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS} ${EIGEN3_INCLUDE_DIR} )
link_directories(${PCL_LIBRARIES_DIRS})
add_definitions(${PCL_DEFINITIONS})


add_executable(lidar_calib
			main.cpp
			)
add_executable(calibwithimu
			withimu.cpp
			)

target_link_libraries(lidar_calib ${catkin_LIBRARIES} ${PCL_LIBRARIES}  ${OpenCV_LIBS} )
target_link_libraries(calibwithimu ${catkin_LIBRARIES} ${PCL_LIBRARIES}  ${OpenCV_LIBS} )
