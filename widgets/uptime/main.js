(function(){
	var w = $.extend({}, Widget);

	w.mainTpl = '<table width="99%">'+
		'<tr style="font-size:30px"><td class="uptimeDays" align="right" width="40%"><td><td>days</td>'+
		'<tr style="font-size:25px"><td class="uptimeHours" align="right"><td><td>hours</td>'+
		'<tr style="font-size:20px"><td class="uptimeMinutes" align="right"><td><td>minutes</td>'+
		'<tr style="font-size:15px"><td class="uptimeSeconds" align="right"><td><td>seconds</td></table>';
	
	w.render = function(data) {
		duration(data*1000);
	};
	
	function two(x) {return ((x>9)?"":"0")+x}
	function three(x) {return ((x>99)?"":"0")+((x>9)?"":"0")+x}
	function duration(ms) {
		var sec = Math.floor(ms/1000)
		ms = ms % 1000
		//t = three(ms)
		
		var min = Math.floor(sec/60)
		sec = sec % 60
		this.$('.uptimeSeconds').text(sec);
		
		var hr = Math.floor(min/60)
		min = min % 60
		this.$('.uptimeMinutes').text(min);
		
		var day = Math.floor(hr/60)
		hr = hr % 60
		this.$('.uptimeHours').text(hr);
		this.$('.uptimeDays').text(day);
	};
	
	$(function(){ 
		WidgetManager.register('UptimeWidget', 'Uptime', w);
	});
})();