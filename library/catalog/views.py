from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookInstance, Genre, Language
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_avaliable = BookInstance.objects.filter(status__exact = 'a').count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_avaliable': num_instances_avaliable,
    }
    
    
    return render(request, 'catalog/index.html', context=context)


class BookCreate(LoginRequiredMixin, CreateView):
    #will look for book_from.html inside the templates
    model = Book
    fields = "__all__"


class BookDetail(DetailView):
    #will look for book_detail.html inside the templates folder.
    model = Book

@login_required
def my_view(request):
    return render(request, 'catalog/my_view.html')


class SignUpView(CreateView):    
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'catalog/signup.html'


class CheckedOutBooksByUserView(LoginRequiredMixin, ListView):
    #list all book instances but filter based on currently loged in user session.
    model = BookInstance
    template_name = 'catalog/profile.html' 
    paginate_by = 5 # 5 book instance per page.
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).all()