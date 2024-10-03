from django.contrib import admin
from django.urls import path
from .views import index,register,login_view,post,changeProfile,userPosts,logout_view,deletePost,updatePost
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,{'page_no':1},name="home"), 
    path('page/<int:page_no>/', index,name="Home"),
 # For root URL '/'
     # Capture group for optional number
    path('login/',login_view,name='login'),
    path('register/',register,name='register'),
    path('logout/',logout_view,name='logout'),
     path('create-post/',post,name="create-post"),
    path('change-profile/',changeProfile,name="change-profile"),
    path('related-posts/',userPosts,name="user_posts"),
    path('delete-post/<int:id>/',deletePost),
    path('update-post/<int:id>/',updatePost),
    # rest passsword

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
    


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

