# def a(num):
#     if num<10:
#         return 10
#     else:
#         b(num)
# print(a(11))
# #栈：具有记忆功能的数据结构
# #a(num)
# #a(num)
# #a
import time
# import asyncio
#
# async def get_num(num):
#     print(f'{num}方法开始调用')
#     await time.sleep(1)
#     print(f'{num}方法停止调用')
#     pass
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     # tasks = [get_num(i) for i in range(4)]
#     tasks = get_num(1)
#     # print(tasks)
#     loop.run_until_complete(asyncio.wait(tasks))
#     # get_num(10)

class A():
    def __init__(self):
        self.a = 1000
        pass
B = type('B',(),{'a':1000})
print(eval('B().a'))
# a = A()
# print(a.__class__.__class__)