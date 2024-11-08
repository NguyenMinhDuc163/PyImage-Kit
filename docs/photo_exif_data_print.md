
[index](./index.md)


Print date to photo by using exif data.


Search font file place of your PC:
```sh
$ sudo find / -name "Arial Black.ttf"
```

　Mac example
```
/Library/Fonts/Arial Black.ttf
```

　copy font file
```sh
$ cp /Library/Fonts/Arial Black.ttf ./
```


```sh
$ python photo_exif_date_print.py sample.jpg
```

 if you want to process many files. make below script named `photo-exif-date-print.sh`
```sh

for f in *.jpg
do
    python photo-exif-date-print.py $f
done
```

 then execute following commands:
```sh
$ chmod 755 photo-exif-date-print.sh
$ ./photo-exif-date-print.sh
```


<img src="https://raw.githubusercontent.com/wiki/karaage0703/python-image-processing/0004.jpg" alt="image" width="640" height="480">


<img src="https://raw.githubusercontent.com/wiki/karaage0703/python-image-processing/0006.jpg" alt="image" width="640" height="480">


