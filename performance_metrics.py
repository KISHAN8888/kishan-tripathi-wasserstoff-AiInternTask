import time
import psutil
from concurrent.futures import ProcessPoolExecutor
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class PerformanceMetrics:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.cpu_percent = []
        self.memory_usage = []
        self.document_times = {}

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def record_metrics(self):
        self.cpu_percent.append(psutil.cpu_percent())
        self.memory_usage.append(psutil.virtual_memory().percent)

    def record_document_time(self, document_name, processing_time):
        self.document_times[document_name] = processing_time

    def get_processing_time(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    def get_avg_cpu_usage(self):
        return sum(self.cpu_percent) / len(self.cpu_percent) if self.cpu_percent else None

    def get_avg_memory_usage(self):
        return sum(self.memory_usage) / len(self.memory_usage) if self.memory_usage else None

    def get_avg_document_time(self):
        if self.document_times:
            return sum(self.document_times.values()) / len(self.document_times)
        return None

def measure_performance(func, max_workers, *args):
    metrics = PerformanceMetrics()
    metrics.start()

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future = executor.submit(func, *args, max_workers=max_workers)
        while not future.done():
            metrics.record_metrics()
            time.sleep(1)

    processed_docs = future.result()
    for doc in processed_docs:
        metrics.record_document_time(doc['filename'], doc.get('processing_time', 0))

    metrics.stop()

    results = {
        'processing_time': metrics.get_processing_time(),
        'avg_cpu_usage': metrics.get_avg_cpu_usage(),
        'avg_memory_usage': metrics.get_avg_memory_usage(),
        'avg_document_time': metrics.get_avg_document_time(),
        'document_times': metrics.document_times
    }

    logger.info(f"Performance with {max_workers} workers:")
    logger.info(f"  Processing time: {results['processing_time']:.2f} seconds")
    logger.info(f"  Average CPU usage: {results['avg_cpu_usage']:.2f}%")
    logger.info(f"  Average memory usage: {results['avg_memory_usage']:.2f}%")
    logger.info(f"  Average document processing time: {results['avg_document_time']:.2f} seconds")

    save_metrics_to_file(results)
    return results

def save_metrics_to_file(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"performance_metrics_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Performance metrics saved to {filename}")
