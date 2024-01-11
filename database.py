import pymysql
def conn():
    return pymysql.connect(host='localhost',
                                 user='root',
                                 password='Vicky@7005',
                                 db='project',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)


def question_fetcher(category_name):
    view = conn()
    view_cur = view.cursor()
    view_cur.execute(f"SELECT * FROM {category_name}")
    r = view_cur.fetchall()
    #print(r)
    dic={}
    for i in r:
        dic[(i['problems'])]=i['id']
    return dic

#print(question_fetcher("display_faq"))

def solution(key,category_name,n):
    view = conn()
    view_cur = view.cursor()
    view_cur.execute(f"SELECT * FROM {category_name} where id={key} ORDER BY score DESC; ")
    r = view_cur.fetchall()
    return r[n]['solution']

def sol_length(key,category_name):
    view = conn()
    view_cur = view.cursor()
    view_cur.execute(f"SELECT * FROM {category_name} where id={key} ORDER BY score DESC; ")
    r = view_cur.fetchall()
    return len(r)


def score_updater(sol,category_name):
    view = conn()
    view_cur = view.cursor()
    print(f'update {category_name} set score=score+1 where solution="{sol}"')
    view_cur.execute(f'update {category_name} set score=score+1 where solution="{sol}"')
    view.commit()
    view.close()
    return 0
