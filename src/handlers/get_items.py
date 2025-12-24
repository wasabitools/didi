import json
import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("HouseCheckTable")


def lambda_handler(event, context):
    """Lambda handler"""
    print("lambda called")

    try:
        res = table.scan()
        items = res["Items"]

        while "LastEvaluatedKey" in res:
            res = table.scan(ExclusiveStartKey=res["LastEvaluatedKey"])
            items.extend(res["Items"])

        return {"statusCode": 200, "body": {json.dumps({"items": items})}}
    except ClientError as e:
        return {"statusCode": 500, "body": event, "exception": str(e)}
