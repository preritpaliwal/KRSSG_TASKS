#!/usr/bin/env python3
# license removed for brevity
import cv2
import rospy
from turtlesim.msg import Pose
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist

img = cv2.imread("/home/tesla/Desktop/tasks/task 3/images/image 2.png",1)
purple = [128,0,128]
brown = [0,140,255]
yellow = [0,255,255]
white = [255,255,255]
img = cv2.resize(img,(300,300),interpolation = cv2.INTER_AREA)
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

def thresh_white(a):
    k=0
    for i in range(3):
        if a[i]>200:
            k+=1
    if k==3:
        return white
    else:
        return a

def thresh(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = thresh_white(img[i][j])


def comp(a1,a2):
    k = 0 
    for i in range(3):
        if a1[i] == a2[i]:
            k+=1
    if k == 3:
        return True
    else:
        return False


def showfeed(data):
    vel = Twist()
    x = int(data.x*300/11)
    y = int(data.y*300/11)
    print(x,y)
    # print(img)
    cv2.circle(img,(x,300-y),2,purple,-1)
    cv2.imshow("feedback",img)
    cv2.waitKey(1)
    if(comp(img[y][x],white)):
        vel.linear.x = 0.2
        pub.publish(vel)
        print("hitting obstacle")
        # if data.theta <-0.785:
        


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
    thresh(img)
    rospy.Subscriber("/turtle1/pose",Pose, showfeed)
    rospy.Subscriber("path_topic",Int32MultiArray,get_path)
    rospy.spin()

if __name__ == '__main__':
    try:
        # cv2.namedWindow("feedback",cv2.WINDOW_NORMAL)
        feedback()
    except rospy.ROSInterruptException:
        pass