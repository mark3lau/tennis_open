from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse


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



# def delete_comment(request, pk):
#     comment = get_object_or_404(Comment, pk=pk, user=request.user)
#     if request.method == 'POST':
#         comment.delete()
#         return redirect('comments')
#     return render(request, 'delete_comment.html', {'comment': comment})


@login_required
# For the user to delete one of their comments
class DeleteComment(DeleteView):
    model = Comment
    template_name = 'delete.html'
    success_url = reverse_lazy('comments')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def delete(self, request, *args, **kwargs):
        booking = self.get_object()
        messages.success(request, "Your booking has been deleted.")
        return super().delete(request, *args, **kwargs)


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