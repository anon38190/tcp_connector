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
            
        #print(msg)    
        return msg
            
    @CSL_Layers.send_msg_dec
    def send_msg(self, msg):
        """
        """
        # All the transport details are handled at a lower layer
        print("INFO: Sending the message...")
        
    def print_responses(self, responses):
        """
        """
        for key, value in responses.items():
            print("%s -> %s" % (key, value))
            
      
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
    
    h.print_responses(res)
    
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
                                    old_hashes = [[0x64, 0x26, 0xd4, 0x06, 0x7d, 0x33, 0xb4, 0xfb, 0x06, 0x4c, 0x5c, 0x62, 0x24, 0x10, 0xc2, 0x45, 0xb2, 0xe0, 0x0e, 0xa1, 0x92, 0x12, 0x86, 0x6e, 0xe1, 0x3d, 0x0e, 0x0e, 0x38, 0xb8, 0x94, 0x15]],
                                    new_hash = None)
                                    #new_hash = [0xcd, 0x08, 0xc5, 0xfd, 0x5f, 0x0a, 0x37, 0x75, 0xca, 0x3b, 0x16, 0x1c, 0xd3, 0x2a, 0xc7, 0x9b, 0x24, 0x45, 0x3c, 0x08, 0x2e, 0x10, 0x63, 0x9e, 0x70, 0xb7, 0x91, 0x73])
    
    # Modify the message here (for testing)
    # See https://construct.readthedocs.io/en/latest/basics.html#fields for how 
    # to parse, mutate, then rebuild a construct object
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg("GetHeaders", msg)
    
    h.print_responses(res)
    
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
    
    h.print_responses(res)
    
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
    
    h.print_responses(res)
    
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
                                    old_hash = [0xd7, 0x54, 0x7f, 0xe3, 0xe1, 0xaa, 0x3b, 0x21, 0x69, 0xa9, 0x2c, 0x4f, 0x8d, 0xb6, 0xa0, 0xb5, 0xb2, 0x43, 0xc4, 0x7d, 0x0f, 0xe3, 0xbc, 0xf0, 0x93, 0x7f, 0xa7, 0x35, 0x2b, 0x5c, 0x80, 0xee],
                                    new_hash = [0x64, 0x26, 0xd4, 0x06, 0x7d, 0x33, 0xb4, 0xfb, 0x06, 0x4c, 0x5c, 0x62, 0x24, 0x10, 0xc2, 0x45, 0xb2, 0xe0, 0x0e, 0xa1, 0x92, 0x12, 0x86, 0x6e, 0xe1, 0x3d, 0x0e, 0x0e, 0x38, 0xb8, 0x94, 0x15])
    
    # Modify the message here (for testing)
    # See https://construct.readthedocs.io/en/latest/basics.html#fields for how 
    # to parse, mutate, then rebuild a construct object
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg("GetBlocks", msg)
    
    h.print_responses(res)
    
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
    msg_components = h.generate_msg(msg_type = "SysStartResponse")
    
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
    msg_components = h.generate_msg(msg_type = "VersionResp")
    
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
                                    header_hash = [0xd7, 0x54, 0x7f, 0xe3, 0xe1, 0xaa, 0x3b, 0x21, 0x69, 0xa9, 0x2c, 0x4f, 0x8d, 0xb6, 0xa0, 0xb5, 0xb2, 0x43, 0xc4, 0x7d, 0x0f, 0xe3, 0xbc, 0xf0, 0x93, 0x7f, 0xa7, 0x35, 0x2b, 0x5c, 0x80, 0xee],
                                    mp_number = 0,
                                    mp_root_hash = [0x69, 0x21, 0x7a, 0x30, 0x79, 0x90, 0x80, 0x94, 0xe1, 0x11, 0x21, 0xd0, 0x42, 0x35, 0x4a, 0x7c, 0x1f, 0x55, 0xb6, 0x48, 0x2c, 0xa1, 0xa5, 0x1e, 0x1b, 0x25, 0x0d, 0xfd, 0x1e, 0xd0, 0xee, 0xf9 ],
                                    mp_wit_hash = [0xe3, 0x4d, 0x74, 0xdb, 0xaf, 0x4f, 0xf4, 0xc6, 0xab, 0xd8, 0x71, 0xcc, 0x22, 0x04, 0x51, 0xd2, 0xea, 0x26, 0x48, 0x84, 0x6c, 0x77, 0x57, 0xfb, 0xaa, 0xc8, 0x2f, 0xe5, 0x1a, 0xd6, 0x4b, 0xea],
                                    gt_tag = 0,
                                    hash_commitments_map = [0xab, 0xd5, 0x8f, 0xc9, 0xe1, 0x3d, 0x05, 0xd2, 0x6f, 0x59, 0x76, 0xe3, 0xb4, 0x8b, 0x69, 0x12, 0xc3, 0xa6, 0xd0, 0x3e, 0x60, 0x65, 0x2f, 0xdf, 0xf5, 0xd1, 0x1a, 0xda, 0xa5, 0x86, 0x7f, 0x58],
                                    hash_vss_cert_map = [0x6d, 0x6c, 0x72, 0xe0, 0xb8, 0xf1, 0x41, 0xf3, 0xfa, 0xeb, 0xf9, 0xf1, 0x00, 0x04, 0x20, 0xd1, 0xf8, 0x7b, 0x09, 0xb2, 0xf9, 0x9f, 0x3b, 0xbb, 0xc7, 0x28, 0x76, 0xcd, 0xb6, 0x57, 0xe7, 0xad],
                                    mp_proxy_sk_proof_hash = [0xe3, 0x4d, 0x74, 0xdb, 0xaf, 0x4f, 0xf4, 0xc6, 0xab, 0xd8, 0x71, 0xcc, 0x22, 0x04, 0x51, 0xd2, 0xea, 0x26, 0x48, 0x84, 0x6c, 0x77, 0x57, 0xfb, 0xaa, 0xc8, 0x2f, 0xe5, 0x1a, 0xd6, 0x4b, 0xea],
                                    mp_update_proof_hash = [0x77, 0x4f, 0x90, 0x18, 0xb4, 0xb2, 0xcd, 0xc0, 0x8f, 0x89, 0x28, 0xe8, 0x9b, 0x0d, 0x96, 0x3a, 0xc3, 0x88, 0xe5, 0x37, 0xb0, 0x03, 0x49, 0x2c, 0x69, 0xaa, 0xfe, 0xea, 0xb9, 0x76, 0xe5, 0x53],
                                    epoch_index = 0,
                                    slot_index = 1,
                                    mcd_leader_key = [0xfb, 0xe9, 0xb5, 0x13, 0xcd, 0x44, 0x71, 0x33, 0x01, 0x5b, 0xc1, 0x63, 0xcc, 0x37, 0x17, 0x3d, 0x08, 0x37, 0xa8, 0x73, 0x1b, 0xc5, 0x32, 0x86, 0xb9, 0x80, 0xa4, 0x3d, 0xa4, 0x76, 0x9f, 0x4b],
                                    mcd_diff = 2,
                                    mcd_sig = [0x9d, 0x03, 0x01, 0xf2, 0x55, 0x82, 0x96, 0xeb, 0x83, 0xfd, 0x5f, 0x28, 0x63, 0xa0, 0x32, 0xef, 
                                               0xe0, 0xa5, 0xd6, 0x0c, 0x23, 0xf5, 0x33, 0xd5, 0xf3, 0x96, 0x74, 0x2c, 0xa4, 0x8c, 0x7f, 0xc4, 
                                               0x6d, 0x05, 0x0c, 0x61, 0xa0, 0xfb, 0x7b, 0xcb, 0xb1, 0x65, 0xc1, 0x36, 0x31, 0xe0, 0xfe, 0xce, 
                                               0x22, 0xdb, 0x3f, 0xf9, 0x7b, 0x12, 0x3e, 0xac, 0x7a, 0x1f, 0x2e, 0x63, 0xec, 0xf7, 0xe4, 0x0c],
                                    block_header_attr = None,)
    
    # Assemble the message (with any of our modifications)
    msg = h.assemble_msg(msg_components)
    
    # Send the message
    res = h.send_msg("BlockHeaders", msg)
    h.print_responses(res)
    
    # Close the node connection
    h.disconnect()
    
def full_suite_test():
    """
    """
    #test_peerstate()       #TODO: waiting for CSL to update message name mapping
    #test_blockheaders()
    #test_getheaders()      
    #test_versionreq()      #TODO: waiting for CSL to update message name mapping
    #test_sysstartrequest() #TODO: attempting to use endpoint he doesn't report to use
    #test_getblocks()
    #test_sysstartresponse()
    #test_versionresp()     #TODO: waiting for CSL to update message name mapping

if __name__ == "__main__":
    full_suite_test()
    
    
    
