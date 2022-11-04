import uuid
from http import HTTPStatus

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel

app = FastAPI()
FIELDS = ['company', 'position_title', 'process_status', 'date_applied']

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table('jobs')


class Job(BaseModel):
    company: str
    position_title: str
    process_status: str
    date_applied: str


@app.get("/jobs")
async def root():
    response = table.scan()
    if response:
        return response['Items']
    return {}


@app.get("/jobs/{job_id}")
async def root(job_id: str):
    response = table.query(KeyConditionExpression=Key('id').eq(job_id))['Items']
    if len(response) != 0:
        return response
    return {"msg": f"job with id {job_id} does not exist"}


@app.post("/jobs", status_code=HTTPStatus.CREATED)
async def post(body: Job):
    response = table.put_item(Item={"id": str(uuid.uuid4()), "company": body.company.title(),
                                    "process_status": body.process_status, "Applied on date": body.date_applied,
                                    "position_title": body.position_title
                                    }
                              )
    return response


@app.delete("/jobs/{job_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete(job_id):
    return table.delete_item(
        Key={
            'id': job_id
        }
    )


@app.patch("/jobs/{job_id}", status_code=HTTPStatus.NO_CONTENT)
async def patch(body: Job, job_id: str):
    update_expression = "SET "
    expression_attribute_values = dict()

    for field in FIELDS:
        if body.__getattribute__(field):
            update_expression += f" {field} = :{field},"
            expression_attribute_values[f":{field}"] = body.__getattribute__(field)

    try:
        response = table.update_item(
            Key={'id': job_id},
            UpdateExpression=update_expression[:-1],
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW")
    except ClientError as err:
        return (
            f"Couldn't update job {job_id} in the table."
            f" Here's why: err.response['Error']['Code']: {err.response['Error']['Message']}",
        )
    else:
        return response['Attributes']


handler = Mangum(app=app)
