/* Used to test the C++ API */

#include <iostream>
#include <sstream>
#include <list>

#include <triton/aarch64Cpu.hpp>
#include <triton/aarch64Specifications.hpp>
#include <triton/api.hpp>
#include <triton/bitsVector.hpp>
#include <triton/config.hpp>
#include <triton/exceptions.hpp>
#include <triton/immediate.hpp>
#include <triton/instruction.hpp>
#include <triton/memoryAccess.hpp>
#include <triton/operandWrapper.hpp>
#include <triton/register.hpp>
#include <triton/x8664Cpu.hpp>
#include <triton/x86Cpu.hpp>
#include <triton/x86Specifications.hpp>

#ifdef TRITON_LLVM_INTERFACE
  #include <triton/tritonToLLVM.hpp>
  #include <triton/llvmToTriton.hpp>
#endif



int test_1(void) {
  triton::arch::x86::x8664Cpu   cpy1;
  triton::arch::x86::x8664Cpu*  cpy2;
  triton::arch::x86::x8664Cpu*  cpy3;
  triton::arch::x86::x8664Cpu   cpu;
  triton::API                   api;

  api.setArchitecture(triton::arch::ARCH_X86_64);
  api.setConcreteRegisterValue(api.registers.x86_rax, 12345);

  if (api.getConcreteRegisterValue(api.registers.x86_rax) != 12345)
    return 1;

  cpy1 = *reinterpret_cast<triton::arch::x86::x8664Cpu*>(api.getCpuInstance());
  if (cpy1.getConcreteRegisterValue(api.registers.x86_rax) != 12345) {
    std::cerr << "test_1: KO (cpy context != api context)" << std::endl;
    return 1;
  }

  cpy2 = new triton::arch::x86::x8664Cpu(*reinterpret_cast<triton::arch::x86::x8664Cpu*>(api.getCpuInstance()));
  if (cpy2->getConcreteRegisterValue(api.registers.x86_rax) != 12345) {
    std::cerr << "test_1: KO (cpy context != api context)" << std::endl;
    return 1;
  }

  cpy3 = new triton::arch::x86::x8664Cpu();
  *cpy3 = *cpy2;
  if (cpy3->getConcreteRegisterValue(api.registers.x86_rax) != 12345) {
    std::cerr << "test_1: KO (cpy context != api context)" << std::endl;
    return 1;
  }

  triton::arch::Instruction inst((const unsigned char*)"\x48\x89\xd8", 3); // mov rax, rbx
  cpu.disassembly(inst);
  if (inst.getType() != triton::arch::x86::ID_INS_MOV) {
    std::cerr << "test_1: KO (getType != ID_INS_MOV)" << std::endl;
    return 1;
  }

  std::cout << "test_1: OK" << std::endl;
  return 0;
}


int test_2(void) {
  triton::arch::x86::x86Cpu   cpy;
  triton::API                 api;

  api.setArchitecture(triton::arch::ARCH_X86);
  api.setConcreteRegisterValue(api.registers.x86_eax, 12345);

  if (api.getConcreteRegisterValue(api.registers.x86_eax) != 12345)
    return 1;

  cpy = *reinterpret_cast<triton::arch::x86::x86Cpu*>(api.getCpuInstance());
  if (cpy.getConcreteRegisterValue(api.registers.x86_eax) != 12345) {
    std::cerr << "test_2: KO (cpy context != api context)" << std::endl;
    return 1;
  }

  std::cout << "test_2: OK" << std::endl;
  return 0;
}


int test_3(void) {
  triton::arch::BitsVector bv;
  std::stringstream        s;

  bv.setHigh(31);
  bv.setLow(0);
  s << &bv;
  if (s.str() != "bv[31..0]") {
    std::cerr << "test_3: KO (" << s.str() << " != bv[31..0])" << std::endl;
    return 1;
  }

  std::cout << "test_3: OK" << std::endl;
  return 0;
}


int test_4(void) {
  triton::arch::Immediate imm;

  imm.setValue(0xff, 1);
  if (imm.getValue() != 0xff) {
    std::cerr << "test_4: KO (" << std::hex << imm.getValue() << std::dec << " != 0xff)" << std::endl;
    return 1;
  }

  imm.setValue(0x1122, 1);
  if (imm.getValue() != 0x22) {
    std::cerr << "test_4: KO (" << std::hex << imm.getValue() << std::dec << " != 0x22)" << std::endl;
    return 1;
  }

  imm.setValue(0x1122, 2);
  if (imm.getValue() != 0x1122) {
    std::cerr << "test_4: KO (" << std::hex << imm.getValue() << std::dec << " != 0x1122)" << std::endl;
    return 1;
  }

  if (imm.getLow() != 0) {
    std::cerr << "test_4: KO (" << std::hex << imm.getLow() << std::dec << " != 0)" << std::endl;
    return 1;
  }

  if (imm.getHigh() != 15) {
    std::cerr << "test_4: KO (" << std::hex << imm.getHigh() << std::dec << " != 15)" << std::endl;
    return 1;
  }

  triton::arch::Immediate imm1(12345, 8);
  triton::arch::Immediate imm2(12345, 8);
  if (imm1 != imm2) {
    std::cerr << "test_4: KO (" << imm2 << " != " << imm2 << ")" << std::endl;
    return 1;
  }

  std::cout << "test_4: OK" << std::endl;
  return 0;
}


int test_5(void) {
  triton::arch::Immediate imm1(0xff, 1);
  triton::arch::Immediate imm2(0xff, 2);
  triton::arch::MemoryAccess mem1(0x1000, 1);
  triton::arch::MemoryAccess mem2(0x1001, 1);
  triton::arch::OperandWrapper op1(imm1);
  triton::arch::OperandWrapper op2(imm2);
  triton::arch::OperandWrapper op3(mem1);
  triton::arch::OperandWrapper op4(mem2);
  std::stringstream s1;
  std::stringstream s2;

  if (op1 == op2) {
    std::cerr << "test_5: KO (" << op1 << " == " << op2 << ")" << std::endl;
    return 1;
  }

  if (op1.getType() != op2.getType()) {
    std::cerr << "test_5: KO (" << op1.getType() << " == " << op2.getType() << ")" << std::endl;
    return 1;
  }

  if (op1.getImmediate() != imm1) {
    std::cerr << "test_5: KO (" << op1.getImmediate() << " != " << imm1 << ")" << std::endl;
    return 1;
  }

  if (op1.getSize() != imm1.getSize()) {
    std::cerr << "test_5: KO (" << op1.getSize() << " != " << imm1.getSize() << ")" << std::endl;
    return 1;
  }

  if (op1.getHigh() != imm1.getHigh()) {
    std::cerr << "test_5: KO (" << op1.getHigh() << " != " << imm1.getHigh() << ")" << std::endl;
    return 1;
  }

  if (op1.getLow() != imm1.getLow()) {
    std::cerr << "test_5: KO (" << op1.getLow() << " != " << imm1.getLow() << ")" << std::endl;
    return 1;
  }

  triton::arch::OperandWrapper opx = op1;
  if (opx != op1) {
    std::cerr << "test_5: KO (" << opx << " == " << op1 << ")" << std::endl;
    return 1;
  }

  s1 << &op1;
  s2 << &imm1;
  if (s1.str() != s2.str()) {
    std::cerr << "test_3: KO (" << s1.str() << " != " << s2.str() << ")" << std::endl;
    return 1;
  }

  if (op2 < op1) {
    std::cerr << "test_3: KO (" << op2 << " < " << op1 << ")" << std::endl;
    return 1;
  }

  if (op3 == op4) {
    std::cerr << "test_5: KO (" << op3 << " == " << op4 << ")" << std::endl;
    return 1;
  }

  op3 = op4;
  if (op3 != op4) {
    std::cerr << "test_5: KO (" << op3 << " != " << op4 << ")" << std::endl;
    return 1;
  }

  op3.setMemory(mem2);
  if (op3.getMemory() != mem2) {
    std::cerr << "test_5: KO (" << op3.getMemory() << " != " << mem2 << ")" << std::endl;
    return 1;
  }

  op1.setImmediate(imm2);
  if (op1.getImmediate() != imm2) {
    std::cerr << "test_5: KO (" << op1.getImmediate() << " != " << imm2 << ")" << std::endl;
    return 1;
  }

  std::cout << "test_5: OK" << std::endl;
  return 0;
}


int test_6(void) {
  triton::API ctx;

  ctx.setArchitecture(triton::arch::ARCH_X86_64);
  triton::arch::Instruction inst1((const unsigned char*)"\x48\x89\xd8", 3); // mov rax, rbx
  triton::arch::Instruction inst2;

  ctx.processing(inst1);
  inst2 = inst1;

  if (inst2.getType() != inst1.getType()) {
    std::cerr << "test_6: KO (" << inst2.getType() << " != " << inst1.getType() << ")" << std::endl;
    return 1;
  }

  triton::arch::Instruction inst3(inst2);
  if (inst3.getType() != inst2.getType()) {
    std::cerr << "test_6: KO (" << inst3.getType() << " != " << inst2.getType() << ")" << std::endl;
    return 1;
  }

  if (!inst3.isReadFrom(triton::arch::OperandWrapper(ctx.getRegister(triton::arch::ID_REG_X86_RBX)))) {
    std::cerr << "test_6: KO (!isReadFrom(rbx))" << std::endl;
    return 1;
  }

  inst3.removeReadRegister(ctx.getRegister(triton::arch::ID_REG_X86_RBX));
  if (inst3.isReadFrom(triton::arch::OperandWrapper(ctx.getRegister(triton::arch::ID_REG_X86_RBX)))) {
    std::cerr << "test_6: KO (isReadFrom(rbx))" << std::endl;
    return 1;
  }

  if (!inst3.isWriteTo(triton::arch::OperandWrapper(ctx.getRegister(triton::arch::ID_REG_X86_RAX)))) {
    std::cerr << "test_6: KO (!isWriteTo(rax))" << std::endl;
    return 1;
  }

  inst3.removeWrittenRegister(ctx.getRegister(triton::arch::ID_REG_X86_RAX));
  if (inst3.isWriteTo(triton::arch::OperandWrapper(ctx.getRegister(triton::arch::ID_REG_X86_RAX)))) {
    std::cerr << "test_6: KO (isReadFrom(rax))" << std::endl;
    return 1;
  }

  if (inst3.isSymbolized()) {
    std::cerr << "test_6: KO (isSymbolized)" << std::endl;
    return 1;
  }

  if (inst3.isTainted()) {
    std::cerr << "test_6: KO (isTainted)" << std::endl;
    return 1;
  }

  inst3.setTaint(true);
  if (!inst3.isTainted()) {
    std::cerr << "test_6: KO (!isTainted)" << std::endl;
    return 1;
  }

  triton::arch::Instruction inst4((const unsigned char*)"\x48\x8b\x03", 3); // mov rax, [rbx]
  ctx.processing(inst4);
  if (!inst4.isReadFrom(triton::arch::OperandWrapper(triton::arch::MemoryAccess(0, 8)))) {
    std::cerr << "test_6: KO (!isReadFrom(0x0))" << std::endl;
    return 1;
  }

  inst4.removeLoadAccess(triton::arch::MemoryAccess(0, 8));
  if (inst4.isReadFrom(triton::arch::OperandWrapper(triton::arch::MemoryAccess(0, 8)))) {
    std::cerr << "test_6: KO (isReadFrom(0x0))" << std::endl;
    return 1;
  }

  triton::arch::Instruction inst5((const unsigned char*)"\x48\x89\x18", 3); // mov [rax], rbx
  ctx.processing(inst5);
  if (!inst5.isWriteTo(triton::arch::OperandWrapper(triton::arch::MemoryAccess(0, 8)))) {
    std::cerr << "test_6: KO (!isWriteTo(0x0))" << std::endl;
    return 1;
  }

  inst5.removeStoreAccess(triton::arch::MemoryAccess(0, 8));
  if (inst5.isWriteTo(triton::arch::OperandWrapper(triton::arch::MemoryAccess(0, 8)))) {
    std::cerr << "test_6: KO (isWriteTo(0x0))" << std::endl;
    return 1;
  }

  triton::arch::Instruction inst6((const unsigned char*)"\xb0\x01", 2); // mov al, 1
  ctx.processing(inst6);
  if (!inst6.isReadFrom(triton::arch::OperandWrapper(triton::arch::Immediate(1, 1)))) {
    std::cerr << "test_6: KO (!isReadFrom(1))" << std::endl;
    return 1;
  }

  inst5.removeReadImmediate(triton::arch::Immediate(1, 1));
  if (inst5.isReadFrom(triton::arch::OperandWrapper(triton::arch::Immediate(1, 1)))) {
    std::cerr << "test_6: KO (isReadFrom(1))" << std::endl;
    return 1;
  }

  std::cout << "test_6: OK" << std::endl;
  return 0;
}


int test_7(void) {
  triton::API ctx;

  ctx.setArchitecture(triton::arch::ARCH_X86);

  triton::arch::Instruction  inst1((const unsigned char*)"\x37", 1); // aaa
  triton::arch::Instruction  inst2((const unsigned char*)"\xd5\x0a", 2); // aad
  triton::arch::Instruction  inst3((const unsigned char*)"\xd5\x08", 2); // aad 8
  triton::arch::Instruction  inst4((const unsigned char*)"\xd4\x08", 2); // aam
  triton::arch::Instruction  inst5((const unsigned char*)"\xd4\x08", 2); // aam 8
  triton::arch::Instruction  inst6((const unsigned char*)"\x3f", 1); // aas
  triton::arch::Instruction  inst7((const unsigned char*)"\x0f\x06", 2); // clts
  triton::arch::Instruction  inst8((const unsigned char*)"\xfa", 1); // cli
  triton::arch::Instruction  inst9((const unsigned char*)"\x0f\xa2", 2); // cpuid
  triton::arch::Instruction inst10((const unsigned char*)"\x0f\x08", 2); // invd
  triton::arch::Instruction inst11((const unsigned char*)"\x0f\x01\x38", 3); // invlpg [eax]
  triton::arch::Instruction inst12((const unsigned char*)"\x0f\xae\x38", 3); // clflush [eax]
  triton::arch::Instruction inst13((const unsigned char*)"\x98", 1); // cwde
  triton::arch::Instruction inst14((const unsigned char*)"\x0f\xae\x10", 3); // ldmxcsr [eax]
  triton::arch::Instruction inst15((const unsigned char*)"\x0f\xae\xe8", 3); // lfence
  triton::arch::Instruction inst16((const unsigned char*)"\x0f\xae\xf0", 3); // mfence
  triton::arch::Instruction inst17((const unsigned char*)"\xf2\x0f\xd6\xc9", 4); // movdq2q mm1, xmm1
  triton::arch::Instruction inst18((const unsigned char*)"\x66\x0f\xe7\x08", 4); // movntdq [eax], xmm1
  triton::arch::Instruction inst19((const unsigned char*)"\x0f\xc3\x18", 3); // movnti [eax], ebx
  triton::arch::Instruction inst20((const unsigned char*)"\x66\x0f\x2b\x08", 4); // movntpd [eax], xmm1
  triton::arch::Instruction inst21((const unsigned char*)"\x0f\x2b\x08", 3); // movntps [eax], xmm1
  triton::arch::Instruction inst22((const unsigned char*)"\x0f\xe7\x08", 3); // movntq [eax], mm1
  triton::arch::Instruction inst23((const unsigned char*)"\x0f\xe7\x08", 3); // movntq [eax], mm1
  triton::arch::Instruction inst24((const unsigned char*)"\xf3\x0f\xd6\xca", 4); // movq2dq xmm1, mm2
  triton::arch::Instruction inst25((const unsigned char*)"\x66\x0f\xd6\x08", 4); // movq [eax], xmm1
  triton::arch::Instruction inst26((const unsigned char*)"\x66\x0f\xdb\xca", 4); // pand xmm1, xmm2
  triton::arch::Instruction inst27((const unsigned char*)"\x66\x0f\xdf\xca", 4); // pandn xmm1, xmm2
  triton::arch::Instruction inst28((const unsigned char*)"\xf3\x90", 2); // pause
  triton::arch::Instruction inst29((const unsigned char*)"\x61", 1); // popal
  triton::arch::Instruction inst30((const unsigned char*)"\x9d", 1); // popfd
  triton::arch::Instruction inst31((const unsigned char*)"\x66\x0f\xeb\xca", 4); // por xmm1, xmm2
  triton::arch::Instruction inst33((const unsigned char*)"\x0f\x18\x00", 3); // prefetchnta [eax]
  triton::arch::Instruction inst34((const unsigned char*)"\x0f\x18\x08", 3); // prefetcht0 [eax]
  triton::arch::Instruction inst35((const unsigned char*)"\x0f\x18\x10", 3); // prefetcht1 [eax]
  triton::arch::Instruction inst36((const unsigned char*)"\x0f\x18\x18", 3); // prefetcht2 [eax]
  triton::arch::Instruction inst37((const unsigned char*)"\x0f\x0d\x08", 3); // prefetchw [eax]
  triton::arch::Instruction inst38((const unsigned char*)"\x0f\x70\xca\x08", 4); // pshufw mm1, mm2, 8
  triton::arch::Instruction inst39((const unsigned char*)"\x60", 1); // pushal
  triton::arch::Instruction inst40((const unsigned char*)"\x9c", 1); // pushfd
  triton::arch::Instruction inst41((const unsigned char*)"\x0f\x31", 2); // rdtsc
  triton::arch::Instruction inst42((const unsigned char*)"\x0f\xae\xf8", 3); // sfence
  triton::arch::Instruction inst43((const unsigned char*)"\xfb", 1); // sti
  triton::arch::Instruction inst44((const unsigned char*)"\x0f\xae\x18", 3); // stmxcsr [eax]
  triton::arch::Instruction inst45((const unsigned char*)"\x9b", 1); // wait
  triton::arch::Instruction inst46((const unsigned char*)"\x0f\x09", 2); // wbinvd

  try {
    ctx.processing(inst1);
    ctx.processing(inst2);
    ctx.processing(inst3);
    ctx.processing(inst4);
    ctx.processing(inst5);
    ctx.processing(inst6);
    ctx.processing(inst7);
    ctx.processing(inst8);
    ctx.processing(inst9);
    ctx.processing(inst10);
    ctx.processing(inst11);
    ctx.processing(inst12);
    ctx.processing(inst13);
    ctx.processing(inst14);
    ctx.processing(inst15);
    ctx.processing(inst16);
    ctx.processing(inst17);
    ctx.processing(inst18);
    ctx.processing(inst19);
    ctx.processing(inst20);
    ctx.processing(inst21);
    ctx.processing(inst22);
    ctx.processing(inst23);
    ctx.processing(inst24);
    ctx.processing(inst25);
    ctx.processing(inst26);
    ctx.processing(inst27);
    ctx.processing(inst28);
    ctx.processing(inst29);
    ctx.processing(inst30);
    ctx.processing(inst31);
    ctx.processing(inst33);
    ctx.processing(inst34);
    ctx.processing(inst35);
    ctx.processing(inst36);
    ctx.processing(inst37);
    ctx.processing(inst38);
    ctx.processing(inst39);
    ctx.processing(inst40);
    ctx.processing(inst41);
    ctx.processing(inst42);
    ctx.processing(inst43);
    ctx.processing(inst44);
    ctx.processing(inst45);
    ctx.processing(inst46);
  }
  catch (const triton::exceptions::Exception& e) {
    std::cerr << "test_7: KO (bad semantics building)" << std::endl;
    return 1;
  }

  std::cout << "test_7: OK" << std::endl;
  return 0;
}


int test_8(void) {
  triton::arch::arm::aarch64::AArch64Cpu cpy;
  triton::API api;

  api.setArchitecture(triton::arch::ARCH_AARCH64);
  api.setConcreteRegisterValue(api.registers.aarch64_x0, 12345);

  if (api.getConcreteRegisterValue(api.registers.aarch64_x0) != 12345)
    return 1;

  cpy = *reinterpret_cast<triton::arch::arm::aarch64::AArch64Cpu*>(api.getCpuInstance());
  if (cpy.getConcreteRegisterValue(api.registers.aarch64_x0) != 12345) {
    std::cerr << "test_8: KO (cpy context != api context)" << std::endl;
    return 1;
  }

  std::cout << "test_8: OK" << std::endl;
  return 0;
}


int test_9(void) {
  triton::API api;

  api.setArchitecture(triton::arch::ARCH_X86_64);

  triton::engines::symbolic::PathConstraint pco;
  auto node = api.getAstContext()->equal(api.getAstContext()->bvtrue(), api.getAstContext()->bvtrue());
  pco.addBranchConstraint(false, 0x123, 0x100, node);
  pco.addBranchConstraint(true,  0x123, 0x200, node);
  pco.addBranchConstraint(false, 0x123, 0x300, node);
  api.pushPathConstraint(pco);

  if (api.getPathConstraints().size() != 1) {
    std::cerr << "test_9: KO (pathConstraints size != 1)" << std::endl;
    return 1;
  }

  auto branches = api.getPathConstraints().at(0).getBranchConstraints();
  if (branches.size() != 3) {
    std::cerr << "test_9: KO (branches size != 3)" << std::endl;
    return 1;
  }

  auto br1 = branches.at(0);
  if ((std::get<0>(br1) != false) ||
      (std::get<1>(br1) != 0x123) ||
      (std::get<2>(br1) != 0x100) ||
      (std::get<3>(br1)->getHash() != node->getHash())) {
    std::cerr << "test_9: KO (wrong br1)" << std::endl;
    return 1;
  }
  auto br2 = branches.at(1);
  if ((std::get<0>(br2) != true)  ||
      (std::get<1>(br2) != 0x123) ||
      (std::get<2>(br2) != 0x200) ||
      (std::get<3>(br2)->getHash() != node->getHash())) {
    std::cerr << "test_9: KO (wrong br2)" << std::endl;
    return 1;
  }
  auto br3 = branches.at(2);
  if ((std::get<0>(br3) != false) ||
      (std::get<1>(br3) != 0x123) ||
      (std::get<2>(br3) != 0x300) ||
      (std::get<3>(br3)->getHash() != node->getHash())) {
    std::cerr << "test_9: KO (wrong br3)" << std::endl;
    return 1;
  }

  std::cout << "test_9: OK" << std::endl;
  return 0;
}


#ifdef TRITON_LLVM_INTERFACE
bool smt_proof(triton::API& ctx, const triton::ast::SharedAbstractNode& node1, const triton::ast::SharedAbstractNode& node2) {
  auto actx = ctx.getAstContext();
  if (ctx.isSat(actx->distinct(node1, node2)) == false)
    return true;
  return false;
}


int test_10(void) {
  triton::API ctx(triton::arch::ARCH_X86_64);
  auto actx = ctx.getAstContext();
  auto varx = ctx.newSymbolicVariable(8, "x");

  std::list<triton::ast::SharedAbstractNode> nodes = {
    /* bitvector */
    actx->bvadd(actx->bv(10, 8), actx->variable(varx)),
    actx->bvadd(actx->variable(varx), actx->bv(11, 8)),
    actx->bvand(actx->bv(12, 8), actx->variable(varx)),
    actx->bvashr(actx->bv(13, 8), actx->variable(varx)),
    actx->bvlshr(actx->bv(14, 8), actx->variable(varx)),
    actx->bvmul(actx->bv(15, 8), actx->variable(varx)),
    actx->bvnand(actx->bv(16, 8), actx->variable(varx)),
    actx->bvneg(actx->bv(17, 8)),
    actx->bvneg(actx->variable(varx)),
    actx->bvnor(actx->bv(18, 8), actx->variable(varx)),
    actx->bvnot(actx->bv(19, 8)),
    actx->bvnot(actx->variable(varx)),
    actx->bvor(actx->bv(20, 8), actx->variable(varx)),
    actx->bvrol(actx->variable(varx), actx->bv(21, 8)),
    actx->bvror(actx->variable(varx), actx->bv(22, 8)),
    actx->bvsdiv(actx->variable(varx), actx->bv(23, 8)),
    actx->bvshl(actx->variable(varx), actx->bv(24, 8)),
    actx->bvsmod(actx->variable(varx), actx->bv(25, 8)),
    actx->bvsrem(actx->variable(varx), actx->bv(26, 8)),
    actx->bvsub(actx->bv(27, 8), actx->variable(varx)),
    actx->bvudiv(actx->variable(varx), actx->bv(28, 8)),
    actx->bvurem(actx->variable(varx), actx->bv(29, 8)),
    actx->bvxnor(actx->bv(30, 8), actx->variable(varx)),
    actx->bvxor(actx->bv(31, 8), actx->variable(varx)),
    actx->sx(24, actx->variable(varx)),
    actx->sx(8, actx->variable(varx)),
    actx->zx(24, actx->variable(varx)),
    actx->zx(8, actx->variable(varx)),
    actx->bswap(actx->variable(varx)),

    /* logical */
    actx->equal(actx->bv(32, 8), actx->variable(varx)),
    actx->distinct(actx->bv(33, 8), actx->variable(varx)),
    actx->bvsge(actx->bv(34, 8), actx->variable(varx)),
    actx->bvsgt(actx->bv(35, 8), actx->variable(varx)),
    actx->bvsle(actx->bv(36, 8), actx->variable(varx)),
    actx->bvslt(actx->bv(37, 8), actx->variable(varx)),
    actx->bvuge(actx->bv(38, 8), actx->variable(varx)),
    actx->bvugt(actx->bv(39, 8), actx->variable(varx)),
    actx->bvule(actx->bv(40, 8), actx->variable(varx)),
    actx->bvult(actx->bv(41, 8), actx->variable(varx)),
    actx->bvsge(actx->variable(varx), actx->bv(34, 8)),
    actx->bvsgt(actx->variable(varx), actx->bv(35, 8)),
    actx->bvsle(actx->variable(varx), actx->bv(36, 8)),
    actx->bvslt(actx->variable(varx), actx->bv(37, 8)),
    actx->bvuge(actx->variable(varx), actx->bv(38, 8)),
    actx->bvugt(actx->variable(varx), actx->bv(39, 8)),
    actx->bvule(actx->variable(varx), actx->bv(40, 8)),
    actx->bvult(actx->variable(varx), actx->bv(41, 8)),
    actx->land(actx->equal(actx->bv(10, 8), actx->variable(varx)), actx->bvsge(actx->bv(10, 8), actx->variable(varx))),
    actx->lor(actx->equal(actx->bv(10, 8), actx->variable(varx)), actx->bvsge(actx->bv(10, 8), actx->variable(varx))),
    actx->lxor(actx->equal(actx->bv(10, 8), actx->variable(varx)), actx->bvsge(actx->bv(10, 8), actx->variable(varx))),

    /* misc */
    actx->concat(actx->concat(actx->concat(actx->bv(50, 8), actx->variable(varx)), actx->bv(0xff, 8)), actx->variable(varx)),
    actx->extract(11, 4, actx->concat(actx->bv(0xff, 8), actx->variable(varx))),
    actx->ite(actx->equal(actx->bv(52, 8), actx->bv(60, 8)), actx->variable(varx), actx->bvadd(actx->variable(varx), actx->bv(1, 8))),
    actx->ite(actx->equal(actx->bv(53, 8), actx->bv(61, 8)), actx->variable(varx), actx->bvadd(actx->variable(varx), actx->bv(2, 8))),
    actx->ite(actx->bvsge(actx->bv(54, 8), actx->bv(62, 8)), actx->variable(varx), actx->bvadd(actx->variable(varx), actx->bv(3, 8))),
    actx->ite(actx->bvslt(actx->bv(55, 8), actx->variable(varx)), actx->variable(varx), actx->bvadd(actx->variable(varx), actx->bv(4, 8))),
  };

  for (const auto& node : nodes) {
    /* Triton to LLVM */
    llvm::LLVMContext llvmContext;
    triton::ast::TritonToLLVM ttllvm(llvmContext);
    auto llvmModule = ttllvm.convert(node);
    //std::cerr << "IN: " << node << std::endl;

    /* LLVM to Triton */
    triton::ast::LLVMToTriton llvmtt(actx);
    auto nout = llvmtt.convert(llvmModule.get());
    //std::cerr << "OUT: " << nout << std::endl;

    if (smt_proof(ctx, node, nout) == false) {
      //std::cerr << "Node not equal" << std::endl;
      //std::cerr << "IN: " << node << std::endl;
      //std::cerr << "OUT: " << nout << std::endl;
      return 1;
    }
  }

  std::cout << "test_10: OK" << std::endl;
  return 0;
}
#endif


int main(int ac, const char **av) {
  if (test_1())
    return 1;

  if (test_2())
    return 1;

  if (test_3())
    return 1;

  if (test_4())
    return 1;

  if (test_5())
    return 1;

  if (test_6())
    return 1;

  if (test_7())
    return 1;

  if (test_8())
    return 1;

  if (test_9())
    return 1;

  #ifdef TRITON_LLVM_INTERFACE
  if (test_10())
    return 1;
  #endif

  return 0;
}
