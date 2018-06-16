import multiprocessing
import time

from fitoemanews import main


class EmaNewsProcess(multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        super(EmaNewsProcess, self).__init__(*args, **kwargs)
        self.exit = multiprocessing.Event()

    def run(self):
        while not self.exit.is_set():
            pass

    def shutdown(self):
        self.exit.set()


def test_startup():
    process = EmaNewsProcess(target=main, args=(True,))
    process.start()
    time.sleep(5)
    assert process.is_alive()
    process.shutdown()
