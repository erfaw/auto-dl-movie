# `threading` and `queue` to parralelism

Target is to learn how make a thread for a process to run parallel with other process.

## First question is: Asyncio or threading? which one is better for where? 
> `ChatGPT`
>> * **`asyncio`**: Single-threaded, cooperative concurrency; best for **I/O-bound** tasks (HTTP, sockets, APIs, async DB).
>> * **`threading`**: Multiple OS threads; best for **blocking I/O** or integrating with synchronous libraries.
>> * **CPU-bound work**: Neither is ideal in CPython due to the **GIL**; use `multiprocessing` or `ProcessPoolExecutor`.
>> * **`asyncio`** scales to thousands of concurrent I/O tasks with low overhead.
>> * **`threading`** is simpler when code is already synchronous or cannot be made async.
>> * Rule of thumb: **I/O + async ecosystem → `asyncio`; blocking I/O → `threading`; CPU-intensive → `multiprocessing`.**

### What exactly is CPU-intensive?
> `ChatGPT`
>> * A task that spends most of its time **computing**, not waiting.
>> * Examples: image/video processing, encryption, ML training, large matrix operations, prime-number search.
>> * Performance is limited mainly by **CPU speed/cores**.
>> * In CPython, threads cannot execute Python bytecode truly in parallel because of the **GIL**.
>> * For these tasks, prefer **`multiprocessing`**.

### Some about `multiprocessing`
> `ChatGPT`
>> * Creates **separate processes**, each with its own Python interpreter and memory.
>> * Achieves **true parallelism** on multi-core CPUs.
>> * Bypasses the **GIL**, making it ideal for CPU-intensive work.
>> * Processes communicate via `Queue`, `Pipe`, or shared memory (slower than thread communication).
>> * Higher memory and startup overhead than threads.
>> * Rule: **Heavy computation → `multiprocessing`; blocking I/O → `threading`; async I/O → `asyncio`.**

---

## GIL problem
in my assumption, when we think about threads we have a Process which going to use many threads (or better say could).
> `ChatGPT`
>> A process always has at least one thread (the main thread), and it may create additional threads that share the same memory and resources.

which in threading module we using one process with many threads. but, we have some <u>issue with GIL in python during that</u>.

### More about GIL (Global Interpreter Lock)
> `ChatGPT`
>> * **GIL** is a lock in **CPython** that allows **only one thread to execute Python bytecode at a time**.
>> * It exists to make **memory management and reference counting** thread-safe.
>> * **CPU-bound threads** cannot run Python code in parallel because they compete for the GIL.
>> * **I/O-bound threads** are mostly unaffected because they release the GIL while waiting (disk, network, sleep, etc.).
>> * The OS still schedules multiple threads, but only one holds the GIL at any instant.
>> * Extensions written in C/C++ (e.g., NumPy) can release the GIL during heavy computations.
>> * `multiprocessing` avoids the GIL by creating **separate processes**, each with its own interpreter and GIL.
>> * **The GIL is a CPython implementation detail**, not a Python language feature; other implementations may not have it.

---
## What is in our mind? 
I need these 2 functionality for my program at the same time:
1. Download a file from internet with my ready methods (sync)
2. Copy fully downloaded file in an external storage with my ready methods (sync)

in my point of view i need to use threading module in combination with queue module. make a main thread and 2 other threads following above targets.

---

## Roadmap
> `ChatGPT`
>> Given your use case (download → copy concurrently using your existing synchronous code), I'd learn them in this order:
>> 
>> 1. **`threading` (first)** ✅
>> 
>>    * Thread objects (`Thread`)
>>    * `start()` / `join()`
>>    * Daemon threads
>>    * Thread synchronization basics (`Lock`, optional)
>>    * Producer–consumer pattern
>> 
>> 2. **`queue` (immediately after `threading`)** ✅
>> 
>>    * `Queue`
>>    * `put()`, `get()`
>>    * `task_done()`
>>    * `join()`
>>    * Sentinel values (e.g., `None`) to stop worker threads
>> 
>> 3. **`asyncio` (later)**
>> 
>>    * Event loop
>>    * Coroutines (`async`/`await`)
>>    * Tasks
>>    * Queues (`asyncio.Queue`)
>>    * Running blocking code (`asyncio.to_thread()`)
>> 
>> For your project, **`threading` + `queue`** is exactly the combination you should master first. Once you're comfortable with that, learning `asyncio` will be much easier because you'll already understand concurrent program design.

---

## Reading [`threading`](https://docs.python.org/3.12/library/threading.html#module-threading)

[short intro](https://docs.python.org/3.12/tutorial/stdlib2.html#multi-threading)

simple example of zipping a file in bg:
```
import threading, zipfile

class AsyncZip(threading.Thread):
    def __init__(self, infile, outfile):
        threading.Thread.__init__(self)
        self.infile = infile
        self.outfile = outfile

    def run(self):
        f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
        print('Finished background zip of:', self.infile)

background = AsyncZip('mydata.txt', 'myarchive.zip')
background.start()
print('The main program continues to run in foreground.')

background.join()    # Wait for the background task to finish
print('Main program waited until background was done.')
```

when i think about combination of threading and queue, which talks to each other in this way, APIs in web came in my mind. 

* [threading.enumerate()](https://docs.python.org/3.12/library/threading.html#threading.enumerate): Return a list of all Thread objects currently active.
* [threading.current_thread()](https://docs.python.org/3.12/library/threading.html#threading.current_thread): Return the current Thread object
* [threading.active_count()](https://docs.python.org/3.12/library/threading.html#threading.active_count): Return the number of Thread objects currently alive.

threading.enumerate() Return a list of all Thread objects currently active. The list includes daemonic threads and dummy thread objects created by current_thread(). It excludes terminated threads and threads that have not yet been started. However, the main thread is always part of the result, even when terminated.
> `ChatGPT`
>> threading.enumerate() returns all Python Thread objects that are alive within the process that called it. It does not list threads from other Python processes or from the operating system (Windows/Linux) as a whole.

### what is a daemon thread?
> `ChatGPT`
>> A **daemon thread** is a **background thread** that runs alongside your main program.
>> * It performs supporting work (e.g., logging, monitoring, cleanup).
>> * When **all non-daemon threads finish**, Python **automatically stops** daemon threads, even if they're still running.
>> * Use daemon threads only for tasks that don't need to finish before the program exits.

### What is a `Lock` object in `threading`?
> `ChatGPT`
>> A **`Lock`** is a synchronization object that lets **only one thread** access a shared resource (critical section) at a time.
>> * Prevents **race conditions** when multiple threads modify the same data.
>> * A thread **acquires** the lock before entering the critical section.
>> * Other threads must **wait** until the lock is **released**.
>> * Think of it as a **room key**: only the thread holding the key can enter the room.

### What is a `Semaphore` object?
> `ChatGPT`
>> A **`Semaphore`** is a synchronization object that allows **up to N threads** to access a shared resource at the same time.
>> * Unlike a `Lock` (1 thread), a semaphore permits **multiple threads**.
>> * It maintains an internal **counter** (e.g., 3).
>> * Each `acquire()` decreases the counter; each `release()` increases it.
>> * When the counter reaches **0**, additional threads wait until one releases the semaphore.
>> * Example: limit access to **3 database connections** or **5 download slots** simultaneously.


### What is an `Event` object?
> `ChatGPT`
>> An **`Event`** is a synchronization object used to **signal** between threads.
>> * One thread calls `event.set()` to signal.
>> * Other threads call `event.wait()` and block until the event is set.
>> * Useful for "start now", "stop now", or "ready" notifications.

---

### What is a `Timer` object?
> `ChatGPT`
>> A **`Timer`** is a thread that **waits for a specified delay**, then runs a function.
>> * Similar to `time.sleep()`, but runs in its **own thread**.
>> * Can be **canceled** before it executes.
>> * Useful for delayed tasks.

---

### What is a `Barrier` object?
> `ChatGPT`
>> A **`Barrier`** makes **multiple threads wait** until all of them reach the same point.
>> * You specify the number of participating threads.
>> * Each thread calls `barrier.wait()`.
>> * When all have arrived, they all continue together.
>> * Useful for synchronizing phases of parallel work.

---
