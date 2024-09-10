$(document).ready(function (){

	$("#title").text(getCookie("cur_df"));

	$.getJSON('/db/abci?prmtv=dump+'+getCookie("cur_df")+'+with+50',
	function(dataAll){
		var results=dataAll.result;
		var ret=dataAll.ret;			
		var result=JSON.parse(results);

		data=result.data;
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
		var index=result.index;	
		var myCol=result.columns;//获取列名
		var myCol2=[];
		for (var i = 0; i < myCol.length; i++) {
			var a=myCol[i].toString();
			myCol2.push(a);
			//console.info(typeof(myCol2[i]));
		}
		
		//console.info(myCol);
		//讲index添加到列名中
		//unshift：将参数添加到原数组开头，并返回数组的长度
		var b = myCol2.unshift("index"); // b为新数组的长度，myCol除了原来的对象，增加里index
		//console.info(myCol); 
		myColArrs=[];
		dataArr=[];			
		//console.info(myCol2);
			for(var i=0;i<myCol2.length;i++){
				
				//console.info(typeof(myCol2[i]));
				myColArrs.push({"title":myCol2[i]})
			}
			for (var i = 0; i < data.length; i++) {
			var b=data[i].unshift(index[i]);
			dataArr.push(data[i]);
			}
			//console.info(myColArrs);
			//console.info(dataArr);
		

		//console.info(myColArrs);
		insertDataToTable();
	});

	var language={
		"lengthMenu" : "显示 _MENU_ 项结果",
		"info" : "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
		"infoEmpty" : "显示第 0 至 0 项结果，共 0 项",
		"emptyTable" : "表中数据为空",
		"loadingRecords" : "载入中..."
	};
	function insertDataToTable(){
		table=$("#data").DataTable({
			columns : myColArrs,
			data:dataArr,
			language:language,
			ordering:false,
			info:false,
			paging:false,
			searching:false,
			scrollY:480
		});
	};
	/*$('.dataTables_scrollHead thead tr').first().before("<tr>new</tr>");*/
	/*$("body").on("mouseover","td",function(){		
		var colIdx=table.cell(this).index().column;//这个单元格所在的列
		//console.info(colIdx);
		if(colIdx!==null){
			$(table.cells().nodes()).removeClass("highLight");
			$(table.column(colIdx).nodes()).addClass("highLight");
		}
	})
	.on("mouseleave",function(){
		$(table.cells().nodes()).removeClass("highLight");
	});*/

	/*$("body").on("click","li a",function(){
		alert();
		$(this).addClass("red");
	});*/
});
