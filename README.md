# Doro   #桌面宠物
![Logo](./logo.png)
# 感谢支持与喜爱！( ˘ ³˘)♥

## 公益项目 | 感谢大家的支持

作者碎碎念：  
随便写的一个小demo没想到有这么多人喜欢，感谢大家的支持与喜爱。😊  
**欢迎大家一起开发合作，让更多人喜欢 doro！**  
谁不向往单纯的爱情呢？现实与理想，**doro**承载了对理想与纯真的寄托！💖

## Installation   # #安装

1. Clone the repository:   1. 克隆此仓库：
   ```bash   ”“bash
   git clone https://github.com/yourusername/desktop-pet.git使用以下命令克隆仓库：

```
git clone https://github.com/yourusername/desktop-pet.git
```
   cd desktop-pet
   ```   ' ' '

2. Install the required dependencies:2. 安装所需的依赖项：2. 安装所需的依赖项：
   ```bash   ”“bash
   pip install -r requirements.txt运行 `pip install -r requirements.txt` 安装依赖包。
   ```   ' ' '

3. Create a `.env` file in the project root with your DeepSeek API key:3. 在项目根目录中创建一个 `.env` 文件，并放入您的 DeepSeek API 密钥：
   ```bash   ”“bash
   cp .env.example .env
   # Edit .env and add your DeepSeek API key编辑.env文件并添加您的 DeepSeek API 密钥
   ```   ' ' '

## Usage   # #使用

Run the program:   运行程序：
```bash   ”“bash   ”“bash
python main.py
```

## Configuration   # #配置

You can customize the following settings in the `.env` file:您可以在 `.env` 文件中自定义以下设置：

- `DEEPSEEK_API_KEY`: Your DeepSeek API key- `DEEPSEEK_API_KEY`：您的 DeepSeek API 密钥
- `ANIMATION_FPS`: Animation frame rate (default: 30)- `ANIMATION_FPS`：动画帧率（默认值：30）
- `WINDOW_WIDTH`: Pet window width (default: 300)- `WINDOW_WIDTH`：宠物窗口宽度（默认值：300）
- `WINDOW_HEIGHT`: Pet window height (default: 300)- `WINDOW_HEIGHT`：宠物窗口高度（默认值：300）
- `CURRENT_THEME`: Theme color (default: "粉色主题")

## Development   # #发展

The project structure:   项目结构：
```
desktop-pet/
├── src/
│   ├── config.py      # Configuration management
│   ├── deepseek_client.py  # DeepSeek API client
│   ├── pet_window.py  # Main window and UI│   ├── pet_window.py  # 主窗口和用户界面
│   ├── system_monitor.py  # System monitoring│   ├── system_monitor.py  # 系统监控
│   └── system_tray.py  # System tray integration│   └── system_tray.py  # 系统托盘集成
├── main.py           # Entry point├── main.py           # 入口点
├── requirements.txt  # Dependencies├── requirements.txt  # 依赖项
├── .env.example     # Example configuration├── .env.example     # 配置示例
└── README.md        # Documentation
```



## License   # #许可证

MIT License 
