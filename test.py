from keystone import *
from triton_test.triton import *
from arybo.tools import *

try:
    from auto import *
except ImportError:
    pass

ks = keystone.Ks(KS_ARCH_X86, KS_MODE_64)

ctx = TritonContext()
astCtx = ctx.getAstContext()
ctx.setArchitecture(ARCH.X86_64)
ctx.setAstRepresentationMode(AST_REPRESENTATION.SMT)
ctx.setMode(MODE.ALIGNED_MEMORY, True)
ctx.setMode(MODE.ONLY_ON_SYMBOLIZED, True)

rax = ctx.getRegister("rax")
rbx = ctx.getRegister("rbx")
rcx = ctx.getRegister("rcx")
rdx = ctx.getRegister("rdx")
rsp = ctx.getRegister("rsp")
rip = ctx.getRegister("rip")
zf = ctx.getRegister("zf")

ctx.symbolizeRegister(rax, "sym_rax")
ctx.symbolizeRegister(rbx, "sym_rbx")
ctx.setConcreteRegisterValue(ctx.registers.rcx, 1)
ctx.setConcreteRegisterValue(ctx.registers.rdx, 1)
ctx.setConcreteRegisterValue(ctx.registers.rsi, 0x4f0000)
ctx.setConcreteRegisterValue(ctx.registers.rdx, 0x4f0000)
ctx.setConcreteRegisterValue(ctx.registers.rsp, 0x4f100c)
ctx.setConcreteRegisterValue(ctx.registers.rbp, 0x4f100c)
ctx.setConcreteMemoryAreaValue(0x4f1000, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# code = [ks.asm(r"add rax,rbx")[0], ks.asm(r"mov rdx,rbx")[0], ks.asm(r"add rax,rbx")[0], ks.asm(r"mov rdx,rax")[0],
#         ks.asm(r"mov rax,rbx")[0]]
code = [ks.asm(r"mov rcx,rax")[0],
        ks.asm(r"push rax")[0],
        ks.asm(r"pop rbx")[0],
        ks.asm(r"mov ds:[esp],bl")[0],
        ks.asm(r"pop rcx")[0],
        ks.asm(r"xor rcx,rcx")[0],
        # ks.asm(r"or cl,1")[0],
        # ks.asm(r"and cl,1")[0],
        # ks.asm(r"movzx rcx,cl")[0]
        ]
code1 = [ks.asm(r"mov  r11,rcx")[0],
         ks.asm(r"mov  rcx,ds:[rdi]")[0],
         ks.asm(r"mov  rax,ds:[rsi]")[0],
         ks.asm(r"push r14")[0],
         ks.asm(r"push r13")[0],
         ks.asm(r"mov  r10d,0x1")[0],
         ks.asm(r"push r12")[0],
         ks.asm(r"push rbp")[0],
         ks.asm(r"lea  r8,[rcx+0x1]")[0],
         ks.asm(r"not  rcx ")[0],
         ks.asm(r"push rbx ")[0],
         ks.asm(r"mov  r9,rcx ")[0],
         ]
addr = 0x401000
for ins in code:
    inst = Instruction()
    inst.setOpcode(bytes(ins))
    # inst.setOpcode(bytes(code[3]))
    inst.setAddress(addr)
    ctx.processing(inst)
    addr = ctx.getConcreteRegisterValue(ctx.registers.rip)
    # for expression in inst.getSymbolicExpressions():
    # print(f"符号表达式 {expression}")
    # print(type(expression))
    # print(
    #   f"ASTNODE {expression.getAst()} 类型 {type(expression.getAst())} 展开{astCtx.unroll(expression.getAst())} 化简{ctx.simplify(astCtx.unroll(expression.getAst()))} AST计算结果 {expression.getAst().evaluate()}")
    # mba = tritonast2arybo(astCtx.unroll(expression.getAst()))
    # print(f"是否符号化 {expression.isSymbolized}")
    # print(f"得到最大寄存器 {expression.getOrigin()}")
    # print(inst.getDisassembly())
    # for reg, ast in inst.getReadRegisters():
    #     print("读取的寄存器", reg)
    # for imm, ast in inst.getReadImmediates():
    #     print("读取的立即数", imm)
    # for reg, ast in inst.getWrittenRegisters():
    #     print("写入的寄存器", reg, "astNode", ast)
    # for mem, ast in inst.getLoadAccess():
    #     print("读取的内存地址", mem)
    #     op = inst.getOperands()
    #     print("op lea astNode eval", hex(op[1].getLeaAst().evaluate()), "scale", op[1].getScale())

print(ctx.getRegisterAst(rcx))
if ctx.getRegisterAst(rcx).isSymbolized():
    print("符号状态")
    print(ctx.getSymbolicRegister(rcx).getAst().evaluate(), astCtx.unroll(ctx.getSymbolicRegister(rcx).getAst()))

print(ctx.getSymbolicRegisterValue(rcx))
print(ctx.getConcreteRegisterValue(rcx))
# print(ctx.getParentRegister(rax))
# print(ctx.isTaintEngineEnabled())
# a = astCtx.bv(1,8)
# b = astCtx.bv(2,8)
# c = astCtx.bv(3,8)
# d = a+b+c
# node = astCtx.bvadd(astCtx.bvand(astCtx.bv(0x12, 8), astCtx.bv(0x45, 8)), astCtx.bv(3, 8))
# print(node)


# def get_leaf(node):
#     if node.getLevel() == 2:
#         print(node, node.evaluate())
#         return
#     for sub in node.getChildren():
#         get_leaf(sub)


# get_leaf(node)
# print(node.setChild(1, astCtx.bv(123,8)))
# print(node.isSigned())
# print(a.equalTo(b))
