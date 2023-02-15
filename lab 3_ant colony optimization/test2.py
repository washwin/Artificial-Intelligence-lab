file = open("tp.txt", "r")
x = file.readline()
y = file.readline().split()
print(y[1])