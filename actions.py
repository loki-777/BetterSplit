import json
import uuid
from flask import Flask
from models import db, UserGroup
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bettersplit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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

def init_new_group(user, group_name):
    group_uuid = str(uuid.uuid1().hex)
    print(group_name)
    new_group = UserGroup(
        name = group_name,
        uuid = group_uuid
    )
    db.session.add(new_group)
    db.session.commit()
    with open('groups.json', 'r') as groups:
        group_dict = json.load(groups)
    group_dict[group_uuid] = [user]
    with open('groups.json', 'w') as groups:
        json.dump(group_dict, groups)
    with open('profiles.json', 'r') as profiles:
        profile_dict = json.load(profiles)
    profile_dict[user]['groups'].append(group_uuid)
    with open('profiles.json', 'w') as profiles:
        json.dump(profile_dict, profiles)
    return group_uuid

def join_group(user, group_uuid):
    with open('profiles.json', 'r') as profiles:
        profile_dict = json.load(profiles)
    profile_dict[user]['groups'].append(group_uuid)
    with open('profiles.json', 'w') as profiles:
        json.dump(profile_dict, profiles)
    with open('groups.json', 'r') as groups:
        group_dict = json.load(groups)
    group_dict[group_uuid].append(user)
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

def get_groups(user):
    with open('profiles.json', 'r') as profiles:
        profile_dict = json.load(profiles)
    return profile_dict[user]['groups']

def get_members(group_uuid):
    with open('groups.json', 'r') as groups:
        group_dict = json.load(groups)
    return group_dict[group_uuid]