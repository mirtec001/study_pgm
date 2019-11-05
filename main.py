import sqlite3
import random


def import_questions():
    # open database
    connection = sqlite3.connect('cissp1.db')
    # read file in to list

    print("Please enter the name of the file")
    filename = input(">> ")

    with open(filename, 'r') as fr:
        read_in = fr.readlines()

    letter_list = ['a', 'b', 'c', 'd']
    # organize the list so it reads Question,Correct,Answer,Answer,Answer

    for j in range(int(len(read_in) / 6)):
        question = []
        # Here's our structure
        question.append(read_in[j * 6].strip())
        answers = [read_in[(j * 6) + 1].strip(), read_in[(j * 6) + 2].strip(),
                   read_in[(j * 6) + 3].strip(), read_in[(j * 6) + 4].strip()]
        int_answer = letter_list.index(read_in[(j * 6) + 5].strip().lower())
        question.append(answers[int_answer])
        if int_answer == 0:
            question.append(answers[1])
            question.append(answers[2])
            question.append(answers[3])
        if int_answer == 1:
            question.append(answers[0])
            question.append(answers[2])
            question.append(answers[3])
        if int_answer == 2:
            question.append(answers[0])
            question.append(answers[1])
            question.append(answers[3])
        if int_answer == 3:
            question.append(answers[0])
            question.append(answers[1])
            question.append(answers[2])

        # write the changes to the database
        connection.execute("INSERT INTO questions(Question,Answer1,Answer2,Answer3,Answer4) VALUES(?,?,?,?,?)",
                           (question[0], question[1], question[2],
                            question[3], question[4]))
    connection.commit()


def print_question(item):
    question = item
    print(question[1])
    print("A. " + question[2])
    print("B. " + question[3])
    print("C. " + question[4])
    print("D. " + question[5])


def take_test(number_of_questions):
    alphabet = ['a', 'b', 'c', 'd']
    total_right = 0
    current_question = 0
    conn = sqlite3.connect('cissp1.db')
    c = conn.cursor()
    questions = []
    for row in c.execute("SELECT * From questions"):
        questions.append(row)

    if number_of_questions == 9999:
        number_of_questions = len(questions)

    total_questions = number_of_questions

    random.shuffle(questions)
    for x in range(number_of_questions):
        mark = questions[x]
        current_question += 1
        grade = (total_right / total_questions) * 100
        temp_question = []

        shuffled_answers = []
        while len(shuffled_answers) != 4:
            ans = random.randint(2, 5)
            while ans not in shuffled_answers:
                shuffled_answers.append(ans)
                ans = random.randint(2, 5)
                if ans not in shuffled_answers:
                    shuffled_answers.append(ans)

        temp_question.append(mark[0])
        temp_question.append(mark[1])
        temp_question.append(mark[shuffled_answers[0]])
        temp_question.append(mark[shuffled_answers[1]])
        temp_question.append(mark[shuffled_answers[2]])
        temp_question.append(mark[shuffled_answers[3]])

        print("Question: " + str(current_question) + " of " + str(total_questions) + "                                          Grade: " + str(int(grade)) + "%")
        print_question(temp_question)
        print("-------------------")
        answer = input(">> ")

        i_answer = alphabet.index(answer.lower()) + 2

        correct_answer = 0
        for j in range(len(shuffled_answers)):
            if shuffled_answers[j] == 2:
                correct_answer = j + 2

        '''print("[DEBUG]: Your answer " + str(i_answer))
        print("[DEBUG]: Correct answer " + str(correct_answer))'''

        if i_answer == correct_answer:
            print("Correct")
            total_right += 1
        else:
            print("I'm sorry, the correct answer is " + alphabet[correct_answer - 2].upper())

        grade = (total_right / total_questions) * 100

    c.close()
    print("Final grade: " + str(int(grade)) + "%")


def main():
    answer = ""
    while answer not in {"n", "no"}:
        print("Do you have questions to import? (y/n)")
        answer = input(">> ")
        if answer.lower() in {"y", "yes"}:
            import_questions()
    print("How many questions do you want to take? Press Enter for all")
    answer = input(">> ")
    if len(answer) > 0:
        number_of_questions = int(answer)
        take_test(number_of_questions)
    else:
        take_test(9999)


if __name__ == "__main__":
    main()
