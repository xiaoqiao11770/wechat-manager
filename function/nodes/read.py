# -*- coding: utf-8 -*-
import os


class Read(object):
    def __init__(self, type):
        self.type = type
        self.path = os.getcwd()
        self.dir = self.path + '/text_nodes/%s/' %(type,)
        if not os.path.isdir(self.dir):
            raise Exception("Not find this dir: %s" %(self.dir))

    def hand(self, name):
        node_file = self.dir + name + '.txt'
        if not os.path.isfile(node_file):
            raise Exception("Not find this file: %s" %(node_file))
        text = open(node_file)
        hand = ''
        start = True
        while start:
            test_line = text.readline()
            if test_line[:3] == '"""':
                start = False
                hand = test_line[3:-4]
        if hand:
            return hand

    def node_list(self):
        file_list = []
        all_file = os.listdir(self.dir)
        for f in all_file:
            file_list.append(os.path.splitext(f)[0])
        return file_list

if __name__ == '__main__':
    print Read('pop').node_list()