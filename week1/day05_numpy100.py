#1-5
import numpy as np
print(np.__version__)
arr=np.zeros(10)
print(arr.nbytes)
#In terminal -> python -c "import numpy as np; help(np.add)"

#6-10
arr[4]=1
print(arr)
arr1=np.arange(10,50)
print(arr1)
print(arr1[::-1])
matrix=np.arange(0,9).reshape(3,3)
print(matrix)
arr2=[1,2,0,0,4,0]
indices=np.nonzero(arr2)
print("10:",indices)    #exercise 10 output shows (array([0, 1, 4]),) — that tuple wrapper is because np.nonzero returns a tuple of arrays (one per dimension). 
print(np.nonzero(arr2)[0])  #For a 1D array, this is cleaner access

#11-15
print("-"*20)
print("11:",np.eye(3))
twelve=np.random.rand(27).reshape(3,3,3)    #print(np.random.rand(3,3,3))
print("12:",twelve)
thirteen=np.random.rand(10,10)
print("13:",thirteen)
print(f"Max:{thirteen.max()},Min:{thirteen.min()}")
fourteen=np.random.rand(30)
print(f"Mean of 30 random numbers:{fourteen.mean()}")
fifteen=np.ones((5,5))
fifteen[1:-1,1:-1]=0
print("15:\n",fifteen)
print("-"*20)

#16-20
print("16:\n",np.pad(fifteen,pad_width=1))
print("17:\n")  #NaN = not a number, inf = infinity`
print(0 * np.nan)
print(np.nan == np.nan)
print(np.inf > np.nan)
print(np.nan - np.nan)
print(np.nan in set([np.nan]))
print(0.3 == 3 * 0.1)
print(set([np.nan]))
v=np.arange(1,5)
print("18:\n",np.diag(v,k=-1))
nineteen=np.zeros((8,8))
nineteen[::2,::2]=1
nineteen[1::2,1::2]=1
print("19:\n",nineteen)
print("20:\n",np.unravel_index(99, (6,7,8)))
print("21:\n",np.tile([0,1],(8,4)))
arr22=np.random.rand(5,5)
print("22:\n",(arr22-arr22.min())/(arr22.max()-arr22.min()))
color=np.dtype([("r",np.ubyte),
                ("g",np.ubyte),
                ("b",np.ubyte),
                ("a",np.ubyte)])
print("23:\n",color)
arr_5_3=np.random.random((5,3))
arr_3_2=np.random.random((3,2))
print("24:\n",arr_5_3 @ arr_3_2)
arr25=np.arange(11)
arr25[(3<arr25) & (arr25<8)]*=-1
print("25:\n",arr25)