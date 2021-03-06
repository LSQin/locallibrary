from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('books/', views.BookListView.as_view(), name="books"),

    # path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/<pk>', views.BookDetailView.as_view(), name='book-detail'),
    # re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),

    path('authors/', views.AuthorListView.as_view(), name="authors"),

    path('author/<pk>', views.AuthorDetailView.as_view(), name="author-detail"),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
]

urlpatterns += [
    path('borrowed/', views.AllBorrowedBooksListView.as_view(), name="all-borrowed"),
]

# Add a url configuration for the renew_books page.
urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name="renew-book-librarian"),
]