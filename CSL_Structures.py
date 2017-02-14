from construct import *

# Constants
DEFAULT_HASH_SIZE = 32
PUB_KEY_SIZE = 32
DEFAULT_SIGNATURE_SIZE = 64
VERSION_MAGIC = 16842752
PROTOCOL_MAGIC = 0
MAJ_VER = 0
MIN_VER = 0
ALT_VER = 0
SOFTWARE_VER = "cardano"
DATA_MAX = 0x100
DEFAULT_NONCE_SIZE = 14

BID_TRANS = ["SysStartRequest", "GetHeaders", "GetBlocks", "VersionReq", "PeerState", "BlockHeaders"]
UND_TRANS = ["SysStartResponse", "VersionResp"]

MSG_NAME_MAP = {"SysStartRequest":1001,
                "GetHeaders":4,
                "GetBlocks":6,
                "VersionReq":None,
                "PeerState":None,
                "BlockHeaders":5,
                "SysStartResponse":1002,
                "VersionResp":None}
                
ENC_DATA = Struct("enc_data" / VarInt)

# Structures
DATA_MSG = Struct("lwcid" / Int32ub,
                  "size" / Int32ub,
                  "msg" / Array(this.size, Byte))
                  
BID_CONTROL_HEADER = Struct("cc" / Byte,
                            "nonce" / Int64ub)
                            
UND_CONTROL_HEADER = Struct("cc" / Int8ub)

GETBLOCKS = Struct("old_hash" / Array(DEFAULT_HASH_SIZE, Byte),
                   "new_hash" / Array(DEFAULT_HASH_SIZE, Byte))
                   
SYSSTARTREQUEST = Struct("null" / Byte)

VERSIONREQ = Struct()

GETHEADERS_RANGE = Struct("count" / Int8ub,
                          "old_hashes" / Array(this.count * DEFAULT_HASH_SIZE, Byte),
                          "new_hash" / Array(DEFAULT_HASH_SIZE, Byte))
                          
GETHEADERS_SINGLE = Struct("count" / Int8ub,
                           "old_hashes" / Array(this.count * DEFAULT_HASH_SIZE, Byte),
                           "new_hash" / Default(Byte, 0x00))

PROTOCOL_VERSION = Struct("pv_major" / Int16ub, "pv_minor" / Int16ub, "pv_alt" / Int8ub)

#TODO: investigate way to handle optional parameters...
PEERSTATE_VER = Struct(Embedded(PROTOCOL_VERSION))

PEERSTATE = Struct()

#TODO: Don't see any of this in the documentation, might be wrong...
TIMESTAMP = Struct("size" / Int8ub,
                   "timestamp" / Array(this.size, Byte))

SYSSTARTRESPONSE = Struct("vers_magic" / Int32ub,
                          Embedded(PROTOCOL_VERSION),
                          "timestamp" / Embedded(TIMESTAMP))
                          
VERSIONRESP = Struct("vers_magic" / Int32ub,
                     Embedded(PROTOCOL_VERSION))

ATTRIBUTES = Struct("size" / Int32ub,
                    "data" / Array(this.size, Byte))

MERKLE_ROOT = Struct("mr_hash" / Array(DEFAULT_HASH_SIZE, Byte))

SLOT_ID = Struct("epoch_index" / VarInt,
                 "slot_index" / VarInt)

BLOCK_VERSION = Struct("major" / Int16ub,
                       "minor" / Int16ub,
                       "alt" / Int8ub)

# Not a null terminated string
SOFTWARE_VERSION = Struct("length" / VarInt, 
                          "name" / String(this.length, encoding="utf-8"))

COMMITMENTS_PROOF = Struct("hash_commitments_map" / Array(DEFAULT_HASH_SIZE, Byte),
                           "hash_vss_cert_map" / Array(DEFAULT_HASH_SIZE, Byte))
                           
OPENINGS_PROOF = Struct("hash_openings_map" / Array(DEFAULT_HASH_SIZE, Byte),
                        "hash_vss_cert_map" / Array(DEFAULT_HASH_SIZE, Byte))
                        
SHARES_PROOF = Struct("hash_shares_map" / Array(DEFAULT_HASH_SIZE, Byte),
                      "hash_vss_cert_map" / Array(DEFAULT_HASH_SIZE, Byte))
                      
CERTIFICATES_PROOF = Struct("hash_vss_vert_map" / Array(DEFAULT_HASH_SIZE, Byte))

#TODO: not sure why no attributes yields an 8-byte array of nulls...
BLOCK_HEADER_ATTRIBUTES = Struct("attr" / Default(Array(8, Byte), [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

#TODO: Might be a better way to handle fields based on another field (e.g. "tag")
GT_PROOF = Struct("tag" / Int8ub,
                  "gt_data" / Switch(this.tag,
                  {
                    0:Array(COMMITMENTS_PROOF.sizeof(), Byte),
                    1:Array(OPENINGS_PROOF.sizeof(), Byte),
                    2:Array(SHARES_PROOF.sizeof(), Byte),
                    3:Array(CERTIFICATES_PROOF.sizeof(), Byte)
                  }))

PUBLIC_KEY = Struct("pub_key" / Array(PUB_KEY_SIZE, Byte))

MAIN_PROOF = Struct("mp_number" / VarInt,
                    Embedded(MERKLE_ROOT),
                    "mp_witnesses_hash" / Array(DEFAULT_HASH_SIZE, Byte),
                    Embedded(GT_PROOF),
                    "mp_proxy_sks_proof" / Array(DEFAULT_HASH_SIZE, Byte),
                    "mp_update_proof" / Array(DEFAULT_HASH_SIZE, Byte))

MAIN_CONSENSUS_DATA = Struct(Embedded(SLOT_ID),
                             Embedded(PUBLIC_KEY),
                             "mcd_difficulty" / VarInt,
                             "mystery2" / Default(Byte, 0),
                             "mcd_signature" / Array(DEFAULT_SIGNATURE_SIZE, Byte))

MAIN_EXTRA_HEADER_DATA = Struct(Embedded(BLOCK_VERSION),
                                Embedded(SOFTWARE_VERSION),
                                Embedded(BLOCK_HEADER_ATTRIBUTES))

MAIN_BLOCK_HEADER = Struct("prot_magic" / Int32ub,
                           "mystery1" / Default(Int16ub, 0), #TODO: what is this field?
                           "header_hash" / Array(DEFAULT_HASH_SIZE, Byte),
                           Embedded(MAIN_PROOF),
                           Embedded(MAIN_CONSENSUS_DATA),
                           Embedded(MAIN_EXTRA_HEADER_DATA))

#TODO: this is temporary until this data structure is documented
HANDLER_LIST_SIZE = 192
PEER_DATA = Struct("nonce" / Array(DEFAULT_NONCE_SIZE, Byte),
                   "protocol_magic" / Int32ub,
                   Embedded(BLOCK_VERSION),
                   "handler_list" / Array(HANDLER_LIST_SIZE, Byte)) # Just throw everything in here...

