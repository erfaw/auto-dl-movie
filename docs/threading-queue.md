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
