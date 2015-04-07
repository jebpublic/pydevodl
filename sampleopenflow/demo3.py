#!/usr/bin/python

import sys
import time
import json


from framework.controller.controller import Controller
#from framework.controller.openflownode import OpenflowNode
from framework.openflowdev.ofswitch import OFSwitch
from framework.common.status import STATUS
from framework.common.utils import load_dict_from_file


if __name__ == "__main__":

    f = "cfg.yml"
    d = {}
    if(load_dict_from_file(f, d) == False):
        print("Config file '%s' read error: " % f)
        exit()

    try:
        ctrlIpAddr = d['ctrlIpAddr']
        ctrlPortNum = d['ctrlPortNum']
        ctrlUname = d['ctrlUname']
        ctrlPswd = d['ctrlPswd']
    except:
        print ("Failed to get Controller device attributes")
        exit(0)
    
    
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print ("<<< Demo Start")
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    rundelay = 5

    print ("\n")
    print ("<<< Creating Controller instance")
    time.sleep(rundelay)
    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd, None)
    print ("'Controller':")
    print ctrl.brief_json()
    
    
    print ("\n")
    name = "openflow:1"
#    name = "openflow:10195227440578560"
    print ("<<< Get detailed information about ports on OpenFlow node '%s'" % name)
    time.sleep(rundelay)
    ofswitch = OFSwitch(ctrl, name)
    
    result = ofswitch.get_ports_list()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        ports = result[1]
        for port in ports:
            result = ofswitch.get_port_detail_info(port)
            status = result[0]
            if(status.eq(STATUS.OK) == True):
                print ("Port '%s' info:" % port)
                info = result[1]
                print json.dumps(info, indent=4)
            else:
                print ("\n")
                print ("!!!Demo terminated, reason: %s" % status.brief().lower())
                exit(0)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
    sys.exit(0)

#    print ("\n")
    result = ofswitch.get_ports_brief_info()
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("'%s' ports:" % name)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    
    
    '''
    print ("\n")
    tableid = 0
    result = ofswitch.get_operational_flows(tableid)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' operational flows:" % tableid)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    print ("\n")
    tableid = 0
    result = ofswitch.get_operational_flows_ovs_syntax(tableid, sort=True)
    status = result[0]
    
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' operational flows:" % tableid)
        flist = result[1]
        for f in flist:
            print json.dumps(f)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    print ("\n")
    tableid = 0
    result = ofswitch.get_configured_flows(tableid)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' configured flows:" % tableid)
        info = result[1]
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)

    print ("\n")
    tableid = 0
    result = ofswitch.get_configured_flows_ovs_syntax(tableid, sort=True)
    status = result[0]
    
    if(status.eq(STATUS.OK) == True):
        print ("Table '%s' configured flows:" % tableid)
        flist = result[1]
        for f in flist:
            print json.dumps(f)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    '''
