from pprint import pprint
from JavaBenchmarkFacade import JavaBenchmarkFacade
from PythonBenchmarkFacade import PythonBenchmarkFacade
import logging
import argparse
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

def plotResults(title, means, lang, db):
    fig, ax = plt.subplots()
    ax.bar(title, means)

    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    ax.grid(visible = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)

    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
                str(round((i.get_width()), 2)),
                fontsize = 10, fontweight ='bold',
                color ='grey')

    ax.set_title(f'{db} {lang} Benchmark',
             loc ='center',)
             

    plt.xlabel('Operation', fontweight ='bold')
    plt.ylabel('Time(ms)', fontweight ='bold')
    plt.show()

def result_display(results):
    title_op = []
    mean_op = []
    language = ['python', 'java', 'nodejs']
    database = ['mysql', 'cassandra', 'mongodb']

    for lang in language:
        if lang not in results:
            continue

        data = results[lang]
        for db in database:            
            for op in data.keys():
                if not data[op]['success']:
                    continue

                if data[op]['category'] != db:
                    continue

                title_op.append(op)
                mean_op.append(data[op]['time']['mean'])

            if len(title_op) > 0:
                plotResults(title_op, mean_op, lang, db)

            title_op.clear()
            mean_op.clear()


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

    result_display(results)
    # plt.plot(results)

    # plt.ylabel('y numbers')
    # plt.xlabel('x numbers')
    # plt.show()

    # Write results dict to JSON
    try:
        filename = f'{args.output}_{args.db}.json'
        with open(filename, 'w') as file:
            json.dump(results, file)
        logging.info(f'Wrote output to {filename}')
    except Exception as e:
        logging.error('Write output to JSON file failed.')
        logging.exception(e)


if __name__ == '__main__':
    main()
