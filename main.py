from Node.node import Node
from Node.director import Director
from Nt.nt_item import ConfigItem
from Common.common import print_node

director = Director()
director.setup_from_config('game_ui.conf')
print_node(director)
