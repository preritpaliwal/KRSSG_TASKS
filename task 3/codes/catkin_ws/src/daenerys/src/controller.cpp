#include <ros/ros.h>
#include <std_msgs/Int32MultiArray.h>
#include <turtlesim/Pose.h>
#include <geometry_msgs/Twist.h>
#include <bits/stdc++.h>
// #include </turtle1/teleport_absolute.h>
#include <turtlesim/Spawn.h> 
using namespace std;

vector<float> vx;
vector<float> vy;
turtlesim::Pose turtle_pose;
turtlesim::Pose danny_pose;
ros::Publisher cmd_vel_pub;                 
ros::Subscriber pose_sub;  
ros::Publisher danny_vel_pub;
ros::Subscriber danny_pose_sub;
ros::ServiceClient spawn_client;
turtlesim::Spawn::Request spawn_req;        
turtlesim::Spawn::Response spawn_resp;
int k = 0;


void spawnTurtle() 
{
   spawn_req.x = 8.25;
   spawn_req.y = 5.5;
   spawn_req.theta = 1.57;
   spawn_req.name = "daenerys";
//    cout<<"calling service\n";
   ros::service::waitForService("spawn", ros::Duration(20));
   bool success = spawn_client.call(spawn_req,spawn_resp);
   if(success){
       cout<<"watchout I have dragons"<<endl;
   }else{
       cout<<"Might be busy elsewhere"<<endl;
   }
}

float piddist(float x,float y,float dt=0.1)
{
    double kp,ki,kd;
    kp = 1.01;
    ki = 0.2;
    kd = 0.001;
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
    kp = 3.5;
    ki = 0.05;
    kd = 0.05;
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
    float ddanny ;
    float prev_ddanny = -1;
    float angle;
    ros::Time start = ros::Time::now();
    ros::Time end = ros::Time::now();
    vel.linear.y = 0;
    vel.linear.z = 0;
    vel.angular.x = 0;
    vel.angular.y = 0;
    // double prev_d = d;
    while( d > tollerence)
    {
        geometry_msgs::Twist danny_vel;
        
        danny_vel.angular.z = 1;
        danny_vel.linear.x = 2.75*danny_vel.angular.z;



        d = sqrt(pow((x - turtle_pose.x),2) + pow((y- turtle_pose.y),2));
        // cout<<turtle_pose.x<<","<<turtle_pose.y<<"  "<<d<<endl;
        dt = start.toSec() - end.toSec();
        if(dt<0.005)
        {
            dt = 0.1;
        }
        
        end = start;
        
        // std::cout<<dt<<endl;
        start = ros::Time::now();
        ddanny = sqrt(pow((danny_pose.x - turtle_pose.x),2) + pow((danny_pose.y-turtle_pose.y),2));
        vel.linear.x = piddist(x,y,dt);
        vel.angular.z = pidangle(x,y,dt);
        if(ddanny < 4)
        {
            // cout<<"to close\n";
            vel.linear.x = 0.5*ddanny;
            angle = danny_pose.theta - turtle_pose.theta;

            if(ddanny<1.5)
            {
                if(angle>M_PI_2 && angle<3*M_PI_2)
                {
                    if(sqrt( pow((turtle_pose.x-5.5),2) + pow(turtle_pose.y-5.5,2) ) < 2.75 )
                    {
                        vel.angular.z = -M_PI_4;
                    }
                    else
                    {
                        vel.angular.z = M_PI_4;
                    }
                    if (ddanny<1)
                    {
                        vel.linear.x = -8;
                        vel.angular.z *=-20;
                    }
                }
                else
                {
                    if(ddanny < 1)
                    {
                        vel.linear.x = 8;
                        vel.angular.z *=20;
                    }
                }
                
                    
            }
            cout<<angle<<"    "<<danny_pose.theta<<endl;

        }
        prev_ddanny = ddanny;
        cmd_vel_pub.publish(vel);
        danny_vel_pub.publish(danny_vel);
        ros::spinOnce();
        loop_rate.sleep();

        // prev_d = d
    }
    cout<<"while ended\n";
}

void to_destination()
{
    spawnTurtle();

    for(int i = 0;i<vx.size();i++)
    {
        // cout<<"going to destination";
        cout<<vx[i]<<","<<vy[i]<<endl;
        move_to(vx[i]*11/300.0,11-vy[i]*11/300.0);
    }
    move_to(vx[vx.size()-1]*11/300.0,11-vy[vx.size()-1]*11/300.0);
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
        }//cout<<"heading to destination\n";
        to_destination();
    }
}

void getpose(const turtlesim::Pose::ConstPtr &msg)
{
    turtle_pose = *msg;
}

void getdannypose(const turtlesim::Pose::ConstPtr &msg)
{
    danny_pose = *msg;
    // cout<<"danny pose : "<<msg->x<<","<<msg->y<<endl;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "get_path");
  ros::NodeHandle n;
  cmd_vel_pub = n.advertise<geometry_msgs::Twist>("/turtle1/cmd_vel",10);
  danny_vel_pub = n.advertise<geometry_msgs::Twist>("/daenerys/cmd_vel",10);
  pose_sub = n.subscribe("/turtle1/pose",10,getpose);
  danny_pose_sub = n.subscribe("/daenerys/pose",10,getdannypose);
  ros::Subscriber sub = n.subscribe("path_topic", 10,Callback);
  spawn_client = n.serviceClient<turtlesim::Spawn>("/spawn");
  ros::spin();
//   cout<<"about to call to_destination";
//   to_destination();
  return 0;
}