#!/usr/bin/env python
import mailbox

## custom functions

## define constants and paths
in_mbox_filename='/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash.mbox'
chat_out=mailbox.mbox('/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash_chat.mbox')
inbox_out=mailbox.mbox('/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash_inbox.mbox')
sent_out=mailbox.mbox('/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash_sent.mbox')

chat_count=0
inbox_count=0
sent_count=0
no_label_count=0

## execute functions

## separate chats from inbox messages
in_mbox = mailbox.mbox(in_mbox_filename)
for i, message in enumerate(in_mbox):
    print(message.values()[1])
    if 'X-Gmail-Labels' not in message.keys():
        no_label_count += 1
        continue
    if 'Chat' in message['X-Gmail-Labels']:
        chat_count += 1
        chat_out.add(message)
    elif 'Inbox' in message['X-Gmail-Labels']:
        inbox_count += 1
        inbox_out.add(message)
    elif 'Sent' in message['X-Gmail-Labels']:
        sent_count += 1
        sent_out.add(message)
        
print(str(i+1)+' total messages processed')
print(str(no_label_count)+' Did not have an X-Gmail-Labels label')
print('added '+str(chat_count)+' messages to chat mailbox.')
print('added '+str(inbox_count)+' messages to inbox mailbox.')
print('added '+str(sent_count)+' messages to sent mailbox.')
