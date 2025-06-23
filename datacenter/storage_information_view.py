from datacenter.models import Visit
from django.shortcuts import render

from datacenter.visit_duration import get_duration, is_visit_long, duration_format


def storage_information_view(request):
    # Программируем здесь

    non_closed_visits = []
    for visit in Visit.objects.filter(leaved_at=None):
        non_closed_visits.append(
            {
                'who_entered': visit.passcard.owner_name,
                'entered_at': visit.entered_at,
                'duration': duration_format(get_duration(visit)),
                'is_strange': is_visit_long(visit)
            }
        )

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
