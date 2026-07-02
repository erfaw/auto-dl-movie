# Notes to review later

## Playwright

some useful options we can use according to documents.

### [Locator.highlight()](//*[@id="__next"]/main/div/section/div/section/div/div[1]/section/div[2]/ul)
which highlights corresponding element which is in our variable.

### [Locator.wait_for()](https://playwright.dev/python/docs/api/class-locator#locator-wait-for)
for default waits for visibility of that element located. which has a clear definition of what is visible. 

---

## [tqdm](https://tqdm.github.io/docs/tqdm/) package

its a package to using with **Progress Bars** in CLI and even GUI which we use CLI this time. 

### our usage
```
with rq.get(url, stream=True) as response:
    with open(file_path, 'wb') as file:
        with tqdm(
            total=int(response.headers['Content-Length']),
            unit='B',
            unit_scale=True,
        ) as pb:
            for chunk in response.iter_content(chunk_size=64*1024):
                if chunk :
                    file.write(chunk)
                    pb.update(len(chunk))
```

---

## [Google-Style Docstring](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

[How to write docstrings in python](https://realpython.com/how-to-write-docstrings-in-python/)

This project somehow was a exercise for me to use docstring more than before.

how to add docstring to different ascpect of code like `class`, `module`, `variable`, `function`, `method`, etc.

I found out there is many tools to document your project through your docstring. 

Of course you can use it when you are at debugging. it so much easier. and other devs could gain better understanding of your code.

---

## [shutil](https://docs.python.org/3/library/shutil.html) built-in package

its most powerfull way to work with files and directories.

helpful methods in first look: 
1. [shutil.move()](https://docs.python.org/3/library/shutil.html#shutil.move)
2. [shutil.copy2()](https://docs.python.org/3/library/shutil.html#shutil.copy2)
3. [shutil.copytree()](https://docs.python.org/3/library/shutil.html#shutil.copytree)
4. [shutil.disk_usage()](https://docs.python.org/3/library/shutil.html#shutil.disk_usage)

---

## Walrus Operator (`:=`)

* Introduced in **Python 3.8** to **assign and evaluate** in one expression.
* Example: `while chunk := source.read(CHUNK_SIZE):`
* Equivalent to assigning `chunk` before the loop and after each iteration.
* Commonly used for reading files, sockets, and streams until EOF.
* Docs: https://docs.python.org/3/reference/expressions.html#assignment-expressions | https://peps.python.org/pep-0572/

---

## Streaming in file level with open() and read()
Because **the file object (`source`) keeps an internal file pointer (cursor).**

Every time you call:

```python
source.read(CHUNK_SIZE)
```

Python:

1. Reads `CHUNK_SIZE` bytes **from the current cursor position**.
2. Automatically moves the cursor forward by the number of bytes read.

For example, with `CHUNK_SIZE = 4` and file contents:

```text
ABCDEFGH
```

The calls behave like this:

```text
1st read() -> ABCD   (cursor moves to E)
2nd read() -> EFGH   (cursor moves to EOF)
3rd read() -> b''    (EOF reached)
```

You never have to tell `read()` where to continue—it remembers because the **file object maintains the current position**.

If you're curious, you can inspect it with:

* `source.tell()` → current cursor position.
* `source.seek(offset)` → move the cursor manually.

This "cursor" concept is fundamental to file I/O in Python and most programming languages.

---

## How to implement resume downloading file with requests.get(stream=True)? HTTP Resume (Range Requests)

* Resume downloads use the HTTP `Range` header (e.g. `Range: bytes=<downloaded>-`) to request only the remaining bytes.
* If the server supports it, it responds with **206 Partial Content** and continues the download.
* If it ignores the `Range` header, it responds with **200 OK**, so the download should restart.
* The local file must be opened in **append (`ab`)** mode when resuming.
* Servers often indicate support with `Accept-Ranges: bytes`.

Most important part of this implementation is about Range request.

```
# More codes above...
    downloaded = file_path.stat().st_size if file_path.exists() else 0

    headers = {}
    if downloaded:
        headers["Range"] = f"bytes={downloaded}-"

    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()

        # Server accepted resume
        if response.status_code == 206:
            mode = "ab"
            total = int(response.headers["Content-Length"]) + downloaded

        # Server ignored Range request
        else:
            mode = "wb"
            downloaded = 0
            total = int(response.headers.get("Content-Length", 0))
# More codes below...
```

---

##