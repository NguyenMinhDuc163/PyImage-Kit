[index](./index.md)




color swap from RGB to BGR


prepare target photo


```sh
$ python color_swap.py sample.jpg
```


<img src="https://raw.githubusercontent.com/wiki/karaage0703/python-image-processing/0002.jpg" alt="image" width="640" height="480">




<img src="https://raw.githubusercontent.com/wiki/karaage0703/python-image-processing/0011.jpg" alt="image" width="640" height="480">





gray scale converter


prepare target photo


```sh
$ python color_gray.py sample.jpg
```


<img src="https://raw.githubusercontent.com/wiki/karaage0703/python-image-processing/0002.jpg" alt="image" width="640" height="480">




<img src="https://raw.githubusercontent.com/wiki/karaage0703/python-image-processing/0012.jpg" alt="image" width="640" height="480">




sepia color converter


prepare target photo


```sh
$ python color_sepia.py sample.jpg
```


<img src="https://raw.githubusercontent.com/wiki/karaage0703/python-image-processing/0002.jpg" alt="image" width="640" height="480">


<img src="https://raw.githubusercontent.com/wiki/karaage0703/python-image-processing/0013.jpg" alt="image" width="640" height="480">




extract color


prepare target photo


```sh
$ python extract_color.py sample.jpg h_min, h_max, s_th, v_th
```

example:
```sh
$ python extract_color.py 0002.jpg 10 40 10 50
```


<img src="https://raw.githubusercontent.com/wiki/karaage0703/python-image-processing/0002.jpg" alt="image" width="640" height="480">


<img src="https://raw.githubusercontent.com/wiki/karaage0703/python-image-processing/0014.jpg" alt="image" width="640" height="480">


- Interface 2017/05
- http://venuschjp.blogspot.jp/2015/02/pythonopencv.html
- https://www.blog.umentu.work/python-opencv3で画素のrgb値を入れ替える/
