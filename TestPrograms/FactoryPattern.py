class Factory:

    def Factory(self):
        def listener(message):
            if message == "True":
                print("True")
                self.message = message
            else:
                print("False")
        return listener

    def function(self):
        function = self.Factory()
        function("True")


if __name__ == "__main__":
    Factory = Factory()
    Factory.function()
