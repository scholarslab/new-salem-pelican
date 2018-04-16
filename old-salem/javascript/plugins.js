/**
 * Plugins for Salem Witch Trial Papers
 *
 */

$(document).ready(function(){
  /**
   * Click handler for section eyebrows pushes the name anchor to the URL and
   * scrolls
   *
   * @author Wayne Graham
   * 7/1/2014
   */
  $('.identifier').click(function(event) {
    event.preventDefault();

    var top = $(this).position().top;
    var id = "#" + $(this).data('id');

    history.pushState(null, null, id);
    $('html, body').animate({ scrollTop: top }, 800);

    return false;
  });
});


