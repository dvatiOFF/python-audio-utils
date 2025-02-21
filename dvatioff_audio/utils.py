from functools import wraps
import time
import json
import re
import webbrowser


def retry(exceptions, tries=5, delay=1):
    """
    重试装饰器，当函数抛出指定的异常时，自动重试。
    :param exceptions: 触发重试的异常类型
    :param tries: 最大重试次数
    :param delay: 初始延迟时间
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"警告：{func.__name__} - {e}, 正在重试...")
                    time.sleep(mdelay)
                    mtries -= 1
            return func(*args, **kwargs)

        return wrapper

    return decorator


def load_dict_from_json_file(file_path):
    """
    从 json 文件中加载数据
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def save_dict_to_json_file(file_path, data):
    """
    将数据保存到 json 文件中
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def is_random(name):
    """
    是否是随机类声音
    """
    tail = name.split("_")[-1]
    pattern = r"0[1-9]$"
    return bool(re.match(pattern, tail))


def is_loop(name):
    """
    是否是 Loop 类声音
    """
    tail = name.split("_")[-1]
    pattern1 = r"Loop$"
    pattern2 = r"Lp$"
    return bool(re.match(pattern1, tail) or re.match(pattern2, tail))


def is_voice(name):
    """
    是否是 Voice 类声音
    """
    head = name.split("_")[0]
    pattern = r"VO$"
    return bool(re.fullmatch(pattern, head))


def is_death(name):
    """
    是否是死亡类声音
    """
    tail = name.split("_")[-1]
    pattern = r"Death$"
    return bool(re.match(pattern, tail))


def open_url(url):
    """
    打开指定的 URL
    """
    webbrowser.open(url)