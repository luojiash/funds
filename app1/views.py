from django.shortcuts import render, render_to_response
from django.http import HttpResponse ,HttpResponseRedirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

from .models import Book, Author
from .forms import BookForm, SearchForm

# Create your views here.
def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render_to_response('search.html',{'books': books,'query': q})
    return render_to_response('search.html', {'errors': errors })

class add_book(CreateView):
    model = Book
    template_name = 'add_book.html'
    success_url = '/books/'

class show_books(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'show_books.html'

class show_authors(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'show_authors.html'

