from construct import *

# Constants
DEFAULT_HASH_SIZE = 28
PUB_KEY_SIZE = 32
DEFAULT_SIGNATURE_SIZE = 64
PROTOCOL_VER_SIZE = 5
#VERSION_MAGIC = 16842752
VERSION_MAGIC = 0

BID_TRANS = ["SysStartReq", "GetHeaders", "GetBlocks", "VersionReq", "PeerState"]
UND_TRANS = ["SysStartResponse", "VersionResp"]

# Structures
DATA_MSG = Struct("lwcid" / Int32ub,
                  "size" / Int32ub,
                  "msg" / Array(this.size, Byte))
                  
BID_CONTROL_HEADER = Struct("cc" / Byte,
                            "nonce" / Int64ub)
                            
UND_CONTROL_HEADER = Struct("cc" / Int8ub)

ENC_SMALL_MSG = Struct("size" / Int8ub,
                       "msg" / Array(this.size, Byte))

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

PROTOCOL_VERSION = Struct("pvMajor" / Int16ub, "pvMinor" / Int16ub, "pvAlt" / Int8ub)

#TODO: investigate way to handle optional parameters...
PEERSTATE_VER = Struct("protocolversion" / Array(PROTOCOL_VER_SIZE, Byte))

PEERSTATE = Struct()

#TODO: Don't see any of this in the documentation, might be wrong...
TIMESTAMP = Struct("size" / Int8ub,
                   "timestamp" / Array(this.size, Byte))

SYSSTARTRESPONSE = Struct("vers_magic" / Int32ub,
                          "protocol_vers" / Array(PROTOCOL_VER_SIZE, Byte),
                          "timestamp" / Embedded(TIMESTAMP))
                          
VERSIONRESP = Struct("vers_magic" / Int32ub,
                     "protocol_vers" / Array(PROTOCOL_VER_SIZE, Byte))



