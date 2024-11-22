from memo_card_layout import (
    app, layout_card,
    lb_Question, lb_Correct, lb_Result,
    rbtn_1, rbtn_2, rbtn_3, rbtn_4,
    btn_OK, btn_Menu, show_question, show_result
)
from PyQt5.QtWidgets import QWidget, QApplication
from random import shuffle  # перемішуватимемо відповіді у картці питання
from memo_card_menu import AddQuestionForm
from question import *

card_width, card_height = 600, 500  # початкові розміри вікна "картка"
text_wrong = 'Неправильно'
text_correct = 'Правильно'

# Перемішуємо відповіді між радіокнопками
radio_list = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]
shuffle(radio_list)
answer = radio_list[0]  # правильна відповідь
wrong_answer1, wrong_answer2, wrong_answer3 = radio_list[1], radio_list[2], radio_list[3]


def show_data():
    global question_number
    ''' показує потрібну інформацію на екрані '''
    frm_question = questions[question_number]['question']
    frm_right = questions[question_number]['right']
    frm_wrong1, frm_wrong2, frm_wrong3 = questions[question_number]['wrongs']

    lb_Question.setText(frm_question)
    lb_Correct.setText(frm_right)
    answer.setText(frm_right)
    wrong_answer1.setText(frm_wrong1)
    wrong_answer2.setText(frm_wrong2)
    wrong_answer3.setText(frm_wrong3)


def check_result():
    ''' перевірка, чи правильна відповідь обрана
        Якщо відповідь була обрана, то напис "правильно/неправильно" набуває потрібного
        значення і показується панель відповідей
    '''
    correct = answer.isChecked()  # у цьому радіобаттоні лежить наша відповідь!
    if correct:
        # відповідь вірна, запишемо
        lb_Result.setText(text_correct)  # напис "правильно"
        show_result()
    else:
        incorrect = wrong_answer1.isChecked() or wrong_answer2.isChecked() or wrong_answer3.isChecked()
        if incorrect:
            # відповідь невірна, запишемо і відобразимо у статистиці
            lb_Result.setText(text_wrong)  # напис "неправильно"
            show_result()


question_number = 0


def click_OK():
    global question_number
    if btn_OK.text() != 'Наступне питання':
        check_result()
    else:
        try:
            question_number += 1
            show_question()
            show_data()
        except:
            question_number = 0
            print('Питання закінчилися додай ще')


# Вікно основної гри
win_card = QWidget()
win_card.resize(card_width, card_height)
win_card.move(300, 300)
win_card.setWindowTitle('Memory Card')

win_card.setLayout(layout_card)
show_data()
show_question()
btn_OK.clicked.connect(click_OK)


def open_add_question_form():
    add_question_form = AddQuestionForm()

    def handle_add_new_question():
        add_new_question(add_question_form)

    add_question_form.add_btn.clicked.connect(handle_add_new_question)
    add_question_form.show()


def add_new_question(form):
    new_question = {
        "question": form.question_input.text(),
        "right": form.correct_input.text(),
        "wrongs": [
            form.wrong1_input.text(),
            form.wrong2_input.text(),
            form.wrong3_input.text()
        ]
    }

    questions.append(new_question)
    form.close()
    print("Нове питання додано!")


# При натисканні на кнопку "Меню" відкривається форма для додавання питання
btn_Menu.clicked.connect(open_add_question_form)

win_card.show()
app.exec_()
