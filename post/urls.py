from django.urls import path
from .views import (
    post_detail, post_list, create_post, edit_post, delete_post,
    add_comment, delete_comment, toggle_like, liked_posts_list,
    user_profile, edit_profile
)

urlpatterns = [
    # Post URLs
    path('', post_list, name='posts_list'), 
    path('create/', create_post, name='create_post'), 
    path('<int:post_id>/', post_detail, name='post_detail'),
    path('edit/<int:post_id>/', edit_post, name='edit_post'),
    path('delete/<int:post_id>/', delete_post, name='delete_post'),
    
    # Comment URLs
    path('<int:post_id>/comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    
    # Like URLs
    path('<int:post_id>/like/', toggle_like, name='toggle_like'),
    path('liked/', liked_posts_list, name='liked_posts'),
    
    # Profile URLs
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]

