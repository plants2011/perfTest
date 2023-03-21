#/usr/bin/python
#encoding:utf-8
import csv
import os
import time


class App(object):
    def __init__(self):
        self.content = ""
        self.startTime = 0

    #启动App
    def LaunchApp(self):
        cmd = 'adb shell am start -W -n com.netease.my.gmc/com.micro.cloud.game.ui.CloudGameActivity'
        self.content=os.popen(cmd)
        #com.netease.my.gmc/com.micro.cloud.game.ui.CloudGameActivity
        #com.netease.stzb.netease.yyx/com.netease.android.cloudgame.SplashActivity
        #com.netease.wdstzb.netease.gmc/com.micro.cloud.client.newest.CloudGameActivity

    #停止App
    def StopApp(self):
        #cmd = 'adb shell am force-stop com.netease.my.gmc'
        cmd = 'adb shell input keyevent 3'
        os.popen(cmd)

    #获取启动时间
    def GetLaunchedTime(self):
        for line in self.content.readlines():
            if "TotalTime" in line:
                self.startTime = line.split(":")[1]
                break
        return self.startTime


class Controller(object):
    def __init__(self, count):
        self.app = App()
        self.counter = count
        self.alldata = [("time", "elapsedtime")]

    #单次执行
    def testprocess(self):
        self.app.LaunchApp()
        time.sleep(10)
        elpasedtime = self.app.GetLaunchedTime()
        self.app.StopApp()
        time.sleep(3)
        currenttime = self.getCurrentTime()
        self.alldata.append((currenttime, elpasedtime))

    #多次执行
    def run(self):
        while self.counter >0:
            self.testprocess()
            self.counter = self.counter - 1

    #执行时间
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    #数据存文件
    def SaveDataToCSV(self):
        csvfile = open(file='startTime2.csv', mode='w')
        writer = csv.writer(csvfile)
        writer.writerows(self.alldata)
        csvfile.close()

if __name__ == "__main__":
    controller = Controller(3)

    controller.run()
    controller.SaveDataToCSV()