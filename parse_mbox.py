#!/usr/bin/env python

import mailbox
import re
import time
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import ggplot

## custom functions
def split_mbox(in_mbox_filename, chat_out, inbox_out, sent_out):
    print('Entering split_mbox @ '+time.strftime("%H:%M:%S"))
    chat_count=0    
    inbox_count=0
    sent_count=0
    no_label_count=0    
    in_mbox = mailbox.mbox(in_mbox_filename)
    for i, message in enumerate(in_mbox):
        # print(message.values()[1])
        if 'X-Gmail-Labels' not in message.keys():
            no_label_count += 1
            continue
        if message['X-Gmail-Labels'] == 'Chat':
            chat_count += 1
            chat_out.add(message)
        elif 'Inbox' in message['X-Gmail-Labels'] and 'Chat' not in message['X-Gmail-Labels']:
            inbox_count += 1
            inbox_out.add(message)
        elif 'Sent' in message['X-Gmail-Labels'] and 'Chat' not in message['X-Gmail-Labels']:
            sent_count += 1
            sent_out.add(message)
        
    print(str(i+1)+' total messages processed @ '+time.strftime("%H:%M:%S"))
    print(str(no_label_count)+' Did not have an X-Gmail-Labels label')
    print('added '+str(chat_count)+' messages to chat mailbox.')
    print('added '+str(inbox_count)+' messages to inbox mailbox.')
    print('added '+str(sent_count)+' messages to sent mailbox.')
    
    return() 


## define constants and paths
in_mbox_filename='/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash.mbox'
chat_out=mailbox.mbox('/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash_chat.mbox')
inbox_out=mailbox.mbox('/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash_inbox.mbox')
sent_out=mailbox.mbox('/Users/olga/Documents/google_mail_archive_07062015/data/All_mail_Including_Spam_and_Trash_sent.mbox')



## execute functions

## separate chats from inbox messages
#split_mbox(in_mbox_filename, chat_out, inbox_out, sent_out)

## inventory message into dataframe
print('Entering mbox_inventory @ '+time.strftime("%H:%M:%S"))
   
multipart_count = 0
append_index = 0
columns=['key','sender', 'recepient', 'payloadCharCount', 'dateTime', 'multipart','partCount']
message_df=pd.DataFrame(data=np.zeros((0, len(columns))), columns=columns)
#mbox = mailbox.mbox(in_mbox_filename)
mbox=inbox_out
for j, message in enumerate(mbox):
    #if j > 1000: break
    if message.is_multipart() is False:
        message_df.loc[message_df.shape[0]]=[j, message['From'], message['To'], len(message.get_payload()), message['Date'], 0,0]
        append_index +=1
        
    else: # inventory only the first part of a multi-part message
        message_df.loc[message_df.shape[0]]= [j, message['From'], message['To'], len(message.get_payload()[0].get_payload()), message['Date'], 1, len(message.get_payload())]
        append_index +=1
        multipart_count += 1
        
        continue
## save message_df to file
message_df.to_csv('/Users/olga/Documents/google_mail_archive_07062015/output/inbox_message_df.txt')
    
    
## plot # of messages sent/received as a function of non-olga party
plot_df=pd.DataFrame(message_df.sender.value_counts())
plot_df.index.name='value'
plot_df.reset_index(inplace=True)
plot_df.rename(columns={0:'count'}, inplace=True)
plot_df=plot_df.head(15)

## ggplot
p = ggplot(plot_df, aes(x='value', y='count')) + \
    geom_bar(stat="bar", labels = plot_df['value'].tolist()) + \
    theme(axis_text_x=element_text(angle=90, hjust=1))
print p    

## seaborn
sns.set_style("darkgrid")
bar_plot = sns.barplot(x=plot_df['value'],y=plot_df['count'],
                        palette="muted",
                        x_order=plot_df['value'].tolist())
plt.xticks(rotation=90)
plt.show()

plot_df.plot("value", "count", kind="barh", color=sns.color_palette("deep",3))

## things to remember
"""

sent_out[1].is_multipart() will return true if the email is a nested message
sent_out[1].get_payload()[0].get_payload() gets payload of 1st sub-message of the conversation

remove <...> tags from html-containing messages
re.sub('<[^<]+?>','',sent_out[3].get_payload()[1].get_payload())

remove other crap:
sent_out[3].get_payload()[1].get_payload().replace('&nbsp;','').replace('=\r\n','').replace('\r','').replace('\n','').replace('&gt;','').replace('&lt','')

"""
