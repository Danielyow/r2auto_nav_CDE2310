#this is mainly to test that lidar is working and to check if it is calibrated

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
import numpy as np
import threading

class Scanner(Node):

    def __init__(self):
        super().__init__('scanner')
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.listener_callback,
            qos_profile_sensor_data)
        self.subscription  # prevent unused variable warning
        self.lr2i = 0

    # function to read keyboard input press s to scan
    def readKey(self):
        try:
            while True:
                # get keyboard input
                cmd_char = str(input("Keys w/x a/d s: "))
        
                # check which key was entered
                if cmd_char == 's':
                    # print shortest distance and angle
                    self.get_logger().info('Shortest distance at %i degrees' % self.lr2i)
                
        except Exception as e:
            print(e)

    def listener_callback(self, msg):
        # create numpy array
        laser_range = np.array(msg.ranges)
        # replace 0's with nan
        laser_range[laser_range==0] = np.nan
        # find index with minimum value
        self.lr2i = np.nanargmin(laser_range)

def main(args=None):
    rclpy.init(args=args)

    scanner = Scanner()

    # Start keyboard input in a separate thread
    # this is so that keyboard can be read while spin is running
    key_thread = threading.Thread(target=scanner.readKey, daemon=True)
    key_thread.start()

    rclpy.spin(scanner)

    scanner.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
