from django.shortcuts import render,redirect,get_object_or_404
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from .serializers import PostSerializer 
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden


def home(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 1)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myPblog/home.html',{'page_obj': page_obj})


@login_required
def add_post(request):
    if request.method == 'POST':
        Post.objects.create(
            title = request.POST["title"],
            content = request.POST[""],
            author = request.user
    )
        messages.success(request,"Your post was added successfully.")
        return redirect('home')
        
    return render(request,'myPblog/add_post.html')

@login_required
def edit_post(request,pk):
    post = get_object_or_404(Post,pk = pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post")
    if request.method == "POST":
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.save()

        messages.success(request,"Post updated successfully")
        return redirect('home')
    
    
    return render(request,'myPblog/edit_post.html',{'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
  
    # Optional: Only the author can delete
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post")

    if request.method == 'POST':
        post.delete()

        messages.success(request,"Post deleted successfully")
        return redirect('home')

    return render(request, 'myPblog/delete_post.html', {'post': post})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


@api_view(['GET'])
def post_list_api(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def post_detail_api(request,pk):
    post = Post.objects.get(pk = pk)
    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['POST'])
def create_post_api(request):
    serializer = PostSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(author = request.user)
        return Response(serializer.data,status = 201)
    return Response(serializer.errors, status = 400)

# Create your views here.
