(function($) {
  $(function() {
    var container = $('.object-tools');
    var button = container.find('li').clone();
    button.find('a').attr('href', './make').html('tokens erzeugen');
    container.prepend(button);
  });
})(django.jQuery);
