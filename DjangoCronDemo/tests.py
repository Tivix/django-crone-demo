import os
from datetime import datetime, timedelta
from pathlib import Path

from django.test import TestCase
from django.core.management import call_command
from django_cron.models import CronJobLog
from freezegun import freeze_time

from DjangoCronDemo.example_crons import WriteDateToFileMixin


class TestRunCrons(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestRunCrons, cls).setUpClass()
        cls.my_file_path = Path("test.txt")
        WriteDateToFileMixin.file_path = cls.my_file_path

    def setUp(self):
        self.test_date = datetime(2022, 10, 10, 12, 0, 0)
        os.remove(self.my_file_path) if os.path.exists(self.my_file_path) else None

    @classmethod
    def tearDownClass(cls):
        super(TestRunCrons, cls).tearDownClass()
        os.remove(cls.my_file_path) if os.path.exists(cls.my_file_path) else None

    def test_run_at_time(self):
        with freeze_time("2022-01-01 10:00:00"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunAtTimeCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 0)

        with freeze_time("2022-01-01 11:00:00"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunAtTimeCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 1)

        with freeze_time("2022-01-01 12:30:00"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunAtTimeCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 2)

        expected_output = (
            "Code: cron.RunAtTimeCronJob    Current date: 2022-01-01 11:00:00"
            "\nCode: cron.RunAtTimeCronJob    Current date: 2022-01-01 12:30:00\n"
        )

        with open(self.my_file_path, "r") as f:
            output = f.read()

        self.assertEqual(output, expected_output)

    def test_run_every_ten_minutes(self):
        for _ in range(0, 120):
            self.test_date = self.test_date + timedelta(minutes=1)
            with freeze_time(self.test_date):
                call_command(
                    "runcrons",
                    "DjangoCronDemo.example_crons.RunEveryTenMinutesCronJob",
                )

        self.assertEqual(CronJobLog.objects.all().count(), 11)

        test_date = self.test_date + timedelta(minutes=1, seconds=1)
        with freeze_time(test_date):
            call_command(
                "runcrons",
                "DjangoCronDemo.example_crons.RunEveryTenMinutesCronJob",
            )

        self.assertEqual(CronJobLog.objects.all().count(), 12)

        expected_output = (
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 12:01:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 12:12:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 12:23:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 12:34:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 12:45:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 12:56:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 13:07:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 13:18:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 13:29:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 13:40:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 13:51:00\n"
            "Code: cron.RunEveryTenMinutesCronJob    Current date: 2022-10-10 14:01:01\n"
        )

        with open(self.my_file_path, "r") as f:
            output = f.read()

        self.assertEqual(output, expected_output)

    def test_run_monthly(self):
        with freeze_time("2022-01-21 12:32:12"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunMonthlyCronJob")
        with freeze_time("2022-01-12 10:13:00"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunMonthlyCronJob")
        with freeze_time("2022-12-23 10:00:43"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunMonthlyCronJob")
        with freeze_time("2022-06-02 11:00:00"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunMonthlyCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 0)

        with freeze_time(self.test_date):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunMonthlyCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 1)

        self.test_date = self.test_date + timedelta(minutes=20)

        with freeze_time(self.test_date):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunMonthlyCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 2)

        with freeze_time("2023-01-01 10:00:00"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunMonthlyCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 3)

        expected_output = (
            "Code: cron.RunMonthlyCronJob    Current date: 2022-10-10 12:00:00\n"
            "Code: cron.RunMonthlyCronJob    Current date: 2022-10-10 12:20:00\n"
            "Code: cron.RunMonthlyCronJob    Current date: 2023-01-01 10:00:00\n"
        )

        with open(self.my_file_path, "r") as f:
            output = f.read()

        self.assertEqual(output, expected_output)

    def test_run_weekly(self):
        with freeze_time("2022-05-16 10:00:00"):  # Monday
            call_command("runcrons", "DjangoCronDemo.example_crons.RunWeeklyCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 0)

        with freeze_time("2022-05-16 12:00:00"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunWeeklyCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 1)

        with freeze_time("2022-05-16 12:29:00"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunWeeklyCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 1)

        with freeze_time("2022-05-16 12:30:00"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunWeeklyCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 2)

        with freeze_time("2022-05-17 10:00:00"):
            call_command("runcrons", "DjangoCronDemo.example_crons.RunWeeklyCronJob")
        self.assertEqual(CronJobLog.objects.all().count(), 2)

        expected_output = (
            "Code: cron.RunWeeklyCronJob    Current date: 2022-05-16 12:00:00\n"
            "Code: cron.RunWeeklyCronJob    Current date: 2022-05-16 12:30:00\n"
        )

        with open(self.my_file_path, "r") as f:
            output = f.read()

        self.assertEqual(output, expected_output)
