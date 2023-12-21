from .models import IndianCompany, FCINCompany, LLPCompany
import requests
from django.db.models import Q
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def get_email(cin):
    try:
        url = "https://www.mca.gov.in/bin/MDSMasterDataServlet"
        payload = json.dumps({
            "ID": str(cin).replace(" ", ""),
            "requestID": "cin",
        })
        headers = {
            'authority': 'www.mca.gov.in',
            'accept': 'application/json, text/javascript, /; q=0.01',
            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.mca.gov.in',
            'referer': 'https://www.mca.gov.in/content/mca/global/en/mca/master-data/MDS.html',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("data", {}).get("companyData", {}).get("emailAddress")
    except Exception as e:
        print("#######", e)
        return False

@csrf_exempt
def updateEmailData(request):
    if request.method == 'POST':
        indians = IndianCompany.objects.filter(Q(email="") | Q(email__isnull=True))
        for indian in indians:
            email = get_email(indian.CIN)
            if email:
                indian.email = email
                indian.save()

        llps = LLPCompany.objects.filter(Q(email="") | Q(email__isnull=True))
        for llp in llps:
            email = get_email(llp.LLPIN)
            if email:
                llp.email = email
                llp.save()

        fcins = FCINCompany.objects.filter(Q(email="") | Q(email__isnull=True))
        for fcin in fcins:
            email = get_email(fcin.FCIN)
            if email:
                fcin.email = email
                fcin.save()
        return JsonResponse({'message': 'Data updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})


