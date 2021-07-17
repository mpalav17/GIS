from fastapi import FastAPI as fa
import psycopg2
from collections import defaultdict

app = fa()

conn = psycopg2.connect(
    database="qvinvaue",
    user="qvinvaue",
    password="6wj_hX8SkmAoFj1PIEOYfixVBA9Rm182",
    host="batyr.db.elephantsql.com",
)

dict = {}

@app.get('/village/{village_code}')
def get_village(village_code: int):

    table_name = ['domestic_details','village_details','crop_details_kharif']

    for i in table_name:
        cur = conn.cursor()
        if i == 'village_details':
            cur.execute('select * from '+ i +' where code='+str(village_code)+';')
        else:
            cur.execute('select * from '+ i +' where village_code='+str(village_code)+';')
        res = list(cur.fetchall())
        cur.close()
        cur = conn.cursor()
        # print("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME ='"+ str(i) +"';")
        cur.execute("select * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME ='"+ str(i) +"';")
        res_col = list(cur.fetchall())
        cur.close()
        # print(type(res_col[0][3]))
        # print(res_col[0][3])
        len_res = len(res)
        len_res_col = len(res_col)
        print(len_res)
        # print(list(res))
        cnt = 0
        for row in res:
            cnt+=1
        if res:
            if cnt == 1:
                for j in range(0,len_res):
                    dict_in = {}
                    for k in range(0,len_res_col):
                        dict_in[str(res_col[k][3])] = res[j][k]
            elif cnt >= 2:
                dict_in  = {}
                for j in range(0,len_res_col):
                    list1=[]
                    for k in range(0,len_res):
                        list1.append(res[k][j])
                    dict_in[str(res_col[j][3])] = list1
            dict[i] = dict_in
                # else:
                #     print(i)
                #     for k in range(0,len_res_col):
                #         for l in range(0,len(res[j])):
                #             list1.append(res[j][k][l])
            # print(dict_in)
                        
                
                # create dict here for table name
                # list1 = []
                # dict_in = defaultdict(list)
                # for k in range(0,len_res_col):
                #     if len_res == 1:
                #         dict_in[str(res_col[k][3])].append(res[j][k])
                #     elif len_res >= 2:
                #         for l in range(0,len(res[j][k])):
                #             list1.append(res[j][k][l])
                #     print(list1)
                # for k in range(0,len_res_col):
                    # insert in above dict
                    # print(res[j][k])
                    # dict_in[str(res_col[k][3])].append(res[j][k])
                # print(dict_in)
            # dict[i] = dict_in
            # nested dict, dict in dict
        else:
            for j in range(0,len_res):
                # create dict here for table name
                dict_in = defaultdict(list)
                for k in range(0,len_res_col):
                    # insert in above dict
                    print(res[j][k])
                    dict_in[str(res_col[k][3])].append('-')
            dict[i] = dict_in
    return dict
conn.commit()
            # print(j)
            # print(res[0][j],':',res_col[j][3])
        # if(res):
        #     dict={}
        #     for row in res:
        #         dict['Village Name']=row[5]
        #         dict['Village Area']=row[6]
        # else:
        #     dict['Village Name']= '-' 
        #     dict['Village Area']= '-'
        

