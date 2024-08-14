import json
import datetime
import boto3
from botocore.exceptions import ClientError


#This Lambda grabs Zip file from S3 bucket and deploy as lambda

lambdaclient = boto3.client('lambda')
runtime='python3.6'
role='arn:aws:iam::719217631821:role/lambda_basic_execution'
handler='lambda_function.lambda_handler'
timeout=30
memorysize=256

def lambda_handler(event, context):
    # TODO implement
    print(event)

    for item in event['Records']:
        s3bucket=item['s3']['bucket']['name']
        objectkey=item['s3']['object']['key']
        print(s3bucket)
        print(objectkey)
    
    functionName=objectkey.rpartition('.')[0]
    print(functionName)
    #deployFlag, set C for create, U for Update existing, X for Error
    deployFlag=""
    #check if function exists, if yes update, else create
    try:
        response=lambdaclient.get_function(FunctionName=functionName)
        if response['ResponseMetadata']['HTTPStatusCode']==200:
            print("Function Exists")
            deployFlag="U"
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("Function does not exist")
            deployFlag="C"
        else:
            print("Unexpected error: %s" % e)
            deployFlag="X"
        
    if deployFlag=="C":
        createLambda(functionName, s3bucket, objectkey)
    elif deployFlag=="U":
        updateLambda(functionName, s3bucket, objectkey)
    else:
        print("Error, check pipeline")
    
    return 'End of Lambda Deployer'    

    
def createLambda(functionName, s3bucket, objectkey):
    response=lambdaclient.create_function(
            FunctionName=functionName,
            Runtime=runtime,
            Role=role,
            Handler=handler,
            Code={
            'S3Bucket': s3bucket,
            'S3Key': objectkey
                }
            ,Timeout=timeout
            ,MemorySize=memorysize
                )
    print("in create lambda para***********")
    print(response)

def updateLambda(functionName, s3bucket, objectkey):
    response=lambdaclient.update_function_code(
            FunctionName=functionName,
            S3Bucket=s3bucket,
            S3Key=objectkey
                )
    print("in update lambda para***********")
    print(response) 
 