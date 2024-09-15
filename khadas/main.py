import argparse

from config import *
from tools import *
from mqtt import get_client, subscribe

import os

def loop_default(client, userdata, msg):
    data = msg.payload.decode()
    data = convert_data_str_int(data, threshold=True)
    print(data)

def get_data(client, userdata, msg, letter='a', id=1):
    data = msg.payload.decode()
    data = convert_data_str_int(data, threshold=True)

    os.makedirs(os.path.join('data', letter), exist_ok=True)

    save_data(data, filepath=os.path.join('data', letter, f'{letter}-{id}.txt'))
    print(data)

if __name__ == '__main__':
    # Setup argument parsing
    parser = argparse.ArgumentParser(description='Get data and save it.')
    parser.add_argument('--fn', type=str, default='loop_default', help='Specify the function')
    parser.add_argument('--letter', type=str, default='a', help='Letter used for the directory and filename.')
    parser.add_argument('--id', type=int, default=1, help='ID used for the filename.')

    # Parse arguments
    args = parser.parse_args()

    client = get_client(client_id=CLIENT_ID, username=USERNAME, password=PASSWORD, broker=BROKER, port=PORT)

    if (args.fn == 'get_data'):
        print(f'Saving the data into data/{args.letter}-{args.id}.txt')
        subscribe(client, topic=TOPIC, loop=lambda client, userdata, message: get_data(client, userdata, message, letter=args.letter, id=args.id))
    else :
        subscribe(client, topic=TOPIC, loop=loop_default)

    client.loop_forever()

