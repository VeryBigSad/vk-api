import bot

token = '6bdbfdf13ec1c97de8e1abafe9d33b1e5fca926bff3d1b443bf6081aff0d786318a8681e4f406024a8edc' # main account
token2 = 'a1a14c65c26c673f7fc2decbefa2b9312e54522f71c30620a29043c2102598022aa6c8406e780f4796bcc' # bogban 
token3 = '9be5da3f60c330c2fc03294c99eb9d73402c94a5832fcc975a942e54e2f008281b553a8f6d32be640173d' # flex

account = bot.bot(token2, min_wait_time=60, max_wait_time= 90)

account.add_friends(1000, msg='')
