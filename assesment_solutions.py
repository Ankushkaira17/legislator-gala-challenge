import json
class legislator():

    def __init__(self,numtables,guest,planner_preference):
        self.numtables =numtables
        self.guest = guest
        self.pref = planner_preference
        self.arr = [[0 for i in range(len(self.guest))] for i in range(len(self.guest))] #The adjacaency matrix to visualise the relation between people
        self.adj =self.arr

    def getpairs(self,arr):
            n=len(arr)
            k=2
            def backtrack(first , curr = []):
                    
                if len(curr) == k:  
                    output.append(curr[:])
                for i in range(first, n ):
                    
                    curr.append(arr[i])
                        
                    backtrack(i + 1, curr)
                        
                    curr.pop()
            output = []
            backtrack(0)
            return output

    def getcost(self,p1,p2,adj):
        cost=0
        for i in range(len(p1)):
            for j in range(len(p2)):
                cost+=adj[p1[i]-1][p2[j]-1]
        return cost

    def build_adjacency_matrix(self):
        prefer = []
        avoid = []

        for i in range(len(self.pref)):
            if self.pref[i]["preference"]!="avoid":
                prefer.append(self.pref[i]['guests'])
            if self.pref[i]["preference"]!="pair":
                avoid.append(self.pref[i]['guests'])

        for i in range(len(prefer)):
            temp = prefer[i]
            temp = self.getpairs(temp)
            for j in range(len(temp)):
                temp1=temp[j]
                self.arr[temp1[0]-1][temp1[1]-1]=1
                self.arr[temp1[1]-1][temp1[0]-1]=1

        for i in range(len(avoid)):
            temp = avoid[i]
            temp=self.getpairs(temp)
            for j in range(len(temp)):
                temp1=temp[j]
                self.arr[temp1[0]-1][temp1[1]-1]=-1
                self.arr[temp1[1]-1][temp1[0]-1]=-1
            
        for i in range(len(self.arr[0])):
            self.arr[i][i]=1
        # for i in range(len(self.arr[0])):
        #     print(self.arr[i][:])
        self.adj=self.arr
        return self.arr


    def dfs(self,i,visited,out):

        visited[i]=True
        
        for j in range(len(self.arr[0])):
            if(self.arr[i][j]==-1) and (j+1 in out):
                out.pop(-1)
                break
            
            if(self.arr[i][j]==1 and (not visited[j])):
                self.arr[i][j]=0
                out.append(j+1)
                self.dfs(j,visited,out)
        return self.arr, out

    def dfs_util(self):
        visited=[False]*len(self.arr[0])
        mem=[]
        for i in range(len(self.arr[0])):
            if(not(visited[i])):
                for j in range(len(self.arr[0])):
                    if(self.arr[i][j]==1):
                        self.arr[i][j]=0
                        out=[i+1]
                        
                        arr,out=self.dfs(i,visited,out)
                        mem.append(out)
        return mem

    def calculate_seating(self,mem):
        mult=[]
        sing=[]

        if len(self.pref) == 0:

            return { "table_1": self.guest },True
        if self.numtables == 1:
            return {'table_1':self.guest},True
        
        for i in range(len(mem)):   
            if(len(mem[i])==1):
                sing.append(mem[i][0])
            else:
                mult.append(mem[i])

        total_pairs=len(mult)+1
        total_tables=self.numtables
        output={}
        pairs1=[]
        extra =[]
        finalcost =[]
        for items in mem:
            if len(items)<=1:
                extra.append(items)
            else:
                pairs1.append(items)
        extrapair = self.getpairs(extra)
        # newpair = self.getpairs(mem)
        avoidlist =[]
        for items in extrapair:
            check = self.getcost(items[0],items[1],self.adj)
            finalcost.append(check)
            if check < 0:
                avoidlist.append(items)
        rem=[]
        for i in range(len(avoidlist)):
            temp=avoidlist[i]
            for j in range(len(mult)):
                if((self.getcost(mult[j],temp[0],self.adj))>=0):
                    mult[j].append(temp[0][0])
                    rem.append(temp[0][0])
                if((self.getcost(mult[j],temp[1],self.adj))>=0):
                    mult[j].append(temp[1][0])
                    rem.append(temp[1][0])   
        sing2=[]
        for i in range(len(sing)):
            if(sing[i] not in rem):
                sing2.append(sing[i])
        if(total_pairs<=total_tables):
            for i in range(1,len(mult)+1):
                st="table_"+str(i)
                output[st]=mult[i-1]
            if(len(sing2)>0):
                st="table_"+str(i+1)
                output[st]=sing2

        if(total_pairs>total_tables):
            pairs = self.getpairs(mem)
            cost_d={}
            temp=[]
            for j in range(len(pairs)):
                cost=self.getcost(pairs[j][0],pairs[j][1],self.adj)
                if cost in cost_d:
                    cost_d[cost].append(pairs[j])
                else:
                    cost_d[cost]=[pairs[j]]
            gy=set()
            count=1

            for j in reversed(sorted(cost_d.keys())):
                for m in range (1,len(cost_d[j])+1):
                    curr=cost_d[j][m-1]
                    if (tuple(curr[0]) not in gy )and (tuple(curr[1]) not in gy):
                        st="table_"+str(count)
                        count+=1
                        gy.add(tuple(curr[0]))
                        gy.add(tuple(curr[1]))
                        output[st]= [curr[0],curr[1]]
          
            for i in mem:
                if(tuple(i) not in gy):
                    if(count<=total_tables):
                        st="table_"+str(count)
                        count+=1
                        gy.add(tuple(i))
                        output[st]= i
                    else:
                        output[st].append(i)
        return output,False


    def modify_output(self, op):
        finaldic ={}
        for k in op.keys():
            temp=op[k]
            why=[]
            for i in range(len(temp)):
                
                if(type(temp[i])==int):
                    
                    why.append("names_"+str(temp[i]))
                elif len(temp[i])>1:
                    for j in range(len(temp[i])):
                        why.append("names_"+str(temp[i][j]))
                    
                else:
                    why.append("names_"+str(temp[i][0]))
            finaldic[k] = why
        
        return finaldic
                

        


def get_answer(numoftables, gue,pref):
    m =legislator(numoftables,gue,pref)
    arr = m.build_adjacency_matrix()
    memo = m.dfs_util()

    result,flag = m.calculate_seating(memo)
    if(not flag):
        
        result = m.modify_output(result)
        josn_object = json.dumps(result, indent =4)
    else:
        
        josn_object = json.dumps(result, indent =4)
    # print(josn_object)
    with open("/Users/ankushkaira/OneDrive - nyu.edu/Learning/reactsite/my-blog-backend/output.json", "a") as outfile:
        outfile.write(josn_object)
    print(result)
    return result




class testcase():


    def test1(self):
        numberoftables=2
        gue=['names_1','names_2','names_3','names_4','names_5','names_6','names_7','names_8']
        pref=[
        {
            "preference": "avoid",
            "guests": [1, 2]},{
            "preference": "pair",
            "guests": [2, 3]}, {
            "preference": "pair",
            "guests": [6, 3] }, {
            "preference": "avoid",
            "guests": [1,6,7] },
            ]

        checkanswer= get_answer(numberoftables,gue,pref)
        assert checkanswer == {'table_1': ['names_2', 'names_3', 'names_6'], 'table_2': ['names_1', 'names_4', 'names_5', 'names_7', 'names_8']}, 'Not Expected result'
        print("test case 1 is passed.")
        print("\n")
    
    def test2(self):
        numberoftables = 3
        gue=['names_1','names_2','names_3','names_4','names_5','names_6','names_7','names_8','names_9','names_10','names_11','names_12','names_13','names_14']
        pref=[
        {
            "preference": "avoid",
            "guests": [1, 2]
        },
        {
            "preference": "pair",
            "guests": [2, 3]
        },
        {
            "preference": "pair",
            "guests": [6, 3]

        },
        {
            "preference": "avoid",
            "guests": [1,6,7]
        },
        {
            "preference": "avoid",
            "guests": [10, 12]
        },
        {
            "preference": "pair",
            "guests": [13, 11]
        },
            ]

        checkanswer= get_answer(numberoftables,gue,pref)
        assert checkanswer == {'table_1': ['names_2', 'names_3', 'names_6', 'names_10'], 'table_2': ['names_11', 'names_13', 'names_1', 'names_10'], 'table_3': ['names_4', 'names_5', 'names_7', 'names_8', 'names_9', 'names_12', 'names_14']}," Not Expected Result!"
        print("test case 2 is passed.")
        print("\n")


    def test3(self):
        numberoftables=2
        gue=['names_1','names_2','names_3','names_4','names_5','names_6','names_7','names_8']
        pref=[
        {
            "preference": "avoid",
            "guests": [1, 2]},{
            "preference": "pair",
            "guests": [2, 3]}, {
            "preference": "avoid",
            "guests": [6, 2] }, {
            "preference": "avoid",
            "guests": [1,3,7] },
            {"preference": "avoid",
            "guests": [4,5] }
            ]
        checkanswer = get_answer(numberoftables,gue,pref)
        assert checkanswer=={'table_1': ['names_2', 'names_3', 'names_4'], 'table_2': ['names_1', 'names_5', 'names_6', 'names_7', 'names_8']},"Not as Expexted"
        print("test case 3 is passed.")
        print("\n")
    def test4(self):

        numberoftables=2
        gue=['names_1','names_2','names_3','names_4','names_5','names_6','names_7','names_8','name_9']
        pref=[]
        checkanswer = get_answer(numberoftables,gue,pref)
        assert checkanswer == {'table_1': ['names_1', 'names_2', 'names_3', 'names_4', 'names_5', 'names_6', 'names_7', 'names_8', 'name_9']},"Not As Expected."
        print("test case 4 is passed.")
        print("\n")

    def test5(self):
        numberoftables=8
        gue=['names_1','names_2','names_3','names_4','names_5','names_6','names_7','names_8']
        pref=[
        {
            "preference": "avoid",
            "guests": [1, 2]},{
            "preference": "pair",
            "guests": [2, 3]}, {
            "preference": "pair",
            "guests": [6, 3] }
            ]    
        checkanswer = get_answer(numberoftables,gue,pref)
        assert checkanswer=={'table_1': ['names_2', 'names_3', 'names_6'], 'table_2': ['names_1', 'names_4', 'names_5', 'names_7', 'names_8']},"Not as Expected."
        print("test case 5 is passed.")
        print("\n")

    def test6(self):
        numberoftables=2
        gue=['names_1','names_2','names_3','names_4','names_5','names_6','names_7','names_8']
        pref=[
        {
            "preference": "pair",
            "guests": [1, 2]},{
            "preference": "pair",
            "guests": [2, 5]}, {
            "preference": "pair",
            "guests": [6, 3] }, {
            "preference": "pair",
            "guests": [1,6,7] },{
             "preference": "pair",
            "guests": [2,7] },
            {
            "preference": "pair",
            "guests": [2,8] }

            ]
        checkanswer = get_answer(numberoftables,gue,pref)
        assert checkanswer=={'table_1': ['names_1', 'names_2', 'names_5', 'names_7', 'names_6', 'names_3', 'names_8'], 'table_2': ['names_1', 'names_1', 'names_4']}, "Not as Expected."
        print("test case 6 is passed.")
        print("\n")

    def test7(self):
        numberoftables=2
        gue=['names_1','names_2','names_3','names_4','names_5','names_6','names_7','names_8']
        pref=[
        {
            "preference": "pair",
            "guests": [1, 2]},{
            "preference": "pair",
            "guests": [2, 5]}, {
            "preference": "avoid",
            "guests": [1,3] }
            ]
        checkanswer = get_answer(numberoftables,gue,pref)
        assert checkanswer =={'table_1': ['names_1', 'names_2', 'names_5'], 'table_2': ['names_3', 'names_4', 'names_6', 'names_7', 'names_8']},"Not as Expected."
        print("test case 7 is passed.")
        print("\n")

    def test8(self):

        numberoftables=4
        gue=['names_1','names_2','names_3','names_4','names_5','names_6','names_7','names_8']
        pref=[
        {
            "preference": "pair",
            "guests": [1, 2]},{
            "preference": "pair",
            "guests": [2, 5]},{
            "preference": "pair",
            "guests": [4, 2]},{
            "preference": "pair",
            "guests": [2, 8]}
            ]

        checkanswer = get_answer(numberoftables,gue,pref)
        assert checkanswer =={'table_1': ['names_1', 'names_2', 'names_4', 'names_5', 'names_8'], 'table_2': ['names_3', 'names_6', 'names_7']},"Not as Expected"
        print("test case 8 is passed.")
        print("\n")

    def test9(self):
        numberoftables = 4
        gue=['names_1','names_2','names_3','names_4','names_5','names_6','names_7','names_8',
        'names_11','names_12','names_13','names_14','names_15','names_16','names_17','names_18',
        'names_21','names_22','names_23','names_24','names_25','names_26','names_27','names_28'
        ]
        pref=[
        {
            "preference": "pair",
            "guests": [1, 12]},{
            "preference": "pair",
            "guests": [2, 15]},{
            "preference": "pair",
            "guests": [14, 2]},{
            "preference": "pair",
            "guests": [22, 18]}
            ]
        checkanswer = get_answer(numberoftables,gue,pref)
        assert checkanswer == {'table_1': ['names_1', 'names_12'], 'table_2': ['names_2', 'names_14', 'names_15'], 'table_3': ['names_18', 'names_22'], 'table_4': ['names_3', 'names_4', 'names_5', 'names_6', 'names_7', 'names_8', 'names_9', 'names_10', 'names_11', 'names_13', 'names_16', 'names_17', 'names_19', 'names_20', 'names_21', 'names_23', 'names_24']}, 'Not as Expected.'
        print("Test case 9 is passed.")
        print("\n")

    
    def test10(self):
        numberoftables = 2
        gue=['names_1','names_2','names_3','names_4','names_5','names_6','names_7','names_8','names_9']
        pref=[
        {
            "preference": "avoid",
            "guests": [1, 2]
        },
        {
            "preference": "pair",
            "guests": [2, 3]
        },
        {
            "preference": "pair",
            "guests": [2, 6]
        },
        {
            "preference": "pair",
            "guests": [9, 3]

        },
        {
            "preference": "pair",
            "guests": [1,5]

        },
        {
            "preference": "avoid",
            "guests": [1,6,7]
        },
            {
            "preference": "avoid",
            "guests": [5, 7]

        }  ]
    
        checkanswer = get_answer(numberoftables,gue,pref)
        assert checkanswer == {'table_1': ['names_1', 'names_5', 'names_4'], 'table_2': ['names_2', 'names_3', 'names_9', 'names_6', 'names_8', 'names_7']},'Not as Expected.'
        print("Test case 10 is passed.")
        print("\n")

        
tes = testcase()
tes.test1()
tes.test2()
tes.test3()
tes.test4()
tes.test5()
tes.test6()
tes.test7()
tes.test8()
tes.test9()
tes.test10()

print("All test cases passed!")