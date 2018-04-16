$(function () {
	$('.expand').click(function(){
		var section = $(this) .attr('id').split('_')[1];
		$('#' + section) .toggle();
		if ($(this).attr('title') == 'expand'){
			$(this).html('-');
			$(this).attr('title', 'compact');
		}
		else if ($(this).attr('title') == 'compact'){
			$(this).html('+');
			$(this).attr('title', 'expand');
		}
	});
});