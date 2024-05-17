import sys
import unittest
from unittest.mock import patch, MagicMock
from tests.mocks.browser_mocks import MockDocument, MockWindow
from zenaura.client.tags import Node
from zenaura.client.page import Page
from zenaura.client.component import Component, Reuseable
from zenaura.client.compiler import compiler

sys.modules["pyscript"] = MagicMock()

class TestDom(unittest.TestCase):

    @patch('pyscript.document')
    @patch('pyscript.window')
    def setUp(self, document, window):  # Run before each test
        from tests.mocks.counter_mocks import Counter, BTN_STYLES, CounterState
        from zenaura.client.dom import zenaura_dom
        self.dependencies = {}  # Mock dependencies if needed
        self.btnstyles = BTN_STYLES
        self.counter = Counter(self.dependencies)
        self.counterNewInstance = Counter
        self.document = MockDocument()
        self.window = MockWindow()
        self.zenaura_dom = zenaura_dom
        self.counterState = CounterState
        # advaced dom node mock 
        self.dom_node = MagicMock()
        self.dom_node.getNodeById = MagicMock(return_value=self.dom_node)
        self.dom_node.innerHTML = ""
        
    def test_mount(self):
        self.zenaura_dom.mount(Page([self.counter]))
        self.assertIn(self.counter.componentId, self.zenaura_dom.zen_dom_table.keys())
        prev = self.zenaura_dom.zen_dom_table[self.counter.componentId]
        self.assertTrue(prev)
        # mount is called on root div
        exists = self.document.getNodeById("root")
        self.assertTrue(exists)
	

    async def test_render(self):
        self.zenaura_dom.mount(Page([self.counter]))
        self.counter.set_state(self.counterState(count=1))
        await self.zenaura_dom.render(self.counter)
        re_rendered = self.zenaura_dom.zen_dom_table[self.counter.componentId]
        # print end of line 
        # new data structure Data for data binding
        self.assertEqual(re_rendered.children[0].children[0].children[0].children[0].content, f'Counter: {self.counterState(count=1)}')

        
    def test_mount_existing_component(self):
        
        self.zenaura_dom.mount(Page([self.counter]))
        exists = self.zenaura_dom.zen_dom_table[self.counter.componentId]

        
        self.assertTrue(exists)

    def test_render_unmounted_component(self):
        
        class K(Component):
            def node(self):
                return Node(name="div", children=[Node(name="span", children=["test"])])
        
        unmounted_counter = K()

        
        self.zenaura_dom.render(unmounted_counter)
        key = self.zenaura_dom.zen_dom_table[self.counter.componentId]
        self.assertTrue(key)


        
    def test_componentDidCatchError_with_custom_error_component(self):
        # Arrange
        class CustomErrorComponent(Component):
            def __init__(self, error_message):
                super().__init__()
                self.error_message = error_message
            def node(self):
                return Node("div", children=[Node("p", children=[str(self.error_message)])])

        @Reuseable
        class TestComponent(Component):
            def componentDidCatchError(self, error):
                return CustomErrorComponent(error_message=error)

        test_component = TestComponent()

        self.zenaura_dom.componentDidCatchError(test_component, "Custom error message")

        self.assertEqual(self.zenaura_dom.zen_dom_table[test_component.componentId].children[0].children[0], "Custom error message")

    def test_componentDidCatchError_with_default_error_component(self):

        @Reuseable
        class TestComponent(Component):
            pass
        
        test = TestComponent()
        self.zenaura_dom.componentDidCatchError(test, "Default error message")

        self.assertEqual(self.zenaura_dom.zen_dom_table[test.componentId].children[0].children[0], "Default error message")

    # Mount - testing component lifecycle methods 

    def test_component_did_mount_without_attached_method(self):
        class TestComponent(Component):
            def node(self):
                return Node("p")

        component = TestComponent()

        self.zenaura_dom.mount(Page([component]))

        self.assertEqual(self.zenaura_dom.zen_dom_table[component.componentId].name, "p")

    
    def test_component_did_mount_with_attached_method(self):

        @Reuseable
        class TestComponent(Component):
            x = 0
    
            def attached(self, *args, **kwargs):
                self.x = 10

            def node(self):
                return Node("p")
            
        component = TestComponent()

        self.assertEqual(component.x, 0)
        self.zenaura_dom.mount(Page([component]))
      
        self.assertEqual(component.x, 10)


    def test_component_did_update_without_componentDidUpdate_method(self):

        @Reuseable
        class TestComponent(Component):
            def node(self):
                return Node("p")
            
        component = TestComponent()
        print("soko boko",type(self.zenaura_dom.zen_dom_table[component.componentId]))
        self.zenaura_dom.mount(Page([component]))
        self.assertEqual(self.zenaura_dom.zen_dom_table[component.componentId].name, "p")
        

    async def test_component_did_update_with_componentDidUpdate_method(self):
        @Reuseable
        class TestComponent(Component):
            
            x  = 0
            
            def node(self):
                return Node("p")
            
            def componentDidUpdate(self, *args, **kwargs):
                self.x = 10

        component = TestComponent()
        self.assertEqual(component.x, 0)
        await self.zenaura_dom.render(component)
        self.assertEqual(component.x, 10)
