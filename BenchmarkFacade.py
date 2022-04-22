
from abc import ABC, abstractmethod
from statistics import mean
import logging

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)


class BenchmarkFacade(ABC):

    def __init__(self, args):
        self.args = args

    def run_benchmark(self, instance, name):
        '''
        Run a benchmark with an instance
        :return: results
        :rtype: dict
        '''
        category = str(instance.getCategory())
        if category.lower() != self.args.db:
            return None
        logging.info(f'Running benchmark "{name}"...')
        results = []
        for i in range(self.args.n):
            try:
                t = instance.benchmark()
                logging.info(f'i={i}, Time: {t}ms')
                results.append(float(t))
            except Exception as e:
                logging.error(f'Benchmark "{name}" failed!')
                logging.exception(e)
                try:
                    instance.endQuery()
                except Exception as e:
                    logging.exception(e)
                return {
                    'success': False,
                }
        return {
            'category': category,
            'time': {
                'mean': mean(results),
                'min': min(results),
                'max': max(results),
            },
            'success': True,
        }

    @abstractmethod
    def run(self):
        pass
