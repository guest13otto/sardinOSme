def Factory():
    def listener(self, message):
        if message == "True":
            print("True")
        else:
            print("False")
    return listener

function= Factory()

function(1, "True")
