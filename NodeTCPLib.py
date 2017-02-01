import socket
import random

class NodeTCPInstance:

    def __init__(self, node_ip, node_port):
        """
        """
        self.STATUS_OK = b"\x00\x00\x00\x00\x00\x00\x04\x00"
        self.STATUS_CRAF = b"\x00\x00\x00\x00"
        self.STATUS_CRIF = b"\x00\x00\x00\x01"
        self.STATUS_CNCF = b"\x00\x00\x00\x00"
        self.STATUS_CC = b"\x00\x00\x00\x01"
        self.STATUS_CS = b"\x00\x00\x00\x02"
        self.COMMS_ERROR = -1
        
        self.conn = socket.socket()
        self.conn.connect((node_ip.encode(), node_port))
        
        self.host_ip = self.conn.getsockname()[0]
        self.host_port = self.conn.getsockname()[1]
        
        
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
        
    def create_lightweight_connection(self, ep_id, node_id, lwc_id = None):
        """
        """   
        # Build the data message (see CSL docs)
        addr_bytes = b"%s:%s:%s" % (self.host_ip.encode(), str(self.host_port).encode(), str(node_id).encode())
        data_message = self.build_data_msg(ep_id, addr_bytes)
        self.conn.send(data_message)
        
        # Receive the status response
        res = self.conn.recv(1024)
        
        if res == self.STATUS_CRAF:
            print("INFO: connection accepted")
        elif res == self.STATUS_CRIF:
            print("ERROR: connection refused")
            return self.COMMS_ERROR
        else:
            print("ERROR: unexpected response: %s" % res)
            return self.COMMS_ERROR
        
        # Create new connection id if one was not provided (first 1024 (starting with 0) lwcids are 
        # reserved)
        if lwc_id is None:
            lwc_id = random.randrange(1024, 4096)
        
        # Generate and send the CNCF response
        cncf_message = self.build_cncf_msg(lwc_id)
        self.conn.send(cncf_message)
        
        # TODO: update return value to something more useful
        return lwc_id
        
    def close_heavyweight_connection(self, lwc_id):
        """
        """
        closed = False
        
        # Build and send the close connection message
        csMessage = self.build_cs_msg(lwc_id)
        self.conn.send(csMessage)
        
        # Receive the closure response
        res = self.conn.recv(1024)
        
        if res == csMessage:
            print("INFO: heavyweight connection closed")
            closed = True
        else:
            print("ERROR: failed to close heavyweight connection")
        
        return closed
        
    def get_blocks(self, lwc_id, oldest_hash, newest_hash, nonce = None):
        """
        """
        # Create the nonce if needed
        if nonce is None:
            nonce = random.randrange(0, 0xFFFFFFFFFFFFFFFF)
        nonce_bytes = nonce.to_bytes(8, byteorder = "big")
        
        # Add the control code byte
        nonce_bytes = b"%s%s" % (b"S", nonce_bytes)
        
        # Build the control header
        control_header = self.build_data_msg(lwc_id, nonce_bytes)
        
        # Send the control header
        #conn.send(controlHeader)
        
        # Build the GetBlocks message
        message_name_bytes = b"GetBlocks"
        # TODO: this only works with names less than 0x80 characters in length
        encoded_message_name_bytes = b"%s%s" % (len(message_name_bytes).to_bytes(1, byteorder="big"), message_name_bytes)
        message_name_data = self.build_data_msg(lwc_id, encoded_message_name_bytes)
        
        message_parameter_bytes = b"%s%s" % (oldest_hash, newest_hash)
        message_parameter_data = self.build_data_msg(lwc_id, message_parameter_bytes)
        
        # Send the GetBlocks data message
        self.conn.send(b"%s%s%s" % (control_header, message_name_data, message_parameter_data))
        
        # Receive the status
        status = self.conn.recv(1024)
        
        if (status == self.STATUS_OK):
            print("INFO: Node accepted GetBlocks request")
        else:
            print("ERROR: Node did not accept GetBlocks request")
            print("INFO: Received instead: %s" % status)
            return self.COMMS_ERROR
        
        # Receive the requested data
        #TODO: data can be larger than this, add proper handling of large 
        # transmissions
        res = self.conn.recv(8192)
        
        return res
        
    def close_socket(self):
        """
        """
        self.conn.close()
