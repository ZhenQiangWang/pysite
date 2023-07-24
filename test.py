# @Author   :zhenqiang.wang
# @Time     :2023/7/4 14:31
#
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 创建标签
        label = QLabel('Hello, PyQt5!')

        # 创建按钮
        button = QPushButton('Click me!')

        # 创建文本框
        text_box = QLineEdit()

        # 创建垂直布局
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        layout.addWidget(text_box)

        # 将布局应用到窗口
        self.setLayout(layout)

        # 设置窗口标题和大小
        self.setWindowTitle('My PyQt5 Window')
        self.setGeometry(100, 100, 300, 200)

        # 连接按钮的点击事件到槽函数
        button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        # 按钮点击事件的槽函数
        text = self.text_box.text()
        print('Button clicked! Text entered:', text)

if __name__ == '__main__':
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建窗口对象
    window = MyWindow()

    # 显示窗口
    window.show()

    # 运行应用程序的主循环
    sys.exit(app.exec_())
