import abc
from datetime import datetime

class ITimer(abc.ABC):

    @abc.abstractmethod
    def now(self):
        pass

class FakeTimer(ITimer):

    def __init__(self):
        self.current_time = datetime(1923, 8, 29)

    def now(self):
        return self.current_time

    def update(self, time:datetime):
        self.current_time = time

class RealTimer(ITimer):

    def now(self):
        return datetime.now()
