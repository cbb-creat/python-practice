# 电机振动信号分析 —— Python 练手项目

这是为你量身做的一个练习项目：**用 Python 分析一段电机振动信号**，
把自动化专业的知识（信号、频谱、故障特征频率）和 Python 数据分析串起来。

## 环境

- Python: `D:\DevTools\Python313\python.exe`
- 已装库: numpy, pandas, matplotlib

## 运行方式

在 VS Code 终端里（已配好），或者直接命令行：

```bash
cd D:/DevTools/python-practice
python step1_generate_data.py    # 生成模拟数据
python step2_analyze.py          # 分析 + 画图
```

## 文件说明

| 文件 | 内容 | 练什么 |
|---|---|---|
| `step1_generate_data.py` | 生成带故障特征的振动信号 | numpy 基础、信号合成 |
| `step2_analyze.py` | 时域 + 频域分析并画图 | pandas、matplotlib、FFT |
| `step3_bearing_fault.py` | 轴承故障频率检测 | 综合应用 |

## 学习建议

1. **别只运行**——每个文件逐行读懂，改参数看结果怎么变
2. 改采样率、故障频率、噪声强度，观察频谱图变化
3. 跑通后自己加一个功能（比如加个汉宁窗，或算一下 RMS）
