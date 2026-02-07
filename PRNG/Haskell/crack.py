import sys

class SplitMix64Cracker:
    """
    针对 Haskell System.Random (SplitMix64) 的预测算法。
    需要 2 个连续的 Word64 输出即可完全破解。
    """
    # SplitMix64 标准混合常量
    MASK = (1 << 64) - 1
    MIX_K1 = 0xff51afd7ed558ccd
    MIX_K2 = 0xc4ceb9fe1a85ec53

    def __init__(self, out1, out2):
        """
        初始化破解器。
        :param out1: 第一个观察到的 Word64 (int)
        :param out2: 紧接着的第二个 Word64 (int)
        """
        # 1. 逆向混淆，还原内部状态 Seed
        s1 = self._unmix64(out1)
        s2 = self._unmix64(out2)

        # 2. 计算步长 Gamma (State2 - State1)
        # 注意：在 Haskell 中，gamma 必须是奇数，这里自动推导
        self.gamma = (s2 - s1) & self.MASK
        
        # 3. 保存当前状态 (指向 out2 之后的状态)
        self.state = s2

        print(f"[+] Cracker Initialized!")
        print(f"    Recovered Gamma: {self.gamma}")
        print(f"    Current State  : {self.state}")

    def predict_next(self):
        """预测下一个随机数"""
        # 更新状态：State = State + Gamma
        self.state = (self.state + self.gamma) & self.MASK
        # 混淆输出
        return self._mix64(self.state)

    def _shift_xor(self, n, w):
        return w ^ (w >> n)

    def _mix64(self, z):
        """正向混合函数 (Haskell 的 mix64)"""
        z = (self._shift_xor(33, z) * self.MIX_K1) & self.MASK
        z = (self._shift_xor(33, z) * self.MIX_K2) & self.MASK
        return self._shift_xor(33, z)

    def _unmix64(self, z):
        """
        逆向混合函数 (数学逆运算)
        利用模逆元 (Modular Inverse) 还原状态
        """
        # reverse mix64
        
        z = self._shift_xor(33, z)
        
        k2_inv = pow(self.MIX_K2, -1, 1 << 64)
        z = (z * k2_inv) & self.MASK
        
        z = self._shift_xor(33, z)
        
        k1_inv = pow(self.MIX_K1, -1, 1 << 64)
        z = (z * k1_inv) & self.MASK
        
        z = self._shift_xor(33, z)
        return z

# Example
if __name__ == "__main__":
    obs1 = 17586405056036639638
    obs2 = 4338398458645668384
    
    print(f"样本1: {obs1}")
    print(f"样本2: {obs2}")

    # 1. 初始化破解器
    cracker = SplitMix64Cracker(obs1, obs2)

    # 2. 预测接下来的 3 个数
    print("预测结果 (Predicting next 3 numbers):")
    for i in range(3):
        pred = cracker.predict_next()
        print(f"Next #{i+1}: {pred}")