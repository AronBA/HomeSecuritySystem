def getProjFile(projPath: str = ""):
    """
    Returns a path to the root project folder with the parameter appended to the end.
    for example:
    name of root folder is modul420
    it returns "C:\\...\\modul420\\" + the provided parameter
    :param projPath:
    :return:
    """
    path = __file__
    path = path.split("\\")
    temp = ""
    for i in range(0, len(path)-2):
        temp += path[i] + "\\"
    path = temp + projPath
    return path
