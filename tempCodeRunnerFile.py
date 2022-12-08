for obj in response:
        if(obj['result']=='AC'):
            last_solved_atcoder.append(obj['problem_id'])
    print(last_solved_atcoder)