# -*- coding: utf-8 -*-
import os
import json
import sys

import config

class Read(object):
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.path = os.path.split(os.path.realpath(__file__))[0]
        self.dir = self.path + '/text_nodes/%s/' %(type,)
        self.node = self.dir + name + '.txt'
        if not os.path.isfile(self.node):
            raise Exception("Not find this file: %s" %(self.node))

    def hand(self):
        text = open(self.node)
        hand = ''
        run = 1
        while run:
            text_line = text.readline()
            if text_line[:3] == '"""':
                run = None
                hand = text_line[3:-4]
        if hand:
            return hand
        else:
            return

    # def bewirte(self):
    #     text = open(self.node)
    #     beweirte = ''
    #     run = 1
    #     start = (0, 0)
    #     text_line = ''
    #     while run:
    #         text_line = text.readline()
    #         if start == (1, 1) and text_line:
    #             beweirte += text_line
    #         if text_line[:3] == '"""':
    #             start = (1, 0)
    #             continue
    #         if start == (1, 0) and '\n' == text_line:
    #             start = (1, 1)
    #             continue
    #         if start == (1, 1) and '\n' == text_line:
    #             run = None
    #     return beweirte
    #
    # def node_list(self):
    #     file_list = []
    #     all_file = os.listdir(self.dir)
    #     for f in all_file:
    #         file_list.append(os.path.splitext(f)[0])
    #     return file_list


def find_node(rec):
    ntype = ''
    name = ''
    rec = rec.lower()
    file_dict = config.files_dict
    node_list = ['sop', 'dop', 'shop', 'obj', 'pop', 'chop', 'vop', 'vex', 'out']
    if ':' in rec:
        rec_list = rec.split(':')
        if len(rec_list) != 2:
            print rec_list, 'have more ":"'
            return
        else:
            ntype, name = rec_list
            if ntype not in node_list:
                print ntype, 'Not in node_list.'
                return
            else:
                file_list = file_dict[ntype]
                if name + '.txt' not in file_list:
                    print name, 'Not in node_names.'
                    return
    else:
        i = 0
        while i < len(node_list):
            file_list = file_dict[node_list[i]]
            if rec + '.txt' in file_list:
                ntype = node_list[i]
                name = rec
                break
            i += 1
    return (ntype, name)


def type_nodes(rec):
    ntype_list = ['sop', 'dop', 'shop', 'obj', 'pop', 'chop', 'vop', 'vex', 'out']
    rec = rec.lower()
    if rec in ntype_list:
        type = rec
        file_dict = config.files_dict
        file_list = file_dict[type]
        nodes = '%s: ' % (rec.upper())
        for f in file_list:
            node = os.path.splitext(f)[0]
            node_str = + node + ','
            nodes += node_str
        return nodes
    else:
        return


def _create_ndict(nodes_path):
    ntype_list = config.node_data['node_types']
    files_dict = {}
    for ntype in ntype_list:
        file_value = []
        ntype_path = nodes_path + '/' + ntype
        file_list = os.listdir(ntype_path)
        for file in file_list:
            file_value.append(file)
        files_dict[ntype] = file_value
    print files_dict
    # print files_dict.keys()


def out_json(nodes_path):
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
            summary = node_summary(node_file)
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


def node_summary(node_file):
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
    # rec = find_node('ADD')
    # print rec
    # print Read(rec[0], rec[1]).bewirte()
    a = os.listdir('E:/Project/scripts/wechat-manager/function/nodes/text_nodes/')
    path = 'E:/Project/scripts/wechat-manager/function/nodes/text_nodes/'
    # print a,'\r\n', len(a)
    # print _create_ndict('E:/Project/scripts/wechat-manager/function/nodes/text_nodes')
    # print len(type_nodes('obj'))
    out_json(path)
