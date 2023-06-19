import random
import requests

# function for getting random question from codeforces
def cf_get_random_question_rating(rating, tag = None):
    # Get the problem set
    problem_set = requests.get('https://codeforces.com/api/problemset.problems'+('?tags='+tag if tag else ''))
    data = problem_set.json()['result']['problems']
    q_list = []
    # Get the list of problems with the given rating
    for problem in data:
        for d in problem:
            if (d == 'rating'):
                if (problem[d] == rating):
                    q_list.append(problem)
    if (len(q_list) == 0):
        return None
    #Get a random problem from the list
    q_index = random.randint(0, len(q_list)-1)
    problem = q_list[q_index]
    # Return a tuple of problem link, problem id, problem name, problem rating, problem info
    prob_link = 'https://codeforces.com/problemset/problem/' + \
        str(problem['contestId'])+'/'+str(problem['index'])
    prob_id = str(problem['contestId'])+':' + str(problem['index'])
    prob_name = problem['name']
    prob_rating = problem['rating']
    prob_info = {'problem': problem, 'prob_link': prob_link,
                 'prob_id': prob_id, 'prob_name': prob_name, 'prob_rating': prob_rating}
    return prob_info

# function for getting random question from codeforces with a given tag
def cf_get_random_question_tag(tag, rating=None):
    # First replace all spaces with %20
    for i in range(0, len(tag)):
        if tag[i] == '_':
            tag = tag[0:i] + '%20' + tag[i+1:]
    # Get the random question with tag
    return cf_get_random_question_rating(rating, tag)

# function to discard the japanese problems on atcoder
def is_english_problem(problem):
    # It is a japanese problem if the first 3 letters of the contest id are abc and the contest number is less than 41
    # Or It is a japanese problem if the first 3 letters of the contest id are arc and the contest number is less than 57
    if((str(problem['id'][:3]) == 'abc') and int(problem['contest_id'][3:6]) <= 41):
        return False
    if((problem['id'][:3] == 'arc') and (int(problem['contest_id'][3:6]) <= 57)):
        return False
    return True

# function for getting random question from atcoder
def ac_get_random_question(contest_type, question_type):
    # Get a random question given the contest type and question type (an index from A to Z)
    contest_type = contest_type.lower()
    question_type = question_type.upper()
    q = requests.get(
        'https://kenkoooo.com/atcoder/resources/problems.json').json()
    
    q_list = []
    # Get the list of problems with the given contest type and question type
    for problem in q:
        if ((problem['id'][:3] == contest_type) & (problem['problem_index'] == question_type)):
            if((is_english_problem(problem))):
                q_list.append(problem)
    if (len(q_list) == 0):
        return None         
    # Get a random problem from the list  
    q_index = random.randint(0, len(q_list)-1)
    problem = q_list[q_index]
    # Return a tuple of problem link, problem name, problem info
    prob_link = 'https://atcoder.jp/contests/' + \
        problem['contest_id']+'/tasks/'+problem['id']
    prob_name = problem['title']
    prob_info = {'problem': problem,
                 'prob_link': prob_link, 'prob_name': prob_name}
    return prob_info