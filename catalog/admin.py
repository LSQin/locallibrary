from django.contrib import admin

# Register your models here.

from .models import Book, BookInstance, Genre, Language, Author

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# admin.site.register(Book)
# Register the admin class for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]



# admin.site.register(BookInstance)
# Register the admin class for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {'fields': ('book','imprint','id')}),
        ('Availability', {'fields': ('status', 'borrower', 'due_back')}),
    )

admin.site.register(Genre)

admin.site.register(Language)

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

# admin.site.register(Author)
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)