#!/usr/bin/python

import time
import sys
import json

from framework.controller import Controller
from framework.vrouter5600 import VRouter5600
from framework.status import STATUS

if __name__ == "__main__":

    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 5
    
    print ("\n")
    ctrlIpAddr =  "172.22.18.186"
    ctrlPortNum = "8080"     
    ctrlUname = 'admin' 
    ctrlPswd = 'admin'
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    nodeName = "vRouter"
    nodeIpAddr = "172.22.17.107"
    nodePortNum = 830
    nodeUname = "vyatta"
    nodePswd = "vyatta"      
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    print ("<<< 'Controller': %s, '%s': %s" % (ctrlIpAddr, nodeName, nodeIpAddr))
    
    
    print ("\n")
    time.sleep(rundelay)
    result = ctrl.add_netconf_node(vrouter)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("<<< '%s' added to the Controller" % nodeName)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print ("\n")
    time.sleep(rundelay)
    result = ctrl.check_node_conn_status(nodeName)
    status = result[0]
    if(status.eq(STATUS.NODE_CONNECTED) == True):
        print ("<<< '%s' is connected to the Controller" % nodeName)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
        
    print("\n")
    print ("<<< Show list of dataplane interfaces on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interfaces_list()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print "Dataplane interfaces:"
        dpIfList = result[1]
        print json.dumps(dpIfList, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
        
    print("\n")
    ifName = "dp0p1p7"
    print ("<<< Show '%s' dataplane interface configuration on the '%s'" % (ifName,nodeName))
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interface_cfg(ifName)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Dataplane interface '%s' config:" % ifName)
        cfg = result[1]
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print("\n")
    print ("<<< Show configuration of dataplane interfaces on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_dataplane_interfaces_cfg()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print "Dataplane interfaces config:"
        dpIfCfg = result[1]
        print json.dumps(dpIfCfg, indent=4)
    else:
        print ("Demo terminated, reason: %s" % status.brief().lower())
        sys.exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
