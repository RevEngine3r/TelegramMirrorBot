import time
import Config as Cfg


def iter_msg(client):
    fw_list = []
    rm_list = []

    msg_limit = 5000
    msg_id = 0

    while True:
        for message in client.iter_messages(entity=Cfg.out_id, limit=msg_limit, offset_id=msg_id):
            # print(message)
            print('===')

            msg_id = message.id

            if msg_id <= 1:
                print('all done.')
                return

            try:
                fw_id = message.fwd_from.channel_post
            except Exception as ex:
                print(ex)
                continue

            print(f'{msg_id=}, {fw_id=}')
            print(f'{len(fw_list)=}, {len(rm_list)=}')

            if fw_id in fw_list:
                rm_list.append(msg_id)
                print('added to rm_list.')
            else:
                fw_list.insert(0, fw_id)
                print('added to fw_list.')

        client.delete_messages(entity=Cfg.out_id, message_ids=rm_list)
        print(f'deleted {len(rm_list)} messages.')
        rm_list = []

        time.sleep(3)
