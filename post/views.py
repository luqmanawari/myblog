from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'search_query': search_query
    }
    return render(request, 'posts_list.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts_list')
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Permission check
    if post.author != request.user:
        return HttpResponseForbidden("You cannot edit this post.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
        else:
            print(form.errors)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Increment view count (count unique users only)
    if 'viewed_posts' not in request.session:
        request.session['viewed_posts'] = []
    
    if post_id not in request.session['viewed_posts']:
        post.view_count += 1
        post.save()
        request.session['viewed_posts'].append(post_id)
        request.session.modified = True
    
    # Get comments
    comments = post.comments.all()
    comment_form = CommentForm()
    
    # Check if user liked this post
    user_has_liked = post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked
    }
    return render(request, 'post_detail.html', context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Permission check
    if post.author != request.user:
        return HttpResponseForbidden("You cannot delete this post.")
    
    if request.method == 'POST':
        post.delete()
    return redirect('posts_list')

# Comment views
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    
    return redirect('post_detail', post_id=post_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    
    # Permission check - only author can delete
    if comment.author != request.user:
        return HttpResponseForbidden("You cannot delete this comment.")
    
    if request.method == 'POST':
        comment.delete()
    
    return redirect('post_detail', post_id=post_id)

# Like views
@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': post.get_like_count()
        })
    
    return redirect('post_detail', post_id=post_id)

@login_required
def liked_posts(request):
    """Display all posts liked by the current user"""
    liked_posts = request.user.liked_posts.all().order_by('-created_at')
    
    paginator = Paginator(liked_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'liked_posts.html', {
        'page_obj': page_obj,
        'posts': page_obj.object_list
    })

# User Profile views
@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    user_posts = user.posts.all().order_by('-created_at')
    
    paginator = Paginator(user_posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile': profile,
        'page_obj': page_obj,
        'user_posts': page_obj.object_list,
        'is_owner': request.user == user
    }
    return render(request, 'user_profile.html', context)

@login_required
def edit_profile(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def liked_posts_list(request):
    """Display all posts liked by the current user"""
    liked_posts = request.user.liked_posts.all().order_by('-created_at')
    
    paginator = Paginator(liked_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'liked_posts.html', {
        'page_obj': page_obj,
        'posts': page_obj.object_list
    })

