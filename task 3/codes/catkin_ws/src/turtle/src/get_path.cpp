#include <ros/ros.h>
#include <std_msgs/Int32MultiArray.h>
#include <turtlesim/Pose.h>
#include <geometry_msgs/Twist.h>
#include <bits/stdc++.h>
// #include </turtle1/teleport_absolute.h>
using namespace std;

vector<float> vx;
vector<float> vy;
turtlesim::Pose turtle_pose;
ros::Publisher cmd_vel_pub;                 
ros::Subscriber pose_sub;  
int k = 0;



float piddist(float x,float y,float dt=0.1)
{
    double kp,ki,kd;
    kp = 2.01;
    ki = 0.3;
    kd = 0.005;
    static double prev_e;
    double e = sqrt( pow((x-turtle_pose.x),2) +  pow((y-turtle_pose.y),2) );
    double u = kp*e + ki*e*dt + kd*(e-prev_e)/dt;
    prev_e = e;
    if (u>2)
    return 2;
    else
    return u;
}

float pidangle(float x,float y,float dt=0.1)
{
    double kp,ki,kd;
    kp = 4.5;
    ki = 0.7;
    kd = 0.09;
    static double prev_e;
    double e = atan2(y-turtle_pose.y,x-turtle_pose.x) - turtle_pose.theta;
    double u = kp*e + ki*e*dt + kd*(e-prev_e)/dt;
    prev_e = e;
    return u;
}


void move_to(float x, float y,float tollerence = 0.2)
{
    cout<<"GOAL : "<<x<<","<<y<<endl;
    ros::Rate loop_rate(10);
    geometry_msgs::Twist vel;
    double d  =  sqrt(pow((x - turtle_pose.x),2) + pow((y- turtle_pose.y),2));;
    double dt;
    ros::Time start = ros::Time::now();
    ros::Time end = ros::Time::now();
    vel.linear.y = 0;
    vel.linear.z = 0;
    vel.angular.x = 0;
    vel.angular.y = 0;
    // double prev_d = d;
    while( d > tollerence)
    {
        d = sqrt(pow((x - turtle_pose.x),2) + pow((y- turtle_pose.y),2));
        cout<<turtle_pose.x<<","<<turtle_pose.y<<"  "<<d<<endl;
        dt = start.toSec() - end.toSec();
        if(dt<0.005)
        {
            dt = 0.1;
        }
        
        end = start;
        
        std::cout<<dt<<endl;
        start = ros::Time::now();
        vel.linear.x = piddist(x,y,dt);
        
        vel.angular.z = pidangle(x,y,dt);
        // vel.linear.x = d*0.2;
        // vel.linear.x = d*0.3;
        // vel.angular.z = (atan2(y-turtle_pose.y,x-turtle_pose.x) - turtle_pose.theta);
        cmd_vel_pub.publish(vel);
        ros::spinOnce();
        loop_rate.sleep();
        // prev_d = d
    }
    cout<<"while ended\n";
}

void to_destination()
{
    for(int i = 0;i<vx.size();i++)
    {
        // cout<<"going to destination";
        cout<<vx[i]<<","<<vy[i]<<endl;
        move_to(vx[i]*11/300.0,11-vy[i]*11/300.0);
    }
}

void Callback(const std_msgs::Int32MultiArray::ConstPtr &msg)
{
    k++;
    // cout<<k<<endl;
    if(k==1)
    {
        // {cout<<"some error here\n";
        for(int i = 0;i<msg->data.size();i++)
        {
            if(i%4 == 0)
            {
                vx.push_back(msg->data[i]);
            }
            if(i%4 == 2)
            {
                vy.push_back(msg->data[i]);
            }
        }cout<<"heading to destination\n";
        to_destination();
    }
}

void getpose(const turtlesim::Pose::ConstPtr &msg)
{
    turtle_pose = *msg;
}

int main(int argc, char **argv)
{

  ros::init(argc, argv, "get_path");
  ros::NodeHandle n;
  cmd_vel_pub = n.advertise<geometry_msgs::Twist>("/turtle1/cmd_vel",10);
  pose_sub = n.subscribe("/turtle1/pose",10,getpose);
  ros::Subscriber sub = n.subscribe("path_topic", 10,Callback);
  ros::spin();
//   cout<<"about to call to_destination";
//   to_destination();
  return 0;
}