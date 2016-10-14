import numpy as np

nx, ny = (3,2)
x = np.linspace(0,1,nx)
y = np.linspace(0,1,ny)
#xv, yv = np.meshgrid(y,x)
print(x)
print(y)
print(np.meshgrid(x,y))
print(np.meshgrid(y,x))

# c=complex(1,2)
# l=list(range(1,100,5))
# #l.append(c)
# arr = np.array(l)
# print(arr)