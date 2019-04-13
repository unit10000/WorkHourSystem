import xlwt
import io
def make_work_hour_Ex(dateList,company,start_time,end_time):
    '''
    制作工时报表
    :param dateList: 日期列表
    :param company: 公司对象
    :param start_time: 开始时间1
    :param end_time: 结束时间
    :return:
    '''
    excelTabel= xlwt.Workbook()#创建excel对象
    style = xlwt.XFStyle()  # Create Style
    style.alignment.horz = 2  # 字体居中
    style.alignment.vert = 1
    style.alignment.wrap = 1
    sheet1=excelTabel.add_sheet(start_time+'-'+end_time,cell_overwrite_ok=True)
    sheet1.write(0,0,'项目编号',style)#
    sheet1.col(0).width = 256 * 15
    sheet1.write(0,1,'项目名称',style)#
    sheet1.col(1).width = 256 * 15
    sheet1.write(0,2,'负责人',style)#
    sheet1.col(2).width = 256 * 10
    sheet1.write(0,3,'参与人',style)#
    sheet1.col(3).width = 256 * 10
    x = 1
    a = 3
    u_index = 1
    for d in dateList:
        a+=1
        sheet1.col(a).width=256*12
        sheet1.write(0, a, d,style)
    for d in company.get_valid_departments():
        for p in d.get_valid_projects():
            # if p[2] !=0:
            #     continue
            lsbl = len(p.get_valid_users())#获取项目人数
            if lsbl < 1:#如果项目没有人员则不打印该项目
                continue
            sheet1.write_merge(x,x+ lsbl-1, 0, 0, p.id,style)#写项目id
            sheet1.write_merge(x, x + lsbl - 1, 1, 1, p.name,style)#写项目名称
            if p.super_user:
                sheet1.write_merge(x, x + lsbl - 1, 2, 2, p.super_user.user,style)#写项目负责人
            else:
                sheet1.write_merge(x, x + lsbl - 1, 2, 2, 'null', style)  # 写项目负责人
            for u in p.get_valid_users():#循环项目成员
                sheet1.write(u_index, 3, u.user, style)#写成员姓名
                date_start_index = 4
                work_horus = u.get_work_hours(p.id,start_time ,end_time)#获取指定范围工时
                for w in work_horus:#将对应工时写入表格
                    index = dateList.index(w.date)+date_start_index#获取当前工时在表格中的索引
                    sheet1.write(u_index,index , w.worktime, style)#写入
                u_index+=1
            x +=lsbl
    #directory = os.getcwd()
    s = io.BytesIO()  # 将文件保存到一个io里返回
    excelTabel.save(s)
    return s.getvalue()
def make_BOM_Ex(jsonObj):
    '''
    制作bom报表
    :param jsonObj: bomjson数据
    :return:
    '''
    items = jsonObj['items']
    height_style = xlwt.easyxf('font:height 330')  # 36pt
    def __init_border():
        borders = xlwt.Borders()
        borders.left = 1
        borders.right = 1
        borders.top = 1
        borders.bottom = 1
        borders.bottom_colour = 0x3A
        return borders

    def __init_Font():
        fnt = xlwt.Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
        fnt.name = u'SimSun'  # 设置其字体为宋体
        return fnt
    def __init_titleFont():
        fnt = xlwt.Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
        fnt.name = u'SimSun'  # 设置其字体为宋体
        fnt.bold = True
        return fnt
    def wirte(obj,x,y,style,width,value):
        obj.write(y, x, value, style)  #
        if width:
            obj.col(x).width = width
        row = sheet1.row(y)
        row.set_style(height_style)
    def insert_tag(excel_obj,index_y, style,tag):
        import copy
        wirte(excel_obj, 0, index_y, style, None, '')
        title_style = copy.deepcopy(style)
        title_style.alignment.horz = 2
        title_style.font = __init_titleFont()
        excel_obj.write_merge(index_y, index_y, 1, 7, tag, title_style)
    def __header(excel_obj, style):
        import copy
        title_style = copy.deepcopy(style)
        value_style = copy.deepcopy(style)
        value_style.alignment.horz = 1
        title_style.alignment.horz = 2
        title_style.font = __init_titleFont()
        def init_header(row_index):
            wirte(excel_obj, 0, row_index, title_style, None, "序号")
            wirte(excel_obj, 1, row_index, title_style, None, "物料编码")
            wirte(excel_obj, 2, row_index, title_style, None, "名称")
            wirte(excel_obj, 3, row_index, title_style, None, "型号")
            wirte(excel_obj, 4, row_index, title_style, None, "描述")
            wirte(excel_obj, 5, row_index, title_style, None, "安装位号")
            wirte(excel_obj, 6, row_index, title_style, None, "单位")
            wirte(excel_obj, 7, row_index, title_style, None, "数量")
            wirte(excel_obj, 8, row_index, title_style, None, "备注")
        def insert(index,title,value,title2,value2):
            #写标题
            wirte(excel_obj, 0, index, title_style, 256*5, '')
            wirte(excel_obj,1,index,title_style,256 * 14,'')
            excel_obj.write_merge(index, index, 0, 1, title,title_style)
            #写值
            wirte(excel_obj, 2, index, value_style, 256 * 33, '')
            wirte(excel_obj, 3, index, value_style, 256 * 18, '')
            excel_obj.write_merge(index, index, 2, 3, value, value_style)
            #写标题2
            wirte(excel_obj, 4, index, title_style, 256 * 30, title2)
            #写value2
            # 写值
            wirte(excel_obj, 5, index, value_style, 256 * 23, '')
            wirte(excel_obj, 6, index, value_style, 256 * 5, '')
            wirte(excel_obj, 7, index, value_style, 256 * 5, '')
            wirte(excel_obj, 8, index, value_style, 256 * 8, '')
            excel_obj.write_merge(index, index, 5, 8, value2, value_style)
        #写入头部内容
        insert(0,"项目名称：",jsonObj['project_name'],'项目编号：',jsonObj['project_id'])
        insert(1,"文件名称：", jsonObj['file_name'], '图号/文件号：', jsonObj['file_id'])
        insert(2, "物料编码：", jsonObj['item_num'], '版本号：',jsonObj['version'])
        insert(3, "制 表 人：",  jsonObj['user_name'], '审    核：', jsonObj['auditing'])
        insert(4, "校     对：", jsonObj['proofreading'], '批    准：', jsonObj['approval'])
        insert(5, "会     签：",  jsonObj['signer'], '日    期：', jsonObj['date'])
        init_header(6)
        return 7
    def __body(excel_obj,style,start_y):
        def insert_wl(row_index,map):
            wirte(excel_obj, 0, row_index, style, None, map['index'])
            wirte(excel_obj, 1, row_index, style, None, map['item_number'])
            wirte(excel_obj, 2, row_index, style, None, map['name'])
            wirte(excel_obj, 3, row_index, style, None, map['model'])
            wirte(excel_obj, 4, row_index, style, None, map['note'])
            wirte(excel_obj, 5, row_index, style, None, map['install_number'])
            wirte(excel_obj, 6, row_index, style, None, map['unit'])
            wirte(excel_obj, 7, row_index, style, None, map['number'])
            wirte(excel_obj, 8, row_index, style, None, map['remark'])
        #insert_tag(excel_obj, start_y, style, "整件")
        for row in items:
            insert_wl(start_y,row)
            start_y=start_y+1
    excelTabel= xlwt.Workbook()#创建excel对象
    style = xlwt.XFStyle()  # Create Style
    style.alignment.horz = 2  # 字体居中
    style.alignment.vert = 1
    style.alignment.wrap = 1
    style.font =__init_Font()
    style.borders = __init_border()
    sheet1=excelTabel.add_sheet('BOM表',cell_overwrite_ok=True)
    return_index = __header(sheet1,style=style)
    __body(sheet1,style,return_index)
    s = io.BytesIO()#将文件保存到一个io里返回
    excelTabel.save(s)
    return s.getvalue()
if __name__ == '__main__':
    make_BOM_Ex()

