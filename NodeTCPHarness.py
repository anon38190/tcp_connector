import sys
import time

from NodeTCPLib import NodeTCPInstance

def test_version_request():
    """
    """
    success = False;
    
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
    
    version = session.version_req(lwc_id)
    print("INFO: VersionReq -> %s" % version)

    # Provides time to tinker with WireShark
    time.sleep(2)
    
    session.close_heavyweight_connection(lwc_id)
    
    # Close the socket
    session.close_socket()
    
    success = True
    
    return success

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
    hash_new = b"\x51\x17\xb9\x2d\x4d\x63\xa5\xfe\x6f\xf1\xdb\x90\x4b\x47\xfe\x8e\x30\x43\x24\xe2\xe4\x74\x2b\x26\xf1\xb0\x71\x1b"
    hash_old = b"\xa6\xa7\x18\xc4\x46\x8b\x37\x43\x5e\x5f\x42\x30\xe3\x0f\xa9\x6b\xb7\x9b\xd9\x8e\x48\x15\xbd\x59\xbf\x55\xec\xe8"
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
    test_version_request()

