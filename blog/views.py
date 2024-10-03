# accounts/vi# accounts/views.py

from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import UserProfile,CreatePost
from .forms import CustomUserCreationForm,LoginForm,updateProfile,UserForm,Create_Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Retrieve the image file from the form
            profile_pic = form.cleaned_data.get('profile_pic')
            

            # Create UserProfile instance
            if profile_pic:
               UserProfile.objects.create(user=user, profile_pic=profile_pic)
            else:
                UserProfile.objects.create(user=user)

            # Optionally log the user in after registration
          
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
            return redirect("home")  # Replace 'home' with your desired redirect URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'Register.html', {'form': form})

def login_view(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data["password"]
            username=form.cleaned_data['username']
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return render(request, "login.html", {"form": form, "error": "Invalid username or password."})
        else:
            return render(request,'login.html',{'form':form,"error":"invalid input"})
    else:
        form=LoginForm()
        return render(request,'login.html',{"form":form})
    

def index(request, page_no=1):  # Default to page 1
    posts = CreatePost.objects.select_related('author', 'author__userprofile').all()
    paginator = Paginator(posts, 2)  # Adjust posts per page as needed

    try:
        page = int(page_no)
    except ValueError:
        return HttpResponseBadRequest('Invalid page number')

    try:
        page_obj = paginator.page(page_no)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        posts_data = [
            {
                'post_id': post.id,
                'title': post.title,
                'content': post.content,
                'author': f"{post.author.first_name} {post.author.last_name}",
                'created_at': post.created_at,
                'profile_pic': post.author.userprofile.profile_pic.url if post.author.userprofile.profile_pic else None
            }
            for post in page_obj.object_list
        ]
        return JsonResponse({
            'posts': posts_data,
            'has_next': page_obj.has_next() if page_obj.has_next() else None,
            'has_previous': page_obj.has_previous() if page_obj.has_previous() else None,
            'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'page_num': paginator.num_pages,
            'current_page': page_obj.number
        })
    else:
        return render(request, "index.html", {"page": page_obj, "paginator": paginator})
        



from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def post(request):
    
    if request.method=='POST':
        title = request.POST.get('title')# Safer way to access form data
        content = request.POST.get('content')
        author=request.user
        CreatePost.objects.create(title=title,content=content,author=author)
        return redirect('home')
    else:
        form=Create_Post()
        return render(request,'post-create.html',{"form":form})
    
    
@login_required(login_url="/login/")
def changeProfile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = updateProfile(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_posts')  # Replace 'user_posts' with your desired redirect URL
        else:
            messages.error(request, 'There was an error updating your profile. Please check the form and try again.')
    else:
        user_form = UserForm(instance=request.user)
        

    context = {
        'user_form': user_form,
        
        'img_url': user_profile.profile_pic.url if user_profile.profile_pic else None
    }

    return render(request, 'change-profile.html', context)
     
         
@login_required(login_url="/login/")
def userPosts(request):
    
    posts=CreatePost.objects.filter(author=request.user).select_related('author', 'author__userprofile').all()
    return render(request,"user-posts.html",{"posts":posts})
    


def logout_view(request):
    logout(request)
    return redirect('home')


def deletePost(request,id):
    CreatePost.objects.filter(id=id).delete()
    return redirect('home')




def updatePost(request,id):
    post=get_object_or_404(CreatePost,id=id)

    if request.method=='POST':
        form=Create_Post(request.POST,instance=post)
        if  form.is_valid:
            form.save()
           
            return redirect('home')

    else:
        form=Create_Post(instance=post)
        return render(request,'update-post.html',{"form":form})



