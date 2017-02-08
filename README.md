# tcp_connector

## Adding Support for New Messages
* Add the message data format (as a Python construct) to CSL_Structures.py
* Add message type to either the BID or UND transaction list in CSL_Structures.py
* Add application-level message handler to CSL_Application_Layer.py
  * Add message handling to "build_arg_dict()"
  * Write function for building the message data
* Add control code to CSL_TIME_WARP_Layer.py
  * Update self.cc_msg_type_mapping with the correct control code
    * At this point, only "S" (0x53) and "U" (0x55) are supported
* Add test code to CSL_TCP_Harness.py
