

    function setSelectDate(y,m,d){
        str=y+'-'
        if(m<10){str+='0'+m}else{str +=m}
        str+='-'
        if(d<10){str+='0'+d}else{str+=d}

        document.querySelector('#'+inputDateName).value = str
    }

        $(function(){
            $(".panel-heading").click(function(e){
                /*切换折叠指示图标*/
                $(this).find("span").toggleClass("glyphicon-chevron-down");
                $(this).find("span").toggleClass("glyphicon-chevron-up");
            });
        });
            var inputDateName=""
        	var mySchedule = new Schedule({
		el: '#schedule-box',
		//date: '2018-9-20',
		clickCb: function (y,m,d) {
            setSelectDate(y,m,d)
            //$("#schedule-box").slideToggle("slow");
            $("#schedule-box").animate({left:'+=40'}).animate({left:-$("#schedule-box").outerWidth()});
		},
		nextMonthCb: function (y,m,d) {
			setSelectDate(y,m,d)
		},
		nextYeayCb: function (y,m,d) {
			setSelectDate(y,m,d)
		},
		prevMonthCb: function (y,m,d) {
			setSelectDate(y,m,d)
		},
		prevYearCb: function (y,m,d) {
			setSelectDate(y,m,d)
		}
	});
	$("#date1").bind("click",function(){
	    inputDateName = "date1"
	    var top = $(this).offset().top+$(this).outerHeight();
        var left = $(this).offset().left;
        $("#schedule-box").css("top",-$("#schedule-box").outerHeight());
        $("#schedule-box").css("left",left);
        $("#schedule-box").show();
        $("#schedule-box").animate({top:top+40}).animate({top:top});
    });


    $("#date2").bind("click",function(){
        inputDateName = "date2"
         var top = $(this).offset().top+$(this).outerHeight();
        var left = $(this).offset().left;
        $("#schedule-box").css("top",-$("#schedule-box").outerHeight());
        $("#schedule-box").css("left",left);
        $("#schedule-box").show();
        $("#schedule-box").animate({top:top+30}).animate({top:top});
    });

     $(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$("#date3").bind("click",function(){
        inputDateName = "date3"
      $("#schedule-box").slideToggle("slow");
    });
     $("#schedule-box").hide();
     $(function () {
  $('[data-toggle="tooltip"]').tooltip()
})
    $("#submit_wh_button").click(function(){
        $.hulla = new hullabaloo();
        var work_date =$("#date3").val()
        var project_id = $("#project_id_input").val()
        var worktime = $("#work_time_input").val()
        if(''==work_date || project_id=='' || worktime==''){
            //$.hulla.send("请填写完整参数！", "info");
            alert('请填写完整参数')
            return
        }

        $.post("upworktime",
          {
            date:work_date,
            project_id:project_id,
            worktime:worktime
          },
          function(data,status){
            var jsonObj = JSON.parse(data);
            if(status=='success' && jsonObj['status']){
                //var row_index=$("#row_index").val()
                row_index = $("#work_time_thead").children().length+1
                //$.hulla.send(work_date+" "+jsonObj['message'], "success");
                alert(jsonObj['message'])
                var isExist = false
                $(".work_date").each(function(){
                    if($(this).text()==work_date){
                        $(this).prev().children(":first").text(worktime)
                        isExist = true
                    }
                  });
                if(isExist)return
                var table = $("<tr>\n" +
                    "                          <th scope=\"row\">"+row_index+"</th>\n" +
                    "                          <td>"+project_id+"</td>\n" +
                    "                          <td>{{data['current_project'].name}}</td>\n" +
                    "                            <td><span style=\"font-weight:bold ; \">"+worktime+"</span></td>\n" +
                    "                          <td class='work_date' >"+work_date+"</td>\n" +
                    "                          <td><button type=\"button\" data-toggle=\"tooltip\" data-placement=\"top\" title=\"请刷新页面后进行删除\" class=\"btn btn-danger disabled\">删除</button></td>\n" +
                    "                        </tr>")
                $("#work_time_thead").append(table)
            }else{
                //$.hulla.send(jsonObj['message'])
                alert(jsonObj['message'])
            }
          });
    });
