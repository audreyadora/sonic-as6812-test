# Copyright 2013-present Barefoot Networks, Inc. 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import operator
import ast
import p4_headers
import p4_imperatives
from p4_core import p4_compiler_msg

ops = [
    (ast.Add, operator.add, "+"),
    (ast.Sub, operator.sub, "-"),
    (ast.Mult, operator.mul, "*"),
    (ast.Div, operator.div, "/"),
    (ast.Mod, operator.mod, "%"),
    (ast.Pow, operator.pow, "**"),
    (ast.LShift, operator.lshift, "<<"),
    (ast.RShift, operator.rshift, ">>"),
    (ast.BitOr, operator.or_, "|"),
    (ast.BitXor, operator.xor, "^"),
    (ast.BitAnd, operator.and_, "&"),
    (ast.Invert, operator.invert, "~"),
    (ast.Not, operator.not_, "not"),
    (ast.Eq, operator.eq, "=="),
    (ast.NotEq, operator.ne, "!="),
    (ast.Lt, operator.lt, "<"),
    (ast.LtE, operator.le, "<="),
    (ast.Gt, operator.gt, ">"),
    (ast.GtE, operator.ge, ">="),
    (ast.Or, lambda x,y: x or y, "or"),
    (ast.And, lambda x,y: x and y, "and"),
    (None, None, "valid")
]
str_ops = dict([(str_op,(ast_op,op_op)) for ast_op, op_op, str_op in ops])
ast_ops = dict([(ast_op,(op_op,str_op)) for ast_op, op_op, str_op in ops])
op_ops = dict([(op_op,(ast_op,str_op)) for ast_op, op_op, str_op in ops])

bool_ops = {"<","<=",">",">=","==","!=","or","and","valid","not"}
unary_ops = {"~","not","valid"}

class p4_expression(object):
    """
    TODO: docstring
    """
    def __init__ (self, left=None, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right

    def __str__ (self):
        if type(self.op) is str and self.left is not None:
            return "(({}) {} ({}))".format(self.left, self.op, self.right)
        elif type(self.op) is str:
            return "({} ({}))".format(self.op, self.right)
        else:  # ternary operator
            assert(type(self.op) is p4_expression)
            return "(({}) ? ({}) : ({}))".format(self.op, self.left, self.right)

    def resolve_one_name(self, hlir, local_vars, name):
        if name in local_vars:
            return local_vars[name]
        try:
            return p4_headers.p4_header_instance.get_from_hlir(hlir, name)
        except:
            pass

        try:
            return p4_headers.p4_field.get_from_hlir(hlir, name)
        except:
            pass

        try:
            return p4_imperatives.p4_register_ref.get_from_hlir(hlir, name)
        except:
            raise p4_compiler_msg ("Undeclared identifier '%s'" % name)

    def resolve_names(self, hlir, local_vars=None):
        """
        Change strings in the expression into references to their relevant
        objects.

        The optional local_vars dictionary maps names not in the HLIR to their
        appropriate resolved objects
        """
        if local_vars == None:
            local_vars = {}

        if self.op=="valid":
            self.right = self.resolve_one_name(hlir, local_vars, self.right)
        else:
            if isinstance(self.op, p4_expression):
                # hack for ternary ? :
                self.op.resolve_names(hlir, local_vars)

            if type(self.left) is p4_expression:
                self.left.resolve_names(hlir, local_vars)
            elif type(self.left) is str:
                self.left = self.resolve_one_name(hlir, local_vars, self.left)

            if type(self.right) is p4_expression:
                self.right.resolve_names(hlir, local_vars)
            elif type(self.right) is str:
                self.right = self.resolve_one_name(hlir, local_vars, self.right)
