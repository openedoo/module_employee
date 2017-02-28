$(document).on('click', '.delete-link', function () {
  var usernameWhoWillBeDeleted = $(this).data('username');
  $('#deleteConfirmationModal .modal-body b').text(usernameWhoWillBeDeleted);

  var deleteLink = $(this).data('link');
  $('#deleteConfirmationModal .modal-footer #delete-link').attr('href', deleteLink);
});
