# receipt-manager
## Description
This is an easy receipt invoice generating tool that gets all receipts stored in an S3 bucket and generates a CSV based on receipts that have been uploaded.

## Requirements
- AWS CLI [AWS Command Line Interface](https://aws.amazon.com/cli/)
- Python 3 [Download Python | Python.org](https://www.python.org/downloads/)
- Pip 3 [Installation — pip 19.3.1 documentation](https://pip.pypa.io/en/stable/installing/)
- Boto3 (pip3 install boto3)
- datatime (pip3 install datetime)

## S3 File/Folder formatting
Inside of your buckets you must create a folder that is named `{month_start}{month}{year}-{month_end}{month+1}{year}` e.g. `21102019-21112019` `month_start` and `month_end` can be found on lines 10 and 11 of app.py. (these can be changed_

The uploaded images need to be named `{day}{month}{year}-{description}-{price}.{extension}` e.g. `21102019-coffee-230.jpg` is 21/10/2019 Coffee that cost £2.30

## How to use
- Install all the requirements above.
- Then you will need to change the `profile_name` on line 7 of app.py to whatever your profile you have set up (generally default).
- And you will need to change the bucket name on line 62 of app.py to the name of your S3 bucket.
- Once this is done you need to add a reference in your (~/.bash_profile) or (~/.zshrc) , by adding the line `source ~/repo/s3-expenses/command.sh` or where-ever you have downloaded the repo.
- Now restart your terminal
- The command `generate_report` can now be used.

## Uses
- `generate_report` will generate a full report of any expenses found in s3
- `generate_report 2019` will generate a report for all of 2019
- `generate_report october` will generate a report for October of this year
- `generate_report october 2018` will generate a report for October 2018
All reports are download into your downloads folder

## Next Up
Front End App created for mobile use to take, tag and upload pictures to the S3 bucket.