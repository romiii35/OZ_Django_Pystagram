from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from blog.forms import BlogForm
from blog.models import Blog
from django.urls import reverse


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    # 'created_at' =>ASC(최신글이 아래로)// '-created_at'= DSC(최신글이 위로)
    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )
        # blogs = blogs.filter(content__icontains=q)

    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)


    context = {
        # 'blogs': blogs,
        'object_list' : page_object.object_list,
        'page_obj' : page_object,
    }

    return render(request, 'blog_list.html', context)



def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)

@login_required()
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect(reverse('fb:detail', kwargs={'pk' : blog.pk}))

    context = {'form': form}
    return render(request, 'blog_form.html', context)
@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    # if request.user != blog.author:
    #     raise Http404
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        blog = form.save()
        return redirect(reverse('fb:detail', kwargs={'pk' : blog.pk}))

    context = {
        'form': form
    }
    return render(request, 'blog_form.html', context)

@login_required()
@require_http_methods('POST')
def blog_delete(request, pk):
    # if request.method != 'POST':
    #     raise Http404
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()
    return redirect(reverse('fb:list'))
