from application import Application

app = Application()

try:
  app.run()
except KeyboardInterrupt:
  print('server stop!')
except TypeError as err:
  print(err)
except:
  app.rerun()
finally:
  app.exit()

print('==================== the end ====================')