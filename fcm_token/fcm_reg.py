import requests
import os

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'checkin'))
from checkin import getToken

def register_fcm(gsf_id, sec_token, device_profile, app_details):
    print("[*] Sending FCM Registration Request...")
    fcm_register_url = "https://android.clients.google.com/c2dm/register3"
    
    auth_header = f"AidLogin {gsf_id}:{sec_token}"
    user_agent = f"Android-GCM/1.5 ({device_profile.get('ro.product.system.device', 'unknown')} {device_profile.get('ro.system.build.id', 'unknown')})"
    
    headers = {
        "Authorization": auth_header,
        "User-Agent": user_agent,
    }
    
    form_data = {
        "app": app_details['package_name'],
        "cert": app_details['signature_hash'],
        "app_ver": app_details['version'],
        "sender": app_details['sender_id'],
        "device": gsf_id,
        "target_ver": device_profile.get('ro.system.build.version.sdk'),
        "X-scope": "*",
        # "X-gmp_app_id": app_details['gmp_app_id']
    }

    response = requests.post(fcm_register_url, headers=headers, data=form_data)
    response.raise_for_status()
    
    print(f"[*] FCM STATUS CODE: {response.status_code}")
    # print(f"Response Text: {response.text}")

    if response.text.startswith("token="):
        fcm_token = response.text.split("=")[1].strip()
        return fcm_token
    else:
        raise Exception(f"[-] FCM Registration failed: {response.text}")


def getFcm():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        DEVICE_PROFILE_PATH = os.path.join(script_dir, 'data')
        # ----- FIX APP_DETAILS ----- #
        APP_DETAILS = {
            "package_name": "YOUR_APP_PACKAGENAME_HERE",
            "sender_id": "YOUR_SENDER_ID_HERE",
            "version": 0, # FIX YOUR_VERSION_HERE(INT)
            "signature_hash": "FIX_TO_YOUR_SIGN_HERE",
        }
        # checkin logic -> ret androidId & SecrityToken
        gsf_id, sec_token, device_profile = getToken(DEVICE_PROFILE_PATH)

        fcm_token = register_fcm(gsf_id, sec_token, device_profile, APP_DETAILS)

        print('[+] Successfully issued FCM token')
        print(f'[*] fcm_token: {fcm_token}')
        return fcm_token
        
        
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        return ''
