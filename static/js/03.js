var option,mychart,datas;
var data=[];
var num=[];
var valuearr=[];
var val=new Array();
var k=new Array();



function getData(){
$.ajax({
	 type : 'get',
	 url:'/db/abci?prmtv=dump+'+getCookie("cur_df")+'+with+200000',
	 //url:'03.json',
		cache : false,
		dataType : 'json',
		success:function(dataAll){
			var nameAll=dataAll.result;
			datas=JSON.parse(nameAll);
			var name=datas.columns;
			data=datas.data;
			//add by gjw on 20190210 将map转换成数组
			data = data.map(function dict2array(items){
				var a=[];
				for (var key in items){
					if(key !="index"){
						a.push(items[key]);
					}
				}
				return a;
			});
			num=datas.index;
			var str=[];
			for(var i=0;i<data.length;i++){
				var obj=data[i];//��ȡdata���ÿһ������
				str.push(obj[2]);//��ȡk������ֵ
			}  
			var n = []; 
			for(var i = 0; i < str.length; i++){
				if (n.indexOf(str[i]) == -1){
					n.push(str[i]);		
				}
			}//ȥ��kֵ���
		var o1=[];
		for(var i=0;i<n.length;i++){
			var x=n[i];
			var ss=[];
		 for(var k=0;k<data.length;k++){
			 var dar=data[k];
			if(x==dar[2]){
				var xx=[];
				xx.push(dar[0]);
				xx.push(dar[1]);
				ss.push(xx);
			}
		 }
		 var o={
				name:x,
				type:'scatter',
			    data:ss,
			    itemStyle:{
			    	normal:{
			    		label:{
			    			show:true,
			    			position:'top',
			    			formatter:function(params){
			    				var index;
			    				var x=params.value[0];
			    				var y=params.value[1];
			    				if(data.length<100){
			    				for(var i=0;i<data.length;i++){
			    					valuearr=data[i];
					        		   if(x==valuearr[0]&&y==valuearr[1]){			        		   
					        			   index=num[i];
					        			   return index;						        	 
					        		   }
			    				}
			    				}
			    			}
			    		}
			    	}
			    }
		 };
		 o1.push(o);
		}
		//console.info(o1);
	    option.series=o1;
	    option.xAxis[0].name=name[0];
		option.yAxis[0].name=name[1];
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
//			legend: {
//		        data:['series1'],
//		        itemWidth:4,
//		        itemHeight:4
//		    },
		    color:['orange','red','green','blue','pink',
		           '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                     '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                     '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0',
                     'orange','red','green','blue','pink'
                       ],
		    tooltip:{
	        	   trigger:'axis',
	        	   axisPointer:{
		   	            show:true,
		   	            type:'cross',
		   	            lineStyle: {
		   	                type:'dashed',
		   	                width:1
		   	            }
		   	        },
	        	   formatter:function (params){
		        	   //console.log(params);
		        	   var x=params.value[0];
		        	   var y=params.value[1];
		        	   var result="";
		        	   for(var i=0;i<data.length;i++){
		        		   valuearr=data[i];
		        		   var name=datas.columns;
		        		   if(x==valuearr[0]&&y==valuearr[1]){				        		   
		        			   result="index:"+num[i]+"</br>"+name[0]+":"+x+"</br>"+name[1]+":"+y;
		        			   return result;						        	 
		        		   }
		        	   }
	        	   }  
	            },
			 xAxis : [
			          {
			        	  type : 'value',
			        	  name:'',
			        	  splitLine:{show:false},
			        	  //splitNumber:10,
			        	  boundaryGap:{show:false}
			          }
			      ],
			      yAxis : [
			               {
			                   type : 'value',
			                   name:'',
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
	            	dataZoom : {show: true},
	                dataView : {show: true, readOnly: false},
	                restore : {show: true},  
	                saveAsImage:{show: true}
	            }  
	        },
	        grid:{borderWidth:0},
			calculable:true,
			series : []		
	};
	    getData();



