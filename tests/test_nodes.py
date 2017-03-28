# -*- coding: utf-8 -*-
import unittest

from function.read_node import read


class NodesTestCase(unittest.TestCase):

    def test_parse_node(self):
        user_input = 'sop:add'
        sidefx_home = 'http://www.sidefx.com'
        content = read.parse_node(user_input)
        self.assert_(content, '"%s" not return None' % user_input)
        self.assertEqual(type(content), type(['test']), 'Return type not list')
        self.assertEqual(content[2][:21], sidefx_home, 'Return url not %s' % sidefx_home)
        content = read.parse_node('xxxx')
        self.failIf(content, '%s not return None' % user_input)

if __name__ == '__main__':
    unittest.main()
