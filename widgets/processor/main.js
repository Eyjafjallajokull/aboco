(function(){
	var w = $.extend({}, Widget);
	
	w.mainTpl = '<div class="processorData"></div>';
	
	w.render = function(data) {
		var load = Math.round(data*100/100);
		this.$('.processorData').html(load+' %');
		var c = Math.round(100 * load / 100)+100;
		load = (100-load) / 100;
		this.$('.widget').css({
			'background-image': '-webkit-gradient(linear,left top,left bottom,'+
				'color-stop('+load+', rgba(255,255,255,'+(1-load)+')),'+
				'color-stop('+(load+0.01)+', rgba('+c+',100,100,'+(1-load)+'))	)'
		});
	};
	
	$(function(){ 
		WidgetManager.register('ProcessorWidget', 'Processor', w);
	});
})();
