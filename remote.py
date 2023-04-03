#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from flask import Flask, render_template, request

app = Flask(__name__)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
twist = Twist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    linear_x = request.form['linear_x']
    angular_z = request.form['angular_z']
    twist.linear.x = float(linear_x)
    twist.angular.z = float(angular_z)
    pub.publish(twist)
    return render_template('index.html')

if __name__ == '__main__':
    rospy.init_node('robot_controller', anonymous=True)
    app.run(debug=True, host='0.0.0.0')
