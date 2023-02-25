from concurrent.futures import ThreadPoolExecutor
from pprint import pprint



def thread_function(x):
    """Test Function
    Args:
        x (int): test value
    """
    print(x)


def multiprocess(thread_function, task_list, max_workers=10):
    """multiprocessing
    Args:
        f (_type_): function
        task_list (list): tasks
        max_workers (int): max number of workers. Defaults to 10.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return executor.map(thread_function, task_list)


if __name__ == '__main__':
    result = multiprocess(thread_function, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
    pprint(list(result))