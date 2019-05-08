import time
from controller import PS4Controller
from concurrent.futures import ProcessPoolExecutor

def main():
    with ProcessPoolExecutor() as ex:
        f1 = ex.submit(bar, 'one')
        f2 = ex.submit(foo, 'two')
        print(f2.result())
        print(f1.result())

def bar(e):
    i = 0
    while 1:
        i += 1
        yield i

def foo(e):
    return e

if __name__ == '__main__':
    js = PS4Controller()
    js.init()

    main()
