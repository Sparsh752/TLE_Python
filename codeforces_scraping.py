import random
from bs4 import BeautifulSoup
import requests

# function for verification of the user


# function for getting random question from codeforces

# question based on rating
def cf_get_random_question_rating(rating):
    p = requests.get('https://codeforces.com/api/problemset.problems')
    data = p.json()['result']['problems']
    q_list = []
    for problem in data:
        for d in problem:
            if (d == 'rating'):
                if (problem[d] == rating):
                    q_list.append(problem)
    q_index = random.randint(0, len(q_list)-1)
    problem = q_list[q_index]
    prob_link = 'https://codeforces.com/problemset/problem/' + \
        str(problem['contestId'])+'/'+str(problem['index'])
    prob_id = str(problem['contestId'])+':' + str(problem['index'])
    prob_name = problem['name']
    prob_rating = problem['rating']
    prob_info = {'problem': problem, 'prob_link': prob_link,
                 'prob_id': prob_id, 'prob_name': prob_name, 'prob_rating': prob_rating}
    return prob_info

# question based on tags
def cf_get_random_question_tag(tag, rating=None):
    for i in range(0, len(tag)):
        if tag[i] == '_':
            tag = tag[0:i] + '%20' + tag[i+1:]
    p = requests.get('https://codeforces.com/api/problemset.problems?tags='+tag)
    data = p.json()['result']['problems']
    q_list = []
    for problem in data:
        if "rating" in problem.keys():
            if (problem['rating'] == rating):
                q_list.append(problem)
    if (len(q_list) == 0):
        return None
    q_index = random.randint(0, len(q_list)-1)
    problem = q_list[q_index]
    prob_link = 'https://codeforces.com/problemset/problem/' + \
        str(problem['contestId'])+'/'+str(problem['index'])
    prob_id = str(problem['contestId'])+':' + str(problem['index'])
    prob_name = problem['name']
    prob_rating = problem['rating']
    prob_info = {'problem': problem, 'prob_link': prob_link,
                 'prob_id': prob_id, 'prob_name': prob_name, 'prob_rating': prob_rating}
    return prob_info

# function for getting random question from atcoder

# function to discard japanese problems
def is_english_problem(problem):
    if((str(problem['id'][:3]) == 'abc') and int(problem['contest_id'][3:6]) <= 41):
        return False
    if((problem['id'][:3] == 'arc') and (int(problem['contest_id'][3:6]) <= 57)):
        return False
    return True

def ac_get_random_question(contest_type, question_type):
    contest_type = contest_type.lower()
    question_type = question_type.upper()
    q = requests.get(
        'https://kenkoooo.com/atcoder/resources/problems.json').json()
    q_list = []
    for problem in q:
        if ((problem['id'][:3] == contest_type) & (problem['problem_index'] == question_type)):
            q_list.append(problem)
            if((is_english_problem(problem))):
                pass
                
    q_index = random.randint(0, len(q_list)-1)
    problem = q_list[q_index]
    prob_link = 'https://atcoder.jp/contests/' + \
        problem['contest_id']+'/tasks/'+problem['id']
    prob_name = problem['title']
    prob_info = {'problem': problem,
                 'prob_link': prob_link, 'prob_name': prob_name}
    return prob_info