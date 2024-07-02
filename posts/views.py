from django.shortcuts import render,redirect
from . import forms
from . import models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy

# Create your views here.

# @login_required
# def add_post(request):
#     if request.method == 'POST':
#         post_forms = forms.PostForm(request.POST)
#         if post_forms.is_valid():
#             post_forms.instance.author = request.user
#             post_forms.save()
#             return redirect('homepage')
#     else:
#         post_forms = forms.PostForm()
#     return render(request, 'add_post.html',{'form': post_forms})

#add post class based view 
@method_decorator(login_required, name='dispatch')
class AddPosTCreateView(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('homepage')
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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

#edit post in update view class
@method_decorator(login_required, name='dispatch')
class EditPostView(UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')

@login_required
def delete_post(request,id):
    post = models.Post.objects.get(pk=id)
    post.delete()
    return redirect('homepage')

#class based deleteview added
@method_decorator(login_required, name='dispatch')
class DeletePostView(DeleteView):
    model = models.Post
    template_name = 'delete.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')

class PostDetailView(DetailView):
    model = models.Post 
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'
    

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object 
        comments = post.comments
        if self.request.method == 'POST':
            comment_form = forms.CommentForm(data=self.request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
        else:
            comment_form = forms.CommentForm()

        context['comments'] = comments
        context['comment_form'] = comment_form
        return context