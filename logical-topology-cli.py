#!/usr/bin/python
#
# Script to read ACI logical topology data from a JSON file, created by logical-topology-convert-output.py.
# Have some nice functions to display the output.
#
#####################
# Imports
#####################
#
# list of packages that should be imported for this code to work
import pdb
import json
import readline
import os
import sys
import re

######################################
# Classes
######################################
#
######################################
# Functions
######################################
#
def collect_string_input(prompt, min_chars = 1, max_chars = 1, default_value = ''):
    '''
    Function to collect user input from the command line. Input will be treated as string and check if length is in the range min_chars to max_chars
    '''
    input = ''
    indent = '    '
    if default_value == '':
        prompt = indent+prompt+" >> "
        while True:
            input = raw_input(prompt) or default_value
            input = input.strip()
            if min_chars <= len(input) <= max_chars:
                break
            else:
                print "Sorry, input length should be in the range ["+str(min_chars)+","+str(max_chars)+"]"
                continue
            
    else:
        prompt = indent+prompt+"["+default_value+"] >> "
        while True:
            input = raw_input(prompt) or default_value
            input = input.strip()
            if min_chars <= len(input) <= max_chars:
                break
            else:
                print "Sorry, input length should be in the range ["+str(min_chars)+","+str(max_chars)+"]"
                continue
    return str(input.lower())
# end of function collect_string_input

def reset_session_vars():
    global session_vars
    session_vars = { x:'' for x in session_vars }
# end of function reset_session_vars()

def print_session_vars():
    print "session_vars: "+session_vars['tenant']+' >> '+session_vars['vrf']+' >> '+session_vars['bd']
# end of function print_session_vars()

def get_searchitem_list():
    # returns a dict, key is the index, value is the searchitem
    si_index = 0
    si_list = {}
    si_list = { 'v': 'vlan', 'p': 'port', 'f': 'fulltext (Name, Desc)' }
    return si_list
# end of function tenant_list()

def get_tenant_list():
    # returns a dict, key is the index, value is the tenant name from acitop
    tn_list = []
    for tenant_dn,tenant in acitop.iteritems():
        tn_list.append(tenant['name'])
    return sorted(tn_list)
# end of function tenant_list()

def get_tenant_details():
    details = {}
    try:
        details['0'] = { 'attr': 'Name', 'val': acitop[session_vars['tenant']]['name'] }
        details['1'] = { 'attr': 'Desc', 'val': acitop[session_vars['tenant']]['desc'] }
    except KeyError:
        pass
    return details
# end of function get_tenant_details()

def get_vrf_list():
    # returns a dict, key is the index, value is the vrf name from acitop
    vrf_list = []
    for vrf_dn, vrf in acitop[session_vars['tenant']]['vrfs'].iteritems():
        vrf_list.append(vrf['name'])
    return sorted(vrf_list)
# end of function get_vrf_list()

def get_vrf_details():
    details = {}
    try:
        details['0'] = { 'attr': 'Name', 'val': acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['name'] }
        details['1'] = { 'attr': 'Desc', 'val': acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['desc'] }
    except KeyError:
        pass
    return details
# end of function get_tenant_details()

def get_bd_list():
    # returns a dict, key is the index, value is the bd name from acitop
    bd_list = []
    try:
        for bd_dn,bd in acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['bds'].iteritems():
            bd_list.append(bd['name'])
    except KeyError:
        pass
    return sorted(bd_list)
# end of function get_bd_list()

def get_bd_details():
    details = {}
    try:
        details['0'] = { 'attr': 'Name', 'val': acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['bds'][session_vars['bd']]['name'] }
        details['1'] = { 'attr': 'Desc', 'val': acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['bds'][session_vars['bd']]['desc'] }
        details['2'] = { 'attr': 'Arp Flooding', 'val': acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['bds'][session_vars['bd']]['arpFlood'] }
        details['3'] = { 'attr': 'Limit IP Learning', 'val': acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['bds'][session_vars['bd']]['limitIpLearnToSubnets'] }
        details['4'] = { 'attr': 'multiDstPktAct', 'val': acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['bds'][session_vars['bd']]['multiDstPktAct'] }
        details['5'] = { 'attr': 'unicastRoute', 'val': acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['bds'][session_vars['bd']]['unicastRoute'] }
        details['6'] = { 'attr': 'unkMacUcastAct', 'val': acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['bds'][session_vars['bd']]['unkMacUcastAct'] }
        details['7'] = { 'attr': 'unkMcastAct', 'val': acitop[session_vars['tenant']]['vrfs'][session_vars['vrf']]['bds'][session_vars['bd']]['unkMcastAct'] }
    except KeyError:
        pass
    return details
# end of function get_bd_details()

def get_ap_list():
    # returns a dict, key is the index, value is the ap name from acitop
    ap_list = []
    try:
        for ap_dn,ap in acitop[session_vars['tenant']]['aps'].iteritems():
            ap_list.append(ap['name'])
    except KeyError:
        pass
    return sorted(ap_list)
# end of function get_ap_list()

def get_ap_details():
    details = {}
    try:
        details['0'] = { 'attr': 'Name', 'val': acitop[session_vars['tenant']]['aps'][session_vars['ap']]['name'] }
        details['1'] = { 'attr': 'Name', 'val': acitop[session_vars['tenant']]['aps'][session_vars['ap']]['desc'] }
    except KeyError:
        pass
    return details
# end of function get_ap_details()

def get_epg_list():
    # returns a dict, key is the index, value is the epg name from acitop
    epg_list = []
    try:
        for epg_dn,epg in acitop[session_vars['tenant']]['aps'][session_vars['ap']]['epgs'].iteritems():
            epg_list.append(epg['name'])
    except KeyError:
        pass
    return sorted(epg_list)
# end of function get_epg_list()

def get_epg_details():
    details = {}
    try:
        details['0'] = { 'attr': 'Name', 'val': acitop[session_vars['tenant']]['aps'][session_vars['ap']]['epgs'][session_vars['epg']]['name'] }
        details['1'] = { 'attr': 'Desc', 'val': acitop[session_vars['tenant']]['aps'][session_vars['ap']]['epgs'][session_vars['epg']]['desc'] }
        details['2'] = { 'attr': 'BD', 'val': acitop[session_vars['tenant']]['aps'][session_vars['ap']]['epgs'][session_vars['epg']]['bdDn'] }
        details['3'] = { 'attr': 'Isolated', 'val': acitop[session_vars['tenant']]['aps'][session_vars['ap']]['epgs'][session_vars['epg']]['pcEnfPref'] }
    except KeyError:
        pass
    return details
# end of function get_epg_details()

def get_port_list():
    # returns a dict, key is the index, value is the epg name from acitop
    port_list = []
    try:
        for port_dn,port in acitop[session_vars['tenant']]['aps'][session_vars['ap']]['epgs'][session_vars['epg']]['static_ports'].iteritems():
            port_list.append(port['tdn'])
    except KeyError:
        pass
    return sorted(port_list)
# end of function get_port_list()

def get_help_details():
    details = {}
    details['1'] = { 'attr': 'h', 'val': '(h)elp, this screen' }
    details['2'] = { 'attr': 't', 'val': 'List of (t)enants' }
    details['2'] = { 'attr': 'td', 'val': '(t)enants (d)etails, including list of vrfs or aps' }
    details['3'] = { 'attr': 'v', 'val': 'List of (v)rfs, only if tenant is set' }
    details['4'] = { 'attr': 'vd', 'val': '(v)rf (d)etails, including list of bds, only if tenant and vrf is set' }
    details['4'] = { 'attr': 'bd', 'val': '(b)d (d)etails, only if tenant, vrf and bd is set' }
    details['5'] = { 'attr': 'a', 'val': 'List of (a)ps, only if tenant is set' }
    details['6'] = { 'attr': 'ad', 'val': '(a)p (d)etails, incl. list of epgs, only if tenant and ap is set' }
    details['6'] = { 'attr': 'ed', 'val': '(e)pg (d)etails, incl. list of ports, only if tenant, ap and epg is set' }
    details['7'] = { 'attr': 's', 'val': '(s)earch' }
    details['8'] = { 'attr': 'b', 'val': '(b)ack' }
    details['9'] = { 'attr': 'q', 'val': '(q)uit' }
    return details
# end of function get_epg_details()

def print_generic_menu(breadcrumb, details, index_list):
    print "{:#>102.102}".format('')
    print "# {:99.99}#".format('>> '+breadcrumb)
    print "#{:->100.100}#".format('')
    if len(details) > 0:
        # print details
        print "# {:>10.10} | {:85.85} #".format('Attribute', 'Value')
        print "#{:->100.100}#".format('')
        for k in sorted(details.keys()):
            print "# {:>10.10} | {:85.85} #".format(details[k]['attr'],details[k]['val'])
        print "#{:->100.100}#".format('')

    if len(index_list) > 0:
        if str(type(index_list)) == "<type 'dict'>":
            print "# {:>10.10} | {:85.85} #".format('Index', 'Value')
            print "#{:->100.100}#".format('')
            for k in sorted(index_list.keys()):
                print "# {:>10.10} | {:85.85} #".format(k,index_list[k])
            print "#{:->100.100}#".format('')
        elif str(type(index_list)) == "<type 'list'>":
            print "# {:>10.10} | {:85.85} #".format('Index', 'Value')
            print "#{:->100.100}#".format('')
            for index,item in enumerate(index_list):
                print "# {:>10} | {:85.85} #".format(index,item)
            print "#{:->100.100}#".format('')

    print "{:#>102.102}".format('')
# end of print_generic_menu()

def search_results():
    # search for a vlan or a port by string in session_vars['s_str']
    result_list = []
    if session_vars['s_item'] == 'vlan':
        # iterate over everything an note where the searchstring matches
        for tenant_dn,tenant in acitop.iteritems():
            for ap_dn,ap in tenant['aps'].iteritems():
                for epg_dn,epg in ap['epgs'].iteritems():
                    for port_dn,port in epg['static_ports'].iteritems():
                        if re.search(session_vars['s_str'],port['encap']):
                            result_list.append(tenant['name']+' >> '+ap['name']+' >> '+epg['name']+' >> '+port['encap'])
    elif session_vars['s_item'] == 'port':
        # iterate over everything an note where the searchstring matches
        for tenant_dn,tenant in acitop.iteritems():
            for ap_dn,ap in tenant['aps'].iteritems():
                for epg_dn,epg in ap['epgs'].iteritems():
                    for port_dn,port in epg['static_ports'].iteritems():
                        if re.search(session_vars['s_str'],port['tdn']):
                            result_list.append(tenant['name']+' >> '+ap['name']+' >> '+epg['name']+' >> '+port['tdn'])
    elif session_vars['s_item'] == 'fulltext':
        # iterate over everything an note where the searchstring matches
        for tenant_dn,tenant in acitop.iteritems():
            if re.search(session_vars['s_str'],tenant['name']):
                result_list.append(tenant['name'])
            if re.search(session_vars['s_str'],tenant['desc']):
                result_list.append(tenant['name'])
            for ap_dn,ap in tenant['aps'].iteritems():
                if re.search(session_vars['s_str'],ap['name']):
                    result_list.append(tenant['name']+' >> '+ap['name'])
                if re.search(session_vars['s_str'],ap['desc']):
                    result_list.append(tenant['name']+' >> '+ap['name'])
                for epg_dn,epg in ap['epgs'].iteritems():
                    if re.search(session_vars['s_str'],epg['name']):
                        result_list.append(tenant['name']+' >> '+ap['name']+' >> '+epg['name'])
                    if re.search(session_vars['s_str'],epg['desc']):
                        result_list.append(tenant['name']+' >> '+ap['name']+' >> '+epg['name'])
                    for port_dn,port in epg['static_ports'].iteritems():
                        if re.search(session_vars['s_str'],port['tdn']):
                            result_list.append(tenant['name']+' >> '+ap['name']+' >> '+epg['name']+' >> '+port['tdn'])
            for vrf_dn,vrf in tenant['vrfs'].iteritems():
                if re.search(session_vars['s_str'],vrf['name']):
                    result_list.append(tenant['name']+' >> '+vrf['name'])
                if re.search(session_vars['s_str'],vrf['desc']):
                    result_list.append(tenant['name']+' >> '+vrf['name'])
                for bd_dn,bd in vrf['bds'].iteritems():
                    if re.search(session_vars['s_str'],bd['name']):
                        result_list.append(tenant['name']+' >> '+vrf['name']+' >> '+bd['name'])
                    if re.search(session_vars['s_str'],bd['desc']):
                        result_list.append(tenant['name']+' >> '+vrf['name']+' >> '+bd['name'])

    return sorted(result_list)
# end of function search_results()

def menu_tenant():
    # display tenant menu and read user choice
    reset_session_vars()
    print_generic_menu('Tenants', [], get_tenant_list())
    choice = collect_string_input('h(elp), index for details ', 1, 3, '')
    try:
        session_vars['tenant'] = 'uni/tn-' + get_tenant_list()[int(choice)]
        choice = 'td'
    except KeyError:
        print "choice not valid!"
        choice = 't'
    except ValueError:
        pass
    return choice
# end of function tenant_menu

def menu_tenant_details():
    session_vars['prev_choice'] = choice
    details = get_tenant_details()
    if session_vars['vora'] == 'vrf':
        index_list = get_vrf_list()
        print_generic_menu(session_vars['tenant']+'  >> VRFs', details, index_list)
        local_choice = collect_string_input('(t)enants, (q)uit, index for tenant details ', 1, 3, 'q')
        try:
            session_vars['vrf'] = session_vars['tenant']+'/ctx-'+index_list[int(local_choice)]
            local_choice = 'vd'
        except (KeyError, ValueError):
            pass
        return local_choice
    elif session_vars['vora'] == 'ap':
        index_list = get_ap_list()
        print_generic_menu(session_vars['tenant']+'  >> APs', details, index_list)
        local_choice = collect_string_input('(t)enants, (q)uit, index for tenant details ', 1, 3, 'q')
        try:
            session_vars['ap'] = session_vars['tenant']+'/ap-'+index_list[int(local_choice)]
            local_choice = 'ad'
        except (KeyError, ValueError):
            pass
        return local_choice
    else:
        index_list = { 'v': 'vrf', 'a': 'ap' }
        print_generic_menu(session_vars['tenant'], details, index_list)
        local_choice = collect_string_input('h(elp), index for details ', 1, 3, '')
        if local_choice in index_list.keys():
            session_vars['vora'] = index_list[local_choice]
            local_choice = 'td'
        return local_choice
# end of function tenant_menu_details

def menu_vrf():
    session_vars['prev_choice'] = choice
    details = get_vrf_details()
    index_list = get_bd_list()
    print_generic_menu(session_vars['tenant']+' >> '+session_vars['vrf'], details, index_list)
    local_choice = collect_string_input('h(elp), index for details ', 1, 3, '')
    try:
        session_vars['bd'] = session_vars['tenant']+'/BD-'+index_list[int(local_choice)]
        local_choice = 'b'
    except (KeyError, ValueError):
        pass
    return local_choice
# end of function menu_vrf

def menu_vrf_details():
    session_vars['prev_choice'] = choice
    details = get_vrf_details()
    index_list = get_bd_list()
    print_generic_menu(session_vars['tenant']+' >> '+session_vars['vrf'], details, index_list)
    local_choice = collect_string_input('h(elp), index for details ', 1, 3, '')
    try:
        session_vars['bd'] = session_vars['tenant']+'/BD-'+index_list[int(local_choice)]
        local_choice = 'bd'
    except (KeyError, ValueError):
        pass
    return local_choice
# end of function menu_vrf_details

def menu_bd_details():
    session_vars['prev_choice'] = choice
    details = get_bd_details()
    index_list = []
    print_generic_menu(session_vars['tenant']+' >> '+session_vars['vrf']+' >> '+session_vars['bd'], details, index_list)
    local_choice = collect_string_input('h(elp), index for details ', 1, 3, '')
    return local_choice
# end of function menu_vrf_details

def menu_ap():
    session_vars['prev_choice'] = choice
    details = get_tenant_details()
    index_list = get_ap_list()
    print_generic_menu(session_vars['tenant']+' >> APs', details, index_list)
    local_choice = collect_string_input('h(elp), index for details ', 1, 3, '')
    try:
        session_vars['ap'] = session_vars['tenant']+'/ap-'+index_list[int(local_choice)]
        local_choice = 'ad'
    except (KeyError, ValueError):
        pass
    return local_choice
# end of function menu_ap

def menu_ap_details():
    session_vars['prev_choice'] = choice
    details = get_ap_details()
    index_list = get_epg_list()
    print_generic_menu(session_vars['tenant']+' >> '+session_vars['ap'], details, index_list)
    local_choice = collect_string_input('h(elp), index for details ', 1, 3, '')
    try:
        session_vars['epg'] = session_vars['ap']+'/epg-'+index_list[int(local_choice)]
        local_choice = 'ed'
    except (KeyError, ValueError):
        pass
    return local_choice
# end of function menu_ap_details

def menu_epg_details():
    session_vars['prev_choice'] = choice
    details = get_epg_details()
    index_list = get_port_list()
    print_generic_menu(session_vars['tenant']+' >> '+session_vars['ap']+' >> '+session_vars['epg'], details, index_list)
    local_choice = collect_string_input('h(elp) ', 1, 3, '')
    return local_choice
# end of function menu_epg_details

def menu_searchitem():
    # display menu of seearchable items
    print_generic_menu('Search VLAN / Port / Full text', [], get_searchitem_list())
    local_choice = collect_string_input('h(elp), index for details ', 1, 3, '')
    if local_choice == 'v':
        local_choice = 'ss'
        session_vars['s_item'] = 'vlan'
    elif local_choice == 'p':
        local_choice = 'ss'
        session_vars['s_item'] = 'port'
    elif local_choice == 'f':
        local_choice = 'ss'
        session_vars['s_item'] = 'fulltext'
    return local_choice
# end of function menu_search

def menu_searchstr():
    # get user input for search string
    local_choice = collect_string_input('Search string ', 1, 20, '')
    session_vars['s_str'] = local_choice
    return 'sr'
# end of function menu_search

def menu_searchresult():
    # get user input for search string
    details = []
    index_list = search_results()
    print_generic_menu('Search '+' >> '+session_vars['s_item']+' >> '+session_vars['s_str'], details, index_list)
    local_choice = collect_string_input('h(elp)', 1, 3, '')
    return local_choice
# end of function menu_ap

def menu_help():
    details = get_help_details()
    index_list = []
    print_generic_menu('Help '+' >> ', details, index_list)
    choice = collect_string_input('h(elp) ', 1, 3, '')
    return choice
# end of function menu_ap


# Back to previous menu
def back():
    return session_vars['prev_choice']
    
# Exit program
def exit():
    sys.exit()

######################################
# Variables
######################################
#
json_file = "/data/ansible/aci-logical-topology/mpdc/data/json-mpdc.txt"
#
# Menu definition
menu_actions = {
    't': menu_tenant,
    'td': menu_tenant_details,
    'v': menu_vrf,
    'bd': menu_bd_details,
    'vd': menu_vrf_details,
    'a': menu_ap,
    'ad': menu_ap_details,
    'ed': menu_epg_details,
    's': menu_searchitem,
    'ss': menu_searchstr,
    'sr': menu_searchresult,
    'h': menu_help,
    'b': back,
    'q': exit
}

session_vars = {
    'tenant': '',
    'vora': '',
    'vrf': '',
    'bd': '',
    'ap': '',
    'epg': '',
    's_item': '',
    's_str': '',
    'prev_choice': ''
}

choice = ''
#
######################################
# Main program
######################################
#
# open JSON file and read content
jf = open(json_file, 'r')
acitop = json.load(jf)
jf.close()

# pdb.set_trace()

while True:
    os.system('clear')
    try:
        choice = menu_actions[choice]()
    except KeyError:
        print "Invalid selection ["+choice+"], please try again.\n"
        choice = menu_actions['t']()
# end of main program
