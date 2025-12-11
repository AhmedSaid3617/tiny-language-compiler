from abc import ABC, abstractmethod
from typing import Optional, Sequence

class SyntaxTreeNode(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_children(self) -> Sequence['SyntaxTreeNode']:
        pass

    @abstractmethod
    def to_json(self):
        pass


class StatementSequence(SyntaxTreeNode):
    def __init__(self, statements: list['StatementNode']):
        super().__init__()
        self.statements = statements

    def get_children(self) -> Sequence['SyntaxTreeNode']:
        return self.statements
    
    def to_json(self):
        return {
            "type": "Block",
            "statements": [stmt.to_json() for stmt in self.statements]
        }


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

    def to_json(self):
        result = {
            "type": "IfStatement",
            "test": self.test.to_json(),
            "then": self.then_part.to_json()
        }
        if self.else_part:
            result["else"] = self.else_part.to_json()
        return result


class RepeatStatementNode(StatementNode):
    def __init__(self, body: 'StatementSequence', test: 'ExpressionNode'):
        super().__init__()
        self.body = body
        self.test = test

    def get_children(self) -> list[SyntaxTreeNode]:
        return [self.body, self.test]
    
    def to_json(self):
        return {
            "type": "RepeatStatement",
            "body": self.body.to_json(),
            "test": self.test.to_json()
        }
    

class AssignmentStatementNode(StatementNode):
    def __init__(self, identifier: str, expression: 'ExpressionNode'):
        super().__init__()
        self.identifier = identifier
        self.expression = expression

    def get_children(self) -> list[SyntaxTreeNode]:
        return [self.expression]
    
    def to_json(self):
        return {
            "type": "Assignment",
            "identifier": self.identifier,
            "value": self.expression.to_json()
        }
    

class WriteStatementNode(StatementNode):
    def __init__(self, expression: 'ExpressionNode'):
        super().__init__()
        self.expression = expression

    def get_children(self) -> list[SyntaxTreeNode]:
        return [self.expression]
    
    def to_json(self):
        return {
            "type": "WriteStatement",
            "value": self.expression.to_json()
        }
    

class ReadStatementNode(StatementNode):
    def __init__(self, identifier: str):
        super().__init__()
        self.identifier = identifier

    def get_children(self) -> list[SyntaxTreeNode]:
        return []
    
    def to_json(self):
        return {
            "type": "ReadStatement",
            "identifier": self.identifier
        }
    

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
    
    def to_json(self):
        return {
            "type": "BinaryExpression",
            "operator": self.operator,
            "left": self.left.to_json(),
            "right": self.right.to_json()
        }
    

class IdentifierNode(ExpressionNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def get_children(self) -> list[SyntaxTreeNode]:
        return []
    
    def to_json(self):
        return {
            "type": "Identifier",
            "name": self.name
        }
    

class ConstantNode(ExpressionNode):
    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def get_children(self) -> list[SyntaxTreeNode]:
        return []
    
    def to_json(self):
        return {
            "type": "Literal",
            "value": self.value
        }