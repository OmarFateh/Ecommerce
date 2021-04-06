from django.urls import path

from .views import (
    register,
    login_user,
    login_register_user, 
    logout_user,
    profile, 
    add_delete_favourite,
    update_delete_review,
    validate_email,
)

# namespace = accounts

urlpatterns = [
    # Authentication
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('login/register/', login_register_user, name='login-register'),
    path('logout/', logout_user, name='logout'),
    
    # Profile 
    path('account/', profile, name='profile'),
    # js validations
    path('ajax/validate/email/', validate_email, name='ajax-validate-email'),
    # favourites
    path('ajax/favourite/add/', add_delete_favourite, name='add-delete-favourite'),
    # Reviews
    path('ajax/review/<int:review_id>/update/delete/', update_delete_review, name='update-delete-review'),
]    