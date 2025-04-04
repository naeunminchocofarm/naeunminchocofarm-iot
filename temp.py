class AAA:
  def __init__(self, name):
    self.name = name

  def start(self):
    raise NotImplementedError('worker의 start 함수가 구현되지 않았습니다.')

class BBB(AAA):
  def __init__(self, name):
    super().__init__(name)
  
  def start(self):
    print('hello, my name is', self.name);


bbb = BBB('bbb')
bbb.start()