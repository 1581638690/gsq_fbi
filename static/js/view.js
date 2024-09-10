$(document).ready(function (){	
	$('.tag:eq(0)').hide();
	//$('#select1 > li:eq(0)').addClass("btn-success");
	//选项卡导航
    $('#select1 > li').click(function(){
    	var allLi = $('#select1 > li').removeClass("btn-success");//将所有选项卡变为浅色，并让allLi表示为所有的选项卡；
    	$(this).addClass('btn-success');
    	var index = allLi.index(this);//找出点击中的选项卡处于队列中的第几个；
    	$('.tag:visible').hide();//让其他的选项卡内容隐藏；
    	draw(index);
    	$('.tag:eq('+index+')').show();//显示被点中的选项卡内容；

    });
   
	var vData="";
	function draw(index){
		console.info(index);
		if (index==1){ //json 展示
			
			var options = {
				dom : '#JSON' //对应容器的css选择器
				};
			var jf = new JsonFormater(options); //创建对象
			jf.doFormat(vData); //格式化json//当页面载入时，自动运行以下代码；
		}
		if (index==2){
			draw2(vData);
		}
		if (index==3){
			draw3(vData);
		}
		//add by gjw on 20180505 画表格
		if (index==4){  
			draw_table(vData);
		}	
	}

  //回车查询
	$("#select_id").keypress(function(e){  
		
		if (e.which == 13){
		 $("#chaxun").click();
	   }       
		
	 });
	
    //获取JSON
    $('#chaxun').click(function(){
    	$('#select1 > li').removeClass("btn-success");
    	$('.tag:visible').hide();
    	$.ajax({
    		type : 'get',
    		url:'/db/query/ssdb0',
    		data:{"key":$('#select_id').val().trim()},
    		cache : false,
    		dataType : 'json',
    		success:function(data){
    			if(data!=""){
					vData = data;
					$('#raw').text(JSON.stringify(data));
					draw(4);
					$('.tag:eq(4)').show();
						$('#select1 > li:eq(4)').addClass("btn-success")
					}
    			else{alert("数据不存在")}
    		} 
     	});
    });
	
	//初始化图表
	var datas;
	var data=[];
	var num=[];
	var name=[];
	var valuearr=[];
	var val=new Array();
	var k=new Array();

	var oneoption = {
		title : {
			text: ''
		},
		tooltip : {
			trigger: 'axis'
			//formatter:'{b} :{c} 万'
		},
		legend: {
			data:[]
		},
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
		calculable : true,
		xAxis : [
			{   
			type : 'category',
			name:'',
			splitLine:{show:false},
			axisLine:{show:true},
				'axisLabel':{'interval':0}
				//data : ['xit']
				
			}
		],
		yAxis : [
			{
				type : 'value'
				//name:'数量(万)'
			}
		],
		series : []
	};

	var oneChart = echarts.init(document.getElementById("bar"));
	oneChart.setOption(oneoption);
	oneChart.showLoading({
			text : '数据获取中',
			effect : 'whirling'
		});
	
	var threeoption={
			title:{
				text:''
				//x:'center'
			},
			
		    color:['rgb(193,35,43)','orange','green','blue','pink',
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
		        		   //var name=datas.columns;
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
			        	  axisLine:{show:true},
			        	  data:[]
			        	  //splitNumber:10
			        	  //boundaryGap:{show:false}
			          }
			      ],
			      yAxis : [
			               {
			                   type : 'value',
			                   name:'',
			                   axisLine:{show:false},
			                   splitLine:{show:true}
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
	var threeChart =　echarts.init(document.getElementById("scatter"));
	threeChart.setOption(threeoption);
	threeChart.showLoading({
			text : '数据获取中',
			effect : 'whirling'
	});

	////将所有的选项卡内容隐藏;
	$('.tag:gt(0)').hide();	


function draw2(datas){
	    	oneChart.hideLoading();
	    	var x=[];
	    	var str=[];
	    	var tl=[];
			var name=datas.columns;
			var data=datas.data;//��ȡdata
			 x=datas.index;
			var val = [];
			var legend=[];
				for(var i=0;i<name.length;i++){
					var value=[];
					for(var j=0;j<data.length;j++){
						var valueAll=data[j];
						value.push(valueAll[i]);							
					};
				var o={
						name:name[i],
						type:'bar',
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
			}
				oneoption.xAxis[0].data=x;
				oneoption.series=str;
				oneChart.setOption(oneoption,true);
				//oneChart.refresh();
				//oneChart.restore();
	}

	function draw3(datas){
				threeChart.hideLoading();
				//var nameAll=dataAll.result;
				//datas=JSON.parse(nameAll);
				name=datas.columns;
				data=datas.data;
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
				    markPoint : {
		                data : [
		                    {type : 'max', name: '最大值'},
		                    {type : 'min', name: '最小值'}
		                ]
		            },
			 };
			 o1.push(o);
			}
			//console.info(o1);
		    threeoption.series=o1;
		    threeoption.xAxis[0].name=name[0];
			threeoption.yAxis[0].name=name[1];
			threeChart.setOption(threeoption,true);
			//threeChart.refresh();
			//threeChart.restore();
	}

//add by gjw on 20180505 用jqGrid展示数据
	function draw_table(result){
		$("#d_12").html("<table id='df_12'></table>");
		var config={ datatype: "local", height:600, autowidth:true,rowNum:1000,scroll:true}; 
			config.colNames=[];
			config.colModel=[]
			
			//var result = JSON.parse(result);
			var i=1;
			var sort_type="text";
			config.colNames[0] = "Index";
			if (typeof(result.index[0])=="number")
			{
				sort_type="int";
			}
			config.colModel[0] = {name:"index",index:"index",width:100,sorttype:sort_type};   
			if ("columns" in result) {
				var len = result.columns.length;
				
				for (key in result.columns){
					config.colNames[i] = result.columns[key];
					sort_type="text";
					if (result.data.length >0 && typeof(result.data[0][key])=="number")
					{
						sort_type="int";
					}
					config.colModel[i] = {name:result.columns[key],index:result.columns[key],sorttype:sort_type};
					
					i++;
				}
			}else{ //not a df
				config.colNames[i] = result.name;
				config.colModel[i] = {name:result.name,index:result.name,width:600};
				i++;
			}
			config.colNames[i] = "@";
			config.colModel[i] = {name:"",index:"",width:20};
		var data=[];
		for(var i=0;i<result.data.length;i++){
		
			var rawdata={};
			rawdata["index"] = "<xmp>"+result.index[i]+"</xmp>";
			
			if ("name" in result){
				rawdata[result.name] = "<xmp>"+result.data[i]+"</xmp>";
			}else{						
				for (key in result.columns){
					rawdata[result.columns[key]] = "<xmp>"+result.data[i][key]+"</xmp>";							
				}
			}
			data.push(rawdata);
		}
		config.data = data;
		jQuery("#df_12").jqGrid(config);
		
	}//end function draw_table

	
//code end
});

