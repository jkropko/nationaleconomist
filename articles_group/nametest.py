print(__name__)
def myfunction():
    print(__name__)
def mysecondfunction():
    myfunction()
    
myfunction()
mysecondfunction()