#/usr/bin/python
#encoding:utf-8
import csv
import os
import time


class Controller(object):
    def __init__(self, count):
        self.counter = count
        self.alldata = [("time", "cpuvalue")]

    #单次执行
    def testprocess(self):
        result = os.popen("adb shell dumpsys cpuinfo | findstr com.netease.my.gmc")
        line = result.readlines()
        cpuvalue = line[0].split("%")[0]
        #for line in result.readlines():
         #   print(line)
        #    cpuvalue =  line.split("%")[0]

        currenttime = self.getCurrentTime()
        self.alldata.append((currenttime, cpuvalue))

    #多次执行
    def run(self):
        while self.counter >0:
            self.testprocess()
            self.counter = self.counter - 1
            time.sleep(2)

    #执行时间
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    #数据存文件
    def SaveDataToCSV(self):
        csvfile = open(file='cpu.csv', mode='w')
        writer = csv.writer(csvfile)
        writer.writerows(self.alldata)
        csvfile.close()

if __name__ == "__main__":
    controller = Controller(5)
    controller.run()
    controller.SaveDataToCSV()
