#!/usr/bin/python
import sh
import os.path
import json
import sys 

apis = [
"useragentapi",
"advertiser1",
"goalsservice",
"ibidapi",
"vertigoteam",
"pixelevent",
"productdatafeedapi",
"rtbloggingapi",
"useragentapi",
"cataloguedatafeed",
"bidoptimisationapiv2",
"bidoptimisationapi",
"adscaleopenrtb"
]
for api in apis:
  old_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), api + ".old")
  new_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), api + ".new")
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
        "channel":"#vertigo",
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
  else:
    print("no diff found for " + api)
