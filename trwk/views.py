# -*- encoding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from documents.models import Document
from seminars.models import Seminar
#from django.views.decorators.cache import cache_page


def trwk_home(request):
    notable_documents = Document.objects.filter(
        status=1, notable_rank__gt=0).order_by('-notable_rank')[0:3]
    notable_seminars = Seminar.objects.filter(
        status=1, notable_rank__gt=0).order_by('-notable_rank')[0:3]
    return render_to_response(
        'home.html',
        {
            'notable_documents': notable_documents,
            'notable_seminars': notable_seminars,
        },
        context_instance=RequestContext(request)
    )
