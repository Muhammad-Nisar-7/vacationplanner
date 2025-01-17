import os
import pandas as pd
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Path to the Excel file
EXCEL_FILE_PATH = r"vacation data.xlsx"
def home(request):
    # Load the Excel file
    df = pd.read_excel(EXCEL_FILE_PATH)
    df = df.dropna(subset=['Name'])
    df = df.dropna(subset=['Start Date'])

    # Ensure date columns are properly parsed
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
    df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')

    # Convert the dates to ISO format (string) for JavaScript
    df['Start Date'] = df['Start Date'].dt.strftime('%Y-%m-%d')
    df['End Date'] = df['End Date'].dt.strftime('%Y-%m-%d')

    # Convert the data to a list of dictionaries with 'name', 'startDate', 'endDate'
    employees = df[['Name', 'Company', 'Start Date', 'End Date']].rename(columns={
        'Name': 'name',
        'Company': 'Company',
        'Start Date': 'startDate',
        'End Date': 'endDate'
    }).to_dict(orient="records")

    # Pass the data to the template
    return render(request, "index.html", {"tasks": employees})

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
