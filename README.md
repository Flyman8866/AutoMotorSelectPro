# AutoMotorSelectPro

Python 3.12 + PySide6 的伺服电机筛选示例项目。

> **DEMO_ONLY_NOT_FOR_ENGINEERING_USE**

## 功能

- 硬筛选逻辑：
  - 峰值转矩不足淘汰
  - RMS 连续转矩不足淘汰
  - 最高转速不足淘汰
  - 惯量比过大淘汰
  - 垂直轴需要抱闸时，无抱闸电机淘汰
- 图形界面（PySide6）演示筛选
- `--smoke-test` 快速自检

## 运行

```bash
pip install -r requirements.txt
python main.py --smoke-test
python main.py
```

## 测试

```bash
python -m pytest
```
