from application import Application

try:
  app = Application()
  app.run()
except TypeError as err:
  print(err)
except:
  app.rerun()
finally:
  app.exit()

print('==================== the end ====================')