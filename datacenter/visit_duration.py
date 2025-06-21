import django
from datetime import timedelta
from datacenter.models import Visit


def get_duration(visit: Visit) -> timedelta:
    """
    Function checks the person's time in the vault
    :param visit: object with information about visits
    :return: how much time user was in vault
    """

    leaved_at_local = django.utils.timezone.localtime(visit.leaved_at)
    if visit.entered_at and visit.leaved_at:
        entered_at_local = django.utils.timezone.localtime(visit.entered_at)
        delta = leaved_at_local - entered_at_local
        duration = timedelta(days=delta.days, seconds=delta.seconds)
        return duration
    else:
        return timedelta(minutes=0)


def is_visit_long(visit: Visit, minutes: int = 60) -> bool:
    """
    Function check visit  for strange.

    :param visit: object with information about visits
    :param minutes: it`s number of how much minutes is ok for visit
    :return: if visit more then minutes, it`s strange visit
    """

    duration = get_duration(visit)
    return duration > timedelta(minutes=minutes)