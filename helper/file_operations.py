import pandas as pd
from variables.variables import excel_storage_path

async def write_to_excel(user_excel_data, file_name, path=excel_storage_path):
    df = pd.DataFrame(
        {
            'id': user_excel_data['id'],
            'access_hash': user_excel_data['access_hash'],
            'username': user_excel_data['username'],
            'first_name': user_excel_data['first_name'],
            'last_name': user_excel_data['last_name'],
            'mutual_contact': user_excel_data['mutual_contact'],
            'phone': user_excel_data['phone'],
            'sending_report': user_excel_data['sending_report'] if user_excel_data.get("sending_report") else ["-" for i in range(0, len(user_excel_data['id']))]
        }
    )

    file_name = "data.xlsx" if not file_name else file_name + ".xlsx"
    file_full_path = path + file_name
    df.to_excel(file_full_path, sheet_name='Sheet1')
    print(f'\nExcel was writting')
    return file_full_path
