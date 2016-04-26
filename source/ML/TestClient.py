# -*- coding: utf-8 -*-
import os
import sys
import msgpackrpc

client = msgpackrpc.Client(msgpackrpc.Address("127.0.0.1", 6000))
result = client.call('predict',[30,1,46.3288,0,-22.411464,-0.028708,-4.91025,20.8182,52.89575,17.55085,73.233,41.6452,66.726])
print str(result)