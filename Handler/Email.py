from flask import jsonify

from DAO.Email import EmailDao
from DAO.Folder import FolderDao
from DAO.User import UserDao

class EmailHandler:

    def build_email_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['eid'] = row[1]
        result['ename'] = row[2]
        result['subject'] = row[3]
        result['body'] = row[4]
        result['emailtype'] = row[5]
        result['recipientid'] = row[6]
        return result
    def build_email_count_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['eid'] = row[1]
        result['ename'] = row[2]
        result['subject'] = row[3]
        result['body'] = row[4]
        result['emailtype'] = row[5]
        result['recipientid'] = row[6]
        result['reccount'] = row[7]
        return result

    def build_email_count2_dict(self, row):
        result = {}
        result['recipientid'] = row[0]
        result['countf'] = row[1]
        return result

    def build_email_count3_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['email'] = row[1]
        result['userrecieves'] = row[2]
        return result

    def build_email_attributes(self, user_id, eid, ename, subject, body, emailtype, recipientid):
        result = {}
        result['user_id'] = user_id
        result['eid'] = eid
        result['ename'] = ename
        result['subject'] = subject
        result['body'] = body
        result['emailtype'] = emailtype
        result['recipientid'] = recipientid
        return result

    def build_email_folder_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['eid'] = row[1]
        result['ename'] = row[2]
        result['subject'] = row[3]
        result['body'] = row[4]
        result['emailtype'] = row[5]
        result['recipientid'] = row[6]
        result['folder_name'] = row[7]
        result['wasdeleted'] = row[8]
        result['wasread'] = row[9]
        result['fromfriend']= row[10]
        return result

    def getAllUsersEmails(self):
        dao = EmailDao()
        emails_list = dao.getAllUsersEmails()
        return jsonify(emails_list)


    def getUserEmailsByIDENAME(self, user_id, ename):
        dao = EmailDao()
        emails_list = dao.getUserEmailsByIDENAME(user_id, ename)
        result_list = []
        for row in emails_list:
            result = self.build_email_dict(row)
            result_list.append(result)
        return jsonify(Emails=result_list)
    def getAllUsersEmailsByID(self, user_id):
        dao = EmailDao()
        emails_list = dao.getAllUsersEmailsByID(user_id,)
        result_list = []
        for row in emails_list:
            result = self.build_email_folder_dict(row)
            result_list.append(result)
        return jsonify(Emails=result_list)


    def deleteEmail(self, user_id, eid):
        dao = FolderDao()
        check = dao.deleteFromFolder(user_id, eid)
        if check:
            return jsonify("Email was deleted successfully")
        else:
            return jsonify("Error during deletion"), 404



    def getEmailByFolderAndUserID(self, user_id, folder_name):
        dao = EmailDao()
        emails_list = dao.getEmailByFolderAndUserID(user_id, folder_name)
        result_list = []
        for row in emails_list:
            result = self.build_email_dict(row)
            result_list.append(result)
        if result_list:
            return jsonify(Emails=result_list)
        else:
            return jsonify(Error="No emails in the folder"), 404

    def createEmailJson(self, json):
        user_id = json['user_id']
        ename = json['ename']
        subject = json['subject']
        body = json['body']
        emailtype = json['emailtype']
        recipientid = json['recipientid']

        if user_id and ename and subject and body and emailtype and recipientid:
            edao = EmailDao()
            fdao = FolderDao()
            eid = edao.insertNewEmail(user_id, ename, subject, body, emailtype, recipientid)
            result = self.build_email_attributes(user_id, eid, ename, subject, body, emailtype, recipientid)

            wasdeleted = False
            wasread = False
            fromfriend = False

            draft = "Draft"

            fcheck = fdao.insertIntoFolder(user_id, eid, draft, wasdeleted, wasread, fromfriend)

            if fcheck:
                return jsonify(Email=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def readEmail(self, user_id, eid):
        dao = EmailDao()

        email = dao.getEmailInInboxByUserID(user_id, eid)
        dao.readEmail(user_id, eid)

        result_list = []

        for row in email:
            result = self.build_email_dict(row)
            result_list.append(result)
        return result_list

    def editEmail(self, user_id, eid, json):

        edao = EmailDao()
        udao = UserDao()
        fdao = FolderDao()

        premiumcheck = udao.isPremiumuser(user_id)

        ename = json['ename']
        subject = json['subject']
        body = json['body']
        emailtype = json['emailtype']
        recipientid = json['recipientid']

        if premiumcheck:
            folder = "Draft"
            foldercheck = fdao.changeFolderOutbox(user_id, eid, folder)

            editcheck = edao.editEmail(user_id, eid, ename, subject, body, emailtype, recipientid)

            if foldercheck == "Inbox":
                return jsonify("Inbox emails cannot be edited.")
            else:
                if editcheck:
                    return jsonify("Email has been edited")
                else:
                    return jsonify("Error while editing")

    def sendEmailAsReply(self, user_sent, user_to, reply_eid):
        result = FolderDao().sendReplyEmail(user_sent, user_to, reply_eid)
        if result:
            return jsonify("Reply was sent successfully")
        else:
            return jsonify(Error="Reply could not be sent"), 404

    def createReplyEmailJson(self, json):
        user_id = json['user_id']
        ename = json['ename']
        subject = json['subject']
        body = json['body']
        emailtype = json['emailtype']
        recipientid = json['recipientid']


        if user_id and ename and subject and body and emailtype and recipientid:
            edao = EmailDao()
            fdao = FolderDao()
            eid = edao.insertNewEmail(user_id, ename, subject, body, emailtype, recipientid)
            result = self.build_email_attributes(user_id, eid, ename, subject, body, emailtype, recipientid)

            wasdeleted = False
            wasread = False
            fromfriend = False
            draft = "DraftToReply"

            fcheck = fdao.insertIntoFolder(user_id, eid, draft, wasdeleted, wasread, fromfriend)

            if fcheck:
                return jsonify(Email=result), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def updateFavorites(self, user_id, eid):
        fdao = FolderDao()
        foldercheck = fdao.getFolder(user_id, eid)
        fcheck = False
        if foldercheck == "Outbox":
            favorite = "Outbox/Favorite"
            fcheck = fdao.changeFolder(user_id, eid, favorite)
        elif foldercheck == "Inbox":
            favorite = "Inbox/Favorite"
            fcheck = fdao.changeFolder(user_id, eid, favorite)
        elif foldercheck == "Replies":
            favorite = "Replies/Favorite"
            fcheck = fdao.changeFolder(user_id, eid, favorite)

        elif foldercheck == "Outbox/Favorite":
            favorite = "Outbox"
            fcheck = fdao.changeFolder(user_id, eid, favorite)
        elif foldercheck == "Inbox/Favorite":
            favorite = "Inbox"
            fcheck = fdao.changeFolder(user_id, eid, favorite)
        elif foldercheck == "Replies/Favorite":
            favorite = "Replies"
            fcheck = fdao.changeFolder(user_id, eid, favorite)
        else:
            return jsonify("Error. Could not favorite email."), 404

        if fcheck:
            if favorite == "Outbox" or favorite == "Inbox" or favorite == "Replies":
                return jsonify("Email was removed from favorites.")
            else:
                return jsonify("Email set as favorite.")
        else:
            return jsonify("Error. Could not favorite email."), 404

    def getEmailwithMostRecipients(self):
        dao = EmailDao()
        most_recipients = dao.getEmailwithMostRecipients()
        return jsonify(Email_MostRecipients=most_recipients)

    def getEmailwithMostReplies(self):
        dao = EmailDao()
        most_replies = dao.getEmailwithMostReplies()
        return jsonify(Email_MostReplies=most_replies)

    def getTop10UsersWithMoreEmailsInbox(self):
        dao = EmailDao()
        top10inbox = dao.getTop10UsersWithMoreEmailsInbox()
        return jsonify(Email_Top10Inbox=top10inbox)

    def getTop10UsersWithMoreEmailsOutbox(self):
        dao = EmailDao()
        top10outbox = dao.getTop10UsersWithMoreEmailsOutbox()
        return jsonify(Email_Top10Outbox=top10outbox)

    def getUsersEmailMostRecipients(self, user_id):
        dao = EmailDao()
        emails_list = dao.getUsersEmailMostRecipients(user_id)
        result_list = []
        for row in emails_list:
            result = self.build_email_count_dict(row)
            result_list.append(result)
        return jsonify(EmailMostRecipient=result_list)

    def getUsersEmailMostReplies(self, user_id):
        dao = EmailDao()
        emails_list = dao.getUsersEmailMostReplies(user_id)
        result_list = []
        for row in emails_list:
            result = self.build_email_count_dict(row)
            result_list.append(result)
        return jsonify(EmailMostReplies=result_list)

    def getTop5UsersYouSend(self, user_id):
        dao = EmailDao()
        emails_list = dao.getTop5UsersYouSend(user_id)
        result_list = []
        for row in emails_list:
            result = self.build_email_count2_dict(row)
            result_list.append(result)
        return jsonify(EmailTop5Send=result_list)

    def getTop5UsersYouRecieve(self, user_id):
        dao = EmailDao()
        emails_list = dao.getTop5UsersYouRecieve(user_id)
        result_list = []
        for row in emails_list:
            result = self.build_email_count3_dict(row)
            result_list.append(result)
        return jsonify(EmailTop5Recieve=result_list)