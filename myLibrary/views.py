from django.shortcuts import render , redirect , get_object_or_404
from .models import *
from .forms import *
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
# Create your views here.

@login_required
def home_view(request):
    total_books = BookModel.objects.count()
    total_members = MemberModel.objects.count()
    total_issued = IssueModel.objects.filter(return_date__isnull=True).count()
    total_overDue = IssueModel.objects.filter(return_date__isnull=True , due_date__lt = date.today()).count()

    context = {
        'total_books': total_books,
        'total_members': total_members,
        'total_issued': total_issued,
        'total_overDue': total_overDue
    }
    return render(request,'home.html',context)


def return_book(request,issue_id):
    issue = get_object_or_404(IssueModel ,  id=issue_id)
    issue.return_date = date.today()
    issue.book.available_copies += 1
    issue.book.save()
    issue.save()
    return redirect('issue_book')



# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# BOOKS
@login_required
@login_required
def books(request):
    books = BookModel.objects.all()
    form = BookForm(request.POST or None)
    search_form = BookSearchForm(request.GET)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('books')

    if search_form.is_valid() and search_form.cleaned_data['query']:
        q = search_form.cleaned_data['query']
        books = books.filter(title__icontains=q)

    return render(request, 'books.html', {
        'form': form,
        'books': books,
        'search_form': search_form
    })


# MEMBERS
@login_required
def members(request):
    form = MemberForm(request.POST or None)
    search_form = MemberSearchForm(request.GET)
    members = MemberModel.objects.all()

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('members')

    if search_form.is_valid() and search_form.cleaned_data['query']:
        q = search_form.cleaned_data['query']
        members = members.filter(name__icontains=q)

    return render(request, 'members.html', {
        'form': form,
        'members': members,
        'search_form': search_form
    })

# ISSUE / RETURN
@login_required
def issue_book(request):
    issues = IssueModel.objects.filter(return_date__isnull=True)
    form = IssueForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        issue = form.save(commit=False)
        issue.issue_date = date.today()
        issue.due_date = issue.issue_date + timedelta(days=14)
        issue.save()
        return redirect('issue_book')
    return render(request, 'issue_book.html', {'form': form, 'issues': issues})

@login_required
def return_book(request, issue_id):
    issue = get_object_or_404(IssueModel, id=issue_id)
    issue.return_date = date.today()
    issue.book.available_copies += 1
    issue.book.save()
    issue.save()
    return redirect('issue_book')