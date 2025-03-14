import time


def time_it(func):
    """ A decorator that calculates the execution time of a function. """
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start timer
        result = await func(*args, **kwargs)  # Run the actual function
        end_time = time.perf_counter()  # End timer
        elapsed_time = end_time - start_time
        print(f"⏱️ {func.__name__} took {elapsed_time:.4f} seconds")
        return result  # Return the function's actual result
    return wrapper
