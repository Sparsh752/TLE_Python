import random
from bs4 import BeautifulSoup
import requests

# function for verification of the user

# function for getting random question from codeforces

# gets the total number of pages in the problem set, which contains the required questions
def number_of_pages(rating):
    try:
        s = 'https://codeforces.com/problemset?tags='
        s += str(rating)+'-'+str(rating)
        resp=requests.get(s)
        S = BeautifulSoup(resp.text, 'lxml')
        return (S.find_all('span',class_='page-index')[-1].text)
    except Exception as e:
        print(e)

# finds the number of questions on the last-page, as it might not contain the standard 100 questions
def number_of_q_last_page(last_page, rating):
    try:
        s = 'https://codeforces.com/problemset/page/'
        s += str(last_page) + '?tags=' + str(rating)+'-'+str(rating)
        resp=requests.get(s)
        S = BeautifulSoup(resp.text, 'lxml')
        q_set = S.find_all('td',class_='act')
        return (len(q_set))
    except Exception as e:
        print(e)

# the random question finder 
def question_finder(rating):
    total_pages = number_of_pages(rating)
    total_questions = number_of_q_last_page(total_pages, rating) + (int(total_pages)-1)*100

    random_q = random.randint(1, total_questions)
    page = random_q//100 + 1
    q = random_q%100
    try:
        s = 'https://codeforces.com/problemset/page/'
        s += str(page) + '?tags=' + str(rating)+'-'+str(rating)
        resp=requests.get(s)
        S = BeautifulSoup(resp.text, 'lxml')
        q_set = S.find_all('td',class_='id')
        return (q_set[q].find('a').get('href'))
    except Exception as e:
        print(e)
q_id = question_finder(1800) 
# update 1800 with the rating given in the input by the user
question = 'https://codeforces.com/' + q_id
print(question)