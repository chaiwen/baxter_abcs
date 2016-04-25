#!/usr/bin/env python
import sys
import rospy
import baxter_interface

from vision.srv import *
from std_msgs.msg import String

rospy.init_node('control', anonymous=False)
# create instance of Limb class
limb = baxter_interface.Limb('right')

angles = {}



# client to get XYZ from letter of block alphabet
def get_xyz_client(abc):
    rospy.wait_for_service('get_xyz_from_abc')
    try:
        get_xyz_from_abc = rospy.ServiceProxy('get_xyz_from_abc', GetXYZFromABC)
        resp1 = get_xyz_from_abc(abc)
        return resp1.x, resp1.y, resp1.z
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    wave()


def wave():
    # store first and second wave position
    wave_1 = {'right_s0': -0.459, 'right_s1': -0.202, 'right_e0': 1.807, 'right_e1': 1.714, 'right_w0': -0.906, 'right_w1': -1.545, 'right_w2': -0.276}
    wave_2 = {'right_s0': -0.395, 'right_s1': -0.202, 'right_e0': 1.831, 'right_e1': 1.981, 'right_w0': -1.979, 'right_w1': -1.100, 'right_w2': -0.448}

    for _move in range(3):
        limb.move_to_joint_positions(wave_1)
        limb.move_to_joint_positions(wave_2)


def control():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    
    # get current joint angles
    angles = limb.joint_angles()
    angles['right_s0']=0.0
    angles['right_s1']=0.0
    angles['right_e0']=0.0
    angles['right_e1']=0.0
    angles['right_w0']=0.0
    angles['right_w1']=0.0
    angles['right_w2']=0.0

    limb.move_to_joint_positions(angles)

    rospy.Subscriber("speech_command", String, callback)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    #control() # this will subscribe and wave robot arm?
    abc = "BLOCK A!"
    print "Requesting position of %s"%(abc)

    x, y, z = get_xyz_client(abc)

    print "%s = %d %d %d"%(abc, x, y, z)
