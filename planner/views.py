import os
import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

user = 'MYK'
pswrd = 'MYK@binghalib'

def login_view(request):
    return render(request, 'login.html')

# Path to the Excel file
EXCEL_FILE_PATH = r"vacation data.xlsx"
def home(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == user and password == pswrd:
        
        # Load the Excel file
        df = pd.read_excel(EXCEL_FILE_PATH)
        df = df.dropna(subset=['Name'])
        df = df.dropna(subset=['Start Date'])
        df = df.dropna(subset=['D.O.J'])

        # Ensure date columns are properly parsed
        df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
        df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
        df['D.O.J'] = pd.to_datetime(df['D.O.J'], errors='coerce')

        # Convert the dates to ISO format (string) for JavaScript
        df['Start Date'] = df['Start Date'].dt.strftime('%Y-%m-%d')
        df['End Date'] = df['End Date'].dt.strftime('%Y-%m-%d')
        df['D.O.J'] = df['D.O.J'].dt.strftime('%Y-%m-%d')

        # Convert the data to a list of dictionaries with 'name', 'startDate', 'endDate'
        employees = df[['Name', 'Company','D.O.J', 'Start Date', 'End Date']].rename(columns={
            'Name': 'name',
            'Company': 'Company',
            'D.O.J':'DOJ',
            'Start Date': 'startDate',
            'End Date': 'endDate'
        }).to_dict(orient="records")

        # Pass the data to the template
        return render(request, "index.html", {"tasks": employees})
    else:
        return render(request, "login.html", {})

@csrf_exempt
def save_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        status_data = data.get('data', [])

        # Load the Excel file
        df = pd.read_excel(EXCEL_FILE_PATH)

        # Update the status data in the DataFrame
        for status in status_data:
            employee = status.get('name')
            status_value = status.get('status')

            # Find the employee row and update status
            df.loc[df['Name'] == employee, 'Status'] = status_value

        # Save the updated Excel file
        df.to_excel(EXCEL_FILE_PATH, index=False)

        return JsonResponse({'message': 'Status data saved successfully'})

    return JsonResponse({'message': 'Invalid request'}, status=400)
