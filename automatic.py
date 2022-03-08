import json
import tkinter as tk  # 使用Tkinter前需要先导入
import webbrowser

import pyautogui
import time
import pyperclip
import platform
import os
import asyncio
import websockets


# pyautogui库其他用法 https://blog.csdn.net/qingfengxd1/article/details/108270159

async def mouseClick(clickTimes, lOrR, img, reTry):
    '''设置屏幕分辨率'''
    print('00000000')
    screenwidth, screenheight = pyautogui.size()
    im1 = pyautogui.screenshot()
    dpi = im1.size[0] / screenwidth
    await sendMsg('分辨率'+str(dpi))
    if reTry == 1:
        while True:
            try:
                location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            except IOError:
                await sendMsg("未找到相应图片")
            if location is not None:
                await sendMsg(pyautogui.position())
                pyautogui.click(location.x / dpi, location.y / dpi, clicks=clickTimes, interval=0.2, duration=0.2,
                                button=lOrR)
                break
            await sendMsg("未找到匹配图片,0.1秒后重试")
            time.sleep(0.1)
    elif reTry == -1:
        while True:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
            time.sleep(0.1)
    elif reTry > 1:
        i = 1
        while i < reTry + 1:
            location = pyautogui.locateCenterOnScreen(img, confidence=0.9)
            if location is not None:
                pyautogui.click(location.x, location.y, clicks=clickTimes, interval=0.2, duration=0.2, button=lOrR)
                await sendMsg("重复")
                i += 1
            time.sleep(0.1)


# 任务
async def mainWork(arr):
    for arrmsg in arr:
        print(arrmsg)
        await sendMsg("匹配中")
        time.sleep(0.5)
        if arrmsg["name"] == '1' or arrmsg["name"] == 1:
            # 取图片名称
            img = arrmsg["value"]
            reTry = 1

            await mouseClick(1, "left", img, reTry)

        # 2代表双击左键
        elif arrmsg["name"] == '2' or arrmsg["name"] == 2:
            # 取图片名称
            img = arrmsg["value"]

            mouseClick(2, "left", img, 1)
            await sendMsg("双击左键")
        # 3代表右键
        elif arrmsg["name"] == '3' or arrmsg["name"] == 3:
            # 取图片名称
            img = arrmsg["value"]
            # 取重试次数
            reTry = 1
            mouseClick(1, "right", img, reTry)
            await sendMsg("右键")
            # 4代表输入
        elif arrmsg["name"] == '4' or arrmsg["name"] == 4:
            await sendMsg("执行输入")
            inputValue = arrmsg["value"]
            pyperclip.copy(inputValue)
            '''系统类型'''
            if platform.system() == 'Windows':
                sys = 'Windows';
            else:
                sys = "Other";
            if sys == 'Windows':
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.1)
            else:
                pyautogui.hotkey('command', 'v')
                time.sleep(0.1)
            time.sleep(0.5)
            await sendMsg("输入")
            # 5代表等待
        elif arrmsg["name"] == '5' or arrmsg["name"] == 5:
            # 取图片名称
            waitTime = arrmsg["value"]
            time.sleep(int(waitTime))
            await sendMsg("等待....")
        # 6代表滚轮
        elif arrmsg["name"] == '6' or arrmsg["name"] == 7:
            # 取图片名称
            scroll = arrmsg["value"]
            pyautogui.scroll(int(scroll))
            await sendMsg("滚轮滑动")
        # 7代表回车
        elif arrmsg["name"] == '7':
            pyautogui.press('enter')

        await sendMsg("执行完毕！")


# 读取配置文件
def readfile():
    with open(os.getcwd() + '/config.json', 'r') as f:
        content = f.read()
        jsonMsg = json.loads(content)
        return jsonMsg


# 存储配置文件
def savefile(msg):
    d = json.dumps(msg)
    with open(os.getcwd() + '/config.json', 'w', ) as w:
        w.write(d)


# 展示配置文件
def showConfig():
    mm = ""
    mm = mm + '\n----------已存在指令------------\n'
    arr = readfile()["value"]
    for x in arr:
        mm = mm + ('|命令:' + str(x["name"]) + '--------执行:' + str(x["value"]) + '|\n')
    mm = mm + '------------------------------\n'
    print(mm)
    return mm


async def saveUtil(obj):
    configJSON = readfile()
    arr = configJSON["value"]
    arr.append(obj)
    configJSON["value"] = arr
    savefile(configJSON)
    await sendMsg("指令添加成功！")
    await showConfigTwo()


async def showConfigTwo():
    await sendMsg(showConfig() + '\n')


async def deleteUtil():
    configJSON = readfile()
    configJSON["value"] = []
    savefile(configJSON)
    await showConfigTwo()


def addMsg():
    theObj = {}
    conName = input('鼠标键盘指令（1 单击  2 双击  3 右键  4 输入  5 等待  6 滚轮  7 回车  8 空格） \n')
    theObj["name"] = conName
    conValue = input('执行类型（单击：图片地址  输入：内容  等待：时长  滚轮：像素-《整数》往上滚动《负数》往下滚动） \n')
    theObj["value"] = conValue
    # saveUtil(theObj)


def textMeth(msg):
    global text
    msg = msg + '\n'
    text.insert(tk.END, msg)


async def sendMsg(msg):
    await names.send(f"{msg}"+'\n')


def win1():
    win1 = tk.Tk()
    # 给主窗口起一个名字，也就是窗口的名字
    win1.title('自动化工具')
    win1.geometry('500x500')
    win1["background"] = '#ffffff'
    tk.Label(win1, bg='white', text='欢迎使用automatic自动化工具', pady=30).pack()
    # 创建输入框控件
    win1.mainloop()


def message_back(msg):
    print(msg)


async def hello(websocket, path):
    await websocket.send('主程序已启动\n')
    await websocket.send('欢迎使用自动化工具\n')
    await websocket.send(showConfig() + '\n')

    RUNKEY = 'runkey'
    ADDKEY = 'addkey'
    DELETEKEY = 'deletekey'
    RUNWHILEKEY = 'runwhilekey'

    while True:
        global names

        name = await websocket.recv()
        name = json.loads(name)
        print(name)
        # greeting = f"Hello {name}!"
        # await websocket.send(greeting)
        names = websocket
        if name['name'] == RUNKEY:
            await mainWork(readfile()["value"])
            configJSON = readfile()
            arr = configJSON["value"]
            if len(arr)<1:
                await sendMsg('暂无指令可以执行')
        elif name['name'] == RUNWHILEKEY:
            configJSON = readfile()
            arr = configJSON["value"]
            if len(arr)<1:
                await sendMsg('暂无指令可以执行')
                return
            while True:
                await mainWork(readfile()["value"])
                time.sleep(0.1)
                print("等待0.1秒")
        elif name['name'] == ADDKEY:
            await saveUtil(name['value'])
        elif name['name'] == DELETEKEY:
            await deleteUtil()
            await sendMsg('已删除指令')


if __name__ == '__main__':

    webbrowser.open_new_tab(os.getcwd() + '/index.html')
    names = ""

    start_server = websockets.serve(hello, 'localhost', 6688)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

