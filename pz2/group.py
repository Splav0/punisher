def group_parser(group):
    if not group.startswith('733'):
        print('Это не группа 3 курса')
        return

    if group.endswith('3'):
        print('%s - Третья группа' % group)
    elif group.endswith('4'):
        print('%s - Четверная группа' % group)
    elif group.endswith('5'):
        print('%s - Пятая группа' % group)
    else:
        print('%s - Непонятная группа' % group)


def main():
    """Определятор"""
    group_parser('abc')
    for group_num in range(7331, 7336):
        group = str(group_num)
        group_parser(group)

    answer = input('Попробуйте выйти: ')
    while answer != 'exit' and answer != 'q':
        answer = input('Неправильно! Попробуйте ещё раз: ')
    print('Успех!')


if __name__ == '__main__':
    main()