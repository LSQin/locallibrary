from django.forms.utils import to_current_timezone
from django.shortcuts import render

# Create your views here.

from .models import Book, BookInstance, Author, Genre

def index(request):
    """View function for home page of site."""

    # Fectch the number of records
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Numer of visits to this view, as counted in session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_visits' : num_visits,
    }

    # Render the HTML template 'index.html' with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing bookinstances on load to the current user."""
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user)\
            .filter(status__exact='o').order_by('due_back')

from django.contrib.auth.mixins import PermissionRequiredMixin

class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    """"""
    model = BookInstance
    permission_required =('catalog.can_mark_returned',)
    paginate_by = 2
    template_name = "catalog/bookinstance_list_borrowed.html"

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import RenewBookForm
import datetime

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""

    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is POST request then process the Form data.
    if request.method == 'POST':
        
        # Create a form object and populate it with the data from request (binding).
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            
            # Process the data in form .cleaned_data as required
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            
            # Redirect to a new url:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)    
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date,})

    context = {
        'form' : form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context=context)