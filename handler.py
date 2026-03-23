import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MyItemsTable')

def main(event, context):
    # Common CORS headers
    cors_headers = {
        "Access-Control-Allow-Origin": "http://my-serverless-dynamodb.s3-website.ap-south-1.amazonaws.com",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
    }

    # Handle preflight OPTIONS request
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": ""
        }

    # Handle POST request (create user)
    if event.get("httpMethod") == "POST":
        try:
            body = json.loads(event.get("body") or "{}")
            user_id = str(uuid.uuid4())

            table.put_item(
                Item={
                    "id": user_id,
                    "name": body.get("name"),
                    "email": body.get("email")
                }
            )

            return {
                "statusCode": 200,
                "headers": cors_headers,
                "body": json.dumps({"message": "User saved successfully!", "userId": user_id})
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": cors_headers,
                "body": json.dumps({"error": str(e)})
            }

    # Handle GET request (list users)
    if event.get("httpMethod") == "GET":
        try:
            response = table.scan()
            items = response.get("Items", [])

            return {
                "statusCode": 200,
                "headers": cors_headers,
                "body": json.dumps({"items": items})
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": cors_headers,
                "body": json.dumps({"error": str(e)})
            }

    # Default response for unsupported methods
    return {
        "statusCode": 400,
        "headers": cors_headers,
        "body": json.dumps({"message": "Unsupported method"})
    }