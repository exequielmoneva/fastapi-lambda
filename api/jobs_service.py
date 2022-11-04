import boto3
import uuid
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

from api.schemas import Job

FIELDS = ['company', 'position_title', 'process_status', 'date_applied']


class JobsService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
        self.table = self.dynamodb.Table('jobs')

    def get_all_jobs(self):
        response = self.table.scan()
        if response:
            return response['Items']
        return {}

    def get_job_by_id(self, job_id: str):
        response = self.table.query(KeyConditionExpression=Key('id').eq(job_id))['Items']
        if len(response) != 0:
            return response
        return {"msg": f"job with id {job_id} does not exist"}

    def delete_job(self, job_id: str):
        return self.table.delete_item(
            Key={
                'id': job_id
            }
        )

    def update_job(self, job_id: str, body: Job):
        update_expression = "SET "
        expression_atribute_values = dict()

        for field in FIELDS:
            if body.__getattribute__(field):
                update_expression += f" {field} = :{field},"
                expression_atribute_values[f":{field}"] = body.__getattribute__(field)

        try:
            response = self.table.update_item(
                Key={'id': job_id},
                UpdateExpression=update_expression[:-1],
                ExpressionAttributeValues=expression_atribute_values,
                ReturnValues="UPDATED_NEW")
        except ClientError as err:
            return (
                f"Couldn't update job {job_id} in the table."
                f" Here's why: err.response['Error']['Code']: {err.response['Error']['Message']}",
            )
        else:
            return response['Attributes']

    def post_job(self, body):
        response = self.table.put_item(Item={"id": str(uuid.uuid4()), "company": body.company.title(),
                                             "process_status": body.process_status, "Applied on date": body.date_applied,
                                             "position_title": body.position_title
                                             }
                                       )
        return response
