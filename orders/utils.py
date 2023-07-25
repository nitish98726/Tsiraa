
import requests
from django.http import JsonResponse

def pincode_lookup():
    url = 'https://staging-express.delhivery.com/c/api/pin-codes/json/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token c7455929fcbc3300158c3cf44d18a2cc6fe1d7d6'
    }
    params = {
        'filter_codes': '141010'
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(data)
    # return JsonResponse(data)
# pincode_lookup()
def invoice_charges():
    url = 'https://track.delhivery.com/api/kinko/v1/invoice/charges/.json'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token c7455929fcbc3300158c3cf44d18a2cc6fe1d7d6'
    }
    params = {
        'md': 'E',
        'ss': 'DTO',
        'd_pin': '110085',
        'o_pin': '141010',
        'cgm': '400',
        
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(data)
    # return JsonResponse(data)
invoice_charges()