# examples

该目录用于存放基于 botpy 开发的机器人的完整示例。

```
examples/
.
├── README.md
├── adddata.py
├── apytest.py
├── config.example.yaml          # 示例配置文件（需要修改为config.yaml）
├── demo_group_reply_text.py     # 机器人群内发消息相关示例
├── demo_group_reply_file.py     # 机器人群内发富媒体消息相关示例
├── getdata.py
├── main.py                      #机器人启动主函数
├── maint.py
├── showdata.py
```

## 环境安装

``` bash
pip install qq-botpy
```

## 使用方法

1. 拷贝 config.example.yaml 为 config.yaml ：

    ``` bash
    cp config.example.yaml config.yaml
    ```

2. 修改 config.yaml ，填入自己的 BotAppID 和  Bot secret 。
3. 运行机器人。例如：

    ``` bash
    python main.py
    ```
