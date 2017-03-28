# -*- coding: utf-8 -*-
import os
import json

DATA_NAME = 'data_nodes'
data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), DATA_NAME)


def parse_node(text):
    type_name, node_name = _normal_input(text)
    if not _is_node(node_name):
        return
    types = _is_node(node_name)
    ntype_list = ['sop', 'dop', 'shop', 'obj', 'pop', 'chop', 'cop2', 'vop', 'vex', 'out']
    if type_name:
        if type_name not in ntype_list:
            return
        return _read_node(type_name, node_name)
    else:
        type_name = types[0]
        return _read_node(type_name, node_name)


def _read_node(type_name, node_name):
    data_file = data_dir + '/' + type_name + '.json'
    f = open(data_file, 'r')
    content = json.loads(f.read())
    f.close()
    data = content[node_name]
    return data


def _normal_input(text):
    if text.count(':') == 1:
        type_name, node_name = text.split(':')
        return type_name, node_name
    return None, text


def _is_node(text):
    data_nodes = data_dir + '/' + 'nodes.json'
    f = open(data_nodes, 'r')
    content = json.loads(f.read())
    f.close()
    if text in content:
        return content[text]
    else:
        return None


def _out_json(nodes_path):
    ntype_list = ['sop', 'dop', 'shop', 'obj', 'pop', 'chop', 'cop2', 'vop', 'vex', 'out']
    nodes = {}
    for index, type in enumerate(ntype_list):
        value = type
        ntype_file = os.path.join(nodes_path, type)
        node = {}
        for node_name in os.listdir(ntype_file):
            node_name = os.path.splitext(node_name)[0]
            key = node_name
            if key in nodes:
                nodes[key].append(value)
            else:
                nodes[key] = [value]
            node_file = nodes_path + type + '/' + node_name + '.txt'
            summary = __node_summary(node_file)
            like = 'http://www.sidefx.com/docs/houdini/nodes/%s/%s' % (type, node_name)
            print summary
            node[key] = (summary, 'icon', like)

        # out node_type.json
        type_data = json.dumps(node, sort_keys=True, indent=4, separators=(',', ': '))
        json_file = nodes_path + type + '.json'
        f = open(json_file, 'w')
        f.write(type_data)
        f.close()

    # out nodes.json
    nodes_data = json.dumps(nodes, sort_keys=True, indent=4, separators=(',', ': '))
    json_file = os.path.join(nodes_path, 'nodes.json')
    f = open(json_file, 'w')
    f.write(nodes_data)
    f.close()


def __node_summary(node_file):
    text = open(node_file)
    hand = ''
    run = 1
    # if '"""' not in text.readlines():
    #     run = None
    while run:
        run += 1
        text_line = text.readline()
        if text_line[:3] == '"""':
            run = None
            hand = text_line[3:-4]
        if run == 501:
            run = None
    if hand:
        return hand
    else:
        return


if __name__ == '__main__':
    # a = os.listdir('E:/Project/scripts/wechat-manager/function/nodes/text_nodes/')
    # path = 'E:/Project/scripts/wechat-manager/function/nodes/text_nodes/'
    # _out_json(path)
    # print is_node('add')
    # print _normal_input('addsdf')
    print parse_node('哈：哈')