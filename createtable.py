import os
import boto3
from flask import Flask, render_template, request, redirect, session, jsonify
import datetime 
from boto3.dynamodb.conditions import Key


def createTables(aws_access_key_id,aws_secret_access_key,aws_session_token):
    region_name = "us-east-1"

    dynamodb = boto3.resource('dynamodb', region_name=region_name, aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)

    responsePolicyData = dynamodb.create_table(
      TableName="policyData",
      AttributeDefinitions=[
        {
          "AttributeName": "policyNumber",
          "AttributeType": "S"
        },
        {
          "AttributeName": "expirationDate",
          "AttributeType": "S"
        }
      ],
      KeySchema=[
        {
          "AttributeName": "policyNumber",
          "KeyType": "HASH"
        },
        {
          "AttributeName": "expirationDate",
          "KeyType": "RANGE"
        }
      ],
      ProvisionedThroughput={
        "ReadCapacityUnits": 1,
        "WriteCapacityUnits": 1
      }
    )

    print(responsePolicyData)


    responsePolicyCoverage = dynamodb.create_table(
      TableName="policyCoverage",
      AttributeDefinitions=[
        {
          "AttributeName": "policyNumber",
          "AttributeType": "S"
        },
        {
          "AttributeName": "covType",
          "AttributeType": "S"
        }
      ],
      KeySchema=[
        {
          "AttributeName": "policyNumber",
          "KeyType": "HASH"
        },
        {
          "AttributeName": "covType",
          "KeyType": "RANGE"
        }
      ],
      ProvisionedThroughput={
        "ReadCapacityUnits": 1,
        "WriteCapacityUnits": 1
      }
    )

    print(responsePolicyCoverage)





    responseUserData = dynamodb.create_table(
      TableName="userData",
      AttributeDefinitions=[
        {
          "AttributeName": "userId",
          "AttributeType": "S"
        },
        {
          "AttributeName": "name",
          "AttributeType": "S"
        }
      ],
      KeySchema=[
        {
          "AttributeName": "userId",
          "KeyType": "HASH"
        },
        {
          "AttributeName": "name",
          "KeyType": "RANGE"
        }
      ],
      ProvisionedThroughput={
        "ReadCapacityUnits": 1,
        "WriteCapacityUnits": 1
      }
    )

    print(responseUserData)




    # responseClaimData = dynamodb.create_table(
    #   TableName="claimData",
    #   AttributeDefinitions=[
    #     {
    #       "AttributeName": "claimNumber",
    #       "AttributeType": "S"
    #     },
    #     {
    #       "AttributeName": "policyNumber",
    #       "AttributeType": "S"
    #     }
    #   ],
    #   KeySchema=[
    #     {
    #       "AttributeName": "claimNumber",
    #       "KeyType": "HASH"
    #     },
    #     {
    #       "AttributeName": "policyNumber",
    #       "KeyType": "RANGE"
    #     }
    #   ],
    #   ProvisionedThroughput={
    #     "ReadCapacityUnits": 1,
    #     "WriteCapacityUnits": 1
    #   }
    # )

    # print(responseClaimData)

