# Doro 开发文档

## 项目简介

Doro 是一个桌面宠物应用，提供丰富的交互功能，包括动画展示、系统信息显示、随机移动等。

## 安装步骤

1. 克隆项目代码：

   ```bash
   git clone https://github.com/IMUTshuaiwei/doro
   ```

2. 进入项目目录：

   ```bash
   cd doro
   ```

3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

## 运行方法

1. 启动应用：

   ```bash
   python main.py
   ```

2. 确保资源文件夹 `resources` 存在并包含必要的配置和动画文件。

## 目录结构

```plain
doro/
├── build/               # 构建脚本
├── doc/                 # 文档
├── resources/           # 资源文件（动画、配置等）
├── src/                 # 源代码
│   ├── auto_typehint/   # 自动生成的类型提示
│   ├── state/           # 状态处理器
│   ├── config.py        # 配置管理
│   ├── pet_window.py    # 主窗口逻辑
│   ├── style_sheet.py   # 样式表生成
│   └── setting_gui.py   # 设置界面
└── main.py              # 程序入口
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库。
2. 创建一个新的分支：

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. 提交更改并推送到您的分支：

   ```bash
   git commit -m "描述您的更改"
   git push origin feature/your-feature-name
   ```

4. 提交 Pull Request。
