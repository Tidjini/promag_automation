

from abc import ABC, abstractclassmethod

from .observable import WindowObservable


class Observer(ABC):
    '''Abstract class convetion for all observers'''
    @abstractclassmethod
    def notify(self, notifier: WindowObservable):
        pass


class RunningObserver(Observer):

    def notify(self, notifier: WindowObservable):

        if notifier.is_running:
            # continue proceeding or restart service
            pass
        else:
            # stop actions what doing
            pass
        print('{} Window {}'.format(notifier.name.upper(),
              'is running' if notifier.is_running else 'is not runing'))
