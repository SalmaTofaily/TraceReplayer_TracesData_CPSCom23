def dictionaryToFile(filename:str,dic):
    with open(filename, 'w') as f: 
        for key, value in dic.items(): 
            f.write('%s:%s\n' % (key, value))