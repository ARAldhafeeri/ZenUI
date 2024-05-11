import sys
import unittest
from unittest.mock import patch, MagicMock
from tests.mocks.browser_mocks import MockDocument, MockWindow
from zenaura.client.tags import Node

sys.modules["pyscript"] = MagicMock()

class TestComponent(unittest.TestCase):

    @patch('pyscript.document')
    @patch('pyscript.window')
    def setUp(self, document, window):  # Run before each test
        from tests.mocks.counter_mocks import Counter, BTN_STYLES, CounterState
        from zenaura.client.dom import zenaura_dom
        self.dependencies = {}  # Mock dependencies if needed
        self.btnstyles = BTN_STYLES
        self.counter = Counter(self.dependencies)
        self.document = MockDocument()
        self.window = MockWindow()
        self.zenaura_dom = zenaura_dom
        self.counterState = CounterState
        
    def test_mount(self):
        self.zenaura_dom.mount(self.counter)
        self.assertIn(self.counter.componentId, self.zenaura_dom.zen_dom_table.keys())
        prev = self.zenaura_dom.zen_dom_table[self.counter.componentId]
        self.assertTrue(prev)
        # mount is called on root div
        exists = self.document.getNodeById("root")
        self.assertTrue(exists)
	
    def test_search(self):
        prevTree = self.counter.node()
        # simulate search table mount manually for testing
        self.zenaura_dom.zen_dom_table[self.counter.componentId] = prevTree
        self.counter.set_state("test")
        newTree = self.counter.node()
        diff = self.zenaura_dom.search(prevTree, newTree)
        # hader location on tree, effected by change
        changedNodeId = prevTree.nodeId
        self.assertEqual(changedNodeId, diff[0][0])


    def test_render(self):
        self.zenaura_dom.mount(self.counter)
        self.counter.set_state(self.counterState(count=1))
        self.zenaura_dom.render(self.counter)
        re_rendered = self.zenaura_dom.zen_dom_table[self.counter.componentId]
        self.assertEqual(re_rendered.children[0].children[0].children[0].children[0], f'Counter: {self.counterState(count=1)}')

    def test_update(self):
        prevTree = self.counter.node()
        newChildren = Node(name="div", children=["test"])
        updated = self.zenaura_dom.update(prevTree, prevTree.nodeId, newChildren)
        self.assertEqual(prevTree.children, newChildren.children)

        
