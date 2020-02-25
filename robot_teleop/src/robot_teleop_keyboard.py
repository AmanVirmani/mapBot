#!/usr/bin/env python
from __future__ import print_function

#import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy 
from geometry_msgs.msg import Twist
import sys, select
import termios, tty

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

moveCommands = {
    'w' : [1,0,0,0],
    's' : [-1,0,0,0],
    'a' : [0,0,0,1],
    'd' : [0,0,0,-1]
}
speedCommands = {
    'q' : [1.1,1.1],
    'z' : [0.9,0.9],
    'e' : [1.1,1.1],
    'c' : [0.9,0.9]
}

msg = """
Use Below mentioned keys to control the robot:
    q : Increase default speed by 10%
    z : Decrease default speed by 10%
    e : Increase default steering speed by 10%
    c : Decrease default steering speed by 10%
    w : move forward
    s : move backward
    a : turn left
    d : turn right
"""
if __name__=='__main__':
    settings = termios.tcgetattr(sys.stdin)

    pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
    rospy.init_node('robot_teleop_keyboard')

    speed = rospy.get_param("--speed", 1.0)
    turn = rospy.get_param("--turn", 0.5)

    print("linear speed: {}".format(speed))
    print("steering speed: {}".format(turn))
    try:
        print(msg)
        while(1):
            key = getKey()
            if key in moveCommands.keys():
                x = moveCommands[key][0]
                print(x)
                y = moveCommands[key][1]
                z = moveCommands[key][2]
                steer = moveCommands[key][3]
            elif key in speedCommands.keys():
                speed *= speedCommands[key][0]
                turn *= speedCommands[key][1]

                print("linear speed: {}".format(speed))
                print("steering speed: {}".format(turn))
            else :
                x =0; y=0;z=0;steer = 0
                if (key == '\x03'):
                    break

            twist = Twist()
            twist.linear.x = x*speed; twist.linear.y = y*speed; twist.linear.z = z*speed;
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = steer*turn;
            pub.publish(twist)
    except Exception as e:
        print(e)
    finally :
            twist = Twist
            #twist = Twist()
            twist.linear.x = x*speed; twist.linear.y = y*speed; twist.linear.z = z*speed;
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = steer*turn;
            pub.publish(twist)

            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
