from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.admin.filters import FieldListFilter
from django.contrib.admin.options import IncorrectLookupParameters

from payment_processor.models import Payment

# Register your models here.


class EmptyFieldListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        if not field.empty_strings_allowed and not field.null:
            raise ImproperlyConfigured(
                "The list filter '%s' cannot be used with field '%s' which "
                "doesn't allow empty strings and nulls." % (
                    self.__class__.__name__,
                    field.name,
                )
            )
        self.lookup_kwarg = '%s__isempty' % field_path
        self.lookup_val = params.get(self.lookup_kwarg)
        super().__init__(
            field, request, params, model, model_admin, field_path)

    def queryset(self, request, queryset):
        if self.lookup_kwarg not in self.used_parameters:
            return queryset
        if self.lookup_val not in ('0', '1'):
            raise IncorrectLookupParameters

        lookup_condition = models.Q()
        if self.field.empty_strings_allowed:
            lookup_condition |= models.Q(**{self.field_path: ''})
        if self.field.null:
            lookup_condition |= models.Q(
                **{'%s__isnull' % self.field_path: True})
        if self.lookup_val == '1':
            return queryset.filter(lookup_condition)
        return queryset.exclude(lookup_condition)

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, changelist):
        for lookup, title in (
            (None, _('All')),
            ('1', _('Empty')),
            ('0', _('Not empty')),
        ):
            yield {
                'selected': self.lookup_val == lookup,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}),
                'display': title,
            }


class PaymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_filter = (
        'currency',
        ('tx_ids', EmptyFieldListFilter),
    )


admin.site.register(Payment, PaymentAdmin)
