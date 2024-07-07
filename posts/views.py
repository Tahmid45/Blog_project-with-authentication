from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
#class based view
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView,DetailView

from django.utils.decorators import method_decorator

# Create your views here.
@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            # post_form.cleaned_data['author'] = request.user
            post_form.instance.author = request.user
            post_form.save()
            return redirect('profilePage')
    else:
        post_form = forms.PostForm()
    return render(request, 'add_post.html', {'form':post_form})

#Add post using class based view
@method_decorator(login_required, name = 'dispatch')
class AddPostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('profilePage')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def edit_post(request, id):
    post = models.Post.objects.get(pk=id)
    post_form = forms.PostForm(instance = post)
    # print(post.title)
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            return redirect('profilePage')
    return render(request, 'add_post.html', {'form':post_form})

#Update post using class based view
@method_decorator(login_required, name = 'dispatch')
class EditPostView(UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profilePage')



@login_required
def delete_post(request, id):
    post = models.Post.objects.get(pk=id)
    post.delete()
    return redirect('homepage')


#delete post using class based view
@method_decorator(login_required, name = 'dispatch')
class DeletePostView(DeleteView):
    model = models.Post
    template_name = 'delete.html'
    success_url = reverse_lazy('profilePage')
    pk_url_kwarg = 'id'

class DetailPostView(DetailView):
    model = models.Post
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'
    
    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        post = self.get_object() # In which post we commented
        if comment_form.is_valid():
            new_comment = models.Comment(post = post, name=comment_form.cleaned_data.get('name'), email=comment_form.cleaned_data.get('email'), body=comment_form.cleaned_data.get('body')) # Create an new Comment object
            new_comment.save()
        
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object # # In which post we commented
        comments = models.Comment.objects.filter(post=post) # Filter the comment on of the post
        comment_form = forms.CommentForm()
        
        context['comments'] = comments 
        context['comment_form'] = comment_form
        return context
        

    
    