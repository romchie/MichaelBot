from MysteryBox import MysteryBox

if __name__ == '__main__':
    db = MysteryBox()
    print('\nClear Types:')
    for clear_type in db.db_clear_types:
        print(f'> {clear_type}')
    chosen_type = input(f'\nEnter clear type: ')
    if chosen_type in db.db_clear_types:
        if input(f'\nAre you sure to want to clear db of type {chosen_type}?\n(y/n): ') == 'y':
            db.clearDataBase(chosen_type)
            print(f'cleared {chosen_type}')
        else:
            print('Clear cancelled')
    else:
        print('not a valid clear type')