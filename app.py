import os
from werkzeug.utils import secure_filename
import boto3
from flask import Flask, render_template, request, redirect, session, jsonify
import datetime 
from boto3.dynamodb.conditions import Key
import json
import random
from flask_httpauth import HTTPBasicAuth
import hashlib


app = Flask(__name__)
auth = HTTPBasicAuth()
uploads_dir = os.path.join(app.instance_path, 'uploads')
# os.makedirs(uploads_dir, exist_ok=True)

@auth.verify_password
def verify_password(username, password):
    salt = b"\xa4v\x94\xf7'a\xb7\xca\xcc\x86\xfdq\xab\x0e!\x04v\x8a\x9e\xd5#\xbd\xff;\xfe\xb2g\x87W\xd5\xa7$"
    key = b'G{\x16+W2\xc1\xeeaB|-\x84\xbc\x91x\x16\xf5i\xd1 <5\x0c\xa0\xf8\x97\x93\xa6Yj\\'
    
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    print(new_key)
    print(key)
    if key == new_key:
        return True
    else:
        return False


@app.route('/resume1', methods=['POST'])
@auth.login_required
def resume():
    print('request.files', request.files)
    file = request.files['file']
    filepath = os.path.join(uploads_dir, secure_filename(file.filename))
    file.save(filepath)
    
    # Algorithm Start 
    app.secret_key = os.urandom(24)
    region_name = "us-east-1"
    aws_access_key_id = request.headers['aws_access_key_id']
    aws_secret_access_key = request.headers['aws_secret_access_key']
    aws_session_token = request.headers['aws_session_token']

    dynamo = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    y=[]

    with open(filepath, 'r') as datafile:
        records = json.load(datafile)
    for claimData in records:
        claimNumber = 'CLM' + str(random.randint(1111,9999))
        policyNumber = claimData['policyNumber']
        print(claimData)
        item = {
                'claimNumber': claimNumber,
                'policyNumber':claimData['policyNumber'],
                'dateOfLoss':claimData['dateOfLoss'],                
                'userName':claimData['userName'],
                'dateOfBirth':claimData['dateOfBirth'],
                'vehicleNumber':claimData['vehicleNumber'],
                'policeReport':claimData['policeReport'],
                'accAddress1':claimData['accAddress1'],
                'accCity':claimData['accCity'], 
                'accState':claimData['accState'], 
                'accZipCode':claimData['accZipCode'],
                'otherPartyInvolved':claimData['otherPartyInvolved'], 
                'opName':claimData['opName'],
                'opMake':claimData['opMake'],
                'opModel':claimData['opModel'],
                'opYear':claimData['opYear'],
                'opDamageDetails':claimData['opDamageDetails'],
                'opAddress':claimData['opAddress'],
                'opPhone':claimData['opPhone'],
                'opDriverLiscence':claimData['opDriverLiscence'],
                'vendorInvolved':claimData['vendorInvolved'],
                'vendorAmountSpent':claimData['vendorAmountSpent']
        }
        print(item)
        table = dynamo.Table('claimData')
        response = table.put_item( 
            Item=item
        )
        print("UPLOADING ITEM")
        print(response)
        print("policynumber")
        print(policyNumber)
    
        tablePolicyData = dynamo.Table('policyData')
        responsePolicyData = tablePolicyData.query(
            KeyConditionExpression = Key('policyNumber').eq(policyNumber)
        )
        policyData = responsePolicyData['Items'][0]
        print(policyData)
        userid = policyData["userId"]

        tableClaimData = dynamo.Table('claimData')
        responseClaimData = tableClaimData.query(
            KeyConditionExpression = Key('claimNumber').eq(claimNumber)
        )
        claimData = responseClaimData['Items'][0]
        print(claimData)

        tablePolicyCoverage = dynamo.Table('policyCoverage')
        responsePolicyCoverage = tablePolicyCoverage.query(
            KeyConditionExpression = Key('policyNumber').eq(policyNumber)
        )
        policyCoverage = responsePolicyCoverage['Items']
        print(policyCoverage)


        tableUserData = dynamo.Table('userData')
        responseUserData = tableUserData.query(
            KeyConditionExpression = Key('userId').eq(userid)
        )
        userData = responseUserData['Items'][0]
        print(userData)

        policyValid = False
        claimStatus = 'Open'
        amtPayableByInsured = 0
        amtPayableByCompany = 0
        UpdateTotalAmountSpentinDB = 0
        rating = 0
        policyPremium = 0

        #Check policy validity

        policyExpDate = policyData['expirationDate']
        currentDate = datetime.datetime.today().strftime('%Y-%m-%d')

        if (policyExpDate < currentDate):
            print("Policy invalid")  
        else:
            print("Policy valid")
            policyValid = True

            print(policyValid)

            if (policyValid):
                #Check collision coverage
                for cov in policyCoverage:
                    if(cov['covType']=="collision" or cov['covType']=="liability"):
                        if(cov['usedAmt']>=cov['annLimit']):
                            claimStatus = 'Closed'
                            #Send email
                            #return False
                        else:
                            #Calculate avail limit
                            availLimit = cov['annLimit'] - cov['usedAmt']
                            availDeductible = policyData['deductible'] - policyData['totalAmountSpent']
                            
                            vendorAmountSpent = claimData['vendorAmountSpent']
                            
                            
                            if (vendorAmountSpent > availDeductible):
                                amtPayableByInsured = availDeductible
                                amtPayableByCompany = vendorAmountSpent - availDeductible
                                UpdateTotalAmountSpentinDB = policyData['deductible']
                            elif ((vendorAmountSpent < availDeductible)):
                                amtPayableByInsured = vendorAmountSpent
                                amtPayableByCompany = 0
                                UpdateTotalAmountSpentinDB = policyData['totalAmountSpent'] + vendorAmountSpent

                #Calculate rating
                if (userData['drivingExp']>15):
                    if((userData['noOfAccidents'] == 0) and (userData['noOftickets'] == 0)):
                        policyPremium = 1200
                        rating = 5
                    elif ((userData['noOfAccidents'] == 1) and (userData['noOftickets'] == 0)):
                        policyPremium = 1400
                        rating = 4
                    elif ((userData['noOfAccidents'] == 0) and (userData['noOftickets'] == 1)):
                        policyPremium = 1400
                        rating = 4
                    elif ((userData['noOfAccidents']>1 and userData['noOfAccidents']<4) and (userData['noOftickets']>1 and userData['noOftickets']<4)):
                        policyPremium = 1400
                        rating = 3
                elif (userData['drivingExp']>=10 and userData['drivingExp']<=15):
                    if ((userData['noOfAccidents'] == 1) and (userData['noOftickets'] == 0)):
                        policyPremium = 1600
                        rating = 3
                    elif ((userData['noOfAccidents'] == 0) and (userData['noOftickets'] == 1)):
                        policyPremium = 1600
                        rating = 3
                    elif ((userData['noOfAccidents']>1 and userData['noOfAccidents']<4) and (userData['noOftickets']>1 and userData['noOftickets']<4)):
                        policyPremium = 1600
                        rating = 2
                elif (userData['drivingExp']<10):
                    if ((userData['noOfAccidents'] == 1) and (userData['noOftickets'] == 0)):
                        policyPremium = 1800
                        rating = 2
                    elif ((userData['noOfAccidents'] == 0) and (userData['noOftickets'] == 1)):
                        policyPremium = 1800
                        rating = 2
                    elif ((userData['noOfAccidents']>1 and userData['noOfAccidents']<4) and (userData['noOftickets']>1 and userData['noOftickets']<4)):
                        policyPremium = 2000
                        rating = 1
                elif (userData['drivingExp']<6):
                    if ((userData['noOfAccidents'] == 1 or userData['noOfAccidents'] == 0) and (userData['noOftickets'] == 0 or userData['noOftickets'] == 1)):
                        policyPremium = 2000
                        rating = 1


            #Send email

            print(amtPayableByInsured)
            print(amtPayableByCompany)
            print(UpdateTotalAmountSpentinDB)
            print(rating)
            print(policyPremium)

            tableUpdate = dynamo.Table('policyData')

            response = tableUpdate.update_item(
                Key={
                    'policyNumber': 'POL1000',
                    "expirationDate": '2022-01-01'
                },
                UpdateExpression="set #rating=:r, #annualPremium=:p, #totalAmountSpent=:t",
                ExpressionAttributeNames= {
                    '#rating' : 'rating',
                    '#annualPremium' : 'annualPremium',
                    '#totalAmountSpent' : 'totalAmountSpent'
                },
                ExpressionAttributeValues={
                    ':r': 5,
                    ':p': 1400,
                    ':t': UpdateTotalAmountSpentinDB
                },
                ReturnValues="UPDATED_NEW"
            )
            returnJson = {"amtPayableByInsured":str(amtPayableByInsured),"amtPayableByCompany":str(amtPayableByCompany),
                        "UpdateTotalAmountSpentinDB":str(UpdateTotalAmountSpentinDB),"rating":str(rating),
                        "policyPremium":str(policyPremium)}
        
            y.append(returnJson)

    return jsonify(response=y)


if __name__ == "__main__":
    app.run()