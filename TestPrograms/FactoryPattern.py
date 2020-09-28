def Factory(topic):
  def innerListener(message):
    print("in listener")
    level = message.get("logLevel")
    if level:
        print(f"{topic}.{level}({message})")
    else:
        exec(f"{topic}.debug({message})")
  return innerListener


if __name__ == "__main__":
  #gamepad_listener = Factory("gamepad")
  #gamepad_listener(message = {"log=level": 'debug'})
  topics = "gamepad, command"
  topics = tuple(map(str, topics.split(',')))
  print(topics)
