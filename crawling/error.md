# 1

```bash
multiprocessing.pool.RemoteTraceback: 
"""
Traceback (most recent call last):
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connection.py", line 159, in _new_conn
    conn = connection.create_connection(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/util/connection.py", line 61, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
  File "/usr/lib/python3.8/socket.py", line 918, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno -3] Temporary failure in name resolution

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 670, in urlopen
    httplib_response = self._make_request(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 381, in _make_request
    self._validate_conn(conn)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 978, in _validate_conn
    conn.connect()
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connection.py", line 309, in connect
    conn = self._new_conn()
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connection.py", line 171, in _new_conn
    raise NewConnectionError(
urllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPSConnection object at 0x7f3e576823a0>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/adapters.py", line 439, in send
    resp = conn.urlopen(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 726, in urlopen
    retries = retries.increment(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/util/retry.py", line 446, in increment
    raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='www.weather.go.kr', port=443): Max retries exceeded with url: /weather/earthquake_volcano/domesticlist.jsp?startSize=0.0&endSize=999.0&keyword=&startTm=1975-04-01&endTm=1975-06-30 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f3e576823a0>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.8/multiprocessing/pool.py", line 125, in worker
    result = (True, func(*args, **kwds))
  File "/usr/lib/python3.8/multiprocessing/pool.py", line 48, in mapstar
    return list(map(*args))
  File "/home/dohan/project/crawling/crawling/kma/earthquake.py", line 23, in get_all_querys
    res = requests.get(url)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/api.py", line 76, in get
    return request('get', url, params=params, **kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/api.py", line 61, in request
    return session.request(method=method, url=url, **kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/sessions.py", line 530, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/sessions.py", line 643, in send
    r = adapter.send(request, **kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='www.weather.go.kr', port=443): Max retries exceeded with url: /weather/earthquake_volcano/domesticlist.jsp?startSize=0.0&endSize=999.0&keyword=&startTm=1975-04-01&endTm=1975-06-30 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f3e576823a0>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution'))
"""

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "entrypoint.py", line 5, in <module>
    data = crawling.kma_earthquake()
  File "/home/dohan/project/crawling/crawling/crawling.py", line 70, in kma_earthquake
    ret = p.map(earthquake.get_all_querys , querys)
  File "/usr/lib/python3.8/multiprocessing/pool.py", line 364, in map
    return self._map_async(func, iterable, mapstar, chunksize).get()
  File "/usr/lib/python3.8/multiprocessing/pool.py", line 771, in get
    raise self._value
requests.exceptions.ConnectionError: None: Max retries exceeded with url: /weather/earthquake_volcano/domesticlist.jsp?startSize=0.0&endSize=999.0&keyword=&startTm=1975-04-01&endTm=1975-06-30 (Caused by None)
```



```
//안됨
https://www.weather.go.kr/weather/earthquake/domesticlist.jsp?startSize=0.0&endSize=999.0&keyword=&startTm=2020-08-23&endTm=2020-11-23

//됨
https://www.weather.go.kr/weather/earthquake_volcano/domesticlist.jsp?startSize=0.0&endSize=999.0&startTm=2020-08-23&endTm=2020-11-23
```

```bash
multiprocessing.pool.RemoteTraceback: 
"""
Traceback (most recent call last):
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connection.py", line 159, in _new_conn
    conn = connection.create_connection(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/util/connection.py", line 61, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
  File "/usr/lib/python3.8/socket.py", line 918, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno -3] Temporary failure in name resolution

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 670, in urlopen
    httplib_response = self._make_request(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 381, in _make_request
    self._validate_conn(conn)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 978, in _validate_conn
    conn.connect()
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connection.py", line 309, in connect
    conn = self._new_conn()
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connection.py", line 171, in _new_conn
    raise NewConnectionError(
urllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPSConnection object at 0x7f59ddae5a60>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/adapters.py", line 439, in send
    resp = conn.urlopen(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 726, in urlopen
    retries = retries.increment(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/util/retry.py", line 446, in increment
    raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='www.weather.go.kr', port=443): Max retries exceeded with url: /weather/earthquake_volcano/domesticlist.jsp?startSize=0.0&endSize=999.0&keyword=&startTm=2020-07-01&endTm=2020-09-30 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f59ddae5a60>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.8/multiprocessing/pool.py", line 125, in worker
    result = (True, func(*args, **kwds))
  File "/usr/lib/python3.8/multiprocessing/pool.py", line 48, in mapstar
    return list(map(*args))
  File "/home/dohan/project/crawling/crawling/kma/earthquake.py", line 29, in get_all_querys
    res = requests.get(url)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/api.py", line 76, in get
    return request('get', url, params=params, **kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/api.py", line 61, in request
    return session.request(method=method, url=url, **kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/sessions.py", line 530, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/sessions.py", line 643, in send
    r = adapter.send(request, **kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='www.weather.go.kr', port=443): Max retries exceeded with url: /weather/earthquake_volcano/domesticlist.jsp?startSize=0.0&endSize=999.0&keyword=&startTm=2020-07-01&endTm=2020-09-30 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f59ddae5a60>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution'))
"""

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "entrypoint.py", line 5, in <module>
    data = crawling.kma_earthquake()
  File "/home/dohan/project/crawling/crawling/crawling.py", line 71, in kma_earthquake
    ret = p.map(earthquake.get_all_querys , urls)
  File "/usr/lib/python3.8/multiprocessing/pool.py", line 364, in map
    return self._map_async(func, iterable, mapstar, chunksize).get()
  File "/usr/lib/python3.8/multiprocessing/pool.py", line 771, in get
    raise self._value
requests.exceptions.ConnectionError: None: Max retries exceeded with url: /weather/earthquake_volcano/domesticlist.jsp?startSize=0.0&endSize=999.0&keyword=&startTm=2020-07-01&endTm=2020-09-30 (Caused by None)
```

```bash
Traceback (most recent call last):
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connection.py", line 159, in _new_conn
    conn = connection.create_connection(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/util/connection.py", line 61, in create_connection
    for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
  File "/usr/lib/python3.8/socket.py", line 918, in getaddrinfo
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno -3] Temporary failure in name resolution

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 670, in urlopen
    httplib_response = self._make_request(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 381, in _make_request
    self._validate_conn(conn)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 978, in _validate_conn
    conn.connect()
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connection.py", line 309, in connect
    conn = self._new_conn()
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connection.py", line 171, in _new_conn
    raise NewConnectionError(
urllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPSConnection object at 0x7f63c28ddac0>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/adapters.py", line 439, in send
    resp = conn.urlopen(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 726, in urlopen
    retries = retries.increment(
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/urllib3/util/retry.py", line 446, in increment
    raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='www.weather.go.kr', port=443): Max retries exceeded with url: /weather/earthquake_volcano/domesticlist.jsp?startSize=0.0&endSize=999.0&keyword=&startTm=1981-07-01&endTm=1981-09-30 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f63c28ddac0>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.8/multiprocessing/pool.py", line 125, in worker
    result = (True, func(*args, **kwds))
  File "/usr/lib/python3.8/multiprocessing/pool.py", line 48, in mapstar
    return list(map(*args))
  File "/home/dohan/project/crawling/crawling/kma/earthquake.py", line 29, in get_all_querys
    res = requests.get(url)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/api.py", line 76, in get
    return request('get', url, params=params, **kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/api.py", line 61, in request
    return session.request(method=method, url=url, **kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/sessions.py", line 530, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/sessions.py", line 643, in send
    r = adapter.send(request, **kwargs)
  File "/home/dohan/project/crawling/venv/lib/python3.8/site-packages/requests/adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='www.weather.go.kr', port=443): Max retries exceeded with url: /weather/earthquake_volcano/domesticlist.jsp?startSize=0.0&endSize=999.0&keyword=&startTm=1981-07-01&endTm=1981-09-30 (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f63c28ddac0>: Failed to establish a new connection: [Errno -3] Temporary failure in name resolution'))
```

