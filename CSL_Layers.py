from CSL_Status_Codes import *
from construct import *

def connect_dec(func):
    """
    """
    
    def func_wrapper(self, ip, port, ep_id):
        """
        """                
        # Call original function
        func(self, ip, port, ep_id)

        # Let NT layer handle connecting
        self.create_lightweight_connection(ip, port, ep_id)
            
    return func_wrapper
       
def disconnect_dec(func):
    """
    """
    
    def func_wrapper(self):
        """
        """
        # Call the original function
        func(self)
        
        # Delete the heavyweight connection
        self.close_heavyweight_connection()
        
    return func_wrapper
    
def generate_msg_dec(func):
    """
    """
    
    def func_wrapper(self, **kwargs):
        """
        """
        # Call the original function
        func(self)
        
        # Encode the message type
        encoded_msg_name = self.encode_msg(kwargs["msg_type"]) 
        
        # Assemble the message data
        msg_data = self.build_arg_dict(**kwargs)
       
        # Build the control header
        control_header = self.build_control_header(kwargs["msg_type"])
        
        # Format the message for transmission
        msg_components = self.format_msg(control_header, encoded_msg_name, msg_data)
        
        # Return the dict of generated pieces
        return msg_components
        
    return func_wrapper
        
def send_msg_dec(func):
    """
    """
    
    def func_wrapper(self, msg_type, msg):
        """
        """
        # Send the message
        res = self.transport_msg(msg_type, msg)
        
        return res
            
    return func_wrapper
        
        

