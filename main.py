from application import Application
import time

app = Application()

try:
  app.run()
  while True:
    time.sleep(1)
    print('1s')
except KeyboardInterrupt:
  print('server stop!')
except TypeError as err:
  print(err)
except:
  app.rerun()
finally:
  app.exit()

print('==================== the end ====================')