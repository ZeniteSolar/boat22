#!/usr/bin/env python3
import json
import sys
import glob
import os
import itertools
from timeit import default_timer as timer
import pandas
import vaex


def parse_row(row):
    # ex. row = "(1580415599.609366) can0 011#E4360F0000780216"
    try:
        timestamp, interface, msg = row.split()
        timestamp = float(timestamp[1:-1])
        if timestamp > 1670000000:
            return None
        topic_id = int(msg[0:3], 16)
        payload = bytes.fromhex(msg[4:])
        return None if (len(payload) > 8) else {
            'timestamp': timestamp,
            'interface': interface,
            'topic_id': topic_id,
            'payload': payload
        }
    except Exception as error:
        print(f"Warning: fail to parse row: {row}. Ignoring... error:", error)
        return None


def load_can_ids(filename: str, verbose=False):
    try:
        with open(filename) as schema_file:
            schema = json.load(schema_file)

            if(verbose):
                print(f'Loaded {len(schema["modules"])} modules:')
                for i, _ in enumerate(schema['modules']):
                    print(
                        f'\t{schema["modules"][i]["name"]}({schema["modules"][i]["signature"]})')
                print('')

            return schema
    except Exception as error:
        sys.stderr.write('Failed loading CAN IDS: %s\n' % (str(error)))
        sys.exit(1)


def find_module(schema: list, parsed_signature: bytearray):
    return next((module for module in schema['modules'] if module['signature'] == parsed_signature), None)


def find_topic(module: list, parsed_topic_id: bytearray):
    return next((topic for topic in module['topics'] if topic['id'] == parsed_topic_id), None)


def interpret_payload(topic, parsed_payload):
    payload_data_list = []

    try:
        for b, byte in enumerate(topic['bytes'][1:]):
            if byte is not None:
                parsed_byte_type = byte['type']
                parsed_byte_units = byte['units']
                parsed_byte_name = byte['name']

                if parsed_byte_type == 'u8':
                    parsed_byte_data = parsed_payload[b]
                elif parsed_byte_type == 'u16':
                    if parsed_byte_name[-2:] == '_H':
                        continue
                    parsed_byte_name = parsed_byte_name[:-2]
                    parsed_byte_data = (parsed_payload[b]) + (parsed_payload[b + 1] * 256)
                elif parsed_byte_type == 'bitfield':
                    for parsed_bit, parsed_bit_name in enumerate(byte['bits']):
                        if parsed_bit_name is not None:
                            parsed_byte_data = (parsed_payload[b] >> parsed_bit) & 1

                            parsed_dict = {
                                "byte_name": parsed_byte_name + parsed_bit_name,
                                "data": parsed_byte_data,
                                "unit": ''
                            }
                            payload_data_list += [parsed_dict]
                    continue
                else:
                    print("FAIL!")
                    print(topic)
                    print(parsed_payload)
                    continue

                if parsed_byte_units == '%':
                    parsed_byte_scale = 1 / 255
                    parsed_byte_data *= parsed_byte_scale
                else:
                    if parsed_byte_units != '':
                        parsed_byte_units = ["".join(x) for _, x in itertools.groupby(
                            parsed_byte_units, key=str.isdigit)]
                        parsed_byte_scale = 1 / \
                            float(
                                parsed_byte_units[1])
                        parsed_byte_units = parsed_byte_units[0].replace(
                            '/', '')
                        parsed_byte_data *= parsed_byte_scale

                parsed_dict = {
                    "byte_name": parsed_byte_name,
                    "data": parsed_byte_data,
                    "unit": parsed_byte_units
                }
                payload_data_list += [parsed_dict]
    except Exception as e:
        sys.stderr.write('Error: %s\n' % (str(e)))
        print('bug! topic:', topic, ', parsed_payload:', parsed_payload)
        payload_data_list = None

    return payload_data_list


def process_row(row):
    try:
        parsed = parse_row(row)
        if (parsed is None):
            return None

        parsed_timestamp = parsed['timestamp']
        parsed_signature = parsed['payload'][0]
        parsed_payload = parsed['payload'][1:]
        parsed_topic_id = parsed['topic_id']

        module = find_module(schema, parsed_signature)
        if (module is None):
            # todo: print here debug information about this case
            return None
        parsed_module_name = module['name']
    #     parsed_module_description = module['description']

        topic = find_topic(module, parsed_topic_id)
        if (topic is None):
            # todo: print here debug information about this case
            return None
        parsed_topic_name = topic['name']
    #     parsed_topic_description = topic['description']

        parsed_data_dict_list = interpret_payload(topic, parsed_payload)
        if (parsed_data_dict_list is None):
            # todo: print here debug information about this case
            return None

        timestamp_list = []
        module_name_list = []
        topic_name_list = []
        byte_name_list = []
        data_list = []
        unit_list = []

        for parsed_data_dict in parsed_data_dict_list:
            timestamp_list.append(parsed_timestamp)
            module_name_list.append(parsed_module_name)
            topic_name_list.append(parsed_topic_name)
            byte_name_list.append(parsed_data_dict['byte_name'])
            data_list.append(parsed_data_dict['data'])
            unit_list.append(parsed_data_dict['unit'])

        return {
            "timestamp": timestamp_list,
            "module_name": module_name_list,
            "topic_name": topic_name_list,
            "byte_name": byte_name_list,
            "data": data_list,
            "unit": unit_list
        }
    except Exception as error:
        sys.stderr.write('Error: %s\n' % (str(error)))
        return None


def process_file(input_filename: str, verbose=False):
    global schema

    time_start = timer()

    schema = load_can_ids('can_ids.json', verbose)

    chunksize = 1e6
    reader = pandas.read_csv(
        input_filename,
        names=['log_data'],
        chunksize=chunksize,
        encoding='ISO-8859-1',
        lineterminator='\n',
        engine='c',
        low_memory=False,
        dtype=str,
        memory_map=True,
        error_bad_lines=False
    )

    columns = ['timestamp', 'module_name', 'topic_name', 'byte_name', 'data', 'unit']

    total_input_lines = 0
    total_output_lines = 0

    for c_index, chunk in enumerate(reader):
        output_filename = input_filename + '_chunk_' + str(c_index) + '.hdf5'
        if os.path.isfile(output_filename):
            print("File", output_filename, 'already converted, skipping this chunk...')
            continue

        chunk_time_start = timer()

        timestamp_chunk = []
        module_name_chunk = []
        topic_name_chunk = []
        byte_name_chunk = []
        data_chunk = []
        unit_chunk = []

        for index, row in chunk.iterrows():
            processed_row = process_row(row['log_data'])
            if (processed_row is None):
                continue

            timestamp_chunk += processed_row['timestamp']
            module_name_chunk += processed_row['module_name']
            topic_name_chunk += processed_row['topic_name']
            byte_name_chunk += processed_row['byte_name']
            data_chunk += processed_row['data']
            unit_chunk += processed_row['unit']

        parsed_df = pandas.DataFrame(zip(
            timestamp_chunk,
            module_name_chunk,
            topic_name_chunk,
            byte_name_chunk,
            data_chunk,
            unit_chunk
        ), columns=columns)

        #parsed_df = parsed_df[~parsed_df['timestamp'].str.contains(r'[^\x00-\x7F]+')]
        parsed_df['timestamp'] = pandas.to_datetime(parsed_df['timestamp'], unit='s')
        print(parsed_df.head(1).append(parsed_df.tail(1)))
        print(parsed_df.info(memory_usage='deep'))

        vaex_parsed_df = vaex.from_pandas(parsed_df)
        if vaex_parsed_df.length() > 0:
            vaex_parsed_df.export_hdf5(output_filename)
        vaex_parsed_df.close_files()

        chunk_time_end = timer()
        chunk_time_elapsed = chunk_time_end - chunk_time_start
        total_input_lines += len(chunk)
        total_output_lines += len(parsed_df)
        print(f"Chunk {c_index}, elapsed: {chunk_time_elapsed} s, output/input: {len(parsed_df)}/{len(chunk)} lines")

        del parsed_df

    time_end = timer()
    time_elapsed = time_end - time_start

    return {
        'Input File Name': input_filename,
        'Output File Name': output_filename,
        'Elapsed time': time_elapsed,
        'Input lines': total_input_lines,
        'Output lines': total_output_lines
    }


def process_dataset(dataset_path: str, filename_prefix: str):
    input_filename_glob = dataset_path + '/' + filename_prefix + '.log'

    input_file_list = glob.glob(input_filename_glob)

    print('Files to process:', input_file_list)

    for input_filename in input_file_list:
        print('Processing file:', input_filename)
        report = process_file(input_filename)

        print('Report:')
        print('\tElapsed time:', report['Elapsed time'], 'seconds')
        if report['Input lines'] > 0:
            print('\tConversion rate:', report['Elapsed time'] * 1000 / report['Input lines'], 'ms per line')
        else:
            print('\tConversion rate: empty input file, not converted.')


if __name__ == '__main__':
    dataset_path = '../datalog'
    filename_prefix = 'candump-2020-0[12]*'
    process_dataset(dataset_path, filename_prefix)
