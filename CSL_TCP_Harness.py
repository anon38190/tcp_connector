#NOTES: Splitting the generation and build allows for user modification (if 
#       desired)

from CSL_Application_Layer import ApplicationLayer
from CSL_Status_Codes import *

import CSL_Layers

class Harness(ApplicationLayer):
    
    def __init__(self,):
        """
        """
        super().__init__()
        
    @CSL_Layers.connect_dec
    def connect(self, ip, port, ep_id):
        """
        """
        # All of the connection work is done at a lower layer
        print("INFO: Connecting to node...")

    @CSL_Layers.disconnect_dec   
    def disconnect(self):
        """
        """
        # All of the disconnection work is done at a lower layer
        print("INFO: Disconnecting from node...")
        
    @CSL_Layers.generate_msg_dec
    def generate_msg(self, **kwargs):
        """
        """
        # All the message generation is done at a lower layer
        print("INFO: Generating a CSL-compliant message...")
        
    def assemble_msg(self, msg_components):
        """
        """
        msg = b""
        
        # Lower layers have taken care of ordering
        for c in msg_components:
            msg = b"%s%s" % (msg, c)
            
        return msg
            
    @CSL_Layers.send_msg_dec
    def send_msg(self, msg):
        """
        """
        # All the transport details are handled at a lower layer
        print("INFO: Sending the message...")
      
#TODO: This appears to follow the documentation, but doesn't seem to work...  
def test_peerstate():
    """
    """
    # Create the harness instance
    h = Harness()
    
    # Connect to a node
    h.connect("127.0.0.1", 3000, 0)
    
    # Generate a "PeerState" message
    msg_components = h.generate_msg(msg_type = "PeerState", protocolversion=None)
    
    # Modify the message here (for testing)
    # See https://construct.readthedocs.io/en/latest/basics.html#fields for how 
    # to parse, mutate, then rebuild a construct object
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg(msg)
    
    print("INFO: response -> %s" % res)
    
    # Close the node connection
    h.disconnect()

#TODO: This appears to follow the documentation, but doesn't seem to work...        
def test_getheaders():
    """
    """
    # Create the harness instance
    h = Harness()
    
    # Connect to a node
    h.connect("127.0.0.1", 3000, 0)
    
    # Generate a "GetHeaders" message
    msg_components = h.generate_msg(msg_type = "GetHeaders",
                                    old_hash = [0x0f, 0xbb, 0xf2, 0x7a, 0xa3, 0x99, 0x84, 0x90, 0xca, 0x4e, 0x94, 0x56, 0xf2, 0xb9, 0x2f, 0x82, 0xbc, 0x9b, 0x10, 0xff, 0x37, 0xc9, 0x46, 0xd0, 0xc7, 0xb4, 0x5f, 0xc8],
                                    new_hash = [0xe4, 0x30, 0xef, 0x7a, 0xe5, 0x70, 0x4e, 0x01, 0xbc, 0xa5, 0x8e, 0xd3, 0xea, 0x82, 0x77, 0x46, 0x51, 0x15, 0xd2, 0x40, 0xfc, 0x67, 0x57, 0x93, 0x07, 0x30, 0xe9, 0x04])
    
    # Modify the message here (for testing)
    # See https://construct.readthedocs.io/en/latest/basics.html#fields for how 
    # to parse, mutate, then rebuild a construct object
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg(msg)
    
    print("INFO: response -> %s" % res)
    
    # Close the node connection
    h.disconnect()

def test_versionreq():
    """
    """
    # Create the harness instance
    h = Harness()
    
    # Connect to a node
    h.connect("127.0.0.1", 3000, 0)
    
    # Generate a "VersionReq" message
    msg_components = h.generate_msg(msg_type = "VersionReq")
    
    # Modify the message here (for testing)
    # See https://construct.readthedocs.io/en/latest/basics.html#fields for how 
    # to parse, mutate, then rebuild a construct object
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg(msg)
    
    print("INFO: response -> %s" % res)
    
    # Close the node connection
    h.disconnect()
    
def test_sysstartrequest():
    """
    """
    # Create the harness instance
    h = Harness()
    
    # Connect to a node
    h.connect("127.0.0.1", 3000, 0)
    
    # Generate a "SysStartRequest" message
    msg_components = h.generate_msg(msg_type = "SysStartRequest", null = 0x00)
    
    # Modify the message here (for testing)
    # See https://construct.readthedocs.io/en/latest/basics.html#fields for how 
    # to parse, mutate, then rebuild a construct object
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg(msg)
    
    print("INFO: response -> %s" % res)
    
    # Close the node connection
    h.disconnect()

def test_getblocks():
    """
    """
    # Create the harness instance
    h = Harness()
    
    # Connect to a node
    h.connect("127.0.0.1", 3000, 0)
    
    # Generate a "GetBlocks" message
    msg_components = h.generate_msg(msg_type = "GetBlocks",  
                                    old_hash = [0x0f, 0xbb, 0xf2, 0x7a, 0xa3, 0x99, 0x84, 0x90, 0xca, 0x4e, 0x94, 0x56, 0xf2, 0xb9, 0x2f, 0x82, 0xbc, 0x9b, 0x10, 0xff, 0x37, 0xc9, 0x46, 0xd0, 0xc7, 0xb4, 0x5f, 0xc8],      
                                    new_hash = [0xe4, 0x30, 0xef, 0x7a, 0xe5, 0x70, 0x4e, 0x01, 0xbc, 0xa5, 0x8e, 0xd3, 0xea, 0x82, 0x77, 0x46, 0x51, 0x15, 0xd2, 0x40, 0xfc, 0x67, 0x57, 0x93, 0x07, 0x30, 0xe9, 0x04])
    
    # Modify the message here (for testing)
    # See https://construct.readthedocs.io/en/latest/basics.html#fields for how 
    # to parse, mutate, then rebuild a construct object
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg(msg)
    
    print("INFO: response -> %s" % res)
    
    # Close the node connection
    h.disconnect()
    

if __name__ == "__main__":
    test_getblocks()
