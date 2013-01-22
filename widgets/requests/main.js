(function(){
	var w = $.extend({}, Widget);

    w.mainTpl = '<table width="99%">'+
        '<tr style="font-size:20px"><td id="requestsWidgetNum" align="right" width="50%">0<td><td>hits/sec</td></table>';

	w.render = function(data) {
		if (data instanceof Object && typeof data.error !== undefined) {
			this.$('.widget').text(data.error);
		} else {
			this.$('#requestsWidgetNum').text(data);
		}
	};
	
	$(function(){ 
		WidgetManager.register('RequestsWidget', 'Requests', w);
	});
})();
