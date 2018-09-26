# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.forms import all_valid
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.text import get_text_list
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from extra_views import UpdateWithInlinesView, CreateWithInlinesView


class WebixCreateWithInlinesView(CreateWithInlinesView):
    template_name = 'django_webix/generic/create.js'

    def get_success_url(self):
        return reverse(self.object.WebixMeta.url_update, kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        response = super(WebixCreateWithInlinesView, self).post(request, *args, **kwargs)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        inlines = self.construct_inlines()

        anonymous = request.user.is_anonymous() if callable(request.user.is_anonymous) else request.user.is_anonymous
        if all_valid(inlines) and form.is_valid() and not anonymous:
            from django.contrib.admin.models import LogEntry, ADDITION
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(self.object).pk,
                object_id=self.object.pk,
                object_repr=force_text(self.object),
                action_flag=ADDITION
            )

        return response


class WebixCreateWithInlinesUnmergedView(WebixCreateWithInlinesView):
    template_name = 'django_webix/generic/create_inline_unmerged.js'


class WebixUpdateWithInlinesView(UpdateWithInlinesView):
    template_name = 'django_webix/generic/update.js'

    def get_success_url(self):
        return reverse(self.object.WebixMeta.url_update, kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        response = super(WebixUpdateWithInlinesView, self).post(request, *args, **kwargs)

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        inlines = self.construct_inlines()

        anonymous = request.user.is_anonymous() if callable(request.user.is_anonymous) else request.user.is_anonymous
        if all_valid(inlines) and form.is_valid() and not anonymous:
            from django.contrib.admin.models import LogEntry, CHANGE
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=ContentType.objects.get_for_model(self.object).pk,
                object_id=self.object.pk,
                object_repr=force_text(self.object),
                action_flag=CHANGE,
                change_message=_('Changed %s.') % get_text_list(form.changed_data, _('and'))
            )

        return response


class WebixUpdateWithInlinesUnmergedView(WebixUpdateWithInlinesView):
    template_name = 'django_webix/generic/update_inline_unmerged.js'


class WebixDeleteView(DeleteView):
    template_name = 'django_webix/generic/delete.js'

    def get_success_url(self):
        return reverse(self.object.WebixMeta.url_list)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        anonymous = request.user.is_anonymous() if callable(request.user.is_anonymous) else request.user.is_anonymous
        if not anonymous:
            from django.contrib.admin.models import LogEntry, DELETION
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(self.object).pk,
                object_id=self.object.pk,
                object_repr=force_text(self.object),
                action_flag=DELETION
            )

        return super(WebixDeleteView, self).delete(request, *args, **kwargs)
