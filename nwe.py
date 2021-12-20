sy = int(input())
ey = int(input())

count = 0

for i in range(sy, ey+1):
	if i%4 == 0 or i%400 == 0:
		count += 1

print(count)