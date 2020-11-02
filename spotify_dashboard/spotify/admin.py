import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.contrib import admin
from .models import Code, AccessToken, Update, Artist, Album, Track
from django.utils.safestring import mark_safe

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    readonly_fields = ('data_prettified',)

    def data_prettified(self, instance):
        response = json.dumps(instance.data, sort_keys=True, indent=2)
        response = response[:5000]
        formatter = HtmlFormatter(style='colorful')
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + response)

    data_prettified.short_description = 'data prettified'

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    pass


@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    pass

