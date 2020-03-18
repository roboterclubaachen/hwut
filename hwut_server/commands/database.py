from flask_script import Manager, prompt_bool

from hwut_server.database import db
from hwut_server.models import Users, Boards, Microcontrollers, Runners

manager = Manager(help="Perform database operations")


@manager.command
def create():
    """ Initialize the database by creating the necessary tables and indices """

    # create all tables and indices
    db.create_all()


@manager.command
def drop():
    """ Drops database tables """

    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
    else:
        exit(1)


@manager.command
def test_data():
    """ Populated the database with some sample data """

    user = Users('user', '1234', 1)
    db.session.add(user)
    print('Normal user created:')
    print('\tusername: user')
    print('\tpassword: 1234')
    print('')

    superuser = Users('superuser', '123456', 10000)
    db.session.add(superuser)
    print('Superuser created:')
    print('\tusername: superuser')
    print('\tpassword: 123456')
    print('')

    microcontroller = Microcontrollers('stm32f303re', manufacturer='STMicroelectronics')
    db.session.add(microcontroller)
    print('Microcontroller created: {}'.format(microcontroller.name))
    print('')

    board = Boards('nucleo-f303re', 'stm32f303re', manufacturer='STMicroelectronics')
    db.session.add(board)
    print('Board created: {}'.format(board.name))
    print('')

    runner = Runners(user.name, board.name)
    runner.token = 'Uu51AhKNCbaiAci5CXmAm3vQepPG7zEoBJ5tpj81cd8'  # Don't do this at home!
    db.session.add(runner)
    db.session.commit()
    print('Runner created:')
    print('\tusername/id: {}'.format(runner.id))
    print('\tpassword: {}'.format(runner.token))
