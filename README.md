# Android Tools

#### 介绍

Android Tools 集成了常用的adb指令和gui工具, 实现快捷调用,  提高效率.
开发者可定制化资源文件, 支持windows和linux系统

------------


#### Windows安装说明
1. 下载AnroidTools的源码

   git clone git@github.com:Ghitbug/AnroidTools.git


2. 如果系统有python3环境, 略过此步骤. 否则安装python3.9, 参考:
   https://blog.csdn.net/zh452647457/article/details/110296025

3. 进入AnroidTools/目录, 在终端当前路径执行: python setup.py
4. 第3步执行完后，需要关闭当前终端, 重开个终端(环境生效). 执行ac -v，能输出版本信息则安装成功

------------
#### Linux安装说明
##### 一. 下载AnroidTools源码
   `git clone git@github.com:Ghitbug/AnroidTools.git`
##### 二. 安装python3.9
   若已安装，略过此步骤. 下载python3.9源码, 并安装


    wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
    sudo tar -zxvf Python-3.9.0.tgz
    sudo apt-get install libffi-dev
    cd Python-3.9.0
    ./configure --prefix=/opt/python3.9 --enable-shared 
    make
    sudo make install
    sudo ln -s /opt/python3.9/bin/python3.9 /usr/bin/python3.9
    python3.9 -V
    rm Python-3.9.0.tgz
    rm -rf Python-3.9.0/
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 100
    #系统python版本切换: sudo update-alternatives --config python 

##### 三. 配置ACT环境变量
  执行以下面命令, 完成后重启终端，环境生效:
  
    cd AnroidTools/
    python3.9 setup.py
##### 四. 验证安装成功
   能正常打印版本信息, 则安装成功
   `ac -v`

------------


#### 使用说明

 `ac -h`

------------


#### 软件界面

![输入图片说明](https://gitee.com/dyldmy/AnroidCommonTool/raw/master/res/ac.PNG "在这里输入图片标题")
