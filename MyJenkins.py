__author__ = 'nguyenbon'
import json
import time
import serial
import subprocess
import sys

# Configurations
ping_server = 30
jenkins_username = 'dev_ops__'
jenkins_apitoken = 'e09592116b63e92c31972cebb0eedfe9'
jenkins_host = "devops.com.vn"
jenkins_port = "8082"
jenkins_jobs = ["MyJenkinsBackEnd"]
# ser = serial.Serial('COM3', 9600)
ser = serial.Serial('/dev/cu.usbmodem1411', 9600)
# Arduino Configuration
SUCCESS = 'b'
FAILURE = 'r'
BUILDING = 'a'
UNSTABLE = 'y'

time.sleep(5)


def get_status(jobName):
    try:
        jenkins_url = 'http://'+jenkins_username+":"+jenkins_apitoken+"@" + jenkins_host+":"+jenkins_port+"/job/"+jobName+"/lastBuild/api/json"
        cmd = 'curl --silent --show-error ' + jenkins_url
        args = cmd.split()
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
    except Exception, e:
        print stderr
        print "URL Error: " + str(e.code)
        print "      (job name [" + jobName + "] probably wrong)"
        sys.exit(2)
    try:
        buildStatusJson = json.loads(stdout)
    except:
        print "Failed to parse json"
        sys.exit(3)
    return jobName, buildStatusJson["timestamp"], buildStatusJson["result"],

while (1):
    for job in jenkins_jobs:
        status = get_status(job)
        #write the marker ~ to serial
        ser.write('~')
        time.sleep(5)
        if status[2] == "UNSTABLE":
            ser.write(UNSTABLE)
            print "Unstable"
        elif status[2] == "SUCCESS":
            ser.write(SUCCESS)
            print "Success"
        elif status[2] == "FAILURE":
            ser.write(FAILURE)
            print "Failure"
        elif status[2] == None:
            ser.write(BUILDING)
            print "Building"
        time.sleep(ping_server)