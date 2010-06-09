'''
Created on 10.06.2010

@author: Bao
'''


'''
Created on 10.06.2010

@author: Bao

removes blanks from a list
'''
def removeBlanksInList(list):
    err=None
    while(err==None):
        try:
            list.remove('')
        except:
            err=True
    return list




list=str('a+b++c++d+e++f').split('+')
list=removeBlanksInList(list)

        

print list

