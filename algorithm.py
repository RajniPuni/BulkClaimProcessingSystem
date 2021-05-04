import os, boto3, datetime, json, random, hashlib
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session, jsonify
from boto3.dynamodb.conditions import Key
from flask_httpauth import HTTPBasicAuth

 
def processAlgorithm(aws_access_key_id, aws_secret_access_key, aws_session_token):
    # Algorithm Start 
    
    region_name = "us-east-1"

    dynamo = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    sns_client = boto3.client('sns', region_name=region_name, aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    sqs = boto3.client('sqs', region_name=region_name, aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
    queue_url = 'https://sqs.us-east-1.amazonaws.com/682768179417/cloudproject'

    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    print(response)
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Received and deleted message: %s' % message)
    print('*** claim number %s' % message["MessageAttributes"]["claimNumber"])
    claimsList = message["MessageAttributes"]["claimNumber"]["StringValue"].split(",")
    #print(claimsList)

    responseJson=[]

    for claim in claimsList:

        policyValid = False
        claimStatus = 'Open'
        amtPayableByInsured = 0
        amtPayableByCompany = 0
        UpdateTotalAmountSpentinDB = 0
        rating = 0
        policyPremium = 0

        claimNumber = claim        
        
        tableClaimData = dynamo.Table('claimData')
        responseClaimData = tableClaimData.query(
            KeyConditionExpression = Key('claimNumber').eq(claimNumber)
        )
        claimData = responseClaimData['Items'][0]
        policyNumber = claimData['policyNumber']
        
        tablePolicyData = dynamo.Table('policyData')
        responsePolicyData = tablePolicyData.query(
            KeyConditionExpression = Key('policyNumber').eq(policyNumber)
        )
        policyData = responsePolicyData['Items'][0]
        userid = policyData["userId"]
        
        tablePolicyCoverage = dynamo.Table('policyCoverage')
        responsePolicyCoverage = tablePolicyCoverage.query(
            KeyConditionExpression = Key('policyNumber').eq(policyNumber)
        )
        policyCoverage = responsePolicyCoverage['Items']
        

        tableUserData = dynamo.Table('userData')
        responseUserData = tableUserData.query(
            KeyConditionExpression = Key('userId').eq(userid)
        )
        userData = responseUserData['Items'][0]
        userTopicArn = userData["topicArn"]
        
        
        #Check policy validity

        policyExpDate = policyData['expirationDate']
        currentDate = datetime.datetime.today().strftime('%Y-%m-%d')

        if (policyExpDate < currentDate):
            print("Policy invalid" + claimNumber)  
            policyInvalidJson = {"Claim Number":claimNumber,"Policy Number":policyNumber,"Error":"Policy is expired"}        
            responseJson.append(policyInvalidJson)
            sns_client.publish(
                TopicArn = userTopicArn,
                Subject = 'Claim ' + claimNumber + ' is not processed.',
                Message = 'Hi, '+ userData["name"] +'\n\n\n' +
                            'Your claim is not processed successfully. \n' +
                            'You policy number is invalid.\n\n' +
                            'Thanks, \n' +
                            'Insurance Company'
            )
        else:
            print("Policy valid" + claimNumber)
            policyValid = True

            if (policyValid):
                #Check collision coverage
                for cov in policyCoverage:
                    if(cov['covType']=="collision" or cov['covType']=="liability"):
                        if(cov['usedAmt']>=cov['annLimit']):
                            print("Policy invalid coverage" + claimNumber)
                            claimStatus = 'Closed'
                            policyInvalidJson = {"Claim Number":claimNumber,"Policy Number":policyNumber,"Error":"Policy annual limit is reached"}        
                            responseJson.append(policyInvalidJson)
                            
                            sns_client.publish(
                                TopicArn = userTopicArn,
                                Subject = 'Claim ' + claimNumber + ' is not processed.',
                                Message = 'Hi, '+ userData["name"] +'\n\n\n' +
                                            'Your claim is not processed successfully. \n' +
                                            'You annual limit is exceeded.\n\n' +
                                            'Thanks, \n' +
                                            'Insurance Company'
                            )
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
                sns_client.publish(
                    TopicArn = userTopicArn,
                    Subject = 'Claim ' + claimNumber + ' processed successfully.',
                    Message = 'Hi, '+ userData["name"] +'\n\n\n' +
                                'Your claim is processed successfully. \n' +
                                'Following are the details: \n' +
                                'Amount you need to pay: $' +  str(amtPayableByInsured) + '\n' +
                                'Amount out Insurance company will pay: $' +  str(amtPayableByCompany) + '\n' +
                                'Rating: ' +  str(UpdateTotalAmountSpentinDB) + '\n' +
                                'New policy premium (applicable from next year): $' +  str(policyPremium) + '\n\n' +
                                'Thanks, \n' +
                                'Insurance Company'
                )

                tableUpdate = dynamo.Table('policyData')

                response = tableUpdate.update_item(
                    Key={
                        'policyNumber': policyNumber,
                        "expirationDate": policyData['expirationDate']
                    },
                    UpdateExpression="set #rating=:r, #annualPremium=:p, #totalAmountSpent=:t",
                    ExpressionAttributeNames= {
                        '#rating' : 'rating',
                        '#annualPremium' : 'annualPremium',
                        '#totalAmountSpent' : 'totalAmountSpent'
                    },
                    ExpressionAttributeValues={
                        ':r': rating,
                        ':p': policyPremium,
                        ':t': UpdateTotalAmountSpentinDB
                    },
                    ReturnValues="UPDATED_NEW"
                )
                returnJson = {"Claim Number":claimNumber,"Policy Number":policyNumber,"amtPayableByInsured":str(amtPayableByInsured),"amtPayableByCompany":str(amtPayableByCompany),
                            "UpdateTotalAmountSpentinDB":str(UpdateTotalAmountSpentinDB),"rating":str(rating),
                            "policyPremium":str(policyPremium)}
            
                responseJson.append(returnJson)

    return jsonify(response=responseJson)

