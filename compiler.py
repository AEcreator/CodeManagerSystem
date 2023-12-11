# -*- coding: gbk –*-
# !/usr/bin/python

import os
import subprocess


def run(id):
    try:
        f = open('output_test', 'w')
        f.seek(0)
        f.truncate()
        f.close()
        file1 = open("JudgeSystemA/output_std_"+id, "r")
        file2 = open("JudgeSystemA/output_std", "w")
        s = file1.read()
        w = file2.write(s)

        file1.close()
        file2.close()
        """
        os.system("g++ test.cpp -o test")
        # os.system("Standard < input > output_Standard")
        os.system("test < JudgeSystemA/input_1 > output_test")
        os.system("g++ judge.cpp -o judge")
        # os.system("judge")
        """
        def temp(path):
            try:
                # 执行编译命令
                result = subprocess.run(['g++', path + '.cpp', '-o', path], capture_output=True, text=True, timeout=5)
                # 获取编译结果输出
                output = result.stdout
                error = result.stderr

                if output:
                    return 'AC'
                if error:
                    return 'CE'
            except Exception as e:
                return 'CE'
        if temp('test') == 'CE':
            return 'Compile Error'
        # os.system(f"test < JudgeSystemA/input_{id} > output_test")

        try:
            command = f"test < JudgeSystemA/input_{id} > output_test"
            subprocess.run(command, shell=True, timeout=2)
        except subprocess.TimeoutExpired as timeout:
            # print(f"命令执行超时：{timeout}")
            return 'Time Limited Exceed'
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败：{e}")

        if temp('judge') == 'CE':
            return 'Compile Error'

    except OSError as e:
        return f'Compile Error:{e}'

    except Exception as e:
        return f'Unknown Error:{e}'

    try:
        # 执行外部命令，捕获其输出
        # result = subprocess.run(["./your_cpp_program"], capture_output=True, text=True,
        # input="your_input_data", timeout=5)
        result = subprocess.run(["judge"], capture_output=True, text=True, timeout=5)

        # 获取评测结果
        output = result.stdout  # 获取标准输出
        error = result.stderr  # 获取标准错误

        if output:
            return output  # 如果有标准输出，作为评测结果返回
        elif error:
            return error  # 如果有错误输出，作为评测结果返回
        else:
            return "No output or error"  # 如果没有输出，返回相应消息
    except subprocess.TimeoutExpired as e:
        return f"Timeout: {e}"
    except OSError as e:
        return f'Compile Error:{e}'
    except Exception as e:
        return f"Error: {e}"

