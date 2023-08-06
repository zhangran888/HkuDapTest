# author: zhangran
# createTime: 2023/5/11 16:10:03
# describe:
import asyncio
import time
from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium import webdriver


async def open_lab():
    print("并发打印")
    return 200


async def main():
    tasks = []
    success_count = 0
    total_time = 0
    start_time = time.perf_counter()
    print(f"开始时间统计到: {start_time:.2f} s")
    # 创建500个并发任务
    for i in range(500):
        task = asyncio.create_task(open_lab())
        tasks.append(task)

    # # 等待所有任务完成后获取结果
    # for coro in asyncio.as_completed(tasks):
    #     result = await coro  # 注意这里是await
    #     success_count += 1
    #     total_time += time.time() - start_time
    #     print(result)
    # tps = len(tasks) / total_time
    # qps = success_count / total_time
    # print(f"总耗时: {total_time:.2f} s")
    # print(f"总请求: {len(tasks)}")
    # print(f"成功请求: {success_count}")
    # print(f"TPS: {tps:.2f}")
    # print(f"QPS: {qps:.2f}")
    # 记录每个任务的执行结果和耗时
    results = []
    durations = []
    for task in tasks:
        start_timestamp = time.perf_counter()
        result = await task
        end_timestamp = time.perf_counter()
        results.append(result)
        durations.append(end_timestamp - start_timestamp)
    # 输出每个任务的执行结果和耗时
    for i, (result, duration) in enumerate(zip(results, durations)):
        print(f"Task {i}: Result {result}, Duration {duration:.2f}s")
    # 统计总耗时和其他信息
    success_count = sum(1 for result in results if result == 200)
    total_time = time.perf_counter() - start_time
    tps = len(tasks) / total_time if total_time > 0 else 0
    print(f"总耗时: {total_time:.2f} s")
    print(f"总请求: {len(tasks)}")
    print(f"成功请求: {success_count}")
    print(f"TPS: {tps:.2f}")


def hello():
    print("hello")


# 不适用，废弃
# def taskThread():
#     executor = ThreadPoolExecutor(max_workers=10)  # 声明一个最多包含500个线程的线程池
#     future_tasks = []
#
#     for i in range(10):
#         future = executor.submit(hello)
#         future_tasks.append(future)
#
#     for future in as_completed(future_tasks):
#         try:
#             data = future.result()  # 获取线程执行结果
#             print(data)
#         except Exception as exc:
#             print(f'发生异常：{exc}')


def openUrl():
    chromepath = r"D:\\chromedriver_32_113\\chromedriver.exe"
    options = Options()
    # options.headless = True

    driver = webdriver.Chrome(options=options, executable_path=chromepath)

    driver.get("http://47.96.2.99/dap-client/#/myLabs")

    console_logs = driver.execute_script('return console.error')
    print_logs = driver.get_log('browser')

    # 遍历所有的日志项并保存到列表中
    all_logs = []
    for log in print_logs:
        if log['level'] in ['INFO', 'WARNING', 'SEVERE']:
            all_logs.append(log['message'])
    # 输出控制台日志信息
    if len(all_logs) > 0:
        print('控制台日志信息：')
        for log in all_logs:
            print(log)
    else:
        print('没有控制台日志信息。')

    # print(print_logs)
    if console_logs:
        print('控制台上有{}个错误：'.format(len(console_logs)))
        for log in console_logs:
            print(log)
    else:
        print('控制台上没有错误信息。')

    # 输出页面标题和 URL
    print(f'Title: {driver.title}')
    print(f'URL: {driver.current_url}')

    time.sleep(600)


def tsf():
    for i in range(10):
        print(f"student{i + 1}")


def atestSign():
    try:
        import base64
        import hmac
        from hashlib import sha256
        # 密钥key
        SecretKeySpec = "5921ba25ad974899bf8f2b48ef1cb77c"
        # 密钥ID
        SecretIdSpec = "9936520aaa4745caa59c7cf61aeb4511"
        sign = base64.b64encode(
            hmac.new(SecretKeySpec.encode("utf-8"), SecretIdSpec.encode("utf-8"), digestmod=sha256).digest()).decode()
        print(sign)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # tsf()
    # openUrl()
    # asyncio.run(main())
    # taskThread()
    # hello()
    # starttime = time.time()
    # time.sleep(10)
    # time = time.time()
    # ss = time-starttime
    # print(f"开始时间统计到:{ss:.2f} " )
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"持续结束时间: {datetime.now()} ")
    output_text = '11111'
    print(f"代码未完成或发生错误 ({current_time}): {output_text}")
    # atestSign()
