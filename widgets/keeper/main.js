(function(){
	var w = $.extend({}, Widget);
	
	w.mainTpl = '<ul class="keeperData"></ul>';
	
	w.init = function() {
		this.$('h3').text(this.config.title)
	};
	
	w.render = function(data) {
		var kd = this.$('.keeperData').html('');
		data.forEach(function(monitor){
			var statusHead = '';
			var statusText = '';
			var statusOk = true;
			
			if (monitor.type=='process') {
				statusHead = 'Process <b>'+monitor.value+'</b>';
				switch (monitor.status) {
				case 0: 
					statusText = 'not running';
					break;
				case 1:
					statusText = 'running 1 thread';
					break;
				default:
					statusText = 'running '+monitor.status+' threads';
					break;
				}
				statusOk = monitor.status > 0;
			}
			
			if (monitor.type=='file') {
				statusHead = 'File <b>'+U.shortenPath(monitor.value,27)+'</b>';
				statusOk = monitor.status > -1;
				if (statusOk)
					statusText = 'exists, size: '+U.prettyFileSize(monitor.status)+'';
				else
					statusText = ' does not exists';
			}
			
			if (monitor.type=='command') {
				statusHead = 'Command <b>'+monitor.value+'</b>';
				statusOk = monitor.status == 0;
				if (statusOk)
					statusText = 'succeded';
				else
					statusText = 'failed (returned status: '+monitor.status+')';
			}
			
			kd.append('<li>'+statusHead+'<br><span class="'+
					(statusOk?'statusOk':'statusFail')+'">'+
					statusText+'</span></li>');
		});
	};
	
	$(function(){ 
		WidgetManager.register('KeeperWidget', '', w);
	});
})();