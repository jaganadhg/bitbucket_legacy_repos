import re
import mailbox
from pymongo import MongoClient


def clean(text):
	text_spl = text.split("\n")
	splitted = [ l for l in text_spl if not l.startswith(">") and \
	not l.endswith("wrote:") and len(l) > 0]
	return " ".join(splitted)

def get_multi_payload(msg):
	content = ""
	for part in msg.walk():
		if part.get_content_type() == "text/plain":
			content = part.get_payload()
			break
	return content

def name_mail(email_string):
	name = ""
	mail = ""
	name_mail = re.search('(.*)\<(.*)\>',email_string)
	if name_mail:
		name = name_mail.group(1).strip()
		mail = name_mail.group(2).strip()

	return name,mail

def mbox_to_mongo(mboxfile,mongodetails):
	mbox = mailbox.mbox(mboxfile)
	for msg_ in mbox.keys():
		msg = mbox[msg_]
		mbox_doc = {}
		if msg.is_multipart():
			mbox_doc['Original'] = repr(get_multi_payload(msg)).decode('utf8')
			mbox_doc['OriginalClean'] = repr(clean(get_multi_payload(msg))).decode('utf8')
		else:
			mbox_doc['Original'] = repr(msg.get_payload()).decode('utf8')
			mbox_doc['OriginalClean'] = repr(clean(msg.get_payload())).decode('utf8')
		name,mail = name_mail(msg['From'])
		mbox_doc['Name'] = name
		mbox_doc['Email'] = mail
		mbox_doc['Subject'] = msg['Subject']
		mbox_doc['Date'] = msg['Date']
		mbox_doc['In-Reply-To'] = msg['In-Reply-To']
		mbox_doc['Message-ID'] = msg['Message-ID']
		mongodetails.insert(mbox_doc)

if __name__ == "__main__":
	client = MongoClient('Maya', 27017)
	database = client["mbox_test"]
	mbcol = database['precommit']
	mbox_to_mongo("201212.mbox",mbcol)

		
	
