import telethon.sync
import Config as Cfg
import time
import json
import pathlib
from Args import args
import RevUtils.Logger as RLog
import sys

RLog.init_logger(args.config)

config = {"in_id": None, "out_id": None}
config_file = pathlib.Path(f'{args.config}.json')

msg_map = {}
msg_map_file = pathlib.Path(f'{args.config}.map.json')


def load(file):
    RLog.info('load()...')

    if file.is_file():
        return json.loads(file.read_text())
    return False


def save(file, obj):
    RLog.info('save()...')
    file.write_text(json.dumps(obj))


def save_config():
    global config, config_file

    RLog.info('save_config()...')
    save(config_file, config)


def load_config():
    global config, config_file

    RLog.info('load_config()...')
    if config_file.is_file():
        config = load(config_file)
    else:
        save_config()

    Cfg.in_id = config['in_id']
    Cfg.out_id = config['out_id']

    if (Cfg.in_id is None) or (Cfg.out_id is None):
        RLog.info('invalid config, exiting...')
        sys.exit(0)


def load_map():
    global msg_map, msg_map_file

    RLog.info('load_map()...')
    tmp = msg_map.copy()
    for key, val in tmp.items():
        msg_map[int(key)] = val

    if msg_map_file.is_file():
        msg_map = load(msg_map_file)
    else:
        save_map()


def save_map():
    global msg_map, msg_map_file

    RLog.info('save_map()...')

    tmp = msg_map.copy()

    for key, val in tmp.items():
        tmp[key] = val.id

    save(msg_map_file, tmp)


def is_bot(event):
    if event.message.via_bot_id or (event.__str__().find('t.me/zekrm/') > -1):
        RLog.info('its bot...')
        return True
    return False


async def get_valid_msgs(client: telethon.TelegramClient):
    RLog.info('check_msg_ids()...')

    keys = list(msg_map.keys())
    values = list(msg_map.values())

    key_msgs = await client.get_messages(entity=Cfg.in_id, ids=keys)
    time.sleep(3)
    value_msgs = await client.get_messages(entity=Cfg.out_id, ids=values)

    for i in range(len(keys)):
        if not key_msgs[i]:
            msg_map.pop(keys[i], None)
        else:
            msg_map[keys[i]] = value_msgs[i]

    save_map()


def run(client: telethon.TelegramClient):
    global msg_map

    load_config()
    load_map()

    client.loop.run_until_complete(get_valid_msgs(client))
    RLog.info(f'{msg_map=}')

    @client.on(telethon.events.NewMessage(chats=Cfg.in_id))
    async def new_message_listener(event: telethon.events.NewMessage.Event):
        RLog.info('new_message_listener...')

        channel_post = event.message.id

        RLog.info(event)
        RLog.info(f'{channel_post=}')

        if event.message.message is None:
            event.message.message = ''

        event.message.message += f'\n\n{channel_post}'

        msg = await client.send_message(entity=Cfg.out_id, message=event.message)

        if not is_bot(event):
            msg_map[channel_post] = msg
            save_map()

        time.sleep(1)

    @client.on(telethon.events.MessageEdited(chats=Cfg.in_id))
    async def message_edited_listener(event: telethon.events.MessageEdited.Event):
        RLog.info('message_edited_listener...')

        RLog.info(event)

        if is_bot(event):
            return

        if event.message.message is None:
            event.message.message = ''

        channel_post = event.message.id
        event.message.message += f'\n\n{channel_post}'

        if event.message.media:
            RLog.info(f'media message...')
            await new_message_listener(event)
        else:
            try:
                msg: telethon.types.Message = msg_map[channel_post]
            except Exception as ex:
                await new_message_listener(event)
                RLog.info(ex)
                return

            if msg.message != event.message.message:
                msg = await client.edit_message(entity=Cfg.out_id, message=str(msg.id), text=event.message.message)
                msg_map[channel_post] = msg

        time.sleep(1)

    @client.on(telethon.events.MessageDeleted(chats=Cfg.in_id))
    async def message_deleted_listener(event: telethon.events.MessageDeleted.Event):
        RLog.info('message_deleted_listener...')
        RLog.info(event)

        for msg_id in event.deleted_ids:
            msg_map.pop(msg_id, None)

        save_map()
