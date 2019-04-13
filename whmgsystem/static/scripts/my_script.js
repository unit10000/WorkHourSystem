
function set_bottom(){

    var a = $(document.body).height()
    var b = $(window).height()
    var css= ''
    if (a>b){
        css="navbar-static-bottom"


    }else{
        css="navbar-fixed-bottom"
        var nav_height = $('#my_bottom').height()+10
        $(document.body).css("padding-bottom",nav_height+"px");
    }
    $("#my_bottom").addClass(css); // 追加样式
}
function set_body(){
    var nav_height = $('#nav_top').height()+20
    $(document.body).css("padding-top",nav_height+"px");

}
function getNow(s) {
    return s < 10 ? '0' + s: s;
}
function get_nowtime(){
    var myDate = new Date();
    //获取当前年
    var year=myDate.getFullYear();
    //获取当前月
    var month=myDate.getMonth()+1;
    //获取当前日
    var date=myDate.getDate();
    var now=year+'-'+getNow(month)+"-"+getNow(date)
    return now
}
function is_IE(){

if (window.ActiveXObject || "ActiveXObject" in window){
        alert("ie")
    }else{
        alert("not ie")
    }
}
String.prototype.myReplace=function(f,e){//吧f替换成e
    var reg=new RegExp(f,"g"); //创建正则RegExp对象
    return this.replace(reg,e);
}
setTimeout("set_bottom()",0);
set_body()