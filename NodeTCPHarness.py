import sys
import time

from NodeTCPLib import NodeTCPInstance

def test_sys_start_request():
    """
    """
    success = False
    
    # Create a node TCP instance
    session = NodeTCPInstance("127.0.0.1", 3000)
    
    lwc_id = session.create_lightweight_connection(0, 0)
    if lwc_id == -1:
        print("INFO: could not create lightweight connection, terminating early")
        early_termination(session)
        return success
    else:
        print("INFO: started comms with node with lwcid %d" % (lwc_id))
        
    # Provides time to tinker with WireShark    
    time.sleep(2)
    
    # Send SysStartRequest
    res = session.sys_start_request(lwc_id)
    print("INFO: SysStartResponse -> %s" % res)
    
    # Provides time to tinker with WireShark
    time.sleep(2)
    
    session.close_heavyweight_connection(lwc_id)
    
    # Close the socket
    session.close_socket()
    
    success = True
    
    return success

def test_get_blocks():
    """
    """
    success = False
    
    # Create a node TCP instance
    session = NodeTCPInstance("127.0.0.1", 3000)
    
    lwc_id = session.create_lightweight_connection(0, 0)
    if lwc_id == -1:
        print("INFO: could not create lightweight connection, terminating early")
        early_termination(session)
        return success
    else:
        print("INFO: started comms with node with lwcid %d" % (lwc_id))
    
    # Provides time to tinker with WireShark
    time.sleep(2)
    
    # GetBlocks
    # Dummy values for testng, these need to change based on the current blockchain
    hash_new = b"\x61\x3c\x9c\x67\xe1\x77\x5d\x6c\x54\xe2\x17\xea\x12\xff\xbd\x04\xdb\xac\x5e\x9f\x26\xe7\x42\x56\x40\x5b\x09\xa7"
    hash_old = b"\xff\x31\x1b\xc9\x1c\xec\xb0\x4d\x22\xd9\xe9\x07\x8f\x3a\x93\x51\x43\x08\xf9\x51\xcd\x88\x53\x84\x88\x4b\x26\xf1"
    blocks = session.get_blocks(lwc_id, hash_old, hash_new)
    
    #TODO: add some kind of response value checking
    print("INFO: Blocks -> %s" % blocks)
    
    # Provides time to tinker with WireShark
    time.sleep(2)
    
    session.close_heavyweight_connection(lwc_id)
    
    # Close the socket
    session.close_socket()
    
    success = True
    
    return success
    

def early_termination(session, lwc_id = None):
    """
    """
    
    # Close the connection
    if lwc_id is not None:
        session.close_heavyweight_connection(lwc_id)
    
    # Close the socket
    session.close_socket()

if __name__ == "__main__":
    test_sys_start_request()

