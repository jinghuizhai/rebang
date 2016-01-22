/**
 * zjhlib-1.0.js simple JavaScript library for private use
 * ---------------------------------------------
 * 2015-03-01	Version: 1.0
 */
if(!''.trim){
	String.prototype.trim = function(){
		return this.replace(/^\s+|\s+$/g,'');
	};
}
if(![].forEach){
	Array.prototype.forEach = function(fn){
		var that = this;
		for(var i = 0,len = that.length;i<len;i++){
			fn.call(null,that[i],i);
		}
	};
}
(function(window,undefined){

	var z = {},fnarr = [];

	z._body = document.body;
	z._html = document.documentElement;

	z.get = function(el,context){
		if(typeof context == 'undefined') context = document;
		return typeof el === 'string' ? context.getElementById(el):el;
	};

	z._callFnarr = function(args){
		for(var i = 0,len = args.length;i<len;i++){
			args[i].call();
		}
	};

	z._ready = function(){
		if(document.addEventListener){
			document.addEventListener('DOMContentLoaded',function(){
				z._callFnarr(fnarr);
			});
		}else if(document.documentElement.doScroll){
			void function(){
				try{
					z._html.doScroll('left');
					z._callFnarr(fnarr);
				}catch(e){
					setTimeout(arguments.callee,0);
				}
			}();
		}
	};

	z.ready = function(fn){
		fnarr.push(fn);
	};

	z.browser = function(){
		var str = window.navigator.userAgent.toLowerCase(),
			tag = '',
			version = 0;

		var ie = str.match(/rv:(\d+)/);
		if(ie) return ['ie',ie[1]];

		ie = str.match(/msie\s?(\d+)/);
		if(ie) return ['ie',ie[1]];

		var firefox = str.match(/firefox\/(\d+)/);
		if(firefox) return ['firefox',firefox[1]];

		var opera = str.match(/opr\/(\d+)/);
		if(opera) return ['opera',opera[1]];

		if(str.indexOf('iphone') > 0) return ['iphone'];
		if(str.indexOf('ipad') > 0) return ['ipad'];
		if(str.indexOf('android') > 0) return ['android'];

		var chrome = str.match(/chrome\/(\d+)/);
		if(chrome) return ['chrome',chrome[1]];

		return str;
	};
	//表单验证
	z.validate = function(demo,str){
		switch(demo){
			case 'pass':
				return /^[a-zA-Z0-9_#%$@.]{8,20}$/.test(str);
			case 'phone':
				return /^1[34578]\d{9}$/.test(str);
			case 'email':
				return /^[\da-zA-Z_]{5,}@[a-z\d]+\.(com|cn|net)$/.test(str);
			default:
				return false;
		}
	};
	//浏览器可视区域高度
	z.getViewport = function(){
		return {
			width:document.documentElement.clientWidth,
			height:document.documentElement.clientHeight
		}
	};
	//带borderWidth的文档高度，不包含与box周围的距离
	z.getPagearea = function(){
		//带borderWidth,不带borderWidth是document.body.clientHeight;
		return {
			height:document.documentElement.offsetHeight,
			width:document.documentElement.offsetWidth
		};
	};

	z.screen = function(){
		return {
			height:window.screen.height,
			width:window.screen.width
		};
	};

	z.css = function(el,attr,value){
		if(z.isobj(attr)){
			for(at in attr){
				z.css(el,at,attr[at]);
			}
		}else if(typeof value != 'undefined'){
			el.style[attr] = value;
		}else{
			var style = el.currentStyle ? el.currentStyle : window.getComputedStyle(el);
			if(style.getPropertyValue){
			    return style.getPropertyValue(attr);
			}else{
			    return style.getAttribute(attr);
			}
		}
	};

	z.nth = function(ele,index){
		var lists = ele.childNodes,
			elements = [];
		for(var i = 0,len = lists.length;i<len;i++){
			if(lists[i].nodeType == 1){
				elements.push(lists[i]);
			}
		}
		if(index < 0) index = elements.length+index;
		if(index < 0 || index >= elements.length) return null;
		return elements[index];
	};
	z.first = function(ele){
		return z.nth(ele,0);
	};
	z.last = function(ele){
		return z.nth(ele,-1);
	};
	z.prev = function(ele){
		var pre = ele.previousSibling;
		if(pre && pre.nodeType == 1){
			return pre;
		}else if(pre && pre.nodeType == 3){
			return z.prev(pre);
		}else{
			return null;
		}
	};
	z.next = function(ele){
		var next = ele.nextSibling;
		if(next && next.nodeType == 1){
			return next;
		}else if(next && next.nodeType == 3){
			return z.next(next);
		}else{
			return null;
		}
	};
	z.animate = function(el,attr,fn,val){
	    var arg = arguments;
	    if(z.isobj(attr)){
	       var keyarr = [];
	       for(key in attr){
	       	  keyarr.push(key);
	       }
	       for(key in attr){
	       	 if(keyarr.slice(-1) == key){
	       	 	arg.callee(el,key,fn,attr[key]);
	       	 }else{
	       	 	arg.callee(el,key,null,attr[key]);
	       	 }
	       }
	    }else{
	        el = z.get(el);
	        attr = attr.replace(/([A-Z])/g,'-$1').toLowerCase();
	        target = parseInt(val);

	        var original = parseInt(z.css(el,attr)),
	          far      = target-original,
	          step     = far/20,
	          now      = 0;
	        //单位 px,em .etc
	        var suffix = val.match(/[a-z]+$/i);
	        suffix === null ? 0 : suffix[0];

	        void function(){
	           if(Math.abs(far)-Math.abs(step) <= Math.abs(now)){
	              el.style[attr] = target+suffix;
	              if(z.isfn(fn)) fn.call();
	           }else{
	              el.style[attr] = original+now+suffix;
	              now = now+step;
	              setTimeout(arguments.callee,10);
	           }
	        }();
	    }
	};

	z.hasClass = function(el,clazz){
		if(z.isstr(el)) el = z.get(el);
		if(el.length) el = el[0];
		if((' '+el.className+' ').match(' '+clazz+' ')) return true;
		return false;
	};

	z.addClass = function(el,clazz){
		if(z.isstr(el)) el = z.get(el);
		if(el.length){
			for(var i = 0,len = el.length;i<len;i++){
				z.addClass(el[i],clazz);
			}
		}else{
			var className = el.className.trim();
			if(className) el.className = className+" "+clazz;
			else el.className = clazz;
		}
	};

	z.removeClass = function(el,clazz){
		if(z.isstr(el)) el = z.get(el);
		if(el.length){
			for(var i = 0,len = el.length;i<len;i++){
				z.removeClass(el[i],clazz);
			}
		}else{
			if(z.hasClass(el,clazz)){
				el.className = (' '+el.className+' ').replace(' '+clazz+' ',' ').trim();
			}
		}
	};

	z.toggleClass = function(el,clazz){
		if(z.hasClass(el,clazz)){
			z.removeClass(el,clazz);
		}else{
			z.addClass(el,clazz);
		}
	};

	z.toggle = function(el){
		if(z.css(el,'display') == 'none'){
			z.show(el);
		}else{
			z.hide(el);
		}
	};

	/*没有将html的内容trim，考虑到故意传入空格的情况*/
	z.html = function(el,html){
		if(typeof html == 'undefined'){
			if(el.innerText) return el.innerText;
			return el.textContent;
		}else{
			if(el.innerText) el.innerText = html;
			else el.textContent = html;
		}
	};
	/*
	在同一个ele上绑定相同事件的不同动作的需求较少，所以相同动作只绑定一个函数，如果相同事件绑定不同函数，会覆盖之前的绑定
	若有以上需求，思路是将ele赋值随机的id，根据id缓存函数，然后按顺序执行
	*/
	z.addEvent = function(el,type,fn){
		el = z.get(el);
		if(el.attachEvent){
	    	el.attachEvent('on'+type,fn);
		}else{
		    el.addEventListener(type,fn,false);
		}
	};

	z.removeEvent = function(el,type,fn){
		el = z.get(el);
		if(el.detachEvent){
		    el.detachEvent('on'+type,fn);
		}else{
		    el.removeEventListener(type,fn,false);
		}
	};

	//文档滚动到指定位置
	z.scrollTo = function(position,rate){

		var toz = document.documentElement.scrollTop || document.body.scrollTop,
			target = position ? position === 'top' ? 0 : position === 'bottom' ? document.body.scrollHeight : parseInt(position) : 0,
			far = target - toz,
			now = 0,
			setId,
			step = far/(rate ? parseInt(rate) : 20);

		// console.log(toz,target,far,now,step);
		void function(){
			if(step === 0) return;
			if(far <= 0 ? toz + now <= target : target-now <= step){
				window.scrollTo(0,target);
				// console.log('target',target);
			}else{
				window.scrollTo(0,toz+now);
				now = now + step;
				// console.log(toz+now,target-now);
				setId = setTimeout(arguments.callee,10);
			}
		}();

	};
	z.isfn = function(fn){
		return Object.prototype.toString.call(fn) === '[object Function]';
	};
	z.isarr = function(array){
		return Object.prototype.toString.call(array) === '[object Array]';
	};
	z.isobj = function(object){
		return Object.prototype.toString.call(object) === '[object Object]';
	};
	z.isstr = function(str){
		return Object.prototype.toString.call(str) === '[object String]';
	};
	z.hide = function(ele){
		z.css(ele,'display','none');
	};
	z.show = function(ele){
		z.css(ele,'display','block');
	};
	z.showi = function(ele){
		z.css(ele,'display','inline-block');
		var ie678 = !+"\v1" ;//include IE5
		if(ie678){
			z.css(ele,'display','inline');
			z.css(ele,'zoom','1');
		}
	}
	z.ajax = function(method,url,params,fn,async){

        async = typeof async === "undefined" ? true:async;
        method = method.toUpperCase();

        var xmlhttp,
        	param = '';

        if(window.XMLHttpRequest){
            xmlhttp = new XMLHttpRequest();
        }else{
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange = function(){
            if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
                if(typeof fn === "function") fn(xmlhttp.responseText);
            }
        };
        for(p in params){
        	param = param + "&" + p + "=" + params[p];
        }
       	param = param.slice(1)+"&random="+Math.random();

       	if(method === "GET"){
       		xmlhttp.open(method,url+"?"+param,async);
       		xmlhttp.send();
       	}else if(method === "POST"){
       		xmlhttp.open(method,url,async);
       		xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
       		xmlhttp.send(param);
       	}else{
       		if(window.console) console.log('unknow method '+method);
       		return false;
       	}
    };

    z.setCookie = function(c_name,value,expiredays){
    	var exdate = new Date();
　　　　exdate.setDate(exdate.getDate() + expiredays);
　　　　document.cookie = c_name+ "=" + escape(value) + ((expiredays==null) ? "" : ";expires="+exdate.toGMTString())+";path=/";
    };
    z.getCookie = function(name){
    	if(!name){
    		return document.cookie ? document.cookie : '';
    	}else{
    		var exp = new RegExp(name+'\s*=([^;]+)');
    		var ret = z.getCookie().match(exp);
    		if(ret){
    			return unescape(ret[1]);
    		}else{
    			return '';
    		}
    	}
    };
    z.GET = function(url,params,fn,async){
    	z.ajax('GET',url,params,fn,async);
    };
    z.POST = function(url,params,fn,async){
    	z.ajax("POST",url,params,fn,async);
    };
    //dom ready后添加监听
    if(fnarr){
    	z._ready();
    }
    /*
    * z可以复制给任意的全局对象
    * 按照自己的喜好修改，如
    * window.ed = z or window.$ = z
    * 或者修改成自己名字的简写，在此基础上增加自己需要的方法
    */
	window.z = z;
})(window);