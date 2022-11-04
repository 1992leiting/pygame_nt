def get_effect(tx):
    txs = [0x20F3E242, 'wzife.rsp']  # 问号
    #print("取特效",tx)
    if tx=="飞镖":
        txs[0] = 1229832530
        txs[1] = "addon.rsp"
    elif tx=="失忆符":
        txs[0] = 3567923082
        txs[1] = "magic.rsp"
    elif tx =="状态_渡劫金身" or tx=="状态_诸天看护":
        txs[0] = 999#0x3E795B5A
        txs[1] = 999#"magic.rsp" #光点围绕
    elif tx =="状态_分身术":
        txs[0] = 999
        txs[1] = 999
    elif tx=="状态_失忆符":
        txs[0] = 0xEB3D0AC1
        txs[1] = "waddon.rsp"
    elif tx=="状态_死亡召唤":
        txs[0] = 0x19182964
        txs[1] = "waddon.rsp"
    elif tx=="状态_苍白纸人_敌方":
        txs[0] = 0x2F45B9F0
        txs[1] = "waddon.rsp"
    elif tx=="状态_苍白纸人_我方":
        txs[0] = 0x592EBD89
        txs[1] = "waddon.rsp"
    elif tx=="状态_乾坤玄火塔_敌方":
        txs[0] = 0x325A1F6A
        txs[1] = "waddon.rsp"
    elif tx=="状态_乾坤玄火塔_我方":
        txs[0] = 0xC236BF21
        txs[1] = "waddon.rsp"
    elif tx=="状态_干将莫邪_敌方":
        txs[0] = 0x47F867FF
        txs[1] = "waddon.rsp"
    elif tx=="状态_干将莫邪_我方":
        txs[0] = 0x7838CE56
        txs[1] = "waddon.rsp"
    elif tx=="状态_虚弱":
        txs[0] = 0xAF07277F
        txs[1] = "waddon.rsp"
    elif tx=="状态_八凶法阵":
        txs[0] = 0x39BD5781
        txs[1] = "waddon.rsp"
    elif tx=="摇头摆尾":
        txs[0] = 0x8B036DE8
        txs[1] = "magic.rsp"
    elif tx=="状态_摇头摆尾":
        txs[0] = 0x59322DBA
        txs[1] = "waddon.rsp"
    elif tx=="状态_发瘟匣":
        txs[0] = 0x325A1F6A
        txs[1] = "waddon.rsp"
    elif tx=="魔焰滔天":
        txs[0] = 0x335A5A78
        txs[1] = "magic.rsp"
    elif tx=="逃跑":
        txs[0] = 0xF5189E48
        txs[1] = "addon.rsp"
    elif tx=="金甲仙衣_敌方" or tx =="无魂傀儡_敌方" or tx =="断线木偶_敌方" or tx =="降魔斗篷_敌方" or tx =="金甲仙衣" or tx=="降魔斗篷":
        txs[0] = 0x7AEF08A1
        txs[1] = "magic.rsp"
    elif tx=="状态_无魂傀儡" or tx=="状态_断线木偶" or tx=="状态_无尘扇":
        txs[0] = 0xEAA3EC9B
        txs[1] = "addon.rsp"
    elif tx=="状态_致命":
        txs[0] = 0x287884CC
        txs[1] = "waddon.rsp"
    elif tx=="心随意动":
        txs[0] = 0xDC756B6F
        txs[1] = "magic.rsp"
    elif tx=="状态_心随意动":
        txs[0] = 0x1FDF16A3
        txs[1] = "waddon.rsp"
    elif tx=="龙腾":
        txs[0] = 1936174863
        txs[1] = "magic.rsp"
    elif tx=="长驱直入":
        txs[0] = 0x91109049
        txs[1] = "magic.rsp"
    elif tx=="渡劫金身" or tx=="诸天看护":
        txs[0] = 0x21F550FF
        txs[1] = "magic.rsp"
    elif tx=="无尘扇":
        txs[0] = 0x0B8C9232
        txs[1] = "magic.rsp"
    elif tx=="混元伞":
        txs[0] = 0x1F334661
        txs[1] = "magic.rsp"
    elif tx=="干将莫邪_敌方":
        txs[0] = 0x47F867FF
        txs[1] = "magic.rsp"
    elif tx=="干将莫邪_我方":
        txs[0] = 0x7838CE56
        txs[1] = "magic.rsp"
    elif tx=="清心咒":
        txs[0] = 0x6BF02DCF
        txs[1] = "magic.rsp"
    elif tx=="苍白纸人":
        txs[0] = 0x899DFF11
        txs[1] = "magic.rsp"
    elif tx=="断线木偶" or tx=="无魂傀儡":
        txs[0] = 0x23EBA54C
        txs[1] = "addon.rsp"
    elif tx=="鬼泣" or tx=="惊魂铃":
        txs[0] = 0x96E5FD5D
        txs[1] = "magic.rsp"
    elif tx=="失心钹" :
        txs[0] = 0xB5DC4541
        txs[1] = "magic.rsp"
    elif tx=="乾坤玄火塔" :
        txs[0] = 0xE4A2B66E
        txs[1] = "magic.rsp"
    elif tx=="状态_摄魂" or tx=="摄魂" :
        txs[0] = 0xE02F2E6D
        txs[1] = "magic.rsp"
    elif tx=="状态_断线木偶" or tx=="状态_无魂傀儡":
        txs[0] = 0xEAA3EC9B
        txs[1] = "addon.rsp"
    elif tx=="妙手回春":
        txs[0] = 51617616
        txs[1] = "magic.rsp"
    elif tx=="凝神诀":
        txs[0] = 2128818470
        txs[1] = "magic.rsp"
    elif tx=="千里神行":
        txs[0] = 3356723242
        txs[1] = "magic.rsp"
    elif tx=="水攻":
        txs[0] = 4180877467
        txs[1] = "magic.rsp"
    elif tx=="碎星诀":
        txs[0] = 2704907892
        txs[1] = "common/lbc.rsp"
    elif tx=="尸腐毒":
        txs[0] = 353158077
        txs[1] = "magic.rsp"
    elif tx=="自爆":
        txs[0] = 0xA5199709
        txs[1] = "magic.rsp"
    elif tx=="捕捉开始":
        txs[0] = 3195920150
        txs[1] = "addon.rsp"
    elif tx=="满天花雨":
        txs[0] = 2640278135
        txs[1] = "magic.rsp"
    elif tx=="似玉生香" or tx=="碎玉弄影":
        txs[0] = 1187493750
        txs[1] = "magic.rsp"
    elif tx=="状态_似玉生香":
        txs[0] = 0x59D77EF9
        txs[1] = "waddon.rsp"
    elif tx=="状态_象形":
        txs[0] = 0x3646A4D9
        txs[1] = "waddon.rsp"
    elif tx=="状态_慧眼":
        txs[0] = 0x3646A4D9
        txs[1] = "waddon.rsp"
    elif tx=="状态_雾杀":
        txs[0] = 1506044316
        txs[1] = "common/sml.rsp"
    elif tx=="落岩":
        txs[0] = 180555238
        txs[1] = "magic.rsp"
    elif tx=="回魂咒":
        txs[0] = 2391977602
        txs[1] = "magic.rsp"
    elif tx=="韦陀护法":
        txs[0] = 2493890284
        txs[1] = "magic.rsp"
    elif tx=="烟雨剑法":
        txs[0] = 3496024499
        txs[1] = "magic.rsp"
    elif tx=="飘渺式":
        txs[0] = 3496024499
        txs[1] = "magic.rsp"
    elif tx=="百万神兵":
        txs[0] = 2340755185
        txs[1] = "magic.rsp"
    elif tx=="巨岩破":
        txs[0] = 0xDED2253F
        txs[1] = "magic.rsp"
    elif tx=="惊心一剑":
        txs[0] = 1000651155
        txs[1] = "addon.rsp"
    elif tx=="破釜沉舟" or tx=="致命":
        txs[0] = 0xB0B36693
        txs[1] = "magic.rsp"
    elif tx=="落魄符":
        txs[0] = 1337287235
        txs[1] = "magic.rsp"
    elif tx=="水遁":
        txs[0] = 1280017893
        txs[1] = "magic.rsp"
        #elif tx=="泰山压顶":
        txs[0] = 2017434912
        txs[1] = "magic.rsp"
    elif tx=="泰山压顶1":
        txs[0] = 0xDF4C3BE3
        txs[1] = "magic.rsp"
    elif tx=="泰山压顶2":
        txs[0] = 0xE9401B00
        txs[1] = "magic.rsp"
    elif tx=="泰山压顶3":
        txs[0] = 0x133F8E31
        txs[1] = "magic.rsp"
    elif tx=="达摩护体" or tx=="状态_达摩护体":
        txs[0] = 2565901429
        txs[1] = "magic.rsp"
    elif tx=="地涌金莲":
        txs[0] = 3231850111
        txs[1] = "common/wdd.rsp"
    elif tx=="杀气诀":
        #txs[0] = 3264874295
        #txs[1] = "magic.rsp"
        txs[0] = 0xC29A0737
        txs[1] = "magic.rsp"
    elif tx=="雨落寒沙":
        txs[0] = 0x303AA671
        txs[1] = "magic.rsp"
    elif tx=="雨落寒沙_反":
        txs[0] = 0x665F869A
        txs[1] = "magic.rsp"

    elif tx=="龙卷雨击1":
        txs[0] = 3911640280
        txs[1] = "magic.rsp"
        # elif tx=="地狱烈火": #小火焰
        #     txs[0] = 0x257635EE
        #     txs[1] = "magic.rsp"
        # elif tx=="地狱烈火2": #大火焰
        #     txs[0] = 0xBE325D99
        #     txs[1] = "magic.rsp"
    elif tx == "地狱烈火":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火1":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火2":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火3":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火4":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火5":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火6":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火7":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火8":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火9":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火10":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火11":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火12":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火13":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火14":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火15":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火16":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火17":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火18":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火19":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火20":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火21":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火22":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火23":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火24":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火25":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火26":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火27":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火28":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火29":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火30":
        txs[0] = 0xBE325D99
        txs[1] = "magic.rsp"
    elif tx == "地狱烈火31":
        txs[0] = 0x257635EE
        txs[1] = "magic.rsp"
    elif tx=="炎护":
        txs[0] = 1863894572
        txs[1] = "common/sml.rsp"
    elif tx=="加血":
        txs[0] = 2010253357
        txs[1] = "addon.rsp"
    elif tx=="杳无音讯" or tx=="凋零之歌":
        txs[0] = 2709550029
        txs[1] = "magic.rsp"
    elif tx=="苍茫树":
        txs[0] = 2630577796
        txs[1] = "magic.rsp"
    elif tx=="裂石":
        txs[0] = 741439825
        txs[1] = "common/lbc.rsp"
    elif tx=="断岳势":
        txs[0] = 741439825
        txs[1] = "common/lbc.rsp"
    elif tx=="推气过宫":
        txs[0] = 3899242890
        txs[1] = "magic.rsp"
    elif tx=="清风望月":
        txs[0] = 0x6BA62F2C
        txs[1] = "magic.wd1"
    elif tx=="天命剑法":
        txs[0] = 0x352F1BBD
        txs[1] = "magic.wd1"
    elif tx=="状态_金刚护体":
        txs[0] = 916220457
        txs[1] = "waddon.rsp"
    elif tx=="离魂符":
        txs[0] = 421114130
        txs[1] = "magic.rsp"
    elif tx=="加愤怒":
        txs[0] = 2156718962
        txs[1] = "addon.rsp"
    elif tx=="五雷轰顶":
        txs[0] = 4292234442
        txs[1] = "magic.rsp"
    elif tx=="冰清诀" or tx=="晶清诀" or tx=="玉清诀" or tx=="水清诀" or tx=="同生共死":
        txs[0] = 388205471
        txs[1] = "magic.rsp"
    elif tx=="楚楚可怜":
        txs[0] = 405595707
        txs[1] = "magic.rsp"
    elif tx=="佛门普渡":
        txs[0] = 428453890
        txs[1] = "magic.rsp"
    elif tx=="防御":
        txs[0] = 908223343
        txs[1] = "addon.rsp"
    elif tx=="天神护体":
        txs[0] = 3231493430
        txs[1] = "magic.rsp"
    elif tx=="龙卷雨击4":
        txs[0] = 1459200517
        txs[1] = "magic.rsp"
    elif tx=="活血":
        txs[0] = 51617616
        txs[1] = "magic.rsp"
    elif tx=="雷击":
        txs[0] = 238079300
        txs[1] = "magic.rsp"
    elif tx=="天蚕丝":
        txs[0] = 341882911
        txs[1] = "magic.rsp"
    elif tx=="天罗地网":
        txs[0] = 513152598
        txs[1] = "magic.rsp"
    elif tx=="状态_天罗地网":
        txs[0] = 0x8F3E73D5
        txs[1] = "waddon.rsp"
    elif tx=="罗汉金钟":
        txs[0] = 0xE8725FA6
        txs[1] = "other.rsp"
    elif tx=="状态_罗汉金钟":
        txs[0] = 0x549F4D24 #0x5C5C1544
        txs[1] = "waddon.rsp"
    elif tx=="莲心剑意" or tx=="状态_莲心剑意":
        txs[0] = 0x2D1E688F
        txs[1] = "waddon.rsp"
    elif tx=="状态_爪印":
        txs[0] = 0xA5D7B0F7
        txs[1] = "waddon.rsp"
    elif tx=="威慑":
        txs[0] = 0x1EB0026B
        txs[1] = "magic.rsp"
    elif tx=="状态_威慑":
        txs[0] = 0xA9C8EA87
        txs[1] = "waddon.rsp"
    elif tx=="状态_怒火":
        txs[0] = 0x6350B9E4
        txs[1] = "waddon.rsp"
    elif tx=="波澜不惊" or tx=="状态_波澜不惊":
        txs[0] = 0x32D3023F
        txs[1] = "waddon.rsp"
    elif tx=="魔息术":
        txs[0] = 0xCC2B471C #BEC7680A
        txs[1] = "waddon.rsp"
    elif tx=="状态_魔息术":
        txs[0] = 0xCC2B471C #BEC7680A
        txs[1] = "waddon.rsp"
    elif tx=="天神护法":
        txs[0] = 1935690327
        txs[1] = "magic.rsp"
    elif tx=="状态_夺魄令":
        txs[0] = 566328485
        txs[1] = "common/wdd.rsp"
    elif tx=="牛刀小试":
        txs[0] = 1000651155
        txs[1] = "addon.rsp"
    elif tx=="二龙戏珠":
        txs[0] = 2793449505
        txs[1] = "magic.rsp"
    elif tx=="盘丝阵":
        txs[0] = 1774142217
        txs[1] = "magic.rsp"
    elif tx=="惊魂掌":
        txs[0] = 3285527731
        txs[1] = "common/wdd.rsp"
    elif tx=="状态_尸腐毒":
        txs[0] = 2208088730
        txs[1] = "waddon.rsp"
    elif tx=="四海升平":
        txs[0] = 3497509792
        txs[1] = "magic.rsp"
    elif tx=="雷霆万钧":
        txs[0] = 664467571
        txs[1] = "magic.rsp"
    elif tx=="状态_韦陀护法":
        txs[0] = 2243155697
        txs[1] = "waddon.rsp"
    elif tx=="移形换影":
        txs[0] = 1963789198
        txs[1] = "magic.rsp"
    elif tx=="坐莲":
        txs[0] = 1915810093
        txs[1] = "magic.rsp"
    elif tx=="后发制人":
        txs[0] = 968268166
        txs[1] = "magic.rsp"
    elif tx=="阎罗令":
        txs[0] = 2662404697
        txs[1] = "magic.rsp"
    elif tx=="飞镖":
        txs[0] = 0x494DC152
        txs[1] = "addon.rsp"
    elif tx=="飞砂走石1":
        txs[0] = 0x2ABF191D
        txs[1] = "magic.rsp"
    elif tx=="飞砂走石2":
        txs[0] = 0x49CBD108
        txs[1] = "magic.rsp"
    elif tx=="飞砂走石":
        txs[0] = 0x49CBD108
        txs[1] = "magic.rsp"
    elif tx=="红袖添香":
        txs[0] = 3858048292
        txs[1] = "magic.rsp"
    elif tx=="状态_追魂符":
        txs[0] = 3655438388
        txs[1] = "waddon.rsp"
    elif tx=="牛屎遁":
        txs[0] = 2938873934
        txs[1] = "magic.rsp"
    elif tx=="状态_乾坤玄火塔_敌方":
        txs[0] = 0x325A1F6A
        txs[1] = "waddon.rsp"
    elif tx=="状态_乾坤玄火塔_我方" or tx=="状态_乾坤玄火塔" :
        txs[0] = 0xC236BF21
        txs[1] = "waddon.rsp"
    elif tx=="横扫千军":
        txs[0] = 2896471370
        txs[1] = "magic.rsp"
    elif tx=="命归术":
        txs[0] = 821212684
        txs[1] = "magic.rsp"
    elif tx=="炼气化神":
        txs[0] = 910697598
        txs[1] = "magic.rsp"
    elif tx=="煞气诀":
        txs[0] = 0x5229F242
        txs[1] = "magic.rsp"
    elif tx=="野兽之力" or tx=="魔兽之印":
        txs[0] = 0x203B8C75
        txs[1] = "magic.rsp"
    elif tx=="状态_煞气诀":
        txs[0] = 0x98753F94
        txs[1] = "waddon.rsp"
    elif tx=="移魂化骨":
        txs[0] = 330324521
        txs[1] = "common/wdd.rsp"
    elif tx=="推拿":
        txs[0] = 51617616
        txs[1] = "magic.rsp"
    elif tx=="状态_红袖添香":
        txs[0] = 3037907947
        txs[1] = "waddon.rsp"
    elif tx=="日月乾坤":
        txs[0] = 2802651747
        txs[1] = "magic.rsp"
    elif tx=="状态_楚楚可怜":
        txs[0] = 1923968442
        txs[1] = "waddon.rsp"
    elif tx=="状态_上古灵符" or tx=="状态_长驱直入_挨打方":
        txs[0] = 0x2CE2133E
        txs[1] = "waddon.rsp"
    elif tx=="追魂符":
        txs[0] = 3556918902
        txs[1] = "magic.rsp"
    elif tx=="状态_离魂符":
        txs[0] = 3655438388
        txs[1] = "waddon.rsp"
    elif tx=="神龙摆尾":
        txs[0] = 0xA4790CE1
        txs[1] = "magic.rsp"
    elif tx=="状态_神龙摆尾":
        txs[0] = 0xF184BD59
        txs[1] = "waddon.rsp"
    elif tx=="状态_百万神兵":
        txs[0] = 3297426043
        txs[1] = "waddon.rsp"
    elif tx=="烈火":
        txs[0] = 3507654973
        txs[1] = "magic.rsp"
    elif tx=="状态_定心术":
        txs[0] = 0x2D07CCEC
        txs[1] = "magic.rsp"
    elif tx=="定心术":
        txs[0] = 0x2D07CCEC
        txs[1] = "magic.rsp"
    elif tx=="状态_变身" or tx=="变身":
        txs[0] = 702028255
        txs[1] = "magic.rsp"
    elif tx=="破血狂攻":
        txs[0] = 387269810
        txs[1] = "addon.rsp"
    elif tx=="鹰击":
        txs[0] = 0x82C9074A
        txs[1] = "magic.rsp"
    elif tx=="弓弩攻击":
        txs[0] = 3804004647
        txs[1] = "common/lbc.rsp"
    elif tx=="状态_蓝灯" or tx =="状态_炼气化神":
        txs[0] = 1906144895
        txs[1] = "waddon.rsp"
    elif tx=="状态_红灯":
        txs[0] = 4176381242
        txs[1] = "waddon.rsp"
    elif tx=="状态_生命之泉":
        txs[0] = 4176381242
        txs[1] = "waddon.rsp"
    elif tx=="状态_定身符":
        txs[0] = 2461182746
        txs[1] = "waddon.rsp"
    elif tx=="状态_不动如山":
        txs[0] = 281904888
        txs[1] = "common/lbc.rsp"
    elif tx=="金刚护体" or tx=="法术防御":
        txs[0] = 952243307
        txs[1] = "magic.rsp"
    elif tx=="龙卷雨击3":
        txs[0] = 3514247917
        txs[1] = "magic.rsp"
    elif tx=="浪涌":
        txs[0] = 1065487884
        txs[1] = "common/lbc.rsp"
    elif tx=="状态_如花解语":
        txs[0] = 505084121
        txs[1] = "waddon.rsp"
    elif tx=="气归术":
        txs[0] = 3497509792
        txs[1] = "magic.rsp"
    elif tx=="天崩地裂":
        txs[0] = 2761456237
        txs[1] = "common/lbc.rsp"
    elif tx=="龙吟":
        txs[0] = 1667259533
        txs[1] = "magic.rsp"
    elif tx=="状态_莲步轻舞":
        txs[0] = 3387695093
        txs[1] = "waddon.rsp"
    elif tx=="加蓝":
        txs[0] = 1049700101
        txs[1] = "addon.rsp"
    elif tx=="狮搏":
        txs[0] = 1754178891
        txs[1] = "addon.rsp"
    elif tx=="尘土刃":
        txs[0] = 2645145495
        txs[1] = "common/sml.rsp"
    elif tx=="状态_明光宝烛":
        txs[0] = 540412418
        txs[1] = "common/wdd.rsp"
    elif tx=="判官令":
        txs[0] = 605841034
        txs[1] = "magic.rsp"
    elif tx=="状态_冻结":
        txs[0] = 0x118ABCFD
        txs[1] = "waddon.rsp"
    elif tx=="状态_摧心术":
        txs[0] = 2126428619
        txs[1] = "common/wdd.rsp"
    elif tx=="状态_惊魂掌":
        txs[0] = 2156799976
        txs[1] = "common/wdd.rsp"
    elif tx=="乾坤袋":
        txs[0] = 0x6BA62F2C
        txs[1] = "magic.wd1"
    elif tx=="错乱":
        txs[0] = 783501166
        txs[1] = "magic.rsp"
    elif tx=="状态_炎护":
        txs[0] = 2336654137
        txs[1] = "common/sml.rsp"
    elif tx=="状态_后发制人":
        txs[0] = 707397219
        txs[1] = "waddon.rsp"
    elif tx=="阵型_不动如山":
        txs[0] = 4106238113
        txs[1] = "wzife.wd2"
    elif tx=="状态_碎星诀" or tx=="状态_蜜润":
        txs[0] = 814399755
        txs[1] = "common/lbc.rsp"
    elif tx=="心疗术":
        txs[0] = 4227373440
        txs[1] = "magic.rsp"
    elif tx=="天魔解体":
        txs[0] = 0xD20E78BF
        txs[1] = "magic.rsp"
    elif tx=="状态_日月乾坤":
        txs[0] = 826002553
        txs[1] = "waddon.rsp"
    elif tx=="魔王回首":
        txs[0] = 0x16B27FFC
        txs[1] = "magic.rsp"
    elif tx=="状态_魔王回首":
        txs[0] = 0xBBEA83F4
        txs[1] = "waddon.rsp"
    elif tx=="极度疯狂":
        txs[0] = 0x16B27FFC
        txs[1] = "magic.rsp"
    elif tx=="状态_极度疯狂":
        txs[0] = 0xBBEA83F4
        txs[1] = "waddon.rsp"
    elif tx=="状态" or tx=="状态_天魔解体":
        txs[0] = 0xA168E26F
        txs[1] = "waddon.rsp"
    elif tx=="状态_死地":
        txs[0] = 0x566DC0F3
        txs[1] = "waddon.rsp"
    elif tx=="状态_背水":
        txs[0] = 0xE0AF1925
        txs[1] = "waddon.rsp"
    elif tx=="修罗隐身":
        txs[0] = 0x3E795B5A
        txs[1] = "magic.rsp"
    elif tx=="状态_修罗隐身" or tx=="状态_水清诀" or tx=="状态_玉清诀" or tx=="状态_晶清诀"  or tx=="状态_反间计":
        txs[0] = 0x566DC0F3
        txs[1] = "waddon.rsp"
    elif tx=="状态_凝神术" or tx=="凝神术":
        txs[0] = 0x566DC0F3
        txs[1] = "waddon.rsp"
    elif tx=="状态_盘丝阵":
        txs[0] = 0x369C6A29
        txs[1] = "waddon.rsp"
    elif tx=="落叶萧萧" or tx=="风卷残云":
        txs[0] = 0xBD677226
        txs[1] = "common/sml.rsp"
    elif tx=="落叶萧萧2":
        txs[0] = 0x94931579
        txs[1] = "common/sml.rsp"
    elif tx=="状态_象形":
        txs[0] = 2213550572
        txs[1] = "waddon.rsp"
    elif tx=="水漫金山":
        txs[0] = 2431146143
        txs[1] = "magic.rsp"
    elif tx=="水漫金山2":
        txs[0] = 0x97311BAD
        txs[1] = "magic.rsp"
    elif tx=="水漫金山3":
        txs[0] = 0x9FE48849
        txs[1] = "magic.rsp"
    elif tx=="水漫金山4":
        txs[0] = 0x6EFC43B9
        txs[1] = "magic.rsp"
    elif tx=="泰山压顶":
        txs[0] = 0x00010033
        txs[1] = "other.rsp"
    elif tx=="泰山压顶2":
        txs[0] = 0xDF4C3BE3
        txs[1] = "magic.rsp"
    elif tx=="八凶法阵":
        txs[0] = 0x139426B5
        txs[1] = "magic.rsp"
    elif tx=="天降灵葫":
        txs[0] = 0xF99822CE#0x15016B39
        txs[1] = "magic.rsp"
    elif tx=="叱咤风云":
        txs[0] = 0xA19EAB31
        txs[1] = "magic.rsp"
    elif tx=="天雷斩":
        txs[0] = 3054771897
        txs[1] = "addon.rsp"
    elif tx=="状态_紧箍咒":
        txs[0] = 4024909497
        txs[1] = "waddon.rsp"
    elif tx=="命疗术":
        txs[0] = 4088602190
        txs[1] = "magic.rsp"
    elif tx=="状态_失心符" or tx=="状态_顺势而为":
        txs[0] = 3635978625
        txs[1] = "waddon.rsp"
    elif tx=="钟馗论道" or tx=="状态_钟馗论道":
        txs[0] = 0xDCCB25E2
        txs[1] = "waddon.rsp"
    elif tx=="定身符":
        txs[0] = 3729668740
        txs[1] = "magic.rsp"
    elif tx=="摧心术":
        txs[0] = 2702496872
        txs[1] = "common/wdd.rsp"
    elif tx=="碎甲术" or tx=="破甲术":
        txs[0] = 3505309973
        txs[1] = "magic.rsp"
    elif tx=="夺命咒":
        txs[0] = 2699497351
        txs[1] = "common/wdd.rsp"
    elif tx=="状态_一苇渡江":
        txs[0] = 382287583
        txs[1] = "waddon.rsp"
    elif tx=="一苇渡江":
        txs[0] = 4082420920
        txs[1] = "magic.rsp"
    elif tx=="凝气诀":
        txs[0] = 843116756
        txs[1] = "magic.rsp"
    elif tx=="状态_乘风破浪":
        txs[0] = 3366209335
        txs[1] = "waddon.rsp"
    elif tx=="状态_逆鳞":
        txs[0] = 4066099146
        txs[1] = "waddon.rsp"
    elif tx=="状态_冰封":
        txs[0] = 324036383
        txs[1] = "waddon.rsp"
    elif tx=="如花解语":
        txs[0] = 2319038367
        txs[1] = "magic.rsp"
    elif tx=="状态_杀气诀":
        txs[0] = 0x62EDD1CB
        txs[1] = "waddon.rsp"
    elif tx=="幽冥鬼眼":
        txs[0] = 0x07DF52CA
        txs[1] = "magic.rsp"
    elif tx=="状态_幽冥鬼眼":
        txs[0] = 0x21435203
        txs[1] = "waddon.rsp"
    elif tx=="保护":
        txs[0] = 4027829983
        txs[1] = "addon.rsp"
    elif tx=="复苏":
        txs[0] = 3698682735
        txs[1] = "magic.rsp"
    elif tx=="镇妖":
        txs[0] = 0x1EB0026B
        txs[1] = "magic.rsp"
    elif tx=="状态_镇妖":
        txs[0] = 0x98753F94
        txs[1] = "waddon.rsp"
    elif tx=="状态_催眠符":
        txs[0] = 3398426285
        txs[1] = "waddon.rsp"
    elif tx=="状态_横扫千军" or tx=="状态_连环击" or tx=="状态_破釜沉舟" or tx=="状态_天命剑法":
        txs[0] = 3645258252
        txs[1] = "waddon.rsp"
    elif tx=="还阳术":
        txs[0] = 1538345049
        txs[1] = "magic.rsp"
    elif tx=="状态_毒":
        txs[0] = 3687768876
        txs[1] = "waddon.rsp"
    elif tx=="月光":
        txs[0] = 685510219
        txs[1] = "common/ski.rsp"
    elif tx=="含情脉脉":
        txs[0] = 1399041837
        txs[1] = "magic.rsp"
    elif tx=="状态_错乱":
        txs[0] = 2557820820
        txs[1] = "waddon.rsp"
    elif tx=="纵地金光" or tx=="观照万象":
        txs[0] = 3546433571
        txs[1] = "common/lbc.rsp"
    elif tx=="血雨":
        txs[0] = 0x53E46986
        txs[1] = "magic.rsp"
    elif tx=="普渡众生":
        txs[0] = 804734328
        txs[1] = "magic.rsp"
    elif tx=="状态_颠倒五行":
        txs[0] = 923673984
        txs[1] = "magic.rsp"
    elif tx=="催眠符":
        txs[0] = 2663408206
        txs[1] = "magic.rsp"
    elif tx=="冰川怒":
        txs[0] = 1425547471
        txs[1] = "common/sml.rsp"
    elif tx=="状态_落魄符":
        txs[0] = 3635978625
        txs[1] = "waddon.rsp"
    elif tx=="气疗术":
        txs[0] = 4088602190
        txs[1] = "magic.rsp"
    elif tx=="起死回生":
        txs[0] = 2391977602
        txs[1] = "magic.rsp"
    elif tx=="力劈华山":
        txs[0] = 4281577710
        txs[1] = "magic.rsp"
    elif tx=="叶隐":
        txs[0] = 1859374553
        txs[1] = "common/sml.rsp"
    elif tx=="失心符" or tx=="顺势而为":
        txs[0] = 152755655
        txs[1] = "magic.rsp"
    elif tx=="腾云驾雾":
        txs[0] = 871130409
        txs[1] = "magic.rsp"
    elif tx=="不动如山":
        txs[0] = 4106497964
        txs[1] = "common/lbc.rsp"
    elif tx=="乙木仙遁" or tx=="分身术":
        txs[0] = 1829610500
        txs[1] = "magic.rsp"
    elif tx=="解毒":
        txs[0] = 3727996990
        txs[1] = "magic.rsp"
    elif tx=="奔雷咒":
        txs[0] = 4115415077
        txs[1] = "magic.rsp"
    elif tx=="奔雷咒2":
        txs[0] = 0xF1F26922
        txs[1] = "magic.rsp"
    elif tx=="奔雷咒3":
        txs[0] = 0x2A997658
        txs[1] = "magic.rsp"
    elif tx=="明光宝烛":
        txs[0] = 1479134995
        txs[1] = "common/wdd.rsp"
    elif tx=="状态_移魂化骨":
        txs[0] = 759125516
        txs[1] = "common/wdd.rsp"
    elif tx=="唧唧歪歪":
        txs[0] = 3240896099
        txs[1] = "magic.rsp"
    elif tx=="连环击":
        txs[0] = 1441516140
        txs[1] = "addon.rsp"
    elif tx=="被击中":
        txs[0] = 490729788
        txs[1] = "addon.rsp"
    elif tx=="翻江搅海":
        txs[0] = 3385103645
        txs[1] = "common/lbc.rsp"
    elif tx=="落雷符":
        txs[0] = 4292234442
        txs[1] = "magic.rsp"
    elif tx=="日光华":
        txs[0] = 1170905363
        txs[1] = "magic.rsp"
    elif tx=="地裂火":
        txs[0] = 417414121
        txs[1] = "magic.rsp"
    elif tx=="解封":
        txs[0] = 1833750106
        txs[1] = "magic.rsp"

    elif tx=="魔音摄魂":
        txs[0] = 0x16B27FFC
        txs[1] = "magic.rsp"

    elif tx=="状态_魔音摄魂":
        txs[0] = 0xD9463A0C
        txs[1] = "waddon.rsp"

    elif tx=="反震":
        txs[0] = 3690777786
        txs[1] = "addon.rsp"
    elif tx=="蜜润":
        txs[0] = 3298164407
        txs[1] = "common/sml.rsp"
    elif tx=="三花聚顶":
        txs[0] = 2002768611
        txs[1] = "magic.rsp"
    elif tx=="暴击":
        txs[0] = 3973111811
        txs[1] = "magic.rsp"
    elif tx=="死亡召唤":
        txs[0] = 0x4E02EC44
        txs[1] = "magic.rsp"
    elif tx=="壁垒击破":
        txs[0] = 0x99DDC32A
        txs[1] = "magic.rsp"
    elif tx=="善恶有报":
        txs[0] = 0xDBFCCCBA
        txs[1] = "addon.rsp"

    elif tx=="状态_天神护法":
        txs[0] = 3562887539
        txs[1] = "waddon.rsp"
    elif tx=="荆棘舞":
        txs[0] = 636234317
        txs[1] = "common/sml.rsp"
    elif tx=="三昧真火":
        txs[0] = 0xFCDCCCEC
        txs[1] = "magic.rsp"
    elif tx=="我佛慈悲":
        txs[0] = 540772211
        txs[1] = "magic.rsp"
    elif tx=="慈航普度":
        txs[0] = 0xE1084D39
        txs[1] = "magic.rsp"
    elif tx=="紧箍咒":
        txs[0] = 1417725769
        txs[1] = "magic.rsp"
    elif tx=="杨柳甘露" or tx=="莲花心音":
        txs[0] = 939734977
        txs[1] = "magic.rsp"
    elif tx=="莲步轻舞":
        txs[0] = 2556614190
        txs[1] = "magic.rsp"
    elif tx=="靛沧海":
        txs[0] = 1818198902
        txs[1] = "magic.rsp"
    elif tx=="五雷咒":
        txs[0] = 947658475
        txs[1] = "magic.rsp"
    elif tx=="龙卷雨击2":
        txs[0] = 3592299801
        txs[1] = "magic.rsp"
    elif tx=="龙吟1":
        txs[0] = 0xA5199709
        txs[1] = "magic.rsp"
    elif tx=="龙吟2":
        txs[0] = 0x5EC2D5BB
        txs[1] = "magic.rsp"
    elif tx=="龙吟3":
        txs[0] = 0x3D74BE12
        txs[1] = "magic.rsp"
    elif tx=="龙吟4":
        txs[0] = 0x63605C8D
        txs[1] = "magic.rsp"
    elif tx=="龙吟5":
        txs[0] = 0x9FE48849
        txs[1] = "magic.rsp"
    elif tx=="摄魄":
        txs[0] = 1505585649
        txs[1] = "magic.rsp"
    elif tx=="生命之泉":
        txs[0] = 3537672915
        txs[1] = "magic.rsp"
    elif tx=="颠倒五行":
        txs[0] = 923673984
        txs[1] = "magic.rsp"
    elif tx=="乘风破浪":
        txs[0] = 1172493695
        txs[1] = "magic.rsp"
    elif tx=="捕捉成功":
        txs[0] = 2601915514
        txs[1] = "addon.rsp"
    elif tx=="清心":
        txs[0] = 822452251
        txs[1] = "magic.rsp"
    elif tx=="状态_天神护体":
        txs[0] = 1724676649
        txs[1] = "waddon.rsp"
    elif tx=="勾魂":
        txs[0] = 457649967
        txs[1] = "magic.rsp"
    elif tx=="振翅千里":
        txs[0] = 2661053669
        txs[1] = "magic.rsp"
    elif tx=="逆鳞":
        txs[0] = 81488906
        txs[1] = "magic.rsp"
    elif tx=="安神诀":
        txs[0] = 0xE61DB8B4
        txs[1] = "waddon.rsp"
    elif tx=="状态_安神诀":
        txs[0] = 0xE61DB8B4
        txs[1] = "waddon.rsp"
    elif tx=="象形" or tx=="BOSS绝杀":
        txs[0] = 3188881443
        txs[1] = "magic.rsp"
    elif tx=="惊涛怒":
        txs[0] = 3197608773
        txs[1] = "common/lbc.rsp"
    elif tx=="反间之计":
        txs[0] = 1804814488
        txs[1] = "magic.rsp"
    elif tx=="星月之惠":
        txs[0] = 3298164407
        txs[1] = "common/sml.rsp"
    elif tx=="斗转星移":
        txs[0] = 1056770863
        txs[1] = "magic.rsp"
    elif tx=="状态_含情脉脉":
        txs[0] = 2164502482
        txs[1] = "waddon.rsp"
    elif tx=="雾杀" or tx=="催化":
        txs[0] = 1264783402
        txs[1] = "common/sml.rsp"
    elif tx=="夺魄令":
        txs[0] = 2668097987
        txs[1] = "common/wdd.rsp"
    elif tx=="上古灵符":
        #print("特效上古灵符")
        txs[0] = 48901659
        txs[1] = "magic.rsp"
    elif tx=="升级":
        txs[0] = 2604332261
        txs[1] = "addon.rsp"
    elif tx=="菩提心佑" or tx=="状态_菩提心佑":
        txs[0] = 0x042B06AC
        txs[1] = "waddon.rsp"
    elif tx=="天地同寿":
        txs[0] = 0x21F550FF
        txs[1] = "magic.rsp"
    elif tx=="状态_天地同寿":
        txs[0] = 0xFAD3AD96
        txs[1] = "waddon.rsp"
    elif tx=="乾坤妙法":
        txs[0] = 0x184AA512
        txs[1] = "magic.rsp"
    elif tx=="状态_乾坤妙法":
        txs[0] = 0x7F842CEF
        txs[1] = "waddon.rsp"
    elif tx=="放下屠刀" or tx=="河东狮吼":
        txs[0] = 0x81B4599F
        txs[1] = "magic.rsp"
    elif tx=="夜舞倾城":
        txs[0] = 0xF18C76DD
        txs[1] = "magic.rsp"
    elif tx=="打狗棒":
        txs[0] = 0x1EE9406C
        txs[1] = "magic.rsp"
    elif tx=="驱魔" or tx=="驱尸":
        txs[0] = 0x726AC447
        txs[1] = "magic.rsp"
    elif tx=="寡欲令":
        txs[0] = 0xFDE4BF24
        txs[1] = "magic.rsp"
    elif tx=="破碎无双":
        txs[0] = 0x21FAE73F
        txs[1] = "magic.rsp"
    elif tx=="状态_寡欲令" or tx=="状态_驱魔":
        txs[0] = 0xE89A19DF
        txs[1] = "waddon.rsp"
    elif tx=="金刚护法" or tx=="诸天看护":
        txs[0] = 0x04DB6C0A
        txs[1] = "magic.rsp"
    elif tx=="状态_金刚护法":
        txs[0] = 0x16B27FFC
        txs[1] = "magic.rsp"
    elif tx=="归元咒" :
        txs[0] = 0x517656E2
        txs[1] = "magic.rsp"
    elif tx=="乾天罡气":
        txs[0] = 0x144AF3F8
        txs[1] = "magic.rsp"
    elif tx=="宁心":
        txs[0] = 0xA72FDB18
        txs[1] = "magic.rsp"
    elif tx=="状态_宁心":
        txs[0] = 0x7DCEE534
        txs[1] = "waddon.rsp"
    elif tx=="牛劲" or tx=="状态_牛劲":
        txs[0] = 0x26F090BE
        txs[1] = "magic.rsp"
    elif tx=="失魂符":
        txs[0] = 0x7BCD8BC0
        txs[1] = "magic.rsp"
    elif tx=="碎甲符"or tx=="飞符炼魂" :
        txs[0] = 0xC27C1229
        txs[1] = "magic.rsp"
    elif tx=="状态_失魂符":
        txs[0] = 0x8B43833D
        txs[1] = "waddon.rsp"
    elif tx=="状态_碎甲符":
        txs[0] = 0xEB3D0AC1
        txs[1] = "waddon.rsp"
    elif tx=="飞花摘叶":
        txs[0] = 0x78BF64A4
        txs[1] = "magic.rsp"
    elif tx=="百毒不侵":
        txs[0] = 0xD69CAE82
        txs[1] = "magic.rsp"
    elif tx=="一笑倾城":
        txs[0] = 0x430A96A6
        txs[1] = "magic.rsp"
    elif tx=="状态_百毒不侵":
        txs[0] = 0x860E67C9
        txs[1] = "waddon.rsp"
    elif tx=="状态_一笑倾城":
        txs[0] = 0x760B7BD7
        txs[1] = "waddon.rsp"
    elif tx=="状态_血雨":
        txs[0] = 0x497E890D
        txs[1] = "waddon.rsp"
    elif tx=="状态_护法紫丝":
        txs[0] = 0x042B06AC
        txs[1] = "waddon.rsp"
    elif tx=="状态_激怒":
        txs[0] = 0x5816CDC7
        txs[1] = "waddon.rsp"
    elif tx=="状态_佛法无边":
        txs[0] = 0xEA4D704A
        txs[1] = "waddon.rsp"
    elif tx=="佛法无边":
        txs[0] = 0xC8011EF1
        txs[1] = "magic.rsp"
    elif tx=="舍生取义" or tx=="妙悟" :
        txs[0] = 0xF0CE9045
        txs[1] = "magic.rsp"
    elif tx=="状态_普渡众生" :
        txs[0] = 0xD8857128
        txs[1] = "waddon.rsp"
    elif tx=="状态_灵动九天" :
        txs[0] = 0x95FF4460
        txs[1] = "waddon.rsp"
    elif tx=="火甲术" :
        txs[0] = 0x4B621DF7
        txs[1] = "magic.rsp"
    elif tx=="状态_火甲术" :
        txs[0] = 0x82D17DF8
        txs[1] = "waddon.rsp"
    elif tx=="状态_鹰击" :
        txs[0] = 0x58628406
        txs[1] = "waddon.rsp"
    elif tx=="状态_凋零之歌" :
        txs[0] = 0xBE4CC51E
        txs[1] = "waddon.rsp"
    elif tx=="善恶有报" :
        txs[0] = 0x8D8A818D
        txs[1] = "magic.rsp"
    elif tx=="战斗暴击" :
        txs[0] = 0xECD0E003
        txs[1] = "addon.rsp"
    elif tx=="战斗头标" :
        txs[0] = 0x97C79EDB
        txs[1] = "addon.rsp"
    elif tx=="剑荡四方" :
        txs[0] = "0x729ADE62"#0xE3D6B98D
        txs[1] ="" #"common/general.rsp"
    elif tx=="打雷加电" :
        txs[0] = 0x51EEBFF3
        txs[1] ="magic.rsp"
    elif tx=="特赦令牌" :
        txs[0] = 0x7A55F632
        txs[1] ="magic.rsp"
    elif tx=="闪亮登场":
        txs[0] = 0x6DFE584A
        txs[1] = "wzife.wd2"
    elif tx=="挑战失败":
        txs[0] = 0x36F99CC8
        txs[1] = "wzife.wd2"
    
    return txs
