import json
import codecs


def findID(name, subway):
    for station in subway:
        if station["stationName"] == name:
            return station["stationID"]
    raise Exception("没有找到匹配的站名")


def findroute(begin, end):
    # 读入地铁内容文件
    subway_str = codecs.open('MetroData_SH.json', encoding="utf-8").read()
    subway = json.loads(subway_str)
    stations = subway['station']

    # 判断是不是字符串
    if type(begin) == str:
        print("你输入了站名\n")
        begin = findID(begin, stations)
        end = findID(end, stations)

    # 初始化队列
    movefrom = [-1] * len(stations)  # 存储上一个节点是哪里
    movefrom[begin] = begin
    queue = [begin]  # 查找的队列,广度搜索
    route = [end]  # 最后的结果路径

    while movefrom[end] == -1:  # 还没有找到路径时(终点前一个站点还没有找到)
        process_node = queue.pop(0)  # 队列中取出当前处理的站点
        tempset = set(stations[process_node]["nextStationID"])  # 去重,数据中存在重复
        for nextnode in tempset:  # 当前站点的相邻节点
            if movefrom[nextnode] == -1:  # 如果是-1, 说明还没有遍历到
                queue.append(nextnode)  # 入队
                movefrom[nextnode] = process_node  # 记录是从哪个节点找到的

    # 填充结果
    while True:
        if movefrom[route[-1]] == begin:
            route.append(begin)
            break
        route.append(movefrom[route[-1]])

    # print对应的站名
    for n in route:
        print(stations[n]["stationName"])

    # 返回倒序的路径点,按ID
    return route


if __name__ == '__main__':
    # findroute(126, 128) # 剑川路到马当路
    # findroute(284, 44)  # 滴水湖到花桥 应该是最长路径了吧
    findroute("剑川路", "马当路")
