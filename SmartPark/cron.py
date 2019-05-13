from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 1 minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'SmartPark.my_cron_job'    # a unique code

    def do(self):
        print("test cron yay")    # do your thing here