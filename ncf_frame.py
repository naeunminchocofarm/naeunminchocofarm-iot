class NcfFrame:
  def __init__(self, command, headers={}, body=""):
    self.command = command
    headers['content-length'] = len(body)
    if headers.get('content-type') is None:
      headers['content-type'] = 'text'
    self.headers = headers
    self.body = body

  def __str__(self):
    raw_header = "\n".join([f"{key}:{value}" for key, value in self.headers.items()])
    return "\n".join([self.command, raw_header, '', self.body])
  
  @staticmethod
  def parse(raw_frame = ""):
    lines = raw_frame.split("\n")
    command = lines[0].strip()
    index = 1
    headers = {}
    while index < len(lines):
      raw_header = lines[index].strip()
      index += 1
      if (raw_header == ""): 
        break
      [key, value] = raw_header.split(":")
      headers[key] = value
    body = ''    
    if (index < len(lines)):
      body = "\n".join(lines[index:]).strip()
    return NcfFrame(command, headers, body)
  
  @staticmethod
  def createSubscribe(destination):
    return NcfFrame('SUBSCRIBE', {'destination': destination}, '')
  
  @staticmethod
  def createUnsubscribe(destination):
    return NcfFrame('UNSUBSCRIBE', {'destination': destination}, '')
  
  @staticmethod
  def createSend(headers={}, body = ''):
    return NcfFrame('SEND', headers, body)