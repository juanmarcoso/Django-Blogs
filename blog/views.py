from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

"""
Definiendo una class ListView que sirve parar reemplazar funciones y hace mas ligero el codigo
Va a reemplazar la funcion post_list
"""
class PostListView(ListView):
    queryset = Post.published.all()
    content_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'

def post_list(request):
    post_list = Post.published.all()
    #Vamos a crear un paginador
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    # If page_number is a letter
    except PageNotAnInteger:
        posts = paginator.page(1)
    
    return render(request,'blog/post/list.html', {'posts':posts})

def post_detail(request, year, month, day, post):
    """
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("No posts found")
    return render(request, 'blog/post/detail.hmtl', {'post':post})
    """
    # Alternativa:
    post = get_object_or_404(Post, 
                             status=Post.Status.PUBLISHED,
                             slug = post,
                             publish__year = year,
                             publish__month = month,
                             publish__day = day)
    return render(request, 
                  'blog/post/detail.html', 
                  {'post':post})