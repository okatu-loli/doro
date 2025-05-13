# 项目目录结构及功能

```plain
doro/
├── build/               # 构建脚本和工具
│   └── generate_typehints.py  # 自动生成类型提示的脚本
│   ├── format_files.py  # 格式化文件的脚本
│   ├── build_all.py  # 运行所有构建脚本的脚本
├── doc/                 # 项目文档
│   ├── development/     # 开发相关文档
│   │   ├── Development.MD  # 开发文档
│   │   └── Structure.MD    # 目录结构说明
├── resources/           # 资源文件（动画、配置等）
│   ├── config/          # 配置文件
│   │   ├── default_config.json  # 默认配置
│   │   ├── file_index.json      # 文件索引
│   │   └── theme.json           # 主题配置
│   ├── doro/            # 动画资源
│   └── music/           # 音频资源
├── src/                 # 源代码
│   ├── auto_typehint/   # 自动生成的类型提示
│   │   ├── ConfigHint.py       # 配置类型提示
│   │   ├── FileIndexHint.py    # 文件索引类型提示
│   │   ├── ThemeHint.py        # 主题类型提示
│   │   └── __init__.py         # 类型提示包的初始化
│   ├── state/           # 状态处理器
│   │   ├── base_state.py       # 状态处理器基类
│   │   ├── normal_state_handler.py  # 正常状态处理器
│   │   ├── hungry_state_handler.py  # 饥饿状态处理器
│   │   ├── moving_state_handler.py  # 移动状态处理器
│   │   ├── dragging_state_handler.py  # 拖拽状态处理器
│   │   ├── eating_state_handler.py    # 进食状态处理器
│   │   ├── clicked_state_handler.py   # 点击状态处理器
│   │   └── __init__.py         # 状态处理器包的初始化
│   ├── config.py        # 配置管理模块
│   ├── pet_window.py    # 主窗口逻辑
│   ├── style_sheet.py   # 样式表生成模块
│   └── setting_gui.py   # 设置界面模块
└── main.py              # 程序入口
```

## 功能说明

- **build/**: 包含构建工具和脚本，用于生成类型提示等辅助功能。
- **doc/**: 项目文档，包括开发文档和目录结构说明。
- **resources/**: 存放项目所需的资源文件，如动画、配置和音频。
- **src/**: 项目的核心代码，包括状态处理器、配置管理、主窗口逻辑和样式表生成等。
- **main.py**: 项目的入口文件，用于启动应用程序。
