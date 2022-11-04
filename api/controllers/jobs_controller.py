from api.schemas.schemas import Job
from api.services.jobs_service import JobsService


class JobsController:
    __job_service = JobsService()

    def get_all_jobs(self):
        return self.__job_service.get_all_jobs()

    def get_job_by_id(self, job_id: str):
        return self.__job_service.get_job_by_id(job_id=job_id)

    def delete_job(self, job_id: str):
        return self.__job_service.delete_job(job_id=job_id)

    def update_job(self, job_id: str, body: Job):
        return self.__job_service.update_job(job_id=job_id, body=body)

    def post(self, body: Job):
        return self.__job_service.post_job(body)
