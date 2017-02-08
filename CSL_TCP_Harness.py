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
    res = h.send_msg("PeerState", msg)
    
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
                                    old_hashes = [[0x9b, 0xc2, 0x81, 0x9d, 0xfe, 0x1d, 0x55, 0x3e, 0xbe, 0x6f, 0x25, 0xaf, 0xcd, 0x1f, 0x01, 0xac, 0xfd, 0xe4, 0xbc, 0xb7, 0xcf, 0x3e, 0x6b, 0xeb, 0x9d, 0x19, 0x06, 0x28]],
                                    new_hash = None)
                                    #new_hash = [0xcd, 0x08, 0xc5, 0xfd, 0x5f, 0x0a, 0x37, 0x75, 0xca, 0x3b, 0x16, 0x1c, 0xd3, 0x2a, 0xc7, 0x9b, 0x24, 0x45, 0x3c, 0x08, 0x2e, 0x10, 0x63, 0x9e, 0x70, 0xb7, 0x91, 0x73])
    
    # Modify the message here (for testing)
    # See https://construct.readthedocs.io/en/latest/basics.html#fields for how 
    # to parse, mutate, then rebuild a construct object
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg("GetHeaders", msg)
    
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
    res = h.send_msg("VersionReq", msg)
    
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
    res = h.send_msg("SysStartRequest", msg)
    
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
                                    old_hash = [0xfb, 0x37, 0x0d, 0xb0, 0x36, 0x59, 0x20, 0x96, 0x21, 0x56, 0x6d, 0x68, 0xcd, 0x92, 0x3b, 0xeb, 0x7d, 0x6d, 0x79, 0x68, 0x35, 0x6e, 0x78, 0x5f, 0x86, 0x9b, 0x3f, 0x8c],
                                    new_hash = [0xc0, 0x10, 0x41, 0x79, 0xe6, 0xbb, 0x4c, 0xc9, 0x27, 0xa1, 0xbb, 0xe7, 0xe5, 0x82, 0x7b, 0x65, 0xf1, 0xba, 0x3f, 0x63, 0x89, 0xf0, 0xfa, 0xa8, 0xc7, 0x56, 0x52, 0x11])
    
    # Modify the message here (for testing)
    # See https://construct.readthedocs.io/en/latest/basics.html#fields for how 
    # to parse, mutate, then rebuild a construct object
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg("GetBlocks", msg)
    
    print("INFO: response -> %s" % res)
    
    # Close the node connection
    h.disconnect()
    
def test_sysstartresponse():
    """
    """
    # Create the harness instance
    h = Harness()
    
    # Connect to a node
    h.connect("127.0.0.1", 3000, 0)
    
    # Generate a "SysStartResponse" message
    msg_components = h.generate_msg(msg_type = "SysStartResponse",
                                    protocol_version = [0x00, 0x00, 0x00, 0x00, 0x00])
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    h.send_msg("SysStartResponse", msg)
    
    # Close the node connection
    h.disconnect()

if __name__ == "__main__":
    test_sysstartrequest()
    #test_sysstartresponse()
