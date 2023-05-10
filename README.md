# Satellite Aerial Image Retrieval

***************

### How to run the code:

Please make sure the following environment is configured:

1. Python 3.5+
2. urllib
3. PIL

To run the script, simply input the following commands in Terminal:

```bash
python3 aerialImageRetrieval.py lat1, lon1, lat2, lon2,
```

where (lat1, lon1) is the latitude and longitude of the upper-left coordinate, and (lat2, lon2) is the latitude and longitude of the lower-right coordinate. 

In my code, my program tolerates arbitrary coordinates input, as long as the two coordinates are diagonal. My program will figure out to transform the input coordinates to the standardized one before processing.

##### Single Coordinate Location Image
To retrieve an image of a set width/height of meters centered at a location use the `-b` tag to specify a bounding box size:
```bash
python3 aerialImageRetrieval.py -b lat, lon, width, height
```
where `width` and `height` are approximated distances +/- 1 degree.


##### Output
The retrieved image will be stored in `.\output` folder. The name of the image will follow the 'aerialImage_{}.jpeg' ending with the retrieval level. 

Some sample retrievals could be:

1. Chicago Navy Pier:

```bash
python3 aerialImageRetrieval.py 41.893812 -87.615195 41.885108 -87.597778
```

![](https://ws1.sinaimg.cn/large/006tKfTcgy1fq3s5b4wo9j31kw127hdu.jpg)

2. Chicago Cloud Gate:

```bash
python3 aerialImageRetrieval.py 41.882981 -87.623496 41.882397 -87.623076
```

![](https://ws2.sinaimg.cn/large/006tKfTcgy1fq3s5q070dj308p0g9mxh.jpg)

3. Greater Chicago Area:

```bash
python3 aerialImageRetrieval.py 41.968574 -87.752519 41.774917 -87.566837
```

![](https://ws1.sinaimg.cn/large/006tKfTcgy1fq3s64n5o8j30u1163163.jpg)

4. Eiffel Tower in Paris:

```bash
python3 aerialImageRetrieval.py 48.859261 2.293362 48.856953 2.296194
```

![](https://ws1.sinaimg.cn/large/006tKfTcgy1fq3s6jfe44j30tc10cgqz.jpg)

5. The Palace Museum in China:

```bash
python3 aerialImageRetrieval.py 39.922856 116.391459 39.913278 116.402509
```

![](https://ws3.sinaimg.cn/large/006tKfTcgy1fq3s71164jj31kw1sab2a.jpg)

******



### Source Files:
1. tilesystem.py:
  This module implements a set of static methods used for Bing maps tile system. All the methods in sample C# code in https://msdn.microsoft.com/en-us/library/bb259689.aspx, have been implemented by my own understanding.
2. aerialImageRetrieval.py:
  This module is used to retrieve satellite/aerial image. Given a bounding box, which is composed of left up corner coordinate (latitude, longitude) and right down corner coordinate (latitude, longitude). Return an aerial imagery (with maximum resolution available) downloaded from Bing map tile system. The aerial image will be strictly cropped based on the size of bounding box. Also, if the given bounding box is too large and with the maximum resolution available, the retrieval image could be too large. So I set a maximum image size (8192 * 8192 pixels), approximately 256MB, to filter too large images.









