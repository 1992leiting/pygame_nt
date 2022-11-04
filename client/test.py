import pickle


d = dict()

d['director'] = dict(
    type='Director',
    uuid=100,
    children={}
)

d['director']['children']['world_scene'] = dict(
    type='World',
    uuid=100,
    children={}
)

d['director']['children']['ba'] = dict(
    type='ImageRect',
    uuid=100,
    children={}
)


class ConfigItem:
    def __init__(self, tp, name):
        self.name = name
        self.type = tp
        self.uuid = 0
        self.children = {}

    def add_child(self, tp, name):
        self.children[name] = ConfigItem(tp, name)

    def child(self, name):
        if name in self.children:
            return self.children[name]
        return None


dr = ConfigItem('Director', 'director')
dr.add_child('World', 'world_scene')
dr.child('world_scene').add_child('ImageRect', 'map_jpg')

with open('config.conf', 'wb') as f:
    pickle.dump(dr, f)
