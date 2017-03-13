import binascii

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
                    0: Terminated,
                    1: a
                  }))

# Maybe constructors
Nothing = dict(tag=0, from_just=None)  # TODO: avoid specify `fromJust=None` if tag=0
def Just(x):
    return dict(tag=1, from_just=x)

def List(a):
    return PrefixedArray(VarInt, a)

#######################
# BASIC CARDANO
#######################

HASH = Array(DEFAULT_HASH_SIZE, Byte)
PUBLIC_KEY = Array(DEFAULT_PUBLIC_KEY_SIZE, Byte)
SIGNATURE = Array(DEFAULT_SIGNATURE_SIZE, Byte)
ADDRESS_HASH = Array(DEFAULT_ADDRESS_HASH_SIZE, Byte)

# TODO: support 32333 ADA = \x00\xc5\x15\xae
# TODO: support full coin serialization
# now only 1000 ADA = \x00\x64 is supported
COIN = OneOf(
    ExprAdapter(Int16ub,
        encoder=lambda obj, ctx: 100,
        decoder=lambda obj, ctx: 1000 if obj == 100 else None),
    [1000])

SLOT_ID = "epoch_index" / VarInt + \
          "slot_index" / VarInt

EMPTY_ATTRIBUTES = List(Byte)

SCRIPT = "version"/VarInt + "script"/List(Byte)

# TODO: now only construction (w/o parsing and w/o non-empty data)
def pk_address_attrs(remain, data=Nothing):
    if data != Nothing:
        raise ValueError("only empty attributes supported in ADDRESS_ATTRIBUTES", data)
    remain_len = VarInt.build(len(remain))
    return b'%s%s' % (remain_len, remain)

# >>> ADDRESS_ATTRIBUTES.build(b"hello")
# b'\x05hello'
ADDRESS_ATTRIBUTES = ExprAdapter(GreedyBytes,
    encoder=lambda obj, ctx: pk_address_attrs(obj),
    decoder=lambda obj, ctx: None)  # TODO: parsing is not supported

# >>> ADDRESS.build(dict(tag=0,
#                        key_hash=bytearray.fromhex("380dea393a631ad563154a13bc5ee49fa4b62a60218358b5dcb875e0"),
#                        pk_attrs=b"a"))
# b'\x00\x1e8\r\xea9:c\x1a\xd5c\x15J\x13\xbc^\xe4\x9f\xa4\xb6*`!\x83X\xb5\xdc\xb8u\xe0\x01a\xcfR\xc5\xec'
ADDRESS = Struct("tag" / Int8ub,
                 Embedded(Switch(this.tag,
                 {
                   0: Struct("size" / Const(b"\x1e"),  # TODO: should be length of key_hash + pk_attrs
                             "key_hash" / ADDRESS_HASH,
                             "pk_attrs" / ADDRESS_ATTRIBUTES),
                   1: Struct("size" / Const("\x1C"),
                             "script_hash" / ADDRESS_HASH)
                   # TODO: UnknownAddress
                 })),
                 # TODO: put into each constructor
                 "checksum" / Checksum(Bytes(4),
                                       lambda data: binascii.crc32(data),
                                       lambda ctx: (Int8ub >> Const(b"\x1e") >> ADDRESS_HASH >> ADDRESS_ATTRIBUTES).build(
                                                    [ctx.tag, None, ctx.key_hash, ctx.pk_attrs])))

MERKLE_ROOT = HASH

#######################
# TRANSACTIONS MESSAGES
#######################

TX_IN = "hash" / HASH + \
        "index" / VarInt

# >>> TX_OUT.build(dict(address=dict(tag=0,
#                                    key_hash=bytearray.fromhex("380dea393a631ad563154a13bc5ee49fa4b62a60218358b5dcb875e0"),
#                                    pk_attrs=b"a"),
#                       out_value=1000))
# b'\x00\x1e8\r\xea9:c\x1a\xd5c\x15J\x13\xbc^\xe4\x9f\xa4\xb6*`!\x83X\xb5\xdc\xb8u\xe0\x01a\xcfR\xc5\xec\x00d'
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

TX_DISTRIBUTION = Struct("tag" / Int8ub,
                         Embedded(Switch(this.tag,
                         {
                             0: "number" / VarInt,
                             1: "distr" / List(Pair(HASH, COIN))
                         })))

TX_AUX = Struct("tx" / TRANSACTION,
                "witness" / TX_WITNESS,
                "distribution" / TX_DISTRIBUTION)

#######################
# DELEGATION MESSAGES
#######################

def PROXY_SECRET_KEY(w):
    """
    Creates binary structure description for specific omega.

    :param w: type of additional data (omega)
    :return: structure of proxy secret with additional data
    """
    return Struct("omega" / w,
                  "issuer_pk" / PUBLIC_KEY,
                  "delegate_pk" / PUBLIC_KEY,
                  "cert" / SIGNATURE)

def PROXY_SIGNATURE(w):
    return Struct("omega" / w,
                  "delegate_pk" / PUBLIC_KEY,
                  "cert" / SIGNATURE,
                  "sig" / SIGNATURE)

PROXY_SK_LIGHT = PROXY_SECRET_KEY(Pair(VarInt, VarInt))
PROXY_SIG_LIGHT = PROXY_SIGNATURE(Pair(VarInt, VarInt))
PROXY_SK_HEAVY = PROXY_SECRET_KEY(VarInt)
PROXY_SIG_HEAVY = PROXY_SIGNATURE(VarInt)

SEND_PROXY_SK = Struct("tag" / Int8ub,
                       "send_data" / Switch(this.tag,
                       {
                           0: PROXY_SK_LIGHT,
                           1: PROXY_SIG_HEAVY
                       }))

CONFIRM_PROXY_SK = Struct("key" / PROXY_SK_LIGHT,
                          "sig" / PROXY_SK_LIGHT)

# Examples in REPL:
# >>> cert = bytearray.fromhex("8db543c5fff7dd5dab609d04a834cda77958faf48cabee351def8985a2ec7dae71c7b2f0390caa54c61c9d41f5228e1a0b5da1c08638b99d03a1c02c81cb1607")
# >>> PROXY_SK_LIGHT.build(
#       dict( omega=[0, 10]
#           , issuer_pk=b'\x06Y\xc8\xe2u\x99\xdcG\t\xda\xb3\xbbX\xceP\xd0r\x91P\xfc#\x80\x10\xfd:h\xdc\xf0|b\x1b\xdc'
#           , delegate_pk=b'^\xaf\tDs=\xa88lBvV\xa8v\xb2\n\xe4\x11\xfahn\xa4\xbb\x16[S\xa3\x11\xc8h\xc2\x87'
#           , cert=cert))
# b'\x00\n\x06Y\xc8\xe2u\x99\xdcG\t\xda\xb3\xbbX\xceP\xd0r\x91P\xfc#\x80\x10\xfd:h\xdc\xf0|b\x1b\xdc^\xaf\tDs=\xa88lBvV\xa8v\xb2\n\xe4\x11\xfahn\xa4\xbb\x16[S\xa3\x11\xc8h\xc2\x87\x8d\xb5C\xc5\xff\xf7\xdd]\xab`\x9d\x04\xa84\xcd\xa7yX\xfa\xf4\x8c\xab\xee5\x1d\xef\x89\x85\xa2\xec}\xaeq\xc7\xb2\xf09\x0c\xaaT\xc6\x1c\x9dA\xf5"\x8e\x1a\x0b]\xa1\xc0\x868\xb9\x9d\x03\xa1\xc0,\x81\xcb\x16\x07'
# >>> PROXY_SK_LIGHT.parse(b'\x00\n\x06Y\xc8\xe2u\x99\xdcG\t\xda\xb3\xbbX\xceP\xd0r\x91P\xfc#\x80\x10\xfd:h\xdc\xf0|b\x1b\xdc^\xaf\tDs=\xa88lBvV\xa8v\xb2\n\xe4\x11\xfahn\xa4\xbb\x16[S\xa3\x11\xc8h\xc2\x87\x8d\xb5C\xc5\xff\xf7\xdd]\xab`\x9d\x04\xa84\xcd\xa7yX\xfa\xf4\x8c\xab\xee5\x1d\xef\x89\x85\xa2\xec}\xaeq\xc7\xb2\xf09\x0c\xaaT\xc6\x1c\x9dA\xf5"\x8e\x1a\x0b]\xa1\xc0\x868\xb9\x9d\x03\xa1\xc0,\x81\xcb\x16\x07')
# Container(omega=[0, 10])(issuer_pk=[6, 89, 200, 226, 117, 153, 220, 71, 9, 218, 179, 187, 88, 206, 80, 208, 114, 145, 80, 252, 35, 128, 16, 253, 58, 104, 220, 240, 124, 98, 27, 220])(delegate_pk=[94, 175, 9, 68, 115, 61, 168, 56, 108, 66, 118, 86, 168, 118, 178, 10, 228, 17, 250, 104, 110, 164, 187, 22, 91, 83, 163, 17, 200, 104, 194, 135])(cert=[141, 181, 67, 197, 255, 247, 221, 93, 171, 96, 157, 4, 168, 52, 205, 167, 121, 88, 250, 244, 140, 171, 238, 53, 29, 239, 137, 133, 162, 236, 125, 174, 113, 199, 178, 240, 57, 12, 170, 84, 198, 28, 157, 65, 245, 34, 142, 26, 11, 93, 161, 192, 134, 56, 185, 157, 3, 161, 192, 44, 129, 203, 22, 7])

#######################
# OTHER STRUCTURES
#######################

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