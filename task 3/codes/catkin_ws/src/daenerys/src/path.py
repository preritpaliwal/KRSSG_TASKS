#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import Int32MultiArray
import rrtstarconnect1
import numpy as np

def print1():
    print("hello from ros")

def give():
    pub = rospy.Publisher('path_topic', Int32MultiArray, queue_size=10)
    rospy.init_node('path_node', anonymous=False)
    rate = rospy.Rate(10) # 10hz
    path = Int32MultiArray()
    # path.data = rrtstarconnect1.p4

    while not rospy.is_shutdown():
        # path = rrtstarconnect1.p4
        # img = rrtstarconnect1.imre
        # rrtstarconnect1.show(img)
        p5 = np.array(rrtstarconnect1.p4)
        print(p5)
        # p5 = (p5/300)*11
        path.data = np.frombuffer(p5.tobytes(),'int32')
        print(path.data)
        pub.publish(path)
        rate.sleep()

if __name__ == '__main__':
    try:
        rrtstarconnect1.rrtstarconnect()
        give()
    except rospy.ROSInterruptException:
        pass