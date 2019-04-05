from pprint import pprint	
import requests
import json
from datetime import datetime
#API host MUST have http:// prepended to it if you are using http, defaults to https
host= "http://kb.inquest.net"

token="eyJhbGciOiJIUzUxMiJ9.eyJpZCI6MjR9.L0E51ZHCxWmY32AhZa5Jyz9W1OyqPNabguf2KGaFkBNoLjLimsCxbyuXpvAV7GEe9hsKGAYqmPxIa1JNmn1Oxw"
secret="46723d1f4c8edb06fd2e6fc6d4c828f7a7d6ae66ca3f3275"

headers= {"Content-Type": "application/json;charset=UTF-8"}
params= {"token": token, "secret_key":secret}

def retire_c2(id):
    c2= get_c2(id)
    c2["state"]="Retired"

    return requests.put(url= host+"/ThreatKB/c2ips/"+str(id), headers=headers, data=json.dumps(c2),params=params).ok

def isExpired(expired):
    expiredDate=datetime.strptime(expired,'%Y-%m-%dT%H:%M:%S')
    return datetime.now() > expiredDate

def get_all_c2ips():
    print("Making request")
    response= requests.get(url= host+'/ThreatKB/c2ips', params=params)
    print("request made")
    if(response.ok):
        print("request is legit")
        return json.loads(response.content)
    else:
        return None

   
def expiration_daemon():
    c2ips= get_all_c2ips() 
    for c2 in c2ips["data"]:
        pprint(c2)
        expire_date = c2["expiration_timestamp"]
        if(expire_date is not None):
            if(isExpired(expire_date)):
                retire_c2(c2["id"])
                print("C2 Expired, retiring")
       
       
def get_c2_state(id):
    c2 = get_c2(id)
    return c2["state"]


def delete_c2ip(id):
    return requests.delete(url= host+"/ThreatKB/c2ips/"+str(id), headers=headers, params=params).ok


def discard_c2ip_by_ip(ip):
    id = get_c2ips_id(ip)
    if(id is not None):
        discard_c2(id)
    else:
        return None


def get_c2ips_comments(ip):
    id = get_c2ips_id(ip)

    if( id is not None):
        return json.loads(requests.get(url= host+"/ThreatKB/comments?entity_type=3&entity_id="+str(id), headers=headers, params=params).content)
    else:
        print("IP not found")
        return None

def get_c2(id):
    response= requests.get(url= host+'/ThreatKB/c2ips/'+str(id), params=params)
    if(response.ok):
        return json.loads(response.content)
    else:
        return None

def get_c2ips_id(ip):
    results= requests.get(url= host+'/ThreatKB/c2ips?searches={"ip":"'+ip+'"}', params=params).json()
    if(results["total_count"] != 0):
        for item in results["data"]:
            return item["id"] # we are only matching the first one
    else:
        return None

def get_c2ips_comments(ip):
    id = get_c2ips_id(ip)

    if( id is not None):
        return requests.get(url= host+"/ThreatKB/comments?entity_type=3&entity_id="+str(id), headers=headers, params=params).content

    else:
        print("IP not found")
        return None



expiration_daemon()

#id = get_c2ips_id("122.99.197.89")

#c2 = get_c2(id)

#print(c2["expiration_timestamp"])
#if(isExpired(c2["expiration_timestamp"])):
#    retire_c2(id)




