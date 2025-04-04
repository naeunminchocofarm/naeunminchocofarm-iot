class Worker:
  def __init__(self):
    pass

  def start(self):
    raise NotImplementedError('start method of Worker is not implemented.')
  
  def loop(self):
    raise NotImplementedError('loop method of Worker is not implemented.')
  
  def exit(self):
    raise NotImplementedError('exit method of Worker is not implemented.')