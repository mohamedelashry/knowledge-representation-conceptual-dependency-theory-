from nltk import word_tokenize
corpora = {'table':'loc','go':'act','run':'act','put':'act','school':'loc','home':'loc','room':'loc','kitchen':'loc','book':'pp','give':'act','take':'act','buy':'act','johan':'PP' , 'hit':'act' ,'mary':'PP' , 'throwing': 'act','throwed':'act' , 'throw' :'act' , 'stick':'pp' }
temp_pp_o =[" "]
# CD primitives  action
A_trans = ["give","take","buy"]                       # transfer of an abstract relationship   .
A_trans_mine=["give"]
A_trans_your=["take","buy"]
P_trans =["go","put","run"]                             # transfer of physical location of object .
propel = ["hit" , "push","pull"]     # application of physical force to an  object .
grasp = ["clutch","hold","throwing"]             # actor grasping an object .
move = ["throwing","kick","raise","run","go","put" , "push","pull","throw"]
foot_move = ["kick" , "walk" , "shoot","run","go"]
hand_move = ["puch" ,"throw","wave","throwing","raise","put" ]

#ex_text = "johan hit mary by throwing a stick at her ."
ex_text = " mary run from home  to school ."
tokey=word_tokenize(ex_text)
tokens=[]
for token in tokey :
    tokens.append(token)
def _Atrans(to):
       # rule 5 ::: describe the relationship of two PP  one which provides
       #              a particular kind of information about the other .
      # examples ::
      # johan give  mary  a book   ----
      # mary take abook  from johan  -----
      # johan buy  a book  to  mary ---
      #
      # catch subject
    ID = tokens.index(to)
    subject = object = o_subject ="null"
    bID = ID-1
    while (bID >= 0):
        if tokens[bID] in corpora and corpora[tokens[bID]] == 'PP':
            if tokens[bID] not in temp_pp_o:
                subject = tokens[bID]
                break
        bID -= 1
    ID+=1
     #catch object  and   pre_owner
    while ( object =="null"  or o_subject =="null"):
        if tokens[ID] in corpora and corpora[tokens[ID]] == 'PP':
            o_subject =tokens[ID]
        elif tokens[ID] in corpora and corpora[tokens[ID]] == 'pp':
            object =tokens[ID]
        ID+=1

    if to in A_trans_your:
       print("previously "+object +" poss by "+o_subject)
       print("now " + object + " poss by "+ subject)
    else:
        print("previously " + object + " poss by " + subject)
        print("now " + object + " poss by " + o_subject)

    return
def _Ptrans(to):
    # rule 1 ::: describe the relationship between actor the event he/she
    #               causes .
    # examples ::
    # johan  go   from home to school  ----
    # mary run from kitchen to room   -----
    # johan put a book at table  ---
    #
    # catch subject
    ID = tokens.index(to)
    subject = pos_1 = pos_2 = "null"
    bID = ID - 1
    while (bID >= 0):
        if tokens[bID] in corpora and corpora[tokens[bID]] == 'PP':
            if tokens[bID] not in temp_pp_o:
                subject = tokens[bID]
                break
        bID -= 1
    ID += 1
    # catch  preposition  and  current position
    while (pos_1 == "null" or pos_2 == "null"):
        if tokens[ID] in corpora and corpora[tokens[ID]] == 'loc' and tokens[ID-1]=="from":
            pos_1 = tokens[ID]
        elif tokens[ID] in corpora and corpora[tokens[ID]] == 'loc' and (tokens[ID-1]=="to"or tokens[ID-1]=="at"):
            pos_2 = tokens[ID]
        ID += 1


    print(subject+" move from "+pos_1 +" to "+pos_2)
    return
def _Propel (to):
    # rule 6 ::: describe the relationship between actor and  pp .
    # examples ::
    # johan hit   mary  by  book   ----
    # mary push a book  to johan  -----
    # johan pull  a book  from  mary ---
    # johan throw stick to mary
    # catch subject
    ID = tokens.index(to)
    subject = object = p_object = "null"
    bID = ID - 1
    while (bID >= 0):
        if tokens[bID] in corpora and corpora[tokens[bID]] == 'PP':
            if tokens[bID] not in temp_pp_o:
                subject = tokens[bID]
                break
        bID -= 1
    ID += 1
    # catch object  and  receiver
    while (tokens[ID]!="."):
       if tokens[ID] in corpora and corpora[tokens[ID]]=='PP':    #  person
           p_object = tokens[ID]
           temp_pp_o.append(p_object)
       elif tokens[ID] in corpora and corpora[tokens[ID]]== 'pp':  # object
           object = tokens[ID]
       ID+=1
    print(subject + " propel " +object+" towards "+ p_object )
    return
def _Grasp(to):
    ID = tokens.index(to)
    subject = object = ""
    bID = ID-1
    while (bID >= 0):
        if tokens[bID] in corpora and corpora[tokens[bID]] == 'PP':
            if tokens[bID] not in temp_pp_o:
                subject = tokens[bID]
                break
        bID -= 1
    # catch object
    while (tokens[ID]!='.'):
        if tokens[ID] in corpora and corpora[tokens[ID]] == 'pp':
            object =tokens[ID]
            break
        ID+=1
    print(subject+" grasp "+ object)

    return
def _move (to):
    # the movement of  a body partof an animal by that animal  .
    # we handle two kind of movement by hand  and foot .
    # examples ::
    #
    ID = tokens.index(to)
    subject = object =recipt= ""
    bID = ID - 1
    while (bID >= 0):
        if tokens[bID] in corpora and corpora[tokens[bID]] == 'PP':
            if tokens[bID] not in temp_pp_o:
                subject = tokens[bID]
                break
        bID -= 1
    # catch object
    if object=="":
            while (tokens[ID] != "."):
                ID += 1
                if tokens[ID] in corpora and corpora[tokens[ID]] == 'PP':  # person
                    object = tokens[ID]
                    #temp_pp_o.append(object)
                    break
                elif tokens[ID] in corpora and corpora[tokens[ID]] == 'pp':  # object
                    object = tokens[ID]
                    ID += 1
                    while (tokens[ID] != "."):
                        if tokens[ID] in corpora and corpora[tokens[ID]] == 'PP':  # towards person
                            recipt = tokens[ID]
                            break
                        elif tokens[ID] in corpora and corpora[tokens[ID]] == 'PP':  # towards location
                            recipt = tokens[ID]
                            break
                        ID += 1
                    break  # ------------------------------
                else:
                    while (tokens[ID] != "."):
                        if tokens[ID] in corpora and corpora[tokens[ID]] == 'loc':  # location
                            recipt = tokens[ID]
                        ID += 1
                    break  # ------------------------
    if to in foot_move :
        print(subject+" move foot toward  "+ recipt + object+temp_pp_o[len(temp_pp_o)-1])
    else:
        print(subject+" move hand toward  "+ recipt + object +temp_pp_o[(len(temp_pp_o)-1)])
    return

for tok in tokens:
    if tok in corpora and  corpora[tok] =='act' :
       if tok in propel  : _Propel(tok)
       if tok in move  : _move(tok)
       if tok in grasp : _Grasp(tok)
       if tok in P_trans:_Ptrans(tok)
       if tok in A_trans :_Atrans(tok)







