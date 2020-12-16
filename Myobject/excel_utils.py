import xlwt #写入excel
import xlrd #读excel
from xlutils.copy import copy  #读和写中间转换器

def write_to_excel(words,filename,sheet_name='sheet0'):
    '''
    将item存储到excel中。
    :param words: 保存item的list---[{},{}]
    :return:
    '''
    try:
        # 1、创建工作薄
        work_book = xlwt.Workbook(encoding='utf-8')
        # 2、创建sheet表单
        sheet = work_book.add_sheet(sheet_name)
        # 3、写表头
        # head = ['英文','中文']
        head = []
        for k in words[0].keys():
            head.append(k)

        for i in range(len(head)):
            sheet.write(0, i, head[i])
        # 4、添加内容
        # 行号
        i = 1
        for item in words:
            for j in range(len(head)):
                sheet.write(i, j, item[head[j]])
            # 写完一行，将行号+1
            i += 1
        # 保存
        work_book.save(filename)
        print('写入excel成功！')
    except Exception as e:
        print('写入excel失败！',e)


def append_to_excel(words,filename):
    '''
    追加数据到excel
    :param words: 【item】
    :param filename: 文件名
    :return:
    '''
    try:
        # 打开excel
        word_book = xlrd.open_workbook(filename)
        # 获取所有的sheet表单。
        sheets = word_book.sheet_names()
        # 获取第一个表单
        work_sheet = word_book.sheet_by_name(sheets[0])
        # 获取已经写入的行数
        old_rows = work_sheet.nrows
        # 获取表头信息
        heads = work_sheet.row_values(0)
        # 将xlrd对象变成xlwt
        new_work_book = copy(word_book)
        # 添加内容
        new_sheet = new_work_book.get_sheet(0)
        i = old_rows
        for item in words:
            for j in range(len(heads)):
                new_sheet.write(i, j, item[heads[j]])
            i += 1
        new_work_book.save(filename)
        print('追加成功！')
    except Exception as e:
        print('追加失败！',e)


