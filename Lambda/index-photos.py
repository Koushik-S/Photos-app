import boto3
import json
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection

def lambda_handler(event, context):
    # Get the S3 bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Get the customLabels metadata from the S3 object
    s3 = boto3.client('s3')
    metadata = s3.head_object(Bucket=bucket, Key=key)['Metadata']
    custom_labels = metadata.get('x-amz-meta-customLabels')
    if custom_labels:
        labels = json.loads(custom_labels)
    else:
        labels = []
    
    # Detect labels in the image using Rekognition
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        }
    )
    rek_labels = [label['Name'] for label in response['Labels']]
    
    # Combine custom labels and Rekognition labels
    labels += rek_labels
    
    # Create JSON object to store in OpenSearch index
    doc = {
        'objectKey': key,
        'bucket': bucket,
        'labels': labels
    }
    
    service = 'es'
    host = 'search-restaurant-g56zesqy2cp7vled5m5ivgpep4.us-east-1.es.amazonaws.com'
    region = 'us-east-1'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    es = OpenSearch(
        hosts=[{'host': 'search-photos-lbffn7ibyl5cnd5eqf3b7zeqvy.us-east-1.es.amazonaws.com', 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    res = es.index(index='photos', body=doc)
    print(doc)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Document indexed successfully')
    }