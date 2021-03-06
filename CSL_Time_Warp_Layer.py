#TODO: As written, this only works for sending (S) a bidirectional message.
#      Modify the code to acknowledge (A) bidirectional messages as well.

from CSL_Network_Transport_Layer import NetworkTransportLayer
from CSL_Status_Codes import *
from CSL_Structures import *

import random
from binascii import hexlify

class TimeWarpLayer(NetworkTransportLayer):
    
    def __init__(self):
        """
        """
        super().__init__()
        self.peer_data_received = False
        self.cc_msg_type_mapping = {"SysStartRequest":0x53,
                                    "GetBlocks":0x53,
                                    "VersionReq":0x53,
                                    "GetHeaders":0x53,
                                    "PeerState":0x53,
                                    "SysStartResponse":0x55,
                                    "VersionResp":0x55,
                                    "BlockHeaders":0x53}
        
    def get_control_code(self, msg_type):
        """
        """
        try:
            cc = self.cc_msg_type_mapping[msg_type]
        except KeyError:
            print("ERROR: Unsupported message type: %s" % msg_type)
            cc = None
            
        # Convert to a byte string    
        return cc
        
    def generate_nonce(self):
        """
        """
        return random.randrange(0, 0xFFFFFFFFFFFFFFFF)
    
    def build_control_header(self, msg_type):
        """
        """
        c_code = self.get_control_code(msg_type)
        
        if (c_code == 0x53 or c_code == 0x41):
            nonce_value = self.generate_nonce()
            return BID_CONTROL_HEADER.build(dict(cc = c_code, nonce = nonce_value))        
        elif (c_code == 0x55):
            return UND_CONTROL_HEADER.build(dict(cc = c_code))
        else:
            print("Unsupported control code: %s" % c_code)
            return None
            
    def build_peer_data(self):
        """
        """
        #TODO: as per recommendation, we're hardcoding these until they are documented
        nonce = [0x10, 0xb5, 0x4f, 0x43, 0x52, 0xc7, 0x24, 0x06, 0xb6, 0x5a, 0x9e, 0x0c, 0xeb, 0x4d]
        handler_lists = [0x13, 0x02, 0x0a, 0x02, 0x00, 0x00, 0x02, 0x0a, 0x03, 0x00, 0x00, 0x02, 0x0a, 0x00, 0x00, 0x00, 
                         0x02, 0x0a, 0x01, 0x00, 0x00, 0x02, 0xea, 0x07, 0x00, 0x00, 0x02, 0xe9, 0x07, 0x01, 0x03, 0x02, 
                         0xea, 0x07, 0x01, 0x04, 0x01, 0x02, 0x01, 0x05, 0x01, 0x05, 0x01, 0x02, 0x01, 0x04, 0x01, 0x06, 
                         0x01, 0x02, 0x01, 0x07, 0x02, 0x09, 0x03, 0x00, 0x00, 0x02, 0x08, 0x00, 0x00, 0x00, 0x02, 0x09, 
                         0x02, 0x00, 0x00, 0x02, 0x08, 0x01, 0x00, 0x00, 0x01, 0x02, 0x00, 0x00, 0x02, 0x09, 0x01, 0x00, 
                         0x00, 0x02, 0x08, 0x02, 0x00, 0x00, 0x01, 0x03, 0x00, 0x00, 0x02, 0x09, 0x00, 0x00, 0x00, 0x02, 
                         0x08, 0x03, 0x00, 0x00, 0x12, 0x02, 0x0a, 0x02, 0x00, 0x00, 0x02, 0x0a, 0x03, 0x00, 0x00, 0x02, 
                         0x0a, 0x00, 0x00, 0x00, 0x02, 0x0a, 0x01, 0x00, 0x00, 0x02, 0xea, 0x07, 0x00, 0x00, 0x01, 0x04, 
                         0x01, 0x02, 0x01, 0x05, 0x01, 0x05, 0x01, 0x02, 0x01, 0x04, 0x01, 0x06, 0x01, 0x02, 0x01, 0x07, 
                         0x02, 0x09, 0x03, 0x00, 0x00, 0x02, 0x08, 0x00, 0x00, 0x00, 0x02, 0x09, 0x02, 0x00, 0x00, 0x02, 
                         0x08, 0x01, 0x00, 0x00, 0x01, 0x02, 0x00, 0x00, 0x02, 0x09, 0x01, 0x00, 0x00, 0x02, 0x08, 0x02, 
                         0x00, 0x00, 0x01, 0x03, 0x00, 0x00, 0x02, 0x09, 0x00, 0x00, 0x00, 0x02, 0x08, 0x03, 0x00, 0x00]
        
        return PEER_DATA.build(dict(nonce = nonce, 
                                    protocol_magic = PROTOCOL_MAGIC, 
                                    major = MAJ_VER, 
                                    minor = MIN_VER, 
                                    alt = ALT_VER,
                                    handler_list = handler_lists))

