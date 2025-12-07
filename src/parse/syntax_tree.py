from abc import ABC, abstractmethod
from typing import Optional, Sequence

class SyntaxTreeNode(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_children(self) -> Sequence['SyntaxTreeNode']:
        pass


class StatementSequence(SyntaxTreeNode):
    def __init__(self, statements: list['StatementNode']):
        super().__init__()
        self.statements = statements

    def get_children(self) -> Sequence['SyntaxTreeNode']:
        return self.statements
    

class StatementNode(SyntaxTreeNode):
    pass


class IfStatementNode(StatementNode):
    def __init__(self, test: 'ExpressionNode', then_part: 'StatementSequence', else_part: Optional['StatementSequence']):
        super().__init__()
        self.test = test
        self.then_part = then_part
        self.else_part = else_part

    def get_children(self) -> list[SyntaxTreeNode]:
        children = [self.test, self.then_part, self.else_part]
        return children


class RepeatStatementNode(StatementNode):
    def __init__(self, body: 'StatementSequence', test: 'ExpressionNode'):
        super().__init__()
        self.body = body
        self.test = test

    def get_children(self) -> list[SyntaxTreeNode]:
        return [self.body, self.test]
    

class AssignmentStatementNode(StatementNode):
    def __init__(self, identifier: str, expression: 'ExpressionNode'):
        super().__init__()
        self.identifier = identifier
        self.expression = expression

    def get_children(self) -> list[SyntaxTreeNode]:
        return [self.expression]
    

class WriteStatementNode(StatementNode):
    def __init__(self, expression: 'ExpressionNode'):
        super().__init__()
        self.expression = expression

    def get_children(self) -> list[SyntaxTreeNode]:
        return [self.expression]
    

class ReadStatementNode(StatementNode):
    def __init__(self, identifier: str):
        super().__init__()
        self.identifier = identifier

    def get_children(self) -> list[SyntaxTreeNode]:
        return []
    

class ExpressionNode(SyntaxTreeNode):
    pass


class OperatorNode(ExpressionNode):
    def __init__(self, operator: str, left: 'ExpressionNode', right: 'ExpressionNode'):
        super().__init__()
        self.operator = operator
        self.left = left
        self.right = right

    def get_children(self) -> list[SyntaxTreeNode]:
        return [self.left, self.right]
    

class IdentifierNode(ExpressionNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def get_children(self) -> list[SyntaxTreeNode]:
        return []
    

class ConstantNode(ExpressionNode):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def get_children(self) -> list[SyntaxTreeNode]:
        return []