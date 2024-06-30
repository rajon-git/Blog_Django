from django.shortcuts import render,redirect
from . import forms
from . import models
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_post(request):
    if request.method == 'POST':
        post_forms = forms.PostForm(request.POST)
        if post_forms.is_valid():
            post_forms.instance.author = request.user
            post_forms.save()
            return redirect('homepage')
    else:
        post_forms = forms.PostForm()
    return render(request, 'add_post.html',{'form': post_forms})

@login_required
def edit_post(request,id):
    post = models.Post.objects.get(pk=id)
    post_forms = forms.PostForm(instance=post)
    if request.method == 'POST':
        post_forms = forms.PostForm(request.POST, instance=post)
        if post_forms.is_valid():
            post_forms.instance.author = request.user
            post_forms.save()
            return redirect('profile')

    return render(request, 'add_post.html',{'form': post_forms})

@login_required
def delete_post(request,id):
    post = models.Post.objects.get(pk=id)
    post.delete()
    return redirect('homepage')