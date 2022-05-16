import datetime

from django_cron import CronJobBase, Schedule


class WriteDateToFileMixin:
    """
    Write current date to file.
    """

    file_path = "cron-demo.txt"

    def do(self):
        message = f"Code: {self.code}    Current date: {datetime.datetime.now()}\n"
        with open(self.file_path, "a") as myfile:
            myfile.write(message)


class RunAtTimeCronJob(CronJobBase, WriteDateToFileMixin):
    """
    Run job every day at 11:00 and 12:30
    """

    RUN_AT_TIMES = ["11:00", "12:30"]
    schedule = Schedule(run_at_times=RUN_AT_TIMES, retry_after_failure_mins=1)
    code = "cron.RunAtTimeCronJob"


class RunEveryTenMinutesCronJob(CronJobBase, WriteDateToFileMixin):
    """
    Run the job every 10 minutes
    """

    RUN_EVERY_MINS = 10
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "cron.RunEveryTenMinutesCronJob"


class RunMonthlyCronJob(CronJobBase, WriteDateToFileMixin):
    """
    Run the job every 15 minutes at the 1st and 10th day of month.
    """

    RUN_MONTHLY_ON_DAYS = [1, 10]
    RUN_EVERY_MINS = 15
    schedule = Schedule(
        run_monthly_on_days=RUN_MONTHLY_ON_DAYS, run_every_mins=RUN_EVERY_MINS
    )
    code = "cron.RunMonthlyCronJob"


class RunWeeklyCronJob(CronJobBase, WriteDateToFileMixin):
    """
    Run the job every 10 minutes on Mondays.
    """

    RUN_WEEKLY_ON_DAYS = [0]
    RUN_AT_TIMES = ["12:00", "12:30"]
    schedule = Schedule(run_on_days=RUN_WEEKLY_ON_DAYS, run_at_times=RUN_AT_TIMES)
    code = "cron.RunWeeklyCronJob"
