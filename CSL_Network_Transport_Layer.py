#TODO: add support for multiple LWCIds (dict)
#TODO: update create and close LWC to use construct

from CSL_Status_Codes import *

from CSL_Structures import *
import socket
import random

class NetworkTransportLayer:
    
    def __init__(self):
        """
        """
        self.STATUS_CRAF = b"\x00\x00\x00\x00"
        self.STATUS_CRIF = b"\x00\x00\x00\x01"
        self.STATUS_CNCF = b"\x00\x00\x00\x00"
        self.STATUS_CC = b"\x00\x00\x00\x01"
        self.STATUS_CS = b"\x00\x00\x00\x02"
        self.COMMS_ERROR = -1
        self.COMMS_OK = 0
        
        # hardcoded for now, don't think it matters, since we aren't actually
        # a node...
        self.node_id = 0
        
    def build_craf_msg(self):
        """
        """
        return self.STATUS_CRAF
        
    def build_crif_msg(self):
        """
        """
        return self.STATUS_CRIF
        
    def build_cncf_msg(self, lwc_id):
        """
        """
        return b"%s%s" % (self.STATUS_CNCF, lwc_id.to_bytes(4, byteorder="big"))
        
    def build_cc_msg(self, lwc_id):
        """
        """
        return b"%s%s" % (self.STATUS_CC, lwc_id.to_bytes(4, byteorder="big"))
        
    def build_cs_msg(self, lwc_id):
        """
        """
        return b"%s%s" % (self.STATUS_CS, lwc_id.to_bytes(4, byteorder="big"))

    def build_data_msg(self, mid, data_bytes):
        """
        """
        # Convert the message id (lwcid or epid) to a word32
        mid_bytes = mid.to_bytes(4, byteorder="big")
        
        # Calculate the data size
        size_bytes = len(data_bytes).to_bytes(4, byteorder="big")
        
        # Create a properly formatted message
        message = b"%s%s%s" % (mid_bytes, size_bytes, data_bytes)
        
        return message
    
    def create_lightweight_connection(self, target_ip, target_port, target_ep_id):
        """
        """
        # Init
        self.target_ip = target_ip
        self.target_port = target_port
        self.target_ep_id = target_ep_id
        
        # Create TCP connection
        self.conn = socket.socket()
        self.conn.connect((self.target_ip.encode(), self.target_port))
        
        # Host info for creating a LWC
        self.host_ip = self.conn.getsockname()[0]
        self.host_port = self.conn.getsockname()[1]
        
        # Build the data message (see CSL docs)
        addr_bytes = b"%s:%s:%s" % (self.host_ip.encode(), str(self.host_port).encode(), str(self.node_id).encode())
        data_message = self.build_data_msg(self.target_ep_id, addr_bytes)
        self.conn.send(data_message)
        
        # Receive the status response
        res = self.conn.recv(1024)
        
        if res == self.STATUS_CRAF:
            print("INFO: connection accepted")
        elif res == self.STATUS_CRIF:
            print("ERROR: connection refused")
            return STATUS_COMMS_ERROR
        else:
            print("ERROR: unexpected response: %s" % res)
            return STATUS_COMMS_ERROR
        
        # Create new LWCId (first 1024 (starting with 0) LWCIds are reserved)
        self.lwc_id = random.randrange(1024, 4096)
        
        # Generate and send the CNCF response
        cncf_message = self.build_cncf_msg(self.lwc_id)
        self.conn.send(cncf_message)
        
        return STATUS_COMMS_OK
        
    def close_heavyweight_connection(self):
        """
        """
        closed = False
        
        # Build and send the close connection message
        cs_message = self.build_cs_msg(self.lwc_id)
        self.conn.send(cs_message)
        
        # Receive the closure response
        res = self.conn.recv(1024)
        
        if res == cs_message:
            print("INFO: Heavyweight connection closed")
            closed = True
        else:
            print("ERROR: Failed to close heavyweight connection")
        
        return closed
        
    def format_msg(self, control_header = None, msg_type = None, msg_data = None):
        """
        """
        msg_components = []
        msg_data_chunks = []
        
        # Split the message components on 0x100 byte boundaries
        msg_data_chunks = [msg_data[i:i + DATA_MAX] for i in range(0, len(msg_data), DATA_MAX)]
            
        # Build the control header message
        if control_header is not None:
            control_header_msg = DATA_MSG.build(dict(lwcid = self.lwc_id, size = len(control_header), msg = control_header))
            #msg_components["control_header"] = control_header_msg
            msg_components.append(control_header_msg)
            
        # Build the message name message
        if msg_type is not None:
            msg_type_msg = DATA_MSG.build(dict(lwcid = self.lwc_id, size = len(msg_type), msg = msg_type))
            #msg_components["msg_type"] = msg_type_msg
            msg_components.append(msg_type_msg)
        
        # Build the message data message
        if msg_data is not None:
            for chunk in msg_data_chunks:    
                msg_data_msg = DATA_MSG.build(dict(lwcid = self.lwc_id, size = len(chunk), msg = chunk))
                #msg_components["msg_data"] = msg_data_msg
                msg_components.append(msg_data_msg)
            
        return msg_components
        
    def transport_msg(self, msg_type, msg):
        """
        """
        follow_up = False
        
        # Send the message
        self.conn.send(msg)
        
        # Terminate if sending a unidirectional message
        if msg_type in UND_TRANS:
            return None
        
        res = self.conn.recv(1024)
        
        #TODO: add handling for different response types
        # Check the response
        if res[0:4] == self.STATUS_CNCF:
            if res[-4] != self.lwc_id.to_bytes(4, byteorder="big"):
                # Bidirectional
                self.bid_lwc_id = int.from_bytes(res[-4:], byteorder="big")
                # Expect another message
                follow_up = True
        
        # Get follow-up based on response
        if follow_up:
            res = self.conn.recv(8192)
            
        return res
        
        
        
        
    
