from prefect.client.schemas.schedules import CronSchedule
from prefect.deployments import Deployment

from src.config import settings
from src.flows.storage.memes import ocr_uploaded_memes

deployment_ocr_uploaded_memes = Deployment.build_from_flow(
    flow=ocr_uploaded_memes,
    name="OCR Uploaded Memes",
    schedules=[CronSchedule(cron="*/5 * * * *", timezone="Europe/London")],
    work_pool_name=settings.ENVIRONMENT,
)

deployment_ocr_uploaded_memes.apply()
