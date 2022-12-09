import random
from bs4 import BeautifulSoup
import requests

# function for verification of the user


# function for getting random question from codeforces

# question based on rating
def q_based_on_rating(rating):
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
        str(problem['contestId'])+'/'+problem['index']
    prob_id = problem['contestId']+':' + problem['index']
    prob_name = problem['name']
    prob_rating = problem['rating']
    prob_info = {'problem': problem, 'prob_link': prob_link,
                 'prob_id': prob_id, 'prob_name': prob_name, 'prob_rating': prob_rating}
    return prob_info

# question based on tags
def q_based_on_tags(tag_list):
    p = requests.get('https://codeforces.com/api/problemset.problems')
    data = p.json()['result']['problems']
    q_list = []
    for problem in data:
        for d in problem:
            if (d == 'tags'):
                for tag in d:
                    if (tag in tag_list):
                        q_list.append(problem)
    q_index = random.randint(0, len(q_list)-1)
    problem = q_list[q_index]
    prob_link = 'https://codeforces.com/problemset/problem/' + \
        str(problem['contestId'])+'/'+problem['index']
    prob_id = problem['contestId']+':' + problem['index']
    prob_name = problem['name']
    prob_rating = problem['rating']
    prob_info = {'problem': problem, 'prob_link': prob_link,
                 'prob_id': prob_id, 'prob_name': prob_name, 'prob_rating': prob_rating}
    return prob_info

# function for getting random question from atcoder

# function to discard japanese problems
def ok(problem):
    if((problem['id'][:3] == 'abc') & int(problem['contest_id'][3:6]) > 41):
        return True
    if((problem['id'][:3] == 'arc') & (int(problem['contest_id'][3:6]) > 57)):
        return True
    return False

def random_atcoder_question(contest_type, question_type):
    contest_type = contest_type.lower()
    question_type = question_type.upper()
    q = requests.get(
        'https://kenkoooo.com/atcoder/resources/problems.json').json()
    q_list = []
    for problem in q:
        u = 0
        for data in problem:
            if (data == 'id'):
                if ((problem[data][:3] == contest_type)):
                    if (ok(problem)):
                        u = u+1
            if (data == 'problem_index'):
                if (problem[data] == question_type):
                    u = u+1
            if (u == 2):
                q_list.append(problem)
                break
    q_index = random.randint(0, len(q_list)-1)
    problem = q_list[q_index]
    prob_link = 'https://atcoder.jp/contests/' + \
        problem['contest_id']+'/tasks/'+problem['id']
    prob_name = problem['title']
    prob_info = {'problem': problem,
                 'prob_link': prob_link, 'prob_name': prob_name}
    return prob_info