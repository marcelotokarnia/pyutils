import json


def convert_csv_to_json(file_input, file_output, csv_separator=','):
    def line_to_array(line):
        values = line.replace('\n', '').split(csv_separator)
        return [v[1:-1] if v.startswith('"') and v.endswith('"') else v for v in values]
    with open(file_input, 'r') as fr:
        with open(file_output, 'w') as fw:
            headers = line_to_array(fr.readline())
            for line in fr:
                fw.write((json.dumps({k: v for k, v in zip(headers, line_to_array(line)) if v}, ensure_ascii=False) + '\n'))


def convert_json_to_csv(file_input, file_output, csv_separator=','):
    with open(file_input, 'r') as fr:
        with open(file_output, 'w') as fw:
            line1 = json.loads(fr.readline())
            headers = line1.keys()
            fw.write(csv_separator.join(['"' + k + '"' for k in headers])+'\n')
            fw.write(csv_separator.join(['"' + line1[h] + '"' for h in headers])+'\n')
            for line in fr:
                data = json.loads(line)
                fw.write(csv_separator.join(['"' + data[h] + '"' for h in headers])+'\n')
