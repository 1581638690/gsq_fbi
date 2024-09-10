//gjw on 20160106
// 对Date的扩展，将 Date 转化为指定格式的String
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符， 
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字) 
// 例子： 
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423 
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18 
Date.prototype.Format = function (fmt) { //author: meizz 
	var o = {
		"M+": this.getMonth() + 1, //月份 
		"d+": this.getDate(), //日 
		"h+": this.getHours(), //小时 
		"m+": this.getMinutes(), //分 
		"s+": this.getSeconds(), //秒 
		"q+": Math.floor((this.getMonth() + 3) / 3), //季度 
		"S": this.getMilliseconds() //毫秒 
	};
	if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
	for (var k in o)
	if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
	return fmt;
}


function getCookie(c_name)
{
	console.info(document.cookie);
	if (document.cookie.length>0)
	  {
	  c_start=document.cookie.indexOf(c_name + "=")
	  if (c_start!=-1)
		{ 
		c_start=c_start + c_name.length+1 
		c_end=document.cookie.indexOf(";",c_start)
		if (c_end==-1) c_end=document.cookie.length
		return unescape(document.cookie.substring(c_start,c_end))
		} 
	  }
	return "";
}


 //foreach参数构建
 function param_build(foreach_map,ps){

	var param = foreach_map.param;
	var param2 = [];
	if (param.indexOf('(')==0) { param=param.slice(1,param.length-1)}

	var arr1 = param.split(",");
	  for (var i=0;i<arr1.length;i++){
		var kv = arr1[i].split("=");
		if(kv.length <2)continue;
		//add by gjw on 202200512 两个都为空则去除
		if (kv[0].trim()=="" && kv[1].trim()=="")continue;
		//取每行的值，第x列的值
		v = kv[1].trim();
		v = v.slice(1,v.length);
		v = parseInt(v)
		var value;
		if (v ==0){
			value = foreach_map.index[foreach_map.i];
		}else{
			value = foreach_map.data[foreach_map.i][v-1];
		}
		
		if (kv[0].indexOf("@")==0){
			ps.set(kv[0].trim(),value);
			param2.push(kv[0].trim().slice(1,kv[0].trim().length)+"="+value);
		}else{
			ps.set("@"+kv[0].trim(),value);
			param2.push(kv[0].trim()+"="+value);
		}	
	 }
	 foreach_map.param2 = param2.join(",");
	 //排序
	var arrayps = Array.from(ps);
	arrayps.sort(function(a,b){return b[0].length -a[0].length});
	ps = new Map(arrayps.map(i => [i[0], i[1]]));
	console.info(ps);
	return ps;
 }