def get_map_name(map_id):
    if 1600 <= map_id <= 1620:
        return "迷宫" + str(map_id-1600) + "层"
    if 1600 <= map_id <= 1620:
        return "迷宫" + str(map_id-1600) + "层"
    elif map_id == 5001:
        return "宝藏山"
    elif 6010 <= map_id <= 6019:
        return "帮派竞赛"
    elif map_id == 6020:
        return "中立区"
    if map_id == 1501:
        return "建邺城"
    elif map_id == 1502:
        return "建邺兵铁铺"
    elif map_id == 1503:
        return "李记布庄"
    elif map_id == 1504:
        return "回春堂分店"
    elif map_id == 1505:
        return "东升货栈"
    elif map_id == 1523:
        return "合生记"
    elif map_id == 1524:
        return "万宇钱庄"
    elif map_id == 1526 or map_id == 1525 or map_id == 1527:
        return "建邺民居"
    elif map_id == 1534:
        return "民居内室"
    elif map_id == 1537:
        return "建邺衙门"
    elif map_id == 1506:
        return "东海湾"
    elif map_id == 1116:
        return "龙宫"
    elif map_id == 1126:
        return "东海岩洞"
    elif map_id == 1249:
        return "女魃墓"
    elif map_id == 1507:
        return "东海海底"
    elif map_id == 1508:
        return "海底沉船"
    elif map_id == 1509:
        return "沉船内室"
    elif map_id == 1193:
        return "江南野外"
    elif map_id == 1001:
        return "长安城"
    elif map_id == 1002:
        return "化生寺"
    elif map_id == 1198:
        return "大唐官府"
    elif map_id == 1054:
        return "程咬金府"
    elif map_id == 1004:
        return "大雁塔一层"
    elif map_id == 1005:
        return "大雁塔二层"
    elif map_id == 1006:
        return "大雁塔三层"
    elif map_id == 1007:
        return "大雁塔四层"
    elif map_id == 1008:
        return "大雁塔五层"
    elif map_id == 1090:
        return "大雁塔六层"
    elif map_id == 1009:
        return "大雁塔七层"
    elif map_id == 1028:
        return "长安酒店一楼"
    elif map_id == 1029:
        return "长安酒店二楼"
    elif map_id == 1020:
        return "万胜武器店"
    elif map_id == 1017:
        return "锦绣饰品店"
    elif map_id == 1019:
        return "书香斋"
    elif map_id == 1015:
        return "南北杂货店"
    elif map_id == 1013:
        return "广源钱庄"
    elif map_id == 1021:
        return "平安福寿店"
    elif map_id == 1022:
        return "张记布庄"
    elif map_id == 1030:
        return "云来酒店"
    elif map_id == 1043:
        return "藏经阁"
    elif map_id == 1528:
        return "光华殿"
    elif map_id == 1110:
        return "大唐国境"
    elif map_id == 1168:
        return "江州衙门"
    elif map_id == 1153:
        return "金山寺"
    elif map_id == 1167:
        return "江州名居2"
    elif map_id == 1258:
        return "赤水洲"
    elif map_id == 1150:
        return "凌波城"
    elif map_id == 1049:
        return "丞相府"
    elif map_id == 1056:
        return "秦府内院"
    elif map_id == 1057:
        return "秦府"
    elif map_id == 1025:
        return "冯记铁铺"
    elif map_id == 1116:
        return "龙宫"
    elif map_id == 1117:
        return "水晶宫"
    elif map_id == 1122:
        return "阴曹地府"
    elif map_id == 1140:
        return "普陀山"
    elif map_id == 1092:
        return "傲来国"
    elif map_id == 1099:
        return "傲来国钱庄"
    elif map_id == 1100:
        return "傲来国圣殿"
    elif map_id == 1101:
        return "傲来武器店"
    elif map_id == 1514:
        return "花果山"
    elif map_id == 1251:
        return "幻境花果山"
    elif map_id == 1174:
        return "北俱芦洲"
    elif map_id == 1091:
        return "长寿郊外"
    elif map_id == 1216:
        return "仙缘洞天"
    elif map_id == 1177:
        return "龙窟一层"
    elif map_id == 1178:
        return "龙窟二层"
    elif map_id == 1179:
        return "龙窟三层"
    elif map_id == 1180:
        return "龙窟四层"
    elif map_id == 1181:
        return "龙窟五层"
    elif map_id == 1182:
        return "龙窟六层"
    elif map_id == 1183:
        return "龙窟七层"
    elif map_id == 1186:
        return "凤巢一层"
    elif map_id == 1187:
        return "凤巢二层"
    elif map_id == 1188:
        return "凤巢三层"
    elif map_id == 1189:
        return "凤巢四层"
    elif map_id == 1190:
        return "凤巢五层"
    elif map_id == 1191:
        return "凤巢六层"
    elif map_id == 1192:
        return "凤巢七层"
    elif map_id == 1142:
        return "女儿村"
    elif map_id == 1143:
        return "女儿村村长家"
    elif map_id == 1127:
        return "地狱迷宫一层"
    elif map_id == 1128:
        return "地狱迷宫二层"
    elif map_id == 1129:
        return "地狱迷宫三层"
    elif map_id == 1130:
        return "地狱迷宫四层"
    elif map_id == 1118:
        return "海底迷宫一层"
    elif map_id == 1119:
        return "海底迷宫二层"
    elif map_id == 1120:
        return "海底迷宫三层"
    elif map_id == 1121:
        return "海底迷宫四层"
    elif map_id == 1532:
        return "海底迷宫五层"
    elif map_id == 1111:
        return "天宫"
    elif map_id == 1070:
        return "长寿村"
    elif map_id == 1077:
        return "长寿村药店"
    elif map_id == 1087:
        return "长寿村杂货店"
    elif map_id == 1082:
        return "长寿村神庙"
    elif map_id == 1080:
        return "长寿村村长家"
    elif map_id == 1075:
        return "长寿村酒店"
    elif map_id == 1135:
        return "方寸山"
    elif map_id == 1137:
        return "灵台宫"
    elif map_id == 1173:
        return "大唐境外"
    elif map_id == 1250:
        return "天机城"
    elif map_id == 1170:
        return "高老庄大厅"
    elif map_id == 1171:
        return "高小姐闺房"
    elif map_id == 1123:
        return "森罗殿"
    elif map_id == 1124:
        return "地藏王府"
    elif map_id == 1112:
        return "凌霄宝殿"
    elif map_id == 1512:
        return "魔王寨"
    elif map_id == 1145:
        return "魔王居"
    elif map_id == 1141:
        return "潮音洞"
    elif map_id == 1146:
        return "五庄观"
    elif map_id == 1147:
        return "乾坤殿"
    elif map_id == 1131:
        return "狮驼岭"
    elif map_id == 1132:
        return "大象洞"
    elif map_id == 1133:
        return "老雕洞"
    elif map_id == 1134:
        return "狮王洞"
    elif map_id == 1202:
        return "无名鬼城"
    elif map_id == 1201:
        return "女娲神迹"
    elif map_id == 1138:
        return "神木林"
    elif map_id == 1139:
        return "无底洞"
    elif map_id == 1513:
        return "盘丝岭"
    elif map_id == 1144:
        return "盘丝洞"
    elif map_id == 1205:
        return "战神山"
    elif map_id == 1154:
        return "神木屋"
    elif map_id == 1228:
        return "碗子山"
    elif map_id == 1156:
        return "琉璃殿"
    elif map_id == 1103:
        return "水帘洞"
    elif map_id == 1040:
        return "西梁女国"
    elif map_id == 1208:
        return "朱紫国"
    elif map_id == 1209:
        return "朱紫国皇宫"
    elif map_id == 1226:
        return "宝象国"
    elif map_id == 1227:
        return "宝象国皇宫"
    elif map_id == 1235:
        return "丝绸之路"
    elif map_id == 1042:
        return "解阳山"
    elif map_id == 1041:
        return "子母河底"
    elif map_id == 1210:
        return "麒麟山"
    elif map_id == 1211:
        return "太岁府"
    elif map_id == 1242:
        return "须弥东界"
    elif map_id == 1232:
        return "比丘国"
    elif map_id == 1207:
        return "蓬莱仙岛"
    elif map_id == 1229:
        return "波月洞"
    elif map_id == 1233:
        return "柳林坡"
    elif map_id == 1114:
        return "月宫"
    elif map_id == 1231:
        return "蟠桃园"
    elif map_id == 1203:
        return "小西天"
    elif map_id == 1204:
        return "小雷音寺"
    elif map_id == 1218:
        return "墨家村"
    elif map_id == 1221:
        return "墨家禁地"
    elif map_id == 1920:
        return "凌云渡"
    elif map_id == 1016:
        return "回春堂药店"
    elif map_id == 1033:
        return "留香阁"
    elif map_id == 1024:
        return "长风镖局"
    elif map_id == 1026:
        return "国子监书库"
    elif map_id == 1044:
        return "金銮殿"
    elif map_id == 1400:
        return "幻境"
    elif map_id == 1511:
        return "蟠桃园"
    elif map_id == 1197:
        return "比武场"
    elif map_id == 1113:
        return "兜率宫"
    elif map_id == 1095:
        return "傲来服饰店"
    elif map_id == 1083:
        return "长寿村服装店"
    elif map_id == 1085:
        return "长寿村武器店"
    elif map_id == 1003:
        return "桃源村"
    elif map_id == 2000:
        return "天魔秘境"
    elif map_id == 16050:
        return "天鸣洞天"
    elif map_id == 1125:
        return "轮回司"
    elif map_id == 6021:
        return "三清道观"
    elif map_id == 6022:
        return "道观大殿"
    elif map_id == 6023:
        return "九霄云外"
    elif map_id == 6024:
        return "水陆道场"
    elif map_id == 6025:
        return "繁华京城"
    elif map_id == 6026:
        return "妖魔巢穴"
    elif map_id == 1237:
        return "四方城"
    elif map_id == 1876:
        return "南岭山"
    elif map_id == 9000:
        return "九层妖塔入口"
    elif map_id == 9007:
        return "九层妖塔八"
    elif map_id == 9006:
        return "九层妖塔七"
    elif map_id == 9005:
        return "九层妖塔六"
    elif map_id == 9004:
        return "九层妖塔五"
    elif map_id == 9003:
        return "九层妖塔四"
    elif map_id == 9002:
        return "九层妖塔三"
    elif map_id == 9001:
        return "九层妖塔二"
    elif map_id == 9008:
        return "主墓室"
    elif map_id == 1212:
        return "琅嬛福地"
    elif map_id == 1213:
        return "炼焰谷地"
    elif map_id == 1214:
        return "冰风秘境"
    elif map_id == 1215:
        return "钟乳石窟"
    elif map_id == 9009:
        return "修炼秘境"
    elif map_id == 1885:
        return "庭院"
    elif map_id == 1401:
        return "普通民宅"
    elif map_id == 1402:
        return "高级华宅"
    elif map_id == 1403:
        return "顶级豪宅"
    elif map_id == 1404:
        return "普通民宅"
    elif map_id == 1405:
        return "高级华宅"
    elif map_id == 1406:
        return "顶级豪宅"
    elif map_id == 1407:
        return "普通民宅"
    elif map_id == 1408:
        return "高级华宅"
    elif map_id == 1409:
        return "顶级豪宅"
    elif map_id == 1410:
        return "普通民宅"
    elif map_id == 1411:
        return "高级华宅"
    elif map_id == 1412:
        return "顶级豪宅"
    elif map_id == 1413:
        return "海蓝系民宅"
    elif map_id == 1414:
        return "海蓝系华宅"
    elif map_id == 1415:
        return "海蓝系豪宅"
    elif map_id == 1420:
        return "普通庭院"
    elif map_id == 1421:
        return "中级庭院"
    elif map_id == 1422:
        return "高级庭院"
    elif map_id == 1810:
        return "一级帮派金库_门左"
    elif map_id == 1811:
        return "一级帮派金库_门右"
    elif map_id == 1812:
        return "二、三级帮派金库_门左"
    elif map_id == 1813:
        return "二、三级帮派金库_门右"
    elif map_id == 1814:
        return "四、五级帮派金库_门左"
    elif map_id == 1815:
        return "四、五级帮派金库_门右"
    elif map_id == 1820:
        return "一级帮派书院_门左"
    elif map_id == 1821:
        return "一级帮派书院_门右"
    elif map_id == 1822:
        return "二、三级帮派书院_门左"
    elif map_id == 1823:
        return "二、三级帮派书院_门右"
    elif map_id == 1824:
        return "四、五级帮派书院_门左"
    elif map_id == 1825:
        return "四、五级帮派书院_门右"
    elif map_id == 1830:
        return "一级帮派兽室_门左"
    elif map_id == 1831:
        return "一级帮派兽室_门右"
    elif map_id == 1832:
        return "二、三级帮派兽室_门左"
    elif map_id == 1833:
        return "二、三级帮派兽室_门右"
    elif map_id == 1834:
        return "四、五级帮派兽室_门左"
    elif map_id == 1835:
        return "四、五级帮派兽室_门右"
    elif map_id == 1840:
        return "一级帮派厢房_门左"
    elif map_id == 1841:
        return "一级帮派厢房_门右"
    elif map_id == 1842:
        return "二、三级帮派厢房_门左"
    elif map_id == 1843:
        return "二、三级帮派厢房_门右"
    elif map_id == 1844:
        return "四、五级帮派厢房_门左"
    elif map_id == 1845:
        return "四、五级帮派厢房_门右"
    elif map_id == 1850:
        return "一级帮派药房_门左"
    elif map_id == 1851:
        return "一级帮派药房_门右"
    elif map_id == 1852:
        return "二、三级帮派药房_门左"
    elif map_id == 1853:
        return "二、三级帮派药房_门右"
    elif map_id == 1854:
        return "四、五级帮派药房_门左"
    elif map_id == 1855:
        return "四、五级帮派药房_门右"
    elif map_id == 1860:
        return "一级帮派青龙堂_门左"
    elif map_id == 1861:
        return "一级帮派青龙堂_门右"
    elif map_id == 1862:
        return "二、三级帮派青龙堂_门左"
    elif map_id == 1863:
        return "二、三级帮派青龙堂_门右"
    elif map_id == 1864:
        return "四、五级帮派青龙堂_门左"
    elif map_id == 1865:
        return "四、五级帮派青龙堂_门右"
    elif map_id == 1870:
        return "一级帮派聚义堂_门左"
    elif map_id == 1871:
        return "一级帮派聚义堂_门右"
    elif map_id == 1872:
        return "二、三级帮派聚义堂_门左"
    elif map_id == 1873:
        return "二、三级帮派聚义堂_门右"
    elif map_id == 1874:
        return "四、五级帮派聚义堂_门左"
    elif map_id == 1875:
        return "四、五级帮派聚义堂_门右"
    elif map_id == 6001:
        return "废弃的御花园"
    elif map_id == 6002:
        return "乌鸡国皇宫"
    elif map_id == 1125:
        return "轮回司"
    elif map_id == 1877:
        return "69级比武场"
    elif map_id == 1878:
        return "89级比武场"
    elif map_id == 1879:
        return "109级比武场"
    elif map_id == 1880:
        return "129级比武场"
    elif map_id == 1881:
        return "155级比武场"
    elif map_id == 1882:
        return "175级比武场"
    else:
        return "未知地图"
