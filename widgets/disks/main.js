(function(){
	var w = $.extend({}, Widget);
	
	w.classes = 'doubleWidth';
	
	w.tableTpl = '<table><tr><th>disk</th><th>size</th><th>used</th><th>mount&nbsp;point</th>$1</tr></table>';
	w.tableRowTpl = '<tr><td>$1</td><td class="tar">$2</td><td class="tar">$5</td><td>$6</td></tr>';
	
	w.render = function(data) {
		data = jQuery.trim(data).split('\n')
		var tableRows = '';
		for(var i=0; i<data.length; i++) {
			data[i] = jQuery.trim(data[i]);
			data[i] = $('<div/>').text(data[i]).text();
			data[i] = data[i].replace(
					/^([^\s]+)[\s]+([^\s]+)[\s]+([^\s]+)[\s]+([^\s]+)[\s]+([^\s]+)[\s]+(.*)$/gi,
					this.tableRowTpl);
			tableRows += data[i];
		}
		var table = this.tableTpl.replace('$1',tableRows);
		this.$('.widget').html(table);
	};
	
	$(function(){ 
		WidgetManager.register('DisksWidget', 'Disks', w);
	});
})();