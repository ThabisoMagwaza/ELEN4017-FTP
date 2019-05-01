def PORT(argument):
    return "PORT: " + argument


def STOR(argument):
    return "STOR: " + argument


def indirect(command, argument):
    switcher = {
        "STOR": STOR(argument),
        "PORT": PORT(argument),
    }
    func = switcher.get(command, 'Invalid')
    return func


print(indirect("PORT", " arg"))
print(indirect("QUIT", " arg"))
