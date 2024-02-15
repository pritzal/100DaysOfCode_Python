from array import *

value = array('i',[2,3,5,6,7,8,])
value.reverse()
print(value[3])

### 2 sum
from array import *

value =array('i',[2,3,4,5,6,7,8,9])
k = len(value)
n=int(input("Enter the target = " ))

def sum(value,k,n):
    for i in range(0,k):
        for j in range(1,k):
            if (value[i]+value[j]== n):
                print(f'{value[i]},{value[j]}')

sum(value,k,8)