The Codes for part 2 of this task are present in : 
catkin_ws --> src --> turtle --> src


It has 4 files 
1)path.py      (imports other file rrtstarconnect1.py, runs it and finds the path. Then, publishes that path)
2)get_path.cpp (it gets the path and controls the turtle simulation to move on that path)
3)feedback.py  (shows path traversed by turtle with respect to the image window)


To run it:
1)open 5 terminal windows
   -> roscore
   -> rosrun turtlesim turtlesim_node
   -> rosrun turtle feedback.py (image window should come up)
   -> rosrun turtle get_path
   -> rosrun turtle path.py (another image window should come up)
   
2) After this, just hit any key twice to run the rrtstarconnect algorithm 
(you can set its running time from rrtstarconnect1.py file. Also make sure to select the last image window while pressing key(just like teleop))
3) After running of rrtstartconnect, hit another key(any). This should start the motion of turtle which would go to the start loaction fisrt and the follow the path found just now
4) Also, a live feed back of turtle's motion would be available on the image window.
