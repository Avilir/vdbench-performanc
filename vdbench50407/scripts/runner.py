#!/usr/bin/env python3

'''
    This script is used to run the vdbench benchmark.
    
    Author : Avi Liani <alayani@redhat.com>
    Created : Aug-29-2019
    
    The script accept the number of volumes to run against,
    desirable volume type and the name of the pre-define workload.
    
    it check the type of the volumes (Block devices / rbd mounts)
'''

import sys
import os
from optparse import OptionParser  # Option,

# The Version of this script.
VERSION = '0.1'

# The Script name.
PROG = os.path.basename(os.path.splitext(__file__)[0])

# The Description of this script for the Usage message.
description = """Running vdbench benchmark"""

base_dir = "/opt/vdbench"
base_config = base_dir + "/logs"

test2run = None  # predefine test that will run
type2run = "B"  # type of volumes to run against
vol2run = 1  # the number of volumes to run against

def build_cmd_parameters():
    global parser
    parser = OptionParser(
        usage='usage: %prog -r <regex> | --regex=<regex> [OPTIONS]',
        version='%s %s' % (PROG, VERSION),
        description=description)

    parser.add_option(
        '-f', '--files',
        type="string",
        dest='test2run',
        metavar='FILE',
        default='Basic',
        help='the name of the test to run')

    parser.add_option(
        '-t', '--type',
        type='string',
        dest='type2run',
        metavar='TYPE',
        default='B',
        help='the desirable volumes type to run against')

    parser.add_option(
        '-n', '--volnums',
        type='int',
        dest='vol2run',
        metavar='NUMBER',
        default=1,
        help='number of volumes to run against')

''' 
    parsing the input parameters.
    parameters order is mandatory :
    First parameter is : pre-define workload (default
    Second parameter is : Volume type (F / B)
'''
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    print ("Error: No input file !!!")
    sys.exit(1)

'''
    This function return the type of the volums (B/F)
    B - Block device which mean that raw devices test should be run
    F - RBD devices which mean that File system test should be run
    
    if no volumes found it return None
'''
def vols_type():
    devs = None
    
    ''' check if Block devices '''
    results = os.popen('ls /dev/block* 2>/dev/null').read()
    if results != '':
        devs = "B"
    
    ''' check if Mount devices '''
    results = os.popen('ls /dev/rbd* 2>/dev/null').read()
    if results != '':
        devs = "F"

    return devs

def file_vols():
    devs = os.popen('ls /dev/rbd* 2>/dev/null').read().strip().split('\n')
    return devs

def block_vols():
    devs = os.popen('ls /dev/block* 2>/dev/null').read().strip().split('\n')
    return devs

if __name__ == "__main__":
    
    # building the input parameters object.
    build_cmd_parameters()
    
        # check if no arguments was given.
    if len(sys.argv) == 1:
        parser.parse_args(['--help'])

    # Parse the command line parameters
    OPTIONS, args = parser.parse_args()

    # The --file (-f) parameter is mandatory.
    if OPTIONS.test2run is None:
        print('Error: the [-f | --file] parameter is mandatory !\n')
        parser.parse_args(['--help'])
    else:
        # Verify that the predefine test file is exist. if not, exit with error.
        test2run = base_dir + "/" + OPTIONS.test2run
        if os.path.isfile(test2run) is not True:
            print('Error: Test to run ({}) is not exist'.format(test2run))
            sys.exit(1)
            
    # verify the number of volumes to run against.
    if OPTIONS.vol2run > 10:
            print('Error: Max Number of volumes is 10')
            sys.exit(1)
            
    
    # verify that the input volume type is valid
    if OPTIONS.type2run.upper() not in ['B', 'F']:
        print("Error: Invalid volume type (valid options are : B / F)")
        sys.exit(1)
        
    # verify that the system have the desirable volumes type 
    if vols_type() != OPTIONS.type2run.upper():
        print("Error: volumes type ({}) is not present on the system!".format(OPTIONS.type2run))
        sys.exit(1)
    
    if OPTIONS.type2run.upper() == "B":
        vol2run = int(len(block_vols()))
    elif OPTIONS.type2run.upper() == "F":
        vol2run = int(len(file_vols()))
        
    # verify the the system have enough volumes
    if vol2run < OPTIONS.vol2run:
        print("Error: not enough volumes on the system")
        sys.exit(1)
    
    '''
        Creating include file in the format :
    
        for raw devices (B - block)
        sd=sd01,lun=/dev/block0,size=<vol size>,openflags=o_direct
        ...
        sd=sd<n>,lun=/dev/block<n>,size=<vol size>,openflags=o_direct
        
        for mount devices (F - File) 
        extra parameter will be taken from the test file.
        fsd=fsd01,anchor=<mp>,....
        ...
        fsd=fsd<n>,anchor=<mp>,...
    '''
    include_file = open(base_dir+"/conf/include_disk","w")
    
    if OPTIONS.type2run.upper() == "B":
        counter = 0
        for dev in block_vols():
            dev_size = os.popen('lsblk {} 2>/dev/null | grep disk'.format(dev)).read().strip().split()[3]
            include_file.write("sd=sd{:02d},lun={},size={},openflags=o_direct\n".format(counter+1, dev, dev_size))
            counter = counter + 1
            if counter == OPTIONS.vol2run:
                break
    

    include_file.close()

    tst_file = open(test2run,"r")
    
    test_file = open(base_dir+"/conf/running_test","w")
    
    test_file.write("\ninclude include_disk\n\n")
    line = tst_file.readline()
    while line:
        if "sd=sd" not in line[0:5]:
            test_file.write(line)
        line = tst_file.readline()

    
    
    tst_file.close()
    test_file.close()
    