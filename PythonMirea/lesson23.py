def f23(l):
    table = [[]]
    new_table= [[]]
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
        array_f.append(array[1])
        array_f.append(array[2])
        array_f.append(array[3])
        array_f.append(array[0].split(' ')[0])
        new_table.append(array_f)
    new_table.remove([])
    return new_table