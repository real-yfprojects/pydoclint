import ast
import pytest

from pydoclint.utils.walk import walk
from pydoclint.utils.astTypes import FunctionOrClassDef


src1 = """
def func1():
    return 101

def func2():
    print("No return here")

async def func3():
    def func3_child1():
        print(301)
        def func3_child1_grandchild1():
            print(3011)
    return "async 301"

def func4():
    def func4_child1():
        return "nested 401"
        
    def func4_child2():
        print('402')
        def func4_child2_grandchild1():
            return 4021

def func5():
    if 1 > 2:
        return 501
    
    if 2 > 6:
        return 506
        
class MyClass:
    def __init__(self):
        pass
        
    def method1(self):
        print('a1')
        def method1_child1(self):
            pass
    
    @classmethod     
    def classmethod1(cls):
        pass
        def classmethod1_child1():
            return 'hello'
"""


@pytest.mark.parametrize(
    'src, expected',
    [
        (
            src1,
            [
                ('func1', 'ast.Module'),
                ('func2', 'ast.Module'),
                ('func3', 'ast.Module'),
                ('func4', 'ast.Module'),
                ('func5', 'ast.Module'),
                ('MyClass', 'ast.Module'),
                ('func3_child1', 'func3'),
                ('func4_child1', 'func4'),
                ('func4_child2', 'func4'),
                ('__init__', 'MyClass'),
                ('method1', 'MyClass'),
                ('classmethod1', 'MyClass'),
                ('func3_child1_grandchild1', 'func3_child1'),
                ('func4_child2_grandchild1', 'func4_child2'),
                ('method1_child1', 'method1'),
                ('classmethod1_child1', 'classmethod1'),
            ],
        ),
    ],
)
def testWalk(src: str, expected: list[tuple[str, str]]) -> None:
    result: list[tuple[str, str]] = []
    tree = ast.parse(src)
    for node, parent in walk(tree):
        if 'name' in node.__dict__:
            parent_repr: str
            if isinstance(parent, ast.Module):
                parent_repr = 'ast.Module'
            elif isinstance(parent, FunctionOrClassDef):
                parent_repr = parent.name
            else:
                parent_repr = str(type(parent))

            result.append((node.name, parent_repr))

    assert result == expected
