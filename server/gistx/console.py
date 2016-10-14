from concurrent import futures


def work(callback, items, workers):
    with futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for index, item in enumerate(items):
            executor.submit(callback, item)
    print("---------------- DONE chunk ----------------")
