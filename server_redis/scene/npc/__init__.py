import os

for file in os.listdir():
    if file.startswith('npc_'):
        npc, nid, name, map, mname = file.split('_')
        print(npc, nid, name, map, mname)
        new_file_name = '{}_{}.py'.format(map, name)
        try:
            os.rename(file, new_file_name)
        except:
            pass