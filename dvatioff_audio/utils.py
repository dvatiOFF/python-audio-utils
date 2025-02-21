from functools import wraps
import time


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
