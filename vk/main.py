import vk.bot as bot

alexandr_token       = '87b31e8112b4e8c8187dde07bb3a41e42a867dd7023f623432d7e3699e472ae85f3126821dc9af4d0bc9c'#denkin
account = bot.bot(alexandr_token)
resp=account.method('messages.getConversations', {})
print(resp.text)



