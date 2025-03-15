from django.shortcuts import get_object_or_404, render
from .models import Post, Coment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count, Min, Max, Avg

"""
Defining a PostListView class that can be used to replace functions and makes the code lighter.
It will replace the post_list function.
"""
# class PostListView(ListView):
#     queryset = Post.published.all()
#     content_object_name = 'posts'
#     paginate_by = 5
#     template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None): # if tag_slug=jazz
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug) # slug=jazz
        post_list = post_list.filter(tags__in=[tag]) # filter by jazz
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
    
    return render(request,'blog/post/list.html', {'posts':posts, 'tag':tag})

def post_detail(request, year, month, day, post):
    """
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("No posts found")
    return render(request, 'blog/post/detail.hmtl', {'post':post})
    """
    
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Process the form data
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} {cd['email']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            # Send the email
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']],
            )
            sent = True

    else:
        form = EmailPostForm()
    
    # Render the template with context
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        },
    )
    
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # List for active comments for this post
    comments = post.comments.filter(active=True)
    # Form for user to make a comment
    form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-publish')[:4]
        
    return render(request, 
                  'blog/post/detail.html', 
                  {'post':post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form':form, 'comment':comment})