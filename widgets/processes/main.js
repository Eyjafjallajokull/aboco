(function(){
	var w = $.extend({}, Widget);
	
	w.classes = 'doubleWidth autoHeight'
	w.mainTpl = '<div class="processesData"></div>';
	w.tableTpl = '<table><tr><th>user</th><th title="CPU usage">cpu</th><th title="Memory usage">mem</th><th>command</th></tr>$1</table>';
	w.tableRowTpl = '<tr><td>$1</td><td class="tar">$3</td><td class="tar">$4</td>'+
		'<td title="$5 $6">$5</td></tr>';
	
	w.render = function(data) {
		data = jQuery.trim(data).split('\n')
		var tableRows = '';
		for(var i=0; i<data.length; i++) {
			data[i] = jQuery.trim(data[i]);
			data[i] = $('<div/>').text(data[i]).text();
			data[i] = data[i].replace(
					/^([^\s]+)[\s]+([^\s]+)[\s]+([^\s]+)[\s]+([^\s]+)[\s]+([^\s]+)(.*)$/gi,
					this.tableRowTpl);
			tableRows += data[i];
		}
		var table = this.tableTpl.replace('$1',tableRows);
		$('.processesData').html(table);
		
	};
	
	$(function(){ 
		WidgetManager.register('ProcessesWidget', 'Processes', w);
	})
})();