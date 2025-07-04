from compiler.code_generator.base_codegen import BaseCodeGenerator
from compiler.code_generator.opcode import Opcode
from utils.logger import get_logger

logger = get_logger(__name__)

class DeleteCodeGenerator(BaseCodeGenerator):
    def generate(self):
        logger.info("Generating DELETE code")
        table = self.ast["table"]
        where = self.ast.get("where", None)
        
        loop_label = self.new_label()
        end_label = self.new_label()
        skip_label = self.new_label()
        
        code = [
            (Opcode.OPEN_TABLE, table),
            (Opcode.SCAN_START,),
            (Opcode.LABEL, loop_label),
            (Opcode.SCAN_NEXT,),
            (Opcode.JUMP_IF_FALSE, end_label)
        ]

        if where:
            # If where is a list (from parse_where_clause), use the first condition
            cond = where[0] if isinstance(where, list) else where
            col = cond["column"]
            code += [
                (Opcode.LOAD_COLUMN, col),
                (Opcode.LOAD_CONST, cond["value"]),
                (self._get_comparison_opcode(cond["operator"]),),
                (Opcode.JUMP_IF_FALSE, skip_label)
            ]

        code.append((Opcode.DELETE_ROW,))

        if where:
            code.append((Opcode.LABEL, skip_label))

        code += [
            (Opcode.JUMP, loop_label),
            (Opcode.LABEL, end_label),
            (Opcode.SCAN_END,)
        ]
        logger.debug(f"Generated DELETE code: {code}")
        return code

    def _get_comparison_opcode(self, operator):
        return {
            "=": Opcode.COMPARE_EQ,
            "==": Opcode.COMPARE_EQ,
            "!=": Opcode.COMPARE_NEQ,
            "<": Opcode.COMPARE_LT,
            "<=": Opcode.COMPARE_LTE,
            ">": Opcode.COMPARE_GT,
            ">=": Opcode.COMPARE_GTE,
        }.get(operator) or ValueError(f"Unsupported operator: {operator}")