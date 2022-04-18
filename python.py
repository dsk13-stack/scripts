# Декораторы
def time_benchmark(function):
    """Декоратор для подсчета времени работы"""

    def inner(*args, **kwargs):
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        end_time = time.perf_counter()
        print("[*]Время выполнения функции {0} сек".format(end_time - start_time))
        return result
    return inner


def function_time_control(timeout=float):
    """Декоратор для контроля максимального времени выполнения"""

    def shutdown(function_name, timeout):
        print("Функция {1} выполняется дольше {0} сек".format(timeout, function_name))
        thread.interrupt_main()

    def outer(function):
        def inner(*args, **kwargs):
            timer = threading.Timer(timeout, function=shutdown, args=[function.__name__, timeout])
            timer.start()
            try:
                result = function(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer
