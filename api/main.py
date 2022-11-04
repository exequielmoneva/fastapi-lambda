from http import HTTPStatus

from fastapi import FastAPI
from mangum import Mangum

from api.jobs_controller import JobsController
from api.schemas import Job

app = FastAPI()


@app.get("/jobs")
async def root():
    return JobsController().get_all_jobs()


@app.get("/jobs/{job_id}")
async def root(job_id: str):
    return JobsController().get_job_by_id(job_id=job_id)


@app.post("/jobs", status_code=HTTPStatus.CREATED)
async def post(body: Job):
    return JobsController().post(body=body)


@app.delete("/jobs/{job_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete(job_id):
    return JobsController().delete_job(job_id=job_id)


@app.patch("/jobs/{job_id}", status_code=HTTPStatus.NO_CONTENT)
async def patch(body: Job, job_id: str):
    return JobsController().update_job(job_id=job_id, body=body)


handler = Mangum(app=app)
