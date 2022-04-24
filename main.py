from pprint import pprint
from JavaBenchmarkFacade import JavaBenchmarkFacade
from PythonBenchmarkFacade import PythonBenchmarkFacade
from DataPlotter import DataPlotter
import logging
import argparse
import json

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)

parser = argparse.ArgumentParser(
    description='CMPE 220 DBMS Benchmarker Framework',
)
parser.add_argument(
    '-n',
    type=int,
    default=10,
    help='Number of times to run each benchmark',
)
parser.add_argument(
    '-o',
    '--output',
    type=str,
    default='results',
    help='Ouput file name, saved as {output}_{db}.json.'
         'Overwrites any previous files.'
)
parser.add_argument(
    '--db',
    required=True,
    type=str,
    help='Which DBMS to benchmark',
    choices=['cassandra', 'mysql', 'mongo'],
)
parser.add_argument(
    '--no-java-compile',
    action='store_true',
    default=False,
    help='Skip compiliation of Java benchmarks',
)
parser.add_argument(
    '--no-java',
    action='store_true',
    default=False,
    help='Skip all Java benchmarks',
)
parser.add_argument(
    '--no-python',
    action='store_true',
    default=False,
    help='Skip all Python benchmarks',
)
parser.add_argument(
    '--java-dir',
    type=str,
    default='java_benchmarks',
    help='Which directory Java benchmarks are located',
)
parser.add_argument(
    '--python-dir',
    type=str,
    default='python_benchmarks',
    help='Which directory Python benchmarks are located',
)


def main():
    args = parser.parse_args()
    results = {}
    benchmark_instances = {}
    if args.no_java is False:
        benchmark_instances['java'] = JavaBenchmarkFacade(args)
    if args.no_python is False:
        benchmark_instances['python'] = PythonBenchmarkFacade(args)

    # Run all benchmarks
    for name in benchmark_instances:
        logging.info(f'Running {name} benchmarks...')
        result = benchmark_instances[name].run()
        if result:
            results[name] = result

    pprint(results)

    # Write results dict to JSON
    try:
        filename = f'{args.output}_{args.db}.json'
        with open(filename, 'w') as file:
            json.dump(results, file)
        logging.info(f'Wrote output to {filename}')
    except Exception as e:
        logging.error('Write output to JSON file failed.')
        logging.exception(e)

    DataPlotter(results, args.db).result_display()


if __name__ == '__main__':
    main()
