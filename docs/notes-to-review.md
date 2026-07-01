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
