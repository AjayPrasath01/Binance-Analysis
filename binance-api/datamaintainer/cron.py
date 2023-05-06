from django_cron import CronJobBase, Schedule
from datamaintainer.tasks import data_updater

class DataUpdaterCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'datamainteiner.cron'  # Unique identifier for the cron job

    def do(self):
        data_updater()