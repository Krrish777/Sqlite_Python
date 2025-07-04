from compiler.code_generator.base_codegen import BaseCodeGenerator
from compiler.code_generator.opcode import Opcode
from utils.logger import get_logger

logger = get_logger(__name__)

class InsertCodeGenerator(BaseCodeGenerator):
    def generate(self):
        
        table = self.ast["table"]
        values = self.ast["values"]
        
        code = []
        code.append((Opcode.OPEN_TABLE, table))
        
        for value in values:
            code.append((Opcode.LOAD_CONST, value))
            
        code.append((Opcode.INSERT_ROW, table))
        
        return code