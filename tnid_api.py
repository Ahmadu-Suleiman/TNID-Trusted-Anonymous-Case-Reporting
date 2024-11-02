import requests

API_KEY = '<YOUR_API_KEY>'
TNID_API_URL = 'https://api.staging.v2.tnid.com/auth/create_user_otp'


def verify_phone_number(phone_number):
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.post(TNID_API_URL, json={'phone_number': phone_number})

    if response.status_code == 200:
        result = response.json()
        return result.get('verified', False)
    return False
