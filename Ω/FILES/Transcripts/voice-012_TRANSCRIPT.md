# Voice 012 — định nghĩa phép đo, chứng minh cải tiến và giới hạn thử nghiệm qua WAF

Nguồn: [Voice 012.m4a](file:///C:/Users/Admin/Documents/Collection/Data/Recording/Voice%20012.m4a)

Thời lượng: 00:47:33. ASR: large-v3 / cuda.

Trạng thái: đã rà văn bản; chờ nghe đối chiếu. Người nói chưa được xác định nếu không có ghi chú riêng.
Bản này bảo toàn thứ tự và nội dung nhận dạng; các đoạn nghi lỗi được giữ dấu vết để nghe lại.

## Đặt vấn đề và các tỷ lệ mất cân bằng

<a id="S00001"></a>
**[00:00:24 → 00:02:56] [Người nói?]** [nghe không rõ 00:00:24; cần đối chiếu] Hãy đăng ký kênh để ủng hộ kênh của mình nhé!

<a id="S00002"></a>
**[00:02:57 → 00:03:01] [Người nói?]** [nghe không rõ 00:02:57; cần đối chiếu] nhằm nâng cao và phát triển sự chiến học máy

<a id="S00003"></a>
**[00:03:01 → 00:03:05] [Người nói?]** và mục tiêu của em sẽ là các mô hình tấn công SQL Injection

<a id="S00004"></a>
**[00:03:05 → 00:03:10] [Người nói?]** thì em xin phép vào phần đặt vấn đề

<a id="S00005"></a>
**[00:03:10 → 00:03:16] [Người nói?]** hiện trạng là dữ liệu tấn công SQL Injection trong tập huấn luyện bị mất cân bằng nghiêm trọng

<a id="S00006"></a>
**[00:03:16 → 00:03:24] [Người nói?]** thường là lớp ATTACK sẽ có tỷ lệ ít hơn lớp NORMAL rất là nhiều

<a id="S00007"></a>
**[00:03:24 → 00:03:30] [Người nói?]** Nên mục tiêu của em là sẽ sinh ra thêm dữ liệu SQL, injection tổng hợp

<a id="S00008"></a>
**[00:03:30 → 00:03:38] [Người nói?]** Và vừa có thể giữ được đúng cấu trúc SQL, vừa có tính đa dạng và cũng sẽ cải thiện Recall Look Attack

<a id="S00009"></a>
**[00:03:39 → 00:03:42] [Người nói?]** Thì đầu tiên là em sẽ có 4 mô hình

<a id="S00010"></a>
**[00:03:42 → 00:03:46] [Người nói?]** [nghe không rõ 00:03:42; cần đối chiếu] Thì đầu tiên là nhóm phương pháp Baylight

<a id="S00011"></a>
**[00:03:46 → 00:03:48] [Người nói?]** [nghe không rõ 00:03:46; cần đối chiếu] Thì đại diện sẽ là SMOD

<a id="S00012"></a>
**[00:03:48 → 00:03:53] [Người nói?]** Thì cơ chế sẽ chỉ là nội sinh để có thể sinh ra dữ liệu

<a id="S00013"></a>
**[00:03:53 → 00:03:56] [Người nói?]** Tiếp theo là 3 nhóm tạo mô hình sinh dữ liệu

<a id="S00014"></a>
**[00:03:56 → 00:04:03] [Người nói?]** [nghe không rõ 00:03:56; cần đối chiếu] sẽ gồm có GAN cơ bản, CT GAN và mô hình SQL GAN

<a id="S00015"></a>
**[00:04:05 → 00:04:07] [Người nói?]** Đây là mô hình GAN cơ bản

<a id="S00016"></a>
**[00:04:07 → 00:04:15] [Người nói?]** Mô hình GAN cơ bản sẽ là sự đối kháng giữa Generator và Discriminator

<a id="S00017"></a>
**[00:04:17 → 00:04:22] [Người nói?]** Mô hình CT GAN thay vì nhận dữ liệu trực tiếp

<a id="S00018"></a>
**[00:04:22 → 00:04:32] [Người nói?]** thì sẽ biến đổi thành các dạng bảng để có thể dễ dàng tính toán gradient để có thể tìm hướng để cải thiện mô hình

<a id="S00019"></a>
**[00:04:32 → 00:04:38] [Người nói?]** Còn mô hình Sequence GAN thì là thay vì sử dụng dạng bảng thì sẽ sử dụng Policy Gradient

<a id="S00020"></a>
**[00:04:43 → 00:04:48] [Người nói?]** Tiếp theo là sẽ đến với các mức cân bằng mà em dùng để thử nghiệm

<a id="S00021"></a>
**[00:04:48 → 00:04:50] [Người nói?]** Em sẽ có 3 mức độ cân bằng

<a id="S00022"></a>
**[00:04:50 → 00:04:54] [Người nói?]** Mức cân bằng thì đầu tiên là mức độ nhẹ là 1 trên 10 và 1 trên 20

<a id="S00023"></a>
**[00:04:54 → 00:04:57] [Người nói?]** nghĩa là cứ có 1 mẫu tấn công

<a id="S00024"></a>
**[00:04:57 → 00:04:59] [Người nói?]** à cứ có 20 mẫu

<a id="S00025"></a>
**[00:04:59 → 00:05:02] [Người nói?]** bình thường thì sẽ có ít nhất 1 mẫu tấn công

<a id="S00026"></a>
**[00:05:02 → 00:05:04] [Người nói?]** và tương tự với 1 trên 50

<a id="S00027"></a>
**[00:05:04 → 00:05:04] [Người nói?]** 1 trên 100

<a id="S00028"></a>
**[00:05:04 → 00:05:06] [Người nói?]** 1 trên 200 và 1 trên 500

<a id="S00029"></a>
**[00:05:06 → 00:05:09] [Người nói?]** em sẽ chọn lấy

<a id="S00030"></a>
**[00:05:10 → 00:05:12] [Người nói?]** trong quá trình triển khai

<a id="S00031"></a>
**[00:05:12 → 00:05:14] [Người nói?]** thì em nhận thấy là

<a id="S00032"></a>
**[00:05:14 → 00:05:16] [Người nói?]** mẫu 1 trên 10 và 1 trên 20

<a id="S00033"></a>
**[00:05:16 → 00:05:18] [Người nói?]** thì có khá nhiều mẫu attack

<a id="S00034"></a>
**[00:05:18 → 00:05:21] [Người nói?]** và có tỷ lệ nó khá là tốt

<a id="S00035"></a>
**[00:05:21 → 00:05:23] [Người nói?]** trong khi đó là mẫu

<a id="S00036"></a>
**[00:05:23 → 00:05:25] [Người nói?]** 1 trên 50 và 1 trên 100

<a id="S00037"></a>
**[00:05:25 → 00:05:27] [Người nói?]** thì nó lại vừa cân bằng

<a id="S00038"></a>
**[00:05:28 → 00:05:30] [Người nói?]** nghĩa là nó có đủ độ khó khăn

<a id="S00039"></a>
**[00:05:30 → 00:05:31] [Người nói?]** để em có thể nhìn thấy được ra kết quả

<a id="S00040"></a>
**[00:05:31 → 00:05:33] [Người nói?]** thế nên trong mô hình thì em

<a id="S00041"></a>
**[00:05:33 → 00:05:35] [Người nói?]** ra loại, loại đi các mức độ nhẹ

<a id="S00042"></a>
**[00:05:35 → 00:05:37] [Người nói?]** và chỉ tập trung vào mức độ trung bình và cao

<a id="S00043"></a>
**[00:05:37 → 00:05:40] [Người nói?]** Thế thì hỏi là cái phân loại

<a id="S00044"></a>
**[00:05:40 → 00:05:42] [Người nói?]** nhẹ trung bình cao là em tự phân loại hay là

<a id="S00045"></a>
**[00:05:42 → 00:05:43] [Người nói?]** có bài làm ra không ạ?

<a id="S00046"></a>
**[00:05:44 → 00:05:45] [Người nói?]** Em tự phân loại

<a id="S00047"></a>
**[00:05:47 → 00:05:49] [Người nói?]** Vâng em tự phân loại bởi thứ nhất là

<a id="S00048"></a>
**[00:05:50 → 00:05:51] [Người nói?]** trong mô hình thì thường là

<a id="S00049"></a>
**[00:05:51 → 00:05:53] [Người nói?]** mức độ nhẹ là em lại không đủ dữ liệu

<a id="S00050"></a>
**[00:05:53 → 00:05:55] [Người nói?]** một số dạng tấn công ví dụ như là

<a id="S00051"></a>
**[00:05:58 → 00:06:03] [Người nói?]** Thì khi mà em chạy là nó không đủ dữ liệu để em có thể chạy được tỷ lệ 1 trên 10

<a id="S00052"></a>
**[00:06:03 → 00:06:09] [Người nói?]** Và khi mà em chạy thì em cảm thấy là tỷ lệ 1 trên 10, 1 trên 20 nó không đóng góp quá nhiều

<a id="S00053"></a>
**[00:06:09 → 00:06:12] [Người nói?]** Và nó lại khá tốn thời gian để training

<a id="S00054"></a>
**[00:06:12 → 00:06:16] [Người nói?]** Nên là em đã loại bỏ và chỉ tập trung vào 4 tỷ lệ còn lại

<a id="S00055"></a>
**[00:06:20 → 00:06:23] [Người nói?]** Các em có bài báo nào đang chia như thế này không?

<a id="S00056"></a>
**[00:06:23 → 00:06:32] [Người nói?]** em sẽ về tìm hiểu. Nhưng mà trong các bài báo em đọc thì em em chưa gặp bài báo nào chia như

<a id="S00057"></a>
**[00:06:32 → 00:06:40] [Người nói?]** tỷ lệ của em. Em sẽ về tìm hiểu thêm ạ. Thì tiếp theo là em sẽ dựa trên bốn chỉ số đánh giá chất

## Chỉ số chất lượng và khảo sát ban đầu

<a id="S00058"></a>
**[00:06:40 → 00:06:51] [Người nói?]** lượng ạ. Thì đầu tiên là structure ạ. Là kiểm tra xem là có dấu hiệu SQL không ạ. Thì mục tiêu của

<a id="S00059"></a>
**[00:06:51 → 00:06:57] [Người nói?]** em là kiểm tra xem là payload còn giữ được hình dạng của SQL injection hay không. Tiếp theo là

<a id="S00060"></a>
**[00:06:57 → 00:07:05] [Người nói?]** là độ độc nhất là em sẽ so khớp đến từng ký tự xem là bị trùng bao nhiêu phần trăm do với dữ liệu đổ vào

<a id="S00061"></a>
**[00:07:05 → 00:07:15] [Người nói?]** tiếp theo là Overlap là lần này em sẽ làm mở rộng hơn là không từng ký tự mà là các cụm từ, các cụm câu để xem là trùng bao nhiêu phần trăm

<a id="S00062"></a>
**[00:07:15 → 00:07:26] [Người nói?]** và cuối cùng là tính Recall để xem là liệu là có các cái phương pháp liệu có tăng hoặc là giảm bức Recall hay không

<a id="S00063"></a>
**[00:07:26 → 00:07:28] [Người nói?]** [nghe không rõ 00:07:26; cần đối chiếu] Có cái dấu gì Delta để trước dịp Recon?

<a id="S00064"></a>
**[00:07:31 → 00:07:34] [Người nói?]** [nghe không rõ 00:07:31; cần đối chiếu] Delta Recon là giữa Bayline trừ đi cả iWomen

<a id="S00065"></a>
**[00:07:34 → 00:07:38] [Người nói?]** [nghe không rõ 00:07:34; cần đối chiếu] là sự thay đổi của Recon

<a id="S00066"></a>
**[00:07:38 → 00:07:41] [Người nói?]** [nghe không rõ 00:07:38; cần đối chiếu] Delta Recon là gì? Mọi người biết không?

<a id="S00067"></a>
**[00:07:43 → 00:07:48] [Người nói?]** [nghe không rõ 00:07:43; cần đối chiếu] Em lấy Recon của mẫu tính đầu vào

<a id="S00068"></a>
**[00:07:48 → 00:07:55] [Người nói?]** [nghe không rõ 00:07:48; cần đối chiếu] sau đó trừ đi, sau khi mà sinh ra thì em lại tính thêm 1 lần Random Forest nữa để trừ đi

<a id="S00069"></a>
**[00:08:04 → 00:08:07] [Người nói?]** Đấy là tiếng Việt nhé, không phải tiếng Anh

<a id="S00070"></a>
**[00:08:12 → 00:08:18] [Người nói?]** Thì đây là em sẽ tiến hành khảo sát ban đầu

<a id="S00071"></a>
**[00:08:19 → 00:08:19] [Người nói?]** Quay lại trước

<a id="S00072"></a>
**[00:08:21 → 00:08:22] [Người nói?]** Rồi quay lại sau

<a id="S00073"></a>
**[00:08:22 → 00:08:24] [Người nói?]** [nghe không rõ 00:08:22; cần đối chiếu] Thì tự nhiên nhảy vào nguồn vụ tiên ra

<a id="S00074"></a>
**[00:08:24 → 00:08:27] [Người nói?]** Chỉ số đây đúng không?

<a id="S00075"></a>
**[00:08:27 → 00:08:28] [Người nói?]** Vâng

<a id="S00076"></a>
**[00:08:28 → 00:08:30] [Người nói?]** [nghe không rõ 00:08:28; cần đối chiếu] Lúc trước nó quả nguồn vụ tiên hoặc là gì?

<a id="S00077"></a>
**[00:08:32 → 00:08:33] [Người nói?]** Nó là trùng lập

<a id="S00078"></a>
**[00:08:33 → 00:08:35] [Người nói?]** [nghe không rõ 00:08:33; cần đối chiếu] Đây là nguồn vụ tiên

<a id="S00079"></a>
**[00:08:36 → 00:08:37] [Người nói?]** Cột này em đang chưa

<a id="S00080"></a>
**[00:08:40 → 00:08:41] [Người nói?]** [nghe không rõ 00:08:40; cần đối chiếu] Dự kiện nha

<a id="S00081"></a>
**[00:08:41 → 00:08:41] [Người nói?]** [nghe không rõ 00:08:41; cần đối chiếu] Dự kiện

<a id="S00082"></a>
**[00:08:41 → 00:08:44] [Người nói?]** Nó dựa vào AI nhiều quá

<a id="S00083"></a>
**[00:08:44 → 00:08:46] [Người nói?]** Thì tiếp

<a id="S00084"></a>
**[00:08:51 → 00:08:52] [Người nói?]** [nghe không rõ 00:08:51; cần đối chiếu] Vâng thì là nguồn vụ tiên

<a id="S00085"></a>
**[00:08:52 → 00:08:56] [Người nói?]** theo là em sẽ đề xuất là sẽ có 2 hướng cải thiện

<a id="S00086"></a>
**[00:08:57 → 00:08:58] [Người nói?]** à vâng

<a id="S00087"></a>
**[00:08:58 → 00:08:59] [Người nói?]** thì đầu tiên là

<a id="S00088"></a>
**[00:08:59 → 00:09:01] [Người nói?]** 3 mô hình đầu tiên

<a id="S00089"></a>
**[00:09:01 → 00:09:04] [Người nói?]** thì là do là chỉ là nội sinh

<a id="S00090"></a>
**[00:09:04 → 00:09:06] [Người nói?]** và cũng học

<a id="S00091"></a>
**[00:09:07 → 00:09:07] [Người nói?]** khá là

<a id="S00092"></a>
**[00:09:07 → 00:09:12] [Người nói?]** nó không cố gắng sinh ra dữ liệu mới

<a id="S00093"></a>
**[00:09:12 → 00:09:14] [Người nói?]** mà nó chỉ học từ dữ liệu cũ

<a id="S00094"></a>
**[00:09:14 → 00:09:16] [Người nói?]** nên là 3 mô hình đầu tiên

<a id="S00095"></a>
**[00:09:16 → 00:09:17] [Người nói?]** thì có structure

<a id="S00096"></a>
**[00:09:17 → 00:09:18] [Người nói?]** [nghe không rõ 00:09:17; cần đối chiếu] giống hệt S-Penetration

<a id="S00097"></a>
**[00:09:18 → 00:09:20] [Người nói?]** [nghe không rõ 00:09:18; cần đối chiếu] có mô hình sinh quần găng gốc

<a id="S00098"></a>
**[00:09:20 → 00:09:23] [Người nói?]** thì là do cố gắng học các mối quan hệ

<a id="S00099"></a>
**[00:09:23 → 00:09:30] [Người nói?]** nên là sinh ra dữ liệu thì có cấu trúc nó sẽ không thể được bằng 3 mềm còn lại

<a id="S00100"></a>
**[00:09:30 → 00:09:36] [Người nói?]** tuy nhiên là tỷ lệ sinh ra dữ liệu độc nhất thì nó sẽ cao hơn

<a id="S00101"></a>
**[00:09:40 → 00:09:42] [Người nói?]** hai cuộc cuối em sẽ về em chỉnh lại

<a id="S00102"></a>
**[00:09:42 → 00:09:44] [Người nói?]** cái này em chưa được chỉnh hết

<a id="S00103"></a>
**[00:09:44 → 00:09:49] [Người nói?]** nhưng mà em muốn nói là sau khi mà chạy xong khám xác ban đầu

<a id="S00104"></a>
**[00:09:49 → 00:09:55] [Người nói?]** thì em có thể nhận thấy là 3 mềm còn lại là về nếu mà tiếp tục sử dụng

<a id="S00105"></a>
**[00:09:55 → 00:10:00] [Người nói?]** Thì nó cũng sẽ chỉ có khả năng là dựa vào bộ

<a id="S00106"></a>
**[00:10:00 → 00:10:02] [Người nói?]** dữ liệu cũ và nó không có khả năng sinh ra dữ liệu có tính mới

<a id="S00107"></a>
**[00:10:02 → 00:10:06] [Người nói?]** Và rất dễ có thể bị bắt và có thể bị đánh chặn

<a id="S00108"></a>
**[00:10:06 → 00:10:08] [Người nói?]** [nghe không rõ 00:10:06; cần đối chiếu] Trong khi đó là mô hình si quần gan

<a id="S00109"></a>
**[00:10:08 → 00:10:14] [Người nói?]** Thì là tuy là hiện tại nó không sinh ra được mẫu có cấu trúc SQL

<a id="S00110"></a>
**[00:10:14 → 00:10:17] [Người nói?]** Nhưng mà nó lại sinh ra các mẫu có độ độc nhất cao

<a id="S00111"></a>
**[00:10:17 → 00:10:26] [Người nói?]** [nghe không rõ 00:10:17; cần đối chiếu] Nên là em sử dụng mô hình si quần gan và cố gắng cải tiến để tăng khả năng sinh dữ liệu của mô hình si quần gan

## Kịch bản dữ liệu và cải tiến thuật toán

<a id="S00112"></a>
**[00:10:26 → 00:10:31] [Người nói?]** Thì em có 2 hướng đề xuất

<a id="S00113"></a>
**[00:10:31 → 00:10:36] [Người nói?]** Thì đầu tiên là sẽ cải thiện dữ liệu là phân phối lại dữ liệu đầu vào

<a id="S00114"></a>
**[00:10:36 → 00:10:41] [Người nói?]** Thì đầu tiên là em sẽ chia ra làm 3 trường hợp tấn công

<a id="S00115"></a>
**[00:10:41 → 00:10:47] [Người nói?]** [nghe không rõ 00:10:41; cần đối chiếu] À 4 trường hợp tấn công thì sẽ gồm có Union, Boland, Time và Erin

<a id="S00116"></a>
**[00:10:47 → 00:10:50] [Người nói?]** Em sẽ tách input theo từng đặc trưng để có

<a id="S00117"></a>
**[00:10:50 → 00:10:56] [Người nói?]** Theo từng family để mô hình tạo sinh có thể học được đúng pattern của từng loại

<a id="S00118"></a>
**[00:10:56 → 00:11:00] [Người nói?]** [nghe không rõ 00:10:56; cần đối chiếu] Tránh bị trống chéo giữa các family heat train

<a id="S00119"></a>
**[00:11:00 → 00:11:04] [Người nói?]** Tiếp theo là em sẽ chuẩn hóa độ dài input về các khoảng hợp lý

<a id="S00120"></a>
**[00:11:06 → 00:11:09] [Người nói?]** Tránh cho việc generator học lệch theo một vài mẫu hiếm

<a id="S00121"></a>
**[00:11:09 → 00:11:12] [Người nói?]** Thiện tiện thứ 2 là hướng thuật toán

<a id="S00122"></a>
**[00:11:12 → 00:11:20] [Người nói?]** Mục tiêu của em là muốn mô hình lần này sẽ học đúng cấu trúc SQL thay vì chỉ đánh lừa discriminator

<a id="S00123"></a>
**[00:11:20 → 00:11:27] [Người nói?]** Tiếp theo em sẽ tokenize từng unit riêng thay vì tách từng ký tự trần

<a id="S00124"></a>
**[00:11:27 → 00:11:30] [Người nói?]** Giúp generator học pháp dễ hơn

<a id="S00125"></a>
**[00:11:30 → 00:11:39] [Người nói?]** Và cuối cùng là em sẽ bổ sung phương pháp chấm điểm payload với mục tiêu là kiểm tra dữ liệu sinh ra có đúng khủng pháp SQL không

<a id="S00126"></a>
**[00:11:39 → 00:11:42] [Người nói?]** Và em sẽ cộng thẳng reward này và update vào generator

<a id="S00127"></a>
**[00:11:45 → 00:11:48] [Người nói?]** Đầu tiên em sẽ đến với 6 kịch bản cải thiện dữ liệu

<a id="S00128"></a>
**[00:11:48 → 00:12:04] [Người nói?]** [nghe không rõ 00:11:48; cần đối chiếu] Thì trong đó kịch bản A là em sẽ vẫn giữ nguyên phương phong cách em lựa chọn cũ sau lúc chạy đồ vào để coi như là mốc ban đầu

<a id="S00129"></a>
**[00:12:04 → 00:12:07] [Người nói?]** Tiếp theo là em sẽ chọn ưu tiên là các ký tự ngắn

<a id="S00130"></a>
**[00:12:07 → 00:12:12] [Người nói?]** C là em sẽ ưu tiên độ dài phổ biến, trung vị

<a id="S00131"></a>
**[00:12:12 → 00:12:22] [Người nói?]** D là em sẽ random không hoàn lại trong vùng trung vị

<a id="S00132"></a>
**[00:12:22 → 00:12:27] [Người nói?]** [nghe không rõ 00:12:22; cần đối chiếu] Em sẽ bỏ 25% đầu và 75% cuối và chỉ tập trung vào 50% ở giữa

<a id="S00133"></a>
**[00:12:27 → 00:12:30] [Người nói?]** Tiếp theo là em sẽ random cho toàn bộ dữ liệu

<a id="S00134"></a>
**[00:12:30 → 00:12:36] [Người nói?]** Và em sẽ giữ chỉ số random trong toàn bộ mô hình này là 88

<a id="S00135"></a>
**[00:12:37 → 00:12:39] [Người nói?]** Để đảm bảo là tính đồng nhất

<a id="S00136"></a>
**[00:12:39 → 00:12:48] [Người nói?]** [ASR cần nghe lại] Và cuối cùng là em sẽ chọn theo phương án...

<a id="S00137"></a>
**[00:12:48 → 00:12:51] [Người nói?]** [ASR cần nghe lại] Em sẽ chọn theo phương án...

<a id="S00138"></a>
**[00:12:51 → 00:12:52] [Người nói?]** [ASR cần nghe lại] Em chọn theo...

<a id="S00139"></a>
**[00:12:53 → 00:12:56] [Người nói?]** [ASR cần nghe lại] Để một tí ạ. Cái này em đang...

<a id="S00140"></a>
**[00:12:56 → 00:12:57] [Người nói?]** [ASR cần nghe lại] Để tiếng Anh em sẽ viết nó ạ.

<a id="S00141"></a>
**[00:12:57 → 00:13:04] [Người nói?]** [nghe không rõ 00:12:57; cần đối chiếu] Nhưng mà em muốn nói là cái phương pháp N này là em sẽ cố gắng chọn để có thể lấy được đa dạng nhất có thể các cái tí tự.

<a id="S00142"></a>
**[00:13:05 → 00:13:07] [Người nói?]** [ASR cần nghe lại] Thì em sẽ chọn theo phương án...

<a id="S00143"></a>
**[00:13:08 → 00:13:10] [Người nói?]** [ASR cần nghe lại] Chọn theo phương án 3 gram.

<a id="S00144"></a>
**[00:13:17 → 00:13:19] [Người nói?]** Tiếp theo là hướng cải thiện thuật toán

<a id="S00145"></a>
**[00:13:19 → 00:13:26] [Người nói?]** sẽ có 3 hướng, đầu tiên là em sẽ tokenize hóa các dữ liệu SQL

<a id="S00146"></a>
**[00:13:30 → 00:13:35] [Người nói?]** thay vì để những dữ liệu có chung ý nghĩa

<a id="S00147"></a>
**[00:13:35 → 00:13:40] [Người nói?]** em sẽ tokenize hóa để tránh việc mô hình vốn học những mẫu

<a id="S00148"></a>
**[00:13:42 → 00:13:45] [Người nói?]** sinh ra những mẫu đặc biệt mà không có ý nghĩa

<a id="S00149"></a>
**[00:13:46 → 00:13:58] [Người nói?]** [nghe không rõ 00:13:46; cần đối chiếu] Tiếp theo là tăng Pre-Chain, em sẽ tăng Pre-Chain từ 120 lên 160 để tránh bị Collapse và cũng làm cho mô hình Pre-Chain Trayator vững chãi hơn

<a id="S00150"></a>
**[00:13:58 → 00:14:01] [Người nói?]** Và cuối cùng là em sẽ tăng thưởng điểm Rewards

<a id="S00151"></a>
**[00:14:05 → 00:14:11] [Người nói?]** [nghe không rõ 00:14:05; cần đối chiếu] Thay vì em để 100% là Disc Creator Rewards thì em sẽ để 70% là Disc Miner Rewards

<a id="S00152"></a>
**[00:14:11 → 00:14:18] [Người nói?]** [nghe không rõ 00:14:11; cần đối chiếu] và 30% còn lại sẽ là SQL SPA REWARD để có thể mong dữ liệu sinh ra được

<a id="S00153"></a>
**[00:14:18 → 00:14:20] [Người nói?]** có cấu trúc SQL hơn ạ

<a id="S00154"></a>
**[00:14:20 → 00:14:26] [Người nói?]** và đây là tổng là sẽ có 8 kịch bản

<a id="S00155"></a>
**[00:14:26 → 00:14:27] [Người nói?]** 2 mục 3

<a id="S00156"></a>
**[00:14:27 → 00:14:35] [Người nói?]** thì là sẽ có là 8 kịch bản

<a id="S00157"></a>
**[00:14:36 → 00:14:44] [Người nói?]** thì sau khi mà áp dụng tất cả các kịch bản đồng thời

<a id="S00158"></a>
**[00:14:44 → 00:14:47] [Người nói?]** thì em sẽ có các cái đánh giá

<a id="S00159"></a>
**[00:14:47 → 00:14:51] [Người nói?]** Đây là mô hình mà có điểm cấu trúc cao nhất

<a id="S00160"></a>
**[00:14:51 → 00:14:53] [Người nói?]** [nghe không rõ 00:14:51; cần đối chiếu] là mô hình thiên nhiên

<a id="S00161"></a>
**[00:14:54 → 00:14:55] [Người nói?]** [nghe không rõ 00:14:54; cần đối chiếu] Bây giờ lại thành Dominant rồi

<a id="S00162"></a>
**[00:14:55 → 00:14:58] [Người nói?]** [nghe không rõ 00:14:55; cần đối chiếu] Bây giờ lại Dominant rồi

<a id="S00163"></a>
**[00:14:58 → 00:15:03] [Người nói?]** [nghe không rõ 00:14:58; cần đối chiếu] Nếu mà tìm đồ gì thì tìm đồ quý đấy nhé

<a id="S00164"></a>
**[00:15:04 → 00:15:04] [Người nói?]** Vâng

## Kết quả, payload và giới hạn trên từng nhóm

<a id="S00165"></a>
**[00:15:08 → 00:15:16] [Người nói?]** Đây là các cái mô hình cấu trúc

<a id="S00166"></a>
**[00:15:16 → 00:15:18] [Người nói?]** các cái kết quả mô hình ạ

<a id="S00167"></a>
**[00:15:18 → 00:15:19] [Người nói?]** thì ở đây sẽ

<a id="S00168"></a>
**[00:15:20 → 00:15:23] [Người nói?]** [nghe không rõ 00:15:20; cần đối chiếu] trong mô hình này thì kịch bản là BV8

<a id="S00169"></a>
**[00:15:23 → 00:15:27] [Người nói?]** là kịch bản mà chiếm gần như đa số

<a id="S00170"></a>
**[00:15:27 → 00:15:36] [Người nói?]** [nghe không rõ 00:15:27; cần đối chiếu] đa số đứng top đầu như đa số trong các lĩnh vực trong đó sẽ có hai kịch bản là cũng đứng top là

<a id="S00171"></a>
**[00:15:36 → 00:15:46] [Người nói?]** [nghe không rõ 00:15:36; cần đối chiếu] sẽ gồm có Bolin dv7 và Union dv2 thì sau đó dựa vào thông số trên ạ thì em đề xuất là cộng cộng

<a id="S00172"></a>
**[00:15:46 → 00:15:55] [Người nói?]** [nghe không rõ 00:15:46; cần đối chiếu] là sẽ có 11 kịch bản em lựa chọn để chạy ạ thì đầu tiên là ứng viên thứ nhất là sẽ là dv8 như em

<a id="S00173"></a>
**[00:15:56 → 00:16:04] [Người nói?]** Tiếp theo là ứng viên số 2 là các kịch bản cũng nằm ở trong top đã được đề xuất ở bên trên

<a id="S00174"></a>
**[00:16:04 → 00:16:10] [Người nói?]** Và ứng viên số 3 là em sẽ chọn để có thể lấy mẫu để có thể so sánh

<a id="S00175"></a>
**[00:16:10 → 00:16:21] [Người nói?]** [nghe không rõ 00:16:10; cần đối chiếu] Thì ở Poland, trong kết quả thực tế là mô hình V8 và V7 là chiếm vị trí rất là cao và bỏ xa

<a id="S00176"></a>
**[00:16:21 → 00:16:25] [Người nói?]** So với các kết quả khác

<a id="S00177"></a>
**[00:16:25 → 00:16:26] [Người nói?]** Em sẽ chọn lấy

<a id="S00178"></a>
**[00:16:27 → 00:16:29] [Người nói?]** Phần top 3 để em ưu tiên

<a id="S00179"></a>
**[00:16:29 → 00:16:30] [Người nói?]** Tính ngẫu nhiên

<a id="S00180"></a>
**[00:16:30 → 00:16:34] [Người nói?]** [nghe không rõ 00:16:30; cần đối chiếu] Còn đối với kịch bản Aaron

<a id="S00181"></a>
**[00:16:35 → 00:16:36] [Người nói?]** Lỗi thì em sẽ chọn

<a id="S00182"></a>
**[00:16:36 → 00:16:38] [Người nói?]** V4 bởi vì là

<a id="S00183"></a>
**[00:16:38 → 00:16:40] [Người nói?]** Mũ hình này cũng nằm trong top 3

<a id="S00184"></a>
**[00:16:40 → 00:16:41] [Người nói?]** Và cũng có chỉ số ổn định

<a id="S00185"></a>
**[00:16:41 → 00:16:43] [Người nói?]** Tương tự với cả A

<a id="S00186"></a>
**[00:16:43 → 00:16:46] [Người nói?]** V8 thì đối với kịch bản Time

<a id="S00187"></a>
**[00:16:46 → 00:16:47] [Người nói?]** Là nó đặc biệt hơn

<a id="S00188"></a>
**[00:16:47 → 00:16:49] [Người nói?]** Bởi vì là nó cần phải

<a id="S00189"></a>
**[00:16:49 → 00:16:50] [Người nói?]** Nó cần phải học được

<a id="S00190"></a>
**[00:16:50 → 00:16:55] [Người nói?]** Nó cần phải biết được chính xác được

<a id="S00191"></a>
**[00:16:55 → 00:17:03] [Người nói?]** được cả là các ngữ pháp cho từng database riêng nên là trong kịch bản Time này thì chỉ có 3 mô

<a id="S00192"></a>
**[00:17:03 → 00:17:12] [Người nói?]** hình là không bị collapse đến cuối. Và cuối cùng đến kịch bản Union thì là em sẽ chọn Fv3 là ưu

<a id="S00193"></a>
**[00:17:12 → 00:17:21] [Người nói?]** tiên sự đa dạng. Đây là kết quả cuối cùng. Đầu tiên là kết quả với các mô hình cơ bản, 4 mô

<a id="S00194"></a>
**[00:17:21 → 00:17:34] [Người nói?]** Mô hình cơ bản ban đầu thì ở đây là các mô hình, 3 mô hình đầu thì vẫn như cũ là cũng sẽ có tỷ lệ học được cấu trúc SQL rất là cao.

<a id="S00195"></a>
**[00:17:34 → 00:17:53] [Người nói?]** Tuy nhiên là độ unique của nó là không hề tăng và chỉ số recall cũng không tăng quá nhiều và có một vài mô hình bị giảm rất là cao.

<a id="S00196"></a>
**[00:17:53 → 00:18:01] [Người nói?]** Trong khi đó còn các mô hình mà em đề xuất

<a id="S00197"></a>
**[00:18:01 → 00:18:06] [Người nói?]** Thì em đưa ra kết quả của top 5 mô hình tốt nhất

<a id="S00198"></a>
**[00:18:06 → 00:18:11] [Người nói?]** Thì là mô hình DV

<a id="S00199"></a>
**[00:18:11 → 00:18:15] [Người nói?]** [nghe không rõ 00:18:11; cần đối chiếu] Nếu mà sử dụng kịch bản DV8 cho yêu nhiệt

<a id="S00200"></a>
**[00:18:15 → 00:18:17] [Người nói?]** Thì sẽ là tốt nhất có thể

<a id="S00201"></a>
**[00:18:17 → 00:18:20] [Người nói?]** [nghe không rõ 00:18:17; cần đối chiếu] Tương tự với cả Bolin là DV7

<a id="S00202"></a>
**[00:18:20 → 00:18:22] [Người nói?]** [nghe không rõ 00:18:20; cần đối chiếu] Time là DV8

<a id="S00203"></a>
**[00:18:22 → 00:18:23] [Người nói?]** [nghe không rõ 00:18:22; cần đối chiếu] Error là DV3

<a id="S00204"></a>
**[00:18:23 → 00:18:28] [Người nói?]** Thì em kết luận là

<a id="S00205"></a>
**[00:18:29 → 00:18:42] [Người nói?]** Đối với các mô hình cơ bản, độ độc nhất sẽ bị giảm dần nếu như càng tăng mức tỷ lệ càng khắc nhiệt thì độ unique sẽ càng càng giảm

<a id="S00206"></a>
**[00:18:44 → 00:18:48] [Người nói?]** Điểm cấu trúc sẽ luôn rất cao nhưng tỷ lệ trùng lọc cũng đồng thời rất cao

<a id="S00207"></a>
**[00:18:49 → 00:18:53] [Người nói?]** [nghe không rõ 00:18:49; cần đối chiếu] Còn so sánh giữa mô hình si quần góc và si quần cải tiến của em

<a id="S00208"></a>
**[00:18:56 → 00:18:58] [Người nói?]** lần này là em đã thật sự sinh ra chuỗi mới

<a id="S00209"></a>
**[00:18:58 → 00:19:03] [Người nói?]** và bản gốc thì structure đã sụp đổ và bị collapse

<a id="S00210"></a>
**[00:19:03 → 00:19:05] [Người nói?]** khi mà tiến đến tới tỷ lệ 1 trên 50

<a id="S00211"></a>
**[00:19:06 → 00:19:10] [Người nói?]** còn bản của em là vẫn có thể sinh ra dữ liệu

<a id="S00212"></a>
**[00:19:10 → 00:19:12] [Người nói?]** và khả năng cân bằng tốt hơn

<a id="S00213"></a>
**[00:19:12 → 00:19:14] [Người nói?]** và trong đó là sẽ có 2 kịch bản tốt nhất

<a id="S00214"></a>
**[00:19:14 → 00:19:18] [Người nói?]** [nghe không rõ 00:19:14; cần đối chiếu] đó chính là Union thì sẽ sử dụng kịch bản DV8

<a id="S00215"></a>
**[00:19:18 → 00:19:21] [Người nói?]** [nghe không rõ 00:19:18; cần đối chiếu] và Bowden là kịch bản DV7

<a id="S00216"></a>
**[00:19:21 → 00:19:27] [Người nói?]** thì đây cuối cùng là em sẽ đưa vào mô hình tương lượng thực tế

<a id="S00217"></a>
**[00:19:27 → 00:19:29] [Người nói?]** còn đây là các thiết lập của em

<a id="S00218"></a>
**[00:19:29 → 00:19:38] [Người nói?]** [nghe không rõ 00:19:29; cần đối chiếu] thì là khi mà đưa vào thì là sẽ có tỷ lệ bị chặn là 70% trên toàn bộ

<a id="S00219"></a>
**[00:19:38 → 00:19:41] [Người nói?]** [nghe không rõ 00:19:38; cần đối chiếu] và tỷ lệ không bị chặn là 3%

<a id="S00220"></a>
**[00:19:41 → 00:19:47] [Người nói?]** mà sau khi mà em đọc em xem các cái kết quả thực tế

<a id="S00221"></a>
**[00:19:47 → 00:19:54] [Người nói?]** thì em nhận ra là hầu hết cái tỷ lệ không bị chặn này là do là nó dịch ra dữ liệu nhiễu

<a id="S00222"></a>
**[00:19:54 → 00:19:56] [Người nói?]** Nó thật sự không có tác dụng tấn công

<a id="S00223"></a>
**[00:19:56 → 00:19:58] [Người nói?]** Nên nó có khả năng vượt qua được tường lửa

<a id="S00224"></a>
**[00:19:58 → 00:19:59] [Người nói?]** Thế nên là em sẽ

<a id="S00225"></a>
**[00:20:00 → 00:20:07] [Người nói?]** show luôn dữ liệu payload thực tế để phân tích ạ.

<a id="S00226"></a>
**[00:20:07 → 00:20:17] [Người nói?]** [nghe không rõ 00:20:07; cần đối chiếu] Thì đây là đối với mô hình SMODE ạ. Thì ở đây các mẫu sinh ra rất là tốt ạ.

<a id="S00227"></a>
**[00:20:17 → 00:20:25] [Người nói?]** Tuy nhiên là nó sinh ra khá nhiều các mẫu có khoảng trắng và một vài mẫu bị lệch kỹ thuật ạ.

<a id="S00228"></a>
**[00:20:25 → 00:20:31] [Người nói?]** Nghĩa là nếu mà đối với một số mẫu mà yêu cầu về ngữ pháp khá là cao

<a id="S00229"></a>
**[00:20:32 → 00:20:36] [Người nói?]** Ví dụ như Timeline chẳng hạn là rất dễ có thể bị lệch kỹ thuật

<a id="S00230"></a>
**[00:20:36 → 00:20:40] [Người nói?]** Bởi vì nó chỉ biết ghép chứ nó không học được các mối quan hệ

<a id="S00231"></a>
**[00:20:40 → 00:20:43] [Người nói?]** Thế tương tự

<a id="S00232"></a>
**[00:20:43 → 00:20:45] [Người nói?]** [nghe không rõ 00:20:43; cần đối chiếu] Tôi có thể hỏi cái điểm chéo Warp là gì?

<a id="S00233"></a>
**[00:20:46 → 00:20:51] [Người nói?]** Trong này là điểm 100 là đánh giá

<a id="S00234"></a>
**[00:20:51 → 00:20:55] [Người nói?]** Đây là điểm đánh giá xem là có phải là mẫu SQL không

<a id="S00235"></a>
**[00:20:55 → 00:20:59] [Người nói?]** [nghe không rõ 00:20:55; cần đối chiếu] Còn Warp ở đây là kết quả trả về sau khi mà đưa vào tấn công

<a id="S00236"></a>
**[00:20:59 → 00:21:03] [Người nói?]** [nghe không rõ 00:20:59; cần đối chiếu] Là HTTP 403 ở đây là không có kết quả trả về

<a id="S00237"></a>
**[00:21:23 → 00:21:38] [Người nói?]** [ASR cần nghe lại] Tiếp theo là đối với mô hình gan thì nó cũng bị giống như với mô hình smooth thì nó cũng có bít trùng lặp

<a id="S00238"></a>
**[00:21:38 → 00:21:41] [Người nói?]** và một số các cái mô hình

<a id="S00239"></a>
**[00:21:41 → 00:21:43] [Người nói?]** à một số các cái phan đi

<a id="S00240"></a>
**[00:21:43 → 00:21:45] [Người nói?]** mà yêu cầu ngữ pháp cao

<a id="S00241"></a>
**[00:21:45 → 00:21:47] [Người nói?]** thì là nó cũng không học được

<a id="S00242"></a>
**[00:21:47 → 00:21:49] [Người nói?]** nó cũng không học được mà

<a id="S00243"></a>
**[00:21:49 → 00:21:51] [Người nói?]** nó chỉ biết lặp lại

<a id="S00244"></a>
**[00:21:51 → 00:21:54] [Người nói?]** mà nó không học được mối quan hệ ngữ pháp

<a id="S00245"></a>
**[00:21:54 → 00:21:57] [Người nói?]** đối với mô hình CT gan

<a id="S00246"></a>
**[00:21:57 → 00:22:00] [Người nói?]** thì là cũng bị vấn đề như vậy

<a id="S00247"></a>
**[00:22:00 → 00:22:02] [Người nói?]** còn mô hình CT gan

<a id="S00248"></a>
**[00:22:02 → 00:22:04] [Người nói?]** thì như ở trên thông số

<a id="S00249"></a>
**[00:22:04 → 00:22:07] [Người nói?]** là nó thật sự đã học được

<a id="S00250"></a>
**[00:22:07 → 00:22:08] [Người nói?]** cấu trúc nhưng mà khi mà

<a id="S00251"></a>
**[00:22:08 → 00:22:10] [Người nói?]** càng ngày mà càng khắc nhiệt

<a id="S00252"></a>
**[00:22:10 → 00:22:17] [Người nói?]** Kỷ lệ khắc nhật thì nó sẽ cố gắng tìm tới những cái mẫu mà cơ bản và càng ngắn bởi vì nó ưu tiên an toàn.

<a id="S00253"></a>
**[00:22:19 → 00:22:23] [Người nói?]** Mã 200 là vượt qua được ạ.

<a id="S00254"></a>
**[00:22:24 → 00:22:31] [Người nói?]** Có không? Vượt qua nhưng mà nó không có ý nghĩa gì cả đúng không?

<a id="S00255"></a>
**[00:22:34 → 00:22:41] [Người nói?]** [nghe không rõ 00:22:34; cần đối chiếu] Ví dụ như là mã đầu là có tấn công được ạ.

<a id="S00256"></a>
**[00:22:42 → 00:22:52] [Người nói?]** Như bắt đầu có tấn công được nhưng mà nó sẽ chỉ cố gắng là sinh ra những mẫu siêu ngắn bởi vì nó bị collapse và cố gắng ép tới những cái trường hợp mà thật sự an toàn

<a id="S00257"></a>
**[00:22:52 → 00:23:07] [Người nói?]** [nghe không rõ 00:22:52; cần đối chiếu] Thì đến cuối cùng là mô hình cải tiến là nó đã sửa được những gì mà mô hình si quần gan gốc của em gặp vấn đề là nó đã sinh ra dữ liệu dài hơn

<a id="S00258"></a>
**[00:23:07 → 00:23:14] [Người nói?]** Tuy nhiên là nó cũng khi mà gặp những cái kịch bản family mà nó yêu cầu mức pháp quá khắc khe

<a id="S00259"></a>
**[00:23:14 → 00:23:20] [Người nói?]** [nghe không rõ 00:23:14; cần đối chiếu] như là Time và Alien thì nó cũng không học được củ pháp ạ.

<a id="S00260"></a>
**[00:23:20 → 00:23:25] [Người nói?]** Thế nên là trong toàn bộ mô hình của em chỉ có đúng 2 mô hình

<a id="S00261"></a>
**[00:23:25 → 00:23:29] [Người nói?]** [nghe không rõ 00:23:25; cần đối chiếu] là DV8 đối với Poland và DV7 đối với Union

<a id="S00262"></a>
**[00:23:29 → 00:23:34] [Người nói?]** là thật sự sinh ra kết quả tốt và có khả năng ứng dụng được đấy ạ.

<a id="S00263"></a>
**[00:23:34 → 00:23:38] [Người nói?]** [nghe không rõ 00:23:34; cần đối chiếu] Còn 11 kịch bản còn lại thì thật sự là không có kịch bản nào

<a id="S00264"></a>
**[00:23:38 → 00:23:41] [Người nói?]** có thể sinh ra dữ liệu mà có thể sử dụng được.

<a id="S00265"></a>
**[00:23:45 → 00:23:54] [Người nói?]** [nghe không rõ 00:23:45; cần đối chiếu] sẽ đưa đến quyết luận là mô hình của em đã giải quyết được những vấn đề mà mô hình SQL GAN cũ đã gặp phải

<a id="S00266"></a>
**[00:23:54 → 00:24:03] [Người nói?]** [nghe không rõ 00:23:54; cần đối chiếu] nhưng mà tuy nhiên trên thực tế là sẽ chỉ có 2 kịch bản Union và Boland là nó thật sự học được

<a id="S00267"></a>
**[00:24:03 → 00:24:10] [Người nói?]** do là yếu tố yêu cầu về ngữ pháp của nó sẽ thấp hơn so với 2 family còn lại

<a id="S00268"></a>
**[00:24:10 → 00:24:16] [Người nói?]** và 2 family còn lại là kết quả của em là không có quá nhiều cải thiện

<a id="S00269"></a>
**[00:24:16 → 00:25:42] [Người nói?]** [nghe không rõ 00:24:16; cần đối chiếu] Cảm ơn các bạn đã theo dõi và hẹn gặp lại.

<a id="S00270"></a>
**[00:26:13 → 00:26:49] [Người nói?]** [nghe không rõ 00:26:13; cần đối chiếu] Hãy subscribe cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

## Góp ý: chứng minh từng thay đổi và vẽ đúng mô hình

<a id="S00271"></a>
**[00:26:53 → 00:27:14] [Người nói?]** Nó là kết hợp giữa cả là dữ liệu và thuật toán, dữ liệu sẽ là kịch bản B và D, còn thuật toán là kịch bản B8, thì em có đưa 2 cái bản ở đây.

<a id="S00272"></a>
**[00:27:16 → 00:27:26] [Người nói?]** [nghe không rõ 00:27:16; cần đối chiếu] Nếu như mấy loại xe cuốn gan bình thường, xe cuốn gan và xe cuốn gan ở đằng kia thì nó là cái gì mà mua hay không?

<a id="S00273"></a>
**[00:27:27 → 00:27:33] [Người nói?]** Em xin lỗi thầy, nhưng em chưa ý thức được câu hỏi của thầy ạ.

<a id="S00274"></a>
**[00:27:34 → 00:27:42] [Người nói?]** Thì nghĩa là bây giờ em nên viết ra tổng hợp là kịch bản DV8 và DV7 của em là thật sự có những cái gì hay là gì nào?

<a id="S00275"></a>
**[00:27:42 → 00:27:46] [Người nói?]** [nghe không rõ 00:27:42; cần đối chiếu] Không phải, em dở lại cái mô hình của cái xe cuốn gan.

<a id="S00276"></a>
**[00:27:47 → 00:27:49] [Người nói?]** Rồi, đây.

<a id="S00277"></a>
**[00:27:50 → 00:27:52] [Người nói?]** Đấy, trong mô hình này thì em đã tìm cái gì?

<a id="S00278"></a>
**[00:27:52 → 00:27:57] [Người nói?]** Thì trong mô hình này, em cải thiện 3 cái

<a id="S00279"></a>
**[00:27:57 → 00:28:03] [Người nói?]** [nghe không rõ 00:27:57; cần đối chiếu] Đầu tiên là em sẽ tăng thông số pre-chain lên từ 120 lên 160

<a id="S00280"></a>
**[00:28:04 → 00:28:10] [Người nói?]** Để cho mô hình generator sẽ có vững hơn để tránh bị collapse

<a id="S00281"></a>
**[00:28:10 → 00:28:18] [Người nói?]** Tiếp theo là em sẽ có reward thay vì để 100% là distributor reward

<a id="S00282"></a>
**[00:28:18 → 00:28:21] [Người nói?]** thì em sẽ để là 70% thôi ạ

<a id="S00283"></a>
**[00:28:21 → 00:28:24] [Người nói?]** và em sẽ thêm 30% reward của SQL

<a id="S00284"></a>
**[00:28:24 → 00:28:28] [Người nói?]** để mong là mô hình có sinh ra được cấu trúc dòng SQL hơn ạ

<a id="S00285"></a>
**[00:28:31 → 00:28:33] [Người nói?]** Ví dụ như em bảo là có 3 cải tiến

<a id="S00286"></a>
**[00:28:33 → 00:28:39] [Người nói?]** thì cải tiến thứ nhất thì có thử và ra kết quả nó hơn so với phía cũ không?

<a id="S00287"></a>
**[00:28:40 → 00:28:44] [Người nói?]** Cải tiến thứ 2 thì có thử và ra kết quả nó hơn so với phía cũ không?

<a id="S00288"></a>
**[00:28:44 → 00:28:47] [Người nói?]** Ờ em có ạ

<a id="S00289"></a>
**[00:28:47 → 00:28:50] [Người nói?]** Thì em sẽ chạy toàn bộ luôn ạ

<a id="S00290"></a>
**[00:28:50 → 00:28:52] [Người nói?]** là em sẽ áp dụng tổng cộng

<a id="S00291"></a>
**[00:28:52 → 00:28:57] [Người nói?]** [nghe không rõ 00:28:52; cần đối chiếu] Từ từ đã đi đây, tôi muốn hỏi là cái sức khỏe gian của em, em nghĩ cái gì ý đâu ạ?

<a id="S00292"></a>
**[00:28:58 → 00:29:01] [Người nói?]** Em không vẽ vào mô hình ở đây ạ.

<a id="S00293"></a>
**[00:29:01 → 00:29:02] [Người nói?]** [nghe không rõ 00:29:01; cần đối chiếu] Thầy nhập tóc hiểu được.

<a id="S00294"></a>
**[00:29:03 → 00:29:04] [Người nói?]** À rồi, em hiểu như thế.

<a id="S00295"></a>
**[00:29:09 → 00:29:10] [Người nói?]** [nghe không rõ 00:29:09; cần đối chiếu] Nó là sức khỏe gian đúng không?

<a id="S00296"></a>
**[00:29:10 → 00:29:12] [Người nói?]** [nghe không rõ 00:29:10; cần đối chiếu] Sức khỏe gian đẹp đến là không.

<a id="S00297"></a>
**[00:29:12 → 00:29:13] [Người nói?]** Chưa có đúng không ạ?

<a id="S00298"></a>
**[00:29:13 → 00:29:14] [Người nói?]** Vâng ạ, em chưa có mô hình.

<a id="S00299"></a>
**[00:29:15 → 00:29:19] [Người nói?]** [nghe không rõ 00:29:15; cần đối chiếu] Thì cái thật chính của em là cái phần trình bày về cái sức khỏe nguồn cảnh thì em phải nói rõ là phải cải thiện như gì.

<a id="S00300"></a>
**[00:29:20 → 00:29:23] [Người nói?]** Trước cải thiện như thế này và sau cải thiện kết quả như thế nào.

<a id="S00301"></a>
**[00:29:23 → 00:29:32] [Người nói?]** Kết quả bình thường là bạn có sinh ra như thế này và sau khi sinh ra như thế này, các thầy chỉ có đợi ở đấy thôi.

<a id="S00302"></a>
**[00:29:32 → 00:29:41] [Người nói?]** [nghe không rõ 00:29:32; cần đối chiếu] Có bảo vệ, có những lời không để lên nữa thì tốt để lấy trong đó. Chưa hiểu được sinh ra là gì, sao thì hiểu sao.

<a id="S00303"></a>
**[00:29:46 → 00:29:47] [Người nói?]** Cảm ơn thầy.

<a id="S00304"></a>
**[00:29:50 → 00:29:51] [Người nói?]** Thầy tiếp theo.

<a id="S00305"></a>
**[00:29:55 → 00:29:56] [Người nói?]** Có đó.

<a id="S00306"></a>
**[00:29:57 → 00:29:58] [Người nói?]** Em không...

<a id="S00307"></a>
**[00:29:58 → 00:29:58] [Người nói?]** Có đó.

<a id="S00308"></a>
**[00:29:59 → 00:29:59] [Người nói?]** Em không...

<a id="S00309"></a>
**[00:29:59 → 00:30:00] [Người nói?]** Thầy,

<a id="S00310"></a>
**[00:30:00 → 00:30:03] [Người nói?]** [ASR cần nghe lại] là tỷ lệ

<a id="S00311"></a>
**[00:30:07 → 00:30:10] [Người nói?]** [ASR cần nghe lại] Cải thiện cái gì thay cũng chả hiểu, cải thiện cái gì đâu

<a id="S00312"></a>
**[00:30:17 → 00:30:24] [Người nói?]** [nghe không rõ 00:30:17; cần đối chiếu] Ở mức độ kinh nghiệm thì cái cải thiện chỉ là để các thành thường hiểu cho em

<a id="S00313"></a>
**[00:30:24 → 00:30:31] [Người nói?]** [nghe không rõ 00:30:24; cần đối chiếu] Thì còn chứ không cần trình bày phải cải thiện đâu, em hiểu chưa?

<a id="S00314"></a>
**[00:30:31 → 00:30:35] [Người nói?]** [nghe không rõ 00:30:31; cần đối chiếu] Thì đấy là nội dung của kinh nghiệm

<a id="S00315"></a>
**[00:30:35 → 00:30:39] [Người nói?]** [ASR cần nghe lại] Nhưng mà cái trình bày của em vừa rồi cũng dối quá là mọi người không hiểu

<a id="S00316"></a>
**[00:30:39 → 00:30:41] [Người nói?]** [ASR cần nghe lại] Thì thay cũng chưa hiểu đâu

<a id="S00317"></a>
**[00:30:43 → 00:30:51] [Người nói?]** [nghe không rõ 00:30:43; cần đối chiếu] Bây giờ anh tập trung vào một cái tầm mồm là từ cái SQL, bây giờ em sinh ra một cái SQL, đó là một cái cách thức để em đề xuất,

<a id="S00318"></a>
**[00:30:51 → 00:30:54] [Người nói?]** [ASR cần nghe lại] thì em tập trung vào cái việc mà em gọi là để sinh ra.

<a id="S00319"></a>
**[00:30:55 → 00:31:01] [Người nói?]** [nghe không rõ 00:30:55; cần đối chiếu] Trong những cái sinh ra đấy thì em cũng đề xuất là có một cái mô hình mà em muốn gọi là cho nó mất hơn những cái mô hình bình thường.

<a id="S00320"></a>
**[00:31:02 → 00:31:07] [Người nói?]** [nghe không rõ 00:31:02; cần đối chiếu] Thì còn hai cái đấy thôi, thì chúng ta hiểu được là chúng ta tổng thân là tổng thân sinh ra cái SQL Edition.

<a id="S00321"></a>
**[00:31:07 → 00:31:13] [Người nói?]** [nghe không rõ 00:31:07; cần đối chiếu] Và trong các cái mô hình em sử dụng SQL Edition thì em sử dụng trên cả mô hình là SQL GAM và có một phần kiểm nghiệm thôi.

<a id="S00322"></a>
**[00:31:13 → 00:31:16] [Người nói?]** [ASR cần nghe lại] Thế thôi. Nghĩa là nó kiểm tra được những lợi ích gì.

<a id="S00323"></a>
**[00:31:17 → 00:31:18] [Người nói?]** [ASR cần nghe lại] Thế thôi.

<a id="S00324"></a>
**[00:31:18 → 00:31:22] [Người nói?]** [nghe không rõ 00:31:18; cần đối chiếu] Nếu thầy nghĩa là vệt bản và...

<a id="S00325"></a>
**[00:31:22 → 00:31:25] [Người nói?]** [nghe không rõ 00:31:22; cần đối chiếu] Bây giờ em mở quyển luật văn ra xin mở ra cho thầy xem cái chỗ nào là thầy đi.

<a id="S00326"></a>
**[00:31:26 → 00:32:24] [Người nói?]** [nghe không rõ 00:31:26; cần đối chiếu] Có ý thầy bảo em là thầy có ý thầy đi vào.

<a id="S00327"></a>
**[00:32:25 → 00:32:27] [Người nói?]** [ASR cần nghe lại] Slide này cũng chưa phản ánh được cái góp ý lần trước.

<a id="S00328"></a>
**[00:32:27 → 00:32:38] [Người nói?]** [nghe không rõ 00:32:27; cần đối chiếu] Rồi trình bày lại nhiều cái chuyện là đây là cái nhóm mà sinh nhật chưng, đây là cái nhóm sinh chuối.

<a id="S00329"></a>
**[00:32:38 → 00:32:52] [Người nói?]** [ASR cần nghe lại] Đúng không? Lần trước thầy đã góp ý rất nhiều rồi cũng chưa thấy thay đổi bao nhiêu cả.

<a id="S00330"></a>
**[00:32:52 → 00:33:04] [Người nói?]** Đề án mình tập trung vào nghiên cứu về dùng mạng gan để hỗ trợ sinh sinh dữ liệu

<a id="S00331"></a>
**[00:33:04 → 00:33:07] [Người nói?]** Thì em hình dung là cái chuyện em tìm hiểu

<a id="S00332"></a>
**[00:33:08 → 00:33:10] [Người nói?]** [nghe không rõ 00:33:08; cần đối chiếu] Citygan hay Citygan đấy là nó góp rồi

<a id="S00333"></a>
**[00:33:13 → 00:33:16] [Người nói?]** Thì trong tìm hiểu đấy mình nói là mình phân biệt ra 2 loại

<a id="S00334"></a>
**[00:33:16 → 00:33:17] [Người nói?]** [nghe không rõ 00:33:16; cần đối chiếu] Một là sinh liệt chức

<a id="S00335"></a>
**[00:33:17 → 00:33:20] [Người nói?]** [nghe không rõ 00:33:17; cần đối chiếu] Sinh liệt chức là ra cái thứ mà không ai hiểu là cái gì cả

<a id="S00336"></a>
**[00:33:20 → 00:33:25] [Người nói?]** Nhưng mà đưa vào cái mô hình máy thì nó vẫn nhận

<a id="S00337"></a>
**[00:33:25 → 00:33:27] [Người nói?]** [nghe không rõ 00:33:25; cần đối chiếu] Cái anh ta là sinh hẳn cái chú ý thật

<a id="S00338"></a>
**[00:33:27 → 00:33:40] [Người nói?]** [nghe không rõ 00:33:27; cần đối chiếu] Anh ta bảo Citygan là sinh rất là chú ý thật

<a id="S00339"></a>
**[00:33:40 → 00:33:41] [Người nói?]** Cái này thầy cũng đang chưa hiểu

<a id="S00340"></a>
**[00:33:41 → 00:33:51] [Người nói?]** [nghe không rõ 00:33:41; cần đối chiếu] Đúng ạ. Thì là gan với cả CD gan là nó cũng chỉ sinh đặc trưng vào xây quần gan thì là...

<a id="S00341"></a>
**[00:33:51 → 00:33:57] [Người nói?]** [ASR cần nghe lại] Đúng thế. Cái vấn đề là em cứ tập trung cái chuyện cải tiến này, cải tiến là đấy là làm hết.

<a id="S00342"></a>
**[00:33:57 → 00:34:03] [Người nói?]** [ASR cần nghe lại] Mình trình bày cái mặt chính luôn, tốt đi đã. Đúng không?

<a id="S00343"></a>
**[00:34:04 → 00:34:13] [Người nói?]** [nghe không rõ 00:34:04; cần đối chiếu] Thay là nói đồ ăn về cái mạng gan. Thế trước đây em trình bày mạng gan ở chỗ nào nhỉ? Đúng chưa?

<a id="S00344"></a>
**[00:34:13 → 00:34:20] [Người nói?]** [nghe không rõ 00:34:13; cần đối chiếu] Trước đây trình bày mạng gan, gan cấu trúc những thành phần như thế nào, hàm lót xuất như thế nào. Đúng không?

<a id="S00345"></a>
**[00:34:20 → 00:34:22] [Người nói?]** [ASR cần nghe lại] Tại sao dùng gan để xin dữ liệu?

<a id="S00346"></a>
**[00:34:22 → 00:34:30] [Người nói?]** Chứ nếu em cứ nhảy vào thì cải thiện luôn, hóa ra đầy dài phải đi vào là trọng tâm em cải thiện ra không?

<a id="S00347"></a>
**[00:34:35 → 00:34:54] [Người nói?]** [nghe không rõ 00:34:35; cần đối chiếu] Chưa vẽ mô hình, em cũng chỉ vẽ là lưu đồ thật toán.

<a id="S00348"></a>
**[00:34:55 → 00:34:57] [Người nói?]** Cần về cái gì em phải cải thiện.

<a id="S00349"></a>
**[00:34:58 → 00:34:59] [Người nói?]** Về xem lại đi.

<a id="S00350"></a>
**[00:34:59 → 00:35:00] [Người nói?]** Vâng.

<a id="S00351"></a>
**[00:35:00 → 00:35:06] [Người nói?]** [nghe không rõ 00:35:00; cần đối chiếu] Có 1 cái slide cho mà hơn 1 tuần rồi em cũng thử lại cái này rồi.

## Phạm vi WAF: qua bộ lọc khác với khai thác thành công

<a id="S00352"></a>
**[00:35:14 → 00:35:16] [Người nói?]** Em có 1 phần thử nghiệm với tường lửa phải không?

<a id="S00353"></a>
**[00:35:17 → 00:35:17] [Người nói?]** Dạ.

<a id="S00354"></a>
**[00:35:17 → 00:35:24] [Người nói?]** [nghe không rõ 00:35:17; cần đối chiếu] Nhưng mà cái đấy thì có cái mẫu nào mà đúng tốt đấy mà thân hiệp gọi quản được không?

<a id="S00355"></a>
**[00:35:24 → 00:35:35] [Người nói?]** Có, có 157 mẫu, nhưng mà trong lúc thuyết trình em cảm giác là em đang bị nói hơi không đúng trọng tâm nha em đã

<a id="S00356"></a>
**[00:35:35 → 00:35:48] [Người nói?]** Cái này em hơi thắc mắc tại vì là thường các cái tường lửa và ứng dụng thì ví dụ như nó bắt câu lệnh thì nó bắt theo cấu trúc rồi

<a id="S00357"></a>
**[00:35:49 → 00:35:55] [Người nói?]** [nghe không rõ 00:35:49; cần đối chiếu] Tức là cái đoạn thay hội theo số thì chúng ta vẫn biết tại vì nó tuân thuyết cấu trúc rất lớn nhỉ

<a id="S00358"></a>
**[00:35:55 → 00:35:59] [Người nói?]** [nghe không rõ 00:35:55; cần đối chiếu] bình thường cái tên ngựa mà đi bắt một câu đấy xí lệch thì nó đi qua

<a id="S00359"></a>
**[00:36:00 → 00:36:05] [Người nói?]** thì nó sẽ thường cũng đã biết cái cấu trúc vừa rồi

<a id="S00360"></a>
**[00:36:05 → 00:36:10] [Người nói?]** còn cái thay tham số thì nó vẫn bắt lại

<a id="S00361"></a>
**[00:36:10 → 00:36:19] [Người nói?]** trong mô hình của em là em sử dụng cái phương án nó không cao cấp

<a id="S00362"></a>
**[00:36:19 → 00:36:24] [Người nói?]** [nghe không rõ 00:36:19; cần đối chiếu] và nó khá đặc trà là most security và rule là OAV

<a id="S00363"></a>
**[00:36:24 → 00:36:30] [Người nói?]** nên là với cả em cũng không có xây dựng cái DB nó quá là đầy đủ

<a id="S00364"></a>
**[00:36:31 → 00:36:41] [Người nói?]** [ASR cần nghe lại] Ví dụ như chỉ cần tấn công vượt qua mà báo về mẫu 200 mà lúc đấy em sẽ ngồi đọc payload xem là có các đặc tính

<a id="S00365"></a>
**[00:36:41 → 00:36:46] [Người nói?]** [ASR cần nghe lại] Nếu mà đưa vào thực tế thì có thể nó sẽ không khai thác được quá nhiều

<a id="S00366"></a>
**[00:36:46 → 00:36:48] [Người nói?]** [nghe không rõ 00:36:46; cần đối chiếu] Thế là đây là em có cao tiền với cái mẫu 200

<a id="S00367"></a>
**[00:36:50 → 00:36:57] [Người nói?]** [ASR cần nghe lại] Em không thay đổi, em tải rồi em sử dụng lại nên không thay đổi trong quá trình chạy học

<a id="S00368"></a>
**[00:36:59 → 00:37:07] [Người nói?]** Nó có 2 kiểu trường hợp, một là dữ liệu sinh ra nó không theo cấu trúc của SQL vượt qua được

<a id="S00369"></a>
**[00:37:07 → 00:37:08] [Người nói?]** hoặc là cũng nhiễu đúng không?

<a id="S00370"></a>
**[00:37:08 → 00:37:09] [Người nói?]** Đúng ạ

<a id="S00371"></a>
**[00:37:09 → 00:37:15] [Người nói?]** [nghe không rõ 00:37:09; cần đối chiếu] Cái đó là nếu nó tốt như cấu trúc thì cái tham số trong đấy nó phải như nào đó đúng không?

<a id="S00372"></a>
**[00:37:15 → 00:37:16] [Người nói?]** [nghe không rõ 00:37:15; cần đối chiếu] Phải có giá trị địa tấn công đúng không?

<a id="S00373"></a>
**[00:37:16 → 00:37:16] [Người nói?]** Vâng

<a id="S00374"></a>
**[00:37:16 → 00:37:22] [Người nói?]** [nghe không rõ 00:37:16; cần đối chiếu] Cái đấy mình hỏi là cái đấy có sinh ra cả đám kia thế như thế không để vượt qua tấn công không?

<a id="S00375"></a>
**[00:37:22 → 00:37:24] [Người nói?]** Vượt qua tầng lửa của tấn công không?

<a id="S00376"></a>
**[00:37:26 → 00:37:33] [Người nói?]** [nghe không rõ 00:37:26; cần đối chiếu] Nếu vượt qua tường lửa của em, trong mô hình của em, nếu vượt qua được 200

<a id="S00377"></a>
**[00:37:34 → 00:37:37] [Người nói?]** Lúc đấy em sẽ thật sự vào để em đọc và xem có cấu trúc

<a id="S00378"></a>
**[00:37:37 → 00:37:44] [Người nói?]** Còn nếu yêu cầu trong môi trường thực tế, tường lửa của các doanh nghiệp thì chắc chắn là không vượt qua

<a id="S00379"></a>
**[00:37:46 → 00:37:52] [Người nói?]** [nghe không rõ 00:37:46; cần đối chiếu] Cái mô security của nó khá là mạnh, sinh cái streamer SQL và đưa theo

<a id="S00380"></a>
**[00:37:52 → 00:37:55] [Người nói?]** [nghe không rõ 00:37:52; cần đối chiếu] Bản chất của nó chỉ là theo cái tham số thôi chứ đúng không?

<a id="S00381"></a>
**[00:37:55 → 00:38:20] [Người nói?]** Không nghĩa là bởi vì trong chính cái kịch bản của em ạ, nó cũng không có database ạ, nó chỉ đơn giản là đưa vào bộ lọc và nếu như trả về kết quả 200 thì em sẽ biết là một là nó đã vượt qua hoặc là noise, lúc đấy em bắt đầu mới đọc xem là nó có cấu trúc SV ạ, còn em trong mô hình này em không có thử nhận xem có tấn công được để em không.

<a id="S00382"></a>
**[00:38:20 → 00:38:33] [Người nói?]** [nghe không rõ 00:38:20; cần đối chiếu] Nếu mà đạt về 200 nó trả lời nó hoạt động, những khu vực này bình thường thì nó vẫn hoạt động của mình trong cơ sở thì có gì nó sẽ hoàn thành được để đạt ra đợt tổng hợp SRL?

<a id="S00383"></a>
**[00:38:34 → 00:38:49] [Người nói?]** [nghe không rõ 00:38:34; cần đối chiếu] Đúng rồi. Thì là trong mô hình thì mình chỉ tập trung vào việc là một cái câu SRL, Injection có cấu trúc SRL khi đeo qua tường lửa và trả về kết quả 200

<a id="S00384"></a>
**[00:38:49 → 00:38:55] [Người nói?]** Chứ nó không bị chặn 403. Thì mình sẽ chỉ tập trung khai thác những cái thông tin như thế

<a id="S00385"></a>
**[00:38:55 → 00:38:59] [Người nói?]** [nghe không rõ 00:38:55; cần đối chiếu] nghĩa là AFL có sự tuyên bẩn và có sự tỉnh đại

<a id="S00386"></a>
**[00:38:59 → 00:39:06] [Người nói?]** [nghe không rõ 00:38:59; cần đối chiếu] có sự tỉnh đại thì cứ xử lý được mình mới có gì để cho nó ra ra được

<a id="S00387"></a>
**[00:39:06 → 00:39:06] [Người nói?]** [ASR cần nghe lại] rồi

<a id="S00388"></a>
**[00:39:07 → 00:39:10] [Người nói?]** [ASR cần nghe lại] người ta chỉ cần phát hiện được thôi

<a id="S00389"></a>
**[00:39:10 → 00:39:17] [Người nói?]** [ASR cần nghe lại] cái câu lệnh mà đi qua mà theo những kiểu tấn công để xem nó sinh ra như thế nào

<a id="S00390"></a>
**[00:39:17 → 00:39:18] [Người nói?]** [ASR cần nghe lại] không có chuyện khác

<a id="S00391"></a>
**[00:39:21 → 00:39:26] [Người nói?]** [nghe không rõ 00:39:21; cần đối chiếu] nghĩa là nếu mà câu lệnh này chính phẩm AFL thì mình chỉ cần kiểm thử được

<a id="S00392"></a>
**[00:39:26 → 00:39:33] [Người nói?]** [nghe không rõ 00:39:26; cần đối chiếu] vì mình có thể phản định câu lệnh này là AFL chính phẩm tuyên bẩn

<a id="S00393"></a>
**[00:39:33 → 00:39:35] [Người nói?]** [nghe không rõ 00:39:33; cần đối chiếu] mình là nhắn một tay cả hẳn

<a id="S00394"></a>
**[00:39:35 → 00:39:38] [Người nói?]** [nghe không rõ 00:39:35; cần đối chiếu] nhưng mà bản thân nó có phải tự tin cho AFL là một nền để tương ứng

<a id="S00395"></a>
**[00:39:38 → 00:39:41] [Người nói?]** [ASR cần nghe lại] thế thì vấn đề nó cũng hỏi đấy

<a id="S00396"></a>
**[00:39:51 → 00:39:59] [Người nói?]** [nghe không rõ 00:39:51; cần đối chiếu] Bộ dữ liệu này có tấn công đa dạng trên nhiều DB và nó cũng yêu

<a id="S00397"></a>
**[00:40:00 → 00:40:09] [Người nói?]** cũng yêu cầu các cái đầu vào payload và các cái cấu trúc là nó khác biệt chứ nó không tưởng chung một cái cú pháp

<a id="S00398"></a>
**[00:40:09 → 00:40:23] [Người nói?]** [nghe không rõ 00:40:09; cần đối chiếu] Thế nên là trước là mình cũng có làm là cũng có xây dựng lên nhưng mà là do là phải thêm thấp những cái HTTP phải chuẩn thì lúc đó nó thật sự ảnh hưởng

<a id="S00399"></a>
**[00:40:23 → 00:40:32] [Người nói?]** nên là lúc đấy là mình mới bỏ phương án đấy và mình chỉ quan tâm việc là có vượt qua được bộ rule set và có trả về 200 hay không

<a id="S00400"></a>
**[00:40:35 → 00:40:43] [Người nói?]** [nghe không rõ 00:40:35; cần đối chiếu] Nếu mà xây dựng như Lam nói thì khả năng cao là sẽ không vượt qua được thật

<a id="S00401"></a>
**[00:40:45 → 00:40:57] [Người nói?]** Nhưng mà giả sử nếu cần phải làm chia sẻ mức đấy thì sẽ phải viết từng cái cấu trúc để cho từng cái tài loại một và đưa vào

<a id="S00402"></a>
**[00:40:58 → 00:41:00] [Người nói?]** Chứ không thể kiểu sửa ứng dụng đại trà được

<a id="S00403"></a>
**[00:41:00 → 00:41:05] [Người nói?]** Thì đấy là vấn đề mà mình gặp phải về cái đưa vào từng lượng

<a id="S00404"></a>
**[00:41:05 → 00:41:09] [Người nói?]** [nghe không rõ 00:41:05; cần đối chiếu] Thế là mục tiêu này là sinh ra dữ liệu kiểm công không? Kiểm thử dễ công không?

<a id="S00405"></a>
**[00:41:09 → 00:41:10] [Người nói?]** Đúng

<a id="S00406"></a>
**[00:41:10 → 00:41:19] [Người nói?]** [nghe không rõ 00:41:10; cần đối chiếu] Còn có thể là test thử với bộ phát hiện người mốt sinh ra dữ liệu không để test thử xem

<a id="S00407"></a>
**[00:41:23 → 00:41:29] [Người nói?]** [nghe không rõ 00:41:23; cần đối chiếu] Cũng làm, cũng hạ hạ xuống

<a id="S00408"></a>
**[00:41:29 → 00:41:36] [Người nói?]** Vì lúc đầu cũng đúng như anh với cả Lao nói là cũng muốn là thật sự xem là tường lửa có được không

<a id="S00409"></a>
**[00:41:36 → 00:41:43] [Người nói?]** Trong lúc triển khai thì phải tự nhiên nó phức tạp hơi nhiều so với mục tiêu ban đầu

<a id="S00410"></a>
**[00:41:43 → 00:41:46] [Người nói?]** Và cảm giác nó hơi lệch nên là mới thu nhỏ xuống

<a id="S00411"></a>
**[00:41:46 → 00:41:55] [Người nói?]** [nghe không rõ 00:41:46; cần đối chiếu] Nó chỉ đơn giản là chỉ cần trả về mẫu 200 sau khi vượt qua đổi thu xét, kiểm tra xem có dùng SVL Injection hay không, hay là nhiễu

<a id="S00412"></a>
**[00:41:55 → 00:41:59] [Người nói?]** [nghe không rõ 00:41:55; cần đối chiếu] Nếu như là SVL Injection thì sẽ đưa vào luôn

<a id="S00413"></a>
**[00:42:00 → 00:42:07] [Người nói?]** [nghe không rõ 00:42:00; cần đối chiếu] Mẫu tấn công này có đặc tính SVL Injection chứ không nhằm tới việc là có thật sự định nghĩa và khai thác thực tế

## Chốt lại cấu trúc trình bày

<a id="S00414"></a>
**[00:42:17 → 00:42:22] [Người nói?]** Mình về trình bày lại cho rõ trong văn lẫn, trong slide nhé

<a id="S00415"></a>
**[00:42:23 → 00:42:26] [Người nói?]** [nghe không rõ 00:42:23; cần đối chiếu] Đấy, thứ nhất thầy nói thì bạn phải lấy cường để ghi như thầy nói cả

<a id="S00416"></a>
**[00:42:26 → 00:42:30] [Người nói?]** [nghe không rõ 00:42:26; cần đối chiếu] Trước đây có bị ít rồi, tuần này có lệch

<a id="S00417"></a>
**[00:42:30 → 00:42:33] [Người nói?]** Thứ hai là đầu tiên phải nói về cái bài thoáng phát hiện

<a id="S00418"></a>
**[00:42:33 → 00:42:40] [Người nói?]** [nghe không rõ 00:42:33; cần đối chiếu] Tấn công là chỉ quen với một section rất clear ở trên slide

<a id="S00419"></a>
**[00:42:40 → 00:42:42] [Người nói?]** Người ta đã từng làm gì thế nào?

<a id="S00420"></a>
**[00:42:43 → 00:42:45] [Người nói?]** Người ta đã từng làm gì?

<a id="S00421"></a>
**[00:42:46 → 00:42:48] [Người nói?]** Đấy chưa?

<a id="S00422"></a>
**[00:42:50 → 00:42:53] [Người nói?]** [nghe không rõ 00:42:50; cần đối chiếu] Cái work và cái detector nó là những cái gì?

<a id="S00423"></a>
**[00:42:53 → 00:43:10] [Người nói?]** Đấy chưa?

<a id="S00424"></a>
**[00:43:21 → 00:43:23] [Người nói?]** Tiếp theo là liên quan tới sinh dữ liệu

<a id="S00425"></a>
**[00:43:24 → 00:43:27] [Người nói?]** Cơ bản người ta dùng SMOTE

<a id="S00426"></a>
**[00:43:27 → 00:43:37] [Người nói?]** Và trong luận văn này em tìm hiểu về một phương pháp sử dụng sinh dữ liệu

<a id="S00427"></a>
**[00:43:37 → 00:43:41] [Người nói?]** Thì gan nó là cái gì? Tại sao phải sử dụng gan?

<a id="S00428"></a>
**[00:43:42 → 00:43:43] [Người nói?]** [nghe không rõ 00:43:42; cần đối chiếu] Mình cứ nói cho không xuyên xoay

<a id="S00429"></a>
**[00:43:46 → 00:43:51] [Người nói?]** [nghe không rõ 00:43:46; cần đối chiếu] Và trong đoàn đề án này em tìm hiểu những mùi gan như sau

<a id="S00430"></a>
**[00:43:51 → 00:43:54] [Người nói?]** [nghe không rõ 00:43:51; cần đối chiếu] CT gan, CT cột gan

<a id="S00431"></a>
**[00:43:54 → 00:43:59] [Người nói?]** Được kết quả như thế này

<a id="S00432"></a>
**[00:43:59 → 00:44:02] [Người nói?]** [nghe không rõ 00:43:59; cần đối chiếu] Trình bày những phần bản đánh vọng thôi

<a id="S00433"></a>
**[00:44:02 → 00:44:06] [Người nói?]** [nghe không rõ 00:44:02; cần đối chiếu] Các thầy không thể hiểu các thầy làm cái gì lắm

<a id="S00434"></a>
**[00:44:06 → 00:44:09] [Người nói?]** Em dạng được kết quả như thế này

<a id="S00435"></a>
**[00:44:09 → 00:44:13] [Người nói?]** [nghe không rõ 00:44:09; cần đối chiếu] Chỉ phải đúng theo dựa dựa như thế này nhé

<a id="S00436"></a>
**[00:44:13 → 00:44:17] [Người nói?]** Đã được kết quả như thế này

<a id="S00437"></a>
**[00:44:17 → 00:44:20] [Người nói?]** [nghe không rõ 00:44:17; cần đối chiếu] Và em thấy với sinh quần ngoan, sinh quần gan

<a id="S00438"></a>
**[00:44:21 → 00:44:23] [Người nói?]** Thì nó khác cái gan kia nó là cái gì

<a id="S00439"></a>
**[00:44:23 → 00:44:26] [Người nói?]** Hai nhóm, một nhóm là sinh đặc trưng

<a id="S00440"></a>
**[00:44:26 → 00:44:27] [Người nói?]** [nghe không rõ 00:44:26; cần đối chiếu] Một nhóm là sinh sinh quần

<a id="S00441"></a>
**[00:44:27 → 00:44:28] [Người nói?]** Ví dụ nó như thế này

<a id="S00442"></a>
**[00:44:28 → 00:44:37] [Người nói?]** Ví dụ vào thành phần ngay trên slide

<a id="S00443"></a>
**[00:44:37 → 00:44:41] [Người nói?]** Sinh đặc trưng nó sinh cái gì

<a id="S00444"></a>
**[00:44:45 → 00:44:46] [Người nói?]** Sinh chuỗi nó như thế này

<a id="S00445"></a>
**[00:44:47 → 00:44:50] [Người nói?]** [nghe không rõ 00:44:47; cần đối chiếu] Với kết quả hiện nay sinh quần gan nó đạt được mức độ như thế này

<a id="S00446"></a>
**[00:44:50 → 00:44:52] [Người nói?]** Em thấy là nó chưa được tốt lắm

<a id="S00447"></a>
**[00:44:52 → 00:44:59] [Người nói?]** [nghe không rõ 00:44:52; cần đối chiếu] Như vậy em có một đề xuất thêm, cải thiện xịt bồn gan, xịt bồn gan và cải thiện cái gì phải nói rõ.

<a id="S00448"></a>
**[00:44:59 → 00:45:05] [Người nói?]** Và cuối cùng kết quả đạt được như thế nào?

<a id="S00449"></a>
**[00:45:09 → 00:45:26] [Người nói?]** Quay trước thôi, em phải sửa làm sao để phản ảnh hiểu được.

<a id="S00450"></a>
**[00:45:26 → 00:46:18] [Người nói?]** [nghe không rõ 00:45:26; cần đối chiếu] Chưa, em hãy bổ sung giải thích câu hỏi này dầu quá.
