import mysql.connector
from mysql.connector import Error
import pandas as pd

try:
    db_config = {
        'host': '52.66.53.122',
        'user': 'root',
        'password': 'django@123',
        'database': 'django_project',
    }
    # Connect to the database
    conn = mysql.connector.connect(**db_config)

    if conn.is_connected():
        query = "SELECT * FROM data_app_bulkfilemodels where is_active = true and file_name = 'llp_20231215225518.xlsx';"
        df = pd.read_sql(query, con=conn)
        for row in df.loc[:].itertuples():
            print(row.id, row.file_name, row.file_url, row.month, row.year)
            read_file_df = pd.read_excel(row.file_url)
            read_file_df['month'] = row.month
            read_file_df['file_name'] = row.file_name
            read_file_df = read_file_df.fillna("")
            if "indian_" in row.file_name:
                read_file_df['date_of_registration'] = pd.to_datetime(read_file_df['date_of_registration'], dayfirst=True).dt.date
                read_file_df['CIN'] = read_file_df['CIN'].str.strip()
                read_file_df['authorized_capital'] = read_file_df['authorized_capital'].astype("float")
                read_file_df['paid_up_capital'] = read_file_df['paid_up_capital'].astype("float")
                read_file_df['year'] = int(row.year)
                read_file_df = read_file_df.fillna("")
                data_point = ['CIN', 'company_name',"date_of_registration", "month_name", "state", "roc", "company",
                              "category", "company_type", "authorized_capital", "paid_up_capital", "activity",
                              "activity_description", "description", "registered_office_address", "year", "month", "file_name"]
                read_file_df = read_file_df[data_point]
                print(read_file_df)
                values_tuple = tuple(data_point)
                cursor = conn.cursor()
                try:
                    for data in read_file_df.loc[:].itertuples(index=False):
                        exists_df = pd.read_sql(f"SELECT * FROM data_app_indiancompany WHERE CIN='{data.CIN}'", con=conn)
                        if data.authorized_capital != "" and not pd.isnull(data.authorized_capital):
                            authorized_capital = data.authorized_capital
                        else:
                            authorized_capital = None

                        if data.paid_up_capital != "" and not pd.isnull(data.paid_up_capital):
                            paid_up_capital = data.paid_up_capital
                        else:
                            paid_up_capital = None
                        if len(exists_df) == 0:
                            insert_query = """
                                        INSERT INTO data_app_indiancompany 
                                        (CIN, company_name, date_of_registration, month_name, state, roc, company, category, 
                                        company_type, authorized_capital, paid_up_capital, activity, activity_description, description, 
                                        registered_office_address, year, month, file_name) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """
                            values_list = (data.CIN, data.company_name, data.date_of_registration,
                                                  data.month_name, data.state, data.roc, data.company,  data.category,
                                                  data.company_type,  authorized_capital,  paid_up_capital, data.activity,
                                                  data.activity_description,  data.description, data.registered_office_address,
                                           row.year, row.month, row.file_name
                                                  )
                            cursor.execute(insert_query, values_list)
                            conn.commit()
                        else:
                            update_sql = """ UPDATE data_app_indiancompany SET
                                 company_name = %s, date_of_registration = %s,  month_name = %s,
                                state = %s, roc = %s, company = %s, category = %s, company_type = %s,  authorized_capital = %s,
                                paid_up_capital = %s,activity = %s, activity_description = %s, description = %s, registered_office_address = %s,
                                 year = %s, month = %s, file_name = %s
                                WHERE CIN = %s;
                            """
                            values_list = ( data.company_name, data.date_of_registration,
                                           data.month_name, data.state, data.roc, data.company, data.category,
                                           data.company_type, authorized_capital, paid_up_capital, data.activity,
                                           data.activity_description, data.description, data.registered_office_address,
                                            row.year, row.month, row.file_name,
                                            data.CIN
                                           )
                            cursor.execute(update_sql, values_list)
                            conn.commit()
                    cursor.execute(f"UPDATE data_app_bulkfilemodels SET is_active = false Where id = {row.id}")
                    conn.commit()
                except Exception as e:
                    print("errr")
            elif "llp_" in row.file_name:
                read_file_df['founded'] = pd.to_datetime(read_file_df['founded'], dayfirst=True).dt.date
                read_file_df['LLPIN'] = read_file_df['LLPIN'].str.strip()
                read_file_df['obligation_of_contribution'] = read_file_df['obligation_of_contribution'].astype("float")
                read_file_df['year'] = int(row.year)
                read_file_df = read_file_df.fillna("")

                data_point = ['LLPIN', 'llp_name', 'founded', 'roc_location', 'status', 'industrial_activity',
                              'activity_description', 'description', 'obligation_of_contribution', 'number_of_partners',
                              'number_of_designated_partners', 'state', 'district', 'address',
                              "year", "month", "file_name"]
                read_file_df = read_file_df[data_point]
                print(read_file_df)
                values_tuple = tuple(data_point)
                cursor = conn.cursor()
                try:
                    for data in read_file_df.loc[:].itertuples(index=False):
                        exists_df = pd.read_sql(f"SELECT * FROM data_app_llpcompany WHERE LLPIN='{data.LLPIN}'",
                                                con=conn)
                        if data.obligation_of_contribution != "" and not pd.isnull(data.obligation_of_contribution) and\
                                type(data.obligation_of_contribution) == float:
                            obligation_of_contribution = float(data.obligation_of_contribution)
                        else:
                            obligation_of_contribution = None

                        if data.number_of_partners != "" and not pd.isnull(data.number_of_partners) and \
                                type(data.number_of_partners) == int:
                            number_of_partners = data.number_of_partners
                        else:
                            number_of_partners = None
                        if len(exists_df) == 0:
                            insert_query = """
                                    INSERT INTO data_app_llpcompany 
                                    (LLPIN, llp_name, founded, roc_location, status, industrial_activity, 
                              activity_description, description, obligation_of_contribution, number_of_partners,
                              number_of_designated_partners, state, district, address, year, month, file_name) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                                    """
                            values_list = (data.LLPIN, data.llp_name, data.founded, data.roc_location, data.status,
                                           data.industrial_activity, data.activity_description, data.description,
                                           obligation_of_contribution, number_of_partners,
                                           data.number_of_designated_partners,
                                           data.state, data.district, data.address,
                                           row.year, row.month, row.file_name
                                           )
                            cursor.execute(insert_query, values_list)
                            conn.commit()
                        else:
                            update_sql = """ UPDATE data_app_llpcompany SET
                                            llp_name = %s, founded = %s, roc_location = %s, status = %s, 
                                            industrial_activity = %s, activity_description = %s, description = %s, 
                                            obligation_of_contribution = %s, number_of_partners = %s,
                                            number_of_designated_partners = %s, state = %s, district = %s, 
                                            address = %s, year = %s, month = %s, file_name = %s
                                            WHERE LLPIN = %s;
                                            """
                            values_list = (data.llp_name, data.founded, data.roc_location, data.status,
                                           data.industrial_activity, data.activity_description, data.description,
                                           obligation_of_contribution, number_of_partners,
                                           data.number_of_designated_partners,
                                           data.state, data.district, data.address,
                                           row.year, row.month, row.file_name, data.LLPIN
                                           )
                            cursor.execute(update_sql, values_list)
                            conn.commit()
                    cursor.execute(f"UPDATE data_app_bulkfilemodels SET is_active = false Where id = {row.id}")
                    conn.commit()
                except Exception as e:
                    print("errr")
            elif "fcin_" in row.file_name:
                read_file_df['date'] = pd.to_datetime(read_file_df['date'], dayfirst=True).dt.date
                read_file_df['FCIN'] = read_file_df['FCIN'].str.strip()
                read_file_df['year'] = int(row.year)
                read_file_df = read_file_df.fillna("")
                data_point =['FCIN', 'company_name', 'date', 'status', 'activity', 'activity_description',
                        'description', 'office_type', 'address', 'state', "year", "month", "file_name"]
                read_file_df = read_file_df[data_point]
                print(read_file_df)
                values_tuple = tuple(data_point)
                cursor = conn.cursor()
                try:
                    for data in read_file_df.loc[:].itertuples(index=False):
                        exists_df = pd.read_sql(f"SELECT * FROM data_app_fcincompany WHERE FCIN='{data.FCIN}'", con=conn)
                        if len(exists_df) == 0:
                            insert_query = """
                                 INSERT INTO data_app_fcincompany 
                                       (FCIN, company_name, date, status, activity, activity_description,
                                            description, office_type, address, state, year, month, file_name) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                                                    """
                            values_list = (data.FCIN, data.company_name, data.date, data.status, data.activity,
                                           data.activity_description, data.description, data.office_type,
                                           data.address,  data.state,
                                           row.year, row.month, row.file_name
                                           )
                            cursor.execute(insert_query, values_list)
                            conn.commit()
                        else:
                            update_sql = """ UPDATE data_app_fcincompany SET
                                                 company_name = %s, date = %s, status = %s, activity = %s,
                                                activity_description = %s, description = %s, office_type = %s,
                                                address = %s,  state= %s, year = %s, month = %s, file_name = %s
                                                 WHERE FCIN = %s;
                                                            """
                            values_list = (data.company_name, data.date, data.status, data.activity,
                                           data.activity_description, data.description, data.office_type,
                                           data.address, data.state,
                                           row.year, row.month, row.file_name, data.FCIN
                                           )
                            cursor.execute(update_sql, values_list)
                            conn.commit()
                    cursor.execute(f"UPDATE data_app_bulkfilemodels SET is_active = false Where id = {row.id}")
                    conn.commit()
                except Exception as e:
                    print("errr", e)


except Error as e:
    print(f"Error: {e}")

finally:
    if conn.is_connected():
        conn.close()
        print("Connection closed")


# S3 Insert - Done
# insert db -
# status
