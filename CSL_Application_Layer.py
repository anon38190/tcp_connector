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
    def encode_msg(self, msg_data):
        """
        """
        encoded_msg_data = None
        
        # determine encoding handling based on the length of the message
        # type
        #if len(msg_type) < 0x80:
        #    encoded_msg_name = self.byte_encode_message(msg_type)
        #else:
        #    encoded_msg_name = self.var_encode_message(msg_type)
        
        if msg_data is not None:
            encoded_msg_data = self.var_encode_message_data(msg_data)    
        
        return encoded_msg_data
        
    #def byte_encode_message(self, msg_type):
        #"""
        #""" 
        #return ENC_SMALL_MSG.build(dict(size = len(msg_type), msg = msg_type.encode()))
        #return MSG_NAME_ENC.build(dict(msg_type = MSG_NAME_MAP[msg_type]))
           
    def var_encode_message_data(self, msg_data):
        """
        """
        enc_msg_data = ENC_DATA.build(dict(enc_data = msg_data))
        return b"%s%s" % (len(enc_msg_data).to_bytes(1, byteorder="big"), enc_msg_data)
        
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
        elif msg_type == "VersionResp":
            msg = self.set_versionresp_args(**kwargs)
        elif msg_type == "BlockHeaders":
            msg = self.set_blockheaders_args(**kwargs)
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
        #TODO: PeerState doesn't require the protocol version
        return PEERSTATE_VER.build(dict(pv_major = MAJ_VER, pv_minor = MIN_VER, pv_alt = ALT_VER))
            
    def set_sysstartresponse_args(self, **kwargs):
        """
        """
        # Get a timestamp
        dt = datetime.now().microsecond
        ts = dt.to_bytes((dt.bit_length() + 7) // 8, byteorder="big")
        
        #TODO: does this magic value ever change?
        return SYSSTARTRESPONSE.build(dict(vers_magic = VERSION_MAGIC,
                                           pv_major = MAJ_VER, 
                                           pv_minor = MIN_VER, 
                                           pv_alt = ALT_VER,
                                           size = len(ts),
                                           timestamp = ts))
                                           
    def set_versionresp_args(self, **kwargs):
        """
        """
        return VERSIONRESP.build(dict(vers_magic = VERSION_MAGIC,
                                      pv_major = MAJ_VER, 
                                      pv_minor = MIN_VER, 
                                      pv_alt = ALT_VER))
        
    def set_blockheaders_args(self, **kwargs):
        """
        """
        # Build the GodTossing proof
        if (kwargs["gt_tag"] == 0):
            gt = COMMITMENTS_PROOF.build(dict(hash_commitments_map = kwargs["hash_commitments_map"], 
                                              hash_vss_cert_map = kwargs["hash_vss_cert_map"]))
        elif (kwargs["gt_tag"] == 1):
            gt = OPENINGS_PROOF.build(dict(hash_openings_map = kwargs["hash_openings_map"], 
                                           hash_vss_cert_map = kwargs["hash_vss_cert_map"]))
        elif (kwargs["gt_tag"] == 2):
            gt = SHARES_PROOF.build(dict(hash_shares_map = kwargs["hash_shares_map"], 
                                         hash_vss_cert_map = kwargs["hash_vss_cert_map"]))
        elif (kwargs["gt_tag"] == 3):
            gt = CERTIFICATES_PROOF.build(dict(hash_vss_vert_map = kwargs["hash_vss_vert_map"]))
        else:
            print("ERROR: unsupported GT tag: %s" % kwargs["gt_tag"])
            return None
            
        ## Build the block version
        #bv = BLOCK_VERSION.build(dict(major = MAJ_VER, minor = MIN_VER, alt = ALT_VER))    
            
        ## Build the software version
        #sv = SOFTWARE_VERSION.build(dict(length = len(SOFTWARE_VER), name = SOFTWARE_VER))
        
        return MAIN_BLOCK_HEADER.build(dict(prot_magic = VERSION_MAGIC,
                                       header_hash = kwargs["header_hash"],
                                       mp_number = kwargs["mp_number"],
                                       mr_hash = kwargs["mp_root_hash"],
                                       mp_witnesses_hash = kwargs["mp_wit_hash"],
                                       tag = kwargs["gt_tag"],
                                       gt_data = gt,
                                       mp_proxy_sks_proof = kwargs["mp_proxy_sk_proof_hash"],
                                       mp_update_proof = kwargs["mp_update_proof_hash"],
                                       epoch_index = kwargs["epoch_index"],
                                       slot_index = kwargs["slot_index"],
                                       pub_key = kwargs["mcd_leader_key"],
                                       mcd_difficulty = kwargs["mcd_diff"],
                                       mcd_signature = kwargs["mcd_sig"],
                                       major = MAJ_VER,
                                       minor = MIN_VER,
                                       alt = ALT_VER,
                                       length = len(SOFTWARE_VER),
                                       name = SOFTWARE_VER.encode()))

