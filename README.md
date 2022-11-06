# Jobs API

A Rest API for registering the jobs that you've applied.

# Introduction
This is a simple CRUD serverless API that allows you to keep track of your job applications

# Technical Stack
- Python & FastAPI for development
- AWS DyndamoDB as database
- AWS Lambda and API Gateway for deployment
- GitHub Actions for the CI/CD


## API specification

|       Task       |     URL      | Method | Response code |     Response     |
|:----------------:|:------------:|:------:|:-------------:|:----------------:|
| request all jobs |    /jobs     |  GET   |      200      | List of all jobs |
|  Get single job  | /jobs/job_id |  GET   |      200      |       Job        |
|   Create a job   |    /jobs     |  POST  |      204      |    No content    |
|    Update job    | /jobs/job_id | PATCH  |      200      |   Updated job    |
|    Delete job    |    /jobs     | DELETE |      204      |    No content    |
