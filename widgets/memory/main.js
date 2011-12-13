(function(){
	var w = $.extend({}, Widget);

	w.mainTpl = '<div class="memoryLoad"></div><div class="memorySums"></div>';
	
	w.render = function(data) {
		var load = data.used/data.total;
		load = Math.round(load*100);
		this.$('.memoryLoad').text(load+' %');
		this.$('.memorySums').html('Total: '+Math.round(data.total/102.4)+
			'M Used: '+Math.round(data.used/102.4)+
			'M<br> Buffers: '+Math.round(data.buffers/102.4)+
			'M Cached: '+Math.round(data.cached/102.4) + 'M');
		
		var c = Math.round(100 * load / 100)+100;
		load = (100-load) / 100;
		this.$('.MemoryWidget').css({
			'background-image': '-webkit-gradient(linear,left top,left bottom,'+
				'color-stop('+load+', #fff),'+
				'color-stop('+(load+0.01)+', rgba('+c+',100,100,'+(1-load)+'))  )'
		});
	};
	
	$(function(){ 
		WidgetManager.register('MemoryWidget', 'Memory', w);
	});
})();
