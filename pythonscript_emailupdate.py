import mysql.connector
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

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("data", {}).get("companyData", {}).get("emailAddress")
    except Exception as e:
        print("#######", e)
        return False
# Database connection parameters
db_config = {
    'host': '52.66.53.122',
    'user': 'root',
    'password': 'django@123',
    'database': 'django_project',
}

# Create a connection
connection = mysql.connector.connect(**db_config)

try:
    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    select_query = "SELECT DISTINCT CIN FROM data_app_indiancompany WHERE email = '' OR email IS NULL;"
    cursor.execute(select_query)
    records = cursor.fetchall()
    for record in records:
        record_id = record[0]
        fecth_email = get_email(record_id)
        if fecth_email:
            updated_value = fecth_email
            update_query = "UPDATE data_app_indiancompany SET email = %s WHERE CIN = %s"
            update_data = (updated_value, record_id)
            cursor.execute(update_query, update_data)
            connection.commit()
            print(f"Record with id {record_id} updated.")
except mysql.connector.Error as err:
    print(f"Error: {err}")


try:
    cursor = connection.cursor()
    select_query = "SELECT DISTINCT LLPIN FROM data_app_llpcompany WHERE email = '' OR email IS NULL;"
    cursor.execute(select_query)
    records = cursor.fetchall()
    for record in records:
        record_id = record[0]
        fecth_email = get_email(record_id)
        if fecth_email:
            updated_value = fecth_email
            update_query = "UPDATE data_app_llpcompany SET email = %s WHERE LLPIN = %s"
            update_data = (updated_value, record_id)
            cursor.execute(update_query, update_data)
            connection.commit()
            print(f"Record with id {record_id} updated.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

try:
    cursor = connection.cursor()
    select_query = "SELECT DISTINCT FCIN FROM data_app_fcincompany WHERE email = '' OR email IS NULL;"
    cursor.execute(select_query)
    records = cursor.fetchall()
    for record in records:
        record_id = record[0]
        fecth_email = get_email(record_id)
        if fecth_email:
            updated_value = fecth_email
            update_query = "UPDATE data_app_fcincompany SET email = %s WHERE FCIN = %s"
            update_data = (updated_value, record_id)
            cursor.execute(update_query, update_data)
            connection.commit()
            print(f"Record with id {record_id} updated.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection.is_connected():
        connection.close()
        print("Connection closed.")
