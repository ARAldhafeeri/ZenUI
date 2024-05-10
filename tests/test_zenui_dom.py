import sys
import unittest
from unittest.mock import patch, MagicMock
from zenui.tags import Attribute, Node
from tests.mocks.browser_mocks import MockDocument, MockWindow

sys.modules["pyscript"] = MagicMock()

class TestComponent(unittest.TestCase):

    @patch('pyscript.document')
    @patch('pyscript.window')
    def setUp(self, document, window):  # Run before each test
        from tests.mocks.counter_mocks import Counter, BTN_STYLES
        from zenui.zenui_dom import zenui_dom
        self.dependencies = {}  # Mock dependencies if needed
        self.btnstyles = BTN_STYLES
        self.counter = Counter(self.dependencies)
        self.document = MockDocument()
        self.window = MockWindow()
        self.zenui_dom = zenui_dom
        
    def test_mount(self):
        self.zenui_dom.mount(self.counter)
        self.assertIn(self.counter.componentId, self.zenui_dom.zen_dom_table.keys())
        prev = self.zenui_dom.zen_dom_table[self.counter.componentId]
        self.assertTrue(prev)
        # mount is called on root div
        exists = self.document.getNodeById("root")
        self.assertTrue(exists)
	
    def test_search(self):
        prevTree = self.counter.node()
        # simulate search table mount manually for testing
        self.zenui_dom.zen_dom_table[self.counter.componentId] = prevTree
        self.counter.set_state("test")
        newTree = self.counter.node()
        diff = self.zenui_dom.search(prevTree, newTree)
        print(diff)
        # hader location on tree, effected by change
        changedNodeId = prevTree.nodeId
        self.assertEqual(changedNodeId, diff[0][0])
