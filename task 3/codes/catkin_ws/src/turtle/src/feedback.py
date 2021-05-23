#!/usr/bin/env python3
# license removed for brevity
import cv2
import rospy
from turtlesim.msg import Pose
from std_msgs.msg import Int32MultiArray

img = cv2.imread("/home/tesla/Desktop/tasks/task 3/images/image 2.png",1)
purple = [128,0,128]
brown = [0,140,255]
yellow = [0,255,255]
img = cv2.resize(img,(300,300),interpolation = cv2.INTER_AREA)


def showfeed(data):
    x = int(data.x*300/11)
    y = int(data.y*300/11)
    print(x,y)
    # print(img)
    cv2.circle(img,(x,300-y),2,purple,-1)
    cv2.imshow("feedback",img)
    cv2.waitKey(1)

def showpath():
    for i in range(len(vx)):
        cv2.circle(img,(vx[i],vy[i]),5,yellow)
        if i+1 !=len(vx):
            cv2.line(img,(vx[i],vy[i]),(vx[i+1],vy[i+1]),brown,3)

k = 0
vx = []
vy = []
def get_path(data):
    global k
    k+=1
    if k ==1:
        for i in range(len(data.data)):
            if i%4 == 0:
                vx.append(int(data.data[i]))
            if i%4 == 2:
                vy.append(int(data.data[i]))
        showpath()

def feedback():
    rospy.init_node('feedback', anonymous=True)
    rospy.Subscriber("/turtle1/pose",Pose, showfeed)
    rospy.Subscriber("path_topic",Int32MultiArray,get_path)
    rospy.spin()

if __name__ == '__main__':
    try:
        # cv2.namedWindow("feedback",cv2.WINDOW_NORMAL)
        feedback()
    except rospy.ROSInterruptException:
        pass