import datetime
import sys
import time
from threading import Thread
from time import sleep
from PyQt5.QtWidgets import *
from PySide2 import QtGui, QtWidgets
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QTableWidgetItem, \
    QAbstractItemView, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from childwindow import Page
import sqlalchemy
import config
import xlsxwriter as xw




class mainPage:
    def __init__(self):
        q_file = QFile("mian.ui")
        q_file.open(QFile.ReadOnly)
        q_file.close()
        self.ui = QUiLoader().load(q_file)
        self.ui.pushButton.clicked.connect(self.openSetPage)
        self.ui.queryData.clicked.connect(self.query)
        self.ui.dataExport.clicked.connect(self.dataExport)
        self._dbEngine = sqlalchemy.create_engine(
            "oracle+cx_oracle://yms_eda:yms_eda@192.168.68.135:1521/?service_name=EDADB",
            connect_args={'encoding': 'utf-8'})

        self._dbEngine.connect()
        self._connObj = self._dbEngine.connect()
        self.connection = self._connObj.connection
        self.cursor = self.connection.cursor()


    # 打开设置页面
    def openSetPage(self):
        self.childwindow = Page(self.cursor, self.connection)
        self.childwindow.ui.show()

    # 数据解析为页面需要的格式
    def parsData(self,fetchall):
        data = []
        for item in fetchall:
            data.append(item[0])
        return data

    # 数据查询
    def query(self):
        try:
            con = {}
            sql = config.QUERY_CONFIG_SQL
            lot_id = self.ui.lotId.text()
            if lot_id == '':
                self.ui.mainLog.append(f'批号不允许为空')
                return
            product_id = self.ui.productId.text()
            if product_id != "":
                sql = sql + " and PRODUCT = :v0"
                con['v0'] = product_id

            item_id = self.ui.itemId.text()
            if item_id != "":
                sql = sql + " and ITEMS = :v1"
                con['v1'] = item_id
            if len(con) == 0:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, con)
            result = self.cursor.fetchall()
            self.ui.mainLog.append(f'---读取配置成功---{result}')
            data = {}
            query_conditions = {}
            header = []
            for rel in result:
                product = rel[0]
                item = rel[1]
                qty = int(rel[2])   # 抓取数量
                upper = float(rel[3])  # 上线
                lower = float(rel[4])  # 下限
                query_conditions['v0'] = product
                query_conditions['v1'] = item
                query_conditions['v2'] = lot_id
                query_conditions['v3'] = lower
                query_conditions['v4'] = upper
                query_conditions['v5'] = qty
                self.cursor.execute(config.QUERY_DATA_SQL, query_conditions)
                fetchall = self.cursor.fetchall()
                if len(fetchall) != 0:
                    header_info = product + '\r\n' + item + \
                                  '\r\n抓取下限:' + str(lower) + '\r\n抓取上限' + str(upper)+'\r\n抓取点数:'+str(qty)
                    header.append(header_info)
                    data[header_info] = self.parsData(fetchall)
            self.ui.mainLog.append(f'---数据查询成功---')
            self.ui.dataTable.setRowCount(0)
            self.ui.dataTable.setColumnCount(0)
            # D2120003
            rownum, column = 0, len(data)
            for param, value in data.items():
                header.append(param)
                if rownum < len(value):
                    rownum = len(value)
            self.ui.dataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.ui.dataTable.setRowCount(rownum + 1)
            self.ui.dataTable.setColumnCount(column)  # 设置表格的列数
            self.ui.dataTable.setHorizontalHeaderLabels(header)  # 设置表格头数据
            table_row_num, table_column_num = 0, 0

            for param, value in data.items():
                for val in value:
                    item = QTableWidgetItem()
                    item.setText(str(val))
                    self.ui.dataTable.setItem(table_row_num, table_column_num, item)
                    table_row_num += 1
                table_row_num = 0
                table_column_num += 1
        except Exception as e:
            self.ui.mainLog.append(f'---查询失败---{e}')

    # 数据导出 D2120003
    def dataExport(self):
        try:
            current_time = time.strftime("%Y%m%d-%H%M%S")
            file_path = "D:\\" + self.ui.lotId.text() + str(current_time) + '.xlsx'
            table = self.ui.dataTable
            # 行数
            rowcount = table.rowCount()
            # 列数
            columncount = table.columnCount()
            headers = [table.horizontalHeaderItem(r).text() for r in range(columncount)]

            data = []
            for rownum in range(rowcount):
                row_data = []
                for columnnum in range(columncount):
                    if table.item(rownum, columnnum) is not None:
                        text = table.item(rownum, columnnum).text()
                        row_data.append(str(text))
                    else:
                        row_data.append("")
                data.append(row_data)
            self.xw_toexcel(headers, data, file_path)
            self.ui.mainLog.append(f'---文件生成成功---{file_path}')
        except Exception as e:
            self.ui.mainLog.append(f'---数据导出失败---{e}')

    def xw_toexcel(self, title, data, file_path):
        try:
            """ 通过 xlsxwriter 方式 """
            # 创建工作簿
            workbook = xw.Workbook(file_path)
            # 创建子表
            worksheet = workbook.add_worksheet("sheet")
            # 激活表
            worksheet.activate()
            # 设置表头
            # 从A1单元格开始写入表头
            worksheet.write_row('A1', title)
            # 从第二行开始写入数据
            i = 2
            for j in range(len(data)):
                insertData = data[j]
                row = 'A' + str(i)
                worksheet.write_row(row, insertData)
                i += 1
            # 关闭表
            workbook.close()
        except Exception as e:
            self.ui.mainLog.append(f'---文件生成失败---{e}')

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            print(e)




if __name__ == '__main__':
    mainApp = QApplication([])
    mainPage = mainPage()
    mainPage.ui.show()
    mainApp.aboutToQuit.connect(mainPage.close)
    sys.exit(mainApp.exec_())
