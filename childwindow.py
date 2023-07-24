from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QTableWidgetItem, \
    QAbstractItemView
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
import config


class Page:

    def __init__(self, cursor, connection):
        q_file = QFile("dataQuery.ui")
        q_file.open(QFile.ReadOnly)
        q_file.close()
        self.ui = QUiLoader().load(q_file)
        self.ui.add.clicked.connect(self.addLine)
        self.ui.rem.clicked.connect(self.delLine)
        self.ui.save.clicked.connect(self.save)
        self.ui.query.clicked.connect(self.query)
        self.cursor = cursor
        self.connection = connection

    # 添加行
    def addLine(self):
        self.ui.tableWidget.insertRow(0)

    # 删除行
    def delLine(self):
        try:
            data = {}
            del_sql = config.DEL_SQL
            table = self.ui.tableWidget
            row = table.currentRow()
            product_id = table.item(row, 0).text()
            item_id = table.item(row, 1).text()
            data['v0'] = product_id
            data['v1'] = item_id
            self.ui.log.append(f'删除数据,产品类型:{product_id},检验项目:{item_id}')
            self.cursor.execute(del_sql, data)
            self.connection.commit()
            table.removeRow(row)
            self.ui.log.append(f'删除成功')
        except Exception as e:
            self.ui.log.append(f'删除失败--{e}')
            self.connection.rollback()

    # 保存
    def save(self):
        try:
            insert_sql = config.INSERT_SQL
            table = self.ui.tableWidget
            # 行数
            rowcount = table.rowCount()
            # 列数
            columncount = table.columnCount()
            data = []
            for rownum in range(rowcount):
                row_data = []
                for columnnum in range(columncount):
                    text = table.item(rownum, columnnum).text()
                    row_data.append(str(text))
                data.append(row_data)
            self.cursor.executemany(insert_sql, data)
            self.connection.commit()
            self.ui.log.append(f'---保存成功---')
        except Exception as e:
            self.ui.log.append(f'---保存失败---{e}')
            self.connection.rollback()

    def query(self):
        try:
            product = {}
            sql = config.QUERY_CONFIG_SQL
            product_id = self.ui.lineEdit.text()
            if product_id != "":
                product['v0'] = product_id
                sql = sql + " and PRODUCT = :v0"
                self.cursor.execute(sql, product)
            else:
                self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.ui.tableWidget.setRowCount(len(result))
            # self.ui.tableWidget.setItem(1, 1, QTableWidgetItem('2'))
            row_num = 0
            for val in result:
                item = QTableWidgetItem()
                item.setText(str(1))
                self.ui.tableWidget.setItem(row_num, 0, QTableWidgetItem(val[0]))
                self.ui.tableWidget.setItem(row_num, 1, QTableWidgetItem(val[1]))
                self.ui.tableWidget.setItem(row_num, 2, QTableWidgetItem(val[2]))
                self.ui.tableWidget.setItem(row_num, 3, QTableWidgetItem(val[3]))
                self.ui.tableWidget.setItem(row_num, 4, QTableWidgetItem(val[4]))
                row_num += 1
            self.ui.log.append(f'---查询成功---')
            # print(result)
            # table = self.ui.tableWidget

        except Exception as e:
            self.ui.log.append(f'---查询失败---{e}')
            self.connection.rollback()

# app = QApplication([])
# page = Page()
# page.ui.show()
# app.exec_()
