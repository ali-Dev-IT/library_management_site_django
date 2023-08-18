from django.shortcuts import render , redirect , get_object_or_404
from .models import Book, Category
from .forms import BookForm 
from .forms import CategoryForm 

# Create your views here.

def index (request) :

    if request.method == 'POST' :
        add_book = BookForm(request.POST , request.FILES)
        if add_book.is_valid() :
            add_book.save()

        add_category = CategoryForm(request.POST)
        if add_category.is_valid() :
            add_category.save()    

    context = {
        'category': Category.objects.all(),
        'books' : Book.objects.all(),
        'bForm' : BookForm(),
        'cForm' : CategoryForm(),
        'allbooks' : Book.objects.filter(active=True).count(),
        'soldbooks' : Book.objects.filter(status='sold').count(),
        'rentalbooks' : Book.objects.filter(status='rental').count(),
        'availblebooks' : Book.objects.filter(status='availble').count(),
    }
    return render(request,'pages/index.html', context)

def books (request) :

    title = None
    search = Book.objects.all()
    if 'search_name' in request.GET :
        title = request.GET['search_name']
        if title :
            search = search.filter(title__icontains=title)

    context = {
        'category': Category.objects.all(),
        'books' : search,
        'cForm' : CategoryForm(),
    }
    return render(request,'pages/books.html', context)


def update(request,id):
    book_id = Book.objects.get(id=id)
    if request.method == 'POST':
        save_book = BookForm(request.POST,request.FILES,instance=book_id)
        if save_book.is_valid():
            save_book.save()
            return redirect('/')
    else:
        save_book = BookForm(instance=book_id)

    context = {
        'uForm' : save_book,
    }            

    return render(request,'pages/update.html',context)

def delete(request,id):
    delete_book = get_object_or_404(Book,id=id)
    if request.method == 'POST':
        delete_book.delete()
        return redirect('/')
    return render(request,'pages/delete.html')        
