import click


@click.command('tick', short_help='Generate TickTick\'s .csv file')
@click.argument('rasp-file', type=str)
@click.option('-n', '--name', help='full name of teacher, default: all teachers',
              default='all')
@click.option('-y', '--year', default=now_year, type=int, show_default=True)
@click.option('-o', '--output', type=str,
              help='Output file name. Default: \'FullName TickTick.csv\'')
@click.option('-t', '--tag', default='', type=str, help='Set tag to all tasks')
@click.option('-f', '--folder-name', default='', type=str, help='Set folder name to all tasks')
@click.option('--names', is_flag=True, help='Show all available teachers names')
@click.option('-l', '--list-name', default='Pairs', type=str,
              help='Task list\'s name', show_default=True)
def tick(rasp_file, name, year,
         names, output, tag, folder_name, list_name):
    """
    Generates .csv file in TickTick format
    :param list_name: task list's name
    :param folder_name: folder name for each task
    :param tag: tag for each task
    :param rasp_file: xlsx file with rasp (path to file)
    :param name: name of the teacher whose schedule you want to export
    :param year: if you generate rasp for next year or
    your computer have wrong date
    :param names: flag to show all available names
    :param output: .csv file name (path to file)
    :return:
    """

    logger = logging.getLogger("gcalendar")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("logs.txt", mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    rasp = Storage.serialize(rasp_file)
    rasp.quantum_check()
    teachers_names = rasp.get_names_list()
    if names:
        print(teachers_names)
        sys.exit(0)
    if name in teachers_names:
        output_file = str(name) + ' TickTick.csv'
        if output:
            output_file = output
        teachers_pairs = rasp.get_teacher_pairs_dict()[name]
        calendar = TickTick(teachers_pairs, year, folder_name, list_name, tag)
        calendar.dump(output_file)
        print('Generated file %s ready to import in your tick tick!' % output_file)
    elif name == 'all':
        for name_ in teachers_names:
            teachers_pairs = rasp.get_teacher_pairs_dict()[name_]
            calendar = TickTick(teachers_pairs, year, folder_name, list_name, tag)
            calendar.dump(output_file=str(name_) + ' TickTick.csv')
            print('Generated file %s ready to import in '
                  'your tick tick!' % ('\'' + str(name_) + ' TickTick.csv\''))
    elif name not in teachers_names:
        print('There is no teacher %s in file, try --names option to get valid names list' % name)
