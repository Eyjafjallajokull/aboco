(function(){
	var w = $.extend({}, Widget);

	w.init = function() {
		this.hostInfoEl = $('#hostInfo');
		this.setTitle = true;
	}

	w.render = function(data) {
		//this.$().remove();
		var html = '';
		html += '<li>'+data['uname']+'</li>';
		html += '<li>'+data['date']+'</li>';
		html += '<li>'+parseUptime(data['uptime'])+'</li>';
		this.hostInfoEl.html(html);

		if (this.setTitle) {
			$('title').prepend(data['uname'].split(' ')[1]+' - ');
			this.setTitle = false;
		}
	};

	function two(x) {return ((x>9)?"":"0")+x}
	function three(x) {return ((x>99)?"":"0")+((x>9)?"":"0")+x}
	function parseUptime(ms) {
		var out = '';
		var seconds = parseFloat(ms.split(' ')[0]);
		var days = Math.floor(seconds / 86400);
		var hours = Math.floor((seconds % 86400) / 3600);
		var minutes = Math.floor(((seconds % 86400) % 3600) / 60);

		if (days === 1) {
			out = '1 day ';
		} else if (days > 1) {
			out = days + ' days ';
		}
		out += two(hours) + ':' + two(minutes);

		return 'up '+out;
	};
	
	$(function(){ 
		WidgetManager.register('HostInfoWidget', 'HostInfo', w);
	});
})();