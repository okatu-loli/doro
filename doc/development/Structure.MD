# 项目目录结构及功能

```plain
doro/
├── build/               # 构建脚本和工具
├── doc/                 # 项目文档
│   └── development/     # 开发相关文档
├── resources/           # 资源文件（动画、配置、音频等）
│   ├── config/          # 配置文件
│   │   ├── config.json         # 主配置
│   │   ├── default_config.json # 默认配置
│   │   ├── file_index.json     # 文件索引
│   │   └── theme.json          # 主题配置
│   ├── doro/            # 动画资源
│   ├── icons/           # 图标资源
│   └── music/           # 音频资源
├── scripts/             # 辅助脚本(如格式化, 自动生成类型标注, 打包等)
├── src/                 # 源代码
│   ├── auto_typehint/   # 自动生成的类型标注
│   ├── MainLayer/       # 主逻辑中间层
│   ├── ResourceManager/ # 资源管理器
│   ├── state/           # 状态处理器
│   ├── utils/           # 工具模块
│   ├── config.py        # 配置管理模块
│   ├── pet_window.py    # 主窗口逻辑
│   ├── setting_gui.py   # 设置界面模块
│   ├── style_sheet.py   # 样式表生成模块
│   ├── system_monitor.py# 系统信息监控
│   └── system_tray.py   # 系统托盘相关
├── Test/                # 测试脚本，统一命名为 test_xxx.py
├── tools/               # 工具类脚本，如图片处理等
├── main.py              # 程序入口
├── requirements.txt     # Python 依赖
├── environment.yml      # conda环境配置
├── README.md            # 项目说明
├── LICENSE              # 许可证
├── logo.png             # 项目 logo
```

## 目录与命名

- **build/**：仅存放构建、打包相关脚本，产物输出到 dist/
- **dist/**：专门存放编译和打包后的可分发产物（如 Doro.exe），便于用户查找和分发
- **resources/**：资源细分为 config/（配置）、doro/（动画）、icons/（图标）、music/（音频）等，命名清晰
- **src/**：所有核心源代码
- **scripts/**：存放开发、部署、辅助等脚本，避免与 build/ 混淆
- **Test/**：所有测试脚本统一以 test\_ 开头，便于自动化测试
- **tools/**：存放与主业务无关的工具类脚本
