$(".work_hour").click(function(){
    if ( $(this).children("input").length > 0 ){//当前元素正在编辑返回
            return
        }
        var val = $(this).text()
        $(this).attr("old_html",val)
        $(this).html('<input class="edit_input" autofocus="autofocus" type="text"  style="border: 0px solid #ddd;margin:0px 0px; width:100%; height:100%;text-align:center" value="'+val+'" />')
        $(".edit_input").focus()
        $(".edit_input").blur(function(){
            var val = $(this).val()
            var out_obj = $(this).parent()
            var obj = $(this).parent().parent()
            val = val.replace(/\s+/g, "");
            var ival = parseFloat(val)
            if(val==''){
                if (out_obj.attr("old_html")!='')
                delete_workHours(out_obj)
                $(this).prop("outerHTML",'')
                up_sumColumnWorkHour(obj)
                up_rowSumWorkHour()
                return
            }
            if(isNaN(ival)){
                $(this).prop("outerHTML",'')
               alert(val +"不是数字,请输入数字");
               return
            }


            $(this).prop("outerHTML",ival)
            up_sumColumnWorkHour(obj)
            up_rowSumWorkHour()
            up_workHours(out_obj,ival)
        });


})
function up_rowSumWorkHour(){
    tbodyObj= work_hour_obj.parent().parent()//获取tbody
    for (var i = 0 ; i<work_hour_obj.length ; i++){//循环所有行，获取到的td是显示的2倍不知道原因
          obj = work_hour_obj.eq(i)//获取第n个合计td
          trObj = obj.parent()//获取该td所在tr
          column_index = trObj.children().index(obj)//获取需要统计的列索引
          row_index = tbodyObj.children().index(trObj)//获取需要统计的行索引
          sum = 0 //初始化合计
          for (var row =1 ;row < row_index ; row++){//遍历所有列
                num = tbodyObj.children().eq(row).children().eq(column_index).html()
                if(num=='')continue;
                sum += parseFloat(num)
          }
          obj.html(sum)
//          var a = l.length/2
//          l.eq(i+a).html(sum) //不知道为什么需要设置第二份td才能正确显示
//          l.eq(i).html()
    }
}
function up_sumColumnWorkHour(obj){

    out_obj = $(".sumColumnWorkHour")
    work_hours = obj.find(".work_hour")
    sum = 0
    row_index = obj.parent().children().index(obj)
    for (var i = 0 ; i < work_hours.length ; i++){
        num = work_hours.eq(i).html()
        if(num=='')continue;
        sum += parseFloat(num)
    }
    out_obj.eq(row_index-1).html(sum)

}
function up_workHours(obj,value){
    project_id = get_projectID(obj)
    date = get_workHoursDate(obj)
    ajax_upWorkHours(project_id,date,value)
}
function delete_workHours(obj){
    project_id = get_projectID(obj)
    date = get_workHoursDate(obj)
    ajax_deleteWorkHours(project_id,date)
}
function get_projectID(obj){
    return obj.parent().attr("project_id")
}
function get_workHoursDate(obj){
    column_index = obj.parent().children().index(obj)
    date = $("#my_tr").children().eq(column_index).attr("date")
    return date
}
function ajax_upWorkHours(project_id,date,value){
        $.post("upworktime",
      {
        project_id:project_id,
        date:date,
        worktime:value
      },
      function(data,status){
        switch (status){
            case 'success':
            var jsonObj = JSON.parse(data);
            if(jsonObj.status){
                $.hulla.send(jsonObj.message, "success");
            }else{
                $.hulla.send(jsonObj.message, "warning");
            }
            break;
        }
      });
}
function ajax_deleteWorkHours(project_id,date){
        $.get("delework",
      {
        project_id:project_id,
        date:date
      },
      function(data,status){
        switch (status){
            case 'success':
            var jsonObj = JSON.parse(data);
            if(jsonObj.status){
                $.hulla.send(jsonObj.message, "danger");
            }else{
                $.hulla.send(jsonObj.message, "warning");
            }
            break;
        }

      });
}
var work_hour_obj  = $("td.sum_work_hours")//获取所有横向合计td
up_rowSumWorkHour()