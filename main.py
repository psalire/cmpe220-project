from pprint import pprint
from JavaBenchmarkFacade import JavaBenchmarkFacade
from PythonBenchmarkFacade import PythonBenchmarkFacade
import logging
import argparse
# import json


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
    '--db',
    required=True,
    type=str,
    help='Which DBMS to benchmark',
    choices=['cassandra', 'mysql'],
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
        results[name] = benchmark_instances[name].run()

    pprint(results)


if __name__ == '__main__':
    main()
