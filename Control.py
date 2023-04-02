#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class RobotController:
    def __init__(self):
        rospy.init_node('robot_controller', anonymous=True)
        rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.twist = Twist()

    def scan_callback(self, data):
        # Define the desired distance from obstacles
        desired_distance = 0.5

        # Calculate the average distance to obstacles
        ranges = data.ranges
        valid_ranges = [r for r in ranges if r > 0.0 and r < 10.0]
        if len(valid_ranges) > 0:
            avg_distance = sum(valid_ranges) / len(valid_ranges)
        else:
            avg_distance = 10.0

        # Adjust the robot's velocity based on the distance to obstacles
        if avg_distance > desired_distance:
            self.twist.linear.x = 0.5
            self.twist.angular.z = 0.0
        else:
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.5

        # Publish the new velocity to the robot
        self.pub.publish(self.twist)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    controller = RobotController()
    controller.run()
