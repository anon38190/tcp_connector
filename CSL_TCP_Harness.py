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
            
        print(msg)    
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
    
def test_versionresp():
    """
    """
    # Create the harness instance
    h = Harness()
    
    # Connect to a node
    h.connect("127.0.0.1", 3000, 0)
    
    # Generate a "VersionResp" message
    msg_components = h.generate_msg(msg_type = "VersionResp",
                                    protocol_version = [0x00, 0x00, 0x00, 0x00, 0x00])
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    h.send_msg("VersionResp", msg)
    
    # Close the node connection
    h.disconnect()
    
def test_blockheaders():
    """
    """
    # Create the harness instance
    h = Harness()
    
    # Connect to a node
    h.connect("127.0.0.1", 3000, 0)
    
    #TODO: Not sure what values I could expect to have at the harness layer...
    # Generate a "BlockHeaders" message
    msg_components = h.generate_msg(msg_type = "BlockHeaders",
                                    header_hash = [0xe0, 0x5a, 0xa4, 0x25, 0xd9, 0x10, 0x4a, 0xb1, 
                                                   0xbc, 0xd0, 0x56, 0xad, 0xd2, 0xd9, 0xd8, 0x90, 
                                                   0xe9, 0xed, 0x6b, 0xac, 0x2c, 0x81, 0x4b, 0x50, 
                                                   0x74, 0xbb, 0xc4, 0xf2],
                                    mp_number = 0,
                                    mp_root_hash = [0x1f, 0xa1, 0x29, 0x1e, 0x65, 0x24, 0x8b, 0x37, 
                                                    0xb3, 0x43, 0x34, 0x75, 0xb2, 0xa0, 0xdd, 0x63, 
                                                    0xd5, 0x4a, 0x11, 0xec, 0xc4, 0xe3, 0xe0, 0x34, 
                                                    0xe7, 0xbc, 0x1e, 0xf4],
                                    mp_wit_hash = [0x61, 0xb9, 0x4e, 0xc9, 0x46, 0x22, 0xa3, 0x91, 
                                                   0xd2, 0xae, 0x42, 0xe6, 0x45, 0x6c, 0x90, 0x12, 
                                                   0xd5, 0x80, 0x07, 0x97, 0xb8, 0x86, 0x5a, 0xfc, 
                                                   0x48, 0x21, 0x97, 0xbb],
                                    gt_tag = 0,
                                    hash_commitments_map = [0x32, 0x0b, 0x16, 0x1c, 0xb2, 0x3e, 0x0c, 0x68, 
                                                            0x69, 0xe3, 0x16, 0xe5, 0x37, 0xca, 0x6d, 0x75, 
                                                            0x23, 0xea, 0xa7, 0x17, 0xf4, 0x72, 0x71, 0xee, 
                                                            0xdb, 0xc0, 0x49, 0x8e],
                                    hash_vss_cert_map = [0x8e, 0xbe, 0x2c, 0xf4, 0x21, 0x22, 0x8d, 0xf2, 
                                                         0x3d, 0x25, 0x88, 0xbf, 0x3e, 0xf0, 0xa6, 0x0a, 
                                                         0xe8, 0xf3, 0x3f, 0x99, 0xab, 0x7c, 0x6a, 0xb0, 
                                                         0xa4, 0x79, 0xf5, 0xd3],
                                    mp_proxy_sk_proof_hash = [0x61, 0xb9, 0x4e, 0xc9, 0x46, 0x22, 0xa3, 0x91, 
                                                              0xd2, 0xae, 0x42, 0xe6, 0x45, 0x6c, 0x90, 0x12, 
                                                              0xd5, 0x80, 0x07, 0x97, 0xb8, 0x86, 0x5a, 0xfc, 
                                                              0x48, 0x21, 0x97, 0xbb],
                                    mp_update_proof_hash = [0x2e, 0x50, 0xc1, 0xed, 0x96, 0x84, 0x93, 0xb6, 
                                                            0x15, 0x10, 0x2e, 0xa2, 0x0b, 0xff, 0x32, 0xfb, 
                                                            0xa3, 0xea, 0xdf, 0x00, 0x02, 0x6a, 0xef, 0xc2, 
                                                            0xfb, 0xab, 0x16, 0xc4],
                                    epoch_index = 0,
                                    slot_index = 2,
                                    mcd_leader_key = [0xef, 0x1e, 0x69, 0xde, 0xc2, 0xbf, 0xfb, 0x79, 
                                                      0xe7, 0x66, 0x6f, 0x34, 0x36, 0x14, 0xdd, 0xd7, 
                                                      0xad, 0x2b, 0xc6, 0x6c, 0xb2, 0x0c, 0x4c, 0x2c, 
                                                      0xde, 0x43, 0x7e, 0x2e, 0x84, 0x72, 0xa9, 0xf1],
                                    mcd_diff = 2,
                                    mcd_sig = [0x9a, 0x89, 0x90, 0xe3, 0x22, 0x9b, 0xc8, 0xfe, 
                                               0x1e, 0x7f, 0x85, 0x94, 0xb2, 0x23, 0x52, 0xe7, 
                                               0xc0, 0x48, 0x78, 0x2c, 0x73, 0x53, 0x70, 0x7b, 
                                               0x3b, 0x4d, 0x8e, 0xb8, 0xcf, 0x33, 0x1d, 0xc4, 
                                               0x28, 0x67, 0x11, 0x9c, 0x2c, 0x1d, 0xe5, 0x1e, 
                                               0x46, 0x5a, 0xa5, 0xa2, 0x41, 0x47, 0xf5, 0x24, 
                                               0x90, 0xed, 0x16, 0xd8, 0x6e, 0xc6, 0x0f, 0x90, 
                                               0x7e, 0xce, 0x52, 0x95, 0xcf, 0xcb, 0x81, 0x0a],
                                    block_header_attr = None,)
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg("BlockHeaders", msg)
    print("INFO: response -> %s" % res)
    
    # Close the node connection
    h.disconnect()
    
    

if __name__ == "__main__":
    test_blockheaders()
