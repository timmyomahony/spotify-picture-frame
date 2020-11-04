import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.contrib import admin
from .models import Track
from django.utils.safestring import mark_safe


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    readonly_fields = ("title", "artist", "album", "image", "href", "data_prettified")
    fields = ("title", "artist", "album", "image", "href", "data_prettified")
    list_display = ("title", "artist", "album", "published")
    list_editable = ("published",)

    def data_prettified(self, instance):
        response = json.dumps(instance.data, sort_keys=True, indent=2)
        response = response[:5000]
        formatter = HtmlFormatter(style='colorful')
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + response)

    data_prettified.short_description = 'data prettified'
