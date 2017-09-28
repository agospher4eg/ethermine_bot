import get_data_from_ethermine, json
filename = "data.json"
user_dict={}

try:
    fh= open(filename, encoding="utf-8")
    user_dict = json.loads(fh.read())
    print('user_dict: ',user_dict)
except FileNotFoundError:
    print('there is no file, user_dict is empty')

def add_to_user_dict(tele_id,value):
    value=value.strip()
    error = 0
    tele_id=str(tele_id)
    global user_dict
    if get_data_from_ethermine.get_new_info(value)[2].strip()=='OK':
        first_responce='good token'
        if user_dict.get(tele_id)==None:
            user_dict[tele_id]=[value]
            second_responce='new key: {} the value was added: {}'.format(tele_id, value)
        else:
            for i in range(0,len(user_dict[tele_id])):
                if user_dict[tele_id][i]==value:
                    error=1
            if error==0:
                user_dict[tele_id].append(value)
                second_responce='existed key: {} the value was added: {}'.format(tele_id,value)
            else:
                second_responce='existed key: {} existed value {}'.format(tele_id,value)
    else:
        first_responce='bad token'
    return('{},{}'.format(first_responce,second_responce))

def write_to_json(tele_id,value):
    try:
        resp=add_to_user_dict(tele_id,value)
        #print(resp)
        fh=open(filename, "w", encoding="utf-8")
        fh.write(json.dumps(user_dict, ensure_ascii=False, indent=4))
        fh.close()
    except UnicodeEncodeError:
        resp='check your token'
        #print(resp)
    return(resp)

