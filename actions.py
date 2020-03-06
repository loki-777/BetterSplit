import json
import uuid

def quick_pay(amount, to_user, from_user):
    pass

def group_pay():
    pass

def pay():
    pass

def init_new_user(user, gpay, paytm):
    with open('profiles.json', 'r') as profiles:
        profile_dict = json.load(profiles)
    new_user = {
        'groups' : [],
        'gpay' : gpay,
        'paytm' : paytm
    }
    profile_dict[user] = new_user
    with open('profiles.json', 'w') as profiles:
        json.dump(profile_dict, profiles)

def init_new_group(user, group_name, group_members):
    group_uuid = uuid.uuid1()
    member_list = [member for member in group_members]
    member_list.append(user)
    with open('profiles.json', 'r') as profiles:
        profile_dict = json.load(profiles)
    for member in member_list:
        profile_dict[member]['groups'].append(group_uuid)
    with open('profiles.json', 'w') as profiles:
        json.dump(profile_dict, profiles)
    with open('groups.json', 'r') as groups:
        group_dict = json.load(groups)
    group_dict[group_uuid] = member_list
    with open('groups.json', 'w') as groups:
        json.dump(group_dict, groups)

def delete_group(group_uuid):
    member_list = []
    with open('groups.json', 'r') as groups:
        group_dict = json.load(groups)
    member_list = group_dict[group_uuid]
    del group_dict[group_uuid]
    with open('groups.json', 'w') as groups:
        json.dump(group_dict, groups)
    with open('profiles.json', 'r') as profiles:
        profile_dict = json.load(profiles)
    for member in member_list:
        profile_dict[member]['groups'].remove(group_uuid)
    with open('profiles.json', 'w') as profiles:
        json.dump(profile_dict, profiles)