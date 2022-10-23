from Common.constants import *
from PyQt5 import QtGui, QtWidgets
import uuid
import pickle


class ConfigItem:
    def __init__(self, name, tp, uid):
        self.node_name = name
        self.node_type = tp
        self.node_uuid = uid
        self.children = {}

    def add_child(self, name, tp, uid):
        self.children[name] = ConfigItem(name, tp, uid)

    def child(self, name):
        if name in self.children:
            return self.children[name]
        return None


class TreeWidget(QtWidgets.QTreeWidget):
    def __init__(self):
        super(TreeWidget, self).__init__()
        self.setDragDropMode(QtWidgets.QTreeWidget.InternalMove)
        self.setDragEnabled(True)
        self.config_data = None

    def dragMoveEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            super(TreeWidget, self).dragMoveEvent(event)
        else:
            event.ignore()

    def dropEvent(self, event) -> None:
        item = self.itemAt(event.pos())
        if item:
            super(TreeWidget, self).dropEvent(event)
        else:
            event.ignore()

    def tree_to_config(self, config_file='config.conf'):
        if not config_file:
            config_file = 'config.conf'
        top_item = self.topLevelItem(0)
        self.config_data = ConfigItem(top_item.text(COL_NAME), top_item.text(COL_TYPE), top_item.text(COL_UUID))
        self.traverse_tree_widget(top_item, self.config_data)
        print('save:', top_item, top_item.text(0), self.config_data.node_name)
        with open(config_file, 'wb') as f:
            pickle.dump(self.config_data, f)

    def tree_from_config(self, config_file='config.conf'):
        with open(config_file, 'rb') as f:
            config_data = pickle.load(f)
            top_item = TreeWidgetItem(config_data.node_name, config_data.node_type, self)
            top_item.set_text()
            self.traverse_config_item(config_data, top_item)

    def traverse_config_item(self, config_item: ConfigItem, tree_widget_item: QtWidgets.QTreeWidgetItem):
        """
        config --> tree
        :param config_item:
        :param tree_widget_item:
        :return:
        """
        tree_widget_item.setText(COL_NODE, config_item.node_name)
        tree_widget_item.setText(COL_TYPE, config_item.node_type)
        tree_widget_item.setText(COL_NAME, config_item.node_name)
        tree_widget_item.setText(COL_UUID, config_item.node_uuid)
        if config_item.children:
            for _, child in config_item.children.items():
                print('add tree item:', child.node_name)
                tree_item = TreeWidgetItem(child.node_name, child.node_type, parent=tree_widget_item)
                tree_item.set_text()
                self.traverse_config_item(child, tree_item)

    def traverse_tree_widget(self, item: QtWidgets.QTreeWidgetItem, config_item):
        """
        tree --> config
        :param item:
        :param config_item:
        :return:
        """
        child_cnt = item.childCount()
        if child_cnt > 0:
            for i in range(child_cnt):
                child = item.child(i)
                config_item.add_child(child.text(COL_NAME), child.text(COL_TYPE), child.text(COL_UUID))
                self.traverse_tree_widget(child, config_item.child(child.text(COL_NAME)))


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, node_name, node_type):
        super(TreeWidgetItem, self).__init__()
        # 自定义参数, 和节点相关
        self.node_name = node_name
        self.node_type = node_type
        self.node_uuid = str(uuid.uuid4())

    def set_text(self):
        self.setText(COL_NODE, self.node_name)
        self.setText(COL_TYPE, self.node_type)
        self.setText(COL_NAME, self.node_name)
        self.setText(COL_UUID, self.node_uuid)
        icon_path = 'icon/{}.png'.format(self.node_type)
        if os.path.exists(icon_path):
            self.setIcon(COL_NODE, QtGui.QIcon(icon_path))
