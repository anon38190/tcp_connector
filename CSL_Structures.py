from construct import *

# Constants

## Sizes
DEFAULT_HASH_SIZE = 32  # hash size for Blake2s_256 hashing
DEFAULT_PUBLIC_KEY_SIZE = 32
DEFAULT_SIGNATURE_SIZE = 64
DEFAULT_ADDRESS_HASH_SIZE = 28  # hash size for Blake2s_224 hashing

## Protocol constants
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

#######################
# COMMON HASKELL
#######################

def Pair(a, b):
    return a >> b  # or better Struct("fst"/a, "snd"/b)?

def Maybe(a):
    """
    >>> Maybe(VarInt).build(dict(tag=0, from_just=None))
    b'\x00'
    >>> Maybe(VarInt).build(dict(tag=1, from_just=3))
    b'\x01\x03'

    :param a: type of optional value
    :return: structure that encodes `Maybe a`
    """
    return Struct("tag" / Int8ub,
                  "from_just" / Switch(this.tag,
                  {
                    0: Terminated,  # TODO: avoid specify `fromJust=None` if tag=0
                    1: a
                  }))

def List(a):
    return PrefixedArray(VarInt, a)

#######################
# BASIC CARDANO
#######################

# TODO: some hardcore here...
COIN = Struct()

HASH = Array(DEFAULT_HASH_SIZE, Byte)
PUBLIC_KEY = Array(DEFAULT_PUBLIC_KEY_SIZE, Byte)
SIGNATURE = Array(DEFAULT_SIGNATURE_SIZE, Byte)

SLOT_ID = "epoch_index" / VarInt + \
          "slot_index" / VarInt

EMPTY_ATTRIBUTES = List(Byte)

# TODO: describe SCRIPT
SCRIPT = Struct()

# TODO: describe AddressAttributes
ADDRESS_ATTRIBUTES = Struct()

# TODO: describe Address
ADDRESS = Struct()

MERKLE_ROOT = HASH

#######################
# TRANSACTIONS MESSAGES
#######################

TX_IN = "hash" / HASH + \
        "index" / VarInt

TX_OUT = "address" / ADDRESS + \
         "out_value" / COIN

TX_OUT_AUX = Struct("output" / TX_OUT,
                    "distr" / List(Pair(HASH, COIN)))

TX_SIG_DATA = Struct("id" / HASH,
                     "index" / Int32ub,
                     "hash_out" / HASH,
                     "hash_distr" / HASH)

# >>> TX_IN_WITNESS.build(dict(tag=0, key=range(32), sig=range(64)))
# b'\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12
TX_IN_WITNESS = Struct("tag" / Int8ub,
                       Embedded(Switch(this.tag,
                       {
                         0: Struct("key" / PUBLIC_KEY,
                                   "sig" / SIGNATURE),
                         1: Struct("validator" / SCRIPT,
                                   "redeemer" / SCRIPT)
                       })))

TX_WITNESS = List(TX_IN_WITNESS)

TRANSACTION = Struct("inputs" / List(TX_IN),
                     "outputs" / List(TX_OUT),
                     "attributes" / EMPTY_ATTRIBUTES)

# TODO: describe distribution serialization logic
TX_DISTRIBUTION = Struct()

TX_AUX = Struct("tx" / TRANSACTION,
                "witness" / TX_WITNESS,
                "distribution" / TX_DISTRIBUTION)

##################
# Other Structures
##################

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