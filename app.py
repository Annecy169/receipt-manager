import boto3
import os
import json
import sys
from datetime import datetime

session = boto3.Session(profile_name='default')
s3 = boto3.client('s3')

month_start = 21
month_end = 20

def month_string_to_number(string):
    s = string.strip()[:3]
    months = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
        'may':5,
        'jun':6,
        'jul':7,
        'aug':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dec':12
    }

    try:
        out = months[s]
        return out
    except:
        raise ValueError('Not a month')

try:
    try:
        if int(sys.argv[1]) > 1:
            month = "none"
    except:
        month = month_string_to_number(sys.argv[1].lower())
except:
    month = "none"

try:
    try:
        if int(sys.argv[2]) > 1:
            if (int(sys.argv[2]) - 2000) > 0:
                year = int(sys.argv[2])
            else:
                year = "none"
    except:
        if int(sys.argv[1]) > 1:
            if (int(sys.argv[1]) - 2000) > 0:
                year = int(sys.argv[1])
            else:
                year = "none"
except:
    year = "none"

response = s3.list_objects(
    Bucket="my_receipt_bucket"
)

if (month != "none") and (year != "none"):
    spending_report = open("monthly_report_%s_%s.csv" % (month, year),"w")
elif (month == "none") and (year != "none"):
    spending_report = open("annual_report_%s.csv" % (year),"w")
elif (month != "none") and (year == "none"):
    current_year = datetime.today().year
    spending_report = open("monthly_report_%s_%s.csv" % (month, current_year),"w")
else:
    spending_report = open("spending_report.csv","w") 

csv = '''Date,Price,Description
'''

def set_csv(csv_data, object_value):
    file = (object_value["Key"].split("/")[1]).split(".")[0]
    extension = (object_value["Key"].split("/")[1]).split(".")[1]
    date = "%s/%s/%s" %((file.split("-")[0])[:-6], ((file.split("-")[0])[:-4])[-2:], (file.split("-")[0])[-4:])
    description = file.split("-")[1]
    price = "%s.%s" %((file.split("-")[2])[:-2], (file.split("-")[2])[-2:])
    item = '''%s,%s,%s
''' % (date, price, description)
    csv_data = csv_data + item
    return csv_data

if (month != "none") and (year != "none"):
    for object in response["Contents"]:
        folder = '%s%s%s-%s%s%s' % (month_start, month, year, month_end, month + 1, year)
        if ((object["Key"].split("/")[0] == folder) and (object["Key"].split("/")[1])):
            csv = set_csv(csv, object)
elif (month == "none") and (year != "none"):
    for object in response["Contents"]:
        for x in range(0, 12):
            m = x + 1
            folder = '%s%s%s-%s%s%s' % (month_start, m, year, month_end, m + 1, year)
            if ((object["Key"].split("/")[0] == folder) and (object["Key"].split("/")[1])):
                csv = set_csv(csv, object)
elif (month != "none") and (year == "none"):
    for object in response["Contents"]:
        current_year = datetime.today().year
        folder = '%s%s%s-%s%s%s' % (month_start, month, current_year, month_end, month + 1, current_year)
        if ((object["Key"].split("/")[0] == folder) and (object["Key"].split("/")[1])):
            csv = set_csv(csv, object)
else:
    for object in response["Contents"]:
        if object["Key"].split("/")[1]:
            csv = set_csv(csv, object)

spending_report.writelines(csv) 
spending_report.close()
