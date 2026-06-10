#!/usr/bin/env python
import math

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

THRESHOLD = 1.0
LINEAR_SPEED = 0.5
ANGULAR_SPEED = 0.5


def range_at_angle(scan, angle):
    index = int(round((angle - scan.angle_min) / scan.angle_increment))
    if 0 <= index < len(scan.ranges):
        value = scan.ranges[index]
        if math.isfinite(value):
            return value
    return float("inf")


class WallAvoidance:
    def __init__(self):
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        rospy.Subscriber("/scan", LaserScan, self.scan_callback)

    def scan_callback(self, scan):
        front = range_at_angle(scan, 0.0)
        left = range_at_angle(scan, math.pi / 2)
        right = range_at_angle(scan, -math.pi / 2)

        cmd = Twist()

        if front < THRESHOLD:
            cmd.angular.z = ANGULAR_SPEED
        elif right < THRESHOLD:
            cmd.angular.z = ANGULAR_SPEED
        elif left < THRESHOLD:
            cmd.angular.z = -ANGULAR_SPEED
        else:
            cmd.linear.x = LINEAR_SPEED

        self.cmd_pub.publish(cmd)


if __name__ == "__main__":
    rospy.init_node("wall_avoidance")
    WallAvoidance()
    rospy.spin()
