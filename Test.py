import yaml
import logging
import logging.config

#conastants
handler = {}

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
  with open('LoggerConfig.yaml', 'rt') as f:
      config = yaml.safe_load(f.read())
      logging.config.dictConfig(config)
      logger = logging.getLogger("gamepad")

      handler["Logger_console"] = config["handlers"]["Logger_console"]
      handler["Logger_file"] = config["handlers"]["Logger_file"]
      logger.addHandler[config["handlers"]]
      print(handler)
