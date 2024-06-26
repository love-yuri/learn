'''
Author: love-yuri yuri2078170658@gmail.com
Date: 2024-04-05 23:03:15
LastEditTime: 2024-05-22 19:43:55
Description: python工具
'''
import json
import os
import sys
import time
import threading
import pickle

mutex = threading.Lock()
write_in_file = False  # 是否写入文件


def log_result(msg, output=sys.stdout):
  print(msg, file=output)


def set_write_in_file():
  global write_in_file
  write_in_file = True


class Log:
  def __init__(self, line, is_error=False):
    self.ost = []
    if is_error and not write_in_file:
      self.ost.append("\x1b[31m")
    
    current_time = time.strftime("%H:%M:%S", time.localtime())
    self.ost.append(f"{current_time} line:{line} -> ")
  
  def __del__(self):
    mutex.acquire()
    try:
      if write_in_file:
        try:
          with open("log.txt", "a") as f:
            log_result("".join(self.ost), output=f)
        except Exception as e:
          print(e)
      else:
        self.ost.append("\x1b[0m")
        log_result("".join(self.ost))
    finally:
      mutex.release()
  
  def __lshift__(self, val):
    self.ost.append(str(val))
    return self


def info():
  return Log(sys._getframe().f_back.f_lineno)


def error():
  return Log(sys._getframe().f_back.f_lineno, is_error=True)


class Utils:
  '''
  description: 
  param {*} file 文件名
  return {*} 返回脚本目录
  '''
  
  @staticmethod
  def get_script_dir(file) -> str:
    return os.path.dirname(os.path.realpath(file))
  
  '''
  description: 
  param {callable} fun 待测试的函数
  param {array} args 函数所需的参数
  return {*} 返回执行所耗ms
  '''
  
  @staticmethod
  def action(fun: callable, *args, **kwargs) -> float:
    debug = kwargs.get("debug", True)  # 默认开启调试模式，可以通过debug=False来关闭调试模式。
    start = time.perf_counter_ns()
    fun(*args)
    end = time.perf_counter_ns()
    used = round((end - start) / 1000000, 2)
    if debug:
      info() << f"{fun.__name__} 执行耗时 {used} ms"
    return used
  
  @staticmethod
  def LoadConfig(fileName: str, ConfigClass):
    with open(fileName, 'r', encoding='utf-8') as file:
      return ConfigClass(**json.loads(file.read()))
  
  @staticmethod
  def SetConfig(fileName: str, ConfigClass):
    with open(fileName, 'w', encoding='utf-8') as file:
      file.write(json.dumps(ConfigClass.__dict__, indent=2))
