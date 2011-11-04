import unittest
import time
from threading import Timer

from showbox.webcast.scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.executed = 0
        
    def mockFunc(self):
        self.executed += 1
        
    def testPeriodicalExecution(self):
        sched = Scheduler(self.mockFunc, period=0.1)
        sched.start()
        time.sleep(0.15)
        self.assertEqual(1, self.executed)
        time.sleep(0.2)
        self.assertEqual(3, self.executed)
        sched.stop()
        
    def testStop(self):
        sched = Scheduler(self.mockFunc, period=0.1)
        sched.start()
        sched.stop()
        time.sleep(0.15)
        self.assertEqual(0, self.executed)
        