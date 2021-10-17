# standard library
from pathlib import Path

# external library
import pyscca

# custom library
# from utils.events import Events


def parse_pf_file(prefetch_file: str) -> list:
    """
    Parse prefetch file, return one result for every time the binary was run.
    :param prefetch_file: location of the prefetch file
    :return: a list of result dictionaries
    """
    if not isinstance(prefetch_file, str):
        raise ValueError('prefetch_file location is not a string')

    parsed_prefetch_entries = list()

    # open the prefetch file
    pf_data = pyscca.open(prefetch_file)

    # build our parsed data
    executable_name = pf_data.executable_filename
    run_count = pf_data.run_count
    file_imports = '|'.join([file_metric.filename for file_metric in pf_data.file_metrics_entries])

    for run_time_index in range(0, run_count):
        try:
            # run_time_index == 0 ensures that we always record one entry, even if it hasn't been run.
            if run_time_index == 0:
                timestamp = pf_data.get_last_run_time(run_time_index).strftime("%Y-%m-%d %H:%M:%S")
            elif pf_data.get_last_run_time_as_integer(run_time_index) > 0:
                timestamp = pf_data.get_last_run_time(run_time_index).strftime("%Y-%m-%d %H:%M:%S")
            else:
                continue
        except OSError as e:
            break

        entry = {'timestamp': timestamp,
                 'executable_name': executable_name,
                 'run_count': run_count,
                 'imports': file_imports}

        parsed_prefetch_entries.append(entry)

    return parsed_prefetch_entries


def parse_prefetch(prefetch_location: str) -> list:
    if not isinstance(prefetch_location, str):
        raise ValueError('prefetch_file location is not a string')

    all_parsed_prefetch_files = list()

    prefetch_data_location = Path(prefetch_location)

    if prefetch_data_location.is_dir():
        for file in prefetch_data_location.glob('*.pf'):
            parsed_prefetch_data = parse_pf_file(str(file))
            all_parsed_prefetch_files.extend(parsed_prefetch_data)
    else:
        all_parsed_prefetch_files = [parse_pf_file(str(prefetch_data_location))]

    return all_parsed_prefetch_files


def main():
    data_dir = 'c:\\users\\user\\desktop\\prefetch\\'

    results = parse_prefetch(data_dir)
    print()


if __name__ == '__main__':
    main()
