#!/usr/bin/python

"""
@authors: Sergei Garbuzov

"""

import time
import json


from framework.controller.controller import Controller
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
        nodeName = d['nodeName']
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
    print ("<<< Get information about OpenFlow node '%s'" % nodeName)
    time.sleep(rundelay)
    ofswitch = OFSwitch(ctrl, nodeName)
    result = ofswitch.get_switch_info()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Node '%s' generic info:" % nodeName)
        info = result.get_data()
        print json.dumps(info, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    print ("\n")
    result = ofswitch.get_features_info()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Node '%s' features:" % nodeName)
        features = result.get_data()
        print json.dumps(features, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    result = ofswitch.get_ports_list()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        ports = result.get_data()
        print ("Node '%s' ports list:" % nodeName)
        print json.dumps(ports, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    result = ofswitch.get_ports_brief_info()
    status = result.get_status()
    if(status.eq(STATUS.OK) == True):
        print ("Node '%s' ports brief information:" % nodeName)
        info = result.get_data()
        print json.dumps(info, indent=4, sort_keys=True)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    