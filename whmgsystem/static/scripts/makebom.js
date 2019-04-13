//刷新绑定事件
function refurbish(){
    //绑定删除物料事件
    $(".delete_item").click(function(){
            $(this).parent().parent().remove()
            refurbish_td_index()
        })
     //检索函数
     function select_item(obj,type){
            if (obj.children("input").length > 0 ){//当前元素正在编辑返回
                return
            }
            var val = obj.text()
            var this_width = obj.width()-100
            var this_height = obj.height()-4
            obj.html('<input class="edit_input" autocomplete="off" id="edit_select" autofocus="autofocus" type="text"  style="border: 0px solid #ddd;margin:0px 0px; width:100%; height:100%;text-align:center" value="'+val+'" />')
            $(".edit_input").focus()
            $(".edit_input").blur(function(){
                var val = $(this).val()
                $(this).prop("outerHTML",val)
            });
            $('#edit_select').bind('input propertychange', function() {//绑定编辑框内容改变事件进行模糊搜索物料型号
             //进行相关操作
                like_value = $(this).val()
                ajax_select_item($(this),like_value,type)
            });

        }
     // 绑定型号检索事件
    $(".model_edit").click(function(){
        select_item($(this),"FModel")
    })
    //检索描述
    $(".note_edit").click(function(){
        select_item($(this),"FNote")
    })
    //检索名称
    $(".name_edit").click(function(){
        select_item($(this),"FName")
    })
    //检索物料编码
    $(".itemNuber_edit").click(function(){
        select_item($(this),"FNumber")
    })
     // 绑定可编辑td事件
    $(".is_edit").click(function(){
        if ( $(this).children("input").length > 0 ){//当前元素正在编辑返回
            return
        }
        var val = $(this).text()
        var this_width = $(this).width()-100
        var this_height = $(this).height()-4
        $(this).html('<input class="edit_input" autofocus="autofocus" type="text"  style="border: 0px solid #ddd;margin:0px 0px; width:100%; height:100%;text-align:center" value="'+val+'" />')
        $(".edit_input").focus()
        $(".edit_input").blur(function(){
            var val = $(this).val()
            $(this).prop("outerHTML",val)
        });
    });


}
//发送ajax模糊检索请求
function ajax_select_item(ojb , value ,type){
    $.post("/api/select_icitem",
      {
//        company_id:$("#company").val(),
        data:ojb.val(),
        type:type
      },
      function(data,status){
        switch (status){
            case 'success':
            var jsonObj = JSON.parse(data);
            if(jsonObj.status){
                icitem_list.refurbish_data(ojb,jsonObj.items,type)
            }else{
                alert(jsonObj.message)
            }
            break;
        }


      });
}

//绑定弹出项目检索事件
$(".project_edit").click(function(){
    if ( $(this).children("select").length > 0 ){//当前元素正在编辑返回
        return
    }
    var top = $(this).offset().top;
    var left = $(this).offset().left;
    $("#bom_select_project").css("top",top);
    $("#bom_select_project").css("left",left);
    $("#bom_select_project").toggle()
    $(".selectpicker").unbind("blur");//卸载失去焦点事件
    var this_width = $(this).width()
    $(".bootstrap-select").width(this_width);
});
//表格处理工具
var excel_utils = {
    tableObj : $("#tableToExcel"),
    isSuccess:true,
    excel_header:null,
    excel_items:null,
    save_bom:function(){
        //保存bom
        this.check_table()
        if (this.isSuccess){
            $("#save_button").attr("disabled","disabled")
            $("#save_button").html("保存中...")
            setTimeout(function() {
                $("#save_button").removeAttr("disabled")
                $("#save_button").html("文件")
            }, 10000);
            this.__send_from("save_bom")
        }
    },copy_bom:function(){
        //复制bom
        this.check_table()
        if (this.isSuccess){
            $("#save_button").attr("disabled","disabled")
            $("#save_button").html("复制中...")
            setTimeout(function() {
                $("#save_button").removeAttr("disabled")
                $("#save_button").html("文件")
            }, 10000);
            this.__send_from("copy_bom")
        }
    },
    check_table:function(){
        //检查初始化表格数据
        this.isSuccess = true
        this.__check_header()
        this.__check_body()
    },
    download:function(){
        //开始下载表格
        this.check_table()
        if (this.isSuccess){
            this.__send_from("download_bom")
        }
    },
    __check_header:function(){
        //初始化表单头部并检查
        this.excel_header =null
        header = this.tableObj.find("thead")
        rows = header.find("tr")
        var key = ['project_name','project_id','file_name','file_id','item_num','version','user_name','auditing','proofreading','approval','signer','date']
        var check_value = ['project_name','project_id','file_name','file_id','version','user_name']//需要检查的表单
        var table = {}
        var index = 0
        for(var i = 0 ; i < rows.length-1 ; i++){
            table[key[index]]=rows.eq(i).find("td").eq(1).html()
            if(check_value.indexOf(key[index])!= -1 &&  table[key[index]]==''){//检查表项是否为空
                rows.eq(i).find("td").eq(1).css({"background": "#e5b8bc"});
                this.isSuccess = false
            }else{
                rows.eq(i).find("td").eq(1).css({"background": "#fff"});
            }

            table[key[index+1]]=rows.eq(i).find("td").eq(3).html()
            if(check_value.indexOf(key[index+1])!= -1 &&  table[key[index+1]]==''){
                rows.eq(i).find("td").eq(3).css({"background": "#e5b8bc"});
                this.isSuccess = false
            }else{
                rows.eq(i).find("td").eq(3).css({"background": "#fff"});
            }
            index+=2
        }
        this.excel_header = table
        console.log(table)


    },
    __check_body:function(){
        //初始化表单items并检查
        this.excel_items =null
        body = this.tableObj.find("tbody")
        rows = body.find("tr")
        var key = ['index','item_number','name','model','note','install_number','unit','number','remark']
        var check_value = ['model']
        var item_list = []
        for (var i = 0 ; i < rows.length-1;i++){
            var table = {}
            trOjb = rows.eq(i)
            for (var n = 0 ; n < key.length ; n++){
                var val = trOjb.find("td").eq(n).html()
                table[key[n]] = val
                if (val=='' && check_value.indexOf(key[n])!=-1){
                    trOjb.find("td").eq(n).css({"background": "#e5b8bc"});
                    this.isSuccess = false
                }else{
                    trOjb.find("td").eq(n).css({"background": "#fff"});
                }
            }
            item_list.push(table)
        }
        this.excel_items= item_list
        console.log(item_list)
    },
    __send_from:function(action){
        var from_json = this.excel_header
        from_json['items'] = this.excel_items
        console.log(from_json)
        var form = $("<form  method='post'></form>");
        var input;
        form.attr({"action":action});
        varStr = JSON.stringify(from_json)
        varStr= varStr.replace(new RegExp(/(&nbsp;)/g),' ')
        var params = {"json":varStr,"table_id":this.tableObj.attr("table_id")}
        $.each(params,function (key,value) {
            input = $("<input type='hidden'>");
            input.attr({"name":key});
            input.val(value);
            form.append(input);
        });
        $(document.body).append(form);
        form.submit();
    }
}
function refurbish_td_index(){
    rows = $("#tableToExcel").find("tbody").find("tr")
    for (var i = 0 ; i < rows.length-1 ; i++){
        row = rows.eq(i)
        row.children().eq(0).html(i+1)
    }
}
//物料搜索结果显示列表
var icitem_list = {
            htmlOjb : $("#select_ICitem"),
            mainDiv:$("#select_ICitem_div"),
            outInputOjb:null,
            data:null,
            opt_item:null,
            show : function(){//显示
                this.mainDiv.show()
            },//隐藏
            hide:function(){
                this.mainDiv.hide()
            },//更新数据
            refurbish_data:function(inputOjb,data,type){
                this.outInputOjb = inputOjb.parent()
                this.data = data
                this.hide()
                html =  '<div  class="list-group">'
                if(data.length<1){
                    html +='<a href="javascript:void(0);" class="list-group-item">没有搜索到相关物料</a>'
                }else{
                     for(i = 0 ; i < data.length; i++){
                        html +='<a href="javascript:void(0);" index="'+i+'" class="list-group-item ic_item">'+data[i][type]+' [<span style="color:red">'+data[i]['FQty']+'</span>]'+'</a>'
                    }
                }
                html+='</div>'
                this.htmlOjb.html(html)
                var input_top=inputOjb.offset().top;
                var input_left=inputOjb.offset().left-20;//减去关闭按钮宽度
                var input_height = inputOjb.height()
                this.mainDiv.css("top",input_top+input_height);
                this.mainDiv.css("left",input_left);
                this.show()
                $(".ic_item").click(this.install_data)
            },//点击item插入数据
            install_data:function(){
                data_index = $(this).attr('index')
                FNumber = icitem_list.data[data_index].FNumber
                FName = icitem_list.data[data_index].FName
                FModel = icitem_list.data[data_index].FModel
                FNote = icitem_list.data[data_index].FNote
                icitem_list.outInputOjb.html(FModel)
                parent = icitem_list.outInputOjb.parent()
                if(parent.children().length==10){
                    parent.children().eq(1).html(FNumber)
                    parent.children().eq(2).html(FName)
                    parent.children().eq(3).html(FModel)
                    parent.children().eq(4).html(FNote)
                }else{
                    alert('遍历节点出错！')
                }
                icitem_list.hide()
            },
            install_items:function(item_list){
                opt_item=null
                var error_item = new Array();
                var error = ''
                var success=0
                var i =0
                for (i = 0 ; i < item_list.length ; i++){
                    var item = item_list[i]
                    if(item['jieguo'].length==1){
                        install_item(item['jieguo'][0].FNumber,item['jieguo'][0].FName,item['jieguo'][0].FModel,item['jieguo'][0].FNote,item.install_num,item.item_num,'')
                        success+=1
                    }else{
                        error_item.push(item)
                    }
                }
                if(error_item.length >0 ){
                        show_opt_item(error_item)
                }else{
                        refurbish()//添加完后绑定事件

                }
                $.hulla.send('共输入:<strong class="red_text">'+i+'</strong>条物料,导入成功:<strong class="red_text">'+success+'</strong>条物料', "success");
                //alert("以下物料添加失败（结果不是唯一或没有搜索到结果），请手动重试：\n "+error)

            }
        }
//显示选择有冲突的物料modle
function show_opt_item(item_list){
        var htmlText = ''
        opt_num = 0
        for (var i = 0 ; i < item_list.length ; i++){

            if(item_list[i].jieguo.length==0){
                install_item('','','','',item_list[i].install_num,item_list[i].item_num,'【错误】'+item_list[i].select_data)
                continue
             }
            htmlText+='<div class="row"  style="border-top:1px dashed #000;border-bottom:1px dashed #000;padding:20px 0px;">'+
                                  '<div class="col-md-3" style="text-align:center;">'+
                                  '<a href="#" class="btn btn-danger disabled" role="button">'+item_list[i].select_data+'</a>'+
                                  '</div>'+
                                  '<div class="col-md-9">'
            item_text = ''
            for(var n = 0 ;n < item_list[i].jieguo.length ; n++){
                var text = item_list[i].jieguo[n].FNumber+' '+item_list[i].jieguo[n].FName+' '+item_list[i].jieguo[n].FModel+' '+item_list[i].jieguo[n].FNote+' 库存【'+item_list[i].jieguo[n].FQty+'】'
                item_text +='<button type="button" FNumber="'+item_list[i].jieguo[n].FNumber+'" FName="'+item_list[i].jieguo[n].FName+'" FModel="'+item_list[i].jieguo[n].FModel+'" FNote="'+item_list[i].jieguo[n].FNote+'" install_num="'+item_list[i].install_num+'" item_num="'+item_list[i].item_num+'" class="btn btn-default btn-lg btn-block opt_button" style="overflow: hidden;text-overflow: ellipsis;" data-toggle="tooltip" data-placement="top" title="'+text+'">☞ '+text+'</button>'
             }
             opt_num+=1
             htmlText+=item_text
             htmlText+='</div>'+
                                '</div>'
        }
        $(".opt-body").html(htmlText)
        if(opt_num>0){
            $('#opt_item').modal('show')
            $(".opt_button").click(function(){
                parentObj = $(this).parent().parent()
                parentObj.slideUp()
                install_item($(this).attr("FNumber"),$(this).attr("FName"),$(this).attr("FModel"),$(this).attr("FNote"),$(this).attr("install_num"),$(this).attr("item_num"),'')
                $.hulla.send('导入成功:<strong class="red_text">1</strong>条物料', "success");
                refurbish()//添加完后绑定事件
                setTimeout(function(){  //使用  setTimeout（）方法设定定时2000毫秒后判断是否关闭窗口
                    mainObj = parentObj.parent()
                    if(mainObj.children().length==1)
                        $('#opt_item').modal('hide')
                    setTimeout(function(){
                        parentObj.remove()
                    },200);
                },500);
            });
        }
        excel_utils.check_table()
        refurbish()//添加完后绑定事件
}
refurbish()
