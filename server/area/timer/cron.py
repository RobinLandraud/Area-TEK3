from django.utils import timezone
from .models import Timer
from services.models import Service
from services.functions import callReaction

def update_timers():
    print(f"[{str(timezone.now())}]")
    print("[TIMER CRON]: Updating timers")
    for timer in Timer.objects.all():
        service = Service.objects.get(id=timer.service.id)
        time_lift = int((timer.date_time - timezone.now()).total_seconds() / 60)
        if time_lift < 0:
            time_lift = 0
        service.action_data["time"] = str(time_lift)
        service.save()
        if timer.date_time <= timezone.now() and timer.is_passed == False:
            print(f"[TIMER CRON]: Timer {timer.id} is expired")
            timer.is_passed = True
            timer.save()
            callReaction("ATI0", service.owner)
        else:
            print(f"[TIMER CRON]: Timer {timer.id} is not expired")
    print("[TIMER CRON]: Done updating timers")