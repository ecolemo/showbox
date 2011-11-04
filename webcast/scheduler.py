from threading import Timer

class Scheduler(object):
    
    def __init__(self, func, period):
        self.func = func
        self.period = period
        self.timer = None
        
    def start(self):
        if self.timer: self.timer.cancel()
        self.timer = Timer(self.period, self.run)
        self.timer.start()
    
    def stop(self):
        if self.timer: self.timer.cancel()
        self.timer = None
        
    def run(self):
        if not self.timer: return

        self.func()
        self.start()
        
