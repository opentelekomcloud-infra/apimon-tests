#!/usr/bin/env python3

import openstack
from urllib.parse import urljoin
from otcextensions import sdk
import json
import requests
#from pprint import pprint
#openstack.enable_logging(debug=True)

conn = openstack.connect()
sdk.register_otc_extensions(conn)


endpoints = [urljoin(endpoint.url,'/') for endpoint in conn.identity.endpoints()]
endpoint_list = (sorted(set(endpoints)))
print('##################### QUOTAS FROM OPENSTACK/PROPRIETARY API #########################')
for endpoint in endpoint_list:
    service=endpoint.split('/')[2].split('.')[0].upper()
    if 'ecs' in endpoint or 'evs' in endpoint or 'sfs' in endpoint:
        resp=conn.compute.get(endpoint + 'v2/' + conn.auth['project_id'] + '/os-quota-sets/' + conn.auth['project_id'], headers={'content-type': 'application/json'})
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
        if 'ecs' in endpoint:
            resp=conn.compute.get_limits()._body.attributes
            print(json.dumps(resp, indent=4, sort_keys=True))
    elif '/as.' in endpoint:
        resp=conn.compute.get(endpoint + 'autoscaling-api/v1/' + conn.auth['project_id'] + '/quotas')
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    elif 'ces' in endpoint:
        resp=conn.compute.get(endpoint + 'V1.0/' + conn.auth['project_id'] + '/quotas')
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    elif 'csbs' in endpoint:
        resp=conn.compute.get(endpoint + 'v1/' + conn.auth['project_id'] + '/quotas')
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    elif 'dcs' in endpoint:
        resp=conn.compute.get(endpoint + 'v1.0/' + conn.auth['project_id'] + '/quota')
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    elif 'deh' in endpoint:
        resp=conn.compute.get(endpoint + 'v1.0/' + conn.auth['project_id'] + '/quota-sets/' + conn.auth['project_id'])
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    elif 'dms' in endpoint:
        resp=conn.compute.get(endpoint + 'v1.0/' + conn.auth['project_id'] + '/quotas/dms', headers={'content-type': 'application/json'})
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    #Only old ELB
    elif 'elb' in endpoint:
        resp=conn.compute.get(endpoint + 'v1.0/' + conn.auth['project_id'] + '/elbaas/quotas')
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    elif 'ims' in endpoint:
        resp=conn.compute.get(endpoint + 'v1/cloudimages/quota')
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    elif 'kms' in endpoint:
        resp=conn.compute.get(endpoint + 'v1.0/' + conn.auth['project_id'] + '/kms/user-quotas')
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    elif 'sdrs' in endpoint:
        resp=conn.compute.get(endpoint + 'v1/' + conn.auth['project_id'] + '/sdrs/quotas')
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    elif 'vpc' in endpoint:
        resp=conn.compute.get(endpoint + 'v1/' + conn.auth['project_id'] + '/quotas')
        print('##################### ' + service + ' #########################')
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
        #Quotas extensions (openstack API) https://docs.openstack.org/api-ref/network/v2/?expanded=list-quotas-for-projects-with-non-default-quota-values-detail not supported


print('##################### QUOTAS FROM CONSOLE API #########################')
password=conn.auth['password']
domain=conn.auth['user_domain_name']
username=conn.auth['username']
prefix='userpasswordcredentials'
data=prefix + '.domain=' + domain + '&' + prefix + '.domainType=name&' + prefix + '.username=' + username + '&' + prefix + '.countryCode=0049&' + prefix + '.verifycode=&' + prefix + '.password=' + password + '&' + prefix + '.companyLogin=true&' + prefix + '.userInfoType=name&__checkbox_warnCheck=true&isAjax=true&Submit=Login'
headers={'Content-Type': 'application/x-www-form-urlencoded', 'Accept': '*/*', 'X-Language': 'en-us'}
resp = conn.compute.post('https://auth.otc.t-systems.com/authui/validateUser.action?service=https://console.otc.t-systems.com/console/', data=data, headers=headers)
url = resp.json()['redirectUrl']
print('Redirect URL: ' + url)
session = requests.Session()
response = session.get(url, headers=headers)
token='J_SESSION_ID=' + session.cookies.get_dict()['J_SESSION_ID']
headers={'Cookie': token, 'Content-Type': 'application/json', 'Accept': 'application/json', 'X-Language': 'en-us'}
print('Authentication headers:', headers)
resp=conn.compute.get('https://console.otc.t-systems.com/console/rest/quotas', headers=headers)
services=resp.json()['serviceIds']
print('############# Supported services ################')
print(services)
for service in services:
    if 'cae' in service or 'ccs' in service or 'cdn' in service or 'cloudtable' in service or 'codecheck' in service or 'codeci' in service or 'codehub' in service or 'ddm' in service or 'fgs' in service or 'projectman' in service or 'releaseman' in service or 'testman' in service:
        continue
    else:
        print('##################### ' + service.upper() + ' #########################')
        resp=conn.compute.get('https://console.otc.t-systems.com/console/rest/' + service + '/v1.0/' + conn.auth['project_id'] + '/quotas', headers=headers)
        try:
            print(json.dumps(resp.json(), indent=4, sort_keys=True))
        except:
            print(resp.reason, resp.status_code)

