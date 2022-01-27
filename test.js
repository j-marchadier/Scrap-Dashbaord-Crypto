$('.form-inline').on('show.bs.dropdown', function () {
$(this).parents('.item-content').addClass('active');
});
$('.dropdown').on('hide.bs.dropdown', function () {
$(this).parents('.item-content').removeClass('active');
});