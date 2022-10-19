from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from Qtui.nodemanager import Ui_NodeManager as UIM
from Nt.nt_item import *


COL_NODE = 0
COL_TYPE = 1
COL_NAME = 2
COL_UUID = 3
NODE_LIST = [
    'Node', 'Animation', 'Animation8D', 'Button', 'Director', 'ImageRect', 'Label', 'ProgressBar', 'RichText',
    'TextEdit', 'LineEdit', 'Camera', 'BasicCharacter', 'Character', 'NPC', 'BattleUnit', 'Emoji', 'HpEffect',
    'BuffEffect', 'MagicEffect', 'FullScreenEffect', 'MapMask', 'Mouse', 'Portal', 'World'
]


class NewUiMainWindow(UIM):
    def __init__(self):
        super(NewUiMainWindow, self).__init__()
        self.setupUi(MainWindow)
        self.treeWidget_node_tree = TreeWidget(self.groupBox)
        self.treeWidget_node_tree.setGeometry(QtCore.QRect(10, 20, 771, 471))
        self.treeWidget_node_tree.headerItem().setText(0, '节点')
        self.treeWidget_node_tree.headerItem().setText(1, '类型')
        self.treeWidget_node_tree.headerItem().setText(2, '名称')
        self.treeWidget_node_tree.headerItem().setText(3, 'UUID')
        self.treeWidget_node_tree.setColumnWidth(0, 300)
        self.treeWidget_node_tree.setColumnWidth(3, 150)
        self.sb_timer = QtCore.QTimer()
        self.sb_timer.timeout.connect(self.statusbar.clearMessage)
        self.config_file = ''

    def setup(self):
        MainWindow.setWindowTitle('pygame_nt UI管理器')
        MainWindow.setWindowIcon(QtGui.QIcon('icon/icon_tree.png'))
        # 信号链接
        self.pushButton_load_config_file.clicked.connect(self.select_config_file)
        self.pushButton_create_config_file.clicked.connect(self.create_config_file)
        self.pushButton_create_child_node.clicked.connect(self.add_child_node)
        self.pushButton_modify_node_attr.clicked.connect(self.modify_node_attr)
        self.pushButton_save.clicked.connect(self.save_config_file)
        self.pushButton_delete_node.clicked.connect(self.delete_tree_item)

        # Node列表
        for node in NODE_LIST:
            self.comboBox_node_type_list.addItem(node)

    def add_child_node(self):
        """
        增加子节点, 检测到节点重名时会增加后缀符号
        :return:
        """
        cur_item = self.treeWidget_node_tree.currentItem()
        if cur_item:
            tp = self.comboBox_node_type_list.currentText()
            name = self.lineEdit_node_name_input.text()
            if not name:
                name = 'Node'
            for i in range(cur_item.childCount()):
                child = cur_item.child(i)
                if name == child.text(COL_NAME):
                    name += '#'
            child_item = TreeWidgetItem(name, tp, cur_item)
            child_item.set_text()

    def modify_node_attr(self):
        cur_item = self.treeWidget_node_tree.currentItem()
        if cur_item:
            tp = self.comboBox_node_type_list.currentText()
            name = self.lineEdit_node_name_input.text()
            if not name:
                name = 'Node'
            for i in range(cur_item.childCount()):
                child = cur_item.child(i)
                if name == child.text(COL_NAME):
                    name += '#'
            cur_item.node_name = name
            cur_item.node_type = tp
            cur_item.set_text()
    
    def show_sb_msg(self, msg: str):
        """
        状态栏提示消息并在3秒后清除
        """
        self.statusbar.showMessage(msg)
        self.sb_timer.start(3000)

    def delete_tree_item(self):
        cur_item = self.treeWidget_node_tree.currentItem()
        if cur_item and cur_item.parent():
            cur_item.parent().removeChild(cur_item)

    def save_config_file(self):
        self.treeWidget_node_tree.tree_to_config(self.config_file)
        self.show_sb_msg('节点配置已保存:' + self.config_file)
        
    def create_config_file(self):
        widget = QtWidgets.QWidget(self.centralwidget)
        config_file = QtWidgets.QFileDialog.getSaveFileName(widget, '创建', './', '*.conf')[0]
        tree_widget = TreeWidget()
        director_item = TreeWidgetItem('director', 'Director')
        director_item.set_text()
        tree_widget.addTopLevelItem(director_item)
        tree_widget.tree_to_config(config_file)
        
    def select_config_file(self):
        widget = QtWidgets.QWidget(self.centralwidget)
        self.config_file = QtWidgets.QFileDialog.getOpenFileName(widget, '浏览', './', '*.conf')[0]
        self.load_config_file()
        
    def load_config_file(self):
        if not self.config_file:
            return
        try:
            self.treeWidget_node_tree.tree_from_config(self.config_file)
            self.show_sb_msg('已加载配置文件:' + self.config_file)
            self.lineEdit_config_file.setText(self.config_file)
        except:
            self.show_sb_msg('无法加载该配置文件')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = NewUiMainWindow()
    ui.setup()
    MainWindow.show()
    sys.exit(app.exec_())
