// Submit the comment form using AJAX
$('#comment-form').on('submit', function(e) {
    e.preventDefault();
    var message = $('#comment-message').val();
    $.ajax({
        url: commentCreateUrl,
        type: 'POST',
        data: {
            'message': message,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            console.log('Comment created successfully:', data);
            $('#comment-message').val('');
            $('#comment-list').prepend(data);
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log('Error creating comment:', errorThrown);
        }
    });
});

// Delete a comment using AJAX
$('#comment-list').on('click', '.delete-comment', function() {
    var commentId = $(this).data('comment-id');
    if (confirm('Are you sure you want to delete this comment?')) {
        $.ajax({
            url: commentDeleteUrlTemplate.replace('{commentId}', commentId),
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function() {
                console.log('Comment deleted successfully');
                $('#comment-' + commentId).fadeOut();
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('Error deleting comment:', errorThrown);
            }
        });
    }
});

// Edit a comment using AJAX
$('#comment-list').on('click', '.edit-comment', function() {
    var commentId = $(this).data('comment-id');
    var message = $('#comment-' + commentId + '-message').text();
    $('#comment-' + commentId + '-message').replaceWith('<textarea id="comment-' + commentId + '-message-edit" class="form-control">' + message + '</textarea>');
    $(this).removeClass('btn-primary').addClass('btn-success').text('Save').off('click').on('click', function() {
        message = $('#comment-' + commentId + '-message-edit').val();
        $.ajax({
            url: commentEditUrlTemplate.replace('{commentId}', commentId),
            type: 'POST',
            data: {
                'message': message,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                console.log('Comment edited successfully:', data);
                $('#comment-' + commentId + '-message-edit').replaceWith('<p id="comment-' + commentId + '-message" class="card-text">' + message + '</p>');
                $('#comment-' + commentId + ' .edit-comment').removeClass('btn-success').addClass('btn-primary').text('Edit');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('Error editing comment:', errorThrown);
            }
        });
    });
});
