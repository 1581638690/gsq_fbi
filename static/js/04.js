function getData(){
$.ajax({
	 type : 'get',
	 	url:'/db/abci?prmtv=dump+'+getCookie("cur_df")+'+with+20000',
	    //url:'03.json',
		cache : false,
		dataType : 'json',
		success:function(dataAll){
			var results=dataAll.result;
			var result=JSON.parse(results);
			var index=result.index;
			var str=[];
			var legendS=[];
			var dataEnd=[];
			var columns=result.columns;
			//console.info(columns);
			var dataArr=result.data;
						//add by gjw on 20190210 将map转换成数组
			dataArr = dataArr.map(function dict2array(items){
				var a=[];
				for (var key in items){
					if(key !="index"){
						a.push(items[key]);
					}
				}
				return a;
			});
			//console.info(dataArr);
			
			for(var i=0;i<columns.length;i++){
				if(i<2){
				var data=[];
				var dataEnd=[];
				var otherAll=0;
				//数据解析排序
				for(var j=0;j<dataArr.length;j++){
					var datas=dataArr[j];					
					//data.push(datas[i]);
					var value=datas[i];					
					var name=index[j];
					var arrAy={value:value,name:name};					
					dataEnd.push(arrAy);
					dataEnd.sort(function (a,b){
						return b.value-a.value;
					})
				}
				//分类
				var dataarr=[];
				var sum=0;
				var little=0;
				var ss=0;
				/*for(var k=0;k<dataEnd.length;k++){
				  if(k<10){
					  dataarr.push(dataEnd[k]);
				  }else{
					  ss+=dataEnd[k].value;
				  }
				  
				}
				var oo={
						name:'其他',
						value:ss
				}
				dataarr.push(oo);*/
				for(var k=0;k<dataEnd.length;k++){
					sum+=dataEnd[k].value;
				}
				//console.info(sum);
				for(var k=dataEnd.length-1;k>=0;k--){
					little+=dataEnd[k].value;
					if(little/sum>=0&&little/sum<=0.05){
						//dataarr.push(dataEnd[k]);
						ss+=dataEnd[k].value;												
					}else {						
						dataarr.push(dataEnd[k]);
						//ss+=dataEnd[k].value;
					}
				}
				//if(ss!=0){
					var oo={
						name:'其他',
						value:ss
					}
				
				//}
				dataarr.sort(function (a,b){
					return b.value-a.value;
				})
				if(oo.value!=0){
					dataarr.push(oo)
				}
				console.info(dataarr);
				//圆心
				var center;				
				if(columns.length==1){
					center=['50%','60%'];
					
				}else if(columns.length>=2){
					center=[((i*50)+25)+'%','60%'];
				}
							
				var o={
					name:columns[i],
					type:'pie',
					radius:'55%',
					center:center,
					//clockWise:false, 
					data:dataarr
				};
				//图例
				
				for(var k=0;k<dataarr.length;k++){
					if(dataarr[k].value!=0){
						var legend=dataarr[k].name;					
						//legendS.push(legend);
						if (legendS.indexOf(legend) == -1){
							legendS.push(legend);	
						}
					}

				}	
					str.push(o);
																
			}
			//console.info(dataEnd)
			//console.info(str);
			option.series=str;
			option.legend.data=legendS;
			mychart.setOption(option,true);
			mychart.refresh();
		}},
		error:function(XMLHttpRequest,message){
			console.log(message)
		}

});
};
		mychart=echarts.init(document.getElementById("main"));
		option = {
			    title : {
			        text:getCookie("cur_df"),
			        x:'center'
			    },
			    tooltip : {
			        trigger: 'item',
			        formatter: "{a} <br/>{b} : {c} ({d}%)"
			    },
			    legend: {
			        //orient : 'vertical',
			        x : 'center',
			        y:'12%',
			        data:[]
			    },
			    toolbox: {
			        show : true,
			        feature : {
			            mark : {show: true},
			            dataView : {show: true, readOnly: false},
			            restore : {show: true},
			            saveAsImage : {show: true}
			        }
			    },
			    calculable : true,
			    series :[]
			};
	    getData();



