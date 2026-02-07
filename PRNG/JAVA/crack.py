class JavaRandomCracker:
    """
    利用 2 个连续样本，穷举缺失的低 16 位状态 (2^16 次尝试) 还原 Seed。
    """
    def __init__(self, val1, val2):
        self.state = None
        # Java LCG 标准参数
        self.MULTIPLIER = 0x5DEECE66D
        self.ADDEND = 0xB
        self.MASK = (1 << 48) - 1

        # 转为无符号整数 (处理 Java 的有符号 int 输出)
        v1_u = val1 & 0xffffffff
        v2_u = val2 & 0xffffffff

        print(f"    样本 1 (Unsigned): {v1_u}")
        print(f"    样本 2 (Unsigned): {v2_u}")

        # === 核心逻辑 ===
        # v1 提供了 State 的高 32 位，只需穷举低 16 位 (0-65535)
        # 找到能演进出 v2 的那个状态即为真 Seed
        
        found = False
        for low_16 in range(65536):
            # 1. 拼凑猜测状态 (High_32 | Low_16)
            candidate_state = (v1_u << 16) | low_16
            
            # 2. 演进一次状态 (LCG 公式)
            next_state = (candidate_state * self.MULTIPLIER + self.ADDEND) & self.MASK
            
            # 3. 检查高 32 位是否匹配样本 2
            if (next_state >> 16) == v2_u:
                print(f"[+] 破解成功! 找到低 16 位: {low_16}")
                print(f"    当前 Seed: {next_state}")
                self.state = next_state
                found = True
                break
        
        if not found:
            print("[-] 破解失败，样本可能不连续。")
            exit()

    def next_int(self):
        """模拟 Java random.nextInt()"""
        if self.state is None: return 0
        
        # LCG 状态更新
        self.state = (self.state * self.MULTIPLIER + self.ADDEND) & self.MASK
        
        # 获取高 32 位并转回 Java 有符号 int
        res_u = self.state >> 16
        return res_u - 4294967296 if res_u > 2147483647 else res_u

# --- 使用示例 ---
if __name__ == "__main__":
    input1 = -1631771576
    input2 = 595259081
        
    cracker = JavaRandomCracker(input1, input2)
    
    print("-" * 30)
    for i in range(3):
        print(f"Next #{i+1}: {cracker.next_int()}")