$(function () {
	if($('#range') .children("option:selected") .attr('value') == 'from'){
		$('.toDate_hidden') .attr('class', 'toDate_visible');
	}
		
	$('#range') .change(function(){
		if($(this) .children("option:selected") .attr('value') == 'from'){
			$('.toDate_hidden') .attr('class', 'toDate_visible');
		}
		else{$('.toDate_visible') .attr('class', 'toDate_hidden');}
	});

	$('#search_button') .click(function(){	
		//var range = $('#range') .attr('value');
		var year = '';
		var month = '';
		var day = '';
		var range  = '';
		
		if ($('#year').attr('value') != '' || $('#month').attr('value') != '' || $('#day').attr('value') != ''){			
			if ($('#year').attr('value') != ''){
				year = 'y' + $('#year').attr('value');
			} else {
				year = 'y*';
			}
			if ($('#month').attr('value') != ''){
				month = 'm' + $('#month').attr('value');
			} else {
				month = 'm*';
			}
			
			if ($('#day').attr('value') != ''){
				day = 'd' + $('#day').attr('value');
			} else {
				day = 'd*';
			}
			range = ' AND date:' + year + month + day;
		}
		/*var year = $('#year').attr('value');
		var month = $('#month').attr('value');
		var day = $('#day').attr('value');
		var date;*/
		if ($('#q') .attr('value') != ''){
			var search_text = $('#q') .attr('value');
		} else { 
			search_text = '*:*';
		}
		//var search_text = $('#q') .attr('value');
				
		/*if (range == 'exactly'){
			date = year + month + day;
		}
		else if (range == 'after'){
			date = '[' + year + month + day + ' TO *]';
		}
		else if (range == 'before'){
			date = '[* TO ' + year + month + day + ']';
		}
		else if (range == 'from'){
			var year2 = $('#year2').attr('value');
			var month2 = $('#month2').attr('value');
			var day2= $('#day2').attr('value');
		
			date = '[' + year + month + day + ' TO ' + year2 + month2 + day2 + ']';
		}
		else{ date = 'none';};
		*/
		
		$('#q') .attr('value', search_text + range);
	});
	
	
});