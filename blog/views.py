import pdb
from math import ceil

from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from blog.models import Post
from .forms import PostForm

PAGE_SIZE = 2


def truncate(p):
    p.text = p.text[:500] + "....."
    return p


def post_list(request):
    all_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    size = all_posts.count()
    try:
        page = int(request.GET['page'])
    except KeyError:
        page = 1
    number_of_pages = int(ceil(size / PAGE_SIZE))
    pages = list(range(1, number_of_pages+1))
    paginator = Paginator(all_posts, PAGE_SIZE)
    paginated_posts = paginator.page(page)
    posts = map(truncate, paginated_posts)
    def prev():
        if int(page) == 1:
            return page
        else:
            return int(page) - 1

    def next():
        if int(page) == number_of_pages:
            return page
        else:
            return int(page) + 1

    return render(request, 'blog/post_list.html', {
        'posts': posts, 'pages': pages, 'current_page': page, 'prev': prev(), "next": next()
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('/')
            else:
                return redirect('error/')
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return redirect('/accounts/login')


def error(request):
    return HttpResponseNotFound("<h1>Oops... something went wrong!</h1>")


def post_error(request):
    return HttpResponseNotFound(
        "<a href=\"/accounts/login/\"> Try Logging In</a>")


def profile(request):
    if request.user.is_authenticated:
        all_posts = Post.objects.filter(author=request.user.id)
        size = all_posts.count()
        try:
            page = int(request.GET['page'])
        except KeyError:
            page = 1
        number_of_pages = int(ceil(size / PAGE_SIZE))
        pages = list(range(1, number_of_pages + 1))
        paginator = Paginator(all_posts, PAGE_SIZE)
        paginated_posts = paginator.page(page)
        posts = map(truncate, paginated_posts)

        def prev():
            if int(page) == 1:
                return page
            else:
                return int(page) - 1

        def next():
            if int(page) == number_of_pages:
                return page
            else:
                return int(page) + 1

        return render(request, 'blog/profile.html', {
        'posts': posts, 'pages': pages, 'current_page': page, 'prev': prev(), "next": next()
    })
    else:
        return redirect('/accounts/login')
