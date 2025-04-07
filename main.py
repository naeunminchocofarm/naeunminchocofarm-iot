from application import Application
import time

app = Application()

try:
  app.run()
  while True:
      time.sleep(60)
except KeyboardInterrupt:
  print('server stop!')
except TypeError as err:
  print(err)
finally:
  app.exit()

print('==================== the end ====================')
