$(document).on('click', '#complete_matches', function(e) {
    e.preventDefault();
    $('.match_status').attr('checked', 'checked');
});