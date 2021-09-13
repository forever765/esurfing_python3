# esurfing_python3
  广东天翼校园客户端替代品，支持广东财经大学华商学院校园网认证，项目代码基于【[GDCTSCP](https://github.com/mynuolr/GDCTSCP)】使用Python3.8重写，并作如下优化：
  1. 使用Python3重写
  2. 标准化部分函数名
  3. 增加生成随机mac地址
  4. 增加自动获取本机IP地址
  5. 使用requests替代urllib2
  6. 优化认证流程，修改不合理死循环，整合无用函数，增强异常处理

**特别声明：本脚本仅供研究学习使用，遵循GPL开源协议，严禁任何商业使用。**  
· 2020-10-29，电信禁止了web门户认证，强制要求使用天翼校园客户端登录。但天翼校园win客户端无法识别本人笔记本的无线网络状态，无奈只能自力更生  
· 感谢前人@NipGeihou提供的认证和保活算法  
· 如有Openwrt路由器自动认证需求，请移步至[lua_esurfing](https://github.com/NipGeihou/lua_esurfing)

# 可用学校列表
广东财经大学华商学院（测试通过）

广东工业大学华立学院（理论上支持）

# 运行截图
![image](https://github.com/forever765/esurfing_python3/blob/main/running.png)

# 关于心跳发送间隔
以下为广东财经大学华商学院认证心跳大概的时间间隔，其他学校请自行测试，修改time.sleep时间即可，单位为s  
~~有线：120s左右~~
~~WiFi：1h左右~~

实测目前服务器并未要求客户端提供心跳，脚本认证成功后之后退出即可

# 环境依赖
1、Python3.8

2、python requests模块

* Python安装第三方库的方法：
    使用pip命令进行安装，以安装requests库为例：

pip install requests

# 运行方法
  请确保环境依赖已经安装完毕  
  修改esurfing_python3.py第157、158行的账号密码并保存  
  python esurfing_python3.py
  
# 已知问题
  某些情况下（如获取ip失败，连接认证服务器超时等）的异常处理失效导致抛出一大堆异常。~~你问我为啥不修？又不是不能用。。。~~

# 扩展知识
  安卓可安装Tremux终端，在里面安装python后执行此脚本，让手机认证校园网。
  苹果iOS也有类似软件，实测可行，需自行动手折腾

# 开源协议
AGPL V3：禁止任何个人或者公司将本代码投入商业使用，由此造成的后果和法律责任均与本人无关。
