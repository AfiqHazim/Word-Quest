def leaderboard_sort_desc(list_with_dic):
    length=len(list_with_dic)
    for i in range(0,length-1):
        for j in range(i+1,length):
            if list_with_dic[i]["score"]<list_with_dic[j]["score"]:
                temp=list_with_dic[i]
                list_with_dic[i]=list_with_dic[j]
                list_with_dic[j]=temp


leaderboard=[{"username": "Afiq", "score": 78}, {"username": "Mia", "score": 100}, {"username": "Afzal", "score": 59}]
leaderboard_sort_desc(leaderboard)
print(leaderboard)