"""
Step 2: 时域 + 频域分析

这个脚本做三件事：
  1. 读入振动信号数据
  2. 做时域统计（均值、RMS、峰值）
  3. 做 FFT 得到频谱，把故障频率找出来
  4. 画图保存

运行前先跑 step1_generate_data.py
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # 无界面环境也能出图
import matplotlib.pyplot as plt

# 让 matplotlib 正常显示中文
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ---------- 1. 读数据 ----------
df = pd.read_csv("data/motor_vibration.csv")
t = df["time_s"].values
x = df["vibration_g"].values

fs = 1 / (t[1] - t[0])         # 从时间轴反推采样率
print(f"采样点数: {len(x)}，采样率: {fs:.0f} Hz")

# ---------- 2. 时域指标 ----------
print("\n=== 时域统计 ===")
print(f"均值     : {x.mean():.4f} g")
print(f"标准差   : {x.std():.4f} g")
print(f"RMS      : {np.sqrt(np.mean(x**2)):.4f} g")
print(f"峰值     : {np.max(np.abs(x)):.4f} g")
print(f"峭度     : {pd.Series(x).kurt():.4f}   (正常信号≈3，有冲击时会变大)")

# ---------- 3. 频域分析（FFT）----------
N = len(x)
xf = np.fft.rfft(x)                  # 实数傅里叶变换
freqs = np.fft.rfftfreq(N, 1 / fs)   # 对应的频率轴
amp = np.abs(xf) * 2 / N             # 幅值归一化

# ---------- 4. 找峰值 ----------
peak_idx = np.argsort(amp)[-5:][::-1]   # 幅值最大的 5 个频率
print("\n=== 频谱中的主要频率成分 ===")
for i in peak_idx:
    print(f"  {freqs[i]:7.1f} Hz   幅值 {amp[i]:.4f}")

# ---------- 5. 画图 ----------
fig, axes = plt.subplots(2, 1, figsize=(11, 7))

axes[0].plot(t[:1000], x[:1000], linewidth=0.8)
axes[0].set_title("时域波形（前 1000 个采样点）")
axes[0].set_xlabel("时间 (s)")
axes[0].set_ylabel("振动加速度 (g)")
axes[0].grid(alpha=0.3)

axes[1].plot(freqs, amp, linewidth=0.9, color="crimson")
axes[1].set_xlim(0, 300)             # 只看 0-300 Hz
axes[1].set_title("频谱（FFT）")
axes[1].set_xlabel("频率 (Hz)")
axes[1].set_ylabel("幅值 (g)")
axes[1].grid(alpha=0.3)
axes[1].axvline(105, color="blue", linestyle="--", alpha=0.6, label="埋入的故障频率 105Hz")
axes[1].legend()

plt.tight_layout()
plt.savefig("data/analysis_result.png", dpi=120)
print("\n图已保存到 data/analysis_result.png")
print("看看频谱里 105 Hz 附近是不是有个明显的尖峰？")
