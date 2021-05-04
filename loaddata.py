import os
import boto3
import json
from flask import Flask, render_template, request, redirect, session, jsonify


def loaddata(aws_access_key_id,aws_secret_access_key,aws_session_token):
    region_name = "us-east-1"
    dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    print(dynamodb.__dict__)


    with open('policyData.json', 'r') as datafile:
        policyrecords = json.load(datafile)
    for policy in policyrecords:
        print(policy)
        item = {
                'policyNumber':policy['policyNumber'],
                'userId':policy['userId'],
                'expirationDate':policy['expirationDate'],
                'deductible':policy['deductible'],
                'totalAmountSpent':policy['totalAmountSpent'],
                'rating':policy['rating'],
                'annualPremium':policy['annualPremium']
        }
        print(item)
        table = dynamodb.Table('policyData')
        print(table)
        response = table.put_item( 
            Item=item
        )
        print("UPLOADING ITEM p ")
        print(response)


    with open('policyCoverage.json', 'r') as datafile:
        polcovrecords = json.load(datafile)
    for policyCoverage in polcovrecords:
        print(policyCoverage)
        item = {
                'policyNumber':policyCoverage['policyNumber'],
                'covType':policyCoverage['covType'],
                'annLimit':policyCoverage['annLimit'],
                'usedAmt':policyCoverage['usedAmt']
        }
        print(item)
        table = dynamodb.Table('policyCoverage')
        response = table.put_item( 
            Item=item
        )
        print("UPLOADING ITEM pc")
        print(response)



    with open('userData.json', 'r') as datafile:
        userdatarecords = json.load(datafile)
    for userData in userdatarecords:
        print(userData)
        item = {
                'userId':userData['userId'],
                'name':userData['name'],
                'address1':userData['address1'],
                'city':userData['city'],
                'state':userData['state'],
                'zip':userData['zip'],
                'drivingExp':userData['drivingExp'],
                'noOfAccidents':userData['noOfAccidents'],
                'noOftickets':userData['noOftickets'],
                'topicArn':userData['topicArn']
        }
        print(item)
        table = dynamodb.Table('userData')
        response = table.put_item( 
            Item=item
        )
        print("UPLOADING ITEM u")
        print(response)

    return True

