(function(){
	var w = $.extend({}, Widget);
	
	w.mainTpl = '<pre class="commanderData" style="font-family: monospace;"></pre>';
	
	w.init = function() {
		if (this.config.title)
			this.$('h3').text(this.config.title)
		else
			this.$('h3').text(this.config.command)
	};
	
	w.render = function(data) {
		this.$('.commanderData').text(data);
	};
	
	$(function(){ 
		WidgetManager.register('CommanderWidget', 'Commander', w);
	});
})();