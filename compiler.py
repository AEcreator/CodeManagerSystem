# -*- coding: gbk �C*-
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
                # ִ�б�������
                result = subprocess.run(['g++', path + '.cpp', '-o', path], capture_output=True, text=True, timeout=5)
                # ��ȡ���������
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
            # print(f"����ִ�г�ʱ��{timeout}")
            return 'Time Limited Exceed'
        except subprocess.CalledProcessError as e:
            print(f"����ִ��ʧ�ܣ�{e}")

        if temp('judge') == 'CE':
            return 'Compile Error'

    except OSError as e:
        return f'Compile Error:{e}'

    except Exception as e:
        return f'Unknown Error:{e}'

    try:
        # ִ���ⲿ������������
        # result = subprocess.run(["./your_cpp_program"], capture_output=True, text=True,
        # input="your_input_data", timeout=5)
        result = subprocess.run(["judge"], capture_output=True, text=True, timeout=5)

        # ��ȡ������
        output = result.stdout  # ��ȡ��׼���
        error = result.stderr  # ��ȡ��׼����

        if output:
            return output  # ����б�׼�������Ϊ����������
        elif error:
            return error  # ����д����������Ϊ����������
        else:
            return "No output or error"  # ���û�������������Ӧ��Ϣ
    except subprocess.TimeoutExpired as e:
        return f"Timeout: {e}"
    except OSError as e:
        return f'Compile Error:{e}'
    except Exception as e:
        return f"Error: {e}"

