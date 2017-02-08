from CSL_Time_Warp_Layer import TimeWarpLayer
from CSL_Status_Codes import *

from CSL_Structures import *
from datetime import datetime

class ApplicationLayer(TimeWarpLayer):
    """
    """
    
    def __init__(self,):
        """
        """
        super().__init__()

    # TODO: don't know if this belongs at the application layer
    def encode_msg(self, msg_type):
        """
        """
        encoded_msg_name = None
        
        # determine encoding handling based on the length of the message
        # type
        if len(msg_type) < 0x80:
            encoded_msg_name = self.byte_encode_message(msg_type)
        else:
            encoded_msg_name = self.var_encode_message(msg_type)
            
        return encoded_msg_name
        
    def byte_encode_message(self, msg_type):
        """
        """ 
        return ENC_SMALL_MSG.build(dict(size = len(msg_type), msg = msg_type.encode()))
           
    def var_encode_message(self, msg_type):
        """
        """
        #TODO: implement
    
    def build_arg_dict(self, **kwargs):
        """
        """
        #TODO: take the kwargs (msg type + args), and return a populate arg dict
        msg_type = kwargs["msg_type"]
        msg = None
        
        if msg_type == "GetBlocks":
            msg = self.set_getblocks_args(**kwargs)
        elif msg_type == "SysStartRequest":
            msg = self.set_sysstartrequest_args(**kwargs)
        elif msg_type == "VersionReq":
            msg = self.set_versionreq_args(**kwargs)
        elif msg_type == "GetHeaders":
            msg = self.set_getheaders_args(**kwargs)
        elif msg_type == "PeerState":
            msg = self.set_peerstate_args(**kwargs)
        elif msg_type == "SysStartResponse":
            msg = self.set_sysstartresponse_args(**kwargs)
        else:
            print("ERROR: unsupported message type: %s" % msg_type)
            
        return msg
             
    def set_getblocks_args(self, **kwargs):
        """
        """     
        #TODO: handle cases in which the kwarg is missing
        return GETBLOCKS.build(dict(old_hash = kwargs["old_hash"], new_hash = kwargs["new_hash"]))
        
    def set_sysstartrequest_args(self, **kwargs):
        """
        """
        #TODO: handle cases in which the kwarg is missing
        return SYSSTARTREQUEST.build(dict(null = kwargs["null"]))
        
    def set_versionreq_args(self, **kwargs):
        """
        """
        return VERSIONREQ.build(dict())
        
    def set_getheaders_args(self, **kwargs):
        """
        """
        # Assemble the list of old hashes
        old_hash_list = []
        hash_count  = 0;
        for h in kwargs["old_hashes"]:
            old_hash_list = old_hash_list + h
            hash_count += 1
        
        if not kwargs["new_hash"]:
            return GETHEADERS_SINGLE.build(dict(count = hash_count, old_hashes = old_hash_list))
        else:
            return GETHEADERS_RANGE.build(dict(count = hash_count, old_hashes = old_hash_list, new_hash = kwargs["new_hash"]))
            
    def set_peerstate_args(self, **kwargs):
        """
        """
        if not kwargs["protocolversion"]:
            return PEERSTATE.build(dict())
        else:
            return PEERSTATE_VER.build(dict(protocolversion = kwargs["protocolversion"]))
            
    def set_sysstartresponse_args(self, **kwargs):
        """
        """
        # Get a timestamp
        dt = datetime.now().microsecond
        ts = dt.to_bytes((dt.bit_length() + 7) // 8, byteorder="big")
        
        #TODO: does this magic value ever change?
        return SYSSTARTRESPONSE.build(dict(vers_magic = VERSION_MAGIC,
                                           protocol_vers = kwargs["protocol_version"],
                                           size = len(ts),
                                           timestamp = ts))
        
        
