# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from accounts.models import MyUser, MyUserProfile, Company
from sorl.thumbnail.admin import AdminImageMixin


class MyUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(
        label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and "
            "@/./+/-/_ only."),
        error_messages={
            'invalid': _(
                "This value may contain only letters, numbers and "
                "@/./+/-/_ characters.")})
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_(
        "Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = MyUser
        fields = ('email', 'username')

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            MyUser._default_manager.get(username=username)
        except MyUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = MyUser

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('myuser',)

admin.site.register(MyUserProfile, MyUserProfileAdmin)


class MyUserProfileInline(admin.StackedInline):
    model = MyUserProfile


class MyUserAdmin(UserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    inlines = [MyUserProfileInline]
    fieldsets = (
        ('アカウント', {
            'fields': (
                'email',
                'username',
                'password',
                'is_active',
                'is_admin',
                'is_staff',
                'is_superuser',
                'customer_company',
                'groups',
                'last_login',
                'date_joined',
            )
        }),
    )
    add_fieldsets = (
        ('アカウント', {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'username',
                'customer_company',
            )
        }),
    )

    list_display = (
        'email',
        'date_joined',
        'customer_company',
        'is_active',
        'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('-id', )
    readonly_fields = ('last_login', 'date_joined')
    form = MyUserChangeForm
    add_form = MyUserCreationForm

admin.site.register(MyUser, MyUserAdmin)


class CompanyAdmin(admin.ModelAdmin, AdminImageMixin):
    pass
admin.site.register(Company, CompanyAdmin)
