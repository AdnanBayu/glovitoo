import argparse

from config import *
from tools import *
from mqtt import get_client, subscribe

import os
from datetime import datetime
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
time = datetime.now()

model = SIBIRNNModel(20, 20, 3, 26).to(device)


def loop_default(client, userdata, msg):
    data = msg.payload.decode()
    data = convert_data_str_int(data, threshold=True)
    print(data)


def get_data(client, userdata, msg, letter='a', id=1):
    data = msg.payload.decode()
    data = convert_data_str_int(data, threshold=True)

    os.makedirs(os.path.join('data', letter), exist_ok=True)

    save_data(data, filepath=os.path.join(
        'data', letter, f'{letter}-{id}.txt'))
    print(data)


def predict(client, userdata, msg, seq_len=20):
    data = msg.payload.decode()
    data = convert_data_str_int(data, threshold=True)
    print(data)

    save_data(data, filepath=f'predict-{time}.txt')

    data_from_txt = read_data(filepath=f'predict-{time}.txt')
    current_len_data = len(data_from_txt)
    print(f'LAST{len(data_from_txt[-1].split(", "))}')
    if current_len_data >= 20 and len(data_from_txt[-1].split(', ')) == 11:
        data_torch = convert_data_str_torch(
            data_from_txt, threshold=False, seq_len=seq_len, id=current_len_data-seq_len)
        print(data_torch.shape)
        out = model(data_torch)
        print(chr(torch.argmax(out).item() + 97))

if __name__ == '__main__':
    # Setup argument parsing
    parser = argparse.ArgumentParser(description='Get data and save it.')
    parser.add_argument(
        '--fn', type=str, default='loop_default', help='Specify the function')
    parser.add_argument('--letter', type=str, default='a',
                        help='Letter used for the directory and filename.')
    parser.add_argument('--id', type=int, default=1,
                        help='ID used for the filename.')
    parser.add_argument('--seq_len', type=int, default=20,
                        help='Sequence len gesture data for prediction')

    # Parse arguments
    args = parser.parse_args()

    client = get_client(client_id=CLIENT_ID, username=USERNAME,
                        password=PASSWORD, broker=BROKER, port=PORT)

    if (args.fn == 'get_data'):
        print(f'Saving the data into data/{args.letter}-{args.id}.txt')
        subscribe(client, topic=TOPIC, loop=lambda client, userdata, message: get_data(
            client, userdata, message, letter=args.letter, id=args.id))
    
    elif (args.fn =='predict'):
        print(f'Saving the data into predict-{time}.txt')
        subscribe(client, topic=TOPIC, loop=lambda client, userdata, message: predict(
            client, userdata, message, seq_len=args.seq_len))
    
    else:
        subscribe(client, topic=TOPIC, loop=loop_default)

    client.loop_forever()
