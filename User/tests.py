import threading

def hi():
    print('yes')

t = threading.Timer(10,hi)
t.start()
print('yes')