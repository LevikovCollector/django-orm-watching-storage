from datetime import timedelta

from django.db import models
import django


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit: Visit) -> timedelta:
    """
    Function checks the person's time in the vault
    :param visit: object with information about visits
    :return: how much time user was in vault
    """

    leaved_at_local = django.utils.timezone.localtime(visit.leaved_at)
    if visit.entered_at is None:
        return timedelta(minutes=0)
    else:
        entered_at_local = django.utils.timezone.localtime(visit.entered_at)
        delta = leaved_at_local - entered_at_local
        duration = timedelta(days=delta.days, seconds=delta.seconds)
        return duration


def is_visit_long(visit: Visit, minutes: int = 60) -> bool:
    """
    Function check visit  for strange.

    :param visit: object with information about visits
    :param minutes: it`s number of how much minutes is ok for visit
    :return: if visit more then minutes, it`s strange visit
    """

    duration = get_duration(visit)
    return duration > timedelta(minutes=minutes)
