import json
import hmac
import hashlib
import requests
from datetime import datetime
import sys
import os

def create_signature(payload_string, secret):
    signature = hmac.new(
        secret.encode('utf-8'),
        payload_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"

def submit_application():
    payload = {
        "action_run_link": os.environ.get('ACTION_RUN_LINK'),
        "email": "nomanaslam.devp@gmail.com",
        "name": "Noman Aslam",
        "repository_link": os.environ.get('REPOSITORY_LINK'),
        "resume_link": "https://linkedin.com/in/noman-aslam-a8383a275",
        "timestamp": datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
    }
    
    payload_string = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    
    signing_secret = "hello-there-from-b12"
    signature = create_signature(payload_string, signing_secret)
    
    headers = {
        'Content-Type': 'application/json',
        'X-Signature-256': signature
    }
    
    response = requests.post(
        'https://b12.io/apply/submission',
        data=payload_string.encode('utf-8'),
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"\n✓ SUCCESS!")
            print(f"Receipt: {result.get('receipt')}")
            return 0
    
    return 1

if __name__ == "__main__":
    sys.exit(submit_application())