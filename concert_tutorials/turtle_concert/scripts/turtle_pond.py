#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_services/license/LICENSE
#
##############################################################################
# About
##############################################################################

# Simple script to request a pre-configured number of strolling turtles.
# This could also be done with link graphs, but chatter concert does that.

##############################################################################
# Imports
##############################################################################

import rospy
import rocon_python_comms
import concert_service_utilities
import rocon_scheduler_requests
import unique_id
import scheduler_msgs.msg as scheduler_msgs

##############################################################################
# Classes
##############################################################################


class TurtlePond:
    '''
      Requets handling for getting its mittens on some turtle_stroll'ing
      turtles.
    '''
    __slots__ = [
        'service_name',
        'service_description',
        'service_id',
        'requester',
        'pending_requests',   # [uuid.UUID] list of request id's pending feedback from the scheduler
        'allocated_requests'  # [uuid.UUID] moved here from pending requests once granted
    ]

    def __init__(self):
        ####################
        # Discovery
        ####################
        (self.service_name, self.service_description, self.service_id) = concert_service_utilities.get_service_info()

        ####################
        # Setup
        ####################
        self.requester = self.setup_requester(self.service_id)
        self.pending_requests = []
        self.allocated_requests = []
        number_of_turtles = rospy.get_param("turtles", default=1)
        rospy.loginfo("TurtlePond : requesting %s turtles" % number_of_turtles)
        for unused_i in range(0, number_of_turtles):
            self.request_turtles()

    def setup_requester(self, uuid):
        try:
            scheduler_requests_topic_name = concert_service_utilities.find_scheduler_requests_topic()
            #rospy.loginfo("Service : found scheduler [%s][%s]" % (topic_name))
        except rocon_python_comms.NotFoundException as e:
            rospy.logerr("TurtlePond : %s" % (str(e)))
            return  # raise an exception here?
        frequency = rocon_scheduler_requests.common.HEARTBEAT_HZ
        return rocon_scheduler_requests.Requester(self.requester_feedback, uuid, 0, scheduler_requests_topic_name, frequency)

    def request_turtles(self):
        '''
         Request a turtle.
        '''
        resource = scheduler_msgs.Resource()
        resource.id = unique_id.toMsg(unique_id.fromRandom())
        resource.rapp = 'turtle_concert/turtle_stroll'
        resource.uri = 'rocon:/'
        resource_request_id = self.requester.new_request([resource])
        self.pending_requests.append(resource_request_id)
        self.requester.send_requests()

    def requester_feedback(self, request_set):
        '''
          Keep an eye on our pending requests and see if they get allocated here.
          Once they do, kick them out of the pending requests list so _ros_capture_teleop_callback
          can process and reply to the interaction.

          @param request_set : the modified requests
          @type dic { uuid.UUID : scheduler_msgs.ResourceRequest }
        '''
        for request_id, request in request_set.requests.iteritems():
            if request_id in self.pending_requests:
                if request.msg.status == scheduler_msgs.Request.GRANTED:
                    self.pending_requests.remove(request_id)
                    self.allocated_requests.append(request_id)
        # Need to add logic here for when the request gets released or preempted

    def cancel_all_requests(self):
        '''
          Exactly as it says! Used typically when shutting down or when
          it's lost more allocated resources than the minimum required (in which case it
          cancels everything and starts reissuing new requests).
        '''
        self.requester.cancel_all()
        self.requester.send_requests()

##############################################################################
# Launch point
##############################################################################

if __name__ == '__main__':

    rospy.init_node('turtle_pond')
    turtle_pond = TurtlePond()
    rospy.spin()
    if not rospy.is_shutdown():
        turtle_pond.cancel_all_requests()
