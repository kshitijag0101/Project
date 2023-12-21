import requests,json
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

        response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
        return response.json().get("data", {}).get("companyData", {}).get("emailAddress")
    except Exception as e:
        print("#######", e)
        return False
from datetime import datetime
start_datetime = datetime.now()
print(start_datetime)
get_email("U51202OD2023PTC043874")

end_datetime = datetime.now()
print( end_datetime, end_datetime-start_datetime)