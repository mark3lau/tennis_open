from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm


@login_required
def comment_create(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('comment_list')
    else:
        form = CommentForm()
    return render(request, 'comment_create.html', {'form': form})


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comment_edit.html', {'form': form})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('comment_list')
    return render(request, 'comment_delete.html', {'comment': comment})


def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'comment_list.html', {'comments': comments})