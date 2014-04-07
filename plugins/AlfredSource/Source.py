#!/usr/bin/env python3
import subprocess
import json

class AlfredSource:
    def __init__(self,request_data_type = 158):
        self.request_data_type = request_data_type

    def nodes(self):
        output = subprocess.check_output(["alfred-json","-r",str(self.request_data_type),"-f","json"])
        alfred_data = json.loads(output.decode("utf-8"))
        nodes = []
        for mac, values in alfred_data.items():
            nodes.append({
                    'mac': mac,
                    'name': values.get('hostname'),
                    'contact': values.get('owner', {}).get('contact'),
                    'vpn': values.get('software', {}).get('fastd', {}).get('enabled'),
                    'online': 1,
                    })
        return nodes

if __name__ == "__main__":
    ad = Alfred()
    al = ad.nodes()
    print(al)
