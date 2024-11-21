from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column



app = Flask(__name__)


DATABASE_URL = "sqlite:///lessons.db"
engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    teacher: Mapped[str] = mapped_column(String(50), nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False)

def create_db():
 Base.metadata.create_all(engine)


@app.get('/')
def index():
    with Session(engine) as session:
        lessons = session.query(Lesson).all()
    return render_template('index.html', lessons=lessons)


@app.get('/add')
def show_add_form():
    return render_template('add.html')


@app.post('/add')
def handle_add_lesson():
    with Session(engine) as session:
        title = request.form['title']
        description = request.form['description']
        teacher = request.form['teacher']
        duration = int(request.form['duration'])

        new_lesson = Lesson(
            title=title,
            description=description,
            teacher=teacher,
            duration=duration
        )
        session.add(new_lesson)
        session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

