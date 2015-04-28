#!/usr/bin/python

import time
import json


from framework.controller.controller import Controller
from framework.openflowdev.ofswitch import OFSwitch
from framework.openflowdev.ofswitch import FlowEntry
from framework.openflowdev.ofswitch import Instruction
from framework.openflowdev.ofswitch import OutputAction
from framework.openflowdev.ofswitch import Match

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

    ctrl = Controller(ctrlIpAddr, ctrlPortNum, ctrlUname, ctrlPswd)
    ofswitch = OFSwitch(ctrl, nodeName)

    # --- Flow Match: Ethernet Type
    #                 IP DSCP
    #                 IP ECN
    #                 IPv6 Source Address
    #                 IPv6 Destination Address
    #                 IPv6 Flow Label
    #                 ICMPv6 type
    #                 ICMPv6 Code
    #                 Metadata
    eth_type = 34525 # IPv6 protocol (0x86dd)
    ip_dscp = 60
    ip_ecn = 3
    ipv6_src = "1234:5678:9ABC:DEF0:FDCD:A987:6543:210F/76"
    ipv6_dst = "2000:2abc:edff:fe00::3456/94"
    ipv6_flabel = 15
    ip_proto = 58 # ICMPv6
    icmpv6_type = 6
    icmpv6_code = 3
    metadata = "0x0123456789ABCDEF"
    
    # --- Flow Actions: Output (CONTROLLER)
    output_port = "CONTROLLER"
    
    print ("<<< 'Controller': %s, 'OpenFlow' switch: '%s'" % (ctrlIpAddr, nodeName))
    
    print "\n"
    print ("<<< Set OpenFlow flow on the Controller")
    print ("        Match:  Ethernet Type (%s)\n"
           "                IP DSCP (%s)\n"
           "                IP ECN (%s)\n"
           "                IPv6 Source Address (%s)\n"
           "                IPv6 Destination Address (%s)\n"
           "                IPv6 Flow Label (%s)\n"
           "                ICMPv6 Type (%s)\n"
           "                ICMPv6 Code (%s)\n" 
           "                Metadata (%s)"             % (hex(eth_type), ip_dscp, ip_ecn,
                                                          ipv6_src, ipv6_dst, ipv6_flabel,
                                                          icmpv6_type, icmpv6_code, metadata))
    print ("        Actions: 'Output' (to %s)" % output_port)
    
    
    time.sleep(rundelay)
    
    
    flow_entry = FlowEntry()
    table_id = 0
    flow_id = 26
    flow_entry.set_flow_name(flow_name = "demo20.py")
    flow_entry.set_flow_id(flow_id)
    flow_entry.set_flow_priority(flow_priority = 1019)
    flow_entry.set_flow_cookie(cookie = 250)
    flow_entry.set_flow_cookie_mask(cookie_mask = 255)
    flow_entry.set_flow_hard_timeout(hard_timeout = 1200)
    flow_entry.set_flow_idle_timeout(idle_timeout = 3400)
    
    # --- Instruction: 'Apply-action'
    #     Actions:     'Output'
    instruction = Instruction(instruction_order = 0)
    action = OutputAction(action_order = 0, port = output_port)
    instruction.add_apply_action(action)
    flow_entry.add_instruction(instruction)
    
    # --- Match Fields: Ethernet Type
    #                   IP DSCP
    #                   IP ECN
    #                   IPv6 Source Address
    #                   IPv6 Destination Address
    #                   IPv6 Flow Label
    #                   IP protocol number (ICMPv6)
    #                   ICMPv6 Type
    #                   ICMPv6 Code
    #                   Metadata
    match = Match()    
    match.set_eth_type(eth_type)
    match.set_ip_dscp(ip_dscp)
    match.set_ip_ecn(ip_ecn)   
    match.set_ipv6_src(ipv6_src)
    match.set_ipv6_dst(ipv6_dst)
    match.set_ipv6_flabel(ipv6_flabel)
    match.set_ip_proto(ip_proto)
    match.set_icmpv6_type(icmpv6_type)
    match.set_icmpv6_code(icmpv6_code)
    match.set_metadata(metadata)    
    flow_entry.add_match(match)
    
    
    print ("\n")
    print ("<<< Flow to send:")
    print flow_entry.get_payload()
    time.sleep(rundelay)
    result = ofswitch.add_modify_flow(flow_entry)
    status = result[0]    
    if(status.eq(STATUS.OK) == True):
        print ("<<< Flow successfully added to the Controller")
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.detail())
        exit(0)
    
    
    print ("\n")    
    print ("<<< Get configured flow from the Controller")    
    time.sleep(rundelay)
    result = ofswitch.get_configured_flow(table_id, flow_id)
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("<<< Flow successfully read from the Controller")
        print ("Flow info:")
        flow = result[1]
        print json.dumps(flow, indent=4)
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    print ("<<< Delete flow with id of '%s' from the Controller's cache "
           "and from the table '%s' on the '%s' node" % (flow_id, table_id, nodeName))
    time.sleep(rundelay)
    result = ofswitch.delete_flow(flow_entry.get_flow_table_id(), flow_entry.get_flow_id())
    status = result[0]
    if(status.eq(STATUS.OK) == True):
        print ("<<< Flow successfully removed from the Controller")
    else:
        print ("\n")
        print ("!!!Demo terminated, reason: %s" % status.brief().lower())
        exit(0)
    
    
    print ("\n")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print (">>> Demo End")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    