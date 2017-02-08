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
        self.cc_msg_type_mapping = {"SysStartRequest":0x53,
                                    "GetBlocks":0x53,
                                    "VersionReq":0x53,
                                    "GetHeaders":0x53,
                                    "PeerState":0x53,
                                    "SysStartResponse":0x55}
        
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

