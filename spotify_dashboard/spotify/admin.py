import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.contrib import admin
from .models import Update, Track
from django.utils.safestring import mark_safe


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    readonly_fields = ("name", "last_played_at", "image", "href", "data_prettified")
    fields = ("name", "last_played_at", "image", "href", "data_prettified")
    list_display = ("name", "last_played_at")

    def data_prettified(self, instance):
        response = json.dumps(instance.data, sort_keys=True, indent=2)
        response = response[:5000]
        formatter = HtmlFormatter(style='colorful')
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + response)

    data_prettified.short_description = 'data prettified'


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    pass
