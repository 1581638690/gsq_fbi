var option,mychart;
var x=[];
var str=[];
var tl=[];
var value = [];
var once=true;

function getData(){
	var ws=null;
		var ip_addr = document.location.hostname;
		var mq_topic = getCookie("cur_df");
		var url = "ws://"+ip_addr+"/ws/"+mq_topic;
		
		if (ws !=null && ws.url !=url){
			ws.close();
			ws =null;
		}
		
		if (ws==null){
			ws = new WebSocket(url);
			/*
			ws.onopen = function() {
				ws.send(mq_topic);
			};
			*/
			ws.onmessage = function (evt) {
				//console.log(evt.data);
				update(evt.data);
				
			};
			ws.onclose = function(){
				//alert("Connection is closed");
				ws=null;
			};
			ws.error = function()
			{
				//alert("Error Happended");
				ws.close();
				ws=null;
			};
 
		}//end if

}	
	
	
function doPaint(){
	for(var j=0;j<50;j++){
		value.push(0);							
	}
	for(var j=0;j<50;j++){
		x.push(j);							
	}
	var o={
			type:'line',
			smooth:true,
			data:value
	};
	str.push(o);
	option.xAxis.data=x;
	option.legend.data=tl;
	option.series=str;
	mychart.setOption(option,true);
	//mychart.refresh();
}
			

function update(raw_data){
	var datas=JSON.parse(raw_data);
	var name=datas.columns;
	var data=datas.data;
	for (var i=0; i< datas.index.length;i++){
		x.shift();
		x.push(datas.index[i]);
	}

	for(var i=0;i<name.length;i++){
		for(var j=0;j<data.length;j++){
			var valueAll=data[j];
			value.shift();
			value.push(valueAll[i]);							
		}
		var o={
				showSymbol: false,
				hoverAnimation: false,
				smooth:true,
				stack: 'a',
				areaStyle: {
					normal: {}
				},
				type:'line',
				data:value
				
		};
		//str.push(o);
	}//end for
	option.xAxis.data=x;
	option.series=o;
	mychart.setOption(option,true);
}


mychart=echarts.init(document.getElementById("main"));
option={
	title:{
		text:getCookie("cur_df")
	},
	legend: {
		data:[]
	},
	axisLabel : { 
		show:true, 
		interval: 'auto',    // {number} 
	}, 
	xAxis : {

				  type : 'category',
				  name:'',
				  splitLine:{show:false},
				  axisLine:{show:true},
					'axisLabel':{'interval':0},
					data:[]
			  },
	yAxis :	{
			   type : 'value',
			   axisLine:{show:false},
			   splitLine:{show:true,			                	   
				   lineStyle: {
						type: 'dashed'
					} }
	},
	grid:{borderWidth:0},
	calculable:true,
	series:[]	
}

doPaint();

getData();




	
	

