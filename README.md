# SYSU自动健康申报

> + 测试环境：Ubuntu 18.04
> + python版本：python 3.6
> + 特别提醒：由于涉及到netid等敏感信息，工具只能在自己的环境中使用，切勿假手于人。
> + 免责声明：本工具仅供学习和交流，禁止用于任何商业用途和任何诸如ddos攻击等违法行为。本工具今后造成的纠纷和一切后果，均由工具使用者承担，与本作者无关。

## 换源

首先将下载源更换成[阿里源](https://developer.aliyun.com/mirror/ubuntu)。

```shell
sudo gedit /etc/apt/sources.list
```

将里面的内容替换成Ubuntu 18.04的阿里镜像源。

```
deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse
```

更新下载源。

```shell
sudo apt update
```

## 配置环境

下载`pip3`。

```shell
sudo apt install python3-pip -y
```

更新`pip3`，否则后面安装`opencv`时会卡住。

```shell
pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
```

安装`opencv`。

```shell
sudo apt install cmake -y
sudo apt install libopencv-dev -y
pip3 install scikit-build -i https://mirrors.aliyun.com/pypi/simple/
pip3 install opencv-python -i https://mirrors.aliyun.com/pypi/simple/
```

安装`muggle_ocr`，`muggle_ocr`用作验证码识别。

```shell
pip3 install muggle_ocr -i https://mirrors.aliyun.com/pypi/simple/
```

安装`selenium`，`selenium`用来访问健康申报的网站。

```shell
pip3 install selenium -i https://mirrors.aliyun.com/pypi/simple/
```

安装`firefox`。

```shell
sudo apt install firefox
```

下载源码。

```shell
sudo apt install git -y
git clone https://github.com/NelsonCheung688585/SYSU_jksb.git jksb
```

进入`jksb`文件夹。

```shell
cd jksb
```

下载`firefox`驱动，`selenium`将使用其来访问网站。

```shell
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
tar -xvf geckodriver-v0.30.0-linux64.tar.gz
```

## 使用

在源码文件夹下，首先将`geckodriver`加入到环境变量。

```shell
export PATH=.:$PATH
```

启动，在命令行参数下加入`netid`，`passwd`，`hour`，`minute`。

```shell
python3 sysu.py --netid=zhangjy297 --passwd=ilovesysu --hour=07 --minute=00
```

+ `--netid`表示netid。
+ `--passwd`表示密码。
+ `--hour`和`--minute`表示每天提交申报的时间，上面的例子是`07:00`提交申报。

注意，密码中若含有特殊字符需要加上`\`。例如，

```
-passwd=ilovesysu!!!
```

应该输入

```
-passwd=ilovesysu\!\!\!
```

后面就可以看到如下信息。

<img src="gallery/1.PNG" alt="1" style="zoom:50%;" />

对工具实现感兴趣的可以在[reference_guide.md](reference_guide.md)中找到实现方法。

