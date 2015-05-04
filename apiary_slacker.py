#!/usr/bin/python
import sh
import os.path
import json
import sys 

apis = ["useragentapi"]
for api in apis:
  old_file = api + ".old"
  new_file = api + ".new"
  new_out = open(new_file,'w')
  sh.apiary(["fetch", "--api-name", api], _out=new_out)
  if not os.path.isfile(old_file):
    sh.cp(new_file,old_file)
  diff = sh.diff(old_file,new_file,_ok_code=[0,1])
  sh.mv(new_file,old_file)
  if len(diff) > 0:
    print("diff found!")
    message = str(diff)
    titleurl = "http://docs."+api+".apiary.io"
    premessage = "api " + titleurl + " changed"
    print message
    payload = {
        "channel":"#testing-webhooks",
        "username":"apiarybot",
        "text": premessage,
        "icon_emoji":":ghost:",
        "attachments" : [
          {
            "color":"good",
            "fields":[
              {
                "title":"Diff",
                "value":message,
                "short":False
                }
              ]
            }
          ]
        }
    payload = "payload=" + json.dumps(payload)
    print(payload)
    sh.curl(["curl", "-X", "POST" ,"--data-urlencode" ,payload,sys.argv[1]])
