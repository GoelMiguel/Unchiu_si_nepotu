cmake_minimum_required(VERSION 3.0.2)
project(testquiz)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  sensor_msgs
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/wall_avoidance.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
