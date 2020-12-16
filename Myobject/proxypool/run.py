from Myobject.proxypool.api import app
from Myobject.proxypool.Scheduler import Scheduler
def main():
    s = Scheduler()
    s.run()
    app.run()

if __name__ == '__main__':
    main()