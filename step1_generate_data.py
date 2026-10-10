"""
Step 1: 生成一段带故障特征的电机振动信号

背景：
  正常电机的振动主要来自转频（1倍频）及其谐波。
  当轴承出现故障时，会在特定频率上出现能量突增
  —— 这就是"故障特征频率"，例如外圈故障频率 BPFO。

这个脚本会：
  1. 合成一段正常振动信号（转频 + 谐波 + 噪声）
  2. 在其中人为埋入一个外圈故障成分
  3. 保存成 CSV，供后面的脚本分析
"""

import numpy as np
import pandas as pd

np.random.seed(42)

# ---------- 参数设置（试着改这些值，看结果怎么变）----------
fs = 10000          # 采样率 Hz（每秒采多少个点）
duration = 2.0      # 采样时长 秒
fr = 25.0           # 转频 Hz（电机转速 1500 rpm = 25 Hz）
bpfo = 105.0        # 外圈故障特征频率 Hz（后面要靠傅里叶变换把它找出来）

t = np.arange(0, duration, 1 / fs)   # 时间轴

# ---------- 1. 正常振动：转频 + 2/3 倍频 ----------
normal = (
    1.0 * np.sin(2 * np.pi * fr * t)
    + 0.4 * np.sin(2 * np.pi * 2 * fr * t)
    + 0.2 * np.sin(2 * np.pi * 3 * fr * t)
)

# ---------- 2. 埋入外圈故障成分（周期性冲击）----------
fault = 0.6 * np.sin(2 * np.pi * bpfo * t)

# ---------- 3. 加噪声（真实信号一定有噪）----------
noise = 0.3 * np.random.randn(len(t))

signal = normal + fault + noise

# ---------- 保存 ----------
df = pd.DataFrame({"time_s": t, "vibration_g": signal})
df.to_csv("data/motor_vibration.csv", index=False)

print(f"生成完成：{len(df)} 个采样点，时长 {duration}s")
print(f"信号统计：均值 {signal.mean():.4f}，标准差 {signal.std():.4f}")
print("已保存到 data/motor_vibration.csv")
print(f"\n埋入的故障频率是 {bpfo} Hz —— 用 step2 去把它找出来！")
