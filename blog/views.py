from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

"""
Defining a PostListView class that can be used to replace functions and makes the code lighter.
It will replace the post_list function.
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
    
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id = post_id , status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = f"{cd['name']} recomends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'juanmadev69@gmail.com', [cd['to']])
            sent = True
            
    else:
        form = EmailPostForm()
        
    return render(request, 'blog/post/share.html'), {'post': post, 
                                                     'form':form, 
                                                     'sent':sent}