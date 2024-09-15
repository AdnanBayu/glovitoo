def convert_data_str_int(data, threshold=False):
    data = data.split(',')

    if threshold :
        flex_data = [round(apply_threshold(float(x), 2700, 3600), 2) for x in data[:5]]
    else :
        flex_data = data[:5]

    data = flex_data + data[8:-2] + [data[-1].strip()]
    data = [float(x) for x in data]
    data = ', '.join([str(x) for x in data])
    return data

def apply_threshold(val, bottom=0, top=4000):
    return (val - bottom)/(top - bottom)

def save_data(data, filepath='test.txt'):
    with open(filepath, 'a') as f:
        f.write(data + '\n')

def read_data(filepath):
    with open(filepath, 'r') as f:
        data = f.read().splitlines()
        return data

if __name__ == '__main__':
    data = read_data('./data/a/a-1.txt')
    data = [convert_data_str_int(x) for x in data]
    print(data)
