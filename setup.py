#! python3
# -*- coding:utf-8 -*-

import os
import platform
import subprocess
import sys

DIR_ROOT = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'src')
sys.path.append(DIR_ROOT)
PLATFORM = str(platform.system())

SUCCESS = 0
FAILED = 1
OUT_NOT = 0
OUT_RES = 1
OUT_STATUS = 2
OUT_RES_STATUS = 3
OUT_NOT_WAIT = 4
TITLE_SMALL = 1
TITLE_MIDDLE = 2
TITLE_BIG = 3
F_ADB = '../tools/PLATFORM/adb/'
F_AAPT = '../tools/PLATFORM/aapt/'
F_SQLITE3 = '../tools/PLATFORM/sqlite3/'
I_OS_WINDOWS = "Windows"
I_OS_LINUX = "Linux"
I_SUCCESS = "\t\t\t\t\t\t\t\t\t\t[成功]"
I_FAIL = "\t\t\t\t\t\t\t\t\t\t[失败]"


def to_str(lst: list, spe: str):
    if lst and spe:
        return spe.join(lst)


def remove_same(lst: list):
    if lst:
        return sorted(set(lst), key=lst.index)


def run_cmd(cmd, out_type: int, encode='gbk'):
    if out_type == OUT_NOT_WAIT:
        os.system(cmd)
    else:
        ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encode,
                             timeout=60)
        # print('res: ', ret)
        if out_type == OUT_RES:
            if ret.returncode == SUCCESS:
                print(ret.stdout)
            else:
                print(ret.stdout)
                print(ret.stderr)
        elif out_type == OUT_STATUS:
            if ret.returncode == SUCCESS:
                print(I_SUCCESS)
            else:
                print(I_FAIL)
        elif out_type == OUT_RES_STATUS:
            if ret.returncode == SUCCESS:
                print_result(True, ret.stdout)
            else:
                print_result(False, ret.stdout + '\n' + ret.stderr)
        return ret


def linux_install(en: str):
    if en.__eq__('adb'):
        run_cmd('sudo apt-get install android-tools-adb', out_type=OUT_NOT_WAIT)
        return True
    # elif en.__eq__('aapt'):
    #     run_cmd('sudo apt-get update', out_type=OUT_NOT_WAIT)
    #     run_cmd('sudo apt-get install gcc-multilib lib32z1 lib32stdc++6', out_type=OUT_NOT_WAIT)
    #     return True
    elif en.__eq__('sqlite3'):
        run_cmd('sudo apt-get install sqlite3', out_type=OUT_NOT_WAIT)
        return True
    else:
        return False


def add_system_env(env_key: str, env_value: str):
    # print('add_system_en:', env_value)
    success_code = SUCCESS
    if env_value:
        if I_OS_WINDOWS.__eq__(PLATFORM):
            path_list = os.environ['Path'].strip().split(';')
            path_list = remove_same(path_list)
            if not env_key:
                if not path_list.__contains__(env_value):
                    res = run_cmd('setx "Path" "%s;%s"' % (env_value, to_str(path_list, ';')), out_type=OUT_NOT)
                    success_code = res.returncode
            else:
                res = run_cmd(('setx "%s" "%s"' % (env_key, env_value)), out_type=OUT_NOT)
                cmd_str = r'^%' + env_key + r'^%";' + to_str(path_list, ';') + '"'
                res = run_cmd(('setx "Path" %s' % (cmd_str)), out_type=OUT_NOT)
                success_code = res.returncode
        elif I_OS_LINUX.__eq__(PLATFORM):
            bashrc_file = os.path.join(os.environ['HOME'], '.bashrc')
            if not env_key:
                if not os.environ['PATH'].__contains__(env_value):
                    with open(bashrc_file, encoding='ascii', mode='a') as f:
                        f.write('export PATH=%s:$PATH\n' % env_value)
                    f.close()
            else:
                if not os.environ.__contains__(env_key):
                    with open(bashrc_file, encoding='ascii', mode='a') as f:
                        f.write('export %s=%s\n' % (env_key, env_value))
                        f.write('export PATH=$%s:$PATH\n' % env_key)
                    f.close()
                else:
                    cmd_str = 'sed -i "s~^export %s=.*~export %s=%s~g" %s' % (env_key, env_key, env_value, bashrc_file)
                    res = run_cmd(cmd_str, out_type=OUT_NOT)
                    success_code = res.returncode
            run_cmd('source %s' % bashrc_file, out_type=OUT_NOT)
        return (success_code == SUCCESS)


def getEncode():
    if PLATFORM.__eq__(I_OS_WINDOWS):
        return "gbk"
    elif PLATFORM.__eq__(I_OS_LINUX):
        return "utf-8"


def check_env(env_name: str):
    res = None
    if 'java'.__eq__(env_name):
        res = run_cmd('java -version', OUT_NOT, getEncode())
    elif 'adb'.__eq__(env_name):
        res = run_cmd('adb version', OUT_NOT, getEncode())
    elif 'act'.__eq__(env_name):
        res = run_cmd('ac -v', OUT_NOT, getEncode())
    elif 'sqlite3'.__eq__(env_name):
        res = run_cmd('sqlite3 -version', OUT_NOT, getEncode())
    elif 'aapt'.__eq__(env_name):
        res = run_cmd('aapt v', OUT_NOT, getEncode())
    if res and res.returncode == SUCCESS:
        return True
    else:
        return False


def file_path(file_relative_path: str):
    if '/PLATFORM/' in file_relative_path:
        file_relative_path = file_relative_path.replace('PLATFORM', PLATFORM)
    return file_relative_path


def print_title(title: str, is_small_title=TITLE_SMALL):
    if title:
        result = ''
        if is_small_title == TITLE_SMALL:
            result = (3 * '-' + ' %s ' + 3 * '-') % title
        elif is_small_title == TITLE_MIDDLE:
            result = (10 * '-' + ' %s ' + 10 * '-') % title
        elif is_small_title == TITLE_BIG:
            result = (20 * '#' + ' %s ' + 20 * '#') % title
        print(result)


def print_result(is_success: bool, strings=None):
    if strings:
        print(strings)
    if is_success:
        print(I_SUCCESS)
    else:
        print(I_FAIL)


def setup():
    envir = ['act', 'java', 'adb', 'sqlite3', 'aapt']
    fail = 0
    for en in envir:
        # print title
        if en.__eq__('act'):
            print_title('检查%s (必须项)' % en)
        else:
            print_title('检查%s' % en)
        # check env
        res = check_env(en)
        # auto install
        if res:
            print_result(True, en + '已配置')
        else:
            is_success = False
            print('安装%s...' % en)
            if en.__eq__('act'):
                is_success = add_system_env('ACT', DIR_ROOT)
            elif en.__eq__('aapt'):
                is_success = add_system_env(None, os.path.join(DIR_ROOT, file_path(F_AAPT)))
            elif en.__eq__('sqlite3'):
                if I_OS_WINDOWS.__eq__(PLATFORM):
                    is_success = add_system_env(None, os.path.join(DIR_ROOT, file_path(F_SQLITE3)))
                elif I_OS_LINUX.__eq__(PLATFORM):
                    is_success = linux_install(en)
            elif en.__eq__('adb'):
                if I_OS_WINDOWS.__eq__(PLATFORM):
                    is_success = add_system_env(None, os.path.join(DIR_ROOT, file_path(F_ADB)))
                elif I_OS_LINUX.__eq__(PLATFORM):
                    is_success = linux_install(en)
            # res
            if is_success:
                print_result(True)
            else:
                print_result(False, '请手动安装并配置环境变量' + en + ' !')
                fail = fail + 1

    if fail > 0:
        print('\n以上安装出现失败项，请检查. \n非必须不影响ACT整体使用, 失败项可之后手动安装.')
    print('\n重启终端生效!')


if __name__ == '__main__':
    try:
        setup()
    except KeyboardInterrupt:
        pass