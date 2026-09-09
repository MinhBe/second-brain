# Voice 009 — góp ý báo cáo GAN, lựa chọn thí nghiệm và minh chứng trên slide

Nguồn: [Voice 009.m4a](file:///C:/Users/Admin/Documents/Collection/Data/Recording/Voice%20009.m4a)

Thời lượng: 00:33:39. ASR: large-v3 / cuda.

Trạng thái: đã rà văn bản; chờ nghe đối chiếu. Người nói chưa được xác định nếu không có ghi chú riêng.
Bản này bảo toàn thứ tự và nội dung nhận dạng; các đoạn nghi lỗi được giữ dấu vết để nghe lại.

## Tên đề tài, mục tiêu và hai nhóm mô hình sinh

<a id="S00001"></a>
**[00:00:00 → 00:00:01] [Người nói?]** Các thầy mình còn đợi ai không?

<a id="S00002"></a>
**[00:00:03 → 00:00:06] [Người nói?]** Xin phép trình bày báo cáo tổng hợp toàn bộ

<a id="S00003"></a>
**[00:00:06 → 00:00:10] [Người nói?]** Phần nghiên cứu của em về sử dụng mô hình sinh dữ liệu

<a id="S00004"></a>
**[00:00:11 → 00:00:14] [Người nói?]** Để sinh dữ liệu tấn công SQL injection.

<a id="S00005"></a>
**[00:00:14 → 00:00:18] [Người nói?]** Nhằm nâng cao phát hiện dựa trên học máy.

<a id="S00006"></a>
**[00:00:18 → 00:00:20] [Người nói?]** Thì là mục tiêu của em

<a id="S00007"></a>
**[00:00:20 → 00:00:23] [Người nói?]** Mục tiêu tổng quát là sinh

<a id="S00008"></a>
**[00:00:23 → 00:00:25] [Người nói?]** Lựa chọn các phương pháp sinh hoặc bổ sung

<a id="S00009"></a>
**[00:00:25 → 00:00:27] [Người nói?]** Dữ liệu SQL injection có kiểm soát.

<a id="S00010"></a>
**[00:00:27 → 00:00:28] [Người nói?]** Để hỗ trợ mô hình

<a id="S00011"></a>
**[00:00:28 → 00:00:32] [Người nói?]** để nâng cao chất lượng của mô hình học máy

<a id="S00012"></a>
**[00:00:32 → 00:00:35] [Người nói?]** thì sẽ có tổng cộng là có 5 bước

<a id="S00013"></a>
**[00:00:35 → 00:00:39] [Người nói?]** đầu tiên là em sẽ kiểm soát dữ liệu

<a id="S00014"></a>
**[00:00:39 → 00:00:42] [Người nói?]** thì là em sẽ cố gắng điều chỉnh dữ liệu

<a id="S00015"></a>
**[00:00:42 → 00:00:44] [Người nói?]** để nó phù hợp hơn với mô hình bài toán

<a id="S00016"></a>
**[00:00:44 → 00:00:49] [Người nói?]** tiếp theo là em sẽ đề xuất tổng cộng là 5 phương pháp

<a id="S00017"></a>
**[00:00:49 → 00:00:52] [Người nói?]** thì sẽ có 4 phương pháp là 4 mô hình

<a id="S00018"></a>
**[00:00:53 → 00:00:57] [Người nói?]** đầu tiên là mô hình SMOTE là mô hình nội sinh dữ liệu

<a id="S00019"></a>
**[00:00:57 → 00:01:05] [Người nói?]** [nghe không rõ 00:00:57; cần đối chiếu] dữ liệu mô hình gan cơ bản là mô hình sinh dữ liệu gan cơ bản mô hình CT gan và si quần gan thì

<a id="S00020"></a>
**[00:01:05 → 00:01:13] [Người nói?]** [nghe không rõ 00:01:05; cần đối chiếu] CT gan là cũng là phương pháp gan nhưng mà chuyên xử lý cho dữ liệu dạng bảng còn si quần gan là

<a id="S00021"></a>
**[00:01:13 → 00:01:22] [Người nói?]** [nghe không rõ 00:01:13; cần đối chiếu] chuyên xử lý cho mô hình dữ liệu rời rạc sau đó là em sau khi so sánh xong thì em cảm thấy là mô

<a id="S00022"></a>
**[00:01:22 → 00:01:27] [Người nói?]** [nghe không rõ 00:01:22; cần đối chiếu] hình si quần gan có thể học được các mối quan hệ và cấu trúc câu nên là em đề xuất các phương án

<a id="S00023"></a>
**[00:01:27 → 00:01:36] [Người nói?]** và em sẽ đánh giá tổng cộng cả 5 mô hình này trên cùng một đầu và dữ liệu chung

<a id="S00024"></a>
**[00:01:39 → 00:01:47] [Người nói?]** Tên đề tài của em là nghiên cứu mô hình GAN cho sinh dữ liệu tấn công SQL.

<a id="S00025"></a>
**[00:01:47 → 00:01:51] [Người nói?]** Nhằm nâng cao mô hình phát hiện dựa trên học máy.

<a id="S00026"></a>
**[00:01:51 → 00:01:52] [Người nói?]** Đây là tên đề tài của em

<a id="S00027"></a>
**[00:01:52 → 00:01:55] [Người nói?]** Rồi bây giờ quay lại kia, thế này nó phải thể hiện được tên đề tài

<a id="S00028"></a>
**[00:01:56 → 00:01:59] [Người nói?]** Cho nên mục tiêu tổng quát phải gắn với GAN.

<a id="S00029"></a>
**[00:02:00 → 00:02:02] [Người nói?]** Lúc trước trong tin nhắn của người của em

<a id="S00030"></a>
**[00:02:03 → 00:02:05] [Người nói?]** Thế là em phải đi với cái tên đề tài

<a id="S00031"></a>
**[00:02:06 → 00:02:08] [Người nói?]** [nghe không rõ 00:02:06; cần đối chiếu] Học dụng của em có giúp bây giờ thầy đề tài được rồi

<a id="S00032"></a>
**[00:02:08 → 00:02:11] [Người nói?]** Nhưng mà người khách biết, cái mục tiêu rủng quát em phải xem trong đề cương

<a id="S00033"></a>
**[00:02:13 → 00:02:16] [Người nói?]** Thứ mục tiêu trong đề cương mình biết là kiểu này, kiểu này nó lại bị lệch nhau

<a id="S00034"></a>
**[00:02:16 → 00:02:17] [Người nói?]** Em hiểu

<a id="S00035"></a>
**[00:02:19 → 00:02:19] [Người nói?]** [nghe không rõ 00:02:19; cần đối chiếu] Thầy Châu Ước

<a id="S00036"></a>
**[00:02:19 → 00:02:21] [Người nói?]** Cái của em Minh ấy

<a id="S00037"></a>
**[00:02:21 → 00:02:22] [Người nói?]** Tức là mục tiêu là dùng

<a id="S00038"></a>
**[00:02:23 → 00:02:24] [Người nói?]** nghiên cứu về gan

<a id="S00039"></a>
**[00:02:24 → 00:02:27] [Người nói?]** và gan sử dụng trong sinh dữ liệu

<a id="S00040"></a>
**[00:02:27 → 00:02:29] [Người nói?]** Để hỗ trợ nâng cao cái

<a id="S00041"></a>
**[00:02:29 → 00:02:33] [Người nói?]** [nghe không rõ 00:02:29; cần đối chiếu] sức lượng hộp máy luôn đúng không anh nhỉ

<a id="S00042"></a>
**[00:02:33 → 00:02:33] [Người nói?]** Đúng rồi

<a id="S00043"></a>
**[00:02:34 → 00:02:34] [Người nói?]** Thế thì thầy muốn là

<a id="S00044"></a>
**[00:02:34 → 00:02:35] [Người nói?]** [nghe không rõ 00:02:34; cần đối chiếu] Đấy là mục tiêu thủng quá

<a id="S00045"></a>
**[00:02:35 → 00:02:37] [Người nói?]** Thế còn đi vào phép chi tiết ấy

<a id="S00046"></a>
**[00:02:37 → 00:02:37] [Người nói?]** Thì mới đoàn là

<a id="S00047"></a>
**[00:02:37 → 00:02:38] [Người nói?]** Thứ nhất là

<a id="S00048"></a>
**[00:02:38 → 00:02:39] [Người nói?]** không phải kiểm soát dữ liệu

<a id="S00049"></a>
**[00:02:39 → 00:02:41] [Người nói?]** mà đây là tìm hiểu về dữ liệu

<a id="S00050"></a>
**[00:02:41 → 00:02:43] [Người nói?]** Đúng không

<a id="S00051"></a>
**[00:02:44 → 00:02:45] [Người nói?]** Đấy mình tìm hiểu về cái bài toán

<a id="S00052"></a>
**[00:02:46 → 00:02:47] [Người nói?]** Bài toán và dữ liệu

<a id="S00053"></a>
**[00:02:47 → 00:02:49] [Người nói?]** Cái đấy em hiểu nhé

<a id="S00054"></a>
**[00:02:50 → 00:02:53] [Người nói?]** Nhớ với liên quan bài toán và dữ liệu

<a id="S00055"></a>
**[00:02:54 → 00:02:58] [Người nói?]** Bài toán nó là cái gì, dữ liệu là cái gì, đặc trưng là gì vân vân

<a id="S00056"></a>
**[00:02:58 → 00:03:02] [Người nói?]** Dữ liệu nó chỉ là cái mục 1, không phải kiểm soát dữ liệu

<a id="S00057"></a>
**[00:03:02 → 00:03:04] [Người nói?]** Dữ liệu nó chỉ là một hình ảnh nhỏ thôi

<a id="S00058"></a>
**[00:03:05 → 00:03:05] [Người nói?]** Đúng chưa?

<a id="S00059"></a>
**[00:03:06 → 00:03:09] [Người nói?]** Sau đó là các phương pháp giải quyết nó

<a id="S00060"></a>
**[00:03:09 → 00:03:13] [Người nói?]** Theo thầy nói em là SMOTE là baseline của các phương pháp cân bằng.

<a id="S00061"></a>
**[00:03:15 → 00:03:16] [Người nói?]** Để dữ liệu làm cân bằng

<a id="S00062"></a>
**[00:03:18 → 00:03:23] [Người nói?]** [nghe không rõ 00:03:18; cần đối chiếu] Rồi đến nhóm các phương pháp khí văn gân

<a id="S00063"></a>
**[00:03:24 → 00:03:25] [Người nói?]** Nó mới tách ra

<a id="S00064"></a>
**[00:03:26 → 00:03:31] [Người nói?]** Nhóm GAN đấy là nhóm trọng tâm của đồ án.

<a id="S00065"></a>
**[00:03:31 → 00:03:36] [Người nói?]** Và trong nhóm gân đấy thì có 2 nhóm

<a id="S00066"></a>
**[00:03:36 → 00:03:40] [Người nói?]** 1 là nhóm sinh đặc trưng

<a id="S00067"></a>
**[00:03:40 → 00:03:42] [Người nói?]** [nghe không rõ 00:03:40; cần đối chiếu] Nhóm thứ 2 là sinh gân

<a id="S00068"></a>
**[00:03:45 → 00:03:48] [Người nói?]** Nhóm sinh đặc trưng chính là gân truyền thống

<a id="S00069"></a>
**[00:03:48 → 00:03:50] [Người nói?]** [nghe không rõ 00:03:48; cần đối chiếu] rồi WANIGAN, rồi CITIGAN

<a id="S00070"></a>
**[00:03:50 → 00:03:53] [Người nói?]** [nghe không rõ 00:03:50; cần đối chiếu] rồi bắt đầu đến SEQUENT ONE

<a id="S00071"></a>
**[00:03:53 → 00:03:55] [Người nói?]** [nghe không rõ 00:03:53; cần đối chiếu] là nhóm XINYA CHUỐI

<a id="S00072"></a>
**[00:03:55 → 00:03:56] [Người nói?]** [nghe không rõ 00:03:55; cần đối chiếu] XINYA CHUỐI THẬT luôn đấy

<a id="S00073"></a>
**[00:03:58 → 00:03:59] [Người nói?]** Được chưa?

<a id="S00074"></a>
**[00:04:00 → 00:04:02] [Người nói?]** Riêng cái phần đấy em đã chạy được

<a id="S00075"></a>
**[00:04:02 → 00:04:04] [Người nói?]** [nghe không rõ 00:04:02; cần đối chiếu] so sánh SEQUENT GAN, SO SÁNH CITIGAN

<a id="S00076"></a>
**[00:04:04 → 00:04:06] [Người nói?]** [nghe không rõ 00:04:04; cần đối chiếu] so sánh SEQUENT GAN, SO SÁNH CITIGAN

<a id="S00077"></a>
**[00:04:06 → 00:04:08] [Người nói?]** Đấy cũng đã làm phần lớn

<a id="S00078"></a>
**[00:04:08 → 00:04:09] [Người nói?]** mục đích của

<a id="S00079"></a>
**[00:04:09 → 00:04:11] [Người nói?]** của gì nhỉ?

<a id="S00080"></a>
**[00:04:11 → 00:04:13] [Người nói?]** của đồ án

<a id="S00081"></a>
**[00:04:13 → 00:04:16] [Người nói?]** cộng với cái phần kiểm tra toàn này nữa

<a id="S00082"></a>
**[00:04:16 → 00:04:19] [Người nói?]** để mình xem chất lượng nó như thế nào

<a id="S00083"></a>
**[00:04:23 → 00:04:26] [Người nói?]** Cái phần làm thêm xuất sắc chính là phần cải tiến này.

<a id="S00084"></a>
**[00:04:28 → 00:04:33] [Người nói?]** Đó chính là đoán nền cao của em.

<a id="S00085"></a>
**[00:04:35 → 00:04:38] [Người nói?]** Cái đấy phải nhớ về chỉnh sửa cho đúng theo đề cương nhé.

## Dữ liệu, tiền xử lý và ví dụ minh họa

<a id="S00086"></a>
**[00:04:40 → 00:04:42] [Người nói?]** Đầu tiên là nguồn dữ liệu.

<a id="S00087"></a>
**[00:04:43 → 00:04:48] [Người nói?]** [nghe không rõ 00:04:43; cần đối chiếu] Đây là dữ liệu về SQL index được tải nhiều nhất trên Kaggle

<a id="S00088"></a>
**[00:04:48 → 00:04:55] [Người nói?]** và có rất nhiều bài báo có đề cập tới tài liệu này nên em sử dụng làm đại diện đặc trưng ạ

<a id="S00089"></a>
**[00:04:55 → 00:04:59] [Người nói?]** thì tổng dữ liệu thì sẽ có hơn 30.000 ạ

<a id="S00090"></a>
**[00:04:59 → 00:05:03] [Người nói?]** thì sau khi được tiền xử lý là loại bỏ các cái dữ liệu trùng lập

<a id="S00091"></a>
**[00:05:03 → 00:05:08] [Người nói?]** thì xuống còn cũng 30.800 ạ

<a id="S00092"></a>
**[00:05:08 → 00:05:12] [Người nói?]** trong đó thì các chuỗi bình thường thì 19.000 ạ

<a id="S00093"></a>
**[00:05:12 → 00:05:14] [Người nói?]** chuỗi đắn công là 11.000 ạ

<a id="S00094"></a>
**[00:05:20 → 00:05:28] [Người nói?]** Nhược điểm của các phương pháp truyền thống là người ta sẽ đưa thẳng toàn bộ dữ liệu của SQL vào mà không phân chia gì

<a id="S00095"></a>
**[00:05:28 → 00:05:35] [Người nói?]** Nên là khi mà sinh ra dữ liệu thì một câu lệnh có thể có nhiều đặc tính của nhiều dạng tầm công khác nhau

<a id="S00096"></a>
**[00:05:35 → 00:05:40] [Người nói?]** Thế nên là thường là dữ liệu sinh ra là dữ liệu nhiễu và không có giá trị về mặt thực tế

<a id="S00097"></a>
**[00:05:40 → 00:05:52] [Người nói?]** Thế nên là em sẽ tiến hành là sẽ chia nhỏ ra làm các thành phần riêng để có thể tập trung vào các đặc trưng của từng phương pháp

<a id="S00098"></a>
**[00:05:52 → 00:05:55] [Người nói?]** Thì trong này thì em sẽ chia ra làm 4 họ tấn công

<a id="S00099"></a>
**[00:05:55 → 00:06:00] [Người nói?]** [nghe không rõ 00:05:55; cần đối chiếu] Thì sẽ có là tấn công kiểu Poland, Union, Tham và Ireland

<a id="S00100"></a>
**[00:06:00 → 00:06:03] [Người nói?]** Thì trong này là có các cơ chế

<a id="S00101"></a>
**[00:06:03 → 00:06:12] [Người nói?]** [nghe không rõ 00:06:03; cần đối chiếu] Thì trong này có dấu hiệu thường gặp của Boland là trong cái câu toán toán tử đấy sẽ có các cái có

<a id="S00102"></a>
**[00:06:12 → 00:06:19] [Người nói?]** [nghe không rõ 00:06:12; cần đối chiếu] n o các phép so sánh dùng nháy common Union thì sẽ có các từ ngữ nhảy Union select danh sách cột

<a id="S00103"></a>
**[00:06:19 → 00:06:28] [Người nói?]** [nghe không rõ 00:06:19; cần đối chiếu] hoặc là null Time Bay thì sẽ có các hàm tạo độ chế thì ở trong này thì sẽ từng từng database thì nó

<a id="S00104"></a>
**[00:06:28 → 00:06:33] [Người nói?]** [nghe không rõ 00:06:28; cần đối chiếu] thì nó sẽ có những hàm tham bấy khác nhau ạ và Aaron thì là sẽ có hàm cố tình gây ra lỗi ạ

<a id="S00105"></a>
**[00:06:33 → 00:06:35] [Người nói?]** Cái chút này thầy có ghi cho em rồi nhưng em chưa sửa

<a id="S00106"></a>
**[00:06:35 → 00:06:39] [Người nói?]** [nghe không rõ 00:06:35; cần đối chiếu] Nghĩa là nó đã kể ra trong trình bày trong văn đề phần thông tin này luôn là có thêm phần thông tin

<a id="S00107"></a>
**[00:06:40 → 00:06:40] [Người nói?]** Ví dụ

<a id="S00108"></a>
**[00:06:41 → 00:06:43] [Người nói?]** Đấy em luôn cho luôn cái chuỗi ví dụ ở đây

<a id="S00109"></a>
**[00:06:44 → 00:06:46] [Người nói?]** Thì trình bày của thầy thì em thấy là rõ rất nhiều

<a id="S00110"></a>
**[00:06:47 → 00:06:49] [Người nói?]** Cả trong báo cáo cũng trong slides

<a id="S00111"></a>
**[00:06:51 → 00:06:51] [Người nói?]** Vâng ạ

<a id="S00112"></a>
**[00:06:51 → 00:06:51] [Người nói?]** Đúng chưa

<a id="S00113"></a>
**[00:06:52 → 00:06:54] [Người nói?]** Thì em gắn gọn thôi không cần dài

<a id="S00114"></a>
**[00:06:54 → 00:06:54] [Người nói?]** Vâng

<a id="S00115"></a>
**[00:06:54 → 00:07:01] [Người nói?]** Thì đây là quy trình tiền xử lý dữ liệu của em ạ.

<a id="S00116"></a>
**[00:07:01 → 00:07:04] [Người nói?]** Thì là đầu tiên là em sẽ có một bộ dữ liệu

<a id="S00117"></a>
**[00:07:04 → 00:07:06] [Người nói?]** Thì bộ dữ liệu này chỉ đơn giản là có hai cột

<a id="S00118"></a>
**[00:07:06 → 00:07:08] [Người nói?]** Một cột payload và một cột được đánh nhãn.

<a id="S00119"></a>
**[00:07:08 → 00:07:11] [Người nói?]** Tiếp theo là em sẽ chuẩn hóa

<a id="S00120"></a>
**[00:07:11 → 00:07:16] [Người nói?]** Thì là em sẽ cố gắng chuyển tất cả các chữ kiểu dấu nháy

<a id="S00121"></a>
**[00:07:16 → 00:07:18] [Người nói?]** Chữ hoa, chữ thường và khoảng trắng

<a id="S00122"></a>
**[00:07:18 → 00:07:19] [Người nói?]** Khoảng trắng dài

<a id="S00123"></a>
**[00:07:19 → 00:07:22] [Người nói?]** Thì sẽ chuyển hết về một khoảng trắng

<a id="S00124"></a>
**[00:07:22 → 00:07:26] [Người nói?]** Và chữ hoa, chữ thường thì chuyển hết về chữ thường

<a id="S00125"></a>
**[00:07:26 → 00:07:29] [Người nói?]** Nghĩa là đồng bộ hóa lại để hạn chế việc là

<a id="S00126"></a>
**[00:07:30 → 00:07:35] [Người nói?]** [nghe không rõ 00:07:30; cần đối chiếu] sinh giặc học quá nhiều token, học quá nhiều các đặc trưng

<a id="S00127"></a>
**[00:07:35 → 00:07:40] [Người nói?]** [nghe không rõ 00:07:35; cần đối chiếu] si quần gan là học quá nhiều đặc trưng nên là trước đây em làm

<a id="S00128"></a>
**[00:07:41 → 00:07:46] [Người nói?]** vấn đề mà em gặp phải là quá nhiều đặc tính nó hồi học

<a id="S00129"></a>
**[00:07:46 → 00:07:48] [Người nói?]** nên là em làm thế này để hạ thấp các đặc tính xuống

<a id="S00130"></a>
**[00:07:48 → 00:07:49] [Người nói?]** tiếp theo

<a id="S00131"></a>
**[00:07:49 → 00:07:52] [Người nói?]** [nghe không rõ 00:07:49; cần đối chiếu] thầy trước này nhé, xác ngược thầy chung thầy chủ tịch thôi

<a id="S00132"></a>
**[00:07:53 → 00:07:57] [Người nói?]** [nghe không rõ 00:07:53; cần đối chiếu] nhưng mà mình nói như thế này là theo thầy trên website

<a id="S00133"></a>
**[00:07:57 → 00:07:59] [Người nói?]** [nghe không rõ 00:07:57; cần đối chiếu] nên chỉ có mỗi 1 cái shadow này

<a id="S00134"></a>
**[00:08:00 → 00:08:04] [Người nói?]** [nghe không rõ 00:08:00; cần đối chiếu] Em gạch đầu dòng có thể có 1 số lý do tại sao tiền sử dụng như em nói

<a id="S00135"></a>
**[00:08:04 → 00:08:08] [Người nói?]** [nghe không rõ 00:08:04; cần đối chiếu] Đúng không? Đấy nó rất hợp chút nào thì mình cần tiền sử dụng

<a id="S00136"></a>
**[00:08:10 → 00:08:14] [Người nói?]** [nghe không rõ 00:08:10; cần đối chiếu] Đúng không? Chứ em nói bao giờ gần như mọi người chắc không vào tay được

<a id="S00137"></a>
**[00:08:15 → 00:08:20] [Người nói?]** Thế nên mình vừa nói thì phải có vừa 1 số gạch đầu dòng trên slide đó

<a id="S00138"></a>
**[00:08:20 → 00:08:24] [Người nói?]** Em đặt thầy vậy là em nên đưa ra ví dụ hay em cũng chỉ giải thích

<a id="S00139"></a>
**[00:08:24 → 00:08:27] [Người nói?]** Không, trước này là 1 ví dụ, trước này là gạch 1 số đầu dòng là lý do tại sao

<a id="S00140"></a>
**[00:08:27 → 00:08:32] [Người nói?]** [nghe không rõ 00:08:27; cần đối chiếu] để sử dụng vật làm cái gì. Sau đó em mô tả quy trình này.

<a id="S00141"></a>
**[00:08:34 → 00:08:37] [Người nói?]** [nghe không rõ 00:08:34; cần đối chiếu] Chứ kể cái pseudo nó quá bé nên nó tăng cái text lên.

<a id="S00142"></a>
**[00:08:42 → 00:08:46] [Người nói?]** Ở đây mình không thể nhìn được cái text nhỏ nhỏ.

<a id="S00143"></a>
**[00:08:51 → 00:08:54] [Người nói?]** Tiếp theo là tạo fingerprint.

<a id="S00144"></a>
**[00:08:54 → 00:09:02] [Người nói?]** Ở đây thay vì trong các câu lệnh sẽ có những số như 1, 2, 3 hoặc là 99.

<a id="S00145"></a>
**[00:09:03 → 00:09:11] [Người nói?]** thì nếu như để số riêng như thế thì là mô hình nó sẽ học ví dụ như có 99 con số cùng một chức năng

<a id="S00146"></a>
**[00:09:11 → 00:09:16] [Người nói?]** nghĩa là chỉ có giá trị số thì mô hình sẽ phải học tận 99 đặc tính

<a id="S00147"></a>
**[00:09:16 → 00:09:22] [Người nói?]** [nghe không rõ 00:09:16; cần đối chiếu] thay vì thế là em sẽ chuyển hóa tất cả những giá trị ký tự dạng số này thành một chuỗi là ví dụ như 5

<a id="S00148"></a>
**[00:09:22 → 00:09:29] [Người nói?]** [nghe không rõ 00:09:22; cần đối chiếu] để mã hóa lại hoặc là character để mã hóa lại để tập trung dữ liệu hơn

<a id="S00149"></a>
**[00:09:29 → 00:09:33] [Người nói?]** Nghĩa là những cái dữ liệu mà có chung chức năng thì em sẽ em hóa lại ở chung ạ.

<a id="S00150"></a>
**[00:09:33 → 00:09:35] [Người nói?]** [nghe không rõ 00:09:33; cần đối chiếu] Mình nhớ rất là hẻm thẻ em có 15 phần trình bày.

<a id="S00151"></a>
**[00:09:35 → 00:09:36] [Người nói?]** [nghe không rõ 00:09:35; cần đối chiếu] Hôm tới bảo hỏi 8 thế.

<a id="S00152"></a>
**[00:09:36 → 00:09:39] [Người nói?]** Nếu em cứ lăm man này thì em sẽ không đi vào chính được.

<a id="S00153"></a>
**[00:09:41 → 00:09:42] [Người nói?]** Đây là tập để không báo cáo luôn đấy.

<a id="S00154"></a>
**[00:09:43 → 00:09:43] [Người nói?]** Cảm ơn.

<a id="S00155"></a>
**[00:09:45 → 00:09:46] [Người nói?]** Giờ em cũng mới nhận ra.

<a id="S00156"></a>
**[00:09:46 → 00:09:48] [Người nói?]** Em hãy chú ý kỹ hơn.

<a id="S00157"></a>
**[00:09:48 → 00:09:55] [Người nói?]** Tiếp theo là cuối cùng là em sẽ phân loại ra 4 họp SQL dựa trên các đặc tính mà em có nói ở slide trước ạ.

<a id="S00158"></a>
**[00:09:55 → 00:09:58] [Người nói?]** [nghe không rõ 00:09:55; cần đối chiếu] Thông qua một thư viện gọi là SQL Power.

<a id="S00159"></a>
**[00:10:01 → 00:10:07] [Người nói?]** trong này sẽ có 2 nhánh sinh dữ liệu

<a id="S00160"></a>
**[00:10:07 → 00:10:16] [Người nói?]** thì là đầu tiên là trong này sẽ có nhánh sinh dạng dữ liệu cấu trúc

<a id="S00161"></a>
**[00:10:16 → 00:10:17] [Người nói?]** nghĩa là dạng kiểu token

<a id="S00162"></a>
**[00:10:17 → 00:10:22] [Người nói?]** còn những dạng mà chỉ cần dạng bình thường

<a id="S00163"></a>
**[00:10:22 → 00:10:27] [Người nói?]** nghĩa là dữ liệu dạng chỉ có 2 cột là cột payload và cột đánh nhãn

<a id="S00164"></a>
**[00:10:27 → 00:10:31] [Người nói?]** thì em sẽ sinh ra làm 2 nhánh để phục vụ cho 2 mục tiêu riêng

## Trình bày mô hình và thiết kế sơ đồ

<a id="S00165"></a>
**[00:10:31 → 00:10:36] [Người nói?]** Đây là tổng quan về 5 phương pháp của em

<a id="S00166"></a>
**[00:10:36 → 00:10:46] [Người nói?]** [nghe không rõ 00:10:36; cần đối chiếu] Thì đầu tiên là em sẽ đến với thuật toán của SMOD

<a id="S00167"></a>
**[00:10:46 → 00:10:49] [Người nói?]** Thì là em dựa trên bài báo vào năm 2002

<a id="S00168"></a>
**[00:10:51 → 00:10:54] [Người nói?]** Về bài báo liên quan đến nội sinh gốc

<a id="S00169"></a>
**[00:10:54 → 00:10:56] [Người nói?]** Bài báo gốc về thuật toán

<a id="S00170"></a>
**[00:10:56 → 00:10:58] [Người nói?]** Thì đây là cấu trúc

<a id="S00171"></a>
**[00:10:58 → 00:11:04] [Người nói?]** Thì cấu trúc của nó là nó sẽ cố gắng nội sinh

<a id="S00172"></a>
**[00:11:05 → 00:11:07] [Người nói?]** Để tìm ra được giá trị gần nhất

<a id="S00173"></a>
**[00:11:09 → 00:11:10] [Người nói?]** Tìm ra được giá trị gần nhất

<a id="S00174"></a>
**[00:11:11 → 00:11:14] [Người nói?]** phù hợp và từ đó là nó sẽ sinh ra dữ liệu

<a id="S00175"></a>
**[00:11:17 → 00:11:20] [Người nói?]** sinh ra dữ liệu mà có cái độ tương đồng gần nhất

<a id="S00176"></a>
**[00:11:20 → 00:11:25] [Người nói?]** thì trong này sẽ có các công thức

<a id="S00177"></a>
**[00:11:28 → 00:11:29] [Người nói?]** anh muốn hỏi là

<a id="S00178"></a>
**[00:11:29 → 00:11:33] [Người nói?]** [nghe không rõ 00:11:29; cần đối chiếu] em về nhà tập, có 15 chừng 7

<a id="S00179"></a>
**[00:11:33 → 00:11:37] [Người nói?]** tập cho nó chuẩn những cái gì mà nó không phải trọng tâm của mày

<a id="S00180"></a>
**[00:11:37 → 00:11:38] [Người nói?]** [nghe không rõ 00:11:37; cần đối chiếu] để có định sự đi xa

<a id="S00181"></a>
**[00:11:40 → 00:11:46] [Người nói?]** [nghe không rõ 00:11:40; cần đối chiếu] tiếp theo là GAN thì là dựa trên bài báo 2014 của Godfrey

<a id="S00182"></a>
**[00:11:46 → 00:11:49] [Người nói?]** Thì bài báo này cũng là nền tảng của mô hình GAN

<a id="S00183"></a>
**[00:11:49 → 00:11:53] [Người nói?]** Thì đây cũng là lưu đồ thật toán

<a id="S00184"></a>
**[00:11:54 → 00:11:56] [Người nói?]** Thì nó khá là cơ bản

<a id="S00185"></a>
**[00:11:56 → 00:12:02] [Người nói?]** Sẽ tạo ra một generator và tạo ra một discriminator và cố gắng đối kháng

<a id="S00186"></a>
**[00:12:02 → 00:12:09] [Người nói?]** Để có thể tự tiện 2 mỗi 2 thành phần đấy tự tiện hóa để có thể sinh ra dữ liệu tốt hơn

<a id="S00187"></a>
**[00:12:09 → 00:12:15] [Người nói?]** Còn mô hình CTGAN

<a id="S00188"></a>
**[00:12:15 → 00:12:23] [Người nói?]** [nghe không rõ 00:12:15; cần đối chiếu] Mô hình CT GAN là giải quyết bài toán của mô hình GAN là sẽ thay thế hàm mất mát

<a id="S00189"></a>
**[00:12:23 → 00:12:27] [Người nói?]** Bởi vì là mô hình GAN là sẽ rất cần

<a id="S00190"></a>
**[00:12:27 → 00:12:35] [Người nói?]** [nghe không rõ 00:12:27; cần đối chiếu] CT GAN là Contribusal Tabular GAN

<a id="S00191"></a>
**[00:12:35 → 00:12:41] [Người nói?]** Em nhậm Conditional Tabular GAN

<a id="S00192"></a>
**[00:12:43 → 00:12:49] [Người nói?]** Trong mô hình này thì mô hình sẽ không hiểu được ý nghĩa của một chuỗi

<a id="S00193"></a>
**[00:12:50 → 00:12:56] [Người nói?]** Vì vậy là sẽ yêu cầu là cần phải phân tích một chuỗi để ra làm rất nhiều các đặc tính nhỏ hơn

<a id="S00194"></a>
**[00:12:56 → 00:13:00] [Người nói?]** Và từ đó là sẽ học các đặc tính đấy

<a id="S00195"></a>
**[00:13:00 → 00:13:01] [Người nói?]** Quay lại slide trước

<a id="S00196"></a>
**[00:13:13 → 00:13:20] [Người nói?]** [nghe không rõ 00:13:13; cần đối chiếu] Bây giờ em thay thêm một cái hình vẽ khung Facebook của Dan nó dễ hiểu hơn cái này

<a id="S00197"></a>
**[00:13:22 → 00:13:26] [Người nói?]** [nghe không rõ 00:13:22; cần đối chiếu] Đâu là cuối giờ, đâu là cuối đêm, giữ mình vẽ ra

<a id="S00198"></a>
**[00:13:32 → 00:13:35] [Người nói?]** Em đưa thầy phần giải thích của em có cần phải cải thiện

<a id="S00199"></a>
**[00:13:35 → 00:13:38] [Người nói?]** [nghe không rõ 00:13:35; cần đối chiếu] Hay là hỏi em phải phóng thói thì người ta hãy tự tươi dây nhìn với sơ đồ em

<a id="S00200"></a>
**[00:13:38 → 00:13:40] [Người nói?]** thì đọc hỏi nó là cái gì đấy.

<a id="S00201"></a>
**[00:13:41 → 00:13:45] [Người nói?]** [nghe không rõ 00:13:41; cần đối chiếu] Còn người ta đã quen với vật ngang nữa rồi thì mình nên theo chủ ngang.

<a id="S00202"></a>
**[00:13:46 → 00:13:47] [Người nói?]** Chạy từ trái sang phải.

<a id="S00203"></a>
**[00:13:49 → 00:13:53] [Người nói?]** Bây giờ em tự sợ trên mạng mình một cái sơ đồ gàn bao giờ đã vẽ là chạy trái sang phải

<a id="S00204"></a>
**[00:13:53 → 00:13:54] [Người nói?]** [nghe không rõ 00:13:53; cần đối chiếu] thì chạy xuống dưới chiếc của em.

<a id="S00205"></a>
**[00:13:57 → 00:14:02] [Người nói?]** [nghe không rõ 00:13:57; cần đối chiếu] Gàn mô đồ. Đúng chưa?

<a id="S00206"></a>
**[00:14:03 → 00:14:06] [Người nói?]** Ít nhất là một vài cái em thấy nó chạy từ trái sang phải.

<a id="S00207"></a>
**[00:14:06 → 00:14:08] [Người nói?]** Đúng không?

<a id="S00208"></a>
**[00:14:10 → 00:14:15] [Người nói?]** Mình đừng có phát minh ra một cái mới gì cho nó khó hình dung.

<a id="S00209"></a>
**[00:14:15 → 00:14:17] [Người nói?]** Chọn cái tiêu biểu nhất để thầy hay dùng.

<a id="S00210"></a>
**[00:14:17 → 00:14:30] [Người nói?]** [nghe không rõ 00:14:17; cần đối chiếu] Được chưa anh? Rồi, tiếp theo là Sequel Gantt

<a id="S00211"></a>
**[00:14:30 → 00:14:38] [Người nói?]** [nghe không rõ 00:14:30; cần đối chiếu] Sequel Gantt, anh sẽ chú ý để vẽ kỹ hơn

<a id="S00212"></a>
**[00:14:41 → 00:14:46] [Người nói?]** Một người chú ý giúp mình nghĩ là các em nếu dùng AI sinh slide thì phải chú ý

<a id="S00213"></a>
**[00:14:46 → 00:14:51] [Người nói?]** Nó còn sinh bé xíu, tức là mình phải cố gắng nhìn và điều chỉnh

<a id="S00214"></a>
**[00:14:53 → 00:14:59] [Người nói?]** Ở nhà anh để máy tính lên lớp cách cao khoảng 10-15m xem mình có thể nhìn được không

## Vấn đề quan sát và các hướng cải tiến

<a id="S00215"></a>
**[00:15:08 → 00:15:13] [Người nói?]** Thì đây là các vấn đề em quan sát ở gan cơ sở

<a id="S00216"></a>
**[00:15:18 → 00:15:28] [Người nói?]** [nghe không rõ 00:15:18; cần đối chiếu] Thì đây là em nêu ra các vấn đề mà em nhận thấy mô hình si quần gan gặp phải

<a id="S00217"></a>
**[00:15:28 → 00:15:33] [Người nói?]** Thì đầu tiên là cần phải tokenize theo ký tự

<a id="S00218"></a>
**[00:15:33 → 00:15:38] [Người nói?]** bởi vì là các ký tự mà có chung cái mục đích và có chung chức năng

<a id="S00219"></a>
**[00:15:38 → 00:15:41] [Người nói?]** thì nếu như mà không tokenize hóa lại

<a id="S00220"></a>
**[00:15:41 → 00:15:43] [Người nói?]** thì nó sẽ sinh ra rất nhiều các cái đặc tính

<a id="S00221"></a>
**[00:15:43 → 00:15:45] [Người nói?]** mặc dù là nó không giải quyết vấn đề gì ạ

<a id="S00222"></a>
**[00:15:45 → 00:15:50] [Người nói?]** Tiếp theo là trong bài toán mà tác giả Yu đưa ra.

<a id="S00223"></a>
**[00:15:50 → 00:15:52] [Người nói?]** thì độ dài tối đa là 20 ạ

<a id="S00224"></a>
**[00:15:52 → 00:15:55] [Người nói?]** thì là đối với những payload mà nó quá dài

<a id="S00225"></a>
**[00:15:55 → 00:15:58] [Người nói?]** thì nó sẽ bị cắt đi rất nhiều thành phần khá quan trọng ạ

<a id="S00226"></a>
**[00:15:58 → 00:16:02] [Người nói?]** tiếp theo là reward thì chỉ đến từ discriminator

<a id="S00227"></a>
**[00:16:03 → 00:16:08] [Người nói?]** Thì nghĩa là trong này Discriminator chỉ có khả năng nhận biết xem là

<a id="S00228"></a>
**[00:16:08 → 00:16:15] [Người nói?]** Theo thầy như thế này, tức là em sẽ trình bày như thế này

<a id="S00229"></a>
**[00:16:15 → 00:16:16] [Người nói?]** [nghe không rõ 00:16:15; cần đối chiếu] Tức là em sẽ trình bày sức khỏe gan sau

<a id="S00230"></a>
**[00:16:16 → 00:16:18] [Người nói?]** Và em sẽ trình bày luôn phần thử nghiệm

<a id="S00231"></a>
**[00:16:20 → 00:16:22] [Người nói?]** Thử nghiệm giữa các hộ gan với nhau

<a id="S00232"></a>
**[00:16:23 → 00:16:24] [Người nói?]** Và với SMOTE

<a id="S00233"></a>
**[00:16:25 → 00:16:31] [Người nói?]** Sau đó em sẽ đi sang phần nhận xét về vấn đề của nó và các cải tiến

<a id="S00234"></a>
**[00:16:32 → 00:16:33] [Người nói?]** Anh chú ý cho đấy

<a id="S00235"></a>
**[00:16:33 → 00:16:39] [Người nói?]** Rồi, em xin hãy trình bày tiếp nốt slide này ạ

<a id="S00236"></a>
**[00:16:39 → 00:16:44] [Người nói?]** [nghe không rõ 00:16:39; cần đối chiếu] Thì Reward của Digital Editor chỉ có khả năng nhận biết xem là dữ liệu có phải dữ liệu tạo sinh hay không

<a id="S00237"></a>
**[00:16:44 → 00:16:48] [Người nói?]** Chứ không có khả năng nhận biết là có phải mẫu SQL thực tế hay không

<a id="S00238"></a>
**[00:16:48 → 00:16:55] [Người nói?]** Và bất cân bằng nghiêm trọng thì ở đây là khi mà dữ liệu càng ngày càng ít đi ạ

<a id="S00239"></a>
**[00:16:55 → 00:17:01] [Người nói?]** Thì dữ liệu nó sẽ chỉ cố gắng sinh ra những dữ liệu mà nó có khả năng đạt điểm cao nhất ạ

<a id="S00240"></a>
**[00:17:01 → 00:17:05] [Người nói?]** Thế nên là nó sẽ lặp đi lặp lại một cấu trúc chung ạ.

<a id="S00241"></a>
**[00:17:05 → 00:17:10] [Người nói?]** Và tường lửa thực tế thì nó sẽ bị nhận nhầm

<a id="S00242"></a>
**[00:17:10 → 00:17:12] [Người nói?]** [nghe không rõ 00:17:10; cần đối chiếu] Nghĩa là nó sẽ bị nhận nhầm nhoi thành tấn công ạ

<a id="S00243"></a>
**[00:17:12 → 00:17:16] [Người nói?]** Đây là 5 vấn đề mà em đã gặp phải trong lúc triển khai thử nghiệm ạ

<a id="S00244"></a>
**[00:17:17 → 00:17:23] [Người nói?]** Thì đấy em sẽ đề xuất là 4 phương án cải tiến để xử lý cho các vấn đề trên ạ

<a id="S00245"></a>
**[00:17:24 → 00:17:29] [Người nói?]** Thì đầu tiên là như em nói là có tokenize SQL ạ

<a id="S00246"></a>
**[00:17:29 → 00:17:34] [Người nói?]** những cái ký tự mà có chung cái ý nghĩa thì sẽ được tokenize hóa lại ạ

<a id="S00247"></a>
**[00:17:34 → 00:17:38] [Người nói?]** [nghe không rõ 00:17:34; cần đối chiếu] tiếp theo là em sẽ tăng pre-chain lên ạ

<a id="S00248"></a>
**[00:17:38 → 00:17:42] [Người nói?]** bởi vì là discriminator là khá là mạnh

<a id="S00249"></a>
**[00:17:42 → 00:17:46] [Người nói?]** [nghe không rõ 00:17:42; cần đối chiếu] nên là em sẽ cố gắng tăng cái generator pre-chain lên

<a id="S00250"></a>
**[00:17:46 → 00:17:49] [Người nói?]** một con số cao hơn là 120

<a id="S00251"></a>
**[00:17:50 → 00:17:54] [Người nói?]** em sẽ so sánh giữa 120 là của tác giả và 160 là của em ạ

<a id="S00252"></a>
**[00:17:58 → 00:18:09] [Người nói?]** [nghe không rõ 00:17:58; cần đối chiếu] của tác giả là chỉ có 120 nên là khi em làm là vẫn bị cô lao tiếp theo là em sẽ tăng độ dài thì

<a id="S00253"></a>
**[00:18:09 → 00:18:19] [Người nói?]** là tăng từ 20 lên 160 độ dài của trách tờ thì là độ dài độ dài Vâng vâng độ dài của chuỗi đầu vào

<a id="S00254"></a>
**[00:18:25 → 00:18:37] [Người nói?]** [nghe không rõ 00:18:25; cần đối chiếu] Thì ở 20 thì mô hình sẽ chỉ học từng câu nhưng nếu mà tăng lên 1.600 là mô hình sẽ học đến có thể là từng ký tự trong câu

<a id="S00255"></a>
**[00:18:37 → 00:18:49] [Người nói?]** [nghe không rõ 00:18:37; cần đối chiếu] Và cuối cùng là reward cấu trúc thì thay vì để 100% là discriminator thì em sẽ lấy thêm 0.3 đánh giá đến từ SQL PAR

<a id="S00256"></a>
**[00:18:49 → 00:18:53] [Người nói?]** để có thể cố gắng học được cả cấu trúc của SQL nữa

<a id="S00257"></a>
**[00:18:53 → 00:18:59] [Người nói?]** Thì đấy là 4 phần cập nhật mà em áp dụng vào

## Các giai đoạn và kịch bản thử nghiệm

<a id="S00258"></a>
**[00:19:03 → 00:19:10] [Người nói?]** Đây là mô hình của em được chia làm 5 giai đoạn

<a id="S00259"></a>
**[00:19:11 → 00:19:15] [Người nói?]** Thì đầu tiên giai đoạn đầu vào là sẽ chạy 4 mô hình cơ bản

<a id="S00260"></a>
**[00:19:20 → 00:19:27] [Người nói?]** [nghe không rõ 00:19:20; cần đối chiếu] không em không không được em cái này em cắt từ bên luận án bài Word của em xa em

<a id="S00261"></a>
**[00:19:35 → 00:19:44] [Người nói?]** thì đầu tiên là khảo sát ban đầu ạ để xem là vấn đề thực tế gặp phải của các mô hình sinh

<a id="S00262"></a>
**[00:19:44 → 00:19:46] [Người nói?]** tính dữ liệu khi giải quyết bài toán SQL injection

<a id="S00263"></a>
**[00:19:46 → 00:19:52] [Người nói?]** Sau đó là em sẽ chọn các tỷ lệ và chọn dạng dữ liệu

<a id="S00264"></a>
**[00:19:53 → 00:19:58] [Người nói?]** Đầu nghĩa là em sẽ phân tích xem là liệu biến đổi ở phần dữ liệu nó có tác dụng không

<a id="S00265"></a>
**[00:19:58 → 00:19:59] [Người nói?]** và biến đổi ở các

<a id="S00266"></a>
**[00:20:00 → 00:20:04] [Người nói?]** cái tỷ lệ thông số chạy thì nó có tác dụng không ạ tiếp theo

<a id="S00267"></a>
**[00:20:04 → 00:20:12] [Người nói?]** [nghe không rõ 00:20:04; cần đối chiếu] là khi đó là em sẽ đề xuất các 8 phương án để có thể thay thế nâng cấp của mô hình sinh quần gan ạ

<a id="S00268"></a>
**[00:20:12 → 00:20:22] [Người nói?]** thì như ở trong sai trước ạ em có đề xuất là 4 cái hướng xử lý ạ thì em sẽ cho chạy thì là kết hợp

<a id="S00269"></a>
**[00:20:23 → 00:20:25] [Người nói?]** kết hợp 4 cái phương án đấy

<a id="S00270"></a>
**[00:20:25 → 00:20:28] [Người nói?]** thì nó sẽ để ra là 8 kịch bản

<a id="S00271"></a>
**[00:20:28 → 00:20:31] [Người nói?]** thì có kịch bản sẽ là không phương án

<a id="S00272"></a>
**[00:20:31 → 00:20:34] [Người nói?]** nâng cấp nào và sẽ có kịch bản là chỉ 2 phương án nâng cấp

<a id="S00273"></a>
**[00:20:34 → 00:20:37] [Người nói?]** thì tổng cộng là 8 phương án nâng cấp để xem là đâu là

<a id="S00274"></a>
**[00:20:37 → 00:20:39] [Người nói?]** mô hình có độ ổn định cao nhất

<a id="S00275"></a>
**[00:20:39 → 00:20:42] [Người nói?]** cuối cùng là em sẽ chạy đánh giá đầy đủ

<a id="S00276"></a>
**[00:20:42 → 00:20:45] [Người nói?]** khi này là em sẽ chạy với cấu hình tối đa

<a id="S00277"></a>
**[00:20:45 → 00:20:48] [Người nói?]** như khi này là sẽ chạy full Epoch

<a id="S00278"></a>
**[00:20:48 → 00:20:51] [Người nói?]** để đảm bảo là tất cả mô hình đều có chung

<a id="S00279"></a>
**[00:20:52 → 00:20:52] [Người nói?]** chất lượng

<a id="S00280"></a>
**[00:20:52 → 00:20:55] [Người nói?]** và cuối cùng là em sẽ đưa vào trong mô hình tường lửa

<a id="S00281"></a>
**[00:20:55 → 00:20:57] [Người nói?]** để đánh giá kết quả thực tế

<a id="S00282"></a>
**[00:20:57 → 00:21:01] [Người nói?]** thì kết quả của giai đoạn 1

<a id="S00283"></a>
**[00:21:01 → 00:21:03] [Người nói?]** thì là ở đây

<a id="S00284"></a>
**[00:21:03 → 00:21:04] [Người nói?]** thì là mô hình smooth

<a id="S00285"></a>
**[00:21:04 → 00:21:07] [Người nói?]** và 3 mô hình đầu tiên

<a id="S00286"></a>
**[00:21:07 → 00:21:09] [Người nói?]** thì là họ có kết quả rất là tốt

<a id="S00287"></a>
**[00:21:09 → 00:21:10] [Người nói?]** nhưng mà lại là

<a id="S00288"></a>
**[00:21:10 → 00:21:12] [Người nói?]** có bị trùng lặp

<a id="S00289"></a>
**[00:21:13 → 00:21:15] [Người nói?]** khá là cao, trong đó thì mô hình

<a id="S00290"></a>
**[00:21:15 → 00:21:17] [Người nói?]** sequence găng cơ sở thì tuy là

<a id="S00291"></a>
**[00:21:19 → 00:21:20] [Người nói?]** thông số lại xấu hơn

<a id="S00292"></a>
**[00:21:20 → 00:21:22] [Người nói?]** nhưng mà độ trùng lặp thì nó

<a id="S00293"></a>
**[00:21:22 → 00:21:23] [Người nói?]** [nghe không rõ 00:21:22; cần đối chiếu] chỉ rơi khoảng 19,4%

<a id="S00294"></a>
**[00:21:26 → 00:21:36] [Người nói?]** Dạ, nghĩa là bị trùng cấu trúc ạ, cấu trúc của một câu SQL nó bị trùng khớp luôn ạ, nó chỉ đơn giản là thay thế các cái thông số thôi ạ.

<a id="S00295"></a>
**[00:21:38 → 00:21:40] [Người nói?]** Vâng ạ, bản chất chỉ có một cấu trúc riêng ạ.

<a id="S00296"></a>
**[00:21:42 → 00:21:53] [Người nói?]** [nghe không rõ 00:21:42; cần đối chiếu] Vâng, thì khi đấy là em nhận ra là tuy là SQLGAN là có điểm cấu trúc nó thấp hơn và độ độc nhất cũng sẽ thấp nhưng mà nó không bị trùng dữ liệu đầu vào.

<a id="S00297"></a>
**[00:21:53 → 00:21:57] [Người nói?]** [nghe không rõ 00:21:53; cần đối chiếu] Thế nên là em sẽ cố gắng để nâng cấp mô hình SQL Ga lên

<a id="S00298"></a>
**[00:22:00 → 00:22:09] [Người nói?]** Ở giai đoạn 2 thì em sẽ chia ra làm 4 dạng family

<a id="S00299"></a>
**[00:22:09 → 00:22:15] [Người nói?]** Và có 8 kịch bản như em có đề xuất ở trên

<a id="S00300"></a>
**[00:22:16 → 00:22:28] [Người nói?]** Phần này em bị thiếu, em không quên mất công việc

<a id="S00301"></a>
**[00:22:28 → 00:22:36] [Người nói?]** thì đây là từ A đến F thì nó sẽ là các kịch bản để em sử dụng để thay thế đấy

<a id="S00302"></a>
**[00:22:36 → 00:22:37] [Người nói?]** kịch bản không thay đổi gì hả kịch bản?

<a id="S00303"></a>
**[00:22:38 → 00:22:38] [Người nói?]** dạ

<a id="S00304"></a>
**[00:22:39 → 00:22:41] [Người nói?]** không thay đổi là A

<a id="S00305"></a>
**[00:22:42 → 00:22:46] [Người nói?]** [nghe không rõ 00:22:42; cần đối chiếu] phần này em bị thiếu, em xin phép em mở vào Facebook của em đi

<a id="S00306"></a>
**[00:22:48 → 00:23:45] [Người nói?]** phần này em không để ý, em đã không đưa vào

<a id="S00307"></a>
**[00:23:45 → 00:23:55] [Người nói?]** thì đây ạ, tổng cộng là 6 kịch bản ạ

<a id="S00308"></a>
**[00:23:55 → 00:23:59] [Người nói?]** Nghĩa là khi mà chọn dữ liệu mất cân bằng

<a id="S00309"></a>
**[00:23:59 → 00:24:00] [Người nói?]** Nghĩa là em sẽ

<a id="S00310"></a>
**[00:24:01 → 00:24:03] [Người nói?]** Nghĩa là ví dụ như em sẽ có 3.000 dữ liệu

<a id="S00311"></a>
**[00:24:03 → 00:24:05] [Người nói?]** Em sẽ chỉ lấy 1.000 dữ liệu

<a id="S00312"></a>
**[00:24:05 → 00:24:08] [Người nói?]** Để có thể mô tả được về việc mất cân bằng dữ liệu

<a id="S00313"></a>
**[00:24:08 → 00:24:11] [Người nói?]** Thì trong đó em sẽ có tổng cộng là 6 phương án chọn

<a id="S00314"></a>
**[00:24:11 → 00:24:14] [Người nói?]** Thì đầu tiên là em sẽ chọn theo thứ tự

<a id="S00315"></a>
**[00:24:15 → 00:24:16] [Người nói?]** Độ dài

<a id="S00316"></a>
**[00:24:16 → 00:24:16] [Người nói?]** Vâng ạ

<a id="S00317"></a>
**[00:24:20 → 00:24:22] [Người nói?]** Thì sẽ có tổng cộng là

<a id="S00318"></a>
**[00:24:24 → 00:24:27] [Người nói?]** Thì A và B sẽ chọn theo độ dài

<a id="S00319"></a>
**[00:24:27 → 00:24:29] [Người nói?]** thì A sẽ là chọn ưu tiên dài nhất

<a id="S00320"></a>
**[00:24:29 → 00:24:31] [Người nói?]** và B là ưu tiên ngắn nhất

<a id="S00321"></a>
**[00:24:31 → 00:24:34] [Người nói?]** C là ưu tiên các cái chuỗi

<a id="S00322"></a>
**[00:24:34 → 00:24:35] [Người nói?]** mà nằm ở trong

<a id="S00323"></a>
**[00:24:35 → 00:24:36] [Người nói?]** phần phân vị

<a id="S00324"></a>
**[00:24:36 → 00:24:40] [Người nói?]** [nghe không rõ 00:24:36; cần đối chiếu] nghĩa là những cái chuỗi mà có độ khổ biến cao

<a id="S00325"></a>
**[00:24:40 → 00:24:42] [Người nói?]** tiếp theo là D là em sẽ

<a id="S00326"></a>
**[00:24:42 → 00:24:43] [Người nói?]** chọn ở trong khoảng phân vị

<a id="S00327"></a>
**[00:24:43 → 00:24:45] [Người nói?]** nghĩa là em sẽ bỏ đi

<a id="S00328"></a>
**[00:24:46 → 00:24:47] [Người nói?]** [nghe không rõ 00:24:46; cần đối chiếu] 25% đầu và

<a id="S00329"></a>
**[00:24:48 → 00:24:50] [Người nói?]** [nghe không rõ 00:24:48; cần đối chiếu] 75% sau sẽ chỉ tập trung vào

<a id="S00330"></a>
**[00:24:50 → 00:24:52] [Người nói?]** những cái phần dữ liệu mà có mật độ

<a id="S00331"></a>
**[00:24:52 → 00:24:54] [Người nói?]** cao nhất. Tiếp theo là em sẽ lấy

<a id="S00332"></a>
**[00:24:54 → 00:24:56] [Người nói?]** ngẫu nhiên và con số ngẫu nhiên của em

<a id="S00333"></a>
**[00:24:56 → 00:24:57] [Người nói?]** ở đây em lấy là 88

<a id="S00334"></a>
**[00:24:57 → 00:25:01] [Người nói?]** Và cái cuối cũng là em sẽ lấy theo độ đa dạng

<a id="S00335"></a>
**[00:25:01 → 00:25:02] [Người nói?]** Nghĩa là

<a id="S00336"></a>
**[00:25:02 → 00:25:04] [Người nói?]** Em sẽ tập trung vào

<a id="S00337"></a>
**[00:25:06 → 00:25:08] [Người nói?]** Em sẽ tập trung để lấy

<a id="S00338"></a>
**[00:25:08 → 00:25:10] [Người nói?]** Có thể lấy nhiều nhất các cái đặc tính nhất có thể

<a id="S00339"></a>
**[00:25:10 → 00:25:13] [Người nói?]** Thì đây là tổng cộng là 6 hướng

<a id="S00340"></a>
**[00:25:13 → 00:25:14] [Người nói?]** Mà em đề xuất

<a id="S00341"></a>
**[00:25:14 → 00:25:17] [Người nói?]** Em sẽ chú ý hơn

<a id="S00342"></a>
**[00:25:17 → 00:25:18] [Người nói?]** Bổ sung

<a id="S00343"></a>
**[00:25:21 → 00:25:22] [Người nói?]** Thì đây ạ

<a id="S00344"></a>
**[00:25:22 → 00:25:24] [Người nói?]** Thì kết quả của giai đoạn

<a id="S00345"></a>
**[00:25:29 → 00:25:33] [Người nói?]** Thì đây là kết quả của giai đoạn 2A

<a id="S00346"></a>
**[00:25:33 → 00:25:35] [Người nói?]** Thì là kịch bản

<a id="S00347"></a>
**[00:25:35 → 00:25:36] [Người nói?]** Kịch bản E và D

<a id="S00348"></a>
**[00:25:36 → 00:25:40] [Người nói?]** ED và B là 3 kịch bản

<a id="S00349"></a>
**[00:25:40 → 00:25:41] [Người nói?]** mà có được

<a id="S00350"></a>
**[00:25:42 → 00:25:44] [Người nói?]** thứ hạng 1 hoặc 2

<a id="S00351"></a>
**[00:25:44 → 00:25:45] [Người nói?]** cao nhất ạ

<a id="S00352"></a>
**[00:25:45 → 00:25:47] [Người nói?]** nên em sẽ chọn lấy các 3 kịch bản này ạ

<a id="S00353"></a>
**[00:25:47 → 00:25:49] [Người nói?]** đây là bảng xếp hạng ạ

<a id="S00354"></a>
**[00:25:49 → 00:25:55] [Người nói?]** tiếp theo là đến giai đoạn 2B

<a id="S00355"></a>
**[00:25:55 → 00:25:57] [Người nói?]** thì em sẽ

<a id="S00356"></a>
**[00:25:57 → 00:26:01] [Người nói?]** ở đây em sẽ có tổng cộng là 8 kịch bản

<a id="S00357"></a>
**[00:26:01 → 00:26:12] [Người nói?]** thì ở đây ạ

<a id="S00358"></a>
**[00:26:12 → 00:26:14] [Người nói?]** thì đầu tiên là mã V1

<a id="S00359"></a>
**[00:26:14 → 00:26:15] [Người nói?]** thì sẽ là của

<a id="S00360"></a>
**[00:26:15 → 00:26:18] [Người nói?]** tác giả luôn ạ, không thay thế ạ

<a id="S00361"></a>
**[00:26:18 → 00:26:20] [Người nói?]** thì V2 thì em sẽ tăng

<a id="S00362"></a>
**[00:26:20 → 00:26:21] [Người nói?]** độ dài chuỗi đơn vị tối đa lên

<a id="S00363"></a>
**[00:26:21 → 00:26:24] [Người nói?]** và phần còn lại thì vẫn giữ nguyên

<a id="S00364"></a>
**[00:26:24 → 00:26:26] [Người nói?]** và tương tự với các cái

<a id="S00365"></a>
**[00:26:26 → 00:26:28] [Người nói?]** đặc tính đấy nó là 4 cái hướng

<a id="S00366"></a>
**[00:26:28 → 00:26:29] [Người nói?]** mà em đề xuất

<a id="S00367"></a>
**[00:26:39 → 00:26:40] [Người nói?]** em đang

<a id="S00368"></a>
**[00:26:46 → 00:26:57] [Người nói?]** em chuyển từ

<a id="S00369"></a>
**[00:26:57 → 00:26:57] [Người nói?]** Word sang

<a id="S00370"></a>
**[00:26:57 → 00:26:59] [Người nói?]** đây là

## Chọn kết quả, số liệu cụ thể và ví dụ chuỗi đầu ra

<a id="S00371"></a>
**[00:27:16 → 00:27:18] [Người nói?]** một kịch bản mà có

<a id="S00372"></a>
**[00:27:18 → 00:27:20] [Người nói?]** các cái giá trị cao nhất

<a id="S00373"></a>
**[00:27:20 → 00:27:21] [Người nói?]** [nghe không rõ 00:27:20; cần đối chiếu] ví dụ như của Boland

<a id="S00374"></a>
**[00:27:21 → 00:27:24] [Người nói?]** thì là sẽ có kịch bản D

<a id="S00375"></a>
**[00:27:24 → 00:27:27] [Người nói?]** [nghe không rõ 00:27:24; cần đối chiếu] ở cái phần hàn 2A

<a id="S00376"></a>
**[00:27:27 → 00:27:33] [Người nói?]** Và kịch bản V8 là những kịch bản mà có top những cái giá thông số tốt nhất

<a id="S00377"></a>
**[00:27:36 → 00:27:42] [Người nói?]** Thông số tốt nhất là vẫn là như thế, đầu tiên là dữ liệu sẽ phải độc nhất

<a id="S00378"></a>
**[00:27:42 → 00:27:47] [Người nói?]** Tiếp theo là phải có cấu trúc không bị trùng lập với các cấu trúc ban đầu

<a id="S00379"></a>
**[00:27:47 → 00:27:51] [Người nói?]** Có độ độc nhất riêng và phần quan trọng nhất là phải có cấu trúc SQL

<a id="S00380"></a>
**[00:27:51 → 00:28:01] [Người nói?]** [nghe không rõ 00:27:51; cần đối chiếu] Theo thầy nghĩ là con số cụ thể giống như ở giai đoạn 1, 100% trùng bắp, 19% trùng bắp.

<a id="S00381"></a>
**[00:28:02 → 00:28:10] [Người nói?]** Thầy thì khi mà em làm như thế thì nó sẽ có rất nhiều bảng bởi vì là như ở trong này là của em đã có tận 80 kịch bản.

<a id="S00382"></a>
**[00:28:11 → 00:28:18] [Người nói?]** Thì là em không biết là có nên đưa hẳn toàn bộ thông số vào hay là em nên chỉ tập trung vào những cái mà em lựa chọn nữa.

<a id="S00383"></a>
**[00:28:18 → 00:28:19] [Người nói?]** Nó vẫn khá là nhiều.

<a id="S00384"></a>
**[00:28:19 → 00:28:23] [Người nói?]** Trước mắt em chỉ phải đầy đủ hết đã, sau đó người ta quyết định chọn cái nào.

<a id="S00385"></a>
**[00:28:24 → 00:28:27] [Người nói?]** Vâng, em sẽ điều chỉnh lại.

<a id="S00386"></a>
**[00:28:29 → 00:28:32] [Người nói?]** Trên này có tổng cộng 11 kịch bản.

<a id="S00387"></a>
**[00:28:33 → 00:28:45] [Người nói?]** Do kịch bản V8 thắng ở mọi kịch bản nên nó bị mất đi 1 kịch bản.

<a id="S00388"></a>
**[00:28:45 → 00:28:46] [Người nói?]** Bởi vì nó bị trùng nhau.

<a id="S00389"></a>
**[00:28:46 → 00:28:53] [Người nói?]** [nghe không rõ 00:28:46; cần đối chiếu] Nhưng mà tổng cộng là ở đây em có 11 kịch bản là em sẽ đề xuất để nâng cấp đưa vào trong mô hình si quần gan để chạy thử

<a id="S00390"></a>
**[00:28:53 → 00:29:03] [Người nói?]** Thì đây là kết quả của giai đoạn 3

<a id="S00391"></a>
**[00:29:03 → 00:29:10] [Người nói?]** [nghe không rõ 00:29:03; cần đối chiếu] Thì khi ở đây em sẽ chỉ tập trung chạy mô hình si quần gan với các nâng cấp của em

<a id="S00392"></a>
**[00:29:10 → 00:29:15] [Người nói?]** Thì ở đây là cấu trúc V8 thì sẽ có thông số tốt nhất

<a id="S00393"></a>
**[00:29:15 → 00:29:17] [Người nói?]** Thì độ độc nhất rất là cao

<a id="S00394"></a>
**[00:29:17 → 00:29:22] [Người nói?]** [nghe không rõ 00:29:17; cần đối chiếu] Và học được cấu trúc là tỷ lệ đến gần 85%

<a id="S00395"></a>
**[00:29:22 → 00:29:25] [Người nói?]** Tiếp theo sau là 3 mô hình còn lại

<a id="S00396"></a>
**[00:29:25 → 00:29:31] [Người nói?]** Thì đến cuối cùng là giai đoạn cuối là em sẽ chạy

<a id="S00397"></a>
**[00:29:31 → 00:29:33] [Người nói?]** Em sẽ chạy toàn bộ

<a id="S00398"></a>
**[00:29:33 → 00:29:37] [Người nói?]** Thì đây là thông số

<a id="S00399"></a>
**[00:29:38 → 00:29:40] [Người nói?]** Thì ở đây là em sẽ chỉ tập trung vào 3 tỷ lệ

<a id="S00400"></a>
**[00:29:40 → 00:29:44] [Người nói?]** Là 1 trên 100, 1 trên 200 và 1 trên 500

<a id="S00401"></a>
**[00:29:44 → 00:29:54] [Người nói?]** Đây em đang bị đưa thiếu khá nhiều thông tin

<a id="S00402"></a>
**[00:29:54 → 00:29:59] [Người nói?]** Thì em này xin phép là để buổi sau em sẽ bổ sung kỹ hơn

<a id="S00403"></a>
**[00:29:59 → 00:29:59] [Người nói?]** Vì

<a id="S00404"></a>
**[00:30:00 → 00:30:01] [Người nói?]** nói ra hơi bị dài

<a id="S00405"></a>
**[00:30:02 → 00:30:04] [Người nói?]** tiếp theo là

<a id="S00406"></a>
**[00:30:04 → 00:30:06] [Người nói?]** em sẽ đưa toàn bộ tất cả dữ liệu

<a id="S00407"></a>
**[00:30:06 → 00:30:08] [Người nói?]** được sinh ra từ các kịch bản

<a id="S00408"></a>
**[00:30:08 → 00:30:09] [Người nói?]** trên và đưa qua

<a id="S00409"></a>
**[00:30:09 → 00:30:10] [Người nói?]** [nghe không rõ 00:30:09; cần đối chiếu] từng lửa

<a id="S00410"></a>
**[00:30:10 → 00:30:16] [Người nói?]** [nghe không rõ 00:30:10; cần đối chiếu] thì là ở mô hình si quần gan cải tiến

<a id="S00411"></a>
**[00:30:16 → 00:30:17] [Người nói?]** của em ạ, thì tỷ lệ

<a id="S00412"></a>
**[00:30:17 → 00:30:20] [Người nói?]** bị chặn là nó sẽ

<a id="S00413"></a>
**[00:30:21 → 00:30:22] [Người nói?]** bị chặn

<a id="S00414"></a>
**[00:30:25 → 00:30:26] [Người nói?]** [nghe không rõ 00:30:25; cần đối chiếu] xe này cũng bị đưa

<a id="S00415"></a>
**[00:30:27 → 00:30:28] [Người nói?]** [nghe không rõ 00:30:27; cần đối chiếu] xe này cũng bị đưa thiếu

<a id="S00416"></a>
**[00:30:28 → 00:30:29] [Người nói?]** nhưng mà ý em là

<a id="S00417"></a>
**[00:30:29 → 00:30:31] [Người nói?]** [nghe không rõ 00:30:29; cần đối chiếu] trong mô hình si quần gan thì là

<a id="S00418"></a>
**[00:30:31 → 00:30:38] [Người nói?]** [nghe không rõ 00:30:31; cần đối chiếu] là tỷ lệ mà vừa bị không bị chặn và vẫn có cấu trúc ạ thì nó nhân đôi với nhau ạ thì nó sẽ có

<a id="S00419"></a>
**[00:30:38 → 00:30:45] [Người nói?]** [nghe không rõ 00:30:38; cần đối chiếu] thông số là cao nhất ạ còn các mô hình còn lại thì là hầu hết là do bị nó được vượt qua từng lửa là

<a id="S00420"></a>
**[00:30:45 → 00:30:49] [Người nói?]** [nghe không rõ 00:30:45; cần đối chiếu] do là nó sinh ra dữ liệu nhiếu ạ đấy thì cái chỗ đấy em để mấy người phân tích nhiều ở đây thì

<a id="S00421"></a>
**[00:30:50 → 00:31:06] [Người nói?]** Vâng, em bị đưa thiếu, em sẽ chú ý hơn.

<a id="S00422"></a>
**[00:31:06 → 00:31:13] [Người nói?]** Em nhớ cái này giống như của anh Nam, mình đưa lên cái gì nó phải hỗ trợ ra cái quan điểm của mình.

<a id="S00423"></a>
**[00:31:16 → 00:31:18] [Người nói?]** Phần trình bày của em đến đây kết thúc ạ.

<a id="S00424"></a>
**[00:31:19 → 00:31:22] [Người nói?]** Em vẫn muốn em có một ví dụ về kết quả thực tế của em.

<a id="S00425"></a>
**[00:31:22 → 00:31:24] [Người nói?]** Ví dụ về kết quả thực tế của em.

<a id="S00426"></a>
**[00:31:24 → 00:31:29] [Người nói?]** Ví dụ một cái chuỗi như thế này với cơ sở sinh gan.

<a id="S00427"></a>
**[00:31:30 → 00:31:33] [Người nói?]** Một cái chuỗi như thế này.

<a id="S00428"></a>
**[00:31:34 → 00:31:42] [Người nói?]** [nghe không rõ 00:31:34; cần đối chiếu] Ngoài các số liệu thống kê này thì giá trị của sườn gan là nó sinh ra chuỗi.

<a id="S00429"></a>
**[00:31:42 → 00:31:43] [Người nói?]** Chuỗi là người ta nhìn được.

<a id="S00430"></a>
**[00:31:46 → 00:31:46] [Người nói?]** Đúng không?

<a id="S00431"></a>
**[00:31:46 → 00:31:58] [Người nói?]** [nghe không rõ 00:31:46; cần đối chiếu] Vâng, xin cho em là em kết thúc bài trình bày của em và em sẽ cố gắng chỉnh sửa để có thể đưa ra bản size tốt hơn ạ.

<a id="S00432"></a>
**[00:32:01 → 00:32:06] [Người nói?]** [nghe không rõ 00:32:01; cần đối chiếu] Thầy nghĩ là những cái nó coi như là nó ngắn bọn thôi nhưng mà nó toát lên được cái mình làm cái gì và kết quả đạt được cái gì.

<a id="S00433"></a>
**[00:32:07 → 00:32:07] [Người nói?]** Vâng.

<a id="S00434"></a>
**[00:32:08 → 00:32:08] [Người nói?]** Đúng không?

<a id="S00435"></a>
**[00:32:08 → 00:32:08] [Người nói?]** Đúng ạ.

<a id="S00436"></a>
**[00:32:11 → 00:32:23] [Người nói?]** [nghe không rõ 00:32:11; cần đối chiếu] Thế hướng này cũng hay, quan trọng là có thể là cái kết quả sinh ra có thể nó chưa chua nhất, chưa tốt nhưng mà nó có cái hướng phát triển.

<a id="S00437"></a>
**[00:32:23 → 00:32:30] [Người nói?]** [nghe không rõ 00:32:23; cần đối chiếu] Để ví dụ các cơ quan khác thì chỉ xin các chức luôn

<a id="S00438"></a>
**[00:32:30 → 00:32:32] [Người nói?]** [nghe không rõ 00:32:30; cần đối chiếu] Cái này nó xin môn ra nữa

<a id="S00439"></a>
**[00:32:32 → 00:32:42] [Người nói?]** [nghe không rõ 00:32:32; cần đối chiếu] Xin môn ra

<a id="S00440"></a>
**[00:32:42 → 00:32:46] [Người nói?]** [nghe không rõ 00:32:42; cần đối chiếu] Xin môn ra

<a id="S00441"></a>
**[00:32:46 → 00:32:59] [Người nói?]** [nghe không rõ 00:32:46; cần đối chiếu] Xin ra rồi

<a id="S00442"></a>
**[00:32:59 → 00:33:01] [Người nói?]** [nghe không rõ 00:32:59; cần đối chiếu] Cái này là bạn xin xong đây

<a id="S00443"></a>
**[00:33:01 → 00:33:02] [Người nói?]** [nghe không rõ 00:33:01; cần đối chiếu] Nên là có thể giúp anh thấy

<a id="S00444"></a>
**[00:33:02 → 00:33:12] [Người nói?]** [nghe không rõ 00:33:02; cần đối chiếu] Sai trước em là em có đưa ví dụ không truyền đoạn

<a id="S00445"></a>
**[00:33:12 → 00:33:14] [Người nói?]** [nghe không rõ 00:33:12; cần đối chiếu] Và do là em nghĩ là nó

<a id="S00446"></a>
**[00:33:14 → 00:33:16] [Người nói?]** [nghe không rõ 00:33:14; cần đối chiếu] Em lại cho là nó không cần tiên

<a id="S00447"></a>
**[00:33:16 → 00:33:17] [Người nói?]** [nghe không rõ 00:33:16; cần đối chiếu] Em không đưa vào hàng sai

<a id="S00448"></a>
**[00:33:19 → 00:33:29] [Người nói?]** [nghe không rõ 00:33:19; cần đối chiếu] Cái này mới bị tiến rất là cao

<a id="S00449"></a>
**[00:33:29 → 00:33:31] [Người nói?]** Nếu mà em làm thành công

<a id="S00450"></a>
**[00:33:31 → 00:33:32] [Người nói?]** [nghe không rõ 00:33:31; cần đối chiếu] Thì em có thể đối với là

<a id="S00451"></a>
**[00:33:32 → 00:33:34] [Người nói?]** [nghe không rõ 00:33:32; cần đối chiếu] Là một cái côn
