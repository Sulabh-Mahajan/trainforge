from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.html import mark_safe
from django import forms

from .models import Subscription, Trainer, TrainerSpecialization, Client



class TrainerSpecializationInline(admin.TabularInline):
    model               = TrainerSpecialization
    extra               = 1
    verbose_name_plural = 'Specializations'


class ClientInline(admin.TabularInline):
    model            = Client
    extra            = 0
    show_change_link = True
    can_delete       = False
    readonly_fields  = ('first_name', 'last_name', 'email', 'phone', 'sex', 'age')
    fields           = ('first_name', 'last_name', 'email', 'phone', 'sex', 'age')


class TrainerCreationForm(forms.ModelForm):
    first_name       = forms.CharField(max_length=150)
    last_name        = forms.CharField(max_length=150)
    email            = forms.EmailField()
    password         = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model  = Trainer
        fields = ['subscription', 'experience', 'doj', 'primary_certification']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):

    inlines       = [TrainerSpecializationInline, ClientInline]
    list_display  = ('full_name', 'email', 'experience_display', 'is_staff_display',
                 'current_plan', 'ai_included', 'max_customers',
                 'specializations', 'client_count', 'status_badge')
    list_filter   = ('subscription', 'is_archive', 'primary_certification')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    ordering      = ('user__last_name',)
    list_per_page = 20
    actions       = ['archive_trainers', 'unarchive_trainers',
                     'make_superuser', 'remove_superuser']

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return [
                ('Account', {
                    'fields': ('first_name', 'last_name', 'email', 'password', 'confirm_password')
                }),
                ('Trainer Details', {
                    'fields': ('subscription', 'experience', 'doj', 'primary_certification')
                }),
            ]
        return [
            ('Account', {
                'fields': ('full_name_display', 'email_display')
            }),
            ('Trainer Details', {
                'fields': ('experience', 'doj', 'primary_certification', 'subscription', 'is_archive')
            }),
        ]

    def get_readonly_fields(self, request, obj=None):
        return ('full_name_display', 'email_display') if obj else ()

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = TrainerCreationForm
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            user = User.objects.create(
                username   = form.cleaned_data['email'],
                email      = form.cleaned_data['email'],
                first_name = form.cleaned_data['first_name'],
                last_name  = form.cleaned_data['last_name'],
                password   = make_password(form.cleaned_data['password']),
            )
            obj.user = user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    # ── Actions ───────────────────────────────────────────────────────────
    @admin.action(description='Archive selected trainers')
    def archive_trainers(self, request, queryset):
        n = queryset.update(is_archive=True)
        self.message_user(request, '{} trainer(s) archived.'.format(n))

    @admin.action(description='Unarchive selected trainers')
    def unarchive_trainers(self, request, queryset):
        n = queryset.update(is_archive=False)
        self.message_user(request, '{} trainer(s) unarchived.'.format(n))

    @admin.action(description='Grant superuser access')
    def make_superuser(self, request, queryset):
        n = User.objects.filter(trainer__in=queryset).update(is_superuser=True, is_staff=True)
        self.message_user(request, '{} trainer(s) granted superuser access.'.format(n))

    @admin.action(description='Revoke superuser access')
    def remove_superuser(self, request, queryset):
        n = User.objects.filter(trainer__in=queryset).update(is_superuser=False, is_staff=False)
        self.message_user(request, '{} trainer(s) had superuser access revoked.'.format(n))

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop('delete_selected', None)
        return actions

    # ── List columns ──────────────────────────────────────────────────────
    @admin.display(description='Trainer', ordering='user__last_name')
    def full_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)

    @admin.display(description='Email', ordering='user__email')
    def email(self, obj):
        return obj.user.email

    @admin.display(description='Experience', ordering='experience')
    def experience_display(self, obj):
        return obj.experience or '—'

    @admin.display(description='Staff', boolean=True)
    def is_staff_display(self, obj):
        return obj.user.is_staff

    @admin.display(description='Plan', ordering='subscription__plan_name')
    def current_plan(self, obj):
        return obj.subscription.get_plan_name_display() if obj.subscription else '—'

    @admin.display(description='AI', boolean=True)
    def ai_included(self, obj):
        return obj.subscription.ai_included if obj.subscription else False

    @admin.display(description='Max Clients')
    def max_customers(self, obj):
        return obj.subscription.max_customers if obj.subscription else '—'

    @admin.display(description='Specializations')
    def specializations(self, obj):
        specs = obj.trainerspecialization_set.all()
        return ', '.join(s.get_specialization_display() for s in specs) if specs else '—'

    @admin.display(description='Clients')
    def client_count(self, obj):
        return obj.client_set.filter(is_archive=False).count()

    @admin.display(description='Status', ordering='is_archive')
    def status_badge(self, obj):
        if obj.is_archive:
            return mark_safe('<span style="color:#fff;background:#6c757d;padding:2px 10px;border-radius:12px;font-size:0.8em;">Archived</span>')
        return mark_safe('<span style="color:#fff;background:#198754;padding:2px 10px;border-radius:12px;font-size:0.8em;">Active</span>')

    @admin.display(description='Full Name')
    def full_name_display(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)

    @admin.display(description='Email')
    def email_display(self, obj):
        return obj.user.email


# ─────────────────────────────────────────────────────────────────────────────
class ClientActionForm(admin.helpers.ActionForm):
    trainer = forms.ModelChoiceField(
        queryset=Trainer.objects.filter(is_archive=False),
        required=False,
        empty_label="— Trainer —",
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    action_form   = ClientActionForm
    list_display  = ('full_name', 'email', 'phone', 'trainer_name', 'sex', 'age', 'status_badge')
    list_filter   = ('is_archive', 'sex', 'trainer')
    search_fields = ('first_name', 'last_name', 'email', 'phone',
                     'trainer__user__first_name', 'trainer__user__last_name')
    ordering      = ('last_name',)
    list_per_page = 20
    fieldsets     = [
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'sex', 'age')}),
        ('Health',        {'fields': ('height', 'weight', 'initial_fitness_level')}),
        ('Assignment',    {'fields': ('trainer', 'is_archive')}),
    ]
    actions = ['archive_clients', 'unarchive_clients', 'reassign_trainer']

    @admin.action(description='Archive selected clients')
    def archive_clients(self, request, queryset):
        n = queryset.update(is_archive=True)
        self.message_user(request, '{} client(s) archived.'.format(n))

    @admin.action(description='Unarchive selected clients')
    def unarchive_clients(self, request, queryset):
        n = queryset.update(is_archive=False)
        self.message_user(request, '{} client(s) unarchived.'.format(n))

    @admin.action(description='Reassign trainer')
    def reassign_trainer(self, request, queryset):
        trainer_id = request.POST.get('trainer')
        if not trainer_id:
            self.message_user(request, 'Select a trainer from the action bar.', level='warning')
            return
        n       = queryset.update(trainer_id=trainer_id)
        trainer = Trainer.objects.get(pk=trainer_id)
        self.message_user(request, '{} client(s) reassigned to {} {}.'.format(
            n, trainer.user.first_name, trainer.user.last_name))

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop('delete_selected', None)
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description='Client', ordering='last_name')
    def full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    @admin.display(description='Trainer', ordering='trainer__user__last_name')
    def trainer_name(self, obj):
        return '{} {}'.format(obj.trainer.user.first_name, obj.trainer.user.last_name)

    @admin.display(description='Status', ordering='is_archive')
    def status_badge(self, obj):
        if obj.is_archive:
            return mark_safe('<span style="color:#fff;background:#6c757d;padding:2px 10px;border-radius:12px;font-size:0.8em;">Archived</span>')
        return mark_safe('<span style="color:#fff;background:#198754;padding:2px 10px;border-radius:12px;font-size:0.8em;">Active</span>')


# ─────────────────────────────────────────────────────────────────────────────
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    list_display  = ('plan_label', 'max_customers', 'ai_included', 'trainer_count')
    search_fields = ('plan_name',)
    ordering      = ('plan_name',)
    fields        = ('plan_name', 'max_customers', 'ai_included')

    @admin.display(description='Plan')
    def plan_label(self, obj):
        return obj.get_plan_name_display()

    @admin.display(description='Trainers on Plan')
    def trainer_count(self, obj):
        return Trainer.objects.filter(subscription=obj).count()

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop('delete_selected', None)
        return actions

    def has_delete_permission(self, request, obj=None):
        return False