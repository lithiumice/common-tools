


if __name__ == "__main__":
    N = 10
    K = 5
    
    person = [i for i in range(1, N+1)]
    
    cnt = 0
    current_person_index = 0
    
    res = []
    
    while len(person)>1:
        print(f"person: {person} current_person_index: {current_person_index} cnt: {cnt}")
        cnt += 1
        if cnt % K == 0:
            res.append(person[current_person_index])
            person.pop(current_person_index)
            cnt = 0
            
        current_person_index += 1
        if current_person_index >= len(person):
            current_person_index = 0
            
    left_person = person[0]
    
    print(f"poped person: {res}")
    print(f"left_person: {left_person}")
            
            