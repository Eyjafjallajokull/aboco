(function(){
	var w = $.extend({}, Widget);

    w.mainTpl = '<table width="99%">'+
        '<tr style="font-size:20px"><td id="networkDataUp" align="right" width="50%">0<td><td>kbps</td>'+
        '<tr style="font-size:20px"><td id="networkDataDown" align="right">0<td><td>kbps</td></table>';
	
	w.init = function() {
        this.tx = this.rx = null;
	};
	
	w.render = function(data) {
        data = data.split(' ');
        var rx = parseInt(data[0]),
            tx = parseInt(data[1]),
            crx, ctx;
        if (this.tx !== null) {
            crx = Math.round(Math.abs(this.rx - rx)*8/1000);
            ctx = Math.round(Math.abs(this.tx - tx)*8/1000);
            this.$('#networkDataDown').text(crx);
            this.$('#networkDataUp').text(ctx);
        }
        this.tx = tx;
        this.rx = rx;
	};
	
	$(function(){ 
		WidgetManager.register('NetworkWidget', 'Network', w);
	});
})();
