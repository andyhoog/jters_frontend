# -*- encoding: utf-8 -*-
# Create your views here.
from search.models import Search
from search.forms import SearchForm
from django.shortcuts import render_to_response
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import RequestContext
from django.conf import settings
from search.libs import create_search_query, get_search_target_models


def search(request, page=1):
    paged_results = []
    count = 0
    if 'page' in request.GET:
        page = request.GET['page']

    if 'keyword' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = create_search_query(form.cleaned_data['keyword'])
            search_results = Search.objects.filter(
                text__search=query, status=1
            ).order_by('update_date').all()
            if search_results:
                paginator = Paginator(search_results, settings.ITEMS_PER_PAGE)
                try:
                    paged_results = paginator.page(page)
                    count = paginator.count
                except PageNotAnInteger:
                    raise Http404
                except EmptyPage:
                    raise Http404
                else:
                    results = []
                    target_models = get_search_target_models()
                    for target in target_models:
                        model_name = target().__class__.__name__
                        target_results = target.objects.filter(
                            pk__in=[
                                item.model_pk
                                for item in paged_results
                                if item.model == model_name
                            ]
                        )
                        for item in target_results:
                            results.append(item)
                    results.sort(key=lambda x: x.update_date, reverse=True)
                    paged_results.object_list = results
    else:
        form = SearchForm()
    return render_to_response(
        'search/index.html',
        {
            'form': form,
            'count': count,
            'results': paged_results,
        },
        context_instance=RequestContext(request)
    )
