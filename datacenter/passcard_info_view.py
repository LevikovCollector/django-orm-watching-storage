from datacenter.models import Passcard, get_duration, is_visit_long
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    # Программируем здесь

    this_passcard_visits = [

    ]
    for visit in Visit.objects.filter(id=passcard.id):
        this_passcard_visits.append(
            {
                'entered_at': visit.entered_at,
                'duration': get_duration(visit),
                'is_strange': is_visit_long(visit)
            }
        )
    print(Visit.objects.filter(id=passcard.id))
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
