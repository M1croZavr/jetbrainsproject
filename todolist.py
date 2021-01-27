# Write your code here
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False?')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


class ToDoList:

    def __init__(self):
        self.td_plans = {}
        self.today = None
        self.table_rows = None

    def menu(self):
        print('1) Today\'s tasks', '2) Week\'s tasks', '3) All tasks', '4) Missed tasks',  '5) Add task',
              '6) Delete task', '0) Exit', sep='\n')
        point = int(input())
        if point == 1:
            self.show_td_plans()
            self.menu()
        elif point == 2:
            self.show_wk_plans()
            self.menu()
        elif point == 3:
            self.show_all_plans()
            self.menu()
        elif point == 4:
            self.show_missed_plans()
            self.menu()
        elif point == 5:
            task = input('Enter task ')
            deadline = input('Enter deadline ')
            self.add_task_deadline(task, deadline)
            print('The task has been added!')
            self.menu()
        elif point == 6:
            self.delete_task()
            self.menu()
        elif point == 0:
            print('Bye!')
            return None

    def show_missed_plans(self):
        self.today = datetime.today().date()
        self.table_rows = session.query(Table).filter(Table.deadline < self.today).order_by(Table.deadline).all()
        print('Missed tasks:')
        if not self.table_rows:
            print('Nothing is missed!')
            print()
            return None
        for i, row in enumerate(self.table_rows):
            print(f'{i + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
        print()

    def delete_task(self):
        print('Choose the number of the task you want to delete:')
        self.table_rows = session.query(Table).order_by(Table.deadline).all()
        if not self.table_rows:
            print('Nothing to delete')
            return None
        for i, row in enumerate(self.table_rows):
            print(f'{i + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')
        number_to_delete = int(input())
        row_to_delete = self.table_rows[number_to_delete - 1]
        session.delete(row_to_delete)
        session.commit()
        print('The task has been deleted!')

    def show_wk_plans(self):
        self.today = datetime.today().date()
        for day in range(7):
            day = self.today.strftime('%A')
            date = self.today.day
            month = self.today.strftime('%b')
            self.table_rows = session.query(Table).filter(Table.deadline == self.today).all()
            print(f'{day} {date} {month}: ')
            if not self.table_rows:
                print('Nothing to do!')
            else:
                for i, row in enumerate(self.table_rows):
                    print(f'{i + 1}. {row.task}')
            print()
            self.today = self.today + timedelta(days=1)

    def show_all_plans(self):
        self.table_rows = session.query(Table).order_by(Table.deadline).all()
        for i, row in enumerate(self.table_rows):
            print(f'{i + 1}. {row.task}. {row.deadline.day} {row.deadline.strftime("%b")}')

    def add_task_deadline(self, task, deadline):
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        if deadline not in self.td_plans.keys():
            self.td_plans[deadline] = [task]
        else:
            self.td_plans[deadline].append(task)
        new_row = Table(task=task, deadline=deadline)
        session.add(new_row)
        session.commit()

    def show_td_plans(self):
        self.today = datetime.today()
        self.table_rows = session.query(Table).filter(Table.deadline == self.today.date()).all()
        print(f'Today {self.today.day} {self.today.date().strftime("%b")}:')
        if not self.table_rows:
            print('Nothing to do!')
        else:
            for i, row in enumerate(self.table_rows):
                print('{}. {}'.format(i + 1, row.task))


new_list = ToDoList()
new_list.menu()
