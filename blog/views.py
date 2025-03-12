from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        post = paginator.page(paginator.num_pages)
    
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