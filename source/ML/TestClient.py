# -*- coding: utf-8 -*-
import os
import sys
import msgpackrpc

client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
result = client.call('predict',3)
print result