# Django Blog - Feature Quick Start Guide

## How to Use Each Feature

### 1. Creating a Post with Author

```python
# Post automatically assigns current user as author
from post.forms import PostForm

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # ← Automatically set
            post.save()
```

### 2. Viewing User Profiles

```
Visit: /posts/profile/<username>/

Shows:
- User's avatar and bio
- Location and website
- Statistics (posts count, likes received, member since)
- All user's posts with pagination
```

### 3. Editing Your Profile

```
Visit: /posts/profile/edit/

Can edit:
- Bio (up to 500 characters)
- Profile picture
- Website URL
- Location
```

### 4. Searching Posts

```
On posts list page:
- Enter search term in the search box
- Search works across:
  * Post titles
  * Post content
  * Author usernames
- Click "Search" or press Enter
- Click "Clear" to reset
```

### 5. Liking/Unliking Posts

```
On post detail page:
- Click the heart button to like/unlike
- Like count updates immediately
- View your liked posts at /posts/liked/
```

### 6. Commenting on Posts

```
On post detail page:
1. Scroll to "Comments" section
2. Enter your comment in the textarea
3. Click "Post Comment"
4. Your comment appears immediately
5. Only you can delete your own comments
```

### 7. Viewing Post Statistics

```
Post view count:
- Shows on every post card
- Shows on post detail page
- Counts unique users only (uses sessions)

Like count:
- Shows on post cards and detail page
- Click heart to toggle

Comment count:
- Shows on post cards and detail page
- Click to jump to comments section

Author:
- Click author name/avatar to view their profile
```

### 8. Social Sharing

```
On post detail page, click share buttons for:
- Facebook: Opens Facebook share dialog
- Twitter: Pre-fills tweet with post title
- LinkedIn: Shares to LinkedIn
- Copy Link: Copies URL to clipboard
```

### 9. Pagination

```
Posts appear in groups:
- Main list: 10 posts per page
- Profile page: 5 posts per page
- Liked posts: 10 posts per page

Navigation:
- First, Previous, page numbers, Next, Last
- Current page highlighted in blue
- Shows "Page X of Y" info
```

### 10. Permission System

```
Edit/Delete buttons only show if:
- You are logged in AND
- You are the post author

If you try to edit someone else's post:
- You'll get a 403 Forbidden error
- Your changes won't be saved

Same applies to comments - only author can delete
```

---

## Database Models Quick Reference

### Post Model
```python
class Post(models.Model):
    title = CharField(max_length=200)
    content = TextField()
    image = ImageField(upload_to='post_images/', null=True, blank=True)
    author = ForeignKey(User)                    # NEW
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    view_count = IntegerField(default=0)         # NEW
    likes = ManyToManyField(User)                # NEW
```

### Comment Model (NEW)
```python
class Comment(models.Model):
    post = ForeignKey(Post, related_name='comments')
    author = ForeignKey(User)
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
```

### UserProfile Model (NEW)
```python
class UserProfile(models.Model):
    user = OneToOneField(User)
    bio = TextField(max_length=500, blank=True)
    avatar = ImageField(upload_to='avatars/', null=True, blank=True)
    website = URLField(blank=True)
    location = CharField(max_length=100, blank=True)
    created_at = DateTimeField(auto_now_add=True)
```

---

## Admin Panel Access

### To Access Admin

1. Navigate to: `/admin/`
2. Login with superuser account

### What You Can Do

**Posts**
- View all posts with filtering
- See author, view count, likes, comments
- Edit or delete posts
- Manage inline comments

**Comments**
- View all comments
- Filter by date or author
- Delete comments

**User Profiles**
- View all user profiles
- See location, creation date
- View post count for each user

---

## Template Tags & Filters Used

```django
{{ post.author.username }}              # Username
{{ post.author.get_full_name }}         # Full name
{{ post.created_at|date:"M d, Y" }}     # Format date
{{ post.content|linebreaks }}           # Preserve line breaks
{{ post.get_like_count }}               # Method call
{{ post.get_comment_count }}            # Method call
{{ post.view_count }}                   # View count
{% if post.author == user %}            # Permission check
```

---

## URL Patterns Quick Reference

### Public URLs (No Auth Required)
```
/auth/login/                 # Django default
/auth/signup/                # Custom
/admin/                      # Admin login
```

### Protected URLs (Login Required)
```
/posts/                      # All posts list (with search)
/posts/create/              # Create new post
/posts/<id>/                # View post detail
/posts/edit/<id>/           # Edit post (owner only)
/posts/delete/<id>/         # Delete post (owner only)

/posts/<id>/comment/        # Add comment
/posts/comment/<id>/delete/ # Delete comment (author only)

/posts/<id>/like/           # Toggle like
/posts/liked/               # View liked posts

/posts/profile/<username>/  # View user profile
/posts/profile/edit/        # Edit own profile
```

---

## Troubleshooting

### Can't see edit/delete buttons
→ You might not be the post author
→ Try logging in with the correct account

### Like count not changing
→ Make sure you're logged in
→ Refresh the page to see changes

### Comments not appearing
→ Wait a moment and refresh
→ Check browser console for JavaScript errors

### Search not working
→ Make sure search term has at least 1 character
→ Try searching by different field (title vs content vs author)

### Profile picture not showing
→ Check file size (must be under 10MB)
→ Supported formats: JPG, PNG, GIF

### View count stuck
→ View count only counts once per user per session
→ Open post in new session/browser to increment

---

## Best Practices

1. **Always add author when creating posts** ✓ (now automatic)

2. **Check permissions before editing** ✓ (now enforced in view)

3. **Use meaningful post titles** - Helps with search

4. **Keep comments respectful** - Anyone can see them

5. **Use profile picture** - Makes your profile more personal

6. **Search before posting** - Avoid duplicates

7. **Like posts you enjoy** - Show appreciation

8. **Comment thoughtfully** - Engage with community

---

## Performance Tips

1. Search works best with specific terms
2. Pagination prevents page from getting too slow
3. View counting uses sessions (efficient)
4. Like/unlike is instant with POST
5. Comments load on page load (optimal)

---

## API-Ready

The views are structured to support AJAX requests:

```javascript
// Example: Like with AJAX
fetch('/posts/1/like/', {
    method: 'POST',
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken')
    }
})
.then(response => response.json())
.then(data => {
    console.log('Liked:', data.liked);
    console.log('Count:', data.like_count);
});
```

---

## Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG = False` in settings
- [ ] Set `ALLOWED_HOSTS` properly
- [ ] Configure email backend for notifications
- [ ] Set up media file serving (S3, etc.)
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up static files serving
- [ ] Enable HTTPS
- [ ] Set secure cookie flags
- [ ] Configure CSRF settings
- [ ] Set up logging
- [ ] Run `python manage.py collectstatic`
- [ ] Run tests
- [ ] Create backups

---

## Need Help?

Check these resources:

- Django Docs: https://docs.djangoproject.com/
- Models: https://docs.djangoproject.com/en/stable/topics/db/models/
- Forms: https://docs.djangoproject.com/en/stable/topics/forms/
- Templates: https://docs.djangoproject.com/en/stable/topics/templates/
- Views: https://docs.djangoproject.com/en/stable/topics/http/views/
