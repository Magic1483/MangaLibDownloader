# MangaLibDownloader
Написан на python с использованием Selenium и requests
---
Работает с:

  [mangalib](https://mangalib.me/)
  
  [yaoilib](https://yaoilib.me/)
  
  [hentailib](https://hentailib.me/)
  

  
 -------
 # Usage
 ```
 python main.py '**link to mangalib chapters**'
 ```
 or 
 ```
 python main.py '**link to mangalib chapters**' --beg **begin chapter** --end **end chapter**
 ```
 Для скачивания материалов с ограничениями нужно использовать cookie,в соответствии с сайтом.
 ```
 python main.py '**link to mangalib chapters**' --beg **begin chapter** --end **end chapter** --cookie 'path/to/cookie.json'
 ```
 ------
 TO DO:
 
 .добавить  animelib, ranobelib
