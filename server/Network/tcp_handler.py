from Common import constants as GL
from Common.common import *
from Script.scene.scene_handler import *
from Script.player.player_handler import *
from Script.item.item_handler import *
from Script.sys.sys_handler import *
import socketserver
import threading


class TCPHandler(socketserver.BaseRequestHandler):
    lock = threading.Lock()
    clients = {}
    sockets = {}
    heromsg = None
    account = None
    hid = 0
    tmp_str = ''

    def setup(self):
        """
        收到TCP连接
        :return:
        """
        super().setup()
        self.event = threading.Event()
        with self.lock:
            self.clients[self.client_address] = self.request
        print('新加入一个连接{}, 当前连接数量:{}'.format(self.client_address, len(self.clients)))

    def handle(self):
        super(TCPHandler, self).handle()
        while not self.event.is_set():
            data = self.request.recv(2)
            data_len = int.from_bytes(data, byteorder='big')
            print('data len:', data_len)
            data = self.request.recv(data_len)
            msg = json.loads(data)
            print('msg:', msg)
            tp = msg['cmd']

            if tp == C_登陆:
                """
                玩家登陆, 发送角色数据和同场景所有其他玩家数据
                """
                success_flag = False
                print('角色申请登陆:', msg)
                self.account, password, self.hid = str(msg['账号']), str(msg['密码']), str(msg['登陆id'])
                create_player(self.account, self.hid, '我要变强', '龙太子')
                for _, dirs, _ in os.walk('./data'):
                    for _dir in dirs:
                        if _dir == self.account:
                            account_info = formatted_json_to_dict('./data/' + self.account + '/账号数据.json')
                            print(account_info)
                            pw = str(account_info['密码'])
                            if pw == password:
                                # self.heromsg = formatted_json_to_dict('./data/' + self.account + '/' + self.hid + '/角色数据.json')
                                # 检查是否已经登陆
                                if self.hid in GL.PLAYERS:
                                    player_log_out(self.hid, err_text='你的账号已经从另一台电脑上登录，如非本人操作，请立即修改游戏密码！', err_tp='网络错误')
                                # 玩家登陆
                                player_log_in(self.hid, self.account, self.request, self.client_address)
                                success_flag = True
                                break
                            else:
                                send_sys_error(self.request, '密码错误, 无法登陆')
                                return
                        break
                if '新账号' in GL.PLAYERS[self.hid]:
                    del GL.PLAYERS[self.hid]['新账号']
                    refresh_play_attr(self.hid, recover=2, sendmsg=True)  # 首次刷新属性, 恢复气血/魔法
                if not success_flag:
                    send_sys_error(self.request, '账号不存在, 请先注册账号')
                    return
            elif tp == C_更新坐标:
                update_player_xy(msg)
            elif tp == C_发送路径:  # 寻路
                update_player_path(msg)
            elif tp == c_点击NPC:
                get_npc_talk(self.hid, msg)
            elif tp == C_传送点传送:
                print('C_传送点传送', self.hid, msg, GL.PLAYERS[self.hid]['传送完成'])
                if '传送完成' in GL.PLAYERS[self.hid] and GL.PLAYERS[self.hid]['传送完成']:
                    GL.PLAYERS[self.hid]['传送完成'] = False
                    portal_transfer(self.hid, msg['传送圈id'])
            elif tp == C_获取所有物品信息:
                send_all_items(self.hid)
            elif tp == C_申请成为队长:
                be_captain(self.hid)
            elif tp == C_申请组队:
                print('C_申请组队:', msg)
                apply_for_team(self.hid, msg['目标id'])
            elif tp == C_人物确认加点:
                player_人物确认加点(self.hid, msg['属性点'])
            elif tp == C_角色升级:
                player_level_up(self.hid)

    def finish(self):
        """
        只要结束了handle, 该TCP线程就会走到finish
        从clients列表中剔除, 并关闭request
        :return:
        """
        super().finish()
        self.event.set()
        # 连接列表中删除
        with self.lock:
            if self.client_address in self.clients:
                self.clients.pop(self.client_address)
        player_log_out(self.hid)
        # 关闭连接
        self.request.close()
        print('{}退出'.format(self.client_address))

    # def savemsg(self):
    #     if self.account is not None:
    #         with open('./data/' + self.account + '/' + self.hid + '/角色数据tmp.json', 'w', encoding='utf-8') as f:
    #             json.dump(GL.PLAYERS[self.hid], f, cls=MyEncoder, ensure_ascii=False)
    #         os.remove('./data/' + self.account + '/' + self.hid + '/角色数据.json')
    #         os.rename('./data/' + self.account + '/' + self.hid + '/角色数据tmp.json',
    #                   './data/' + self.account + '/' + self.hid + '/角色数据.json')
    #         # 玩家数据列表中删除
    #         GL.PLAYERS.pop(self.hid)

