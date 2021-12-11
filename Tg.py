import telethon.sync
from Args import args

api_id = 5265845  # <== your api id
api_hash = 'your api hash'

if args.mt_proxy:
    connection = telethon.connection.ConnectionTcpMTProxyRandomizedIntermediate
    proxy = ('proxy host',
             1212,  # <== proxy port
             'proxy secret')
else:
    connection = telethon.connection.ConnectionTcpFull
    proxy = None

client = telethon.TelegramClient(
    f'{args.config}', api_id=api_id, api_hash=api_hash,
    connection=connection,
    proxy=proxy)

client.start()
