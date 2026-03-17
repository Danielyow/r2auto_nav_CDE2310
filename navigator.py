#simple navigator
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
import numpy as np
import math
import cmath
import time

# constants for tuning
rotatechange = 0.1
speedchange = 0.05
stop_distance = 0.25
front_angle = 30
front_angles = range(-front_angle,front_angle+1,1)
turn_duration = 3.0
scanfile = 'lidar.txt'
mapfile = 'map.txt'


class AutoNav(Node):

    def __init__(self):
        super().__init__('auto_nav')
        
        # create publisher for moving TurtleBot
        self.publisher_ = self.create_publisher(Twist,'cmd_vel',10)

        # create subscription to track lidar
        self.scan_subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            qos_profile_sensor_data)
        self.scan_subscription  # prevent unused variable warning
        self.laser_range = np.array([])

    def scan_callback(self, msg):
        # create numpy array
        self.laser_range = np.array(msg.ranges)
        # replace 0's with nan
        self.laser_range[self.laser_range==0] = np.nan

        # find nearest obstacle index
        nearest_idx = np.nanargmin(self.laser_range)

        # convert index to angle (front = 0, left = +, right = -)
        max_idx = len(self.laser_range)
        nearest_angle = (nearest_idx * 360 // max_idx) - 180

        # check if should avoid
        if nearest_angle in front_angles and self.laser_range[nearest_idx] < stop_distance:
            self.get_logger().info(f'obstacle detected at angle {nearest_angle}')
            self.stopbot()

            # check if obstacle is on the left
            if nearest_angle < 0:
                self.get_logger().info('obstacle on the left, turning right')
                twist = Twist()
                twist.linear.x = 0.0
                twist.angular.z = rotatechange
                self.publisher_.publish(twist)
                time.sleep(turn_duration)
            
            # check if obstacle is on the right
            elif nearest_angle >= 0:
                self.get_logger().info('obstacle on the right, turning left')
                twist = Twist()
                twist.linear.x = 0.0
                twist.angular.z = -1*rotatechange
                self.publisher_.publish(twist)
                time.sleep(turn_duration)

            # not sure if this will ever be reached but just in case
            else:
                self.get_logger().info('error not sure where obstacle is, continuing straight')
                twist = Twist()
                twist.linear.x = speedchange
                twist.angular.z = 0.0
                self.publisher_.publish(twist)
        
        # no obstacle detected in front, move forward
        else:
            self.get_logger().info('no obstacle detected, moving forward')
            twist = Twist()
            twist.linear.x = speedchange
            twist.angular.z = 0.0
            self.publisher_.publish(twist)
                
            
    def stopbot(self):
        self.get_logger().info('stopbot')
        # publish to cmd_vel to move TurtleBot
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    auto_nav = AutoNav()
    try:
        rclpy.spin(auto_nav)
    except KeyboardInterrupt:
        auto_nav.get_logger().info('Ctrl+C detected! Stopping robot...')
        auto_nav.stopbot()
    finally:
        auto_nav.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()


