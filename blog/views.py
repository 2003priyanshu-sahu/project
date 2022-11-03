from unicodedata import category
from django.forms import SlugField
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post ,Category ,Tag ,Comment
from .forms import PostForm, SignupForm , LoginForm ,CommentForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.http import HttpResponse


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {
                                              'posts':posts,
                                              
                                              })
def CategoryView(request,slug):
    post= get_object_or_404(Post, slug=slug)
    posts = Post.objects.filter(category=post.category)
    return render(request, "blog/categories.html", {"category": category,'posts': posts})




def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post.slug)


    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('post_list')
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form': form})



def login_view(request):
    form = LoginForm()
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form,'00000')
            
            # print(username, password,'111111111111111')
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                print(user, "555555555")
                return redirect('post_list')
            else:
                form = LoginForm()
    return render (request, "blog/login.html", {"form" : form})
        

def logout_view(request):
    
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('post_list')


@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'blog/profile.html', {'user_form': user_form, 'profile_form': profile_form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'blog/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('post_list')





def post_detail(request, slug): 
    comment_form = CommentForm()   

    post = get_object_or_404(Post, slug=slug,
                                   status='published',)

    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj= None
            try:
                parent_id= int(request.POST.get("parent_id"))
            except:
                parent_id= None
            
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    reply_comment = comment_form.save(commit=False)
                    reply_comment.parent= parent_obj
       
            new_comment = comment_form.save(commit=False)

            new_comment.post = post

            new_comment.save()
            
            
    else:
        comment_form = CommentForm()                   
    return render(request,
                  'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


    
def list_posts_by_tag(request, slug=None):

    tag = get_object_or_404(Tag, slug=slug)

    posts = Post.objects.filter(status="published", tags=tag)

    context = {
        "tag_name": tag.name,
        "posts": posts
    }
    return render(request, 'blog/filter_by_tag.html', context)