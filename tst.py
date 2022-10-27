t = 'Глава 12 том 8'
tmp = t.split(' ')
for i in tmp:
    if i.isnumeric():
        print(i)
        break

