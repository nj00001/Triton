#include <iostream>
#include <sstream>
#include <stdexcept>

#include "NotIRBuilder.h"
#include "Registers.h"
#include "SMT2Lib.h"
#include "SymbolicElement.h"


NotIRBuilder::NotIRBuilder(uint64_t address, const std::string &disassembly):
  BaseIRBuilder(address, disassembly) {
}


void NotIRBuilder::reg(AnalysisProcessor &ap, Inst &inst) const {
  SymbolicElement   *se;
  std::stringstream expr, op1;
  uint64_t          reg       = std::get<1>(this->operands[0]);
  uint32_t          regSize   = std::get<2>(this->operands[0]);
  uint64_t          symReg    = ap.getRegSymbolicID(reg);

  /* Create the SMT semantic */
  /* OP_1 */
  if (symReg != UNSET)
    op1 << "#" << std::dec << symReg;
  else
    op1 << smt2lib::bv(ap.getRegisterValue(reg), regSize * REG_SIZE);

  /* Finale expr */
  expr << smt2lib::bvnot(op1.str());

  /* Create the symbolic element */
  se = ap.createRegSE(expr, reg);

  /* Apply the taint */
  ap.aluSpreadTaintRegReg(se, reg, reg);

  /* Add the symbolic element to the current inst */
  inst.addElement(se);
}


void NotIRBuilder::mem(AnalysisProcessor &ap, Inst &inst) const {
  SymbolicElement   *se;
  std::stringstream expr, op1;
  uint64_t          mem       = std::get<1>(this->operands[0]);
  uint32_t          memSize   = std::get<2>(this->operands[0]);
  uint64_t          symMem    = ap.getMemSymbolicID(mem);

  /* Create the SMT semantic */
  /* OP_1 */
  if (symMem != UNSET)
    op1 << "#" << std::dec << symMem;
  else
    op1 << smt2lib::bv(ap.getMemValue(mem, memSize), memSize * REG_SIZE);

  /* Finale expr */
  expr << smt2lib::bvnot(op1.str());

  /* Create the symbolic element */
  se = ap.createMemSE(expr, mem);

  /* Apply the taint */
  ap.aluSpreadTaintMemMem(se, mem, mem);

  /* Add the symbolic element to the current inst */
  inst.addElement(se);
}


void NotIRBuilder::imm(AnalysisProcessor &ap, Inst &inst) const {
  /* There is no <not imm> available in x86 */
  OneOperandTemplate::stop(this->disas);
}


void NotIRBuilder::none(AnalysisProcessor &ap, Inst &inst) const {
  /* There is no <not none> available in x86 */
  OneOperandTemplate::stop(this->disas);
}


Inst *NotIRBuilder::process(AnalysisProcessor &ap) const {
  this->checkSetup();

  Inst *inst = new Inst(ap.getThreadID(), this->address, this->disas);

  try {
    this->templateMethod(ap, *inst, this->operands, "NOT");
    ap.incNumberOfExpressions(inst->numberOfElements()); /* Used for statistics */
  }
  catch (std::exception &e) {
    delete inst;
    throw;
  }

  return inst;
}
