import time

if __name__ == '__main__':
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print(type(date))