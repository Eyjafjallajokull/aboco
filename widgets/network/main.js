(function(){
	var w = $.extend({}, Widget);
	/*
	w.recordTpl = '$2: <span>$1</span><br/>';
	w.render = function(data) {
		data = data.split('\n');
		var html = '';
		for(var i=0; i<data.length; i++) {
			html += data[i].replace(/^\s*(\d+)\s*(.+)\s*$/, this.recordTpl);
		}
		this.$('.widget').html(html);
	};*/
	
	
	w.mainTpl = function() {
		var w = this.$('.widget').width()-2;
		var h = this.$('.widget').height()-2;
		return '<canvas width="'+w+'" height="'+h+'"></canvas>';
	};
	
	w.init = function() {
		this.ts = {
				rx:new TimeSeries(),
				tx:new TimeSeries()
		};
		this.smoothie = new SmoothieChart({
			grid: { 
				strokeStyle:'rgb(200, 200, 200)', fillStyle:'rgb(255, 255, 255)',
				lineWidth: 1, millisPerLine: 250, verticalSections: 6, },
			labels: { fillStyle:'#444' }
		});
		this.smoothie.streamTo(this.$('canvas')[0], 1000);

		this.smoothie.addTimeSeries(this.ts.rx,
				{ strokeStyle:'rgb(0, 255, 0)', fillStyle:'rgba(0, 255, 0, 0.4)', lineWidth:3 });
		this.smoothie.addTimeSeries(this.ts.tx,
				{ strokeStyle:'rgb(255, 0, 0)', fillStyle:'rgba(255, 0, 0, 0.4)', lineWidth:3 });
	};
	
	w.render = function(data) {
		console.log(data);
		
		this.ts.tx.append(new Date().getTime(), data.tx);
		this.ts.rx.append(new Date().getTime(), data.rx);
	};
	
	$(function(){ 
		WidgetManager.register('NetworkWidget', 'Network', w);
	});
})();
