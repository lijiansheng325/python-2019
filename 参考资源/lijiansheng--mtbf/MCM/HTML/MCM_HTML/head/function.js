function isHasElementOne(arr,value){  
    for(var i = 0,vlen = arr.length; i < vlen; i++){  
        if(arr[i] == value){  
            return i;  
        }  
    }  
    return -1;  
}

function isHasElementTwo(arr,value){
	var str = arr.toString();
	var index = str.indexOf(value);
	if(index >= 0){
		//存在返回索引
		var reg1 = new RegExp("((^|,)"+value+"(,|$))","gi");
		return str.replace(reg1,"$2@$3").replace(/[^,@]/g,"").indexOf("@");
	}else{
		return -1;//不存在此项
	}
}

function isHasElementIn(a,b,c){
	var tmp = isHasElementTwo(a,b)
	if(tmp == -1){
		return 'Null';
	}else{
		return c[tmp];
	}
}

function isArray(obj) {   
return Object.prototype.toString.call(obj) === '[object Array]';    
}

//Highcharts
//设置到默认皮肤
function ResetOptions() {
	//删除所有属性 然后在给予默认皮肤
	var defaultOptions = Highcharts.getOptions();
	for (var prop in defaultOptions) {
		if (typeof defaultOptions[prop] !== 'function') delete defaultOptions[prop];
	}
}