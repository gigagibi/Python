def f23(l):
    table = [[]]
    for row in l:
        if row not in table:
            table.append(row)
    table.remove([])
    for line in table:
        array = []
        array_f = []
        for cell in line:
            if cell is not None:
                if str(cell).find('|') != -1:
                    b = cell.split('|')
                    array.append(b[0])
                    array.append(round(float(b[1]), 1))
                elif str(cell).find('@') != -1:
                    array.append(cell.split('@')[1])
                elif cell == '0':
                    array.append('Нет')
        #print(array)
        array_f.append(array[1])
        array_f.append(array[2])
        array_f.append(array[3])
        array_f.append(array[0].split(' ')[0])
        print(array_f)
    # print(table)


f23([['Бикак Мирослав|0.789', None, 'miroslav2@mail.ru', '0'],
     ['Тачко Илья|0.135', None, 'tacko47@rambler.ru', '0'],
     ['Тачко Илья|0.135', None, 'tacko47@rambler.ru', '0'],
     ['Цечокли Тимур|0.894', None, 'zecokli@rambler.ru', '0'],
     ['Тачко Илья|0.135', None, 'tacko47@rambler.ru', '0']])
print('')
print('')
print('')
print('')
f23([['Белий Тамерлан|0.743', None, 'tamerlan88@yandex.ru', '0'],
     ['Сититев Руслан|0.721', None, 'sititev79@rambler.ru', '0'],
     ['Белий Тамерлан|0.743', None, 'tamerlan88@yandex.ru', '0'],
     ['Датук Владислав|0.254', None, 'vladislav50@mail.ru', '0'],
     ['Белий Тамерлан|0.743', None, 'tamerlan88@yandex.ru', '0']])
