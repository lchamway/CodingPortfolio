import requests
import json

employee_api = 'https://api.restpoint.io/api/employee'
license_api = 'https://api.restpoint.io/api/License'
header = 'x-endpoint-key=96d0eaae000a4e36814ae5f807ae5410'

url = employee_api + '?' + header
l_url = license_api + '?' + header

def get_employees():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        employees = data.get('data', [])
        return employees
    # else:
    #     print('Error: ' + str(response.status_code))

def check_license(name):
    l_url = license_api + '/' + name + '?' + header
    response = requests.get(l_url)
    if response.status_code == 200:
        data = response.json()
        status = data.get('license_status')
        return status
    
def change_status(name, new_status):
    url = license_api + '/' + name + '?' + header
    headers = {
    'headerKey': header,
    'Content-Type': 'application/json'
    }

    old_data = requests.get(url)
    user = old_data.json()
    data = {
        "id": user['id'],
        "license_status": new_status
    }
    response = requests.patch(url, headers=headers, json=data)



def get_employee_by_id(employee_id):
    url = employee_api + '/' + employee_id + '?' + header
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    # else:
    #     print('Error: ' + str(response.status_code))

def enter_new_employee(employee_id, employee_name, employee_pass):
    url = employee_api + '?' + header
    data = {
        'id': employee_id,
        'name': employee_name,
        'log_status': False,
        'password': employee_pass,
        'role': "worker",
        'dates_logged': "{}"
    }
    headers ={
          'headerKey': header,
          'Content-Type': 'application/json',
          'accept': 'application/json',
        }  # Set the Content-Type header to application/json

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return True
    # else:
    #     print('Error:', response.status_code, response.text)

def enter_new_admin(employee_id, employee_name, employee_pass):
    url = employee_api + '?' + header
    data = {
        'id': employee_id,
        'name': employee_name,
        'log_status': False,
        'password': employee_pass,
        'role': "admin",
        'dates_logged': "{}"
    }
    headers ={
          'headerKey': header,
          'Content-Type': 'application/json',
          'accept': 'application/json',
        }  # Set the Content-Type header to application/json

    response = requests.post(url, headers=headers, json=data)
    
    # if response.status_code == 200:
    #     print('Employee added successfully')
    # else:
    #     print('Error:', response.status_code, response.text)
 
def delete_employee(employee_id):
    url = employee_api + '/' + employee_id + '?' + header

    headers = {
    'headerKey': header,  # Replace with the actual access token if needed
    'Content-Type': 'application/json'
    }

    response = requests.delete(url, headers=headers)
    # if response.status_code == 200:
    #     print('Employee deleted successfully')
    # else:
    #     print('Error:', response.status_code, response.text)     

def update_employee_password(employee_id, new_value):
    url = employee_api + '/' + employee_id + '?' + header
    headers = {
    'headerKey': header,
    'Content-Type': 'application/json'
    }

    old_data = requests.get(url)
    user = old_data.json()
    data = {
        "id": user['id'],
        "name": user['name'],
        "log_status": user['log_status'],
        "password": new_value,
        "role": user['role'],
        "dates_logged": user['dates_logged']
    }
    response = requests.patch(url, headers=headers, json=data)

    # if response.status_code in [200, 204]:
    #     print('Resource updated successfully')
    # else:
    #     print(f'Failed to update resource. Status code: {response.status_code}')

def update_employee_role(employee_id, new_value):
    url = employee_api + '/' + employee_id + '?' + header
    headers = {
    'headerKey': header,
    'Content-Type': 'application/json'
    }

    old_data = requests.get(url)
    user = old_data.json()
    data = {
        "id": user['id'],
        "name": user['name'],
        "log_status": user['log_status'],
        "password": user['password'],
        "role": new_value,
        "dates_logged": user['dates_logged']
    }
    response = requests.patch(url, headers=headers, json=data)

    # if response.status_code in [200, 204]:
    #     print('Resource updated successfully')
    # else:
    #     print(f'Failed to update resource. Status code: {response.status_code}')
    # print(response.text)

def update_employee_log(employee_id, new_value):
    url = employee_api + '/' + employee_id + '?' + header
    headers = {
    'headerKey': header,
    'Content-Type': 'application/json'
    }

    old_data = requests.get(url)
    user = old_data.json()
    data = {
        "id": user['id'],
        "name": user['name'],
        "log_status": new_value,
        "password": user['password'],
        "role": user['role'],
        "dates_logged": user['dates_logged']
    }
    response = requests.patch(url, headers=headers, json=data)

    # if response.status_code in [200, 204]:
    #     print('Resource updated successfully')
    # else:
    #     print(f'Failed to update resource. Status code: {response.status_code}')

def update_employee_dates_logged(employee_id, new_value):
    url = employee_api + '/' + employee_id + '?' + header
    headers = {
    'headerKey': header,
    'Content-Type': 'application/json'
    }

    old_data = requests.get(url)
    user = old_data.json()
    data = {
        "id": user['id'],
        "name": user['name'],
        "log_status": user['log_status'],
        "password": user['password'],
        "role": user['role'],
        "dates_logged": new_value
    }
    response = requests.patch(url, headers=headers, json=data)

    # if response.status_code in [200, 204]:
    #     print('Resource updated successfully')
    # else:
    #     print(f'Failed to update resource. Status code: {response.status_code}')

def update_employee_hours(employee_id, new_value):
    url = employee_api + '/' + employee_id + '?' + header
    headers = {
    'headerKey': header,
    'Content-Type': 'application/json'
    }

    old_data = requests.get(url)
    user = old_data.json()
    data = {
        "id": user['id'],
        "name": user['name'],
        "log_status": user['log_status'],
        "password": user['password'],
        "role": user['role'],
        "dates_logged": user['dates_logged'],
        "hours_logged": new_value
    }
    response = requests.patch(url, headers=headers, json=data)

    # if response.status_code in [200, 204]:
    #     print('Resource updated successfully')
    # else:
    #     print(f'Failed to update resource. Status code: {response.status_code}')
# enter_new_admin("GAdmin", "Gregory Roper", "admin")
# enter_new_admin("HamwayAdmin", "Liam Hamway (Admin)", "hamway13")
# print(get_employees())
# update_employee_role("90089770", "admin")
# change_status("Roper", True)