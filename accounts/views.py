# -*- encoding: utf-8 -*-
"""
Views which edit user accounts

"""
from django import forms
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.models import RequestSite, Site
from registration.forms import ChangeEmailForm
from registration.backends import get_backend
from registration.models import RegistrationProfile, ChangeEmailProfile
from accounts.forms import MyUserProfileEditForm, CompanyEditform
from accounts.models import MyUserProfile, Company
from trwk.libs.request_utils import set_next_url

@login_required
def mypage_home(request):
    return render_to_response(
        'accounts/mypage.html',
        {},
        context_instance=RequestContext(request)
    )

@login_required
@csrf_protect
def mypage_edit_profile(request):
    user_pk = request.user.pk
    current_profile = MyUserProfile.objects.get(myuser=user_pk)
    if request.method == 'POST':
        form = MyUserProfileEditForm(request.POST, instance=current_profile)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'ユーザー情報の変更に成功しました')
            #return redirect('mypage_home')
    else:
        form = MyUserProfileEditForm(instance=current_profile)
    set_next_url(request)
    return render_to_response(
        'accounts/edit_profile.html',
        {
            'form' : form,
        },
        context_instance=RequestContext(request)
    )
@login_required
@csrf_protect
def mypage_edit_company(request):
    company = request.user.customer_company
    if not company:
        messages.add_message(request, messages.ERROR, '掲載企業が登録されていません')
        return redirect('mypage_home')
    current_company = Company.objects.get(pk=company.pk)
    if request.method == 'POST':
        form = CompanyEditform(request.POST, request.FILES, instance=current_company)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '掲載企業情報を保存しました')
            return redirect('mypage_home')
    else:
        form = CompanyEditform(instance=current_company)

    return render_to_response(
        'accounts/edit_company.html',
        {
            'form' : form,
        },
        context_instance=RequestContext(request)
    )

