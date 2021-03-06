#!/usr/bin/env python
#       
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_tutorials/license/LICENSE
#
##############################################################################
# Imports
##############################################################################

import os
import sys
import subprocess

import rospy

##############################################################################
# Methods
##############################################################################

            #print("Starting process %s" % ['rocon_launch', temp.name, '--screen'])
            #process = subprocess.Popen(['rocon_launch', temp.name, '--screen'])
            #process = rocon_utilities.Popen(['konsole'])
            #process = subprocess.Popen('konsole -p tabtitle=Dude --nofork -e "/bin/bash" -c ls', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            #process = subprocess.Popen(['ls', '-l'])
            #process = subprocess.Popen('/usr/bin/konsole --nofork', shell=True)
            #process = subprocess.Popen(['konsole'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #process = subprocess.Popen(['gnome-terminal']) # works
            #process = subprocess.Popen(['eog'])  # works
            #process = subprocess.Popen('eog', shell=True)  # works
            #process = subprocess.Popen('gnome-terminal', shell=True)  # works
            #process = subprocess.Popen('konsole --nofork', shell=True, stdout=sys.stdout, stderr=sys.stdout)
            #process = subprocess.Popen(['konsole', '--nofork', '--hold',  '-e', '/bin/bash', '-c', 'ls'])
            #print("Poll: %s" % process.poll())
            #process = subprocess.Popen(['konsole', '--nofork', '--hold',  '-e', '/bin/bash', '-c', 'ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #print("Process communicate [0]: %s" % process.communicate()[0])
            #print("Process communicate [1]: %s" % process.communicate()[1])
            #print("Return code: %s" % process.returncode)
            #process = subprocess.Popen(['konsole', '--nofork'])
            #process = subprocess.Popen(['konsole', '-p', 'tabtitle=Dude', '--hold', '-e', '/bin/bash', '-c', 'ls'])
            #print("Pid: %s" % process.pid)
            #process = subprocess.Popen(['konsole', '-p', 'tabtitle=Dude', '--nofork', '--hold', '-e', "/bin/bash"])
            #self.turtles.extend(turtles)
            #self._process_info.append(ProcessInfo(process, temp))
                
#     def shutdown(self):
#         for process_info in self._process_info:
#             print("Pid: %s" % process_info.process.pid)
#             #process_info.process.terminate()
#             process_info.process.send_signal(signal.SIGINT)
#             #send_signal(signal.SIGINT)
#             os.unlink(process_info.temp_file.name)
# 
#     def signal_handler(self, sig, frame):
#         for process_info in self._process_info:
#             print("Pid: %s" % process_info.process.pid)
#             process_info.process.terminate()
#             try:
#                 #process_info.process.terminate()
#                 process_info.process.send_signal(signal.SIGHUP)
#             except OSError:
#                 print("OSERROR on SIGHUP")
#             os.unlink(process_info.temp_file.name)
#             #wait_pid(pid)

##############################################################################
# Launch point
##############################################################################

if __name__ == '__main__':
    args = ['konsole', '--nofork', '--hold',  '-e', '/bin/bash', '-c', 'ls']
    print("Opening process")
    print("  Session id: %s" % os.getsid(os.getpid()))
    process = subprocess.Popen(['konsole_ls']) #, preexec_fn=os.setsid)
    print("Running")
    try:
        process.wait()
    except KeyboardInterrupt:
        pass
    #rospy.init_node('spawn_kobuki')
    # This would ideally have ros service pairs for
    # spawning and killing turtles
    #turtle_herder = TurtleHerder()
    #signal.signal(signal.SIGINT, turtle_herder.signal_handler)
    #turtle_herder.spawn_turtles(rospy.get_param('~turtles', ['kobuki', 'guimul']))
    #rospy.spin()
    #turtle_herder.shutdown()
