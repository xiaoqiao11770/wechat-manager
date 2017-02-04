# -*- coding: utf-8 -*-
import os
import sys


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

    def bewirte(self):
        text = open(self.node)
        beweirte = ''
        run = 1
        start = (0, 0)
        text_line = ''
        while run:
            text_line = text.readline()
            if start == (1, 1) and text_line:
                beweirte += text_line
            if text_line[:3] == '"""':
                start = (1, 0)
                continue
            if start == (1, 0) and '\n' == text_line:
                start = (1, 1)
                continue
            if start == (1, 1) and '\n' == text_line:
                run = None
        return beweirte

    def node_list(self):
        file_list = []
        all_file = os.listdir(self.dir)
        for f in all_file:
            file_list.append(os.path.splitext(f)[0])
        return file_list

if __name__ == '__main__':
    print Read('sop', 'add').node_list()
