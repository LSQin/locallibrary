from django.contrib import admin

# Register your models here.

from .models import Book, BookInstance, Genre, Language, Author

admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Author)