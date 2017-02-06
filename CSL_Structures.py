from construct import *

# Constants
HEADER_HASH_SIZE = 28
PROTOCOL_VER_SIZE = 5

# Structures
DATA_MSG = Struct("lwcid" / Int32ub,
                  "size" / Int32ub,
                  "msg" / Array(this.size, Byte))
                  
BID_CONTROL_HEADER = Struct("cc" / Byte,
                            "nonce" / Int64ub)
                            
UND_CONTROL_HEADER = Struct("cc" / Int8ub)

ENC_SMALL_MSG = Struct("size" / Int8ub,
                       "msg" / Array(this.size, Byte))

GETBLOCKS = Struct("old_hash" / Array(HEADER_HASH_SIZE, Byte),
                   "new_hash" / Array(HEADER_HASH_SIZE, Byte))
                   
SYSSTARTREQUEST = Struct("null" / Byte)

VERSIONREQ = Struct()

#TODO: investigate way to handle optional parameters...
GETHEADERS_RANGE = Struct("old_hash" / Array(HEADER_HASH_SIZE, Byte),
                          "new_hash" / Array(HEADER_HASH_SIZE, Byte))
                          
GETHEADERS_SINGLE = Struct("old_hash" / Array(HEADER_HASH_SIZE, Byte))

PROTOCOL_VERSION = Struct("pvMajor" / Int16ub, "pvMinor" / Int16ub, "pvAlt" / Int8ub)

#TODO: investigate way to handle optional parameters...
PEERSTATE_VER = Struct("protocolversion" / Array(PROTOCOL_VER_SIZE, Byte))

PEERSTATE = Struct()
