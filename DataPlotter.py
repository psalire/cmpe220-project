import matplotlib.pyplot as plt
import pandas as pd
import logging

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)

class DataPlotter:

    def __init__(self, data, db):
        self.data = data
        self.db = db.capitalize()

    def plot_means(self, title, means, lang):
        fname = f'{self.db}_{lang}_means.png'
        try:
            fig, ax = plt.subplots()
            ax.bar(title, means)

            ax.set_title(f'{lang.capitalize()} {self.db} Benchmark',
                    loc ='center',)
            ax.set_xticklabels(title,rotation=90)

            plt.xlabel('Operation', fontweight ='bold')
            plt.ylabel('Mean Time(ms)', fontweight ='bold')
            plt.savefig(fname, bbox_inches='tight')
            logging.info(f'Created plot {fname}')
            # plt.show()
        except Exception as e:
            logging.error(f'Create plot {fname} failed.')
            logging.exception(e)

    def plot_language_comparison(self):
        fname = f'{self.db}_language_comparison.png'
        try:
            d = {}
            for lang in self.data:
                d[lang] = {}
                for b in self.data[lang]:
                    if self.data[lang][b]['success'] is False:
                        continue
                    d[lang][b] = self.data[lang][b]['time']['mean']
            df = pd.DataFrame(d)

            ax = df.plot.bar()
            ax.set_xlabel('Benchmark')
            ax.set_ylabel('Mean time (ms)')
            ax.set_title(f'{self.db} Benchmarks')
            plt.savefig(fname, bbox_inches='tight')
            logging.info(f'Created plot {fname}')
        except Exception as e:
            logging.error(f'Create plot {fname} failed.')
            logging.exception(e)

    def plot_mean_max_min(self):
        for lang in self.data:
            d = {'mean': {}, 'max': {}, 'min': {}}
            for b in self.data[lang]:
                if self.data[lang][b]['success'] is False:
                    continue
                for k in d.keys():
                    d[k][b] = self.data[lang][b]['time'][k]
            df = pd.DataFrame(d)

            fname = f'{self.db}_{lang}_mean_max_min.png'
            ax = df.plot.bar()
            ax.set_xlabel('Benchmark')
            ax.set_ylabel('Time (ms)')
            ax.set_title(f'{self.db} Benchmarks')
            plt.savefig(fname, bbox_inches='tight')
            logging.info(f'Created plot {fname}')

    def result_display(self):
        self.plot_language_comparison()
        self.plot_mean_max_min()

        title_op = []
        mean_op = []

        for language in self.data.keys():
            for benchmark in self.data[language]:
                benchmark_data = self.data[language][benchmark]

                if benchmark_data['success'] is False:
                    continue

                title_op.append(benchmark)
                mean_op.append(benchmark_data['time']['mean'])

            if len(title_op) > 0:
                self.plot_means(title_op, mean_op, language)

            title_op.clear()
            mean_op.clear()
