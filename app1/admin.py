from django.contrib import admin

# Register your models here.
from .models import Publisher, Author, Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    list_filter = ('publication_date',)
    date_hierarchy = 'publication_date'
    filter_horizontal = ('authors',)
    raw_id_fields = ('publisher',)
##    fields = ('title', 'authors', 'publisher')#fields can be edited
##    ordering = ('-publication_date',)#'-' means des

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)