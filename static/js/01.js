var option,mychart;
var x=[];
var str=[];
var tl=[];
function getData(){
	 $.ajax({
		 type : 'get',
			//url:'http://192.168.1.101:8080/exec?prmtv=dump+h',
		 	url:'/db/abci?prmtv=dump+'+getCookie("cur_df")+'+with+100000',
		 	//url:'/exec?prmtv=dump+maxm_24+with+20000',
		 	//url:'03.json',
			cache : false,
			dataType : 'json',
			success:function(dataAll){
				//console.info(dataAll);
				//var str=[];
				var nameAll=dataAll.result;
				var datas=JSON.parse(nameAll);
				var name=datas.columns;
				
				//console.info(name)
				var data=datas.data;
				//var x=[];
				 x=datas.index;
				//console.info(x)
				var val = [];
				var legend=[];
				for(var i=0;i<name.length;i++){
					var value=[];
					for(var j=0;j<data.length;j++){
						var valueAll=data[j];
						value.push(valueAll[name[i]]);							
					}
					var o={
							name:name[i],
							type:'line',
							data:value,
							markPoint : {
				                data : [
				                    {type : 'max', name: '最大值'},
				                    {type : 'min', name: '最小值'}
				                ]
				            },
				            markLine : {
				                data : [
				                    {type : 'average', name: '平均值'}
				                ]
				            }
							
					};
					str.push(o);
					tl.push(name[i]);
				}
					 //console.info(str);
					 //console.info(legend);
					 option.xAxis[0].data=x;
					 option.legend.data=tl;
					 option.series=str;
					 mychart.setOption(option,true);
					 mychart.refresh();
			},
			error:function(XMLHttpRequest,message){
				console.log(message)
			}
	
 });
};


		mychart=echarts.init(document.getElementById("main"));
	    option={
			title:{
				text:getCookie("cur_df")
				//x:'center'
			},
			legend: {
		        data:[]
		    },
			tooltip:{
				trigger:'axis',
				//formatter: "{a} <br/>{b} : {c} ({d}%)" ,
			},
			axisLabel : { 
	            show:true, 
	            interval: 'auto',    // {number} 
	        }, 
			 xAxis : [
			          {

			        	  type : 'category',
			          	  name:'',
			          	  splitLine:{show:false},
			          	  axisLine:{show:true},
			                'axisLabel':{'interval':0},
			                data:[]
			          }
			      ],
			      yAxis : [
			               {
			                   type : 'value',
			                   axisLine:{show:false},
			                   splitLine:{show:true,			                	   
				                   lineStyle: {
				                	    type: 'dashed'
				                	} }
			               }
			           ],
			toolbox:{
				show : true,  
	            feature : {
	            	mark : {show: true},  
	                dataView : {show: true, readOnly: false},
	                magicType : {show: true, type: ['line', 'bar','stack']},
	                restore : {show: true},  
	                saveAsImage : {show: true}
	            }  
	        },
	        grid:{borderWidth:0},
			calculable:true,
			series:[]	
	}
	    getData();


	
	

