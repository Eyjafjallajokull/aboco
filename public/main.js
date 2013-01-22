$(function(){
	Config.load(savedConfig);
	WidgetManager.init();
});

var WidgetManager = {
    /**
     * Widget Chief Officer
     *
     * Registers, installs (enables) and renders widgets.
     * Every widget has to register at startup using function `WidgetManager.register`.
     * If widget is enabled in configuration it is installed after registering.
     * Render function is executed at constant intervals, to update measurements.
     */
	registeredWidgets: {},
	installedWidgets: [],
	
	init: function() {
		this.renderWidgets();
		setInterval(this.renderWidgets, Config.get('core','updateInterval')*1000);
		$('#widgetsWrap').isotope({
			layoutMode : 'masonry',
			cellsByRow : {
				    columnWidth : 210,
				    rowHeight : 210
				  },
			itemSelector : '.widgetWrap',
			getSortData : {
				size : function( $elem ) {
					return $elem.width()+$elem.height();
				},
				configOrder : function( $elem ) {
					return parseInt($elem.attr('id').substr(6));
				}
			},
			sortBy : 'configOrder',
			sortAscending : 'asc'
		});
	},
	
	/**
	 * Register widget
	 * @param id internal name
	 * @param title full title, displayed on titlebar
	 * @param widget Widget object
	 */
	register: function(id, title, widget) {
		widget.id = id;
		widget.title = title;
		this.registeredWidgets[id] = widget;

		this.install(widget);
	},

	/**
	 * Install widget if it was enabled in configuration
	 */
	install: function(widget) {
		var widgetConfigs = Config.getNamespace('widgets');
		for (var id in widgetConfigs){
			if (widgetConfigs.hasOwnProperty(id) && widgetConfigs[id].id == widget.id) {
				var widget = WidgetManager.registeredWidgets[widgetConfigs[id].id];
				if (!widget) continue;

				var widgetInstance = jQuery.extend(true, {}, widget);
				widgetInstance._init(widgetConfigs[id].config, id);
				this.installedWidgets[id] = widgetInstance;
			}
		}

	},


	allWidgetsLoaded: function() {
		$('#widgetsWrap').isotope({ 
	          sortBy : 'configOrder',
	          sortAscending : 'asc'});
		$('#widgetsWrap').isotope( 'reLayout' );
	},
	
	/**
	 * Update measurements.
	 * Executes POST request to /update
	 */
	renderWidgets: function() {
		$.ajax({
			type: 'POST',
			url: '/update',
			data: '',
			dataType: 'text',
			success: function(data) {
				data = JSON.parse(data);
				if (Config.get('core', 'logging')=='DEBUG')
					console.log('dataUpdate', data);
				//var widgetsConfig = Config.getNamespace('widgets');
				for (var widgetId in data) {
					if (data.hasOwnProperty(widgetId)) {
						var widget = WidgetManager.installedWidgets[widgetId],
							widgetData = data[widgetId];
						// This widget might be not registred yet. :(
						if (!widget) {
							continue;
						}
						try {
							widget.render(widgetData);
						} catch (e) {
							widget.renderError();
							console.log(e.stack);
						}
					}
				}
			},
			error: function(jqXHR, textStatus, errorThrown) {
				console.log(jqXHR, textStatus, errorThrown);
			},
			complete: function() {
			}
		})
	}	
};


var Config = {
	config: {},
	save: function() {
		var cfg = this.config;
		$.ajax({
			type: 'POST',
			url: '/saveCfg',
			data: JSON.stringify(cfg),
			dataType: 'text',
			success: function(data) {
				console.log(data);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				console.log(jqXHR, textStatus, errorThrown);
			},
			complete: function() {
			}
		})
	},
	load: function(config){
		this.config = config;
	},
	set: function(namespace, name, value) {
		if (!this.config[namespace])
			this.config[namespace] = {};
		this.config[namespace][name] = value;
		this.save();
	},
	get: function(namespace, name, defaultVal) {
		if (this.config[namespace] && this.config[namespace][name])
			return this.config[namespace][name];
		return defaultVal;
	},
	
	getNamespace: function(namespace, defaultVal) {
		return this.config[namespace] || defaultVal;
	},
	
	getWidget: function(id) {
		var ws = this.getNamespace('widgets');
		for (var i=0; i<ws.length; i++)
			if (ws[i].id == id)
				return ws[i];
		return null;
	}
};



var Widget = {
	id: "BaseWidget",
	instanceId: null,
	title: "Base",
	mainTpl: '',
	_$element: null,
	baseTemplate: function() {
		return '<div id="widget'+this.instanceId+'" class="'+
			this.id+'Wrap widgetWrap'+(this.classes?' '+this.classes:'')+'">'+
			'<h3>'+this.title+'</h3>'+
			'<div class="'+this.id+' widget"></div></div>';
	},
	config: {},
	_init: function(config, instanceId) {
		this.config = config;
		this.instanceId = instanceId;
		
		var newItem = $(this.baseTemplate());
		$('#widgetsWrap').isotope( 'insert', newItem );
		
		if (typeof this.mainTpl == 'string')
			this.$('.widget').html(this.mainTpl);
		else if (typeof this.mainTpl == 'function')
			this.$('.widget').html(this.mainTpl()); 
		
		if (Config.getNamespace('widgets').length == WidgetManager.installedWidgets.length)
			WidgetManager.allWidgetsLoaded();
		
		this.init();
        $('#widgetsWrap').isotope( 'reLayout');
	},
	init: function() {
		
	},
	$: function(selector) {
		if (!selector) {
			return this._$element;
		}
		if (!this._$element) {
			this._$element = $('#widget'+this.instanceId);
		}
		return this._$element.find(selector);
	},
    renderError: function() {
        this.$('.widget').html('failed to render widget')
    }
};


var U = {
	prettyFileSize: function(size) {
	    var units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
	    var i = 0;
	    while(size >= 1024) {
	        size /= 1024;
	        ++i;
	    }
	    return size.toFixed(1) + ' ' + units[i];
	},
	
	shortenPath: function(str, chars) {
		if (str.length <= chars)
			return str;
		var pos = str.lastIndexOf('/');
		var lastWordLen = str.length - pos;
		return str.substr(0,chars-3-lastWordLen)+'...'+str.substr(pos);
	}
};












function Graph(element, type) {
	this.element = $(element);
	this.type = type;
	this.data = [];
}

Graph.prototype.setData = function(data) {
	this.data = data
};

Graph.prototype.setTitle = function(title) {
	this.title = title
};

Graph.prototype.draw = function(data) {
    var r = Raphael(this.element);
    r.g.txtattr.font = "12px 'Fontin Sans', Fontin-Sans, sans-serif";
    
    if (this.title)
    	r.g.text(320, 100, this.title).attr({"font-size": 20});
    
    var graph = r.g.piechart(
    		this.element.width(), 
    		this.element.height(),
    		this.element.height()<this.element.width() ? this.element.height()/2-20 : this.element.height()/2-20,
    		this.data, {legend: this.legend, legendpos: "west"});
    
    graph.hover(function () {
        this.sector.stop();
        this.sector.scale(1.1, 1.1, this.cx, this.cy);
        if (this.label) {
            this.label[0].stop();
            this.label[0].scale(1.5);
            this.label[1].attr({"font-weight": 800});
        }
    }, function () {
        this.sector.animate({scale: [1, 1, this.cx, this.cy]}, 500, "bounce");
        if (this.label) {
            this.label[0].animate({scale: 1}, 500, "bounce");
            this.label[1].attr({"font-weight": 400});
        }
    });
};


