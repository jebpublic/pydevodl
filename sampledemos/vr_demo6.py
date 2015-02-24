#!/usr/bin/python

import time
import sys
import json

from framework.controller.controller import Controller
from framework.netconfdev.vrouter.vrouter5600 import VRouter5600
from framework.common.status import STATUS
from framework.common.utils import load_dict_from_file


if __name__ == "__main__":

    f = "cfg4.yml"
    d = {}
    if(load_dict_from_file(f, d) == False):
        print("Config file '%s' read error: " % f)
        exit()

    try:
        ctrlIpAddr = d['ctrlIpAddr']
        ctrlPortNum = d['ctrlPortNum']
        ctrlUname = d['ctrlUname']
        ctrlPswd = d['ctrlPswd']

        nodeName = d['nodeName']
        nodeIpAddr = d['nodeIpAddr']
        nodePortNum = d['nodePortNum']
        nodeUname = d['nodeUname']
        nodePswd = d['nodePswd']
    except:
        print ("Failed to get Controller device attributes")
        exit(0)
    
    
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 5
    
    print ("\n")
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    vrouter = VRouter5600(ctrl, nodeName, nodeIpAddr, nodePortNum, nodeUname, nodePswd)
    print ("<<< 'Controller': %s, '%s': %s" % (ctrlIpAddr, nodeName, nodeIpAddr))
    
    
    print ("\n")
    time.sleep(rundelay)
    result = ctrl.add_netconf_node(vrouter)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("<<< '%s' added to the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    time.sleep(rundelay)
    result = ctrl.check_node_conn_status(nodeName)
    status = result[0]
    if(status.eq(STATUS.NODE_CONNECTED) == True):
        print ("<<< '%s' is connected to the Controller" % nodeName)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Show list of loopback interfaces on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_loopback_interfaces_list()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print "Loopback interfaces:"
        dpIfList = result[1]
        print json.dumps(dpIfList, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    

    print("\n")
    ifName = "lo4"
    print ("<<< Show '%s' loopback interface configuration on the '%s'" % (ifName,nodeName))
    time.sleep(rundelay)
    result = vrouter.get_loopback_interface_cfg(ifName)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Loopback interface '%s' config:" % ifName)
        response = result[1]
        content = response.content
        data = json.loads(content)
        print json.dumps(data, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print("\n")
    print ("<<< Show configuration of loopback interfaces on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_loopback_interfaces_cfg()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print "Loopback interfaces config:"
        lbIfCfg = result[1]
        print json.dumps(lbIfCfg, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
        
    
    print("\n")
    print ("<<< Show interfaces configuration on the '%s'" % nodeName)
    time.sleep(rundelay)
    result = vrouter.get_interfaces_cfg()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print "Interfaces config:"
        cfg = result[1]
        data = json.loads(cfg)
        print json.dumps(data, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    

    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    