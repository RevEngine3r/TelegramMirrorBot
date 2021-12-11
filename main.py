import Tg
import mirror
import iter_msgs
import sys
from Args import args

if args.iter_messages:
    iter_msgs.iter_msg(Tg.client)
    sys.exit(0)

mirror.run(Tg.client)

Tg.client.run_until_disconnected()
