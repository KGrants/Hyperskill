from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
import sqlalchemy as db


Base = declarative_base()


class Tasks(Base):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.VARCHAR)
    deadline = db.Column(db.Date, default=datetime.today())


engine = db.create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)

metadata = db.MetaData()
task_table = db.Table('task', metadata, autoload=True, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()


def first_screen():
    menu_list = ["1) Today's tasks",
                 "2) Week's tasks",
                 "3) All tasks",
                 "4) Add a task",
                 "0) Exit"]
    print("", *menu_list, sep="\n")
    return int(input(">".strip()))


def show_tasks_all():
    counter = 1
    result = session.query(Tasks).order_by(Tasks.deadline).all()
    print("All tasks:")
    for row in result:
        set_date = datetime.strptime(str(row.deadline),'%Y-%m-%d')
        date_to_print = datetime.strftime(set_date, '%#d %b')
        print(f"{counter}. {row.task}. {date_to_print}")
        counter += 1
    return


def show_tasks_day(date=datetime.today().date()):
    counter = 1
    result = session.query(Tasks).filter(Tasks.deadline == date)
    print(f"\n{datetime.strftime(date, '%A %d %b')}")
    if result.first() is None:
        print("Nothing to do!")
    else:
        for row in result:
            print(f"{counter}. {row.task}")
            counter += 1
    return


def show_tasks_week():
    for i in range(7):
        date = datetime.today().date()+timedelta(days=i)
        show_tasks_day(date)
    return


def add_a_task():
    user_input = input("Enter a task\n>")
    deadline_input = input("Enter a deadline\n>")
    date = datetime.strptime(deadline_input, '%Y-%m-%d')
    session.add(Tasks(task=user_input, deadline=date))
    session.commit()
    print("The task has been added!")
    return


def exit_app():
    print("\nBye!")
    session.close()
    sys.exit()


def main():
    while True:
        user_input = first_screen()
        if user_input == 1:
            show_tasks_day()
        elif user_input == 2:
            show_tasks_week()
        elif user_input == 3:
            show_tasks_all()
        elif user_input == 4:
            add_a_task()
        else:
            exit_app()


if __name__ == '__main__':
    main()

