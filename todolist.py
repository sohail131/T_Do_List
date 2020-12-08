from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy.orm import sessionmaker

# Write your code here
Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="Task")
    deadline = Column(Date, default=datetime.datetime.today())

    def __repr__(self):
        return self.task


class ToDoList:
    def __init__(self):
        self.engine = create_engine("sqlite:///todo.db?check_same_thread=False")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def main_function(self):
        while True:
            option = int(input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n"
                               "6) Delete task\n0) Exit\n"))

            if option == 0:
                exit("Bye!")
            elif option == 1:
                self.show_today_tasks()
            elif option == 2:
                self.show_week_tasks()
            elif option == 3:
                self.show_all_tasks()
            elif option == 4:
                self.show_missed_tasks()
            elif option == 5:
                self.add_tasks()
            elif option == 6:
                self.delete_tasks()

    def show_today_tasks(self):
        rows = self.session.query(Table).all()
        today = datetime.datetime.today()
        print(f"\nToday {today.strftime('%d %b')}:")
        count = 0

        if len(rows) == 0:
            print("Nothing to do!\n")
        else:
            for i, j in enumerate(rows):
                if j.deadline.day == today.day:
                    print(f"{count + 1}. {j}")
                    count += 1
            print()

    def show_week_tasks(self):
        today = datetime.datetime.today()
        rows = self.session.query(Table).all()
        index = 0
        for i in range(7):
            next_date = today + datetime.timedelta(days=index)
            print(f"\n{next_date.strftime('%A %d %b')}")
            found = False
            count = 0
            for k, j in enumerate(rows):
                if next_date.day == j.deadline.day:
                    found = True
                    print(f"{count + 1}. {j}")
                    count += 1
            if not found:
                print("Nothing to do!")
            print()
            index += 1

    def show_all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print("\nAll tasks:")
        if rows:
            for i, task in enumerate(rows):
                print('{}. {}. {} {}'.format(i + 1, task, task.deadline.day, task.deadline.strftime('%b')))
        else:
            print("Nothing to do!")
        print()

    def add_tasks(self):
        add_task = input("Enter task\n")
        add_deadline = input("Enter deadline\n")
        new_row = Table(task=add_task, deadline=datetime.datetime.strptime(add_deadline, "%Y-%m-%d"))
        self.session.add(new_row)
        self.session.commit()
        print("The task has been added!\n")

    def show_missed_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        today = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d")
        print("\nMissed tasks:")
        count = 0
        found = False

        if rows:
            for i, j in enumerate(rows):
                if datetime.datetime.strftime(j.deadline, "%Y-%m-%d") < today:
                    print(f"{count + 1}. {j}")
                    count += 1
                    found = True
        if not found:
            print("Nothing is missed!")
        print()

    def delete_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        print("\nChoose the number of the task you want to delete:")
        items = []

        if rows:
            for i, j in enumerate(rows):
                print(f"{i + 1}. {j}. {j.deadline.day} {j.deadline.strftime('%b')}")
                items.append(j)

            number = int(input()) - 1
            self.session.delete(items[number])
            self.session.commit()
            print("The task has been deleted!")
        else:
            print("Nothing to do!")
        print()


if __name__ == '__main__':
    ToDoList().main_function()
