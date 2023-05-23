from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib import messages


@login_required
def post_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('comments')
    else:
        form = CommentForm()
    return render(request, 'post_comment.html', {'form': form})


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comments')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form})


# For the user to post a comment
def comments(request):
    comments = Comment.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('comments')
    else:
        form = CommentForm()
    context = {
        'form': form,
        'comments': comments
    }
    return render(request, 'comments.html', context)


# For the user to edit a comment
class EditComment(UpdateView):
    model = Comment
    fields = ('message',)
    template_name = 'update_comment.html'
    success_url = reverse_lazy('comments')
    success_message = "Your comment has been updated successfully."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(name=self.request.user.username)

    def get_object(self, queryset=None):
        comment_id = self.kwargs['pk']
        return Comment.objects.get(pk=comment_id) 


# For the user to delete a comment
class DeleteComment(DeleteView):
    model = Comment
    template_name = 'delete.html'
    success_url = reverse_lazy('comments')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Your comment has been deleted.")
        return super().delete(request, *args, **kwargs)
