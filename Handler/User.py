from flask import jsonify
from DAO.User import UserDao

class UserHandler:
    def build_user_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['firstname'] = row[1]
        result['lastname'] = row[2]
        result['phone_number'] = row[3]
        result['date_of_birth'] = row[4]
        result['email'] = row[5]
        result['password'] = row[6]
        result['premiumuser'] = row[7]
        result['isfriend'] = row[8]
        return result


    def build_email_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['eid'] = row[1]
        result['ename'] = row[2]
        result['subject'] = row[3]
        result['body'] = row[4]
        result['emailtype'] = row[5]
        result['isread'] = row[6]
        result['wasdeleted'] = row[7]
        result['recipientid'] = row[8]
        return result

    def build_folder_dict(self, row):
        result = {}
        result['folderid'] = row[0]
        result['user_id'] = row[1]
        result['eid'] = row[2]
        result['fdname'] = row[3]
        return result

    def build_user_attributes(self, user_id, firstname, lastname, phone_number, date_of_birth, email, password,
                              premiumuser, isfriend):
        result = {}
        result['user_id'] = user_id
        result['firstname'] = firstname
        result['lastname'] = lastname
        result['phone_number'] = phone_number
        result['date_of_birth'] = date_of_birth
        result['email'] = email
        result['password'] = password
        result['premiumuser'] = premiumuser
        result['isfriend'] = isfriend
        return result

    def getAllUsers(self):
        dao = UserDao()
        users_list = dao.getAllUsers()
        result_list = []
        for row in users_list:
            result = self.build_user_dict(row)
            result_list.append(result)
        return jsonify(Users=result_list)

    def getAllUsersEmails(self):
        dao = UserDao()
        emails_list = dao.getAllUsersEmails()
        return jsonify(emails_list)

    def getAllFolders(self):
        dao = UserDao()
        folder_list = dao.getAllFolders()
        result_list = []
        for row in folder_list:
            result = self.build_folder_dict(row)
            result_list.append(result)
        return jsonify(Folders=result_list)

    def addNewUser(self, form):
        print("form: ", form)
        if len(form) != 8:
            return jsonify(Error="Malformed post request"), 400
            firstname = form['firstname']
            lastname = form['lastname']
            phone_number = form['phone_number']
            date_of_birth = form['date_of_birth']
            email = form['email']
            password = form['password']
            premiumuser = form['premiumuser']
            isfriend = form['isfriend']
            if firstname and lastname and phonenumber and date_of_birth and \
                    email and password and premiumuser and isfriend:
                dao = UserDao()
                user_id = dao.insertNewUser(firstname, lastname, phonenumber,
                                            date_of_birth, email, password, premiumuser,isfriend)

                result = self.build_user_attributes(user_id, firstname, lastname, phonenumber, date_of_birth,
                                                    email, password, premiumuser, isfriend)
                json["user_id"] = user_id
                return jsonify(json), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400


    def addNewUserJson(self, json):
        firstname = json['firstname']
        lastname = json['lastname']
        phone_number = json['phone_number']
        date_of_birth = json['date_of_birth']
        email = json['email']
        password = json['password']
        premiumuser = json['premiumuser']
        isfriend = json['isfriend']

        if firstname and lastname and phone_number and date_of_birth and email and password and premiumuser and isfriend:
            dao = UserDao()
            user_id = dao.insertNewUser(firstname, lastname, phone_number, date_of_birth, email, password, premiumuser, isfriend)
            result = self.build_user_attributes(user_id, firstname, lastname, phone_number, date_of_birth, email, password, premiumuser, isfriend)
            return jsonify(User=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400



    def getUserEmailsByIDENAME(self, user_id, ename):
        dao = UserDao()
        emails_list = dao.getUserEmailsByIDENAME(user_id, ename)
        result_list = []
        for row in emails_list:
            result = self.build_email_dict(row)
            result_list.append(result)
        return jsonify(Emails=result_list)

    def deleteEmail(self, user_id, ename):
        dao = UserDao()
        if not dao.getUserEmailsByIDENAME(user_id, ename):
            return jsonify(Error = "Email not found."), 404
        else:
            dao.deleteEmail(user_id, ename)
            return jsonify(DeleteStatus = "OK"), 200

    def build_email_attributes(self, user_id, eid, ename, subject, body, emailtype, isread, wasdeleted, recipientid):
        result = {}
        result['user_id'] = user_id
        result['eid'] = eid
        result['ename'] = ename
        result['subject'] = subject
        result['body'] = body
        result['emailtype'] = emailtype
        result['isread'] = isread
        result['wasdeleted'] = wasdeleted
        result['recipientid'] = recipientid
        return result

    def createEmailJson(self, json):
        user_id = json['user_id']
        ename = json['ename']
        subject = json['subject']
        body = json['body']
        emailtype = json['emailtype']
        isread = json['isread']
        wasdeleted = json['wasdeleted']
        recipientid = json['recipientid']

        if user_id and ename and subject and body and emailtype and isread and wasdeleted and recipientid:
            dao = UserDao()
            eid = dao.insertNewEmail(user_id, ename, subject, body, emailtype, isread, wasdeleted, recipientid)
            result = self.build_email_attributes(eid, user_id, ename, subject, body, emailtype, isread, wasdeleted, recipientid)
            return jsonify(Email=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400