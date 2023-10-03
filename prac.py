def fun():
    print("inside function")
    
fun()

count = 5
def some_method():
    global count
    print(count)
    count = count + 1
    print(count)
some_method()



def some_fun():
    print("inside some fun")
    def some_inner_fun():
        global var
        var=10
        print("the value of var inside inner function is ",var)
    some_inner_fun()
    print("the outer space of inner function where the value of var is ",var)
some_fun()


val = input("Enter your value: ")
print(val)