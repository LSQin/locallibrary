import uuid
from django.db import models
from django.db.models.deletion import RESTRICT
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Genre(models.Model):
    """Model representing  a book genre."""
    name = models.CharField(max_length=200, help_text="Enter a book gnera (e.g. Science Fiction)")

    def __str__(self) -> str:
        """String for representing the Model object."""
        return self.name


from django.urls import reverse # Used to generate URLs by reversing the URL patterns

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book.)"""
    title = models.CharField(max_length=200)

    # Foreign key is used because book can only have one author, but authors can have multiple books
    # Author as a string rather than an object because it isn't been declared yet in the file
    author = ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")

    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 \
        characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    
    # ManyToManyField used because genre can contain many books.Books can cover many genres.
    # Genre class has already been defined so we can sepcify the object above.
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
import uuid # required for unique book instances

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique id for this part\
        icular book across the llibrary')
    book = models.ForeignKey(Book, on_delete=RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Resvered'),
    )

    status = models.CharField(
        max_length=1, 
        choices=LOAN_STATUS, 
        blank=True, 
        default='m',
        help_text='book availability',
    )

    class Meta:
        ordering = ['due_back']
    
    def __str__(self):
        """String for representing the Model object"""
        return f'{self.id}({self.book.title})'

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_dead = models.DateField('Dead', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self) -> str:
        """String for representing the Model object."""
        return f'{self.first_name},{self.last_name}'