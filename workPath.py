from sys import argv
def reWorkPath() -> str:
    tempPath = argv[0]
    if '\\' in tempPath:
        tempPath = tempPath.replace(tempPath.split('\\')[-1],"")
    elif '/' in tempPath:
        tempPath = tempPath.replace(tempPath.split('/')[-1],"")
    return tempPath
