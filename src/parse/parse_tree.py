from abc import ABC, abstractmethod
from typing import Optional

class ParseTreeNode(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_children(self) -> list['ParseTreeNode']:
        pass

class ProgramNode(ParseTreeNode):
    def __init__(self, statement_seq: 'StatementSequenceNode'):
        super().__init__()
        self.statement_seq = statement_seq

    def get_children(self) -> list['ParseTreeNode']:
        return [self.statement_seq]
    
class StatementSequenceNode(ParseTreeNode):
    def __init__(self, statement: 'StatementNode', statement_seq: Optional['StatementSequenceNode']):
        super().__init__()
        self.statement = statement
        self.statement_seq = statement_seq

    def get_children(self) -> list['ParseTreeNode']:
        children = []
        if self.statement_seq:
            children.append(self.statement_seq)
        children.append(self.statement)
        return children
    
class StatementNode(ParseTreeNode):
    def __init__(self):
        super().__init__()

class IfStatementNode(StatementNode):
    def __init__(self, condition: 'ExpressionNode', then_part: 'StatementSequenceNode', else_part: Optional['StatementSequenceNode']):
        super().__init__()
        self.condition = condition
        self.then_part = then_part
        self.else_part = else_part

    def get_children(self) -> list[ParseTreeNode]:
        children = [self.condition, self.then_part];
        if self.else_part:
            children.append(self.else_part)

        return children
    
class ExpressionNode(ParseTreeNode):
    def __init__(self, left: 'SimpleExpression', operand: Optional['ComparisonOpNode'], right: Optional['SimpleExpression']):
        super().__init__()
        if operand and not right:
            raise ValueError("operand requires a right operand")