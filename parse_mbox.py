#!/usr/bin/env python
import mailbox

## custom functions

## define constants and paths
in_mbox_filename='/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash_head.mbox'
chat_out=mailbox.mbox('/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash_head_chat.mbox')
inbox_out=mailbox.mbox('/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash_head_inbox.mbox')
sent_out=mailbox.mbox('/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash_head_sent.mbox')

chat_count=0
inbox_count=0
sent_count=0

## execute functions

## separate chats from inbox messages
in_mbox = mailbox.mbox(in_mbox_filename)
for i, message in enumerate(in_mbox):
    print(message.values()[1])
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
print('added '+str(chat_count)+' messages to chat mailbox.')
print('added '+str(inbox_count)+' messages to inbox mailbox.')
print('added '+str(sent_count)+' messages to sent mailbox.')
