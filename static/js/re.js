$(document).ready(function(){
	$("#list01").show().addClass("hg");
	$("#list02").hide();
	$("#list03").hide();
	$("h2").eq(0).click(function(){
		$("#list01").toggle();
		$("#list01 li").addClass("hg");
	});
	$("h2").eq(1).click(function(){
		$("#list02").toggle();
		$("#list02 li").addClass("hg");
	});
	$("h2").eq(2).click(function(){
		$("#list03").toggle();
		$("#list03 li").addClass("hg");
	});

	//$(".pipei li").addClass("hg");
	$(".pipei li a").click(function(){
		$("#re").val($(this).attr("title"))
		return false;
	});
	$("#click").click(function(){
		if(!isExist())
			return false;
		document.getElementById("result").value="";
		var regex = buildRegex();
		var inputval=document.getElementById("textInput").value.match(regex);
		if(null==inputval||0==inputval.length){
			document.getElementById("result").value="没有匹配";
		}else{
			document.getElementById("result").value="匹配结果："+inputval;
		}
		return true;
	});
});
function isExist(){
	var  textInput=document.getElementById("textInput");
	if(textInput.value==null||textInput.value.length<1){
		textInput.focus();
		alert("请输入待匹配文字");
		return false;
	}
	var re=document.getElementById("re");
	if(re.value==null||re.value.length<1){
		re.focus();
		alert("请输入正则表达式");
	}
	return true;
}
function buildRegex(){
	//var op="";
	return new RegExp(document.getElementById("re").value);
}
