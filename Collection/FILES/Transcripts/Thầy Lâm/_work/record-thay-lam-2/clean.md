# Bản ghi thầy Lâm (2) — làm rõ nghiên cứu GAN hỗ trợ phát hiện SQL injection

Nguồn: [Record thầy Lâm (2).m4a](file:///C:/Users/Admin/Documents/Collection/Data/Recording/Record%20th%E1%BA%A7y%20L%C3%A2m%20%282%29.m4a)

Thời lượng: 00:21:47. ASR: large-v3 / cuda.

Trạng thái: đã rà văn bản; chờ nghe đối chiếu. Người nói chưa được xác định nếu không có ghi chú riêng.
Bản này bảo toàn thứ tự và nội dung nhận dạng; các đoạn nghi lỗi được giữ dấu vết để nghe lại.

## Báo cáo bài toán mất cân bằng và mô hình sinh dữ liệu

<a id="S00001"></a>
**[00:00:00 → 00:00:09] [Người nói?]** Đây đấy, em đang làm nó đang hơi không kiểm soát được ạ

<a id="S00002"></a>
**[00:00:10 → 00:00:14] [Người nói?]** Thì đề tài của em là em sẽ cố gắng sử dụng GAN trong

<a id="S00003"></a>
**[00:00:16 → 00:00:18] [Người nói?]** [nghe không rõ 00:00:16; cần đối chiếu] Tên của anh

<a id="S00004"></a>
**[00:00:18 → 00:00:23] [Người nói?]** À vâng, em có, em viết tiếng Anh, quên chưa đổi lại

<a id="S00005"></a>
**[00:00:23 → 00:00:29] [Người nói?]** Thì em dùng GAN để tấn công SQL

<a id="S00006"></a>
**[00:00:32 → 00:00:39] [Người nói?]** bài toán thì hiện tại là dữ liệu thì sẽ hầu hết sẽ là các dữ liệu của người dùng rất bình thường

<a id="S00007"></a>
**[00:00:39 → 00:00:44] [Người nói?]** đôi lúc mới có dữ liệu tấn công thì tỷ lệ sẽ rơi khoảng từ 100 trên 1 thì tới 1.000 trên 1

<a id="S00008"></a>
**[00:00:45 → 00:00:50] [Người nói?]** thì theo phương pháp bình thường thì mình sẽ chỉ đơn giản là lọc dữ liệu rồi chuyển nó thành vector

<a id="S00009"></a>
**[00:00:50 → 00:00:58] [Người nói?]** [nghe không rõ 00:00:50; cần đối chiếu] có thể dùng MOT để kiểu định dạng lại thì lúc này mình sẽ dùng GAN bởi vì GAN nó có thể học

<a id="S00010"></a>
**[00:00:58 → 00:01:06] [Người nói?]** Còn cái thằng kia nó chỉ đơn giản nội sinh, nghĩa là mình đưa cho nó cái gì thì nó cũng chỉ thay đổi các string

<a id="S00011"></a>
**[00:01:06 → 00:01:12] [Người nói?]** Nó chỉ học nội sinh thôi nhưng nó không có khả năng sinh ra những cái dữ liệu mới để mình có thể học tiếp

<a id="S00012"></a>
**[00:01:12 → 00:01:16] [Người nói?]** Thế em mới đề xuất ra, thì đây là mô hình của em ạ

<a id="S00013"></a>
**[00:01:16 → 00:01:23] [Người nói?]** [nghe không rõ 00:01:16; cần đối chiếu] Thì đầu tiên là em sẽ lấy dữ liệu, lấy dữ liệu trên Kaggle và một số cái Datap

<a id="S00014"></a>
**[00:01:24 → 00:01:29] [Người nói?]** lấy thêm dữ liệu của các cái CVE, nghĩa là người ta ghi nhận những cái tấn công

<a id="S00015"></a>
**[00:01:33 → 00:01:38] [Người nói?]** dữ liệu thì em lấy, thì em cũng mới chỉ lấy khoảng 30.000

<a id="S00016"></a>
**[00:01:38 → 00:01:40] [Người nói?]** bởi vì là dữ liệu tấn công thực tế

<a id="S00017"></a>
**[00:01:40 → 00:01:45] [Người nói?]** thì khi mà em làm thì em thấy là hầu hết là nó chỉ là noise

<a id="S00018"></a>
**[00:01:45 → 00:01:48] [Người nói?]** nghĩa là nó chỉ có khả năng tấn công

<a id="S00019"></a>
**[00:01:48 → 00:01:52] [Người nói?]** lúc mà em gõ thật thì khả năng tấn công thực tế của nó là không có

<a id="S00020"></a>
**[00:01:52 → 00:01:55] [Người nói?]** nó khá là ít, này em mới nhận ra

<a id="S00021"></a>
**[00:01:55 → 00:01:58] [Người nói?]** còn tiếp theo là

<a id="S00022"></a>
**[00:01:58 → 00:02:01] [Người nói?]** trong mô hình nó sẽ có 2 thành phần

<a id="S00023"></a>
**[00:02:01 → 00:02:05] [Người nói?]** đầu tiên là thành phần Generate

<a id="S00024"></a>
**[00:02:05 → 00:02:08] [Người nói?]** [nghe không rõ 00:02:05; cần đối chiếu] và thành phần Qua lịa và thành phần Quy tích

<a id="S00025"></a>
**[00:02:08 → 00:02:12] [Người nói?]** thì em có thêm vào là

<a id="S00026"></a>
**[00:02:12 → 00:02:15] [Người nói?]** trong này sẽ có thêm

<a id="S00027"></a>
**[00:02:15 → 00:02:23] [Người nói?]** trong thành phần này em sẽ có thêm

<a id="S00028"></a>
**[00:02:23 → 00:02:25] [Người nói?]** cái Mutation

<a id="S00029"></a>
**[00:02:25 → 00:02:30] [Người nói?]** [nghe không rõ 00:02:25; cần đối chiếu] Criticization nghĩa là em sẽ cho nó biết định nghĩa cho cả hai thằng

<a id="S00030"></a>
**[00:02:31 → 00:02:32] [Người nói?]** Gây nhiễu của nó

<a id="S00031"></a>
**[00:02:33 → 00:02:37] [Người nói?]** Cái này là em cũng mới tìm hiểu

<a id="S00032"></a>
**[00:02:37 → 00:02:40] [Người nói?]** Thì em đang hiểu là em sẽ cho nó biết là

<a id="S00033"></a>
**[00:02:40 → 00:02:44] [Người nói?]** Bây giờ SQL injection thì nó sẽ phải có những điều kiện tối thiểu là gì

<a id="S00034"></a>
**[00:02:44 → 00:02:47] [Người nói?]** Em cho cả hai thằng nó học luôn

<a id="S00035"></a>
**[00:02:47 → 00:02:50] [Người nói?]** [nghe không rõ 00:02:47; cần đối chiếu] Còn nếu mà làm theo quyền bình thường thì nó đang hơi loạn

<a id="S00036"></a>
**[00:02:50 → 00:02:54] [Người nói?]** Sau khi mà Critic thành công xong

<a id="S00037"></a>
**[00:02:54 → 00:03:00] [Người nói?]** sau đó em sẽ có thêm một lớp để trách nữa thì nó sẽ gồm 3 cái đầu tiên là kiểm tra xem có phải là

<a id="S00038"></a>
**[00:03:00 → 00:03:07] [Người nói?]** SQL không ạ là cái L1 tiếp theo là sẽ kiểm tra xem là khả năng injection của nó nghĩa là xem là thực

<a id="S00039"></a>
**[00:03:07 → 00:03:14] [Người nói?]** tế nó có khả năng tấn công không ạ Hiện tại là em mới chỉ cho quét qua bộ thư viện OpenSource ở trên

<a id="S00040"></a>
**[00:03:14 → 00:03:21] [Người nói?]** mạng rồi ạ còn cái số 3 là em sẽ quét xem là độ đa dạng xem là nó có thật sự đa dạng nghe nó có thật

<a id="S00041"></a>
**[00:03:21 → 00:03:28] [Người nói?]** [nghe không rõ 00:03:21; cần đối chiếu] thật sự hơn được thay thế được em thay được thằng small không ạ thì trong tương lai thì em sẽ thay

<a id="S00042"></a>
**[00:03:28 → 00:03:35] [Người nói?]** thế cái thằng l2 bằng cách là em cho tấn công thực tế trên các tương lửa thông dụng ạ và cái cuối

<a id="S00043"></a>
**[00:03:35 → 00:03:46] [Người nói?]** cùng là các cái thước đo để xem là mô hình của em đạt những giá trị nào thì em cũng vận thì đây là

<a id="S00044"></a>
**[00:03:46 → 00:03:53] [Người nói?]** [nghe không rõ 00:03:46; cần đối chiếu] kết quả thì nếu như mà tỷ lệ mà rất rất cân bằng như kiểu 500 trên 1 ạ cái cổ ngoài cùng ạ thì là

<a id="S00045"></a>
**[00:03:53 → 00:04:03] [Người nói?]** là nó thì cái mô hình sẽ gan nó sẽ hơn được cái phương pháp cơ bản là 42 phần trăm nhưng mà càng

<a id="S00046"></a>
**[00:04:03 → 00:04:11] [Người nói?]** [nghe không rõ 00:04:03; cần đối chiếu] lên cao thì nếu mà tỷ lệ càng thấp thì thằng mốt nó sẽ thắng được thằng gan thì tỷ lệ đem chọn là

<a id="S00047"></a>
**[00:04:11 → 00:04:17] [Người nói?]** [nghe không rõ 00:04:11; cần đối chiếu] 100 100 trên một là tỷ em cho rằng tỷ lệ mất cân bằng đủ để mình có thể dùng phương pháp ra thì

## Kết quả thử nghiệm và lo ngại độ đa dạng/overfit

<a id="S00048"></a>
**[00:04:20 → 00:04:26] [Người nói?]** Ở hình bên phải, em cũng thử chia ra 4 trường hợp

<a id="S00049"></a>
**[00:04:26 → 00:04:29] [Người nói?]** Nghĩa là trong tấn công SQL sẽ có 4 trường hợp

<a id="S00050"></a>
**[00:04:29 → 00:04:33] [Người nói?]** 2 trường hợp đầu tiên là Boolean và Error

<a id="S00051"></a>
**[00:04:33 → 00:04:38] [Người nói?]** Thì cái này dựa trên phản hồi của máy chủ

<a id="S00052"></a>
**[00:04:38 → 00:04:41] [Người nói?]** Nghĩa là nó không thực sự tấn công

<a id="S00053"></a>
**[00:04:41 → 00:04:43] [Người nói?]** Nó sẽ đợi xem phản hồi máy chủ là gì

<a id="S00054"></a>
**[00:04:43 → 00:04:49] [Người nói?]** Và từ đó họ sẽ mường tượng xem hệ thống của mô hình là như nào

<a id="S00055"></a>
**[00:04:49 → 00:04:54] [Người nói?]** Thì nên là 2 cái đầu là nó sẽ không có đặc biệt

<a id="S00056"></a>
**[00:04:54 → 00:04:57] [Người nói?]** Bởi vì nó chỉ đơn giản là tấn công những cái mà mình đã biết rồi ạ

<a id="S00057"></a>
**[00:04:57 → 00:05:02] [Người nói?]** Nhưng mà 2 cái cuối cùng là sẽ cố gắng tấn công vào cơ sở dữ liệu hoặc là máy chủ ạ

<a id="S00058"></a>
**[00:05:02 → 00:05:06] [Người nói?]** Thì khi này thì nó mới thật sự có khác biệt ạ

<a id="S00059"></a>
**[00:05:06 → 00:05:13] [Người nói?]** [nghe không rõ 00:05:06; cần đối chiếu] Thì ở đây là mô hình GAN mà khi tấn công Time Experience Action thì là hơn được 11%

<a id="S00060"></a>
**[00:05:13 → 00:05:17] [Người nói?]** [nghe không rõ 00:05:13; cần đối chiếu] Và nếu mà tấn công Union Bay thì sẽ là 7% ạ

<a id="S00061"></a>
**[00:05:17 → 00:05:28] [Người nói?]** Thì đây là lược đồ Training Curve của em ạ

<a id="S00062"></a>
**[00:05:28 → 00:05:34] [Người nói?]** Thì khi mà em Training khoảng 50 Epoch thì nó sẽ chững lại ạ

<a id="S00063"></a>
**[00:05:35 → 00:05:40] [Người nói?]** Thì ở đây thì là ở mô hình dưới cùng cái số 3 ạ

<a id="S00064"></a>
**[00:05:40 → 00:05:47] [Người nói?]** Thì là cái đầu tiên thì là khi mà đạt tới 50 Epoch

<a id="S00065"></a>
**[00:05:47 → 00:05:54] [Người nói?]** [nghe không rõ 00:05:47; cần đối chiếu] Thì là từ về sau em sẽ chỉ tạo ra S-Conjection chứ không còn tạo nhiều nữa ạ

<a id="S00066"></a>
**[00:05:54 → 00:05:58] [Người nói?]** Nhưng mà còn diversity thì là em đang không để kéo lên trên 0.6

<a id="S00067"></a>
**[00:05:58 → 00:06:08] [Người nói?]** [nghe không rõ 00:05:58; cần đối chiếu] Nghĩa là nó cũng không để sinh ra được cái dữ liệu SQL Action mà nó thật sự nằm ngoài

<a id="S00068"></a>
**[00:06:09 → 00:06:13] [Người nói?]** Nó thật sự nằm ngoài, nghĩa là nó có đem ra sự khác biệt

<a id="S00069"></a>
**[00:06:13 → 00:06:16] [Người nói?]** Khác hẳn so với cái baseline bình thường của em

<a id="S00070"></a>
**[00:06:16 → 00:06:19] [Người nói?]** Thì đây là cái vấn đề lớn nhất mà hiện tại em đã tạo lại

<a id="S00071"></a>
**[00:06:19 → 00:06:21] [Người nói?]** Nghĩa là dùng GAN nhưng mà không đáng kể

<a id="S00072"></a>
**[00:06:21 → 00:06:29] [Người nói?]** [nghe không rõ 00:06:21; cần đối chiếu] Nghĩa là nếu mà chỉ đơn giản là tạo ra khoảng 0.5 thì có thể vừa dùng SMODE được nó cũng không tạo ra khác biệt lớn

<a id="S00073"></a>
**[00:06:29 → 00:06:34] [Người nói?]** Đây là cái em đang thiếu định hướng nhất ạ

<a id="S00074"></a>
**[00:06:35 → 00:06:38] [Người nói?]** Thiếu định hướng cái gì?

<a id="S00075"></a>
**[00:06:38 → 00:06:39] [Người nói?]** Dạ

<a id="S00076"></a>
**[00:06:39 → 00:06:40] [Người nói?]** Thiếu định hướng cái gì?

<a id="S00077"></a>
**[00:06:40 → 00:06:48] [Người nói?]** Nghĩa là về độ đa dạng ạ, em đang muốn sử dụng GAN để sinh ra cái dữ liệu tấn công nó đa dạng ạ

<a id="S00078"></a>
**[00:06:48 → 00:06:51] [Người nói?]** Còn nếu mà nó chỉ rơi vào khoảng

<a id="S00079"></a>
**[00:06:51 → 00:06:52] [Người nói?]** Quality của em nó chỉ 0.5

<a id="S00080"></a>
**[00:06:53 → 00:06:54] [Người nói?]** Thì chứng tỏ là dữ liệu em

<a id="S00081"></a>
**[00:06:54 → 00:06:56] [Người nói?]** Nó cũng không thật sự quá đa dạng

<a id="S00082"></a>
**[00:06:56 → 00:06:58] [Người nói?]** Nó cũng chỉ đơn giản là ghép đi ghép lại

<a id="S00083"></a>
**[00:06:58 → 00:07:00] [Người nói?]** Cái string nó không học được cái mới

<a id="S00084"></a>
**[00:07:00 → 00:07:03] [Người nói?]** Đây là vấn đề lớn nhất

<a id="S00085"></a>
**[00:07:03 → 00:07:04] [Người nói?]** Mà em đang khá lo lắng

<a id="S00086"></a>
**[00:07:05 → 00:07:06] [Người nói?]** Vẫn như em vẫn đang tìm hiểu

<a id="S00087"></a>
**[00:07:09 → 00:07:10] [Người nói?]** Còn lại là

<a id="S00088"></a>
**[00:07:10 → 00:07:12] [Người nói?]** Hai cái còn lại thì là đầu tiên là

<a id="S00089"></a>
**[00:07:12 → 00:07:15] [Người nói?]** Có phải là dữ liệu SQL không

<a id="S00090"></a>
**[00:07:16 → 00:07:17] [Người nói?]** Hoặc là có phải tấn công không

<a id="S00091"></a>
**[00:07:17 → 00:07:20] [Người nói?]** Thì nó trên 0.9

<a id="S00092"></a>
**[00:07:20 → 00:07:22] [Người nói?]** thì nó cũng có thể chấp nhận được

<a id="S00093"></a>
**[00:07:22 → 00:07:27] [Người nói?]** thế thôi thì?

<a id="S00094"></a>
**[00:07:28 → 00:07:29] [Người nói?]** còn một vấn đề nữa

<a id="S00095"></a>
**[00:07:31 → 00:07:32] [Người nói?]** đây ạ

<a id="S00096"></a>
**[00:07:32 → 00:07:34] [Người nói?]** thì là sau khi mà trend xong

<a id="S00097"></a>
**[00:07:34 → 00:07:36] [Người nói?]** thì là tất cả các M1 của em

<a id="S00098"></a>
**[00:07:36 → 00:07:39] [Người nói?]** [nghe không rõ 00:07:36; cần đối chiếu] đều ra là 0,99%

<a id="S00099"></a>
**[00:07:39 → 00:07:40] [Người nói?]** nghĩa là em đang sợ

<a id="S00100"></a>
**[00:07:40 → 00:07:42] [Người nói?]** là nó đang bị overfit và đang

<a id="S00101"></a>
**[00:07:42 → 00:07:44] [Người nói?]** không sinh ra sự khác biệt

<a id="S00102"></a>
**[00:07:44 → 00:07:46] [Người nói?]** nghĩa là kể cả em có dùng phương án cũ

<a id="S00103"></a>
**[00:07:46 → 00:07:48] [Người nói?]** hay là phương án gan

<a id="S00104"></a>
**[00:07:48 → 00:07:49] [Người nói?]** hay là gì nữa thì

<a id="S00105"></a>
**[00:07:49 → 00:07:55] [Người nói?]** hello, xin chào trưởng

<a id="S00106"></a>
**[00:09:10 → 00:09:21] [Người nói?]** [nghe không rõ 00:09:10; cần đối chiếu] Đây là các chỉ số Matrix thì là cả 4 cái kích bản thì nó không có sự khác biệt ạ và nó thường đạt trên chỉ 9% ạ.

<a id="S00107"></a>
**[00:09:21 → 00:09:24] [Người nói?]** Đây là một vấn đề mà em tìm phương án giải quyết.

<a id="S00108"></a>
**[00:09:25 → 00:09:39] [Người nói?]** [nghe không rõ 00:09:25; cần đối chiếu] Hiện tại là phương án giải quyết mà em đang tìm hiểu thì chỉ có là em sẽ sử dụng thay vì em sẽ sử dụng thêm cả cái top k neutral code để có thể tăng độ đa dạng

<a id="S00109"></a>
**[00:09:39 → 00:09:42] [Người nói?]** Thì em đang mong là nó có thể đem ra sự khác biệt

<a id="S00110"></a>
**[00:09:42 → 00:09:46] [Người nói?]** Thì đấy là toàn bộ phần báo cáo của em

## Góp ý: chốt bài toán và bộ phát hiện

<a id="S00111"></a>
**[00:09:46 → 00:09:49] [Người nói?]** Bây giờ như thế này nhé, em phải chuẩn bị lại cái slide này

<a id="S00112"></a>
**[00:09:51 → 00:09:56] [Người nói?]** Chuẩn bị lại cái slide này và làm rõ mình như thế này

<a id="S00113"></a>
**[00:09:56 → 00:09:59] [Người nói?]** Thứ nhất là cái bài toán, em giải quyết nó là gì, đúng

<a id="S00114"></a>
**[00:10:02 → 00:10:04] [Người nói?]** Bài toán em giải quyết là gì?

<a id="S00115"></a>
**[00:10:04 → 00:10:14] [Người nói?]** Bài toán của em là dùng GAN để phát hiện hay để sinh dữ liệu để hỗ trợ quá trình phát hiện SQL Injection

<a id="S00116"></a>
**[00:10:14 → 00:10:16] [Người nói?]** Đúng không?

<a id="S00117"></a>
**[00:10:17 → 00:10:26] [Người nói?]** Nếu mà mình xem ở đây thì mục tiêu của em đề ra là phân tích thực trạng của vấn đề của nó nhé

<a id="S00118"></a>
**[00:10:27 → 00:10:31] [Người nói?]** [nghe không rõ 00:10:27; cần đối chiếu] Hình cứu phân tích các kỹ thuật phát hiện vòng trống SQL Injection không cần nói nữa nhé

<a id="S00119"></a>
**[00:10:31 → 00:10:34] [Người nói?]** để xuất mô hình giải pháp tổng thể nâng cao hiệu quả phát hiện

<a id="S00120"></a>
**[00:10:38 → 00:10:46] [Người nói?]** Trong đó nhấn mạnh việc ứng dụng mô hình sinh dữ liệu để bổ sung dữ liệu tấn công.

<a id="S00121"></a>
**[00:10:46 → 00:10:51] [Người nói?]** Nhưng trọng tâm của em là vẫn phải có một mô hình phát hiện tấn công

<a id="S00122"></a>
**[00:10:57 → 00:11:03] [Người nói?]** Sau đó mình chỉ ra với dữ liệu nó như thế này

<a id="S00123"></a>
**[00:11:03 → 00:11:08] [Người nói?]** Đặc biệt là mất cân bằng thì người ta có thể dùng SMOTE, đúng không?

<a id="S00124"></a>
**[00:11:09 → 00:11:12] [Người nói?]** Nhưng thay vì SMOTE thì tôi dùng GAN đúng không?

<a id="S00125"></a>
**[00:11:13 → 00:11:15] [Người nói?]** Đấy cái logic của mình nó chỗ đấy đúng không?

<a id="S00126"></a>
**[00:11:16 → 00:11:22] [Người nói?]** Như vậy là em chạy được GAN nên em rất phải so sánh với SMOTE đúng không?

<a id="S00127"></a>
**[00:11:22 → 00:11:27] [Người nói?]** Em xin em hỏi, nghĩa là bây giờ em có cần kiểu đưa ra tỷ lệ

<a id="S00128"></a>
**[00:11:27 → 00:11:32] [Người nói?]** ví dụ như là 100 trên 1 hoặc là 80 trên 1 thì mới nên dùng GAN hoặc mới nên dùng SMOTE không ạ?

<a id="S00129"></a>
**[00:11:32 → 00:11:34] [Người nói?]** Đấy là kết quả về sau thôi.

<a id="S00130"></a>
**[00:11:35 → 00:11:40] [Người nói?]** [nghe không rõ 00:11:35; cần đối chiếu] Nếu mà mình ra thì cũng bị cắn tốt, còn nếu không thì trước mắt là làm sao để mình ra thì chúng ta phải sinh ra dữ liệu

<a id="S00131"></a>
**[00:11:41 → 00:11:44] [Người nói?]** [nghe không rõ 00:11:41; cần đối chiếu] Dùng smart hoặc dùng gai

<a id="S00132"></a>
**[00:11:46 → 00:11:53] [Người nói?]** Như vậy là em phải có các bộ phát hiện thì bộ phát hiện của em nó là gì?

<a id="S00133"></a>
**[00:11:53 → 00:12:04] [Người nói?]** Bộ phát hiện của em thì sẽ có 3 cái, đầu tiên là có 3 cái thư viện

<a id="S00134"></a>
**[00:12:04 → 00:12:07] [Người nói?]** [nghe không rõ 00:12:04; cần đối chiếu] SQL 3 là để check xem có phải SQL không

<a id="S00135"></a>
**[00:12:07 → 00:12:11] [Người nói?]** Một cái SQL Injection Library là để kiểm tra xem phải tấn công không

<a id="S00136"></a>
**[00:12:11 → 00:12:15] [Người nói?]** và cái cuối cùng là sẽ xem là có đa dạng hay không

<a id="S00137"></a>
**[00:12:15 → 00:12:19] [Người nói?]** [nghe không rõ 00:12:15; cần đối chiếu] Cái này là cái tool mình đang áp dụng trên đây để kiểm tra môi phục máy

<a id="S00138"></a>
**[00:12:20 → 00:12:25] [Người nói?]** [nghe không rõ 00:12:20; cần đối chiếu] Môi phục máy thì em mới chỉ đưa ra kịch bản bình thường

<a id="S00139"></a>
**[00:12:25 → 00:12:28] [Người nói?]** [nghe không rõ 00:12:25; cần đối chiếu] Dùng cái gì thường lý? Môi phục máy thì để kiểm tra hiện

<a id="S00140"></a>
**[00:12:30 → 00:12:31] [Người nói?]** Sẽ có đúng không?

<a id="S00141"></a>
**[00:12:31 → 00:12:32] [Người nói?]** Vâng

<a id="S00142"></a>
**[00:12:32 → 00:12:37] [Người nói?]** À không em có dùng cái cơ bản là cái quyết định

<a id="S00143"></a>
**[00:12:38 → 00:12:39] [Người nói?]** Cái baseline của em là gì?

<a id="S00144"></a>
**[00:12:40 → 00:12:45] [Người nói?]** Baseline của em là dùng 2 cái cơ bản là cây quyết định với cả là

<a id="S00145"></a>
**[00:12:45 → 00:12:50] [Người nói?]** cái gì nhỉ, tuyến tính, quên tên rồi

<a id="S00146"></a>
**[00:12:50 → 00:12:53] [Người nói?]** Đấy em liệt kê cho thầy, trong slide em liệt kê cho thầy là các bộ

<a id="S00147"></a>
**[00:12:53 → 00:12:56] [Người nói?]** [nghe không rõ 00:12:53; cần đối chiếu] phát hiện thấy nó là những bộ gì, theo thầy nên ý tuyển bao

<a id="S00148"></a>
**[00:12:56 → 00:13:00] [Người nói?]** [nghe không rõ 00:12:56; cần đối chiếu] có thể là cây quyết định hay gì là ý tuyển bao

<a id="S00149"></a>
**[00:13:00 → 00:13:01] [Người nói?]** Rồi

<a id="S00150"></a>
**[00:13:02 → 00:13:02] [Người nói?]** Đấy

<a id="S00151"></a>
**[00:13:03 → 00:13:07] [Người nói?]** Và với 3 bộ đấy mình chạy trên các phương pháp sinh dữ liệu

<a id="S00152"></a>
**[00:14:19 → 00:14:29] [Người nói?]** Trong đó mình trọng tâm sẽ vào gan đúng không?

<a id="S00153"></a>
**[00:14:30 → 00:14:36] [Người nói?]** Nhưng để nắm được là gan có tốt hay không thì phải so sánh với các phương pháp khác như là SMOTE

<a id="S00154"></a>
**[00:14:36 → 00:14:38] [Người nói?]** Đấy, cái logic của luận văn, em hiểu chưa em nhé?

<a id="S00155"></a>
**[00:14:38 → 00:14:39] [Người nói?]** Em hiểu

<a id="S00156"></a>
**[00:14:39 → 00:14:45] [Người nói?]** [nghe không rõ 00:14:39; cần đối chiếu] Đấy, đối với luật ban này sau khi em đã sửa tư đề thì nó cũng không nhất thiết là phải là thứ gì mới cả đúng không?

<a id="S00157"></a>
**[00:14:45 → 00:14:49] [Người nói?]** [nghe không rõ 00:14:45; cần đối chiếu] Đấy, nếu mà mình có mới thì mình sẽ đảm bảo, không thì mình sẽ làm nó bắt đúng chưa?

## Mô tả dữ liệu và giải thích lựa chọn mô hình

<a id="S00158"></a>
**[00:14:50 → 00:14:54] [Người nói?]** Đấy, thế còn là tiếp theo là bộ dữ liệu của em là gì?

<a id="S00159"></a>
**[00:14:54 → 00:15:10] [Người nói?]** Đấy, em muốn giảm rõ thầy, em bổ dữ liệu, em lấy ở đặc trưng nó là những cái gì, một cái bản ghi dữ liệu trong đấy, cấu trúc nó như thế nào, mình sẽ thực hành.

<a id="S00160"></a>
**[00:15:14 → 00:15:20] [Người nói?]** [nghe không rõ 00:15:14; cần đối chiếu] Giải thích cho thầy SMODE nó sẽ làm như thế nào, giải thích cho thầy GAN là gì, CT GAN là gì, CW GAN là gì?

<a id="S00161"></a>
**[00:15:21 → 00:15:26] [Người nói?]** Những cái đấy là mình giải thích kiểu bằng văn hay là phải có bài toán học được.

<a id="S00162"></a>
**[00:15:27 → 00:15:35] [Người nói?]** Khi giải thích VNM thì mình phải giải thích kiểu bằng văn nói hay là có văn toán nữa

<a id="S00163"></a>
**[00:15:35 → 00:15:41] [Người nói?]** Văn toán nhiều đâu, văn toán trong luận văn.

<a id="S00164"></a>
**[00:15:42 → 00:15:46] [Người nói?]** Còn slide để dẫn dắt vấn đề

<a id="S00165"></a>
**[00:15:48 → 00:15:57] [Người nói?]** [nghe không rõ 00:15:48; cần đối chiếu] Thì GAN, CT GAN, CTW GAN

<a id="S00166"></a>
**[00:15:57 → 00:15:59] [Người nói?]** 3 anh ấy có khác nhau cái gì

<a id="S00167"></a>
**[00:16:02 → 00:16:03] [Người nói?]** Thậm chí em có thể chạy cả 3 anh ấy

<a id="S00168"></a>
**[00:16:03 → 00:16:08] [Người nói?]** [nghe không rõ 00:16:03; cần đối chiếu] GAN truyền thống này, CT GAN này, CW GAN

<a id="S00169"></a>
**[00:16:09 → 00:16:11] [Người nói?]** [nghe không rõ 00:16:09; cần đối chiếu] Thì đưa thầy bảo tích tại sao mọi người tự lựa chọn CW GAN

<a id="S00170"></a>
**[00:16:11 → 00:16:13] [Người nói?]** Anh nghiên cứu nó phải thế không?

<a id="S00171"></a>
**[00:16:26 → 00:16:26] [Người nói?]** Vâng

<a id="S00172"></a>
**[00:16:26 → 00:16:27] [Người nói?]** Được chưa?

<a id="S00173"></a>
**[00:16:28 → 00:16:28] [Người nói?]** Vâng

## Hướng kiểm tra overfit và đối chiếu nghiên cứu trước

<a id="S00174"></a>
**[00:16:31 → 00:16:34] [Người nói?]** Như thầy hiện tại thì cái của em nó đang bị overfit

<a id="S00175"></a>
**[00:16:34 → 00:16:37] [Người nói?]** Thì em đang mong muốn là thầy cho em keyword hoặc là

<a id="S00176"></a>
**[00:16:39 → 00:16:44] [Người nói?]** Một cái keyword để em có thể tìm phương án giải quyết được không?

<a id="S00177"></a>
**[00:16:46 → 00:16:48] [Người nói?]** Overfit thì có thể có mấy lý do như thế này

<a id="S00178"></a>
**[00:16:48 → 00:16:56] [Người nói?]** [nghe không rõ 00:16:48; cần đối chiếu] Nhất là cái mô hình gan đấy có thể là nó lệch giữa Generator và Dissimilator

<a id="S00179"></a>
**[00:17:01 → 00:17:08] [Người nói?]** Critic là khả năng này yếu, đúng chưa?

<a id="S00180"></a>
**[00:17:08 → 00:17:10] [Người nói?]** Thứ hai là cái bộ dữ liệu, xem lại bộ dữ liệu

<a id="S00181"></a>
**[00:17:11 → 00:17:16] [Người nói?]** Nếu chẳng hạn nó lệch quá thì cũng có thể sinh gan cũng không dễ, đúng không?

<a id="S00182"></a>
**[00:17:17 → 00:17:21] [Người nói?]** Đấy, trước mắt mình cũng chọn bộ dữ liệu nó lệch đủ vừa thôi.

<a id="S00183"></a>
**[00:17:22 → 00:17:25] [Người nói?]** Đừng lệch quá mức, để xem nó xem như thế nào

<a id="S00184"></a>
**[00:17:26 → 00:17:32] [Người nói?]** [nghe không rõ 00:17:26; cần đối chiếu] Hiện tại em lấy hầu hết chỉ có lệch 1.1 hoặc 1.2 nên là em đang phải cố gắng cắt bớt xuống một tí ạ

<a id="S00185"></a>
**[00:17:34 → 00:17:40] [Người nói?]** [nghe không rõ 00:17:34; cần đối chiếu] Cắt xuống khoảng 1 trên 50 thì lúc đấy thì gan của em mới phát huy tác dụng nha là mới hợp được

<a id="S00186"></a>
**[00:17:40 → 00:17:46] [Người nói?]** Thế tiếp theo này, câu hỏi tiếp theo là đã có ai đã dùng gan này để sinh dữ liệu cho cái bài báo này thế chưa?

<a id="S00187"></a>
**[00:17:46 → 00:17:56] [Người nói?]** Có em có tham khảo cho nó ở đâu rồi đưa lên xin thông tin xem người ta làm cái gì đúng không?

<a id="S00188"></a>
**[00:17:56 → 00:17:59] [Người nói?]** Có 6 bài báo khoa học có làm giống em ạ

<a id="S00189"></a>
**[00:17:59 → 00:18:07] [Người nói?]** [nghe không rõ 00:17:59; cần đối chiếu] Nhưng mà họ không chia như em là kiểu họ không chia các dạng vật công mà họ chỉ bê nguyên H1N1 vào thôi ạ

<a id="S00190"></a>
**[00:18:08 → 00:18:11] [Người nói?]** Thì đấy là em đang coi như là điểm mới của em

<a id="S00191"></a>
**[00:18:11 → 00:18:14] [Người nói?]** Đầu tiên mình phải làm cái cơ bản này ạ

<a id="S00192"></a>
**[00:18:14 → 00:18:17] [Người nói?]** Đấy, cơ bản nó chạy ổn thì bắt đầu đi ra cái mới được.

<a id="S00193"></a>
**[00:18:17 → 00:18:19] [Người nói?]** [nghe không rõ 00:18:17; cần đối chiếu] Có lý lúc lộ tục theo cũng biết được một lần rồi

<a id="S00194"></a>
**[00:18:19 → 00:18:20] [Người nói?]** Được chưa?

<a id="S00195"></a>
**[00:18:20 → 00:18:21] [Người nói?]** Được

<a id="S00196"></a>
**[00:18:21 → 00:18:29] [Người nói?]** Đấy thế giới cũng thoải mái

<a id="S00197"></a>
**[00:18:31 → 00:18:34] [Người nói?]** [nghe không rõ 00:18:31; cần đối chiếu] Ngoài ra em cũng đang hơi lo. Kết quả nó không được nghĩ.

<a id="S00198"></a>
**[00:18:44 → 00:18:48] [Người nói?]** [nghe không rõ 00:18:44; cần đối chiếu] Nó phải rõ ràng như thế thôi. Thầy cho bàn nó biết được anh ạ.

<a id="S00199"></a>
**[00:18:48 → 00:18:48] [Người nói?]** Vâng ạ.

## Công thức đo, cấu trúc bản ghi và việc chuẩn bị lại slide

<a id="S00200"></a>
**[00:18:50 → 00:18:53] [Người nói?]** Cái diversity là em đổ đo một tí. Cách đo như thế nào?

<a id="S00201"></a>
**[00:18:55 → 00:19:02] [Người nói?]** [nghe không rõ 00:18:55; cần đối chiếu] Em đưa qua một cái thư viện. Em có một bài báo là ESBL.

<a id="S00202"></a>
**[00:19:02 → 00:19:04] [Người nói?]** Người ta có bảo người ta lấy thư viện.

<a id="S00203"></a>
**[00:19:05 → 00:19:10] [Người nói?]** Ba này thì cái ý tưởng với ba bộ quality filter là em lấy từ một bài báo.

<a id="S00204"></a>
**[00:19:10 → 00:19:12] [Người nói?]** Người ta có đăng thư viện cho em đưa về để em thử

<a id="S00205"></a>
**[00:19:12 → 00:19:16] [Người nói?]** Đấy, trong slide em mô tả thầy công thức kỹ tính

<a id="S00206"></a>
**[00:19:20 → 00:19:20] [Người nói?]** Vâng

<a id="S00207"></a>
**[00:19:21 → 00:19:22] [Người nói?]** [nghe không rõ 00:19:21; cần đối chiếu] Thì ta ghi bàn được

<a id="S00208"></a>
**[00:19:26 → 00:19:26] [Người nói?]** Rồi

<a id="S00209"></a>
**[00:19:27 → 00:19:29] [Người nói?]** Bây giờ người ta bảo muốn làm trời làm biển gì

<a id="S00210"></a>
**[00:19:29 → 00:19:35] [Người nói?]** [nghe không rõ 00:19:29; cần đối chiếu] Nhưng mà nếu mà có thích tóm lại dữ liệu anh định dạng làm gì mình trả lời thì xin

<a id="S00211"></a>
**[00:19:35 → 00:19:36] [Người nói?]** Đúng không

<a id="S00212"></a>
**[00:19:37 → 00:19:38] [Người nói?]** Em về trong slide mình nói rõ ràng

<a id="S00213"></a>
**[00:19:38 → 00:19:43] [Người nói?]** Đây thầy, em mô tả thầy xem là một bản ghi nó như thế này

<a id="S00214"></a>
**[00:19:43 → 00:19:43] [Người nói?]** Đúng không

<a id="S00215"></a>
**[00:19:44 → 00:19:45] [Người nói?]** Đấy, đúng chưa

<a id="S00216"></a>
**[00:19:45 → 00:19:48] [Người nói?]** Với sinh ra thì thường nó sẽ thay đổi cái gì nữa thế?

<a id="S00217"></a>
**[00:19:48 → 00:19:54] [Người nói?]** Hãy trình bày lại thầy nào

<a id="S00218"></a>
**[00:19:55 → 00:19:58] [Người nói?]** [nghe không rõ 00:19:55; cần đối chiếu] Chúng tôi mong muốn sớm ạ

<a id="S00219"></a>
**[00:19:58 → 00:19:59] [Người nói?]** Chiều thứ bảy ạ

<a id="S00220"></a>
**[00:19:59 → 00:20:00] [Người nói?]** Chiều

<a id="S00221"></a>
**[00:20:00 → 00:20:00] [Người nói?]** thứ bảy ạ

<a id="S00222"></a>
**[00:20:00 → 00:20:01] [Người nói?]** có kịp không?

<a id="S00223"></a>
**[00:20:01 → 00:20:02] [Người nói?]** hay là sang tuần sau?

<a id="S00224"></a>
**[00:20:02 → 00:20:06] [Người nói?]** chiều thứ bảy em chắc là không kịp

<a id="S00225"></a>
**[00:20:06 → 00:20:07] [Người nói?]** em mong là sang tuần sau

<a id="S00226"></a>
**[00:20:07 → 00:20:09] [Người nói?]** [nghe không rõ 00:20:07; cần đối chiếu] chắc là bằng lời tuần sau

<a id="S00227"></a>
**[00:20:09 → 00:20:10] [Người nói?]** thứ ba hoặc thứ năm được

<a id="S00228"></a>
**[00:20:10 → 00:20:11] [Người nói?]** [nghe không rõ 00:20:10; cần đối chiếu] ok, tuần tuần đi

<a id="S00229"></a>
**[00:20:11 → 00:20:12] [Người nói?]** anh cảm ơn ạ

<a id="S00230"></a>
**[00:20:13 → 00:20:14] [Người nói?]** đấy, tự mình cũng phải nắm vào thầy

<a id="S00231"></a>
**[00:20:14 → 00:20:15] [Người nói?]** thế thì nó ra cũng được

<a id="S00232"></a>
**[00:20:16 → 00:20:16] [Người nói?]** vâng

<a id="S00233"></a>
**[00:20:16 → 00:20:17] [Người nói?]** nhé

<a id="S00234"></a>
**[00:20:17 → 00:20:23] [Người nói?]** bây giờ bắt đầu vào giai đoạn làm rồi đấy

<a id="S00235"></a>
**[00:20:23 → 00:20:29] [Người nói?]** kinh nghiệm là

<a id="S00236"></a>
**[00:20:29 → 00:20:32] [Người nói?]** [nghe không rõ 00:20:29; cần đối chiếu] cũng làm dân làm được với đến tức cả

<a id="S00237"></a>
**[00:20:32 → 00:20:37] [Người nói?]** thì chắc là em cũng

<a id="S00238"></a>
**[00:20:38 → 00:20:40] [Người nói?]** thầy nói thế chắc em cũng phải cân nhắc

<a id="S00239"></a>
**[00:20:40 → 00:20:42] [Người nói?]** cũng phải đập đi một xíu cái

<a id="S00240"></a>
**[00:20:42 → 00:20:53] [Người nói?]** [nghe không rõ 00:20:42; cần đối chiếu] Bởi vì là em đang bị mong muốn thông số đẹp nên là có bà đâu cứ lên đọc vài báo nào thấy có su đu hướng có thể sửa em đập hết vào.

<a id="S00241"></a>
**[00:20:54 → 00:20:58] [Người nói?]** [nghe không rõ 00:20:54; cần đối chiếu] Tức là thầy cứ chạy ra rồi bắt đầu đi sang cái tivi.

<a id="S00242"></a>
**[00:21:00 → 00:21:03] [Người nói?]** Được chưa?

<a id="S00243"></a>
**[00:21:03 → 00:21:03] [Người nói?]** Vâng thầy ạ.

<a id="S00244"></a>
**[00:21:03 → 00:21:09] [Người nói?]** Ra đây nhé.

<a id="S00245"></a>
**[00:21:10 → 00:21:17] [Người nói?]** Ra đây thầy ạ.
