Project này được lấy cảm hứng từ hai project tương tự về [KMeans MapReduce](https://github.com/markomih/kmeans_mapreduce) và [Sử dụng KMeans cùng xử lý ảnh để phân cụm u não](https://github.com/meilylaap/Brain-tumor-segmentation-with-Kmeans-plusplus-clustering)

# Cài đặt K-means MapReduce
Chúng tôi cài đặt thuật toán phân cụm k-means sử dụng MapReduce framework (Hadoop bản 3.4.0).
### Khởi động hadoop
Format namenode:
```bash
hdfs namenode -format
```

Khởi đôngh dfs và yarn
```bash
start-dfs.sh
start-yarn.sh
```
hoặc ngắn gọn hơn
```bash
start-all.sh
```

Nên sử dụng môi trường ảo để chạy chương trình này.

Bạn có thể sử dụng môi trường ```virtualenv``` hoặc ```conda```.

#### virtualenv
```bash
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

#### conda
```bash
conda activate
pip install -r requirements.txt
```


Chạy Shell script ```run.sh```. 

```
sh run.sh
```

Chương trình cần đường dẫn đến file jar và các tham số của nó:

* ```input``` - đường dẫn đến file data
* ```state``` - đường dẫn đến file chứa các centroids được khởi tạo 
* ```number``` - Số lượng reducer
* ```output``` - đường dẫn đến output 
* ```delta``` - ngưỡng hội tụ
* ```max``` - số lần lặp tối đa 
* ```distance``` - phương pháp tính khoảng cách (hiện tại chỉ dùng khoảng cách Euclide vì khối u thường có hình cầu)

## Workflow
Mô hình dưới đây mô tả một lần lặp của MapReduce.

![alt text][flow]

Đầu tiên, các **Centroids** được khởi tạo và danh sách các điểm (points.txt) được nạp vào **Distributed Cache**. Điều này được thực hiện bằng cách ghi đè (override) hàm ```setup``` trong lớp **Mapper** và lớp **Reducer**. 

Sau đó, file dữ liệu đầu vào được chia nhỏ và mỗi điểm dữ liệu được xử lý bởi một hàm ```map``` (trong quá trình **Map**). Hàm này ghi các cặp khóa-giá trị ```<Centroid, Point>```, trong đó **Centroid** tâm gần nhất so với **Point**. 

Tiếp theo, **Combiner** được sử dụng để làm giảm số lượng các lần ghi cục bộ. Trong quá trình này, các điểm dữ liệu nằm trên cùng một máy được cộng dồn và số lượng các điểm dữ liệu đó được lưu trong biến ```Point.number```. 

Bây giờ, vì lý do tối ưu hóa, các giá trị đầu ra được tự động trộn và sắp xếp theo các **Centroids**. 

**Reducer** thực hiện quy trình tương tự như **Combiner**, nhưng đồng thời cũng kiểm tra xem các centroids đã hội tụ hay chưa; bằng cách so sánh sự khác biệt giữa các centroids cũ và centroids mới với tham số đầu vào ```delta```. Nếu một centroid hội tụ, thì **Counter toàn cục** không thay đổi, ngược lại, nó sẽ tăng lên. 

Sau khi hoàn thành xong 1 vòng lặp, các centroids mới sẽ được lưu và chương trình sẽ kiểm tra hai điều kiện, nếu chương trình đạt đến số lượng tối đa vòng lặp hoặc nếu giá trị của **Counter** không thay đổi. Nếu một trong hai điều kiện thỏa mãn, thì chương trình kết thúc, ngược lại, chương trinh chạy lại MapReduce với các centroids mới đã cập nhật.

## Ứng dụng vào phân cụm hình ảnh theo màu
Một ứng dụng quan trọng của KMeans là lượng tử hóa hình ảnh theo màu.

Ảnh gốc             |  Ảnh sau khi được phân cụm
:-------------------------:|:-------------------------:
![alt text][11]  |  ![alt text][segment]


Sau khi phân cụm ảnh, chúng ta sẽ tiến hành nhị phân hóa ảnh, với threshold là 100:

Ảnh sau khi được phân cụm             |  Ảnh sau khi nhị phân hóa
:-------------------------:|:-------------------------:
![alt text][segment]  |  ![alt text][binary]


Sau đó, tiến hành xử lý ảnh, bằng cách erode và dilate hình ảnh để được kết quả mong muốn:

Ảnh sau khi nhị phân hóa            |  Ảnh sau khi xử lý
:-------------------------:|:-------------------------:
![alt text][binary]  |  ![alt text][morf]


Chúng ta có thể so sánh ảnh kết quả và ảnh thu được:

Ảnh sau thu được           |  Kết quả thật 
:-------------------------:|:-------------------------:
![alt text][morf]  |  ![alt text][real]

Sử dụng hệ số Dice để tính toán độ trùng khớp của hai ảnh:

$$
\text{Dice} = \frac {2 |A \cap B|}{|A| + |B|}
$$

Ta có thể thu được độ giống nhau của hai bức ảnh này đạt: 89.12%

[flow]: https://github.com/Maki94/kmeans_mapreduce/blob/master/figures/alg.png "One MapReduce iteration"
[11]: https://github.com/free-dino/KMeans-Mapreduce-for-Image-Segmentation/blob/main/figures/11.png
[segment]: https://github.com/free-dino/KMeans-Mapreduce-for-Image-Segmentation/blob/main/figures/11_colormap.png
[binary]: https://github.com/free-dino/KMeans-Mapreduce-for-Image-Segmentation/blob/main/figures/gambar_biner_100.png
[morf]: https://github.com/free-dino/KMeans-Mapreduce-for-Image-Segmentation/blob/main/figures/morf_11.png
[real]: https://github.com/meilylaap/Brain-tumor-segmentation-with-Kmeans-plusplus-clustering/blob/main/masking_images/11.png
