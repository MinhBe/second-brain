# Voice 017 — kiểm chứng cải tiến, trọng tâm cross-domain và trao đổi về đội ngũ

Nguồn: [Voice 017.m4a](file:///C:/Users/Admin/Documents/Collection/Data/Recording/Voice%20017.m4a)

Thời lượng: 02:03:44. ASR: large-v3 / cuda.

Trạng thái: đã rà văn bản; chờ nghe đối chiếu. Người nói chưa được xác định nếu không có ghi chú riêng.
Bản này bảo toàn thứ tự và nội dung nhận dạng; các đoạn nghi lỗi được giữ dấu vết để nghe lại.

## Tổng quan kiến trúc và phương pháp giải thích — nhiều đoạn chưa rõ

<a id="S00001"></a>
**[00:00:01 → 00:02:44] [Người nói?]** [nghe không rõ 00:00:01; cần đối chiếu] tìm một số hạn chế cho các kiến trúc mô hình, exception, FNF hay là các gì.

<a id="S00002"></a>
**[00:02:46 → 00:02:54] [Người nói?]** [nghe không rõ 00:02:46; cần đối chiếu] Sau đó em đi tập trung nghiên cứu một số các kiến trúc cơ bản của exception,

<a id="S00003"></a>
**[00:02:54 → 00:02:58] [Người nói?]** [nghe không rõ 00:02:54; cần đối chiếu] em cũng tìm hiểu vào từng phần.

<a id="S00004"></a>
**[00:02:58 → 00:03:03] [Người nói?]** [nghe không rõ 00:02:58; cần đối chiếu] Sau khi tìm hiểu kiến trúc exception cơ bản,

<a id="S00005"></a>
**[00:03:03 → 00:03:07] [Người nói?]** [nghe không rõ 00:03:03; cần đối chiếu] em có xem một số các exception đã được cải tiến trong các bài báo.

<a id="S00006"></a>
**[00:03:07 → 00:03:23] [Người nói?]** [nghe không rõ 00:03:07; cần đối chiếu] Ví dụ như là các cái cơ chế mà nó tiếp hợp với lại cơ chế hoặc là cái kinh nghiệm của SINF

<a id="S00007"></a>
**[00:03:23 → 00:03:31] [Người nói?]** [nghe không rõ 00:03:23; cần đối chiếu] Thì đấy là một số cái phát triển của các cơ chế cơ bản và có cái sự cải thiện trong một số các cái bài trước đó

<a id="S00008"></a>
**[00:03:31 → 00:03:40] [Người nói?]** [nghe không rõ 00:03:31; cần đối chiếu] Và cũng đấy cũng có cái hướng là từ đấy tạm thời là dự kiến ra một cái gọi là theo cái hướng này

<a id="S00009"></a>
**[00:03:48 → 00:04:17] [Người nói?]** [nghe không rõ 00:03:48; cần đối chiếu] Hãy subscribe cho kênh La La School Để không bỏ lỡ những video hấp dẫn

<a id="S00010"></a>
**[00:04:23 → 00:04:36] [Người nói?]** [nghe không rõ 00:04:23; cần đối chiếu] chủ yếu là em tạo tìm phần các kỹ thuật này hoạt động thực hiện như thế nào để đảm bảo những phần trong các kỹ thuật của nó.

<a id="S00011"></a>
**[00:04:37 → 00:04:48] [Người nói?]** [nghe không rõ 00:04:37; cần đối chiếu] Tiếp đến về phương pháp VGI thì tôi có thể kê các phương pháp VGI trong các bài đọc thách đi vào cách thức giảm cũng tương tự.

<a id="S00012"></a>
**[00:04:48 → 00:04:52] [Người nói?]** [nghe không rõ 00:04:48; cần đối chiếu] em tìm hiểu những phương pháp cơ bản

<a id="S00013"></a>
**[00:04:52 → 00:04:55] [Người nói?]** [nghe không rõ 00:04:52; cần đối chiếu] ví dụ như cam hay là đường sát

<a id="S00014"></a>
**[00:04:55 → 00:05:00] [Người nói?]** [nghe không rõ 00:04:55; cần đối chiếu] tìm hiểu những phương pháp cải tiến

<a id="S00015"></a>
**[00:05:00 → 00:05:02] [Người nói?]** [nghe không rõ 00:05:00; cần đối chiếu] tức là đã được cải tiến trong các phần báo tới

<a id="S00016"></a>
**[00:05:02 → 00:05:07] [Người nói?]** [nghe không rõ 00:05:02; cần đối chiếu] hoặc các phương pháp sát đã cải tiến trong một số phần báo mới đến đây

<a id="S00017"></a>
**[00:05:07 → 00:05:19] [Người nói?]** [nghe không rõ 00:05:07; cần đối chiếu] ví dụ như là cải tiến về các công thức phân hoạch

<a id="S00018"></a>
**[00:05:24 → 00:06:24] [Người nói?]** [nghe không rõ 00:05:24; cần đối chiếu] Hãy subscribe cho kênh Ghiền Mì Gõ Để không bỏ lỡ những video hấp dẫn

<a id="S00019"></a>
**[00:06:26 → 00:06:40] [Người nói?]** [nghe không rõ 00:06:26; cần đối chiếu] Ví dụ như là cải tiến trong phân cấp tổ chức cây để tính các nguyên minh để kiểm tra, để cải tiến cách kết hợp các nguyên minh của các đặc trưng,

<a id="S00020"></a>
**[00:06:41 → 00:06:54] [Người nói?]** [nghe không rõ 00:06:41; cần đối chiếu] rồi là cách cải tiến để lấy mẫu, cách để lấy mẫu để chúng ta tính, và tổ chức các vấn đề các kỹ mạng,

<a id="S00021"></a>
**[00:06:54 → 00:07:00] [Người nói?]** [nghe không rõ 00:06:54; cần đối chiếu] tức là các kiến thức mạng để hỗ trợ trong việc phát triển các tác.

<a id="S00022"></a>
**[00:07:01 → 00:07:07] [Người nói?]** [nghe không rõ 00:07:01; cần đối chiếu] Từ đấy mình cũng có dự kiến của phần này.

<a id="S00023"></a>
**[00:07:07 → 00:07:14] [Người nói?]** [nghe không rõ 00:07:07; cần đối chiếu] Tuy nhiên ở đây trong vừa rồi em tập trung em mới đang dự kiến ra

<a id="S00024"></a>
**[00:07:15 → 00:07:18] [Người nói?]** [nghe không rõ 00:07:15; cần đối chiếu] lúc tranh tổng thể của 2 loại dung này.

<a id="S00025"></a>
**[00:07:20 → 00:07:25] [Người nói?]** [nghe không rõ 00:07:20; cần đối chiếu] Về phần thứ 3 thì nó khó hơn người ta nghe,

<a id="S00026"></a>
**[00:07:25 → 00:07:27] [Người nói?]** [nghe không rõ 00:07:25; cần đối chiếu] em cũng chưa kỹ hơn cái phần này

<a id="S00027"></a>
**[00:07:27 → 00:07:29] [Người nói?]** [nghe không rõ 00:07:27; cần đối chiếu] tập trung hướng tới của em

<a id="S00028"></a>
**[00:07:29 → 00:07:30] [Người nói?]** [nghe không rõ 00:07:29; cần đối chiếu] thì em đi vào cái

<a id="S00029"></a>
**[00:07:31 → 00:07:32] [Người nói?]** [nghe không rõ 00:07:31; cần đối chiếu] đi vào cái phần chủ yếu

<a id="S00030"></a>
**[00:07:32 → 00:07:34] [Người nói?]** [nghe không rõ 00:07:32; cần đối chiếu] đi vào 2 cái phần đầu

<a id="S00031"></a>
**[00:07:34 → 00:07:37] [Người nói?]** [nghe không rõ 00:07:34; cần đối chiếu] phần thứ nhất là cái phần về sẽ tập trung vào cái phần

<a id="S00032"></a>
**[00:07:37 → 00:07:40] [Người nói?]** [nghe không rõ 00:07:37; cần đối chiếu] giả sát các cái kiến trúc này

<a id="S00033"></a>
**[00:07:40 → 00:07:42] [Người nói?]** [nghe không rõ 00:07:40; cần đối chiếu] và cách thức thì cũng là

<a id="S00034"></a>
**[00:07:42 → 00:07:44] [Người nói?]** [nghe không rõ 00:07:42; cần đối chiếu] đi từ các kiến trúc căn bạc

<a id="S00035"></a>
**[00:07:44 → 00:07:46] [Người nói?]** [nghe không rõ 00:07:44; cần đối chiếu] xong rồi là sẽ có một cái

<a id="S00036"></a>
**[00:07:46 → 00:07:48] [Người nói?]** [nghe không rõ 00:07:46; cần đối chiếu] kẻ kiến của các kiến trúc đấy

<a id="S00037"></a>
**[00:07:48 → 00:07:51] [Người nói?]** [nghe không rõ 00:07:48; cần đối chiếu] thì xác định rõ các kẻ kiến này

<a id="S00038"></a>
**[00:07:51 → 00:07:53] [Người nói?]** [nghe không rõ 00:07:51; cần đối chiếu] nó sẽ có các đặc trưng của

<a id="S00039"></a>
**[00:07:53 → 00:07:55] [Người nói?]** [nghe không rõ 00:07:53; cần đối chiếu] các kẻ kiến này và có các cái

<a id="S00040"></a>
**[00:07:58 → 00:08:02] [Người nói?]** [nghe không rõ 00:07:58; cần đối chiếu] tìm hiểu và giải thích được tất cả chi tiết về cái cải tiến này.

<a id="S00041"></a>
**[00:08:02 → 00:08:08] [Người nói?]** [nghe không rõ 00:08:02; cần đối chiếu] Từ đấy thì em sẽ xem, kiểm tra một số dự kiến

<a id="S00042"></a>
**[00:08:08 → 00:08:16] [Người nói?]** [nghe không rõ 00:08:08; cần đối chiếu] để có thể hỗ trợ ra một dự báo về một kế hoạch mới.

<a id="S00043"></a>
**[00:08:22 → 00:08:26] [Người nói?]** [nghe không rõ 00:08:22; cần đối chiếu] Thứ hai là tập trung vào phần phương pháp nghiên cứu

<a id="S00044"></a>
**[00:08:26 → 00:08:43] [Người nói?]** [nghe không rõ 00:08:26; cần đối chiếu] Trong đó, trong các phương pháp kế hoạch, mình sẽ chủ yếu là nghiên cứu về phương pháp về sát, cũng đã có các nội dung về sát cơ bản và biến đổi, và cũng đã có một số những cải tiến tổ hợp với các cải tiến của sát.

<a id="S00045"></a>
**[00:08:43 → 00:09:00] [Người nói?]** [nghe không rõ 00:08:43; cần đối chiếu] thì em sẽ cố gắng tập trung vào đánh giá những kẻ tiến này rất cụ thể để có một cái bài tổng thể chi tiết trong phương pháp sắp này.

<a id="S00046"></a>
**[00:09:01 → 00:09:09] [Người nói?]** [nghe không rõ 00:09:01; cần đối chiếu] Vướng của em tập trung vào hai cái kẻ tiến này để tập trung vào hai cái hướng.

<a id="S00047"></a>
**[00:09:20 → 00:09:28] [Người nói?]** [nghe không rõ 00:09:20; cần đối chiếu] Hãy subscribe cho kênh Ghiền Mì Gõ Để không bỏ lỡ những video hấp dẫn

<a id="S00048"></a>
**[00:09:46 → 00:09:53] [Người nói?]** [nghe không rõ 00:09:46; cần đối chiếu] Bởi vì sự phát triển của các kiến trúc này nó không chỉ có một cái kiến trúc này khác mà có thể chúng ta có thêm nhiều hơn.

<a id="S00049"></a>
**[00:09:53 → 00:09:59] [Người nói?]** [nghe không rõ 00:09:53; cần đối chiếu] Thì em sẽ phục vụ phần đấy và sẽ chỉ ra, cố gắng chỉ ra được cái trực tạp của các kiến trúc này.

<a id="S00050"></a>
**[00:10:13 → 00:10:34] [Người nói?]** [nghe không rõ 00:10:13; cần đối chiếu] Các bạn hãy đăng ký kênh để ủng hộ kênh của mình nhé.

<a id="S00051"></a>
**[00:10:43 → 00:10:53] [Người nói?]** [nghe không rõ 00:10:43; cần đối chiếu] Cơ bản có phần cải tiến, cách trúc cải tiến, các bước cải tiến chi tiết, những ưu hỏng và những vấn đề đó.

<a id="S00052"></a>
**[00:10:53 → 00:11:02] [Người nói?]** [nghe không rõ 00:10:53; cần đối chiếu] Chúng em sẽ làm báo cáo trước để thử thấy trong cơ bản dự kiến chúng ta có tài liệu trong tuần sau để phổ trung những vấn đề này.

<a id="S00053"></a>
**[00:11:02 → 00:11:08] [Người nói?]** [nghe không rõ 00:11:02; cần đối chiếu] thì cũng đã có phần này nhưng mà em chưa kịp hiểu lắm

<a id="S00054"></a>
**[00:11:08 → 00:11:14] [Người nói?]** [nghe không rõ 00:11:08; cần đối chiếu] nên là em không thể giải thích cái phần hỗn hợp đấy

<a id="S00055"></a>
**[00:11:14 → 00:11:19] [Người nói?]** [nghe không rõ 00:11:14; cần đối chiếu] chưa hiểu hết kỹ vì một số cái khái niệm của em cũng không hiểu

<a id="S00056"></a>
**[00:11:20 → 00:11:22] [Người nói?]** [nghe không rõ 00:11:20; cần đối chiếu] Vậy bộ dữ liệu mẫu như thế này?

<a id="S00057"></a>
**[00:11:23 → 00:11:25] [Người nói?]** [nghe không rõ 00:11:23; cần đối chiếu] Dạ, về bộ dữ liệu mẫu như thế này

<a id="S00058"></a>
**[00:11:38 → 00:11:40] [Người nói?]** [nghe không rõ 00:11:38; cần đối chiếu] về so sánh các cái bộ dữ liệu khác

<a id="S00059"></a>
**[00:11:40 → 00:11:43] [Người nói?]** [nghe không rõ 00:11:40; cần đối chiếu] thì em cũng tìm được cái bộ dữ liệu này

<a id="S00060"></a>
**[00:11:43 → 00:11:48] [Người nói?]** [nghe không rõ 00:11:43; cần đối chiếu] hiện nay thì em cũng có cái tải những cái bộ dữ liệu

<a id="S00061"></a>
**[00:12:03 → 00:12:32] [Người nói?]** [nghe không rõ 00:12:03; cần đối chiếu] Các bạn có thể nhớ đăng kí cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

<a id="S00062"></a>
**[00:12:33 → 00:12:46] [Người nói?]** [nghe không rõ 00:12:33; cần đối chiếu] để giải thích thì cũng mới đang dừng mức độ là giải thích ra nhưng mà chưa được thử minh thông qua các kiến thức chứng để minh hoạt các cái phần gì đấy

<a id="S00063"></a>
**[00:12:47 → 00:13:03] [Người nói?]** [nghe không rõ 00:12:47; cần đối chiếu] thì chúng em xin lấy ra cái phần dữ liệu 2 cái đặc biệt là 2 cái phần file của bộ dữ liệu này thì sẽ bổ sung cái phần cụ thể để cái

<a id="S00064"></a>
**[00:13:11 → 00:13:21] [Người nói?]** [nghe không rõ 00:13:11; cần đối chiếu] Ok, 81 là có ghế hội thảo AI nhé. Nếu kịp thì gửi hội thảo ở nơi hợp lý nhất đấy.

<a id="S00065"></a>
**[00:13:22 → 00:13:26] [Người nói?]** [nghe không rõ 00:13:22; cần đối chiếu] Vậy thì chính xác là sang phần thứ 3 thì em sẽ cố gắng gửi.

<a id="S00066"></a>
**[00:13:26 → 00:13:35] [Người nói?]** [nghe không rõ 00:13:26; cần đối chiếu] Nghĩa là cái đích tới là một là em sẽ bổ sung thêm cái phần đặc biệt một số kiến trúc.

<a id="S00067"></a>
**[00:13:36 → 00:13:37] [Người nói?]** [nghe không rõ 00:13:36; cần đối chiếu] Cái kiến trúc đấy cũng phải đối hợp.

<a id="S00068"></a>
**[00:13:37 → 00:13:42] [Người nói?]** [nghe không rõ 00:13:37; cần đối chiếu] Hai nữa là em sẽ đẩy tất cả thành phần ở trong kiến trúc được được kê.

<a id="S00069"></a>
**[00:13:44 → 00:13:55] [Người nói?]** [nghe không rõ 00:13:44; cần đối chiếu] Về phương pháp thì cũng là phương pháp sạc thì có phương pháp thân bản thì em hiểu rồi

<a id="S00070"></a>
**[00:13:55 → 00:14:01] [Người nói?]** [nghe không rõ 00:13:55; cần đối chiếu] Nhưng phương pháp cải tiến, phương cách cải tiến đây thì em sẽ có hiệu của báo cáo này

<a id="S00071"></a>
**[00:14:02 → 00:14:11] [Người nói?]** [nghe không rõ 00:14:02; cần đối chiếu] Vừa rồi thầy chỉ cho cái chỗ về bộ dữ liệu thì em sẽ làm rõ so sánh bộ dữ liệu đấy có hình chữ có thể

<a id="S00072"></a>
**[00:14:11 → 00:14:15] [Người nói?]** [nghe không rõ 00:14:11; cần đối chiếu] Rồi cảm ơn em

<a id="S00073"></a>
**[00:14:15 → 00:15:00] [Người nói?]** [nghe không rõ 00:14:15; cần đối chiếu] Nó có, bây giờ hết rồi em

<a id="S00074"></a>
**[00:15:00 → 00:15:01] [Người nói?]** [nghe không rõ 00:15:00; cần đối chiếu] Ai báo cáo thế này?

<a id="S00075"></a>
**[00:15:01 → 00:15:07] [Người nói?]** [nghe không rõ 00:15:01; cần đối chiếu] Mới năm ngoái còn. Năm ngoái xài rồi đó anh. Mắc hết cái còn này rồi.

<a id="S00076"></a>
**[00:15:08 → 00:15:13] [Người nói?]** [nghe không rõ 00:15:08; cần đối chiếu] Bây giờ thì hết rồi. Giờ phải trả phí rồi.

<a id="S00077"></a>
**[00:15:18 → 00:15:24] [Người nói?]** [nghe không rõ 00:15:18; cần đối chiếu] Hả? Bây giờ làm gì bộ tiền viên nữa?

<a id="S00078"></a>
**[00:15:24 → 00:15:26] [Người nói?]** [nghe không rõ 00:15:24; cần đối chiếu] Bây giờ hết rồi. Process nó hết rồi.

<a id="S00079"></a>
**[00:15:26 → 00:15:27] [Người nói?]** [nghe không rõ 00:15:26; cần đối chiếu] Còn à?

<a id="S00080"></a>
**[00:15:27 → 00:15:28] [Người nói?]** [nghe không rõ 00:15:27; cần đối chiếu] Ừ.

<a id="S00081"></a>
**[00:15:29 → 00:15:29] [Người nói?]** [nghe không rõ 00:15:29; cần đối chiếu] Không còn nữa.

<a id="S00082"></a>
**[00:15:30 → 00:15:32] [Người nói?]** [nghe không rõ 00:15:30; cần đối chiếu] Hết rồi. Từ năm ngoái là nó xài cái đấy rồi.

<a id="S00083"></a>
**[00:15:34 → 00:15:36] [Người nói?]** [nghe không rõ 00:15:34; cần đối chiếu] Nó bắt kết cái dự án hồi xưa làm cái invoice.

<a id="S00084"></a>
**[00:15:37 → 00:15:39] [Người nói?]** [nghe không rõ 00:15:37; cần đối chiếu] Chatbot invoice nè. Tự động đọc hóa đơn.

<a id="S00085"></a>
**[00:15:40 → 00:15:42] [Người nói?]** [nghe không rõ 00:15:40; cần đối chiếu] Từ đó là đã phải mua thêm rồi. Thì thì hết.

<a id="S00086"></a>
**[00:15:44 → 00:15:49] [Người nói?]** [nghe không rõ 00:15:44; cần đối chiếu] Từ đầu năm nay á. Cái process này hết rồi.

## Báo cáo attention và hợp nhất mô hình

<a id="S00087"></a>
**[00:15:49 → 00:16:28] [Người nói?]** [nghe không rõ 00:15:49; cần đối chiếu] Mình có trách Shell Attention khi mà đưa thương vào trong mô hình STDN gốc hoạt động.

<a id="S00088"></a>
**[00:16:28 → 00:16:34] [Người nói?]** [nghe không rõ 00:16:28; cần đối chiếu] Em có trách thêm bác hoạt toán về Fusion này.

<a id="S00089"></a>
**[00:16:34 → 00:16:37] [Người nói?]** [nghe không rõ 00:16:34; cần đối chiếu] Có trách thêm Adversion và cũng đã có kết quả.

<a id="S00090"></a>
**[00:16:37 → 00:16:45] [Người nói?]** [nghe không rõ 00:16:37; cần đối chiếu] Rồi em sẽ khai quát lại các quan hệ đặc biệt từ STDN.

<a id="S00091"></a>
**[00:16:47 → 00:16:50] [Người nói?]** [nghe không rõ 00:16:47; cần đối chiếu] Tiến trình và rút góp, số dữ phép tính từ 10 tháng.

<a id="S00092"></a>
**[00:16:50 → 00:16:54] [Người nói?]** [nghe không rõ 00:16:50; cần đối chiếu] Rồi xả lốt xuống phần công việc thứ 2, chính là kết quả ESDN đó.

<a id="S00093"></a>
**[00:16:54 → 00:16:57] [Người nói?]** [nghe không rõ 00:16:54; cần đối chiếu] Và qua bài SIS, tức là SIS,

<a id="S00094"></a>
**[00:16:59 → 00:17:05] [Người nói?]** [nghe không rõ 00:16:59; cần đối chiếu] Từ SPDN em đã thay 1 phần CNN thành 1 phần SHELL ATTENTION

<a id="S00095"></a>
**[00:17:05 → 00:17:09] [Người nói?]** [nghe không rõ 00:17:05; cần đối chiếu] Số tham số đi thêm không nhiều, chỉ khoảng 169

<a id="S00096"></a>
**[00:17:09 → 00:17:15] [Người nói?]** [nghe không rõ 00:17:09; cần đối chiếu] Đây là phần kiến trúc

<a id="S00097"></a>
**[00:17:15 → 00:17:23] [Người nói?]** [nghe không rõ 00:17:15; cần đối chiếu] Phần giá dấu vết sản phẩm cũng đã kỳ nguyên từ bài SPDN

<a id="S00098"></a>
**[00:17:23 → 00:17:28] [Người nói?]** [nghe không rõ 00:17:23; cần đối chiếu] Phần này em có đi qua về chỗ này em đã thay SHELL ATTENTION

<a id="S00099"></a>
**[00:17:28 → 00:17:33] [Người nói?]** [nghe không rõ 00:17:28; cần đối chiếu] Tức là block SHELL ATTENTION ở trong này em đã thay cảnh nhánh ESR

<a id="S00100"></a>
**[00:17:33 → 00:17:37] [Người nói?]** [nghe không rõ 00:17:33; cần đối chiếu] và cảnh nhánh tổng hợp các đặc trưng dấu vết TLCSRB

<a id="S00101"></a>
**[00:17:38 → 00:17:44] [Người nói?]** [nghe không rõ 00:17:38; cần đối chiếu] Đối với SRB thì cái kích thước ma trận mà nó nhọc thì em để kích thước của cái block SA là kích thước block vàng

<a id="S00102"></a>
**[00:17:44 → 00:17:52] [Người nói?]** [nghe không rõ 00:17:44; cần đối chiếu] và tự đúng với ma trận dấu vết C là kích thước nằm và ma trận dấu vết T thì là kích thước phối SA này

<a id="S00103"></a>
**[00:17:52 → 00:17:57] [Người nói?]** [nghe không rõ 00:17:52; cần đối chiếu] thì đây là cái tầm thái quát qua của cái mô hình mà em đã thể hiện

<a id="S00104"></a>
**[00:17:57 → 00:18:07] [Người nói?]** [nghe không rõ 00:17:57; cần đối chiếu] Trong Shell Attention này thì em có tham khảo từ bài SCCB từ 2018

<a id="S00105"></a>
**[00:18:07 → 00:18:14] [Người nói?]** [nghe không rõ 00:18:07; cần đối chiếu] Đối với cái cơ chế chú ý, trước thì cơ chế chú ý trong mô hình SD chưa có

<a id="S00106"></a>
**[00:18:14 → 00:18:20] [Người nói?]** [nghe không rõ 00:18:14; cần đối chiếu] Trong cái nhánh tổng hợp các đặc trưng, các dấu phích, em có đưa thêm cơ chế chú ý là nhấn thêm một màn chặn I.

<a id="S00107"></a>
**[00:18:20 → 00:18:27] [Người nói?]** [nghe không rõ 00:18:20; cần đối chiếu] Số lượng tham số thì tăng lên 969 tham số khi mà em tìm cái Shared Tension.

<a id="S00108"></a>
**[00:18:28 → 00:18:36] [Người nói?]** [nghe không rõ 00:18:28; cần đối chiếu] Về phần hàm vấn mắc thì vẫn như thế nhưng mà tuy nhiên em vẫn điều chỉnh cái trọng số trong cái hàm vấn mắc.

<a id="S00109"></a>
**[00:18:36 → 00:18:40] [Người nói?]** [nghe không rõ 00:18:36; cần đối chiếu] Đây là cái khối Edge, tức là cái khối cho những phân loại.

<a id="S00110"></a>
**[00:18:41 → 00:18:43] [Người nói?]** [nghe không rõ 00:18:41; cần đối chiếu] Ở đây thì em đã nâng lên thành 50.

<a id="S00111"></a>
**[00:18:44 → 00:18:48] [Người nói?]** [nghe không rõ 00:18:44; cần đối chiếu] Nó có nguyên do tại vì cái khối stress tension thì nó nặng về cái phần con huyết

<a id="S00112"></a>
**[00:18:48 → 00:18:53] [Người nói?]** [nghe không rõ 00:18:48; cần đối chiếu] Và trong khi đấy thì cái mạng của em thì kết quả nó cũng cao đất tệ

<a id="S00113"></a>
**[00:18:53 → 00:18:57] [Người nói?]** [nghe không rõ 00:18:53; cần đối chiếu] Khi mà giảm cái tỉ lệch MSR đến tốt bắt đầu của SEM

<a id="S00114"></a>
**[00:18:57 → 00:19:00] [Người nói?]** [nghe không rõ 00:18:57; cần đối chiếu] Nó tăng nó lên từ 50 để cho nó tươi tươi thành lý

<a id="S00115"></a>
**[00:19:00 → 00:19:07] [Người nói?]** [nghe không rõ 00:19:00; cần đối chiếu] Em đã đi qua được cái mô hình SASR mà em đã cải thiết lên

<a id="S00116"></a>
**[00:19:09 → 00:19:11] [Người nói?]** [nghe không rõ 00:19:09; cần đối chiếu] Bây giờ đến phần cái thỏa toán thấp nhất các mô hình

<a id="S00117"></a>
**[00:19:13 → 00:19:16] [Người nói?]** [nghe không rõ 00:19:13; cần đối chiếu] Thực ra thấp nhất các mô hình thì có ra nhiều phương pháp

<a id="S00118"></a>
**[00:19:16 → 00:19:24] [Người nói?]** [nghe không rõ 00:19:16; cần đối chiếu] phương pháp lấy trung bình các kết quả, phương pháp lấy trung bình, hoặc phương pháp giải trí, tức là lai lai của 2 phương pháp ở trên

<a id="S00119"></a>
**[00:19:24 → 00:19:32] [Người nói?]** [nghe không rõ 00:19:24; cần đối chiếu] hoặc sử dụng một cây quyết định, cây trăng cường trong giảm quyết định giữa các mô hình nhau

<a id="S00120"></a>
**[00:19:32 → 00:19:38] [Người nói?]** [nghe không rõ 00:19:32; cần đối chiếu] thì đầu tiên sẽ phải chuẩn hóa đầu xác của tất cả các mô hình để dẫn dàng từ 0 đến 1

<a id="S00121"></a>
**[00:19:39 → 00:19:42] [Người nói?]** [nghe không rõ 00:19:39; cần đối chiếu] Những câu thức này là câu thức chuẩn hóa dặn tiêu chuẩn

<a id="S00122"></a>
**[00:19:42 → 00:19:49] [Người nói?]** [nghe không rõ 00:19:42; cần đối chiếu] Sau đấy thì em sẽ có tập toán, chọn cái tổ tập tốt nhất

<a id="S00123"></a>
**[00:19:49 → 00:19:51] [Người nói?]** [nghe không rõ 00:19:49; cần đối chiếu] Tức là em sẽ có khá là nhiều mô hình

<a id="S00124"></a>
**[00:19:51 → 00:19:54] [Người nói?]** [nghe không rõ 00:19:51; cần đối chiếu] Nhưng mà mình thấy sẽ có cả mô hình Vision Transformer

<a id="S00125"></a>
**[00:19:54 → 00:19:56] [Người nói?]** [nghe không rõ 00:19:54; cần đối chiếu] Vision Transformer

<a id="S00126"></a>
**[00:19:56 → 00:19:57] [Người nói?]** [nghe không rõ 00:19:56; cần đối chiếu] Đúng

<a id="S00127"></a>
**[00:19:57 → 00:19:59] [Người nói?]** [nghe không rõ 00:19:57; cần đối chiếu] Cái kiểu socon hay là fix này thì là cái

<a id="S00128"></a>
**[00:20:00 → 00:20:01] [Người nói?]** [nghe không rõ 00:20:00; cần đối chiếu] mô hình em cải thiện của em

<a id="S00129"></a>
**[00:20:03 → 00:20:06] [Người nói?]** [nghe không rõ 00:20:03; cần đối chiếu] Mô hình LDA thì cũng là một cái sô tang ở đây

<a id="S00130"></a>
**[00:20:07 → 00:20:09] [Người nói?]** [nghe không rõ 00:20:07; cần đối chiếu] và cái mô hình No-ADV

<a id="S00131"></a>
**[00:20:09 → 00:20:14] [Người nói?]** [nghe không rõ 00:20:09; cần đối chiếu] tức là mô hình STDN của em, nhưng mà em tắt cái nhánh phân biệt

<a id="S00132"></a>
**[00:20:14 → 00:20:20] [Người nói?]** [nghe không rõ 00:20:14; cần đối chiếu] rủi kháng trong gạm đi. Bằng cái thuật toán trong Tham Lan thì em giữ được lại một cái

<a id="S00133"></a>
**[00:20:20 → 00:20:24] [Người nói?]** [nghe không rõ 00:20:20; cần đối chiếu] tổ lọc mô hình, một bốn mô hình và nó cho cái lỗi là thật nhất

<a id="S00134"></a>
**[00:20:24 → 00:20:30] [Người nói?]** [nghe không rõ 00:20:24; cần đối chiếu] Ở đây là một số các thuật toán mà em đã trải thưởng nghiệm

<a id="S00135"></a>
**[00:20:30 → 00:20:36] [Người nói?]** [nghe không rõ 00:20:30; cần đối chiếu] Trong này em có phân ra thuật toán nào sử dụng nhãn để học trong việc hợp thích mô hình

<a id="S00136"></a>
**[00:20:36 → 00:20:42] [Người nói?]** [nghe không rõ 00:20:36; cần đối chiếu] và thuật toán nào sử dụng để đưa vào trong phương pháp hợp thích mô hình.

<a id="S00137"></a>
**[00:20:42 → 00:20:45] [Người nói?]** [nghe không rõ 00:20:42; cần đối chiếu] Thì ở đây thì thuật toán trung bình hạn, thuật toán cơ bản nhất

<a id="S00138"></a>
**[00:20:45 → 00:20:50] [Người nói?]** [nghe không rõ 00:20:45; cần đối chiếu] thì nó cho kết quả tốt nhất là 0,76 trên mũ text để đổi.

<a id="S00139"></a>
**[00:20:50 → 00:20:55] [Người nói?]** Một số phương pháp khác nâng cao hơn nhưng mà là cho kết quả tệ hơn.

<a id="S00140"></a>
**[00:20:55 → 00:21:01] [Người nói?]** [nghe không rõ 00:20:55; cần đối chiếu] Em có huấn luyện các mô hình kém remote ở đây, đánh xét các mô hình.

<a id="S00141"></a>
**[00:21:01 → 00:21:05] [Người nói?]** [nghe không rõ 00:21:01; cần đối chiếu] Thì phần lớn các mô hình đều tấn luyện với tỉ lệ lỗi trên 1

<a id="S00142"></a>
**[00:21:05 → 00:21:08] [Người nói?]** [nghe không rõ 00:21:05; cần đối chiếu] Nhưng mà tuy nhiên bằng phương pháp 1 trung bình 2

<a id="S00143"></a>
**[00:21:10 → 00:21:13] [Người nói?]** [nghe không rõ 00:21:10; cần đối chiếu] Thì kết quả tỉ lệ lỗi của nó đã xuống được dưới 0,76

<a id="S00144"></a>
**[00:21:14 → 00:21:16] [Người nói?]** [nghe không rõ 00:21:14; cần đối chiếu] Em cũng thường thêm bớt một số mô hình

<a id="S00145"></a>
**[00:21:16 → 00:21:19] [Người nói?]** [nghe không rõ 00:21:16; cần đối chiếu] Trong đấy đặc biệt đưa ra mô hình kiến trúc tế xuất

<a id="S00146"></a>
**[00:21:19 → 00:21:21] [Người nói?]** [nghe không rõ 00:21:19; cần đối chiếu] S-A-X

<a id="S00147"></a>
**[00:21:21 → 00:21:22] [Người nói?]** [nghe không rõ 00:21:21; cần đối chiếu] Nếu như bỏ nó đi

<a id="S00148"></a>
**[00:21:23 → 00:21:27] [Người nói?]** [nghe không rõ 00:21:23; cần đối chiếu] Thì tỉ lệ lỗi nó tăng lên không bằng mô hình số tài

<a id="S00149"></a>
**[00:21:27 → 00:21:29] [Người nói?]** [nghe không rõ 00:21:27; cần đối chiếu] Nó đóng một vai trò rất là trắng tròn

<a id="S00150"></a>
**[00:21:29 → 00:21:31] [Người nói?]** [nghe không rõ 00:21:29; cần đối chiếu] Một số mô hình khác bỏ đi thì nó cũng không thay đổi nhiều

<a id="S00151"></a>
**[00:21:31 → 00:21:33] [Người nói?]** [nghe không rõ 00:21:31; cần đối chiếu] Tăng đến 0% hoặc là 0,5%

<a id="S00152"></a>
**[00:21:33 → 00:21:35] [Người nói?]** [nghe không rõ 00:21:33; cần đối chiếu] Nó cũng đang kể bằng cho mô hình SKS rồi.

<a id="S00153"></a>
**[00:21:39 → 00:21:44] [Người nói?]** [nghe không rõ 00:21:39; cần đối chiếu] Đây là cái bảng mà em so sánh với các số tài trên 4CNR Scoop lần này.

<a id="S00154"></a>
**[00:21:46 → 00:21:49] [Người nói?]** [nghe không rõ 00:21:46; cần đối chiếu] Mô hình mà nó có kết quả tốt nhất bây giờ là mô hình DPM.

<a id="S00155"></a>
**[00:21:49 → 00:21:52] [Người nói?]** [nghe không rõ 00:21:49; cần đối chiếu] Mô hình LDA thì họ mới đăng vào trên Tokai.

<a id="S00156"></a>
**[00:21:52 → 00:21:53] [Người nói?]** [nghe không rõ 00:21:52; cần đối chiếu] Chứ họ chưa có công bố được.

<a id="S00157"></a>
**[00:21:53 → 00:21:54] [Người nói?]** [nghe không rõ 00:21:53; cần đối chiếu] Nhưng mà tuy nhiên vẫn đưa vào report.

<a id="S00158"></a>
**[00:21:55 → 00:21:58] [Người nói?]** [nghe không rõ 00:21:55; cần đối chiếu] Khi mà so sánh trên thì lấy lỗi AUC hay là lấy phaser.

<a id="S00159"></a>
**[00:22:00 → 00:22:03] [Người nói?]** [nghe không rõ 00:22:00; cần đối chiếu] Mô hình của em tốt nhất trong tất cả các chỉ số.

<a id="S00160"></a>
**[00:22:05 → 00:22:12] [Người nói?]** [nghe không rõ 00:22:05; cần đối chiếu] Bên đây em kết luận, với cơ bản phương pháp của em đề xuất thì thẳng trên các số tài trong phần số này

<a id="S00161"></a>
**[00:22:12 → 00:22:15] [Người nói?]** [nghe không rõ 00:22:12; cần đối chiếu] và còn đóng góp thêm về S, A, S, R

<a id="S00162"></a>
**[00:22:17 → 00:22:19] [Người nói?]** [nghe không rõ 00:22:17; cần đối chiếu] Về mặt giới hạn thì nó cũng rất rõ ràng

<a id="S00163"></a>
**[00:22:19 → 00:22:25] [Người nói?]** [nghe không rõ 00:22:19; cần đối chiếu] Cái phép gồm này thì nó cũng giống như là chỉ bắt nốt cái quả mặt của các mô hình

<a id="S00164"></a>
**[00:22:25 → 00:22:27] [Người nói?]** [nghe không rõ 00:22:25; cần đối chiếu] muốn cải thiện tiếp cái kết quả này thì phải

<a id="S00165"></a>
**[00:22:27 → 00:22:30] [Người nói?]** [nghe không rõ 00:22:27; cần đối chiếu] một là đề xuất mô hình mới, hai là sẽ bổ sung thêm các mô hình vào trong phần

<a id="S00166"></a>
**[00:22:31 → 00:22:35] [Người nói?]** [nghe không rõ 00:22:31; cần đối chiếu] Em gửi lại thầy slide này nhé

<a id="S00167"></a>
**[00:22:35 → 00:22:35] [Người nói?]** [nghe không rõ 00:22:35; cần đối chiếu] Vâng

<a id="S00168"></a>
**[00:22:35 → 00:22:41] [Người nói?]** [nghe không rõ 00:22:35; cần đối chiếu] Còn em báo cán không?

## Báo cáo mô hình với server/client — thuật ngữ chưa rõ

<a id="S00169"></a>
**[00:22:41 → 00:23:21] [Người nói?]** [nghe không rõ 00:22:41; cần đối chiếu] Chúng ta đã sử dụng một số nội dung về phương pháp lựa chọn thoa bởi máy PNC.

<a id="S00170"></a>
**[00:23:22 → 00:23:29] [Người nói?]** [nghe không rõ 00:23:22; cần đối chiếu] Thì ở đây thì đối với họ thì em tập trung vào nội dung này là

<a id="S00171"></a>
**[00:23:29 → 00:23:33] [Người nói?]** [nghe không rõ 00:23:29; cần đối chiếu] thêm bản thân sử dụng để diễn kiến rất hiểu.

<a id="S00172"></a>
**[00:23:33 → 00:23:40] [Người nói?]** [nghe không rõ 00:23:33; cần đối chiếu] Thế thì mục tiêu nhất là về đại thiện về sự không dịch dữ liệu.

<a id="S00173"></a>
**[00:23:40 → 00:23:46] [Người nói?]** [nghe không rõ 00:23:40; cần đối chiếu] Ở đây là tụi em tập trung vào đại thiện về nhận dịch dữ liệu về nhãn.

<a id="S00174"></a>
**[00:23:46 → 00:23:52] [Người nói?]** [nghe không rõ 00:23:46; cần đối chiếu] Thứ hai là không lưu ý về nhãn và số lượng bảo.

<a id="S00175"></a>
**[00:23:52 → 00:24:00] [Người nói?]** [nghe không rõ 00:23:52; cần đối chiếu] Thứ hai là về nhận định được số lượng và lớp kiếm của các cây đường.

<a id="S00176"></a>
**[00:24:04 → 00:24:08] [Người nói?]** [nghe không rõ 00:24:04; cần đối chiếu] Đầu tiên là về bài tháp của ESPN 2026.

<a id="S00177"></a>
**[00:24:08 → 00:24:12] [Người nói?]** [nghe không rõ 00:24:08; cần đối chiếu] Em đã kết hợp Star với Logix Assets.

<a id="S00178"></a>
**[00:24:13 → 00:24:23] [Người nói?]** [nghe không rõ 00:24:13; cần đối chiếu] Thì ở đây thì cái Startup này là để truyền hóa cái đặc trưng tại tên và cái Office của chúng mình là để ưu tiên kể các tổng hợp thứ đó kìa

<a id="S00179"></a>
**[00:24:25 → 00:24:36] [Người nói?]** [nghe không rõ 00:24:25; cần đối chiếu] Thì khi mà tựa có các copy cũng như là copy một bản thân liệt và copy một loại thì có một số cái hạn để đối với MyPSP để đánh thức là về cái vụ đó không rõ gì là thông tin

<a id="S00180"></a>
**[00:24:36 → 00:24:44] [Người nói?]** [nghe không rõ 00:24:36; cần đối chiếu] Thứ hai là trước chương trình hành xử lý cái tổng hợp kiến sẽ có một chiếc vẫn sử dụng cái phép pháp về tưởng

<a id="S00181"></a>
**[00:24:44 → 00:24:57] [Người nói?]** [nghe không rõ 00:24:44; cần đối chiếu] Thứ ba là nó còn quá nhẹ cho bệnh viện, nó có đối với bộ test ai hiểu thì chắc là không phải thứ 5 nhưng mà cái collision nó không phải thứ 6, thì có cảnh báo nhiều hơn nhiều.

<a id="S00182"></a>
**[00:24:57 → 00:25:04] [Người nói?]** [nghe không rõ 00:24:57; cần đối chiếu] Chính vì thế thì dù những cái đặc biệt này thì em có hình vị cái hướng nghiên cứu nào là đối với bệnh viện mà không có.

<a id="S00183"></a>
**[00:25:07 → 00:25:18] [Người nói?]** [nghe không rõ 00:25:07; cần đối chiếu] Câu hỏi này sẽ tiến hành xử lý tại server và tiến hành ưu tiên các đề nghệ tiền ở các lớp tiềm

<a id="S00184"></a>
**[00:25:18 → 00:25:23] [Người nói?]** [nghe không rõ 00:25:18; cần đối chiếu] 3 hình ứng quan trọng nhất là hiểu tình đủ lạnh ở server

<a id="S00185"></a>
**[00:25:23 → 00:25:28] [Người nói?]** [nghe không rõ 00:25:23; cần đối chiếu] Thứ hai là hiểu tìm cái khu vực bộ theo cái điều kiện đấy là

<a id="S00186"></a>
**[00:25:29 → 00:25:33] [Người nói?]** [nghe không rõ 00:25:29; cần đối chiếu] bởi vì nếu mà mình luôn luôn bật cho nó công ty ký lập kiếm

<a id="S00187"></a>
**[00:25:33 → 00:25:37] [Người nói?]** [nghe không rõ 00:25:33; cần đối chiếu] thì nó sẽ có những dấu lập nhiều, cảnh báo rất là nhiều

<a id="S00188"></a>
**[00:25:38 → 00:25:42] [Người nói?]** [nghe không rõ 00:25:38; cần đối chiếu] tùy vào các lớp thì mình sẽ bật cái công ty ký lập kiếm

<a id="S00189"></a>
**[00:25:42 → 00:25:48] [Người nói?]** [nghe không rõ 00:25:42; cần đối chiếu] và sẽ gửi đến server đấy thông tin

<a id="S00190"></a>
**[00:25:48 → 00:25:50] [Người nói?]** [nghe không rõ 00:25:48; cần đối chiếu] nhất là về cái trọng số của mô hình

<a id="S00191"></a>
**[00:25:50 → 00:25:54] [Người nói?]** [nghe không rõ 00:25:50; cần đối chiếu] và thứ hai nữa là về cái số lượng lớp của tài chất lượng đấy

<a id="S00192"></a>
**[00:25:57 → 00:26:29] [Người nói?]** [nghe không rõ 00:25:57; cần đối chiếu] Các bạn có thể nhớ đăng ký kênh để ủng hộ kênh của mình nhé.

<a id="S00193"></a>
**[00:26:29 → 00:26:33] [Người nói?]** [nghe không rõ 00:26:29; cần đối chiếu] số lượng màu của lớp đó, chưa biết là lớp nào đó là thiếu

<a id="S00194"></a>
**[00:26:33 → 00:26:35] [Người nói?]** [nghe không rõ 00:26:33; cần đối chiếu] mà chúng ta có thể xử lý

<a id="S00195"></a>
**[00:26:35 → 00:26:39] [Người nói?]** [nghe không rõ 00:26:35; cần đối chiếu] và star bây giờ là điều để giảm lệnh trọng trưng

<a id="S00196"></a>
**[00:26:39 → 00:26:46] [Người nói?]** [nghe không rõ 00:26:39; cần đối chiếu] nhưng mà chưa thể xử lý liên quan đến lệnh nhãn

<a id="S00197"></a>
**[00:26:46 → 00:26:48] [Người nói?]** [nghe không rõ 00:26:46; cần đối chiếu] mà chỉ là liên quan đến chuẩn loại không thể trọng trưng

<a id="S00198"></a>
**[00:26:48 → 00:26:49] [Người nói?]** [nghe không rõ 00:26:48; cần đối chiếu] tổng hợp ở trên

<a id="S00199"></a>
**[00:26:49 → 00:26:53] [Người nói?]** [nghe không rõ 00:26:49; cần đối chiếu] phép ls là điều chỉnh smog 1

<a id="S00200"></a>
**[00:26:53 → 00:26:56] [Người nói?]** [nghe không rõ 00:26:53; cần đối chiếu] nhưng mà server vẫn đang dùng về phép avg

<a id="S00201"></a>
**[00:26:57 → 00:27:00] [Người nói?]** [nghe không rõ 00:26:57; cần đối chiếu] phép 2, phép 2s là bài mẫu của VNST 06

<a id="S00202"></a>
**[00:27:00 → 00:27:11] [Người nói?]** [nghe không rõ 00:27:00; cần đối chiếu] thì tiêu chí mới xích mốc bổ, cải thiện deco lớp yếm nhờ lưu ích, nhưng vẫn sử dụng tham số để cố định

<a id="S00203"></a>
**[00:27:11 → 00:27:17] [Người nói?]** [nghe không rõ 00:27:11; cần đối chiếu] và thứ hai là lưu ích lò lỉa thông tin và cảnh báo cao

<a id="S00204"></a>
**[00:27:17 → 00:27:27] [Người nói?]** [nghe không rõ 00:27:17; cần đối chiếu] thứ ba là lưu ích của roto và roto thì hỗ trợ lớp chung quan sát nhưng ti phí truyền thông hiện tại cao

<a id="S00205"></a>
**[00:27:27 → 00:27:30] [Người nói?]** [nghe không rõ 00:27:27; cần đối chiếu] khoảng 112,5kb trên 1 vòng

<a id="S00206"></a>
**[00:27:32 → 00:27:45] [Người nói?]** [nghe không rõ 00:27:32; cần đối chiếu] Từ những vấn đề này, có thể là nhận biết môi trường trong lớp thiếu thay sự kiện xây dựng hay tài liệu xây dựng hơn và vẫn bảo hành kỹ thuật thông.

<a id="S00207"></a>
**[00:27:47 → 00:27:50] [Người nói?]** [nghe không rõ 00:27:47; cần đối chiếu] Từ nãy đến lúc phát biểu xuất của mình.

<a id="S00208"></a>
**[00:27:51 → 00:28:02] [Người nói?]** [nghe không rõ 00:27:51; cần đối chiếu] Đầu tiên là các dữ liệu thú luyện tại các cây đần và chất thú luyện sẽ được kiểu hóa bằng star, như quả PNCT.

<a id="S00209"></a>
**[00:28:03 → 00:28:08] [Người nói?]** [nghe không rõ 00:28:03; cần đối chiếu] Sau khi được thú luyện thì sẽ gửi 2 thông số lên cho server.

<a id="S00210"></a>
**[00:28:08 → 00:28:14] [Người nói?]** [nghe không rõ 00:28:08; cần đối chiếu] Thứ nhất là về trọng số của mình, thứ hai là số lượng nhám của lớp ở cây đần đấy.

<a id="S00211"></a>
**[00:28:15 → 00:28:22] [Người nói?]** [nghe không rõ 00:28:15; cần đối chiếu] Để mình nhận được lớp nào là lớp kiếm và số lượng mở cuộc tại cái lần đấy so với lần khác

<a id="S00212"></a>
**[00:28:22 → 00:28:28] [Người nói?]** [nghe không rõ 00:28:22; cần đối chiếu] Sau đó chị em tiến hành sử dụng cái PPA này là

<a id="S00213"></a>
**[00:28:28 → 00:28:37] [Người nói?]** [nghe không rõ 00:28:28; cần đối chiếu] Thứ nhất là, nếu mà mình sử dụng cái 5DFCT thì là sử dụng cộng tổng thép AMG

<a id="S00214"></a>
**[00:28:38 → 00:28:39] [Người nói?]** [nghe không rõ 00:28:38; cần đối chiếu] Thì cộng tổng trung tính chung

<a id="S00215"></a>
**[00:28:39 → 00:28:43] [Người nói?]** [nghe không rõ 00:28:39; cần đối chiếu] Nhưng mà một số cây lượng thì nó chất cộng với lớp kiếm ở đấy

<a id="S00216"></a>
**[00:28:43 → 00:28:46] [Người nói?]** [nghe không rõ 00:28:43; cần đối chiếu] Mình chỉ dùng trọng nguyên dung thì trọng nguyên dung đó là nhiễu

<a id="S00217"></a>
**[00:28:46 → 00:28:50] [Người nói?]** [nghe không rõ 00:28:46; cần đối chiếu] và nó làm ảnh hưởng so với classical

<a id="S00218"></a>
**[00:28:52 → 00:28:57] [Người nói?]** [nghe không rõ 00:28:52; cần đối chiếu] Ở đây thì em chỉ là tổng cọng của những cái làm bóng lớn ở đây

<a id="S00219"></a>
**[00:28:57 → 00:29:02] [Người nói?]** [nghe không rõ 00:28:57; cần đối chiếu] Lăng ở phần backbone là cái phần cơ bào của mô hình

<a id="S00220"></a>
**[00:29:02 → 00:29:04] [Người nói?]** [nghe không rõ 00:29:02; cần đối chiếu] thì em sử dụng CPU

<a id="S00221"></a>
**[00:29:06 → 00:29:13] [Người nói?]** [nghe không rõ 00:29:06; cần đối chiếu] Thay vì em sử dụng bởi vì nó chỉ có một tỷ số trong một cái lần

<a id="S00222"></a>
**[00:29:13 → 00:29:26] [Người nói?]** [nghe không rõ 00:29:13; cần đối chiếu] Chính vì thế thì em không tiến hành trọng trung bình chung của số lượng mẫu của cái lần đấy

<a id="S00223"></a>
**[00:29:26 → 00:29:32] [Người nói?]** [nghe không rõ 00:29:26; cần đối chiếu] Không tính trung bình chung của số lượng mẫu của cái lần đấy so với tổng cục mà sẽ tiến hành đấy là

<a id="S00224"></a>
**[00:29:34 → 00:29:42] [Người nói?]** [nghe không rõ 00:29:34; cần đối chiếu] Ví dụ có 3 thì em sẽ lấy 1 phần 3 của cái trung bình chung của từng nhãn 1 sau đó tổng lại

<a id="S00225"></a>
**[00:29:42 → 00:29:46] [Người nói?]** [nghe không rõ 00:29:42; cần đối chiếu] để tổng số sẽ ưu tiên được lớp kiểm ở đây

<a id="S00226"></a>
**[00:29:46 → 00:29:50] [Người nói?]** [nghe không rõ 00:29:46; cần đối chiếu] Thứ ba là lcdn

<a id="S00227"></a>
**[00:29:50 → 00:29:58] [Người nói?]** [nghe không rõ 00:29:50; cần đối chiếu] để thành để là bật hoặc không bật chế độ lupit assessment

<a id="S00228"></a>
**[00:29:59 → 00:30:00] [Người nói?]** [nghe không rõ 00:29:59; cần đối chiếu] hoặc

<a id="S00229"></a>
**[00:30:00 → 00:30:04] [Người nói?]** [nghe không rõ 00:30:00; cần đối chiếu] là mình sử dụng bình thường, theo từng lợi ích, từng ngã, từng lớp

<a id="S00230"></a>
**[00:30:05 → 00:30:11] [Người nói?]** [nghe không rõ 00:30:05; cần đối chiếu] Thực ra tại đây thì em đã có một số kết quả, một số so sánh so với phương pháp của VNCT

<a id="S00231"></a>
**[00:30:11 → 00:30:15] [Người nói?]** [nghe không rõ 00:30:11; cần đối chiếu] Nhất là về xử lý trung cộng thì mình cũng đã có phương pháp đại báo

<a id="S00232"></a>
**[00:30:16 → 00:30:17] [Người nói?]** [nghe không rõ 00:30:16; cần đối chiếu] Đại báo này đã có so với bài VNCT

<a id="S00233"></a>
**[00:30:18 → 00:30:23] [Người nói?]** [nghe không rõ 00:30:18; cần đối chiếu] Vậy nên là các point theo lớp cũng như là thử nghiệm của bộ thử nghiệm bài này đã có so với bài VNCT

<a id="S00234"></a>
**[00:30:23 → 00:30:33] [Người nói?]** [nghe không rõ 00:30:23; cần đối chiếu] Về hóa hình nghiệp thì em sử dụng 4 nguồn dữ liệu. Đấy là TOR-90, TOR-95, SIRP và CIC-IS-200.

<a id="S00235"></a>
**[00:30:34 → 00:30:55] [Người nói?]** [nghe không rõ 00:30:34; cần đối chiếu] Về cấu hình nghiệp thì em sử dụng số lượng gần gần 10. Sử dụng đối tượng tích với tắc số 1.3 và 1.5 và sử dụng 4 kết quả nguồn dữ liệu tầm 0.5 và 1 kết quả nguồn dữ liệu tầm 0.1.

<a id="S00236"></a>
**[00:30:55 → 00:30:58] [Người nói?]** [nghe không rõ 00:30:55; cần đối chiếu] của mình để so sánh với nguyên tố của bệnh hoạt hóa.

<a id="S00237"></a>
**[00:31:00 → 00:31:02] [Người nói?]** [nghe không rõ 00:31:00; cần đối chiếu] Trên đây là một số kết quả chính của chúng ta.

<a id="S00238"></a>
**[00:31:02 → 00:31:08] [Người nói?]** [nghe không rõ 00:31:02; cần đối chiếu] Nhất là về kết quả Macro S1 cũng như S1-4 của chúng ta

<a id="S00239"></a>
**[00:31:08 → 00:31:14] [Người nói?]** [nghe không rõ 00:31:08; cần đối chiếu] của phương pháp đề xuất là F-CF-A là phương pháp đề xuất của bệnh hoạt hóa.

<a id="S00240"></a>
**[00:31:15 → 00:31:21] [Người nói?]** [nghe không rõ 00:31:15; cần đối chiếu] Về so sánh đối với từng hệ phần, từng hệ phần trong phương pháp đề xuất,

<a id="S00241"></a>
**[00:31:21 → 00:31:26] [Người nói?]** [nghe không rõ 00:31:21; cần đối chiếu] khi mà ta tiến hành tổng hợp lại cả phương pháp mà mình đặt ra

<a id="S00242"></a>
**[00:31:26 → 00:31:29] [Người nói?]** [nghe không rõ 00:31:26; cần đối chiếu] thì có kết quả tốt hơn so với từng khuất như lẻ.

<a id="S00243"></a>
**[00:31:29 → 00:31:36] [Người nói?]** [nghe không rõ 00:31:29; cần đối chiếu] Thứ hai là về tiến hành so với các thương cứu ở đây thì

<a id="S00244"></a>
**[00:31:36 → 00:31:44] [Người nói?]** [nghe không rõ 00:31:36; cần đối chiếu] của mình đầu tiên cái bộ có 3 mẫu là bộ CSC, S-AMT và B15 thì kết quả rất là tốt lắm.

<a id="S00245"></a>
**[00:31:44 → 00:31:48] [Người nói?]** [nghe không rõ 00:31:44; cần đối chiếu] Và chúng ta đã có kết quả tốt hơn của các thương cứu nước ngoài đó.

<a id="S00246"></a>
**[00:31:48 → 00:31:53] [Người nói?]** [nghe không rõ 00:31:48; cần đối chiếu] Bộ con AMT trong số mẫu, mẫu kiếm của cái bộ đấy nó rất là ít.

<a id="S00247"></a>
**[00:31:53 → 00:31:57] [Người nói?]** [nghe không rõ 00:31:53; cần đối chiếu] Vì thế thì cái này mình nghĩ mình thấp hơn một chút là không ít.

## Sinh dữ liệu SQL và điểm thưởng

<a id="S00248"></a>
**[00:32:19 → 00:33:09] [Người nói?]** [nghe không rõ 00:32:19; cần đối chiếu] em xin phép báo cáo nhanh tuần trước là em cũng đã thành công bảo vệ thạc sĩ anh thì

<a id="S00249"></a>
**[00:33:09 → 00:33:22] [Người nói?]** [nghe không rõ 00:33:09; cần đối chiếu] là đề tài thì đây là thông số mà em có thuyết trình ạ thì hiện tại thì các thầy

<a id="S00250"></a>
**[00:33:22 → 00:33:23] [Người nói?]** [nghe không rõ 00:33:22; cần đối chiếu] có nói là

<a id="S00251"></a>
**[00:33:23 → 00:33:26] [Người nói?]** [nghe không rõ 00:33:23; cần đối chiếu] so với các mô hình đề xuất thì chỉ có mô hình

<a id="S00252"></a>
**[00:33:26 → 00:33:28] [Người nói?]** [nghe không rõ 00:33:26; cần đối chiếu] SMOTE và mô hình của em

<a id="S00253"></a>
**[00:33:28 → 00:33:29] [Người nói?]** [nghe không rõ 00:33:28; cần đối chiếu] là có thông số khả quan

<a id="S00254"></a>
**[00:33:29 → 00:33:32] [Người nói?]** [nghe không rõ 00:33:29; cần đối chiếu] các mô hình khác thì là thông số

<a id="S00255"></a>
**[00:33:32 → 00:33:33] [Người nói?]** [nghe không rõ 00:33:32; cần đối chiếu] và kết quả đưa ra là

<a id="S00256"></a>
**[00:33:35 → 00:33:36] [Người nói?]** [nghe không rõ 00:33:35; cần đối chiếu] nó chưa đủ thuyết phục

<a id="S00257"></a>
**[00:33:36 → 00:33:38] [Người nói?]** nên với cả là các bài

<a id="S00258"></a>
**[00:33:38 → 00:33:40] [Người nói?]** báo khoa học mà em dựa vào

<a id="S00259"></a>
**[00:33:40 → 00:33:42] [Người nói?]** thì là em có chỉ ra rằng là

<a id="S00260"></a>
**[00:33:42 → 00:33:44] [Người nói?]** [nghe không rõ 00:33:42; cần đối chiếu] hiện nay để tiết kiệm chi phí

<a id="S00261"></a>
**[00:33:44 → 00:33:46] [Người nói?]** [nghe không rõ 00:33:44; cần đối chiếu] và bởi vì mô hình dữ liệu rất là lớn

<a id="S00262"></a>
**[00:33:46 → 00:33:48] [Người nói?]** [nghe không rõ 00:33:46; cần đối chiếu] nên là người ta sẽ ưu tiên dùng phương pháp

<a id="S00263"></a>
**[00:33:48 → 00:33:50] [Người nói?]** [nghe không rõ 00:33:48; cần đối chiếu] SMOTE còn phương pháp sinh dữ liệu

<a id="S00264"></a>
**[00:33:50 → 00:33:51] [Người nói?]** để bổ sung vào cơ sở dữ liệu

<a id="S00265"></a>
**[00:33:51 → 00:33:58] [Người nói?]** [nghe không rõ 00:33:51; cần đối chiếu] dấu hiệu thì là đang em như em đang tìm hiểu thì đang chưa có nhiều bài báo nào thì sau khi em áp

<a id="S00266"></a>
**[00:33:58 → 00:34:06] [Người nói?]** [nghe không rõ 00:33:58; cần đối chiếu] dụng thì đây là kết quả thì đối với mô hình một thông thường thì là các dấu hiệu cơ bản thì mô

<a id="S00267"></a>
**[00:34:06 → 00:34:13] [Người nói?]** [nghe không rõ 00:34:06; cần đối chiếu] hình có khả năng nhận biết rất rõ Tuy nhiên là các dữ liệu mà có yếu tố đặc trưng hơn thì thường bị

<a id="S00268"></a>
**[00:34:13 → 00:34:20] [Người nói?]** [nghe không rõ 00:34:13; cần đối chiếu] lẫn vào ví dụ ở đây là nhóm mà mục tiêu là sinh dữ liệu bộ lần thì lại đôi lúc lại có thêm một số

<a id="S00269"></a>
**[00:34:20 → 00:34:28] [Người nói?]** [nghe không rõ 00:34:20; cần đối chiếu] có một số nhãn về xanh dụng và đôi lúc mà nó quên chưa đóng dấu câu như phần em bôi đỏ thì ở đấy câu

<a id="S00270"></a>
**[00:34:28 → 00:34:39] [Người nói?]** [nghe không rõ 00:34:28; cần đối chiếu] lệnh đấy là câu lệnh sẽ bị lỗi và sẽ bị chặn nghe tức còn dữ liệu môi của em ạ thì là ở hai nhóm

<a id="S00271"></a>
**[00:34:40 → 00:34:47] [Người nói?]** [nghe không rõ 00:34:40; cần đối chiếu] 22 nhóm đầu tiên thì là các cái dấu hiệu về bộ lần vài lần là mô hình là môi của em đã có khả

<a id="S00272"></a>
**[00:34:47 → 00:34:49] [Người nói?]** [nghe không rõ 00:34:47; cần đối chiếu] năng sinh ra rồi và đã được chặn

<a id="S00273"></a>
**[00:34:49 → 00:34:51] [Người nói?]** chặn ở đây nghĩa là

<a id="S00274"></a>
**[00:34:51 → 00:34:53] [Người nói?]** cái tường lửa nó đã nhận biết được là đây

<a id="S00275"></a>
**[00:34:53 → 00:34:55] [Người nói?]** có những dấu hiệu tấn công không phải là

<a id="S00276"></a>
**[00:34:55 → 00:34:57] [Người nói?]** những dấu hiệu nhiễu nữa

<a id="S00277"></a>
**[00:34:57 → 00:35:00] [Người nói?]** còn đối với 2 cái mô hình còn lại

<a id="S00278"></a>
**[00:35:00 → 00:35:01] [Người nói?]** [nghe không rõ 00:35:00; cần đối chiếu] là Time và Union thì cấu trúc

<a id="S00279"></a>
**[00:35:01 → 00:35:03] [Người nói?]** [nghe không rõ 00:35:01; cần đối chiếu] ngư pháp nó yêu cầu cao hơn

<a id="S00280"></a>
**[00:35:03 → 00:35:05] [Người nói?]** nên khi mà sinh ra dữ liệu

<a id="S00281"></a>
**[00:35:05 → 00:35:08] [Người nói?]** thì mô hình của em lại đang không học được

<a id="S00282"></a>
**[00:35:08 → 00:35:09] [Người nói?]** thế nên là sinh ra dữ liệu

<a id="S00283"></a>
**[00:35:09 → 00:35:11] [Người nói?]** [nghe không rõ 00:35:09; cần đối chiếu] nhiễu rất là nhiều và không khỏe năng

<a id="S00284"></a>
**[00:35:11 → 00:35:14] [Người nói?]** [nghe không rõ 00:35:11; cần đối chiếu] khai thác thực tế ạ. Thì trong tuần này

<a id="S00285"></a>
**[00:35:14 → 00:35:16] [Người nói?]** là em cũng đã cố gắng thay đổi

<a id="S00286"></a>
**[00:35:16 → 00:35:18] [Người nói?]** các cái thông số ở trong mô hình

<a id="S00287"></a>
**[00:35:18 → 00:35:21] [Người nói?]** nhưng mà kết quả thì vẫn đang chưa được khả quan

<a id="S00288"></a>
**[00:35:21 → 00:35:27] [Người nói?]** thì hôm nay em trình bày để mong là thầy cho em một định hướng để có thể cải thiện

<a id="S00289"></a>
**[00:35:27 → 00:35:31] [Người nói?]** thì hiện tại mục tiêu của em là em cho rằng là

<a id="S00290"></a>
**[00:35:31 → 00:35:33] [Người nói?]** đối với các loại dữ liệu thông thường

<a id="S00291"></a>
**[00:35:33 → 00:35:36] [Người nói?]** nghĩa là có dữ liệu tấn công lớn mà nhiều

<a id="S00292"></a>
**[00:35:36 → 00:35:41] [Người nói?]** [nghe không rõ 00:35:36; cần đối chiếu] thì phương pháp SMOTE nó sẽ ưu việt hơn về mặt chi phí

<a id="S00293"></a>
**[00:35:41 → 00:35:44] [Người nói?]** tuy nhiên là ở những mẫu mà yêu cầu ngữ pháp cao hơn

<a id="S00294"></a>
**[00:35:44 → 00:35:47] [Người nói?]** [nghe không rõ 00:35:44; cần đối chiếu] thì mô hình của em sẽ tốt hơn để có thể bổ sung vào

<a id="S00295"></a>
**[00:35:47 → 00:35:53] [Người nói?]** thì em đang hiện tại đang đi theo hướng này đây là kết quả của em

<a id="S00296"></a>
**[00:35:53 → 00:36:08] [Người nói?]** thì hiện tại sẽ có hai nhóm đầu tiên là hai nhóm bên trên thì cấu trúc của nó nó sẽ rất là đơn giản

<a id="S00297"></a>
**[00:36:08 → 00:36:12] [Người nói?]** [nghe không rõ 00:36:08; cần đối chiếu] nó chỉ cần yêu cầu ví dụ như là nhóm Aaron là cố gắng sinh ra lỗi

<a id="S00298"></a>
**[00:36:12 → 00:36:15] [Người nói?]** [nghe không rõ 00:36:12; cần đối chiếu] còn nhóm Boland là cố gắng ép

<a id="S00299"></a>
**[00:36:16 → 00:36:17] [Người nói?]** Cố gắng

<a id="S00300"></a>
**[00:36:18 → 00:36:19] [Người nói?]** Thì nói chung là 2 mẫu này

<a id="S00301"></a>
**[00:36:19 → 00:36:22] [Người nói?]** [nghe không rõ 00:36:19; cần đối chiếu] Thì nó sẽ yêu cầu ngữ pháp rất là thấp

<a id="S00302"></a>
**[00:36:22 → 00:36:23] [Người nói?]** Còn 2 mẫu còn lại

<a id="S00303"></a>
**[00:36:23 → 00:36:25] [Người nói?]** Thì nó sẽ yêu cầu phải

<a id="S00304"></a>
**[00:36:25 → 00:36:27] [Người nói?]** Thứ nhất là phải đúng cơ sở dữ liệu

<a id="S00305"></a>
**[00:36:27 → 00:36:28] [Người nói?]** Mà nó tấn công vào

<a id="S00306"></a>
**[00:36:28 → 00:36:31] [Người nói?]** Thì nói chung là 2 mẫu dưới nó yêu cầu cao hơn

<a id="S00307"></a>
**[00:36:31 → 00:36:33] [Người nói?]** [nghe không rõ 00:36:31; cần đối chiếu] Đến cả phương pháp smooth

<a id="S00308"></a>
**[00:36:33 → 00:36:35] [Người nói?]** Nó cũng không làm ổn hết

<a id="S00309"></a>
**[00:36:37 → 00:36:38] [Người nói?]** Thì

<a id="S00310"></a>
**[00:36:39 → 00:36:41] [Người nói?]** Em đang định là

<a id="S00311"></a>
**[00:36:41 → 00:36:43] [Người nói?]** Tập trung vào 2 phương án khó hơn

<a id="S00312"></a>
**[00:36:43 → 00:36:45] [Người nói?]** Nhưng mà 2 phương án khó hơn

<a id="S00313"></a>
**[00:36:45 → 00:36:47] [Người nói?]** Hiện tại em đang cố gắng mà vẫn chưa có cải thiện

<a id="S00314"></a>
**[00:36:47 → 00:36:53] [Người nói?]** Nên là mình đang mong muốn xin định hướng của thầy ạ

<a id="S00315"></a>
**[00:36:53 → 00:37:13] [Người nói?]** [nghe không rõ 00:36:53; cần đối chiếu] Em đưa mô hình này, chứ có mẻ quá không

<a id="S00316"></a>
**[00:37:13 → 00:37:24] [Người nói?]** [nghe không rõ 00:37:13; cần đối chiếu] Đây là mô hình của em, em dựa trên các phần em đánh dấu vuông là em 4 phương án đề xuất ạ

<a id="S00317"></a>
**[00:37:24 → 00:37:29] [Người nói?]** Đầu tiên là em sẽ cố gắng tách theo chuỗi cú pháp SQL

<a id="S00318"></a>
**[00:37:29 → 00:37:34] [Người nói?]** thì thay vì đưa vào các cái thông số như kiểu 123

<a id="S00319"></a>
**[00:37:34 → 00:37:36] [Người nói?]** thì em sẽ biến thành keyword là number

<a id="S00320"></a>
**[00:37:36 → 00:37:41] [Người nói?]** hoặc là các cái cụ SQL thì em sẽ chuẩn hóa nó lại

<a id="S00321"></a>
**[00:37:41 → 00:37:44] [Người nói?]** để tránh việc phải học quá nhiều dữ liệu mà có chung mục đích ạ

<a id="S00322"></a>
**[00:37:44 → 00:37:46] [Người nói?]** tiếp theo là trong bộ sinh

<a id="S00323"></a>
**[00:37:46 → 00:37:50] [Người nói?]** [nghe không rõ 00:37:46; cần đối chiếu] thì là em sẽ tăng số lượng chuỗi

<a id="S00324"></a>
**[00:37:50 → 00:37:53] [Người nói?]** [nghe không rõ 00:37:50; cần đối chiếu] thay vì ở bài gốc của tác giả này là 20

<a id="S00325"></a>
**[00:37:53 → 00:37:55] [Người nói?]** [nghe không rõ 00:37:53; cần đối chiếu] thì em sẽ tăng lên thành 160

<a id="S00326"></a>
**[00:37:57 → 00:38:05] [Người nói?]** còn huấn luyện trước bộ sinh thì em sẽ tăng cường việc huấn luyện trước bộ sinh để tránh việc mô hình bị xụp đổ quá sớm

<a id="S00327"></a>
**[00:38:05 → 00:38:08] [Người nói?]** và cuối cùng là em sẽ kết hợp điểm thưởng

<a id="S00328"></a>
**[00:38:08 → 00:38:16] [Người nói?]** thì thay vì nhận biết là dữ liệu thật hay giả thì sẽ phải thêm một cái nữa là liệu dữ liệu đấy có cấu trúc SQL không ạ

<a id="S00329"></a>
**[00:38:16 → 00:38:18] [Người nói?]** [nghe không rõ 00:38:16; cần đối chiếu] thì đây là 3 thành phần ạ

<a id="S00330"></a>
**[00:38:18 → 00:38:23] [Người nói?]** [nghe không rõ 00:38:18; cần đối chiếu] thì các thầy hội đồng cũng đã nhận ra là em có một vấn đề khá lớn với phần điểm thưởng ạ

<a id="S00331"></a>
**[00:38:23 → 00:38:28] [Người nói?]** [nghe không rõ 00:38:23; cần đối chiếu] Bởi vì đầu tiên là cái hàm mà đánh giá mô hình SQL

<a id="S00332"></a>
**[00:38:28 → 00:38:32] [Người nói?]** [nghe không rõ 00:38:28; cần đối chiếu] Thì nó lại có sự tương đương với hàm đánh giá

<a id="S00333"></a>
**[00:38:32 → 00:38:34] [Người nói?]** [nghe không rõ 00:38:32; cần đối chiếu] Nghĩa là kiểu vừa đạp bóng vừa thổi còi

<a id="S00334"></a>
**[00:38:34 → 00:38:43] [Người nói?]** Thế nên là nó sẽ khiến cho mô hình của em là có xu hướng là cố gắng học những cái thành phần để điểm cao

<a id="S00335"></a>
**[00:38:43 → 00:38:47] [Người nói?]** Thì đây là phần em cũng đang cố gắng tìm hiểu để cải thiện

<a id="S00336"></a>
**[00:38:47 → 00:38:51] [Người nói?]** Còn các thành phần khác thì em chưa gặp vấn đề gì

<a id="S00337"></a>
**[00:38:51 → 00:39:03] [Người nói?]** [nghe không rõ 00:38:51; cần đối chiếu] Phần sau anh muốn nghe rõ về vỉ huẩn của tính như thế nào

<a id="S00338"></a>
**[00:39:03 → 00:39:14] [Người nói?]** [nghe không rõ 00:39:03; cần đối chiếu] Vâng, thế thì phần sau em sẽ làm sai chi tiết hơn về phần này, có giải thích

<a id="S00339"></a>
**[00:39:18 → 00:39:25] [Người nói?]** [nghe không rõ 00:39:18; cần đối chiếu] Thầy thấy còn về định hướng phần làm của em có cần phải chỉnh sửa hay là em cứ làm rõ các vấn đề

<a id="S00340"></a>
**[00:39:25 → 00:39:29] [Người nói?]** Rõ, viết cái bài hội thảo dựa trên cái này

<a id="S00341"></a>
**[00:39:29 → 00:39:30] [Người nói?]** Cái bài hội thảo, vâng

<a id="S00342"></a>
**[00:39:31 → 00:39:32] [Người nói?]** Làm sao cái chuỗi sinh ra nó có nghĩa hơn

<a id="S00343"></a>
**[00:39:33 → 00:39:35] [Người nói?]** [nghe không rõ 00:39:33; cần đối chiếu] Xem cái vỉ huẩn của mình nó đúng chứ

<a id="S00344"></a>
**[00:39:39 → 00:39:40] [Người nói?]** [nghe không rõ 00:39:39; cần đối chiếu] Rồi, hình chính với em đến đây là hết

<a id="S00345"></a>
**[00:39:40 → 00:39:43] [Người nói?]** [nghe không rõ 00:39:40; cần đối chiếu] Hẹn gặp lại các bạn trong những video tiếp theo.

## Theo dõi dữ liệu sinh, chạy lại và lưu bằng chứng

<a id="S00346"></a>
**[00:40:01 → 00:43:00] [Người nói?]** [nghe không rõ 00:40:01; cần đối chiếu] Vậy là loại trùng lọc Epoch, đầu tiên phải ghi lại, còn đối tên là 4 đoạn xe hông hơi so với lần trước.

<a id="S00347"></a>
**[00:43:03 → 00:43:07] [Người nói?]** [nghe không rõ 00:43:03; cần đối chiếu] Mình cũng tìm hiểu xem cái kết quả của vận cho ý không.

<a id="S00348"></a>
**[00:43:07 → 00:43:32] [Người nói?]** [nghe không rõ 00:43:07; cần đối chiếu] 4 lần đầu chạy thì mùi air, hôm trước thì em đang gặp vấn đề có mùi man nang, nó về giá trị không hết.

<a id="S00349"></a>
**[00:43:33 → 00:43:39] [Người nói?]** [nghe không rõ 00:43:33; cần đối chiếu] Giá trị này là giá trị thể hiện cái true positive càng thấp thì càng tốt.

<a id="S00350"></a>
**[00:43:39 → 00:43:49] [Người nói?]** [nghe không rõ 00:43:39; cần đối chiếu] Hôm trước là thầy có thắc mắc tại sao mà nó về không thì em có kiểm tra lại, chạy lại và theo cái phương pháp như thế chung hướng dẫn.

<a id="S00351"></a>
**[00:43:49 → 00:43:54] [Người nói?]** [nghe không rõ 00:43:49; cần đối chiếu] Hôm qua mình đã bỏ 1 thường lạc đi và mình kiểm tra lại chỉ chính xác

<a id="S00352"></a>
**[00:43:54 → 00:43:59] [Người nói?]** [nghe không rõ 00:43:54; cần đối chiếu] Thì cái chỉ số này thì hiện tại là 3 tháng trước

<a id="S00353"></a>
**[00:44:00 → 00:44:05] [Người nói?]** [nghe không rõ 00:44:00; cần đối chiếu] Cái nguồn man D22 này thì em cũng đã trẻ gặp trên cái bộ dữ liệu của DB

<a id="S00354"></a>
**[00:44:08 → 00:44:13] [Người nói?]** [nghe không rõ 00:44:08; cần đối chiếu] Về mặt so sánh thì cái bộ man D22 này, nguồn man D22 này thì vẫn đang tốt hơn cái man gan gốc

<a id="S00355"></a>
**[00:44:15 → 00:44:18] [Người nói?]** [nghe không rõ 00:44:15; cần đối chiếu] Còn cái nguồn cuối cùng, cái nguồn mình đang đề xuất mới

<a id="S00356"></a>
**[00:44:18 → 00:44:22] [Người nói?]** [nghe không rõ 00:44:18; cần đối chiếu] với mùi mát Auto High Factor Nga

<a id="S00357"></a>
**[00:44:24 → 00:44:26] [Người nói?]** [nghe không rõ 00:44:24; cần đối chiếu] mùi này trong lần đầu tiên em chạy

<a id="S00358"></a>
**[00:44:26 → 00:44:30] [Người nói?]** [nghe không rõ 00:44:26; cần đối chiếu] kết quả nó ra rất là tốt như thế này

<a id="S00359"></a>
**[00:44:30 → 00:44:34] [Người nói?]** [nghe không rõ 00:44:30; cần đối chiếu] có một vài 1ml thì gần như vượt qua 100%

<a id="S00360"></a>
**[00:44:34 → 00:44:39] [Người nói?]** [nghe không rõ 00:44:34; cần đối chiếu] có khoảng 2ml thì vẫn hiện ra các mẫu màu đậu sinh ra

<a id="S00361"></a>
**[00:44:39 → 00:44:48] [Người nói?]** em đang chạy lần thứ 2 để kiểm tra kết quả này của mình có vấn đề gì không

<a id="S00362"></a>
**[00:44:48 → 00:44:51] [Người nói?]** [nghe không rõ 00:44:48; cần đối chiếu] hiện tại với lần 1 thì những kết quả này của em

<a id="S00363"></a>
**[00:44:51 → 00:44:55] [Người nói?]** [nghe không rõ 00:44:51; cần đối chiếu] thì em đã có tất cả các file CFP sinh ra

<a id="S00364"></a>
**[00:44:55 → 00:44:57] [Người nói?]** [nghe không rõ 00:44:55; cần đối chiếu] và em có dùng các công cụ tống kê

<a id="S00365"></a>
**[00:44:57 → 00:45:02] [Người nói?]** [nghe không rõ 00:44:57; cần đối chiếu] thì các mẫu dữ liệu sinh ra thì nó không có vấn đề gì thường vẹn

<a id="S00366"></a>
**[00:45:02 → 00:45:05] [Người nói?]** [nghe không rõ 00:45:02; cần đối chiếu] và nó là những dữ liệu không bị trúng lặng

<a id="S00367"></a>
**[00:45:05 → 00:45:10] [Người nói?]** [nghe không rõ 00:45:05; cần đối chiếu] thì nếu mà em chạy thêm một lần nữa

<a id="S00368"></a>
**[00:45:10 → 00:45:11] [Người nói?]** [nghe không rõ 00:45:10; cần đối chiếu] hoặc là một tháng, một tháng lần nữa

<a id="S00369"></a>
**[00:45:11 → 00:45:15] [Người nói?]** [nghe không rõ 00:45:11; cần đối chiếu] nếu mà cái lắp, cái kết quả của mình không có vấn đề gì cả

<a id="S00370"></a>
**[00:45:15 → 00:45:21] [Người nói?]** [nghe không rõ 00:45:15; cần đối chiếu] thì cái này cũng là hoàn toàn đã đạt yêu cầu mình đặt ra

<a id="S00371"></a>
**[00:45:21 → 00:45:29] [Người nói?]** [nghe không rõ 00:45:21; cần đối chiếu] là mẫu sử dụng sinh ra bằng nguồn mạng của tổng cộng thức đô với các bạn sẽ sinh ra một mẫu hoặc chất lượng.

<a id="S00372"></a>
**[00:45:29 → 00:45:33] [Người nói?]** Thì đấy là cái mà em đang chờ kết quả lần thứ 2.

<a id="S00373"></a>
**[00:45:34 → 00:45:37] [Người nói?]** [nghe không rõ 00:45:34; cần đối chiếu] Với kết quả lần 1 thì toàn bộ dữ liệu của em cũng đã check

<a id="S00374"></a>
**[00:45:37 → 00:45:42] [Người nói?]** [nghe không rõ 00:45:37; cần đối chiếu] và thông qua các công cụ AI để có check những bộ hiệu của mình sinh ra.

<a id="S00375"></a>
**[00:45:43 → 00:45:51] [Người nói?]** [nghe không rõ 00:45:43; cần đối chiếu] Đây là bộ dữ liệu mà em cũng đã sau một lần chạy

<a id="S00376"></a>
**[00:45:51 → 00:45:55] [Người nói?]** [nghe không rõ 00:45:51; cần đối chiếu] thì đều tập hợp thành một cái nước kho dữ liệu

<a id="S00377"></a>
**[00:45:55 → 00:46:24] [Người nói?]** [nghe không rõ 00:45:55; cần đối chiếu] có một bước đồng kê lại. Ví dụ ở đây là pho dữ liệu, thì các file CSV này sinh ra chính là mỗi một file sẽ chứa các mát độc sinh ra

<a id="S00378"></a>
**[00:46:24 → 00:46:32] [Người nói?]** [nghe không rõ 00:46:24; cần đối chiếu] và các bộ mát độc này mà đã vượt qua được cái bộ phát hiện mát độc này thì em cũng đều lưu lại để làm cái minh chứng.

<a id="S00379"></a>
**[00:46:34 → 00:47:10] [Người nói?]** [nghe không rõ 00:46:34; cần đối chiếu] Cảm ơn các bạn đã theo dõi và đăng ký kênh của mình.

<a id="S00380"></a>
**[00:47:10 → 00:47:22] [Người nói?]** [nghe không rõ 00:47:10; cần đối chiếu] tháng 9 thì em cũng mong muốn nếu mà được thì em hoàn thiện bài trong thời gian thứ 3 thì thấy được.

<a id="S00381"></a>
**[00:47:22 → 00:47:23] [Người nói?]** [nghe không rõ 00:47:22; cần đối chiếu] Hoàn toàn kết quả rồi.

<a id="S00382"></a>
**[00:47:23 → 00:47:31] [Người nói?]** [nghe không rõ 00:47:23; cần đối chiếu] Vâng, cái kết quả này thì em đã, đến thời điểm này em thấy em đã thêm một phần kiểm tra nữa

<a id="S00383"></a>
**[00:47:31 → 00:47:32] [Người nói?]** [nghe không rõ 00:47:31; cần đối chiếu] thì em cũng đã kết quả được.

<a id="S00384"></a>
**[00:47:34 → 00:47:45] [Người nói?]** [nghe không rõ 00:47:34; cần đối chiếu] Cái hội thảo SOICT thì em cũng đã tìm hiểu qua về các chủ điểm để họ gửi bài

<a id="S00385"></a>
**[00:47:45 → 00:47:48] [Người nói?]** [nghe không rõ 00:47:45; cần đối chiếu] thì họ có 2 mục và nó khá là khác nhau.

<a id="S00386"></a>
**[00:47:52 → 00:48:02] [Người nói?]** [nghe không rõ 00:47:52; cần đối chiếu] Họ sẽ có một phần chuyên về an toàn thông tin, nhưng họ sẽ có một phần chuyên về học máy,

<a id="S00387"></a>
**[00:48:02 → 00:48:10] [Người nói?]** [nghe không rõ 00:48:02; cần đối chiếu] mà với phần học máy của họ thì họ lại có một phần liên quan lạc ngã.

<a id="S00388"></a>
**[00:48:11 → 00:48:20] [Người nói?]** [nghe không rõ 00:48:11; cần đối chiếu] Tức là trong cái thủ điểm của họ thì họ có một cái phần về Security thì nó làm ở trên cùng này rồi.

<a id="S00389"></a>
**[00:48:22 → 00:48:34] [Người nói?]** [nghe không rõ 00:48:22; cần đối chiếu] Ở dưới này thì có phần liên quan đến an toàn thông tin, Cyber Security, Network Security.

<a id="S00390"></a>
**[00:48:35 → 00:48:58] [Người nói?]** [nghe không rõ 00:48:35; cần đối chiếu] Tuy nhiên hội thảo này còn có phần liên quan đến AI và có phần liên quan đến các mùi liên quan đến mạng đa, mùi sinh.

<a id="S00391"></a>
**[00:48:58 → 00:49:13] [Người nói?]** [nghe không rõ 00:48:58; cần đối chiếu] Thật ra em cũng chưa nộp hội thảo bao giờ nên cũng chưa thể nộp vào mục AI hay là mục an toàn tin.

<a id="S00392"></a>
**[00:49:17 → 00:49:25] [Người nói?]** [nghe không rõ 00:49:17; cần đối chiếu] Thế thì điều kiện này em sử dụng bởi SILENCE, VDN, HOODS, QUITY để họ có mục như vậy.

<a id="S00393"></a>
**[00:49:25 → 00:49:32] [Người nói?]** [nghe không rõ 00:49:25; cần đối chiếu] Thì hiện giờ em so sánh kết quả của em

<a id="S00394"></a>
**[00:49:32 → 00:49:35] [Người nói?]** [nghe không rõ 00:49:32; cần đối chiếu] Nếu mà đúng các thí nghiệm của mình

<a id="S00395"></a>
**[00:49:35 → 00:49:38] [Người nói?]** [nghe không rõ 00:49:35; cần đối chiếu] Thì nó sẽ hơn một chút cái mùi man DNA trước đây

<a id="S00396"></a>
**[00:49:38 → 00:49:41] [Người nói?]** [nghe không rõ 00:49:38; cần đối chiếu] Và hơn cái mùi man nan nốt

<a id="S00397"></a>
**[00:49:41 → 00:49:43] [Người nói?]** [nghe không rõ 00:49:41; cần đối chiếu] Cái bộ thí nghiệm của DG

<a id="S00398"></a>
**[00:49:43 → 00:49:47] [Người nói?]** [nghe không rõ 00:49:43; cần đối chiếu] Thì đang thí nghiệm nốt 1-2 lần nữa

<a id="S00399"></a>
**[00:49:47 → 00:49:49] [Người nói?]** [nghe không rõ 00:49:47; cần đối chiếu] Để cho kết quả nó xứng nhận

<a id="S00400"></a>
**[00:49:49 → 00:49:55] [Người nói?]** [nghe không rõ 00:49:49; cần đối chiếu] Anh nghĩ về lao gì đi

<a id="S00401"></a>
**[00:49:55 → 00:50:00] [Người nói?]** [nghe không rõ 00:49:55; cần đối chiếu] Thí nghiệm của này

## Trao đổi bên lề về công việc, tổ chức và xã hội

<a id="S00402"></a>
**[00:50:08 → 00:50:19] [Người nói?]** [nghe không rõ 00:50:08; cần đối chiếu] Bây giờ đang thầy, trong việc của bạn thầy hiệu phó đang có giấy truyền chuyển cho tôi, loạn lắm, may mắn tôi còn chạy trước.

<a id="S00403"></a>
**[00:50:22 → 00:50:28] [Người nói?]** [nghe không rõ 00:50:22; cần đối chiếu] Kiểu, như kiểu sáng nay có quyết định đã đẩy báo cáo lên sớm,

<a id="S00404"></a>
**[00:50:32 → 00:50:37] [Người nói?]** [nghe không rõ 00:50:32; cần đối chiếu] Thấy khả năng sắp xuống phân biệt mật mạng

<a id="S00405"></a>
**[00:50:39 → 00:50:41] [Người nói?]** [nghe không rõ 00:50:39; cần đối chiếu] Phân biệt mật mạng

<a id="S00406"></a>
**[00:50:52 → 00:50:56] [Người nói?]** [nghe không rõ 00:50:52; cần đối chiếu] Phân biệt mật mạng

<a id="S00407"></a>
**[00:50:56 → 00:50:57] [Người nói?]** [nghe không rõ 00:50:56; cần đối chiếu] Mà thầy lên là thầy sao?

<a id="S00408"></a>
**[00:50:57 → 00:51:02] [Người nói?]** [nghe không rõ 00:50:57; cần đối chiếu] Thầy lên là thầy ôn tư tướng

<a id="S00409"></a>
**[00:51:03 → 00:51:05] [Người nói?]** [nghe không rõ 00:51:03; cần đối chiếu] Cái đấy thầy chưa biết

<a id="S00410"></a>
**[00:51:07 → 00:51:08] [Người nói?]** [nghe không rõ 00:51:07; cần đối chiếu] Nhưng mà khả năng chưa

<a id="S00411"></a>
**[00:51:08 → 00:51:12] [Người nói?]** [nghe không rõ 00:51:08; cần đối chiếu] Bởi vì nếu mà thầy phải ở cấp quản lý cao nhất rồi

<a id="S00412"></a>
**[00:51:13 → 00:51:15] [Người nói?]** [nghe không rõ 00:51:13; cần đối chiếu] Còn thầy cũng khá trẻ

<a id="S00413"></a>
**[00:51:15 → 00:51:17] [Người nói?]** [nghe không rõ 00:51:15; cần đối chiếu] Mặc dù thầy trông khá trẻ

<a id="S00414"></a>
**[00:51:17 → 00:51:19] [Người nói?]** [nghe không rõ 00:51:17; cần đối chiếu] Nhưng mà thầy ngọt ngọt cho thầy biết

<a id="S00415"></a>
**[00:51:20 → 00:51:21] [Người nói?]** [nghe không rõ 00:51:20; cần đối chiếu] Thầy dũng khoảng

<a id="S00416"></a>
**[00:51:21 → 00:51:42] [Người nói?]** [nghe không rõ 00:51:21; cần đối chiếu] Thầy, bố tôi 8 tuổi, tôi 50 tuổi, bố tôi cũng sắp về rồi nên là bố tôi hạ tên ngoại gian, hạ quản lý nhiều, khả năng là sẽ phải hạ thành sư.

<a id="S00417"></a>
**[00:51:44 → 00:51:49] [Người nói?]** [nghe không rõ 00:51:44; cần đối chiếu] Thì biết hơi nhiều về cả công cuộc của chị Úc Vĩ Ngọc.

<a id="S00418"></a>
**[00:51:53 → 00:51:55] [Người nói?]** [nghe không rõ 00:51:53; cần đối chiếu] Mong là nhen tôi được.

<a id="S00419"></a>
**[00:51:55 → 00:52:03] [Người nói?]** [nghe không rõ 00:51:55; cần đối chiếu] Thì khả năng là sẽ đi Đại sứ quán, Đại sứ quán Tắc nước Luân Cập.

<a id="S00420"></a>
**[00:52:03 → 00:52:05] [Người nói?]** [nghe không rõ 00:52:03; cần đối chiếu] Khả năng là làm đẹp như là làm.

<a id="S00421"></a>
**[00:52:05 → 00:52:09] [Người nói?]** [nghe không rõ 00:52:05; cần đối chiếu] Nếu mà đi quốc ca với Đại Thái thì hơi nhạy cản.

<a id="S00422"></a>
**[00:52:11 → 00:52:20] [Người nói?]** [nghe không rõ 00:52:11; cần đối chiếu] Chưa biết được, khả năng cả bố mẹ tôi đi khoảng 7 năm, 6 năm rồi.

<a id="S00423"></a>
**[00:52:26 → 00:52:29] [Người nói?]** [nghe không rõ 00:52:26; cần đối chiếu] Hôm nay tôi chỉ học khoảng 60% thôi vì tôi học trên trường ấy.

<a id="S00424"></a>
**[00:52:30 → 00:52:33] [Người nói?]** [nghe không rõ 00:52:30; cần đối chiếu] Nếu mà là xe bên trường thì sẽ không học bổ sung.

<a id="S00425"></a>
**[00:52:49 → 00:52:50] [Người nói?]** [nghe không rõ 00:52:49; cần đối chiếu] Bạn đăng ký cho ai ạ?

<a id="S00426"></a>
**[00:52:50 → 00:52:53] [Người nói?]** [nghe không rõ 00:52:50; cần đối chiếu] Đăng ký cho ai ạ?

<a id="S00427"></a>
**[00:52:53 → 00:53:06] [Người nói?]** [nghe không rõ 00:52:53; cần đối chiếu] Tôi có bổ sung để học đặc sĩ, các bạn vào học đặc sĩ để học quỷ, các bạn ở bên cạnh hết.

<a id="S00428"></a>
**[00:53:06 → 00:53:11] [Người nói?]** [nghe không rõ 00:53:06; cần đối chiếu] Thế giới học đặc sĩ cũng là bổ sung trong tình huống đặc sĩ.

<a id="S00429"></a>
**[00:53:14 → 00:53:28] [Người nói?]** [nghe không rõ 00:53:14; cần đối chiếu] Không khó lắm đâu bởi vì tuyên báo là chỉ có ngôn liên quan tới tập cung ạ, với cả phòng thủ là 2 ngôn là tạm để phải làm.

<a id="S00430"></a>
**[00:53:28 → 00:53:29] [Người nói?]** [nghe không rõ 00:53:28; cần đối chiếu] Ốc cũng được 200-300k

<a id="S00431"></a>
**[00:53:32 → 00:53:32] [Người nói?]** [nghe không rõ 00:53:32; cần đối chiếu] 300k em chứ

<a id="S00432"></a>
**[00:53:36 → 00:53:40] [Người nói?]** [nghe không rõ 00:53:36; cần đối chiếu] Thế là làm phòng đấy là làm phòng về những quan điểm tham đủ không?

<a id="S00433"></a>
**[00:53:40 → 00:53:41] [Người nói?]** [nghe không rõ 00:53:40; cần đối chiếu] Ừ

<a id="S00434"></a>
**[00:53:41 → 00:53:43] [Người nói?]** [nghe không rõ 00:53:41; cần đối chiếu] Anh ấy là người thích em

<a id="S00435"></a>
**[00:53:43 → 00:53:45] [Người nói?]** [nghe không rõ 00:53:43; cần đối chiếu] Em hỏi anh

<a id="S00436"></a>
**[00:53:45 → 00:53:47] [Người nói?]** [nghe không rõ 00:53:45; cần đối chiếu] Em biết anh ấy là người thích em

<a id="S00437"></a>
**[00:53:47 → 00:53:49] [Người nói?]** [nghe không rõ 00:53:47; cần đối chiếu] Nhưng anh ấy nằm lật người anh không phải là thông cá chấp

<a id="S00438"></a>
**[00:53:50 → 00:53:51] [Người nói?]** [nghe không rõ 00:53:50; cần đối chiếu] Em uống khô, xe đi

<a id="S00439"></a>
**[00:53:51 → 00:53:53] [Người nói?]** [nghe không rõ 00:53:51; cần đối chiếu] Có ai

<a id="S00440"></a>
**[00:53:54 → 00:53:55] [Người nói?]** [nghe không rõ 00:53:54; cần đối chiếu] Anh không trách đâu

<a id="S00441"></a>
**[00:53:59 → 00:54:24] [Người nói?]** [nghe không rõ 00:53:59; cần đối chiếu] Các bạn hãy đăng ký kênh để ủng hộ kênh của mình nhé.

<a id="S00442"></a>
**[00:54:27 → 00:54:38] [Người nói?]** [nghe không rõ 00:54:27; cần đối chiếu] Có các điều kiện như bài hỏi, chính trị đi học, chính trị học hành, chính trị giấu lời, công nghệ, đồng hợp học hành.

<a id="S00443"></a>
**[00:54:39 → 00:54:44] [Người nói?]** [nghe không rõ 00:54:39; cần đối chiếu] Em ơi, bên anh có được đơn chuyển đối số không?

<a id="S00444"></a>
**[00:54:45 → 00:54:46] [Người nói?]** [nghe không rõ 00:54:45; cần đối chiếu] Bên anh có được gì?

<a id="S00445"></a>
**[00:54:46 → 00:54:48] [Người nói?]** [nghe không rõ 00:54:46; cần đối chiếu] Bên anh có được trọng 1 trọng 2.

<a id="S00446"></a>
**[00:54:49 → 00:54:51] [Người nói?]** [nghe không rõ 00:54:49; cần đối chiếu] À thế ạ, bên anh mình có được trọng 1 trọng 2.

<a id="S00447"></a>
**[00:54:52 → 00:54:58] [Người nói?]** [nghe không rõ 00:54:52; cần đối chiếu] Nhưng mà nhiều nơi được trọng 2, bên tổng đồng hành, cả truyền đồng số, cả truyền đồng hành.

<a id="S00448"></a>
**[00:55:11 → 00:55:24] [Người nói?]** [nghe không rõ 00:55:11; cần đối chiếu] Các bạn hãy đăng ký kênh để ủng hộ kênh của mình nhé.

<a id="S00449"></a>
**[00:55:32 → 00:56:00] [Người nói?]** [nghe không rõ 00:55:32; cần đối chiếu] Hãy subscribe cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

<a id="S00450"></a>
**[00:56:07 → 00:56:30] [Người nói?]** [nghe không rõ 00:56:07; cần đối chiếu] Hãy subscribe cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

<a id="S00451"></a>
**[00:56:32 → 00:56:35] [Người nói?]** [nghe không rõ 00:56:32; cần đối chiếu] Trắng tay thì 5 triệu chưa tới tay, hôm nay 5 triệu cũng rồi.

<a id="S00452"></a>
**[00:56:36 → 00:56:37] [Người nói?]** [nghe không rõ 00:56:36; cần đối chiếu] Thế hả, thật kỳ.

<a id="S00453"></a>
**[00:56:39 → 00:56:42] [Người nói?]** [nghe không rõ 00:56:39; cần đối chiếu] Thế anh nói bên kia của mình không được lực lượng an ninh mạng chuyên sách hả?

<a id="S00454"></a>
**[00:56:43 → 00:56:44] [Người nói?]** [nghe không rõ 00:56:43; cần đối chiếu] Không.

<a id="S00455"></a>
**[00:56:44 → 00:56:45] [Người nói?]** [nghe không rõ 00:56:44; cần đối chiếu] Không đọc trong luật hả?

<a id="S00456"></a>
**[00:56:45 → 00:56:50] [Người nói?]** [nghe không rõ 00:56:45; cần đối chiếu] Luật an ninh mạng là lực lượng chuyên sách, an ninh mạng là thuộc bộ quan của công phòng.

<a id="S00457"></a>
**[00:56:51 → 00:56:53] [Người nói?]** [nghe không rõ 00:56:51; cần đối chiếu] Sao anh phải đề xuất tên bộ quan kia của mình vậy?

<a id="S00458"></a>
**[00:56:53 → 00:56:55] [Người nói?]** [nghe không rõ 00:56:53; cần đối chiếu] Không được thì còn ai được?

<a id="S00459"></a>
**[00:56:55 → 00:56:56] [Người nói?]** [nghe không rõ 00:56:55; cần đối chiếu] Không gì được.

<a id="S00460"></a>
**[00:56:57 → 00:56:58] [Người nói?]** [nghe không rõ 00:56:57; cần đối chiếu] Từ lời của Tùng thôi.

<a id="S00461"></a>
**[00:56:58 → 00:56:59] [Người nói?]** [nghe không rõ 00:56:58; cần đối chiếu] Tùng được chưa?

<a id="S00462"></a>
**[00:56:59 → 00:57:00] [Người nói?]** [nghe không rõ 00:56:59; cần đối chiếu] Không.

<a id="S00463"></a>
**[00:57:02 → 00:57:06] [Người nói?]** [nghe không rõ 00:57:02; cần đối chiếu] 300% thì có 1 người là tỉnh, nhà nước ngoài đấy

<a id="S00464"></a>
**[00:57:07 → 00:57:09] [Người nói?]** [nghe không rõ 00:57:07; cần đối chiếu] mà không ai đòi

<a id="S00465"></a>
**[00:57:10 → 00:57:11] [Người nói?]** [nghe không rõ 00:57:10; cần đối chiếu] không ai đòi

<a id="S00466"></a>
**[00:57:13 → 00:57:15] [Người nói?]** [nghe không rõ 00:57:13; cần đối chiếu] tỉnh chưa tới tay thì xin chào

<a id="S00467"></a>
**[00:57:15 → 00:57:21] [Người nói?]** [nghe không rõ 00:57:15; cần đối chiếu] xong rồi Tùng lại làm lực lượng ra khải đảo

<a id="S00468"></a>
**[00:57:21 → 00:57:31] [Người nói?]** [nghe không rõ 00:57:21; cần đối chiếu] mình mới nói là về kẻ mạnh

<a id="S00469"></a>
**[00:57:31 → 00:57:34] [Người nói?]** [nghe không rõ 00:57:31; cần đối chiếu] kẻ mạnh đây là ví dụ ngành giáo dục ấy

<a id="S00470"></a>
**[00:57:35 → 00:57:37] [Người nói?]** [nghe không rõ 00:57:35; cần đối chiếu] ngành giáo dục bao nhiêu năm, bao nhiêu đời nay

<a id="S00471"></a>
**[00:57:37 → 00:57:40] [Người nói?]** [nghe không rõ 00:57:37; cần đối chiếu] cứ kêu gọi mát lửa đúng không

<a id="S00472"></a>
**[00:57:55 → 00:58:05] [Người nói?]** [nghe không rõ 00:57:55; cần đối chiếu] Hãy subscribe cho kênh Ghiền Mì Gõ Để không bỏ lỡ những video hấp dẫn

<a id="S00473"></a>
**[00:58:37 → 00:58:38] [Người nói?]** [nghe không rõ 00:58:37; cần đối chiếu] Chắc tỉnh giống giáo hội

<a id="S00474"></a>
**[00:58:38 → 00:58:39] [Người nói?]** [nghe không rõ 00:58:38; cần đối chiếu] Ừ

<a id="S00475"></a>
**[00:58:39 → 00:58:43] [Người nói?]** [nghe không rõ 00:58:39; cần đối chiếu] Nhưng mà hai cái cũng y đôi với nhau đấy

<a id="S00476"></a>
**[00:58:43 → 00:58:49] [Người nói?]** [nghe không rõ 00:58:43; cần đối chiếu] Rồi mấy ông nghỉ một bầy cám rồi lại nôi ra xóa lại

<a id="S00477"></a>
**[00:58:49 → 00:58:51] [Người nói?]** [nghe không rõ 00:58:49; cần đối chiếu] Một loạt phân thây

<a id="S00478"></a>
**[00:58:51 → 00:58:57] [Người nói?]** [nghe không rõ 00:58:51; cần đối chiếu] Mà người nhà đôi mà

<a id="S00479"></a>
**[00:58:57 → 00:59:00] [Người nói?]** [nghe không rõ 00:58:57; cần đối chiếu] Mua nhà mà xé hết rồi thì tự nhiên

<a id="S00480"></a>
**[00:59:00 → 00:59:02] [Người nói?]** [nghe không rõ 00:59:00; cần đối chiếu] Thế không thì cũng trả bây giờ nhỉ, đúng không ạ?

<a id="S00481"></a>
**[00:59:03 → 00:59:04] [Người nói?]** [nghe không rõ 00:59:03; cần đối chiếu] Trả được trả được

<a id="S00482"></a>
**[00:59:04 → 00:59:06] [Người nói?]** [nghe không rõ 00:59:04; cần đối chiếu] Không trả, không trả làm gì được đâu

<a id="S00483"></a>
**[00:59:07 → 00:59:09] [Người nói?]** [nghe không rõ 00:59:07; cần đối chiếu] Không trả, không trả chứ

<a id="S00484"></a>
**[00:59:09 → 00:59:12] [Người nói?]** [nghe không rõ 00:59:09; cần đối chiếu] Ông đã sai phạm, ông đã sai phạm rồi

<a id="S00485"></a>
**[00:59:12 → 00:59:14] [Người nói?]** [nghe không rõ 00:59:12; cần đối chiếu] Bây giờ ông không trả là chết

<a id="S00486"></a>
**[00:59:15 → 00:59:21] [Người nói?]** [nghe không rõ 00:59:15; cần đối chiếu] Ông ấy cũng sai, ông sẽ được nghỉ hưu. Sai là ông giải quyết cho ông ta sai.

<a id="S00487"></a>
**[00:59:22 → 00:59:27] [Người nói?]** [nghe không rõ 00:59:22; cần đối chiếu] Thế nhưng mà về tài chính, chỉ đã làm sai thì phải trả.

<a id="S00488"></a>
**[00:59:27 → 00:59:33] [Người nói?]** [nghe không rõ 00:59:27; cần đối chiếu] Quy tắc tài chính đó là có mục tiêu mà trả, nó cũng trả mà đi nợ.

<a id="S00489"></a>
**[00:59:34 → 00:59:37] [Người nói?]** [nghe không rõ 00:59:34; cần đối chiếu] Trước lượng, trước cách lưu dân.

<a id="S00490"></a>
**[00:59:38 → 00:59:39] [Người nói?]** [nghe không rõ 00:59:38; cần đối chiếu] Thế mà cái chuyện về hưu không về hưu thì ok.

<a id="S00491"></a>
**[00:59:40 → 00:59:43] [Người nói?]** [nghe không rõ 00:59:40; cần đối chiếu] Nên người ta sẽ không quay lại nữa.

<a id="S00492"></a>
**[00:59:44 → 00:59:50] [Người nói?]** [nghe không rõ 00:59:44; cần đối chiếu] Thế nhưng mà riêng tiền ấy, một cái chi sai thì, kết quả sai thì nghĩa là tiền này nó thành sai rồi.

<a id="S00493"></a>
**[00:59:51 → 00:59:54] [Người nói?]** [nghe không rõ 00:59:51; cần đối chiếu] Ông cầm tiền ấy thì có nghĩa là tiền đấy không phải của ông.

<a id="S00494"></a>
**[00:59:56 → 00:59:57] [Người nói?]** [nghe không rõ 00:59:56; cần đối chiếu] Đấy, nó giỡn đấy.

<a id="S00495"></a>
**[00:59:57 → 01:00:00] [Người nói?]** [nghe không rõ 00:59:57; cần đối chiếu] Thế là mình đoán

<a id="S00496"></a>
**[01:00:00 → 01:00:07] [Người nói?]** [nghe không rõ 01:00:00; cần đối chiếu] là nó nhằm vào cái quần tiền đấy thôi, chứ còn vì hưu hay không hưu thì chắc là cho hưu thôi.

<a id="S00497"></a>
**[01:00:13 → 01:00:14] [Người nói?]** [nghe không rõ 01:00:13; cần đối chiếu] Như thế nó cũng hơi bất cập đấy.

<a id="S00498"></a>
**[01:00:14 → 01:00:16] [Người nói?]** [nghe không rõ 01:00:14; cần đối chiếu] Bất cập, quá bất cập.

<a id="S00499"></a>
**[01:00:16 → 01:00:22] [Người nói?]** [nghe không rõ 01:00:16; cần đối chiếu] Bởi vì là cái tiêu chí của cái 1 phần 8 đấy là không xếp được cái vị trí của họ.

<a id="S00500"></a>
**[01:00:24 → 01:00:31] [Người nói?]** [nghe không rõ 01:00:24; cần đối chiếu] Nếu mà họ vẫn còn công tác thì cái vị trí của họ sẽ là khác, mức đơn của họ sẽ là khác so với hưu.

<a id="S00501"></a>
**[01:00:32 → 01:00:35] [Người nói?]** [nghe không rõ 01:00:32; cần đối chiếu] Bây giờ mình phải bắt một cái chính trị này không?

<a id="S00502"></a>
**[01:00:37 → 01:00:40] [Người nói?]** [nghe không rõ 01:00:37; cần đối chiếu] Không phù hợp, không đúng, không ý chế.

<a id="S00503"></a>
**[01:00:41 → 01:00:42] [Người nói?]** [nghe không rõ 01:00:41; cần đối chiếu] Thôi đồ sai chứ này.

<a id="S00504"></a>
**[01:00:42 → 01:00:44] [Người nói?]** [nghe không rõ 01:00:42; cần đối chiếu] Chứ là mình thì mới quyết xảy ra đâu.

<a id="S00505"></a>
**[01:00:44 → 01:00:45] [Người nói?]** [nghe không rõ 01:00:44; cần đối chiếu] Người đó nói thì nghe cái tranh luận không?

<a id="S00506"></a>
**[01:00:46 → 01:00:47] [Người nói?]** [nghe không rõ 01:00:46; cần đối chiếu] Ông Ba nói chuyện hoàn hảo chứ gì?

<a id="S00507"></a>
**[01:00:48 → 01:00:49] [Người nói?]** [nghe không rõ 01:00:48; cần đối chiếu] Ráng nói chuyện phía một xíu.

<a id="S00508"></a>
**[01:00:52 → 01:00:53] [Người nói?]** [nghe không rõ 01:00:52; cần đối chiếu] Ráng nói chuyện phía một xíu.

<a id="S00509"></a>
**[01:00:54 → 01:00:56] [Người nói?]** [nghe không rõ 01:00:54; cần đối chiếu] Đúng bắt đầu là ông cho nó 27.

<a id="S00510"></a>
**[01:00:58 → 01:00:59] [Người nói?]** [nghe không rõ 01:00:58; cần đối chiếu] Thế ông giải thích như thế này.

<a id="S00511"></a>
**[01:00:59 → 01:01:04] [Người nói?]** [nghe không rõ 01:00:59; cần đối chiếu] Đấy là cái hôm nay này nó đúng là khó nhận ra.

<a id="S00512"></a>
**[01:01:04 → 01:01:08] [Người nói?]** [nghe không rõ 01:01:04; cần đối chiếu] Nhưng mà vừa nhận được anh Vĩ khó khổ rồi.

<a id="S00513"></a>
**[01:01:09 → 01:01:09] [Người nói?]** [nghe không rõ 01:01:09; cần đối chiếu] Áp cái sống.

<a id="S00514"></a>
**[01:01:11 → 01:01:12] [Người nói?]** [nghe không rõ 01:01:11; cần đối chiếu] Bình thường nó không về.

<a id="S00515"></a>
**[01:01:12 → 01:01:13] [Người nói?]** [nghe không rõ 01:01:12; cần đối chiếu] Nếu không cầm nhiều tiền về quá.

<a id="S00516"></a>
**[01:01:14 → 01:01:16] [Người nói?]** [nghe không rõ 01:01:14; cần đối chiếu] Nên là nó phải hỏi lại.

<a id="S00517"></a>
**[01:01:17 → 01:01:18] [Người nói?]** [nghe không rõ 01:01:17; cần đối chiếu] Nếu chỉ về hư không.

<a id="S00518"></a>
**[01:01:18 → 01:01:19] [Người nói?]** [nghe không rõ 01:01:18; cần đối chiếu] Sẽ không ai hỏi.

<a id="S00519"></a>
**[01:01:20 → 01:01:23] [Người nói?]** [nghe không rõ 01:01:20; cần đối chiếu] Nhưng vì vừa được hư vừa cầm được khoản tiền to về.

<a id="S00520"></a>
**[01:01:24 → 01:01:24] [Người nói?]** [nghe không rõ 01:01:24; cần đối chiếu] Mấy tỷ.

<a id="S00521"></a>
**[01:01:24 → 01:01:26] [Người nói?]** [nghe không rõ 01:01:24; cần đối chiếu] Mười ba bốn tỷ như thế.

<a id="S00522"></a>
**[01:01:26 → 01:01:28] [Người nói?]** [nghe không rõ 01:01:26; cần đối chiếu] Hai ba bốn tỷ đấy.

<a id="S00523"></a>
**[01:01:28 → 01:01:29] [Người nói?]** [nghe không rõ 01:01:28; cần đối chiếu] Ba tỷ.

<a id="S00524"></a>
**[01:01:29 → 01:01:30] [Người nói?]** [nghe không rõ 01:01:29; cần đối chiếu] Ba tỷ.

<a id="S00525"></a>
**[01:01:31 → 01:01:32] [Người nói?]** [nghe không rõ 01:01:31; cần đối chiếu] Nếu hơn ba tỷ.

<a id="S00526"></a>
**[01:01:35 → 01:01:35] [Người nói?]** [nghe không rõ 01:01:35; cần đối chiếu] Cấp mà cấp to.

<a id="S00527"></a>
**[01:01:35 → 01:01:40] [Người nói?]** [nghe không rõ 01:01:35; cần đối chiếu] Như là chỗ em, anh chồng, bà chị, sớm ba thủy ra đây.

<a id="S00528"></a>
**[01:01:41 → 01:01:43] [Người nói?]** [nghe không rõ 01:01:41; cần đối chiếu] Thế là gần như cao nhất.

<a id="S00529"></a>
**[01:01:43 → 01:01:45] [Người nói?]** [nghe không rõ 01:01:43; cần đối chiếu] Nhưng bộ phòng là không sao, bộ phòng là làm đúng.

<a id="S00530"></a>
**[01:01:46 → 01:01:49] [Người nói?]** [nghe không rõ 01:01:46; cần đối chiếu] Chỉ có mấy bộ, bốn bộ ở ngoài, mấy tỉnh, tạm bốn đây.

<a id="S00531"></a>
**[01:01:51 → 01:02:02] [Người nói?]** [nghe không rõ 01:01:51; cần đối chiếu] Xưa mình thấy là cái giai đoạn mà chúng ta bắt ký bác làm,

<a id="S00532"></a>
**[01:02:02 → 01:02:05] [Người nói?]** [nghe không rõ 01:02:02; cần đối chiếu] tức là bác bắt ký bác làm thì người nghĩ cũng nguy hiểm.

<a id="S00533"></a>
**[01:02:06 → 01:02:07] [Người nói?]** [nghe không rõ 01:02:06; cần đối chiếu] Thế bác nghỉ rồi thì ai đỡ nhỉ?

<a id="S00534"></a>
**[01:02:08 → 01:02:10] [Người nói?]** [nghe không rõ 01:02:08; cần đối chiếu] Sơn Văn Long Thành là một trong những ví dụ.

<a id="S00535"></a>
**[01:02:16 → 01:02:23] [Người nói?]** [nghe không rõ 01:02:16; cần đối chiếu] Hầu kiện sợ, toàn hầu kiện, đúng sai, đúng mong manh.

<a id="S00536"></a>
**[01:02:26 → 01:02:31] [Người nói?]** [nghe không rõ 01:02:26; cần đối chiếu] Thời điểm đấy phải làm thì nó mới làm được.

<a id="S00537"></a>
**[01:02:33 → 01:02:36] [Người nói?]** [nghe không rõ 01:02:33; cần đối chiếu] Chứ nếu nó không làm thì thời điểm này khó để ra giải đáp.

<a id="S00538"></a>
**[01:02:38 → 01:02:41] [Người nói?]** [nghe không rõ 01:02:38; cần đối chiếu] Người ta biết là sai nhưng vẫn sẵn phải làm.

<a id="S00539"></a>
**[01:02:46 → 01:02:46] [Người nói?]** [nghe không rõ 01:02:46; cần đối chiếu] Nhưng họ...

<a id="S00540"></a>
**[01:02:48 → 01:02:50] [Người nói?]** [nghe không rõ 01:02:48; cần đối chiếu] Đó là tiền vẫn mất.

<a id="S00541"></a>
**[01:02:50 → 01:02:52] [Người nói?]** [nghe không rõ 01:02:50; cần đối chiếu] Thằng muốn cho nghỉ thì nó sẽ nghỉ.

<a id="S00542"></a>
**[01:02:52 → 01:02:55] [Người nói?]** [nghe không rõ 01:02:52; cần đối chiếu] Còn cái thằng không muốn cho nghỉ thì nó lại...

<a id="S00543"></a>
**[01:02:55 → 01:02:56] [Người nói?]** [nghe không rõ 01:02:55; cần đối chiếu] Rau như thế đấy.

<a id="S00544"></a>
**[01:02:56 → 01:02:59] [Người nói?]** [nghe không rõ 01:02:56; cần đối chiếu] Anh Sơn là một tình hình.

<a id="S00545"></a>
**[01:02:59 → 01:03:05] [Người nói?]** [nghe không rõ 01:02:59; cần đối chiếu] Anh Sơn nói rằng là nếu bình thường anh Sơn mất phải làm thì nói chung chuyên môn vẫn tốt.

<a id="S00546"></a>
**[01:03:07 → 01:03:13] [Người nói?]** [nghe không rõ 01:03:07; cần đối chiếu] Trong đó cái thằng mà nó chả chuyên môn gì cả thì nó mất các bộ rồi.

<a id="S00547"></a>
**[01:03:13 → 01:03:17] [Người nói?]** [nghe không rõ 01:03:13; cần đối chiếu] Tức là gắn bộ là chuyên môn tốt là nó mất.

<a id="S00548"></a>
**[01:03:17 → 01:03:21] [Người nói?]** [nghe không rõ 01:03:17; cần đối chiếu] Các bộ chỉ huyên trong ngành ở ngoài các bộ khác mình mất nhiều.

<a id="S00549"></a>
**[01:03:23 → 01:03:25] [Người nói?]** [nghe không rõ 01:03:23; cần đối chiếu] Nhiều người người ta dọn người ta suy nghĩ.

<a id="S00550"></a>
**[01:03:32 → 01:03:36] [Người nói?]** [nghe không rõ 01:03:32; cần đối chiếu] Bài toán về quản lý là một cái bài toán rất lớn.

<a id="S00551"></a>
**[01:03:36 → 01:03:39] [Người nói?]** [nghe không rõ 01:03:36; cần đối chiếu] Nói chung là phải dành nhiều cái.

<a id="S00552"></a>
**[01:03:39 → 01:04:12] [Người nói?]** [nghe không rõ 01:03:39; cần đối chiếu] Hãy đăng ký kênh để ủng hộ kênh của mình nhé!

## Góc nhìn về đội ngũ khi sắp xếp đơn vị

<a id="S00553"></a>
**[01:04:14 → 01:04:18] [Người nói?]** Tuy nhiên bài toán về nhân sự cũng là một vấn đề

<a id="S00554"></a>
**[01:04:18 → 01:04:21] [Người nói?]** Vì khi mà ghép với hai nơi thì nó sẽ là ghép thêm ngành

<a id="S00555"></a>
**[01:04:21 → 01:04:23] [Người nói?]** Ngoài ghép đơn vị nhưng mà có ngành nữa

<a id="S00556"></a>
**[01:04:23 → 01:04:28] [Người nói?]** [nghe không rõ 01:04:23; cần đối chiếu] Thì nó dân lê câu chuyện là cái chuẩn của duy trì ngành

<a id="S00557"></a>
**[01:04:28 → 01:04:29] [Người nói?]** [nghe không rõ 01:04:28; cần đối chiếu] Thì phải bắt buộc mà phải đạt được

<a id="S00558"></a>
**[01:04:29 → 01:04:31] [Người nói?]** Nhưng mà nó rất khó trong việc đội ngũ

<a id="S00559"></a>
**[01:04:31 → 01:04:34] [Người nói?]** Thì đấy là một cái vấn đề

<a id="S00560"></a>
**[01:04:34 → 01:04:36] [Người nói?]** Có rất nhiều vấn đề khác nữa cơ

<a id="S00561"></a>
**[01:04:36 → 01:04:41] [Người nói?]** Nhưng mà em nghĩ là mỗi thời mỗi thế

<a id="S00562"></a>
**[01:04:42 → 01:04:50] [Người nói?]** Đều phải nhìn nhận và xem các lãnh đạo có tài hoặc khéo để xử lý và duy trì và sử dụng nhân lực như thế nào

<a id="S00563"></a>
**[01:04:52 → 01:04:54] [Người nói?]** Cũng giống như là thầy hay mọi người vừa nói

<a id="S00564"></a>
**[01:04:54 → 01:04:58] [Người nói?]** Tức là mình không thể nói trước được hôm nay có thể mình làm đúng, nói đúng như thế này

<a id="S00565"></a>
**[01:04:58 → 01:05:00] [Người nói?]** Nhưng mà sau một thời kỳ khác, nó lại là câu chuyện khác

<a id="S00566"></a>
**[01:05:00 → 01:05:08] [Người nói?]** Câu chuyện là mình có đủ nhìn nhận ra là mình vai trò, vị trí của mình lúc này thế nào, bức tranh toàn cục thế nào

<a id="S00567"></a>
**[01:05:08 → 01:05:20] [Người nói?]** [nghe không rõ 01:05:08; cần đối chiếu] Nó lại là một câu chuyện mà phải đòi hỏi một cái tư duy của những người ấy là nó đủ một tầm thôi thôi

## Trò chuyện bên lề — các phát biểu chưa xác minh

<a id="S00568"></a>
**[01:05:20 → 01:05:25] [Người nói?]** [nghe không rõ 01:05:20; cần đối chiếu] Đáng đình giá cho tới những ai nghỉ hưu, mình cũng đang nghĩ nghỉ hưu về là phải Youtuber thôi

<a id="S00569"></a>
**[01:05:25 → 01:05:26] [Người nói?]** [nghe không rõ 01:05:25; cần đối chiếu] Ôi thầy

<a id="S00570"></a>
**[01:05:26 → 01:05:29] [Người nói?]** [nghe không rõ 01:05:26; cần đối chiếu] Nhưng mà làm ảnh thì Youtuber vì giặt mặt mình quá

<a id="S00571"></a>
**[01:05:31 → 01:05:32] [Người nói?]** [nghe không rõ 01:05:31; cần đối chiếu] Thầy

<a id="S00572"></a>
**[01:05:34 → 01:05:35] [Người nói?]** [nghe không rõ 01:05:34; cần đối chiếu] Ăn cũng đau mà, quay ăn cũng đau mà

<a id="S00573"></a>
**[01:05:35 → 01:05:35] [Người nói?]** [nghe không rõ 01:05:35; cần đối chiếu] Thầy

<a id="S00574"></a>
**[01:05:37 → 01:05:38] [Người nói?]** [nghe không rõ 01:05:37; cần đối chiếu] Tới vừa, quay nửa

<a id="S00575"></a>
**[01:05:38 → 01:05:39] [Người nói?]** [nghe không rõ 01:05:38; cần đối chiếu] Nói chuyện xuyên

<a id="S00576"></a>
**[01:05:39 → 01:05:40] [Người nói?]** [nghe không rõ 01:05:39; cần đối chiếu] Vậy hả

<a id="S00577"></a>
**[01:05:40 → 01:05:41] [Người nói?]** [nghe không rõ 01:05:40; cần đối chiếu] Vẫn mấy cái thằng dầu mặt

<a id="S00578"></a>
**[01:05:41 → 01:05:49] [Người nói?]** [nghe không rõ 01:05:41; cần đối chiếu] Cái đấy thực ra bản chất em nghĩ là nó thu lợi của YouTube quá nhiều mà nó lại lọt vào ngân sách nhà nước nhiều quá.

<a id="S00579"></a>
**[01:05:50 → 01:05:57] [Người nói?]** [nghe không rõ 01:05:50; cần đối chiếu] Đâm ra là bắt đầu nó mới bằng vì lợi cá nhân nhiều mà nhà nước không được hưởng lợi thì đấy thôi.

<a id="S00580"></a>
**[01:05:57 → 01:06:00] [Người nói?]** [nghe không rõ 01:05:57; cần đối chiếu] Những người đầu trò đánh điển hình thôi.

<a id="S00581"></a>
**[01:06:00 → 01:06:03] [Người nói?]** [nghe không rõ 01:06:00; cần đối chiếu] Chứ còn sẽ rất nhiều người...

<a id="S00582"></a>
**[01:06:03 → 01:06:07] [Người nói?]** [nghe không rõ 01:06:03; cần đối chiếu] Tôi thấy là nước nước mình hay là có một giai đoạn là để trưng quán, trưng quán là không hút đoạn đâu.

<a id="S00583"></a>
**[01:06:08 → 01:06:10] [Người nói?]** [nghe không rõ 01:06:08; cần đối chiếu] Thì có một giai đoạn là nó cũng làm ăn tốt, hoặc là không tốt.

<a id="S00584"></a>
**[01:06:10 → 01:06:13] [Người nói?]** [nghe không rõ 01:06:10; cần đối chiếu] sau đến lúc nhà nước bắt bổ loạn thì bắt đầu hữu dụng

<a id="S00585"></a>
**[01:06:13 → 01:06:17] [Người nói?]** [nghe không rõ 01:06:13; cần đối chiếu] Vì YouTuber cũng thế, lần này khác làm nhiều ổn định hơn

<a id="S00586"></a>
**[01:06:17 → 01:06:18] [Người nói?]** [nghe không rõ 01:06:17; cần đối chiếu] Vâng

<a id="S00587"></a>
**[01:06:21 → 01:06:27] [Người nói?]** [nghe không rõ 01:06:21; cần đối chiếu] Phải thế thôi Thầy, năm 2020, 2019 toàn mấy cái ảnh hưởng xấu dưới trẻ

<a id="S00588"></a>
**[01:06:29 → 01:06:32] [Người nói?]** [nghe không rõ 01:06:29; cần đối chiếu] Mỗi cái xấu thôi, nhưng mà đi làm ăn đi, làm ăn là xuống thuế thôi

<a id="S00589"></a>
**[01:06:32 → 01:06:34] [Người nói?]** [nghe không rõ 01:06:32; cần đối chiếu] Thứ này là dễ ợt, thế là không xuống được

<a id="S00590"></a>
**[01:06:35 → 01:06:40] [Người nói?]** [nghe không rõ 01:06:35; cần đối chiếu] Như là Youtube hoặc là các cái doanh nghiệp Mỹ lại không có những chi nhánh ở Việt Nam

<a id="S00591"></a>
**[01:06:40 → 01:06:44] [Người nói?]** [nghe không rõ 01:06:40; cần đối chiếu] nên không phải đóng thuế quá nhiều mới phải làm.

<a id="S00592"></a>
**[01:06:44 → 01:06:51] [Người nói?]** [nghe không rõ 01:06:44; cần đối chiếu] Mình nhớ thằng tên đó là Hải Sapa, thịt châu Ấn Độ.

<a id="S00593"></a>
**[01:06:53 → 01:06:55] [Người nói?]** [nghe không rõ 01:06:53; cần đối chiếu] Nếu so với thằng kia thì nó bình thường thôi nhỉ?

<a id="S00594"></a>
**[01:06:55 → 01:06:58] [Người nói?]** [nghe không rõ 01:06:55; cần đối chiếu] Nó không quá lây dưỡng, chắc nó còn hư lậu không?

<a id="S00595"></a>
**[01:06:59 → 01:07:00] [Người nói?]** [nghe không rõ 01:06:59; cần đối chiếu] Hải Sapa, Hải Sapa.

<a id="S00596"></a>
**[01:07:00 → 01:07:02] [Người nói?]** [nghe không rõ 01:07:00; cần đối chiếu] Nó chắc là mùi cội gì cả.

<a id="S00597"></a>
**[01:07:03 → 01:07:06] [Người nói?]** [nghe không rõ 01:07:03; cần đối chiếu] Nhưng mà thuế của Hải Sapa là nhiều nhất.

<a id="S00598"></a>
**[01:07:06 → 01:07:09] [Người nói?]** [nghe không rõ 01:07:06; cần đối chiếu] Em thấy một bài viết nói một tổng thể của Hải Sapa

<a id="S00599"></a>
**[01:07:12 → 01:07:25] [Người nói?]** [nghe không rõ 01:07:12; cần đối chiếu] Đầu tiên là chỉ lái xe du lịch, sau đó là qua các liên lạc về mặt truyền thông thì bắt đầu mới làm ITUBI

<a id="S00600"></a>
**[01:07:25 → 01:07:31] [Người nói?]** [nghe không rõ 01:07:25; cần đối chiếu] ITUBI sau bắt đầu mới quen đội Huấn Hoa Hồng rồi là Phú Lê lập đội anh em Kết Nghĩa Vườn Đào

<a id="S00601"></a>
**[01:07:31 → 01:07:34] [Người nói?]** [nghe không rõ 01:07:31; cần đối chiếu] thì bắt đầu là cái mảng làm cái mảng đấy

<a id="S00602"></a>
**[01:07:35 → 01:07:37] [Người nói?]** [nghe không rõ 01:07:35; cần đối chiếu] và cộng với cái đội của cái mảng của Hoàng Phú Lê

<a id="S00603"></a>
**[01:07:37 → 01:07:39] [Người nói?]** [nghe không rõ 01:07:37; cần đối chiếu] cái thứ là làm cái YouTube

<a id="S00604"></a>
**[01:07:40 → 01:07:45] [Người nói?]** [nghe không rõ 01:07:40; cần đối chiếu] nhưng mà bản chất của YouTube đấy lại kết hợp nhau là làm các cái bán kinh doanh ở trong nữa

<a id="S00605"></a>
**[01:07:45 → 01:07:50] [Người nói?]** [nghe không rõ 01:07:45; cần đối chiếu] và trong đấy thì một trong những cái việc ấy là đó chính là quảng bá các cái sản phẩm trong đó là có cái thịt trâu

<a id="S00606"></a>
**[01:07:51 → 01:07:56] [Người nói?]** [nghe không rõ 01:07:51; cần đối chiếu] ngoài ra thì có rất nhiều những cái quảng bá đương nhiên là làm YouTube nói các quảng bá thì đúng sự thật

<a id="S00607"></a>
**[01:07:57 → 01:07:59] [Người nói?]** [nghe không rõ 01:07:57; cần đối chiếu] Mình nói là thịt châu chỉ là lý do thôi

<a id="S00608"></a>
**[01:08:00 → 01:08:02] [Người nói?]** [nghe không rõ 01:08:00; cần đối chiếu] Chỉ là một cái lý do

<a id="S00609"></a>
**[01:08:03 → 01:08:07] [Người nói?]** [nghe không rõ 01:08:03; cần đối chiếu] Mình biết lịch sử là nó chơi thằng Huấn với thằng Phú Lê

<a id="S00610"></a>
**[01:08:08 → 01:08:09] [Người nói?]** [nghe không rõ 01:08:08; cần đối chiếu] Thằng nữa đấy

<a id="S00611"></a>
**[01:08:09 → 01:08:10] [Người nói?]** [nghe không rõ 01:08:09; cần đối chiếu] Vì 3 thằng khác nhau

<a id="S00612"></a>
**[01:08:11 → 01:08:15] [Người nói?]** [nghe không rõ 01:08:11; cần đối chiếu] Nhưng mà 2 thằng kia theo đường sâu đen thì thằng Hải Thái Quang tách ra

<a id="S00613"></a>
**[01:08:16 → 01:08:19] [Người nói?]** [nghe không rõ 01:08:16; cần đối chiếu] Thằng Hải Thái Quang thì về mặt sâu đen là nó đớn nhất trong 3 thằng đấy

<a id="S00614"></a>
**[01:08:20 → 01:08:24] [Người nói?]** [nghe không rõ 01:08:20; cần đối chiếu] Nhưng mà chắc nó còn một số thứ còn nhầm

<a id="S00615"></a>
**[01:08:25 → 01:08:30] [Người nói?]** [nghe không rõ 01:08:25; cần đối chiếu] Nhưng mà thịt châu Bắc Bếp là một trong những tùy nhấn, tùy lớn

<a id="S00616"></a>
**[01:08:30 → 01:08:34] [Người nói?]** [nghe không rõ 01:08:30; cần đối chiếu] Tùy lớn, bây giờ nếu mà tính qua 30 tỷ là nó là tùy to

<a id="S00617"></a>
**[01:08:36 → 01:08:41] [Người nói?]** [nghe không rõ 01:08:36; cần đối chiếu] Châu Ấn Độ, châu Ước Vận Ấn Độ, châu của Việt Nam làm sao nó làm được

<a id="S00618"></a>
**[01:08:41 → 01:08:49] [Người nói?]** [nghe không rõ 01:08:41; cần đối chiếu] Với lại cả 3 cái đội đấy đều là quyên có tiền tài trợ rất nhiều, lấy tiền tài trợ đấy nhưng mà tiền tài trợ rất nhiều

<a id="S00619"></a>
**[01:08:49 → 01:08:52] [Người nói?]** [nghe không rõ 01:08:49; cần đối chiếu] Nhưng mà thực ra là tất cả các tiền tài trợ của các đơn vị ấy mà lấy

<a id="S00620"></a>
**[01:08:54 → 01:09:00] [Người nói?]** [nghe không rõ 01:08:54; cần đối chiếu] Mình thì không phải xin tội, doanh nghiệp về văn hóa thì xin tội, nếu mà đúng không phải xin tội

<a id="S00621"></a>
**[01:09:00 → 01:09:06] [Người nói?]** [nghe không rõ 01:09:00; cần đối chiếu] Đúng rồi, không sai cái này thì không sai cái này

<a id="S00622"></a>
**[01:09:07 → 01:09:17] [Người nói?]** [nghe không rõ 01:09:07; cần đối chiếu] Hôm nay có một bài báo của một cầu giám đốc của công ty về tòa thuế của Đà Nẵng

<a id="S00623"></a>
**[01:09:17 → 01:09:26] [Người nói?]** [nghe không rõ 01:09:17; cần đối chiếu] Đưa lên rằng là thân lập dân nghiệp thì được mận 2 triệu, nhưng mà giải thể dân nghiệp thì mận gần 2 tất triệu.

<a id="S00624"></a>
**[01:09:26 → 01:09:28] [Người nói?]** [nghe không rõ 01:09:26; cần đối chiếu] Nghĩa là giải thể quá khó.

<a id="S00625"></a>
**[01:09:28 → 01:09:31] [Người nói?]** [nghe không rõ 01:09:28; cần đối chiếu] Thầy, anh xin các đồng chí ký viết vào xe.

<a id="S00626"></a>
**[01:09:33 → 01:09:35] [Người nói?]** [nghe không rõ 01:09:33; cần đối chiếu] Vâng, em sẽ trả lời cho tuyến nhé.

<a id="S00627"></a>
**[01:09:36 → 01:09:38] [Người nói?]** [nghe không rõ 01:09:36; cần đối chiếu] Dạ vâng, em sẽ trả lời cho tuyến nhé.

<a id="S00628"></a>
**[01:09:38 → 01:09:39] [Người nói?]** [nghe không rõ 01:09:38; cần đối chiếu] Thân lập dân nghiệp thì gì anh ạ?

<a id="S00629"></a>
**[01:09:39 → 01:09:41] [Người nói?]** [nghe không rõ 01:09:39; cần đối chiếu] Thân lập giải thể khó lắm.

<a id="S00630"></a>
**[01:09:41 → 01:09:41] [Người nói?]** [nghe không rõ 01:09:41; cần đối chiếu] Dạ, thưa thầy.

<a id="S00631"></a>
**[01:09:41 → 01:09:42] [Người nói?]** [nghe không rõ 01:09:41; cần đối chiếu] Cảm ơn thầy.

<a id="S00632"></a>
**[01:09:48 → 01:09:54] [Người nói?]** [nghe không rõ 01:09:48; cần đối chiếu] Hãy subscribe cho kênh Ghiền Mì Gõ Để không bỏ lỡ những video hấp dẫn

<a id="S00633"></a>
**[01:10:00 → 01:10:02] [Người nói?]** [nghe không rõ 01:10:00; cần đối chiếu] Thế nên là anh chân trí lại nó cũng đáng

<a id="S00634"></a>
**[01:10:03 → 01:10:15] [Người nói?]** [nghe không rõ 01:10:03; cần đối chiếu] Làm ơn để có một kỳ xảo thì chỉ có việc là dựa cái kỳ xảo đấy thì đúng

<a id="S00635"></a>
**[01:10:15 → 01:10:19] [Người nói?]** [nghe không rõ 01:10:15; cần đối chiếu] Nếu như mà điều tra cho đúng thì nó đúng

<a id="S00636"></a>
**[01:10:19 → 01:10:21] [Người nói?]** [nghe không rõ 01:10:19; cần đối chiếu] Mà không cho đúng thì nó là sai

<a id="S00637"></a>
**[01:10:24 → 01:10:26] [Người nói?]** [nghe không rõ 01:10:24; cần đối chiếu] Ví dụ em đơn giản một cái, đơn giản như này

<a id="S00638"></a>
**[01:10:27 → 01:10:39] [Người nói?]** [nghe không rõ 01:10:27; cần đối chiếu] vô đôi là có các thứ là sửa ứng, sửa bột, sửa bột nhưng mà thực ra cả cái bột mình xay trở thành là sửa ví dụ sửa bột đầu nành này

<a id="S00639"></a>
**[01:10:39 → 01:10:46] [Người nói?]** [nghe không rõ 01:10:39; cần đối chiếu] rồi cả cái bột đầu xanh tất cả mình xay, nhưng mà đi kiểm tra lúc đó là nó đủ, thân thân là chuẩn

<a id="S00640"></a>
**[01:10:46 → 01:10:51] [Người nói?]** [nghe không rõ 01:10:46; cần đối chiếu] nhưng mà khi đưa ra bán ở ngoài cả hàng thì nhiệt độ đủ thực tiểu nó tác động vào

<a id="S00641"></a>
**[01:10:51 → 01:10:59] [Người nói?]** [nghe không rõ 01:10:51; cần đối chiếu] Khi nó giảm xuống một chút, bình thường là 5%, bây giờ chỉ có 488 thôi.

<a id="S00642"></a>
**[01:10:59 → 01:11:04] [Người nói?]** [nghe không rõ 01:10:59; cần đối chiếu] Thì sản phẩm đấy sẽ được quý vào là bộ bản hàng giảm.

<a id="S00643"></a>
**[01:11:05 → 01:11:08] [Người nói?]** [nghe không rõ 01:11:05; cần đối chiếu] Nó chỉ thấp một chút, nó sẽ trở thành bộ bản hàng giảm rồi.

<a id="S00644"></a>
**[01:11:08 → 01:11:15] [Người nói?]** [nghe không rõ 01:11:08; cần đối chiếu] Bởi vì theo cái thông số mà bạn đăng ký là nó 5%, bây giờ tự nhiên là 488 thôi.

<a id="S00645"></a>
**[01:11:16 → 01:11:20] [Người nói?]** [nghe không rõ 01:11:16; cần đối chiếu] Thay việc là tất cả mọi cái chất nó đều có sự biến đổi hết.

<a id="S00646"></a>
**[01:11:20 → 01:11:28] [Người nói?]** [nghe không rõ 01:11:20; cần đối chiếu] Như chúng ta cũng giữ trong môi trường, nó đúng, nó không đúng, do phần chuyển ra cái gì thì nó sẽ sai số

<a id="S00647"></a>
**[01:11:28 → 01:11:36] [Người nói?]** [nghe không rõ 01:11:28; cần đối chiếu] Nó sai số đưa ra là đương nhiên là quý vào thằng giả luôn, thằng giả kém chất lượng, nó nguy hiểm thế

<a id="S00648"></a>
**[01:11:37 → 01:11:45] [Người nói?]** [nghe không rõ 01:11:37; cần đối chiếu] Ngay cả cái bảng đầu sánh của Hải Dương chẳng hạn, ai dám thăng bín ra là cái tiêu chuẩn đấy nó chuẩn lắm

<a id="S00649"></a>
**[01:11:45 → 01:11:51] [Người nói?]** [nghe không rõ 01:11:45; cần đối chiếu] Khi mà đưa ra thị trường xáy rồi ép rồi thế nào đưa ra thị trường cái thân phần nó bỏ

<a id="S00650"></a>
**[01:11:51 → 01:11:53] [Người nói?]** [nghe không rõ 01:11:51; cần đối chiếu] Nó khó, nó khó chỗ đấy

<a id="S00651"></a>
**[01:11:53 → 01:11:56] [Người nói?]** [nghe không rõ 01:11:53; cần đối chiếu] Nên khi mà bọc tách ra

<a id="S00652"></a>
**[01:11:56 → 01:11:57] [Người nói?]** [nghe không rõ 01:11:56; cần đối chiếu] Là dễ lắm

<a id="S00653"></a>
**[01:11:59 → 01:11:59] [Người nói?]** [nghe không rõ 01:11:59; cần đối chiếu] Dễ lắm

<a id="S00654"></a>
**[01:12:03 → 01:12:04] [Người nói?]** [nghe không rõ 01:12:03; cần đối chiếu] Rất mong man

<a id="S00655"></a>
**[01:12:04 → 01:12:07] [Người nói?]** [nghe không rõ 01:12:04; cần đối chiếu] Kiểu như tu tung mà đi sói

<a id="S00656"></a>
**[01:12:07 → 01:12:10] [Người nói?]** [nghe không rõ 01:12:07; cần đối chiếu] Ai sói thì làm sao nó thoát được

<a id="S00657"></a>
**[01:12:11 → 01:12:15] [Người nói?]** [nghe không rõ 01:12:11; cần đối chiếu] Bản quyền

<a id="S00658"></a>
**[01:12:16 → 01:12:16] [Người nói?]** [nghe không rõ 01:12:16; cần đối chiếu] Bản quyền

<a id="S00659"></a>
**[01:12:16 → 01:12:19] [Người nói?]** [nghe không rõ 01:12:16; cần đối chiếu] Em bảo thay là bản quyền

<a id="S00660"></a>
**[01:12:19 → 01:12:21] [Người nói?]** [nghe không rõ 01:12:19; cần đối chiếu] Nó đơn giản thế này

<a id="S00661"></a>
**[01:12:21 → 01:12:23] [Người nói?]** [nghe không rõ 01:12:21; cần đối chiếu] Thực ra ở Việt Nam mình mua được bản quyền

<a id="S00662"></a>
**[01:12:23 → 01:12:25] [Người nói?]** [nghe không rõ 01:12:23; cần đối chiếu] Mua rất dễ, nhưng mà

<a id="S00663"></a>
**[01:12:25 → 01:12:27] [Người nói?]** [nghe không rõ 01:12:25; cần đối chiếu] Đầy cả cái bản quyền đầy lấy

<a id="S00664"></a>
**[01:12:27 → 01:12:28] [Người nói?]** [nghe không rõ 01:12:27; cần đối chiếu] nó sẽ trở nên rất đắt

<a id="S00665"></a>
**[01:12:28 → 01:12:31] [Người nói?]** [nghe không rõ 01:12:28; cần đối chiếu] cái máy tính bình thường thì chỉ có 12 hay 3 triệu

<a id="S00666"></a>
**[01:12:31 → 01:12:33] [Người nói?]** [nghe không rõ 01:12:31; cần đối chiếu] bây giờ thêm nữa, trở khoảng 3 triệu nữa

<a id="S00667"></a>
**[01:12:33 → 01:12:34] [Người nói?]** [nghe không rõ 01:12:33; cần đối chiếu] một cái bản quyền

<a id="S00668"></a>
**[01:12:34 → 01:12:36] [Người nói?]** [nghe không rõ 01:12:34; cần đối chiếu] bản quyền là Win, sau đó là Office nữa

<a id="S00669"></a>
**[01:12:36 → 01:12:39] [Người nói?]** [nghe không rõ 01:12:36; cần đối chiếu] Office thì nếu như Office zoom ngoài mạng

<a id="S00670"></a>
**[01:12:39 → 01:12:40] [Người nói?]** [nghe không rõ 01:12:39; cần đối chiếu] thì cũng đâu đó trở khoảng gần 4 triệu

<a id="S00671"></a>
**[01:12:40 → 01:12:43] [Người nói?]** [nghe không rõ 01:12:40; cần đối chiếu] đấy, gần 4 triệu, chưa kể

<a id="S00672"></a>
**[01:12:43 → 01:12:45] [Người nói?]** [nghe không rõ 01:12:43; cần đối chiếu] Office của Photoshop, chưa kể đến

<a id="S00673"></a>
**[01:12:45 → 01:12:47] [Người nói?]** [nghe không rõ 01:12:45; cần đối chiếu] các cái phần bên khác thì còn vào

<a id="S00674"></a>
**[01:12:47 → 01:12:49] [Người nói?]** [nghe không rõ 01:12:47; cần đối chiếu] cái máy đấy nó không phải là 13 triệu nữa

<a id="S00675"></a>
**[01:12:49 → 01:12:51] [Người nói?]** [nghe không rõ 01:12:49; cần đối chiếu] rất là lắm, thì đương nhiên là

<a id="S00676"></a>
**[01:12:51 → 01:12:53] [Người nói?]** [nghe không rõ 01:12:51; cần đối chiếu] sinh viên của mình làm sao

<a id="S00677"></a>
**[01:12:53 → 01:12:55] [Người nói?]** [nghe không rõ 01:12:53; cần đối chiếu] là cái đó, truyền truyền không tưởng

<a id="S00678"></a>
**[01:12:56 → 01:13:05] [Người nói?]** [nghe không rõ 01:12:56; cần đối chiếu] Đơn giản như thế đó. Ví dụ như nhà em, nhà em có 4 máy tính, bởi vì tất cả đều bằng bản quyền thì cái tối lương nó khủng khiếp.

<a id="S00679"></a>
**[01:13:06 → 01:13:11] [Người nói?]** [nghe không rõ 01:13:06; cần đối chiếu] Thế nên nó bây giờ đúng thì kiểm tra thì thiệt sự sai, chứ không kiểm tra nữa.

<a id="S00680"></a>
**[01:13:12 → 01:13:24] [Người nói?]** [nghe không rõ 01:13:12; cần đối chiếu] Việt Nam của mình bây giờ, em nói thầy, các trường đại học, ví dụ trường mật khoa chẳng hạn, có bao nhiêu sinh viên dùng bản quyền của photoshop, đúng không ạ?

<a id="S00681"></a>
**[01:13:26 → 01:13:33] [Người nói?]** [nghe không rõ 01:13:26; cần đối chiếu] hoặc là phần mềm AutoCAD. Những phần mềm đấy thì có AutoLib.

<a id="S00682"></a>
**[01:13:35 → 01:13:36] [Người nói?]** [nghe không rõ 01:13:35; cần đối chiếu] Đấy.

<a id="S00683"></a>
**[01:13:39 → 01:13:41] [Người nói?]** [nghe không rõ 01:13:39; cần đối chiếu] Nó phải bắt mua nguyên cả tổng Adobe.

<a id="S00684"></a>
**[01:13:41 → 01:13:44] [Người nói?]** [nghe không rõ 01:13:41; cần đối chiếu] Rồi chia kể đến các phần mềm AutoCAD, quả rất là đắt.

<a id="S00685"></a>
**[01:13:46 → 01:13:50] [Người nói?]** [nghe không rõ 01:13:46; cần đối chiếu] AutoLib, vẻ mặt điện, những phần mềm trên trường tiện ăn học đắt.

<a id="S00686"></a>
**[01:13:51 → 01:13:54] [Người nói?]** [nghe không rõ 01:13:51; cần đối chiếu] Đấy chỉ có thể tải nguồn không trình thống.

<a id="S00687"></a>
**[01:13:55 → 01:13:57] [Người nói?]** [nghe không rõ 01:13:55; cần đối chiếu] Đấy, tải nguồn không trình thống nghĩa là lỗ.

<a id="S00688"></a>
**[01:13:57 → 01:14:00] [Người nói?]** [nghe không rõ 01:13:57; cần đối chiếu] không có bằng quyền gì nữa

<a id="S00689"></a>
**[01:14:00 → 01:14:03] [Người nói?]** [nghe không rõ 01:14:00; cần đối chiếu] hoặc là ông dùng cả cái trang để crack cái gì

<a id="S00690"></a>
**[01:14:04 → 01:14:06] [Người nói?]** [nghe không rõ 01:14:04; cần đối chiếu] ông đi lọc cái gì nữa

<a id="S00691"></a>
**[01:14:08 → 01:14:10] [Người nói?]** [nghe không rõ 01:14:08; cần đối chiếu] có những vấn đề cực kỳ nát dài

<a id="S00692"></a>
**[01:14:10 → 01:14:12] [Người nói?]** [nghe không rõ 01:14:10; cần đối chiếu] đúng hay sai

<a id="S00693"></a>
**[01:14:13 → 01:14:19] [Người nói?]** [nghe không rõ 01:14:13; cần đối chiếu] công nghiệp hàng tỷ, hàng tỷ cho em đi

<a id="S00694"></a>
**[01:14:19 → 01:14:22] [Người nói?]** [nghe không rõ 01:14:19; cần đối chiếu] 20 năm cho em đi, hàng tỷ cái sai

<a id="S00695"></a>
**[01:14:22 → 01:14:24] [Người nói?]** [nghe không rõ 01:14:22; cần đối chiếu] chỉ đâu chẳng sai

<a id="S00696"></a>
**[01:14:24 → 01:14:27] [Người nói?]** [nghe không rõ 01:14:24; cần đối chiếu] vấn đề là có bắt hay không

<a id="S00697"></a>
**[01:14:27 → 01:14:30] [Người nói?]** [nghe không rõ 01:14:27; cần đối chiếu] ông muốn gì mới trả lời không?

<a id="S00698"></a>
**[01:14:31 → 01:14:33] [Người nói?]** [nghe không rõ 01:14:31; cần đối chiếu] em chưa muốn gì gì

## Quay lại bài báo và mô hình deepfake

<a id="S00699"></a>
**[01:14:33 → 01:14:41] [Người nói?]** [nghe không rõ 01:14:33; cần đối chiếu] không hướng hơn, cho nên có thể là kết hợp cả cái hướng file, giảm hướng, tempo, kế năng chạy, xong rồi.

<a id="S00700"></a>
**[01:14:42 → 01:14:45] [Người nói?]** [nghe không rõ 01:14:42; cần đối chiếu] Mình rất hy vọng bài tổng gửi này được chấp nhận.

<a id="S00701"></a>
**[01:14:46 → 01:14:48] [Người nói?]** [nghe không rõ 01:14:46; cần đối chiếu] Bài mình thấy cũng về mặt chất lượng.

<a id="S00702"></a>
**[01:14:48 → 01:14:53] [Người nói?]** [nghe không rõ 01:14:48; cần đối chiếu] Hai tuần nữa.

<a id="S00703"></a>
**[01:14:53 → 01:14:54] [Người nói?]** [nghe không rõ 01:14:53; cần đối chiếu] Nhanh nhất.

<a id="S00704"></a>
**[01:14:54 → 01:14:56] [Người nói?]** [nghe không rõ 01:14:54; cần đối chiếu] Hy vọng thế, cũng được một tuần thôi.

<a id="S00705"></a>
**[01:14:56 → 01:14:59] [Người nói?]** [nghe không rõ 01:14:56; cần đối chiếu] Phấn mới gửi cái gì đấy Phấn?

<a id="S00706"></a>
**[01:15:01 → 01:15:06] [Người nói?]** [nghe không rõ 01:15:01; cần đối chiếu] Phấn gửi bài bảo, em cũng viết thành.

<a id="S00707"></a>
**[01:15:06 → 01:15:10] [Người nói?]** [nghe không rõ 01:15:06; cần đối chiếu] Được xong rồi có gì không? Có gì đặc biệt?

<a id="S00708"></a>
**[01:15:10 → 01:15:12] [Người nói?]** [nghe không rõ 01:15:10; cần đối chiếu] Chi tiết mình sẽ đọc.

<a id="S00709"></a>
**[01:15:12 → 01:15:24] [Người nói?]** [nghe không rõ 01:15:12; cần đối chiếu] Có thể là con bơ đôi của em có cao hơn cái slide của bà Nguyễn Văn.

<a id="S00710"></a>
**[01:15:25 → 01:15:28] [Người nói?]** [nghe không rõ 01:15:25; cần đối chiếu] Chị cũng chắc là Nguyễn Văn đi nhà.

<a id="S00711"></a>
**[01:15:31 → 01:15:39] [Người nói?]** [nghe không rõ 01:15:31; cần đối chiếu] Chị cũng phải đi cùng với anh.

<a id="S00712"></a>
**[01:15:41 → 01:15:42] [Người nói?]** [nghe không rõ 01:15:41; cần đối chiếu] Thầy đi kìa.

<a id="S00713"></a>
**[01:15:43 → 01:15:57] [Người nói?]** [nghe không rõ 01:15:43; cần đối chiếu] Dạ chí mà cũng rất là đồng ý với anh.

<a id="S00714"></a>
**[01:16:16 → 01:16:48] [Người nói?]** [nghe không rõ 01:16:16; cần đối chiếu] Hãy subscribe cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

<a id="S00715"></a>
**[01:16:48 → 01:16:50] [Người nói?]** [nghe không rõ 01:16:48; cần đối chiếu] Thì nó hợp hợp với mình thôi

<a id="S00716"></a>
**[01:16:51 → 01:16:56] [Người nói?]** [nghe không rõ 01:16:51; cần đối chiếu] Còn có thể em cũng tham khảo cái template của nó

<a id="S00717"></a>
**[01:16:56 → 01:17:02] [Người nói?]** [nghe không rõ 01:16:56; cần đối chiếu] Đầu thời trong mấy cái tuần vừa qua thì em cũng thử khá là nhiều

<a id="S00718"></a>
**[01:17:02 → 01:17:06] [Người nói?]** [nghe không rõ 01:17:02; cần đối chiếu] Đó viết bản báo này

<a id="S00719"></a>
**[01:17:06 → 01:17:09] [Người nói?]** [nghe không rõ 01:17:06; cần đối chiếu] Trong bản báo này thì dự kiến là tên của bản template

<a id="S00720"></a>
**[01:17:11 → 01:17:15] [Người nói?]** [nghe không rõ 01:17:11; cần đối chiếu] Chọn form 1 with F L H A

<a id="S00721"></a>
**[01:17:15 → 01:17:17] [Người nói?]** [nghe không rõ 01:17:15; cần đối chiếu] Cái này là F A có nghĩa là

<a id="S00722"></a>
**[01:17:17 → 01:17:20] [Người nói?]** [nghe không rõ 01:17:17; cần đối chiếu] Front Level Feature Residual

<a id="S00723"></a>
**[01:17:20 → 01:17:26] [Người nói?]** [nghe không rõ 01:17:20; cần đối chiếu] And D M I H A có nghĩa là

<a id="S00724"></a>
**[01:17:26 → 01:17:29] [Người nói?]** [nghe không rõ 01:17:26; cần đối chiếu] Typical Mass Attention

<a id="S00725"></a>
**[01:17:30 → 01:17:33] [Người nói?]** [nghe không rõ 01:17:30; cần đối chiếu] Đi cái tên này là tổng viên tập có cái rối não rồi

<a id="S00726"></a>
**[01:17:33 → 01:17:36] [Người nói?]** [nghe không rõ 01:17:33; cần đối chiếu] Đúng rồi

<a id="S00727"></a>
**[01:17:38 → 01:17:41] [Người nói?]** [nghe không rõ 01:17:38; cần đối chiếu] Viên thắng lại

<a id="S00728"></a>
**[01:17:41 → 01:17:42] [Người nói?]** [nghe không rõ 01:17:41; cần đối chiếu] Bỏ viên thắng lại

<a id="S00729"></a>
**[01:17:43 → 01:17:45] [Người nói?]** [nghe không rõ 01:17:43; cần đối chiếu] Bỏ cái tên này đi

<a id="S00730"></a>
**[01:17:50 → 01:17:54] [Người nói?]** [nghe không rõ 01:17:50; cần đối chiếu] Không biết tên này chắc chắn là tổng viên tập khác nhau rồi

<a id="S00731"></a>
**[01:17:54 → 01:18:07] [Người nói?]** [nghe không rõ 01:17:54; cần đối chiếu] Em đưa cái tên này để nhấn mặn 2 cái phương pháp trong mô hình nhấn mặn hơn

<a id="S00732"></a>
**[01:18:12 → 01:18:16] [Người nói?]** [nghe không rõ 01:18:12; cần đối chiếu] Cái bài báo thì em cũng đã báo rồi

<a id="S00733"></a>
**[01:18:17 → 01:18:26] [Người nói?]** [nghe không rõ 01:18:17; cần đối chiếu] Cơ bản của mô hình tương tự như hôm trước em đã báo cáo thầy

<a id="S00734"></a>
**[01:18:27 → 01:18:31] [Người nói?]** [nghe không rõ 01:18:27; cần đối chiếu] Đầu tiên sẽ qua bước sử dụng diện

<a id="S00735"></a>
**[01:18:31 → 01:18:36] [Người nói?]** [nghe không rõ 01:18:31; cần đối chiếu] Sau đó sẽ qua backbone sử dụng Connect ID

<a id="S00736"></a>
**[01:18:36 → 01:18:40] [Người nói?]** [nghe không rõ 01:18:36; cần đối chiếu] Sau khi qua backbone Connect ID

<a id="S00737"></a>
**[01:18:40 → 01:18:47] [Người nói?]** [nghe không rõ 01:18:40; cần đối chiếu] Nó sẽ trình xuất ra các đặc trưng trong mỗi mũi frame trong video

<a id="S00738"></a>
**[01:18:48 → 01:18:49] [Người nói?]** [ASR cần nghe lại] Thật này rõ ràng rồi

<a id="S00739"></a>
**[01:18:49 → 01:18:58] [Người nói?]** [ASR cần nghe lại] Sau đó nó sẽ chiếu các frame này

<a id="S00740"></a>
**[01:18:58 → 01:19:07] [Người nói?]** Điều này gồm chiếu các cụm này để đưa qua một cái gọi là Frame Level Feature Residual

<a id="S00741"></a>
**[01:19:08 → 01:19:21] [Người nói?]** Đối với cái Frame Level Feature Residual này, mục đích chính của nó là để mà nó sẽ bắt các cái thông tin khác nhau giữa các cái frame

<a id="S00742"></a>
**[01:19:23 → 01:19:32] [Người nói?]** [nghe không rõ 01:19:23; cần đối chiếu] Nếu các bạn so sánh giữa các cái frame với nhau thì ở trong đấy nó sẽ có các cái thông tin vô địch, thông tin tính

<a id="S00743"></a>
**[01:19:32 → 01:19:37] [Người nói?]** [nghe không rõ 01:19:32; cần đối chiếu] Đối với các cái thông tin tĩnh đấy thì cái frame thứ nhất và cái frame thứ hai cũng hợp tương đổi nhau.

<a id="S00744"></a>
**[01:19:38 → 01:19:43] [Người nói?]** Ở đây thì mình sẽ chọn ra được các cái đặc trưng mà nó khác nhau,

<a id="S00745"></a>
**[01:19:43 → 01:19:46] [Người nói?]** không sử dụng các đặc trưng giống nhau lắm.

<a id="S00746"></a>
**[01:19:46 → 01:19:55] [Người nói?]** [nghe không rõ 01:19:46; cần đối chiếu] Thế thì cái tính năng này cũng gần tương tự như là đối với một cái tính năng gọi là self-subtract

<a id="S00747"></a>
**[01:19:55 → 01:20:00] [Người nói?]** [nghe không rõ 01:19:55; cần đối chiếu] ở trong cái bài báo AST của một cái team mà nó đang ở

<a id="S00748"></a>
**[01:20:00 → 01:20:01] [Người nói?]** [nghe không rõ 01:20:00; cần đối chiếu] trên cái IEA của năm 2023

<a id="S00749"></a>
**[01:20:02 → 01:20:09] [Người nói?]** [nghe không rõ 01:20:02; cần đối chiếu] cái bản đó thì nó cũng khá là được áp dụng, được khám chiếu khá nhiều

<a id="S00750"></a>
**[01:20:09 → 01:20:15] [Người nói?]** [nghe không rõ 01:20:09; cần đối chiếu] và cái bản đó thì tùy cho cái lượng chính xác của crop attention

<a id="S00751"></a>
**[01:20:16 → 01:20:23] [Người nói?]** [nghe không rõ 01:20:16; cần đối chiếu] của crop data set rơi vào 84%

<a id="S00752"></a>
**[01:20:24 → 01:20:29] [Người nói?]** [nghe không rõ 01:20:24; cần đối chiếu] cho đến bây giờ thì đối với nội dung mô hình thích hợp

<a id="S00753"></a>
**[01:20:29 → 01:20:35] [Người nói?]** [nghe không rõ 01:20:29; cần đối chiếu] đối với cái cảnh thời gian, thời gian tạo chiếu, cái bài báo rất là nhiều.

<a id="S00754"></a>
**[01:20:36 → 01:20:42] [Người nói?]** Sau khi thực hiện quá trình để mà trích xuất các đặc trưng khác nhau

<a id="S00755"></a>
**[01:20:42 → 01:20:45] [Người nói?]** giữa các frame ở trong một cái video sẽ được mang

<a id="S00756"></a>
**[01:20:45 → 01:20:50] [Người nói?]** [nghe không rõ 01:20:45; cần đối chiếu] cái mô hình Transformer Handcorder, tại cái mô hình Transformer Handcorder

<a id="S00757"></a>
**[01:20:50 → 01:20:53] [Người nói?]** [nghe không rõ 01:20:50; cần đối chiếu] không phải giống như cái Transformer Handcorder thông thường.

<a id="S00758"></a>
**[01:20:53 → 01:21:00] [Người nói?]** [nghe không rõ 01:20:53; cần đối chiếu] Và đây sẽ sử dụng cái cơ chế như là DLModal Max Interframe Shell Attention

<a id="S00759"></a>
**[01:21:00 → 01:21:06] [Người nói?]** [ASR cần nghe lại] có nghĩa là sẽ che chính nó đi

<a id="S00760"></a>
**[01:21:06 → 01:21:11] [Người nói?]** [ASR cần nghe lại] để từ các cái frame khi mà so sánh với nhau

<a id="S00761"></a>
**[01:21:11 → 01:21:13] [Người nói?]** [ASR cần nghe lại] thì nó sẽ không so sánh với chính nó

<a id="S00762"></a>
**[01:21:13 → 01:21:15] [Người nói?]** [ASR cần nghe lại] khi mà nó so sánh với chính nó thì

<a id="S00763"></a>
**[01:21:15 → 01:21:18] [Người nói?]** [ASR cần nghe lại] cái giá trị mà so sánh với chính nó

<a id="S00764"></a>
**[01:21:18 → 01:21:19] [Người nói?]** [ASR cần nghe lại] thì nó sẽ cao nhất so với tất cả

<a id="S00765"></a>
**[01:21:19 → 01:21:22] [Người nói?]** [ASR cần nghe lại] cái việc mà so sánh với các cái frame khác

<a id="S00766"></a>
**[01:21:23 → 01:21:27] [Người nói?]** [ASR cần nghe lại] Đấy là hai cái tư chế mà đề xuất ở trong cái mô hình này

<a id="S00767"></a>
**[01:21:29 → 01:21:39] [Người nói?]** Trong bài báo anh cũng có giải thích cơ chế đó, có thử nghiệm trong bài báo này đối với tầng học.

<a id="S00768"></a>
**[01:21:39 → 01:21:40] [Người nói?]** Vâng, bây giờ mình sẽ giải thích.

<a id="S00769"></a>
**[01:21:44 → 01:21:50] [Người nói?]** [nghe không rõ 01:21:44; cần đối chiếu] Phụ thể đối với tổng số, frame là 106 triệu tham số.

<a id="S00770"></a>
**[01:21:50 → 01:22:01] [Người nói?]** [nghe không rõ 01:21:50; cần đối chiếu] Có nghĩa là đối với cơ chế của 106 triệu tham số, nó cũng sẽ lớn hơn khá nhiều so với môi trường trước đây.

<a id="S00771"></a>
**[01:22:01 → 01:22:23] [Người nói?]** [nghe không rõ 01:22:01; cần đối chiếu] Ví dụ như là Zencomics thì nó là 600 triệu, đối với Instability thì nó gần 200 triệu, với môn kẻ của em nó là 116 triệu.

<a id="S00772"></a>
**[01:22:23 → 01:22:33] [Người nói?]** [nghe không rõ 01:22:23; cần đối chiếu] Có lẽ là cụ thể về đối với các giải thích thì xem thêm như thế này.

## Đánh giá liên tập và làm rõ trọng tâm

<a id="S00773"></a>
**[01:22:33 → 01:22:48] [Người nói?]** [nghe không rõ 01:22:33; cần đối chiếu] Khi mình xem phần introduction, phần ca lợi, ca lợi mình làm cái gì mà nó thấy hay.

<a id="S00774"></a>
**[01:22:51 → 01:23:02] [Người nói?]** [nghe không rõ 01:22:51; cần đối chiếu] Đối với phần introduction này thì chủ nghĩa là nói đến việc là hiện nay đối với các mô hình hiện nay trong việc phát hiện feedback,

<a id="S00775"></a>
**[01:23:03 → 01:23:14] [Người nói?]** [nghe không rõ 01:23:03; cần đối chiếu] Về cơ bản, đối với các kết quả và đánh giá trên nội tập là nó gần gần đã bão mạ rồi

<a id="S00776"></a>
**[01:23:14 → 01:23:22] [Người nói?]** [nghe không rõ 01:23:14; cần đối chiếu] Có nghĩa là độ chính xác hoặc các chỉ số AUC gần như tuyệt đối rồi

<a id="S00777"></a>
**[01:23:22 → 01:23:28] [Người nói?]** [nghe không rõ 01:23:22; cần đối chiếu] Nên sự so sánh sẽ không thiên về nội tập nữa

<a id="S00778"></a>
**[01:23:29 → 01:23:32] [Người nói?]** [nghe không rõ 01:23:29; cần đối chiếu] mà nó chủ yếu là so sánh đối với là điên tập

<a id="S00779"></a>
**[01:23:32 → 01:23:38] [Người nói?]** [nghe không rõ 01:23:32; cần đối chiếu] có nghĩa là huấn luyện ở trên cái tập trí liệu này và kể thử ở trên cái tập trí liệu khác

<a id="S00780"></a>
**[01:23:38 → 01:23:43] [Người nói?]** [nghe không rõ 01:23:38; cần đối chiếu] Thì cụ thể trong cái bài này của em cũng là huấn luyện ở trên những cái tập trí liệu

<a id="S00781"></a>
**[01:23:43 → 01:23:45] [Người nói?]** [nghe không rõ 01:23:43; cần đối chiếu] Phase Forensics hoặc là DC

<a id="S00782"></a>
**[01:23:47 → 01:23:50] [Người nói?]** [nghe không rõ 01:23:47; cần đối chiếu] và test ở trên cái tập trí liệu là Select NS

<a id="S00783"></a>
**[01:23:50 → 01:23:52] [Người nói?]** [nghe không rõ 01:23:50; cần đối chiếu] có nghĩa là test ở trên cái tập trí liệu lên tập

<a id="S00784"></a>
**[01:23:52 → 01:23:59] [Người nói?]** [nghe không rõ 01:23:52; cần đối chiếu] Thì đối với các bài báo đến nay thì thông thường khi mà huấn luyện ở trên tập trí liệu

<a id="S00785"></a>
**[01:23:59 → 01:24:07] [Người nói?]** [nghe không rõ 01:23:59; cần đối chiếu] Ví dụ như Face Forex chẳng hạn, test ở trên tập như là của SelectDF thường là nó sẽ rơi xuống cái độ chính xác

<a id="S00786"></a>
**[01:24:07 → 01:24:15] [Người nói?]** [nghe không rõ 01:24:07; cần đối chiếu] Cái AUC của nó thì nó sẽ rơi xuống khoảng, nếu mà test ở trên cái độ tập thì nó khoảng 99%

<a id="S00787"></a>
**[01:24:16 → 01:24:22] [Người nói?]** [nghe không rõ 01:24:16; cần đối chiếu] Nhưng mà khi mà nó test ở trên cái độ tập thì nó sẽ rơi xuống khoảng 60-75% thôi

<a id="S00788"></a>
**[01:24:24 → 01:24:36] [Người nói?]** [nghe không rõ 01:24:24; cần đối chiếu] Kể cả là đối với mô hình gian Covid thì nó cũng test liên tập thì nó chỉ rơi được khoảng tầm trên 50%

<a id="S00789"></a>
**[01:24:36 → 01:24:40] [Người nói?]** [nghe không rõ 01:24:36; cần đối chiếu] Khi mà test, test thì cũng chắc cái bộ dữ liệu liên tập

<a id="S00790"></a>
**[01:24:40 → 01:24:44] [Người nói?]** [nghe không rõ 01:24:40; cần đối chiếu] Thì cũng chính vì như thế nên là đối với các loại bảo vệ

<a id="S00791"></a>
**[01:24:45 → 01:24:55] [Người nói?]** [nghe không rõ 01:24:45; cần đối chiếu] Bây giờ mình nghĩ rằng là phát hiện effect, kế sức môi hồ sâu cũng không bị về mặt nghiệp trụ sinh năm nay

<a id="S00792"></a>
**[01:24:55 → 01:25:23] [Người nói?]** [nghe không rõ 01:24:55; cần đối chiếu] Nói chung là cái mô hình mới ở đây có nghĩa là đề xuất một cái mô hình để mà có thể phát hiện feedback nhưng mà nó phải có hạt hóa tốt hơn so với các cái mô hình hiện tại.

<a id="S00793"></a>
**[01:25:23 → 01:25:31] [Người nói?]** Tổng phát hóa thể hiện là vấn đề trên một cái mổ dữ liệu và kiểm tra trên một cái mổ dữ liệu mà chưa nhìn thấy.

<a id="S00794"></a>
**[01:25:31 → 01:25:34] [Người nói?]** [nghe không rõ 01:25:31; cần đối chiếu] Thì nó phải là inter-dataset đúng không?

<a id="S00795"></a>
**[01:25:35 → 01:25:38] [Người nói?]** [nghe không rõ 01:25:35; cần đối chiếu] Thì cái inter-dataset nó nằm ở đâu trong cái phần extract và installation?

<a id="S00796"></a>
**[01:25:40 → 01:25:41] [Người nói?]** [nghe không rõ 01:25:40; cần đối chiếu] Inter-dataset nằm ở đây

<a id="S00797"></a>
**[01:25:41 → 01:25:41] [Người nói?]** [nghe không rõ 01:25:41; cần đối chiếu] Ờ

<a id="S00798"></a>
**[01:25:41 → 01:25:51] [Người nói?]** [nghe không rõ 01:25:41; cần đối chiếu] Đây, thì cái ngay đầu tiên của em là Ngu nói cái phần inter-dataset ở đây

<a id="S00799"></a>
**[01:25:52 → 01:25:53] [Người nói?]** [nghe không rõ 01:25:52; cần đối chiếu] Có thể hệ trên tiêu đề nữa không?

<a id="S00800"></a>
**[01:25:53 → 01:25:55] [Người nói?]** [nghe không rõ 01:25:53; cần đối chiếu] Trong phần tiêu đề là nói rồi

<a id="S00801"></a>
**[01:25:55 → 01:25:56] [Người nói?]** [nghe không rõ 01:25:55; cần đối chiếu] Theo tiêu đề là từ nào?

<a id="S00802"></a>
**[01:25:57 → 01:25:58] [Người nói?]** [nghe không rõ 01:25:57; cần đối chiếu] Tiêu đề đúng không? Title đúng không?

<a id="S00803"></a>
**[01:25:58 → 01:26:01] [Người nói?]** [nghe không rõ 01:25:58; cần đối chiếu] À, Title thì cũng không

<a id="S00804"></a>
**[01:26:03 → 01:26:11] [Người nói?]** [nghe không rõ 01:26:03; cần đối chiếu] Bây giờ mình về cao hình này, 75 effect đề xuất một hộp show, rất nhiều người nói

<a id="S00805"></a>
**[01:26:13 → 01:26:19] [Người nói?]** [nghe không rõ 01:26:13; cần đối chiếu] Kẻ em có đề xuất lên khoảng 95% của em nên sau khi mở trang của họ, 8-9% thì nó cũng không có gì mới cả

<a id="S00806"></a>
**[01:26:20 → 01:26:23] [Người nói?]** [nghe không rõ 01:26:20; cần đối chiếu] Đúng chưa? Nó chỉ là một loài mặt kỹ thuật thôi

<a id="S00807"></a>
**[01:26:23 → 01:26:30] [Người nói?]** Thế bây giờ, cái vấn đề mà em giải quyết mà thiệt là sự đột phá đây nó là cái gì?

<a id="S00808"></a>
**[01:26:30 → 01:26:40] [Người nói?]** [nghe không rõ 01:26:30; cần đối chiếu] Đấy, thì phải chăng đó là Inter Domain, Cross Domain

<a id="S00809"></a>
**[01:26:40 → 01:26:46] [Người nói?]** [nghe không rõ 01:26:40; cần đối chiếu] Thì Cross Domain này nó được thể hiện tầm quan trọng ở chỗ nào trong tất cả cái kinh tế này

<a id="S00810"></a>
**[01:26:48 → 01:26:52] [Người nói?]** [nghe không rõ 01:26:48; cần đối chiếu] Cái đấy thì ở trong tool này thì em chưa thể hiện cái việc đó

<a id="S00811"></a>
**[01:26:52 → 01:26:55] [Người nói?]** [nghe không rõ 01:26:52; cần đối chiếu] Nhưng mà trong HeadTrack thì đã thể hiện rồi

<a id="S00812"></a>
**[01:26:55 → 01:27:02] [Người nói?]** [nghe không rõ 01:26:55; cần đối chiếu] Rồi, HeadTrack, tức là ở trong intro hoặc trong tất cả nó có mục riêng cho Cross Domain kinh tế này sẽ được

<a id="S00813"></a>
**[01:27:02 → 01:27:05] [Người nói?]** [nghe không rõ 01:27:02; cần đối chiếu] Không, nó không có mục riêng

<a id="S00814"></a>
**[01:27:05 → 01:27:07] [Người nói?]** [nghe không rõ 01:27:05; cần đối chiếu] Mà thể hiện trong các nội dung

<a id="S00815"></a>
**[01:27:07 → 01:27:08] [Người nói?]** [nghe không rõ 01:27:07; cần đối chiếu] Vẫn này không?

<a id="S00816"></a>
**[01:27:08 → 01:27:09] [Người nói?]** [nghe không rõ 01:27:08; cần đối chiếu] Vẫn này không

<a id="S00817"></a>
**[01:27:13 → 01:27:16] [Người nói?]** Sau mấy bài tạp chí vừa rồi

<a id="S00818"></a>
**[01:27:16 → 01:27:18] [Người nói?]** Họ không đồng ý với bài này

<a id="S00819"></a>
**[01:27:18 → 01:27:20] [Người nói?]** Tại vì nghĩ lại nó có thể rõ hơn

<a id="S00820"></a>
**[01:27:20 → 01:27:23] [Người nói?]** [nghe không rõ 01:27:20; cần đối chiếu] Đa số họ nghĩ là

<a id="S00821"></a>
**[01:27:23 → 01:27:25] [Người nói?]** [nghe không rõ 01:27:23; cần đối chiếu] Mình đề xuất một phương pháp

<a id="S00822"></a>
**[01:27:25 → 01:27:26] [Người nói?]** [nghe không rõ 01:27:25; cần đối chiếu] Giữa trường sâu

<a id="S00823"></a>
**[01:27:27 → 01:27:28] [Người nói?]** [nghe không rõ 01:27:27; cần đối chiếu] Cảm thấy gì đó để

<a id="S00824"></a>
**[01:27:30 → 01:27:33] [Người nói?]** [nghe không rõ 01:27:30; cần đối chiếu] Nhưng họ cảm thấy chưa có gì đáng giá

<a id="S00825"></a>
**[01:27:33 → 01:27:35] [Người nói?]** [nghe không rõ 01:27:33; cần đối chiếu] Với đặc biệt trên các tạp chí lớn

<a id="S00826"></a>
**[01:27:35 → 01:27:39] [Người nói?]** [nghe không rõ 01:27:35; cần đối chiếu] Trên tạp chí lớn họ muốn là

<a id="S00827"></a>
**[01:27:39 → 01:27:45] [Người nói?]** [nghe không rõ 01:27:39; cần đối chiếu] Bài này cũng đề xuất một vấn đề gì đấy mà thực sự nó là mới

<a id="S00828"></a>
**[01:27:49 → 01:27:51] [Người nói?]** [nghe không rõ 01:27:49; cần đối chiếu] Cho em thầy hỏi thử một câu

<a id="S00829"></a>
**[01:27:52 → 01:27:58] [Người nói?]** Nếu em nói là trên cross domain nó là vấn đề quan trọng

<a id="S00830"></a>
**[01:27:58 → 01:28:00] [Người nói?]** [nghe không rõ 01:27:58; cần đối chiếu] và ít thằng nó tới

<a id="S00831"></a>
**[01:28:00 → 01:28:06] [Người nói?]** [nghe không rõ 01:28:00; cần đối chiếu] Thì mình có thể tiêu đề cho nó tới một mục riêng

<a id="S00832"></a>
**[01:28:14 → 01:28:17] [Người nói?]** [nghe không rõ 01:28:14; cần đối chiếu] Vừa rồi mình thấy ông chỉ có mỗi lần

<a id="S00833"></a>
**[01:28:17 → 01:28:19] [Người nói?]** [nghe không rõ 01:28:17; cần đối chiếu] Thấy thằng này làm hay, thằng này làm hay

<a id="S00834"></a>
**[01:28:20 → 01:28:22] [Người nói?]** [nghe không rõ 01:28:20; cần đối chiếu] Ông ghép hai thằng hay với nhau

<a id="S00835"></a>
**[01:28:22 → 01:28:28] [Người nói?]** [nghe không rõ 01:28:22; cần đối chiếu] Đấy, để trở thành một cái thang để trả lời người đấy thì nó gọi chứ gì, đồng ý là được rồi.

<a id="S00836"></a>
**[01:28:28 → 01:28:35] [Người nói?]** [nghe không rõ 01:28:28; cần đối chiếu] Ok, tốt, tốt nhưng chưa phải là, nó gọi là gì, good but not enough.

<a id="S00837"></a>
**[01:28:36 → 01:28:41] [Người nói?]** [nghe không rõ 01:28:36; cần đối chiếu] Đấy, interesting nhưng mà, I'm sorry.

<a id="S00838"></a>
**[01:28:42 → 01:28:44] [Người nói?]** [nghe không rõ 01:28:42; cần đối chiếu] Cái interesting but I'm sorry is not enough.

<a id="S00839"></a>
**[01:28:45 → 01:28:46] [Người nói?]** [nghe không rõ 01:28:45; cần đối chiếu] Chưa đủ. Đấy.

<a id="S00840"></a>
**[01:28:47 → 01:28:49] [Người nói?]** [nghe không rõ 01:28:47; cần đối chiếu] Thế thì, thế thì thầy nhận là gì?

<a id="S00841"></a>
**[01:28:50 → 01:28:53] [Người nói?]** [nghe không rõ 01:28:50; cần đối chiếu] Cái, cái điểm nhấn của mình là chưa đúng trong tầm tầm quan tâm.

<a id="S00842"></a>
**[01:28:55 → 01:28:58] [Người nói?]** [nghe không rõ 01:28:55; cần đối chiếu] Thầy rất ghi nhận cái, đó có phải thầy thấy rất hay.

<a id="S00843"></a>
**[01:28:58 → 01:29:02] [Người nói?]** [nghe không rõ 01:28:58; cần đối chiếu] Nhưng mà bản thân tạp chí người ta chưa đúng với quan tâm của họ

<a id="S00844"></a>
**[01:29:05 → 01:29:14] [Người nói?]** [nghe không rõ 01:29:05; cần đối chiếu] Thế bây giờ ta phải bàn kia nhau xem là cái vấn đề chính mà em quên coi ấy

<a id="S00845"></a>
**[01:29:18 → 01:29:22] [Người nói?]** [nghe không rõ 01:29:18; cần đối chiếu] Điểm vất vả mà người ta đang muốn giải quyết nó là

<a id="S00846"></a>
**[01:29:22 → 01:29:27] [Người nói?]** [nghe không rõ 01:29:22; cần đối chiếu] Mình thực toán thì chắc là khó rồi đúng không?

<a id="S00847"></a>
**[01:29:27 → 01:29:30] [Người nói?]** [nghe không rõ 01:29:27; cần đối chiếu] Thực toán là mình lắp ghép cải tiến rồi

<a id="S00848"></a>
**[01:29:30 → 01:29:33] [Người nói?]** [nghe không rõ 01:29:30; cần đối chiếu] Thế nhưng mà mình phải đánh nó sang miền nước nữa

<a id="S00849"></a>
**[01:29:33 → 01:29:34] [Người nói?]** [nghe không rõ 01:29:33; cần đối chiếu] Nó là cái gì?

<a id="S00850"></a>
**[01:29:34 → 01:29:40] [Người nói?]** Thế em thấy là đúng hạt vị cross-battaset ok?

<a id="S00851"></a>
**[01:29:40 → 01:29:42] [Người nói?]** Vâng, chính là cái đấy

<a id="S00852"></a>
**[01:29:42 → 01:29:44] [Người nói?]** [nghe không rõ 01:29:42; cần đối chiếu] Trong 6 hạt hóa này em đều hướng đến cái đấy

<a id="S00853"></a>
**[01:29:44 → 01:29:48] [Người nói?]** [nghe không rõ 01:29:44; cần đối chiếu] Thế em hiện tư chưa đề cho tới một trong...

<a id="S00854"></a>
**[01:29:48 → 01:29:56] [Người nói?]** [nghe không rõ 01:29:48; cần đối chiếu] Trong cái phần introduction này của em là đều xoay quanh về vấn đề cross-domain

<a id="S00855"></a>
**[01:29:56 → 01:29:59] [Người nói?]** [nghe không rõ 01:29:56; cần đối chiếu] Phần extract cũng xoay

<a id="S00856"></a>
**[01:30:00 → 01:30:03] [Người nói?]** [nghe không rõ 01:30:00; cần đối chiếu] vấn đề raw format, nhưng mà Châu cần tiêu đề, chứ không thể.

<a id="S00857"></a>
**[01:30:03 → 01:30:30] [Người nói?]** Trong tất cả những phần ở dưới cũng đều đề cập đến kiến nghiệm đánh giá trên một bộ dữ liệu khác,

<a id="S00858"></a>
**[01:30:30 → 01:30:39] [Người nói?]** một bộ dữ liệu chưa nhìn thấy, để tăng kết quả của một bộ dữ liệu chưa nhìn thấy.

<a id="S00859"></a>
**[01:30:39 → 01:30:43] [Người nói?]** Trong tất cả các nội dung ở dưới đều đánh giá như thế này.

<a id="S00860"></a>
**[01:30:47 → 01:30:56] [Người nói?]** [nghe không rõ 01:30:47; cần đối chiếu] Các luận giải, các chứng minh cũng nói về việc đó. Trong đấy, em cũng thử khoảng tầm 55 lần rồi mới lại.

<a id="S00861"></a>
**[01:30:57 → 01:31:04] [Người nói?]** [nghe không rõ 01:30:57; cần đối chiếu] Thế bây giờ nó sẽ đặt ngay trên đầu, lên tiêu đề thì ta đặt ra câu hỏi là

<a id="S00862"></a>
**[01:31:04 → 01:31:18] [Người nói?]** [nghe không rõ 01:31:04; cần đối chiếu] Nếu đặt ra tiêu đề là temporal complex cho defective variation in cross domain gì đấy, ra thống của cross domain này có được không?

<a id="S00863"></a>
**[01:31:20 → 01:31:30] [Người nói?]** [nghe không rõ 01:31:20; cần đối chiếu] Lúc đầu em cũng nghĩ như thế rồi, nhưng em thấy là nó chưa nhấn mắt 2 cái FL, FR với MI, F2

<a id="S00864"></a>
**[01:31:30 → 01:31:36] [Người nói?]** [nghe không rõ 01:31:30; cần đối chiếu] Thế FL này là 1 cái đặc trái quan tâm, chỉ tổ theo cấu ấy, nó rảnh luôn

<a id="S00865"></a>
**[01:31:38 → 01:31:42] [Người nói?]** [nghe không rõ 01:31:38; cần đối chiếu] Đấy, ưu đề là nó thấy sức bình dị mà nó rõ ràng thể hiện được cái điểm nhấn mình

<a id="S00866"></a>
**[01:31:42 → 01:31:49] [Người nói?]** [nghe không rõ 01:31:42; cần đối chiếu] Tất cả những thêm bộ bằng Break Timeformer, Network, Defective Duration nó là tầm thường rồi đó

<a id="S00867"></a>
**[01:31:49 → 01:31:53] [Người nói?]** [nghe không rõ 01:31:49; cần đối chiếu] Thế bây giờ cái phần thường đề đó là cross domain thì em được không?

<a id="S00868"></a>
**[01:31:54 → 01:32:04] [Người nói?]** [nghe không rõ 01:31:54; cần đối chiếu] Thế còn cái FL, DMI em à, nếu mà thường thường nó hay thì em giữ tả nó bằng 1, 2 câu mà nó không phải cứ tắt gạch, em thấy hiểu không?

<a id="S00869"></a>
**[01:32:05 → 01:32:08] [Người nói?]** [nghe không rõ 01:32:05; cần đối chiếu] Đấy, đối với cross domain ấy

<a id="S00870"></a>
**[01:32:08 → 01:32:16] [Người nói?]** [ASR cần nghe lại] Vâng, thực ra là trong toàn bộ cái bài này thì cái cross domain mới là cái chính mà em nhắm đến

<a id="S00871"></a>
**[01:32:17 → 01:32:23] [Người nói?]** [nghe không rõ 01:32:17; cần đối chiếu] Chính thế, cho nên là nếu đúng như thế thì ngay từ tiêu đề cho tới thì có trong một cách nhất

<a id="S00872"></a>
**[01:32:23 → 01:32:26] [Người nói?]** [nghe không rõ 01:32:23; cần đối chiếu] Đọc phát là thấy product name nó tràn đọc được

<a id="S00873"></a>
**[01:32:26 → 01:32:30] [Người nói?]** [nghe không rõ 01:32:26; cần đối chiếu] Và chưa thật nào làm được điều đấy thì mình làm thành bản

<a id="S00874"></a>
**[01:32:30 → 01:32:34] [Người nói?]** [nghe không rõ 01:32:30; cần đối chiếu] Thì thật ra nếu em làm như thế thì mình nghĩ là sẽ ăn điện

<a id="S00875"></a>
**[01:32:44 → 01:32:47] [Người nói?]** [nghe không rõ 01:32:44; cần đối chiếu] Kết quả sau của Thuấn mình nghĩ là có rất thậm chí

<a id="S00876"></a>
**[01:32:47 → 01:32:49] [Người nói?]** [nghe không rõ 01:32:47; cần đối chiếu] Cá nhân mình nghĩ chẳng làm thêm được cả

<a id="S00877"></a>
**[01:32:49 → 01:32:53] [Người nói?]** [nghe không rõ 01:32:49; cần đối chiếu] Cái vấn đề là làm thế nào để đặt nó vào đúng cái điểm rơi thôi

<a id="S00878"></a>
**[01:32:53 → 01:32:56] [Người nói?]** [nghe không rõ 01:32:53; cần đối chiếu] Thế là cái điểm giữ cho nó quan tâm

<a id="S00879"></a>
**[01:32:56 → 01:32:56] [Người nói?]** [nghe không rõ 01:32:56; cần đối chiếu] Đấy

<a id="S00880"></a>
**[01:32:57 → 01:33:03] [Người nói?]** [nghe không rõ 01:32:57; cần đối chiếu] Cái cách mà mình làm người ta cứ thấy đều đều đều

<a id="S00881"></a>
**[01:33:03 → 01:33:05] [Người nói?]** [nghe không rõ 01:33:03; cần đối chiếu] Nó cũng giống như người khác làm thôi

<a id="S00882"></a>
**[01:33:05 → 01:33:06] [Người nói?]** [nghe không rõ 01:33:05; cần đối chiếu] Đấy

<a id="S00883"></a>
**[01:33:06 → 01:33:07] [Người nói?]** [nghe không rõ 01:33:06; cần đối chiếu] Thế này này hai này hai

<a id="S00884"></a>
**[01:33:08 → 01:33:09] [Người nói?]** [nghe không rõ 01:33:08; cần đối chiếu] Xộn vào nhau đúng không

<a id="S00885"></a>
**[01:33:09 → 01:33:10] [Người nói?]** [nghe không rõ 01:33:09; cần đối chiếu] Đấy kiểu thế

<a id="S00886"></a>
**[01:33:11 → 01:33:12] [Người nói?]** [nghe không rõ 01:33:11; cần đối chiếu] Thực tế cũng phải

<a id="S00887"></a>
**[01:33:12 → 01:33:16] [Người nói?]** [nghe không rõ 01:33:12; cần đối chiếu] Chứ cái không phải đấy mình làm là giỏi

<a id="S00888"></a>
**[01:33:19 → 01:33:19] [Người nói?]** [nghe không rõ 01:33:19; cần đối chiếu] Thế thôi

<a id="S00889"></a>
**[01:33:19 → 01:33:24] [Người nói?]** [nghe không rõ 01:33:19; cần đối chiếu] Thế thôi những kinh nghiệm của em mình nghĩ là quá đầy đủ

<a id="S00890"></a>
**[01:33:24 → 01:33:25] [Người nói?]** [nghe không rõ 01:33:24; cần đối chiếu] Chứ không phải là đầy đủ vừa

<a id="S00891"></a>
**[01:33:25 → 01:33:29] [Người nói?]** [nghe không rõ 01:33:25; cần đối chiếu] Dạ em nghĩ là kinh nghiệm

<a id="S00892"></a>
**[01:33:32 → 01:33:33] [Người nói?]** [nghe không rõ 01:33:32; cần đối chiếu] Tổng kinh nghiệm

<a id="S00893"></a>
**[01:33:33 → 01:33:34] [Người nói?]** [nghe không rõ 01:33:33; cần đối chiếu] Mình có

<a id="S00894"></a>
**[01:33:35 → 01:33:36] [Người nói?]** [nghe không rõ 01:33:35; cần đối chiếu] Mình đã

<a id="S00895"></a>
**[01:33:37 → 01:33:37] [Người nói?]** [nghe không rõ 01:33:37; cần đối chiếu] Mình đã

<a id="S00896"></a>
**[01:33:37 → 01:33:42] [Người nói?]** [nghe không rõ 01:33:37; cần đối chiếu] Mình đã đi khai mỏ, mình đã có người bảo địa về, mình đã đóng hành vàng khối rồi

<a id="S00897"></a>
**[01:33:43 → 01:33:49] [Người nói?]** [nghe không rõ 01:33:43; cần đối chiếu] Nhưng vấn đề là cho thị trường biết cái vàng khối của mình là sản chất, ngon, hơn cái sản khác

<a id="S00898"></a>
**[01:33:50 → 01:33:51] [Người nói?]** [nghe không rõ 01:33:50; cần đối chiếu] Đấy là nhiệm vụ của tôi

<a id="S00899"></a>
**[01:33:53 → 01:33:59] [Người nói?]** [nghe không rõ 01:33:53; cần đối chiếu] Thì qua những trả lời mình muốn hỏi, tự hóa chính là cái gì thì nếu em nói là crossroom lên tự hóa chính thì em phải thu nó

<a id="S00900"></a>
**[01:34:01 → 01:34:15] [Người nói?]** [nghe không rõ 01:34:01; cần đối chiếu] Thấy không? Hiền có ý gì xin bài không Hiền?

<a id="S00901"></a>
**[01:34:15 → 01:34:15] [Người nói?]** [nghe không rõ 01:34:15; cần đối chiếu] Dạ thôi Hiền

<a id="S00902"></a>
**[01:34:20 → 01:34:28] [Người nói?]** [nghe không rõ 01:34:20; cần đối chiếu] Mình nói trước lần bài cái khách ăn ngon rồi, làm thế nào để gắn vào luận án này thôi?

<a id="S00903"></a>
**[01:34:28 → 01:34:40] [Người nói?]** [nghe không rõ 01:34:28; cần đối chiếu] Em thì cũng có bụi, em báo cáo thế giới em cũng dựa trên cơ bài đấy, cầm gửi cho cơ bài, xin các bạn tính

## Góp ý cho các đề tài: vấn đề chưa giải quyết và khảo sát mới

<a id="S00904"></a>
**[01:34:40 → 01:34:54] [Người nói?]** [nghe không rõ 01:34:40; cần đối chiếu] Câu hỏi này ra nhé, nếu mà mình làm luận án để học sâu cho phát hiện tính tiện thì điểm nhấn nó là cái gì?

<a id="S00905"></a>
**[01:34:56 → 01:34:59] [Người nói?]** Từ mặt học thuật, nó là cái gì mà người ta chưa giải quyết được?

<a id="S00906"></a>
**[01:35:00 → 01:35:10] [Người nói?]** [nghe không rõ 01:35:00; cần đối chiếu] Có thể là em nghĩ ra là cái bài mà ở các em

<a id="S00907"></a>
**[01:35:11 → 01:35:13] [Người nói?]** [nghe không rõ 01:35:11; cần đối chiếu] Nếu như mà thay mà em được

<a id="S00908"></a>
**[01:35:13 → 01:35:16] [Người nói?]** [nghe không rõ 01:35:13; cần đối chiếu] Thì em nghĩ ra là em đang giải quyết vấn đề của

<a id="S00909"></a>
**[01:35:16 → 01:35:20] [Người nói?]** [nghe không rõ 01:35:16; cần đối chiếu] Thì mai ra được con nữ như tình anh thì chắc chắn sẽ

<a id="S00910"></a>
**[01:35:20 → 01:35:24] [Người nói?]** [nghe không rõ 01:35:20; cần đối chiếu] Và em sẽ tập trung theo cái hướng là thức việc

<a id="S00911"></a>
**[01:35:24 → 01:35:33] [Người nói?]** [nghe không rõ 01:35:24; cần đối chiếu] Cơ sở dự liệu bây giờ thì cơ sở dự liệu thì được cả 1.500 bản tin

<a id="S00912"></a>
**[01:35:33 → 01:35:36] [Người nói?]** [nghe không rõ 01:35:33; cần đối chiếu] Cộng với hơn 1.500 bản tin từ xin và ảnh

<a id="S00913"></a>
**[01:35:36 → 01:35:58] [Người nói?]** [nghe không rõ 01:35:36; cần đối chiếu] Thế để cuốn bài thì em phải thay bỏ ý lộ sai

<a id="S00914"></a>
**[01:35:58 → 01:36:08] [Người nói?]** [nghe không rõ 01:35:58; cần đối chiếu] Mình vừa mới ký qua cái mẫu, mình nhận được các slide phải đúng không ạ?

<a id="S00915"></a>
**[01:36:09 → 01:36:13] [Người nói?]** [nghe không rõ 01:36:09; cần đối chiếu] Thì bài thì mình có rốt, mình cũng làm thế nào rồi.

<a id="S00916"></a>
**[01:36:13 → 01:36:16] [Người nói?]** [nghe không rõ 01:36:13; cần đối chiếu] Các mẫu là cái nội dung đó của các slide cho nó hoàn thiện.

<a id="S00917"></a>
**[01:36:16 → 01:36:23] [Người nói?]** [nghe không rõ 01:36:16; cần đối chiếu] Mình chỉ nói cho các em là tất cả các chủ đề của các chương trình ở đây,

<a id="S00918"></a>
**[01:36:24 → 01:36:27] [Người nói?]** [ASR cần nghe lại] thường xuyên các em phải khảo sát xem là người ta đã làm được gì.

<a id="S00919"></a>
**[01:36:27 → 01:36:31] [Người nói?]** [ASR cần nghe lại] Người ta đang làm thì người ta sẽ làm gì?

<a id="S00920"></a>
**[01:36:31 → 01:36:35] [Người nói?]** [ASR cần nghe lại] Trong tất cả những công trình, nếu các em vào năm 2026,

<a id="S00921"></a>
**[01:36:35 → 01:36:40] [Người nói?]** [ASR cần nghe lại] thì các em phải khảo sát đến tận tháng 9 năm 2026 để xem người ta làm được gì.

<a id="S00922"></a>
**[01:36:44 → 01:36:46] [Người nói?]** Thì mình biết là xu hướng thế nào

<a id="S00923"></a>
**[01:36:46 → 01:36:51] [Người nói?]** Và khi xu hướng thế nó ra thì người ta làm nhiều ở lĩnh vực này

<a id="S00924"></a>
**[01:36:51 → 01:36:54] [Người nói?]** [nghe không rõ 01:36:51; cần đối chiếu] Thì đương nhiên nếu mình làm ở đây là làm ở đá

<a id="S00925"></a>
**[01:36:54 → 01:36:55] [Người nói?]** [nghe không rõ 01:36:54; cần đối chiếu] Đúng không?

<a id="S00926"></a>
**[01:36:57 → 01:37:00] [Người nói?]** [nghe không rõ 01:36:57; cần đối chiếu] Thế nhưng mà người ta làm ở phía Bắc thì mình làm ở phía Nam

<a id="S00927"></a>
**[01:37:00 → 01:37:02] [Người nói?]** [nghe không rõ 01:37:00; cần đối chiếu] Phía Nam là làm cái gì? Đúng không?

<a id="S00928"></a>
**[01:37:02 → 01:37:05] [Người nói?]** [nghe không rõ 01:37:02; cần đối chiếu] Đấy tức là mình phải đặt hết để xem người ta làm cái gì

<a id="S00929"></a>
**[01:37:05 → 01:37:12] [Người nói?]** Tiếng Việt đúng là đúng những người ít người khai thác

<a id="S00930"></a>
**[01:37:12 → 01:37:17] [Người nói?]** Thế nhưng mà đặc trưng nó là cái gì thì em cũng phải nói thành lời

<a id="S00931"></a>
**[01:37:17 → 01:37:18] [Người nói?]** Thì mình cũng phải biết được

<a id="S00932"></a>
**[01:37:23 → 01:37:25] [Người nói?]** [nghe không rõ 01:37:23; cần đối chiếu] Vì cái tiếng Việt như thế này

<a id="S00933"></a>
**[01:37:25 → 01:37:27] [Người nói?]** [nghe không rõ 01:37:25; cần đối chiếu] Phải làm được cái đáp là xe của người thầy

<a id="S00934"></a>
**[01:37:27 → 01:37:32] [Người nói?]** [nghe không rõ 01:37:27; cần đối chiếu] Một bản data sẽ phổ biến cho mình cái chất khóa để chia sẻ ra được

<a id="S00935"></a>
**[01:37:32 → 01:37:37] [Người nói?]** [nghe không rõ 01:37:32; cần đối chiếu] Và em để ý cái đó thêm một cái gọi là cái vỉnh mặt của mình luôn

<a id="S00936"></a>
**[01:37:39 → 01:37:49] [Người nói?]** [nghe không rõ 01:37:39; cần đối chiếu] Rồi, nhận được. Ok. Vinh, sử dụng

<a id="S00937"></a>
**[01:37:53 → 01:37:59] [Người nói?]** [nghe không rõ 01:37:53; cần đối chiếu] Bây giờ thầy hỏi Vinh là cái kết quả đó thì thầy đặt ra yêu cầu là

<a id="S00938"></a>
**[01:37:59 → 01:38:02] [Người nói?]** [nghe không rõ 01:37:59; cần đối chiếu] Trong tháng 9 em ra được cái bài mà thả ra

<a id="S00939"></a>
**[01:38:04 → 01:38:07] [Người nói?]** [nghe không rõ 01:38:04; cần đối chiếu] Đang viết một bản draft, một bản kinh nghiệm

<a id="S00940"></a>
**[01:38:09 → 01:38:15] [Người nói?]** [nghe không rõ 01:38:09; cần đối chiếu] Một bản khác mà nói với mình ý, viết ngay từ đầu một tiếng Anh

<a id="S00941"></a>
**[01:38:15 → 01:38:28] [Người nói?]** [nghe không rõ 01:38:15; cần đối chiếu] Ý là em cũng có một bản về thiết kế này rồi, nhưng mà mấy hôm nay đợt kỷ lễ kết quả em báo cáo thầy là 0,59.

<a id="S00942"></a>
**[01:38:29 → 01:38:34] [Người nói?]** [nghe không rõ 01:38:29; cần đối chiếu] Giờ này em lại tỏ cáo là 0,86, tức là cái đợt đấy giảm sát lại thì nó không kết nối.

<a id="S00943"></a>
**[01:38:35 → 01:38:38] [Người nói?]** [nghe không rõ 01:38:35; cần đối chiếu] Xong rồi về sau giảm sát lại thì may mắn là đọc được sớm.

<a id="S00944"></a>
**[01:38:45 → 01:38:49] [Người nói?]** [nghe không rõ 01:38:45; cần đối chiếu] Em rất tự tin là có thể xung quanh được cái tạp chí khi lần đấy đi.

<a id="S00945"></a>
**[01:38:49 → 01:38:52] [Người nói?]** [nghe không rõ 01:38:49; cần đối chiếu] Em nghĩ chủ đề cũng rất là sáng.

<a id="S00946"></a>
**[01:38:52 → 01:38:58] [Người nói?]** [nghe không rõ 01:38:52; cần đối chiếu] Tự nhiên em chảy gì cũng không biết.

<a id="S00947"></a>
**[01:38:59 → 01:39:01] [Người nói?]** [nghe không rõ 01:38:59; cần đối chiếu] Vừa rồi mình mua rất nhiều cái bản án cũng thấy là...

<a id="S00948"></a>
**[01:39:01 → 01:39:09] [Người nói?]** [nghe không rõ 01:39:01; cần đối chiếu] Các bạn em cũng nói trời biển thì nhưng mà trong các cái phần thương tích so sánh em mà không có công trình set-up của em thì hãy tìm.

<a id="S00949"></a>
**[01:39:09 → 01:39:19] [Người nói?]** [nghe không rõ 01:39:09; cần đối chiếu] Năm 2026 mà em không so sánh với những cái công trình so sánh trở về trước, làm năm mùa năm trước thì không hãy tìm.

<a id="S00950"></a>
**[01:39:19 → 01:39:31] [Người nói?]** [nghe không rõ 01:39:19; cần đối chiếu] Có lẽ em so sánh với các dạng của cái bộ thư viện đấy thôi. Các dạng bộ thư viện đấy thì họ cũng khá là chăm chỉ.

<a id="S00951"></a>
**[01:39:31 → 01:39:37] [Người nói?]** [nghe không rõ 01:39:31; cần đối chiếu] Hai công hay tư học suốt một năm, hai năm học suốt vài năm nữa xong rồi đang ở cài để sử dụng.

<a id="S00952"></a>
**[01:39:43 → 01:39:46] [Người nói?]** [nghe không rõ 01:39:43; cần đối chiếu] Như vậy sắp tới nha, cái OECD thì Việt Nam đang kiếm một bài đúng không?

<a id="S00953"></a>
**[01:39:46 → 01:39:54] [Người nói?]** [nghe không rõ 01:39:46; cần đối chiếu] Cái này thì là diện rồi, mình là làm rồi đúng không?

<a id="S00954"></a>
**[01:39:54 → 01:39:59] [Người nói?]** [nghe không rõ 01:39:54; cần đối chiếu] Cái gì chai, cái này thì quên

<a id="S00955"></a>
**[01:40:07 → 01:40:22] [Người nói?]** [nghe không rõ 01:40:07; cần đối chiếu] Hãy subscribe cho kênh Ghiền Mì Gõ Để không bỏ lỡ những video hấp dẫn

## Yêu cầu giải thích điểm thưởng và hiểu mô hình

<a id="S00956"></a>
**[01:41:11 → 01:41:15] [Người nói?]** [nghe không rõ 01:41:11; cần đối chiếu] Đúng hay là thầy còn đang bán bất là suy nghe hết rồi

<a id="S00957"></a>
**[01:41:15 → 01:41:19] [Người nói?]** [nghe không rõ 01:41:15; cần đối chiếu] Nhưng mà thầy chưa thể hiện bày cái phần rì buột là không

<a id="S00958"></a>
**[01:41:20 → 01:41:23] [Người nói?]** [nghe không rõ 01:41:20; cần đối chiếu] Muốn đi show được thuật toán, đóng góp thuật toán

<a id="S00959"></a>
**[01:41:23 → 01:41:25] [Người nói?]** [nghe không rõ 01:41:23; cần đối chiếu] Thì cái đấy mới là cái trọng răng

<a id="S00960"></a>
**[01:41:25 → 01:41:30] [Người nói?]** [nghe không rõ 01:41:25; cần đối chiếu] Em phải trình bày sắp tới, em phải rõ ràng ra

<a id="S00961"></a>
**[01:41:30 → 01:41:32] [Người nói?]** [nghe không rõ 01:41:30; cần đối chiếu] Rì buột được tính như thế nào

<a id="S00962"></a>
**[01:41:34 → 01:41:38] [Người nói?]** [nghe không rõ 01:41:34; cần đối chiếu] Tính như thế nào và ảnh hưởng của rì buột này nó như thế nào

<a id="S00963"></a>
**[01:41:38 → 01:41:43] [Người nói?]** [nghe không rõ 01:41:38; cần đối chiếu] Và mình cải thiện cái gì mà liên quan đến rì buột

<a id="S00964"></a>
**[01:41:43 → 01:41:51] [Người nói?]** [nghe không rõ 01:41:43; cần đối chiếu] Và đối với như là nếu em tiếp tục làm du sinh thì

<a id="S00965"></a>
**[01:41:51 → 01:41:56] [Người nói?]** [nghe không rõ 01:41:51; cần đối chiếu] Thì em thấy bài toán rất có ý nghĩa, bài toán sinh được cái chuỗi, cái sự tích.

<a id="S00966"></a>
**[01:41:58 → 01:42:04] [Người nói?]** [nghe không rõ 01:41:58; cần đối chiếu] XQL đấy mà ứng dụng được thì quá xứng đáng vào luật án luôn.

<a id="S00967"></a>
**[01:42:06 → 01:42:09] [Người nói?]** [nghe không rõ 01:42:06; cần đối chiếu] Cũng mong có cái tương lai lạc quan thế.

<a id="S00968"></a>
**[01:42:09 → 01:42:14] [Người nói?]** [nghe không rõ 01:42:09; cần đối chiếu] Tương lai như nơi khác còn nằm sự tích nào.

<a id="S00969"></a>
**[01:42:17 → 01:42:20] [Người nói?]** [nghe không rõ 01:42:17; cần đối chiếu] Đã tích thì giá tích hẳn luôn.

<a id="S00970"></a>
**[01:42:27 → 01:42:35] [Người nói?]** [nghe không rõ 01:42:27; cần đối chiếu] Mà lần này thì em sẽ chỉ tập trung vào 2 phương án là smoth với cả si quần gan chứ không cần phải quan tâm cái kiểu.

<a id="S00971"></a>
**[01:42:35 → 01:42:38] [Người nói?]** [nghe không rõ 01:42:35; cần đối chiếu] Sư luận gan, em tập trung sư luận gan cho thầy

<a id="S00972"></a>
**[01:42:38 → 01:42:45] [Người nói?]** [nghe không rõ 01:42:38; cần đối chiếu] Và em làm hết mức để thủ đoàn đấy chạy tối đa với tỉ thường gốc giấy của nó

<a id="S00973"></a>
**[01:42:45 → 01:42:50] [Người nói?]** [nghe không rõ 01:42:45; cần đối chiếu] Và sau đó là thầy phải cải thiện nó

<a id="S00974"></a>
**[01:42:50 → 01:42:53] [Người nói?]** [ASR cần nghe lại] Thầy có nhiều ý tưởng cải thiện nó nhưng mà thầy muốn em phải hiểu về nó

<a id="S00975"></a>
**[01:42:55 → 01:42:57] [Người nói?]** [nghe không rõ 01:42:55; cần đối chiếu] Lúc thạc sĩ thì ok, thạc sĩ thế này em hoàn thành xuất sắc

<a id="S00976"></a>
**[01:42:57 → 01:43:03] [Người nói?]** [nghe không rõ 01:42:57; cần đối chiếu] Như vậy là 15 tháng 51 là hạng của FGK

<a id="S00977"></a>
**[01:43:05 → 01:43:07] [Người nói?]** [nghe không rõ 01:43:05; cần đối chiếu] Như vậy em sẽ có từ tháng 9 tháng 10

<a id="S00978"></a>
**[01:43:08 → 01:43:11] [Người nói?]** [nghe không rõ 01:43:08; cần đối chiếu] 5 tuần, 10 tuần

<a id="S00979"></a>
**[01:43:11 → 01:43:31] [Người nói?]** [nghe không rõ 01:43:11; cần đối chiếu] Thế thôi, tới vào cuối tuần

<a id="S00980"></a>
**[01:43:46 → 01:44:23] [Người nói?]** [nghe không rõ 01:43:46; cần đối chiếu] Hãy subscribe cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

## Trao đổi kết thúc, lịch cá nhân và đồ dùng

<a id="S00981"></a>
**[01:44:25 → 01:44:32] [Người nói?]** [nghe không rõ 01:44:25; cần đối chiếu] Cái này sư phụ thấy là sáng rồi, nhưng mà với quả ngoại nữ thì đúng là ngoài tầm

<a id="S00982"></a>
**[01:44:32 → 01:44:35] [Người nói?]** [nghe không rõ 01:44:32; cần đối chiếu] Ngoài tầm của không lưu trưởng được hết

<a id="S00983"></a>
**[01:44:35 → 01:44:39] [Người nói?]** [nghe không rõ 01:44:35; cần đối chiếu] Chỉ còn để mà xong cái kệ đấy thì em là vào làm

<a id="S00984"></a>
**[01:44:39 → 01:44:45] [Người nói?]** [nghe không rõ 01:44:39; cần đối chiếu] Nhưng mà thôi thì viết chứ gì thế, phải chấp nhận

<a id="S00985"></a>
**[01:44:47 → 01:44:50] [Người nói?]** [nghe không rõ 01:44:47; cần đối chiếu] Em không dúng tiếng Anh lên, em còn dúng cũng chỉ là

<a id="S00986"></a>
**[01:44:50 → 01:44:54] [Người nói?]** [nghe không rõ 01:44:50; cần đối chiếu] Dù làm đi trường vào rồi nhưng mà quả nữ của hai em cần tăng cường

<a id="S00987"></a>
**[01:44:54 → 01:44:55] [Người nói?]** [nghe không rõ 01:44:54; cần đối chiếu] Sáng này ai cũng mới xong

<a id="S00988"></a>
**[01:44:56 → 01:45:07] [Người nói?]** [nghe không rõ 01:44:56; cần đối chiếu] Tiếng Anh học thuật thì em cũng ok nhưng mà để mà nói chuyên ngành thì cũng hiếm

<a id="S00989"></a>
**[01:45:22 → 01:45:45] [Người nói?]** [nghe không rõ 01:45:22; cần đối chiếu] Hãy subscribe cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

<a id="S00990"></a>
**[01:45:52 → 01:46:03] [Người nói?]** [nghe không rõ 01:45:52; cần đối chiếu] Tập ra 1, 2 lần học thảo cũng là quen và chỉ để có kinh ngạc du lịch.

<a id="S00991"></a>
**[01:46:05 → 01:46:09] [Người nói?]** [nghe không rõ 01:46:05; cần đối chiếu] Nếu mình đã biết là học thảo quen thì bài thảo khác cũng rất là dễ lấy.

<a id="S00992"></a>
**[01:46:10 → 01:46:13] [Người nói?]** [nghe không rõ 01:46:10; cần đối chiếu] Nếu mình đã được một bài thảo chính quen thì sao các bài thảo chính khác cũng rất dễ.

<a id="S00993"></a>
**[01:46:14 → 01:46:16] [Người nói?]** [nghe không rõ 01:46:14; cần đối chiếu] Cũng giải thích được điều đó nhưng nó là sự ngạc.

<a id="S00994"></a>
**[01:46:16 → 01:46:19] [Người nói?]** [nghe không rõ 01:46:16; cần đối chiếu] Đấy là sự ngạc.

<a id="S00995"></a>
**[01:46:20 → 01:46:23] [Người nói?]** [nghe không rõ 01:46:20; cần đối chiếu] Như Lam biết học thảo trong nước ok rồi đúng không?

<a id="S00996"></a>
**[01:46:23 → 01:46:26] [Người nói?]** [nghe không rõ 01:46:23; cần đối chiếu] Nhưng nếu em cố được bài thảo chính thì sau đó các bài thảo chính em sẽ...

<a id="S00997"></a>
**[01:46:37 → 01:46:48] [Người nói?]** [nghe không rõ 01:46:37; cần đối chiếu] Lúc đầu rất là khó khăn nhé, tạp chí gọi là quay đi quay lại mãi nhưng mà nếu chỉ cần mua lần vào thì lần sau sẽ rất là xếp

<a id="S00998"></a>
**[01:46:53 → 01:46:56] [Người nói?]** [nghe không rõ 01:46:53; cần đối chiếu] Hiển thị lần này vào cái lần sau nghe cũng tùy tới

<a id="S00999"></a>
**[01:47:01 → 01:47:04] [Người nói?]** [nghe không rõ 01:47:01; cần đối chiếu] Vừa rồi Tùng viết cái bài tạp chí của mình thấy nó khác hẳn với tạp chí đúng không?

<a id="S01000"></a>
**[01:47:06 → 01:47:06] [Người nói?]** [nghe không rõ 01:47:06; cần đối chiếu] Đúng

<a id="S01001"></a>
**[01:47:11 → 01:47:11] [Người nói?]** [nghe không rõ 01:47:11; cần đối chiếu] Các hẳn luôn

<a id="S01002"></a>
**[01:47:13 → 01:47:20] [Người nói?]** [nghe không rõ 01:47:13; cần đối chiếu] Nhưng mà mình vẫn đoán các em là đối với tạp chí, cái người cộng với Tập thì khi ta đăng những bài các em thì người tạp chí bắt được đúng từ một từ khoá

<a id="S01003"></a>
**[01:47:22 → 01:47:30] [Người nói?]** [nghe không rõ 01:47:22; cần đối chiếu] Cái mới đó là cái gì? Cái mới đó là nếu chúng ta bắt được phản ánh của mình thì người ta sẽ rất ok với mình, người ta sẽ cho đi phản biệt.

<a id="S01004"></a>
**[01:47:30 → 01:47:36] [Người nói?]** [nghe không rõ 01:47:30; cần đối chiếu] Còn nếu chúng ta không bắt được người ta nghĩ là chỉ là ông Sáu đó làm cái kia kia là xong.

<a id="S01005"></a>
**[01:47:36 → 01:47:39] [Người nói?]** [nghe không rõ 01:47:36; cần đối chiếu] Thì người ta sẽ cho mình một bạch ngay ở góc an ra.

<a id="S01006"></a>
**[01:47:39 → 01:47:48] [Người nói?]** [nghe không rõ 01:47:39; cần đối chiếu] Thế thôi. Cái cảnh này em biết là thời buổi AI bài xong biết liên tục nhiều lắm.

<a id="S01007"></a>
**[01:48:14 → 01:48:14] [Người nói?]** [nghe không rõ 01:48:14; cần đối chiếu] Thoa rồi.

<a id="S01008"></a>
**[01:48:15 → 01:48:17] [Người nói?]** [nghe không rõ 01:48:15; cần đối chiếu] Thoa rồi còn mình xác tổng Covid rồi.

<a id="S01009"></a>
**[01:48:17 → 01:48:21] [Người nói?]** [nghe không rõ 01:48:17; cần đối chiếu] Không biết là Covid không, tự dưng một ngày là tự dưng một ngày.

<a id="S01010"></a>
**[01:48:21 → 01:48:24] [Người nói?]** [nghe không rõ 01:48:21; cần đối chiếu] Mình cũng đã từng Covid được cách đây nhưng mà hôm nay tự dưng Covid không.

<a id="S01011"></a>
**[01:48:24 → 01:48:26] [Người nói?]** [nghe không rõ 01:48:24; cần đối chiếu] Em bị ướt mười ngày rồi.

<a id="S01012"></a>
**[01:48:26 → 01:48:30] [Người nói?]** [nghe không rõ 01:48:26; cần đối chiếu] Mình không xuyên nghiệp nhưng mà chịu chứng mình thấy đối với Covid ngày xưa mình bị quả không?

<a id="S01013"></a>
**[01:48:31 → 01:48:35] [Người nói?]** [nghe không rõ 01:48:31; cần đối chiếu] Em ho là do. Em có bị trước nhỉ lấy, khi hồng nó...

<a id="S01014"></a>
**[01:48:35 → 01:48:40] [Người nói?]** [nghe không rõ 01:48:35; cần đối chiếu] Vì em hồng thì nó mưa hồng...

<a id="S01015"></a>
**[01:48:40 → 01:48:42] [Người nói?]** [nghe không rõ 01:48:40; cần đối chiếu] Tôi nghĩ chắc em bắn bóng thôi cho máy thôi.

<a id="S01016"></a>
**[01:48:45 → 01:48:46] [Người nói?]** [nghe không rõ 01:48:45; cần đối chiếu] Cho thầy quán ra cho thầy xem.

<a id="S01017"></a>
**[01:48:46 → 01:48:48] [Người nói?]** [nghe không rõ 01:48:46; cần đối chiếu] Đi máy.

<a id="S01018"></a>
**[01:48:50 → 01:48:51] [Người nói?]** [nghe không rõ 01:48:50; cần đối chiếu] Nên thầy không đi xe nữa.

<a id="S01019"></a>
**[01:48:53 → 01:48:54] [Người nói?]** [nghe không rõ 01:48:53; cần đối chiếu] Nên thầy không đi xe nữa.

<a id="S01020"></a>
**[01:48:56 → 01:49:02] [Người nói?]** [nghe không rõ 01:48:56; cần đối chiếu] Tưởng thấy chung này ra đi sớm và thầy ngồi vào người trước

<a id="S01021"></a>
**[01:49:02 → 01:49:04] [Người nói?]** [nghe không rõ 01:49:02; cần đối chiếu] Thầy bảo thầy đang ở tận đâu ấy

<a id="S01022"></a>
**[01:49:04 → 01:49:07] [Người nói?]** [nghe không rõ 01:49:04; cần đối chiếu] Cho mình một tiếng ngồi vì thế

<a id="S01023"></a>
**[01:49:07 → 01:49:08] [Người nói?]** [nghe không rõ 01:49:07; cần đối chiếu] Chúng ta nhận được một quán

<a id="S01024"></a>
**[01:49:08 → 01:49:15] [Người nói?]** [nghe không rõ 01:49:08; cần đối chiếu] Và sau đó cái gì ấy

<a id="S01025"></a>
**[01:49:15 → 01:49:20] [Người nói?]** [nghe không rõ 01:49:15; cần đối chiếu] Hôm vừa thầy Trung còn nói

<a id="S01026"></a>
**[01:49:20 → 01:49:22] [Người nói?]** [nghe không rõ 01:49:20; cần đối chiếu] Đi đâu thì đi tìm bà vi hay sao

<a id="S01027"></a>
**[01:49:22 → 01:49:23] [Người nói?]** [nghe không rõ 01:49:22; cần đối chiếu] Đi trong này thôi chứ

<a id="S01028"></a>
**[01:49:23 → 01:49:25] [Người nói?]** [nghe không rõ 01:49:23; cần đối chiếu] Không phải ngồi ở nhà một đấy

<a id="S01029"></a>
**[01:49:25 → 01:49:26] [Người nói?]** [nghe không rõ 01:49:25; cần đối chiếu] Đi đi

<a id="S01030"></a>
**[01:49:26 → 01:49:27] [Người nói?]** [nghe không rõ 01:49:26; cần đối chiếu] Chứ anh ngồi bên hồn

<a id="S01031"></a>
**[01:49:27 → 01:49:29] [Người nói?]** [nghe không rõ 01:49:27; cần đối chiếu] Anh ngồi bên hồn kia

<a id="S01032"></a>
**[01:49:29 → 01:49:32] [Người nói?]** [nghe không rõ 01:49:29; cần đối chiếu] Anh ngồi bên hồn

<a id="S01033"></a>
**[01:49:32 → 01:49:37] [Người nói?]** [nghe không rõ 01:49:32; cần đối chiếu] Anh ngồi bên hồn

<a id="S01034"></a>
**[01:49:38 → 01:49:46] [Người nói?]** [nghe không rõ 01:49:38; cần đối chiếu] Hãy subscribe cho kênh La La School Để không bỏ lỡ những video hấp dẫn

<a id="S01035"></a>
**[01:50:51 → 01:50:57] [Người nói?]** [nghe không rõ 01:50:51; cần đối chiếu] báo cáo cũng

<a id="S01036"></a>
**[01:51:03 → 01:51:07] [Người nói?]** [nghe không rõ 01:51:03; cần đối chiếu] Cũng thầy hơi gấp

<a id="S01037"></a>
**[01:51:09 → 01:51:10] [Người nói?]** [nghe không rõ 01:51:09; cần đối chiếu] Nhưng ông đấy là

<a id="S01038"></a>
**[01:51:10 → 01:51:12] [Người nói?]** [nghe không rõ 01:51:10; cần đối chiếu] Một thầy về ông đấy là

<a id="S01039"></a>
**[01:51:12 → 01:51:14] [Người nói?]** [nghe không rõ 01:51:12; cần đối chiếu] Thầy nhục phó là phải

<a id="S01040"></a>
**[01:51:15 → 01:51:16] [Người nói?]** [nghe không rõ 01:51:15; cần đối chiếu] Phải đợi gần

<a id="S01041"></a>
**[01:51:16 → 01:51:17] [Người nói?]** [nghe không rõ 01:51:16; cần đối chiếu] Nghĩa là hẹn từ sáng

<a id="S01042"></a>
**[01:51:17 → 01:51:19] [Người nói?]** [nghe không rõ 01:51:17; cần đối chiếu] Cuối cùng là cứ đẩy lùi 1 tiếng dần

<a id="S01043"></a>
**[01:51:19 → 01:51:21] [Người nói?]** [nghe không rõ 01:51:19; cần đối chiếu] Đến 4h mới báo cáo được

<a id="S01044"></a>
**[01:51:22 → 01:51:24] [Người nói?]** [nghe không rõ 01:51:22; cần đối chiếu] Thế là ông đấy là em đến trường từ 8h

<a id="S01045"></a>
**[01:51:24 → 01:51:25] [Người nói?]** [nghe không rõ 01:51:24; cần đối chiếu] Xong cứ ngồi dưới thư viện

<a id="S01046"></a>
**[01:51:25 → 01:51:27] [Người nói?]** [nghe không rõ 01:51:25; cần đối chiếu] Đến 4h tư

<a id="S01047"></a>
**[01:51:28 → 01:51:29] [Người nói?]** [nghe không rõ 01:51:28; cần đối chiếu] Xong rồi

<a id="S01048"></a>
**[01:51:31 → 01:51:33] [Người nói?]** [nghe không rõ 01:51:31; cần đối chiếu] Các cô lùi xuống 3h30

<a id="S01049"></a>
**[01:51:33 → 01:51:34] [Người nói?]** [nghe không rõ 01:51:33; cần đối chiếu] Là chốt

<a id="S01050"></a>
**[01:51:34 → 01:51:36] [Người nói?]** [nghe không rõ 01:51:34; cần đối chiếu] Xong rồi ngồi đến 4 giờ thì thầy mới xong

<a id="S01051"></a>
**[01:51:36 → 01:51:41] [Người nói?]** [nghe không rõ 01:51:36; cần đối chiếu] Đấy là may mà em còn được báo cáo sớm

<a id="S01052"></a>
**[01:51:41 → 01:51:46] [Người nói?]** [nghe không rõ 01:51:41; cần đối chiếu] Còn lớp em là tự nhiên là đang nói là đến tháng 12 là báo cáo

<a id="S01053"></a>
**[01:51:46 → 01:51:48] [Người nói?]** [nghe không rõ 01:51:46; cần đối chiếu] Đẩy luôn hành đến tháng 10 báo cáo

<a id="S01054"></a>
**[01:51:48 → 01:51:50] [Người nói?]** [nghe không rõ 01:51:48; cần đối chiếu] Bạn, bao nhiêu người đang chết

<a id="S01055"></a>
**[01:51:50 → 01:51:51] [Người nói?]** [nghe không rõ 01:51:50; cần đối chiếu] Tuần sau là cũng đợi báo cáo

<a id="S01056"></a>
**[01:51:51 → 01:51:53] [Người nói?]** [nghe không rõ 01:51:51; cần đối chiếu] À vâng, tuần sau là đã phải ngồi

<a id="S01057"></a>
**[01:51:54 → 01:51:56] [Người nói?]** [nghe không rõ 01:51:54; cần đối chiếu] Kiểu vừa thông báo còn đúng 5 ngày nộp

<a id="S01058"></a>
**[01:51:56 → 01:52:00] [Người nói?]** [nghe không rõ 01:51:56; cần đối chiếu] Nên là bao nhiêu người đang đi công tác xa phải ngủi hết

<a id="S01059"></a>
**[01:52:00 → 01:52:02] [Người nói?]** [nghe không rõ 01:52:00; cần đối chiếu] Đang hơi loạn

<a id="S01060"></a>
**[01:52:02 → 01:52:04] [Người nói?]** [nghe không rõ 01:52:02; cần đối chiếu] Làm cái trường này có quyết định đi học chưa?

<a id="S01061"></a>
**[01:52:41 → 01:53:03] [Người nói?]** [nghe không rõ 01:52:41; cần đối chiếu] hãy subscribe cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

<a id="S01062"></a>
**[01:53:06 → 01:56:14] [Người nói?]** [nghe không rõ 01:53:06; cần đối chiếu] Các bạn có thể nhìn thấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể lấy tổng tiểu của ông cũng có thể l

<a id="S01063"></a>
**[01:56:14 → 01:56:23] [Người nói?]** [nghe không rõ 01:56:14; cần đối chiếu] Vậy là sao anh sử dụng được cái mô hình tính tác để giải quyết các cái đặc biệt của những loại vật xong?

<a id="S01064"></a>
**[01:56:32 → 01:56:34] [Người nói?]** [nghe không rõ 01:56:32; cần đối chiếu] Em ạ, em bảo thầy...

<a id="S01065"></a>
**[01:56:34 → 01:56:35] [Người nói?]** [nghe không rõ 01:56:34; cần đối chiếu] Khá giống với ba lô hình này mà.

<a id="S01066"></a>
**[01:56:35 → 01:56:36] [Người nói?]** [nghe không rõ 01:56:35; cần đối chiếu] Em bảo...

<a id="S01067"></a>
**[01:56:36 → 01:56:41] [Người nói?]** [nghe không rõ 01:56:36; cần đối chiếu] Để bảo sát anh bảo lại, chắc anh dùng ba lô lừa quá, chắc là mấy anh em nhìn nó che thế nào đấy.

<a id="S01068"></a>
**[01:56:42 → 01:56:48] [Người nói?]** [nghe không rõ 01:56:42; cần đối chiếu] Em bảo bảo với thầy cái ba lô đấy là em gửi Nam chọn, thấy hả?

<a id="S01069"></a>
**[01:56:48 → 01:56:52] [Người nói?]** [nghe không rõ 01:56:48; cần đối chiếu] Đấy, em gửi Nam chọn và ngươi đi trực tiếp ra cái hang của bạn Nam.

<a id="S01070"></a>
**[01:57:01 → 01:57:42] [Người nói?]** [nghe không rõ 01:57:01; cần đối chiếu] Hãy subscribe cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

<a id="S01071"></a>
**[01:57:43 → 01:57:47] [Người nói?]** [nghe không rõ 01:57:43; cần đối chiếu] Thầy là màu xanh navi, em cũng thuộc màng đấy

<a id="S01072"></a>
**[01:57:48 → 01:57:50] [Người nói?]** [nghe không rõ 01:57:48; cần đối chiếu] Thầy thấy đồ của em toàn là màu ấy

<a id="S01073"></a>
**[01:57:51 → 01:57:54] [Người nói?]** [nghe không rõ 01:57:51; cần đối chiếu] Tất cả điện thoại cố gắng là được màu đấy

<a id="S01074"></a>
**[01:57:55 → 01:57:59] [Người nói?]** [nghe không rõ 01:57:55; cần đối chiếu] Cho nên khi chọn cái tuổi đẹp thầy nó cũng khá là sáng

<a id="S01075"></a>
**[01:57:59 → 01:58:03] [Người nói?]** [nghe không rõ 01:57:59; cần đối chiếu] Nó sáng và nó cũng khá là tự động như màu hình này đúng không anh?

<a id="S01076"></a>
**[01:58:03 → 01:58:06] [Người nói?]** [nghe không rõ 01:58:03; cần đối chiếu] Chứ chứa hỏng thì làm sao bỏ đây?

<a id="S01077"></a>
**[01:58:08 → 01:58:09] [Người nói?]** [nghe không rõ 01:58:08; cần đối chiếu] Chứa hỏng

<a id="S01078"></a>
**[01:58:09 → 01:58:11] [Người nói?]** [nghe không rõ 01:58:09; cần đối chiếu] Em bảo cầu thầy này

<a id="S01079"></a>
**[01:58:11 → 01:58:15] [Người nói?]** [nghe không rõ 01:58:11; cần đối chiếu] Tôi đã từng có một quan điểm rằng là

<a id="S01080"></a>
**[01:58:15 → 01:58:17] [Người nói?]** [nghe không rõ 01:58:15; cần đối chiếu] Cứ như cái nào khi đến học thì ấy

<a id="S01081"></a>
**[01:58:17 → 01:58:19] [Người nói?]** [nghe không rõ 01:58:17; cần đối chiếu] Nhưng mà bây giờ dùng đồ thầy

<a id="S01082"></a>
**[01:58:19 → 01:58:22] [Người nói?]** [nghe không rõ 01:58:19; cần đối chiếu] Kể cả áo quân em thấy

<a id="S01083"></a>
**[01:58:22 → 01:58:24] [Người nói?]** [nghe không rõ 01:58:22; cần đối chiếu] Cứ có cái người đó mình sử dụng cả

<a id="S01084"></a>
**[01:58:24 → 01:58:25] [Người nói?]** [nghe không rõ 01:58:24; cần đối chiếu] Cứ dùng là thầy

<a id="S01085"></a>
**[01:58:25 → 01:58:27] [Người nói?]** [nghe không rõ 01:58:25; cần đối chiếu] Không thể chờ được

<a id="S01086"></a>
**[01:58:27 → 01:58:28] [Người nói?]** [nghe không rõ 01:58:27; cần đối chiếu] Có những thứ không thể chờ được

<a id="S01087"></a>
**[01:58:29 → 01:58:32] [Người nói?]** [nghe không rõ 01:58:29; cần đối chiếu] Nói cho các bạn là cái ví thầy nhé

<a id="S01088"></a>
**[01:58:32 → 01:58:34] [Người nói?]** [nghe không rõ 01:58:32; cần đối chiếu] Mình mới thay nhưng mà

<a id="S01089"></a>
**[01:58:34 → 01:58:36] [Người nói?]** [nghe không rõ 01:58:34; cần đối chiếu] Mình dùng cái ví trước nó là

<a id="S01090"></a>
**[01:58:36 → 01:58:37] [Người nói?]** [nghe không rõ 01:58:36; cần đối chiếu] 15 năm

<a id="S01091"></a>
**[01:59:21 → 01:59:23] [Người nói?]** [nghe không rõ 01:59:21; cần đối chiếu] Quân của em đi từ khi

<a id="S01092"></a>
**[01:59:23 → 01:59:29] [Người nói?]** [nghe không rõ 01:59:23; cần đối chiếu] Thêm điểm khi ở OM, 10 thi quân thì mau đấy

<a id="S01093"></a>
**[01:59:29 → 01:59:34] [Người nói?]** [nghe không rõ 01:59:29; cần đối chiếu] Thế là OM nó khắc bó, nó huy động từ Hải Phong, từ Hải Dương lên

<a id="S01094"></a>
**[01:59:36 → 01:59:43] [Người nói?]** [nghe không rõ 01:59:36; cần đối chiếu] Chân ra riêng, tụi bé mới toan đúng màu ấy

<a id="S01095"></a>
**[01:59:43 → 01:59:46] [Người nói?]** [nghe không rõ 01:59:43; cần đối chiếu] Hôm trước là màu này ạ, lúc đầu là 2 em bạn này

<a id="S01096"></a>
**[01:59:46 → 01:59:47] [Người nói?]** [nghe không rõ 01:59:46; cần đối chiếu] Màu này ạ

<a id="S01097"></a>
**[01:59:47 → 01:59:49] [Người nói?]** [nghe không rõ 01:59:47; cần đối chiếu] Đấy, màu này là màu Navi tên thôi

<a id="S01098"></a>
**[01:59:49 → 01:59:52] [Người nói?]** [nghe không rõ 01:59:49; cần đối chiếu] Đấy, cái màu này tại mình tên đẹp rồi đấy

<a id="S01099"></a>
**[01:59:52 → 01:59:58] [Người nói?]** [nghe không rõ 01:59:52; cần đối chiếu] Và sao mình cứ bảo là tại ông dùng nhiều cái đấy quá, mọi người chú ý

<a id="S01100"></a>
**[01:59:58 → 01:59:59] [Người nói?]** [nghe không rõ 01:59:58; cần đối chiếu] Hãy subscribe cho kênh La La School Để không bỏ lỡ

<a id="S01101"></a>
**[02:00:00 → 02:00:03] [Người nói?]** [nghe không rõ 02:00:00; cần đối chiếu] 2 em tìm tính là thay cái túi để cái pick

<a id="S01102"></a>
**[02:00:03 → 02:00:06] [Người nói?]** [nghe không rõ 02:00:03; cần đối chiếu] nhưng mà màu trắng hết rồi

<a id="S01103"></a>
**[02:00:06 → 02:00:09] [Người nói?]** [nghe không rõ 02:00:06; cần đối chiếu] nhưng mà em lại sợ giấy nó bằng màu trắng

<a id="S01104"></a>
**[02:00:09 → 02:00:10] [Người nói?]** [nghe không rõ 02:00:09; cần đối chiếu] cả từ 2 năm ra rồi

<a id="S01105"></a>
**[02:00:11 → 02:00:14] [Người nói?]** [nghe không rõ 02:00:11; cần đối chiếu] màu trắng như kiểu mình hộp hết rồi

<a id="S01106"></a>
**[02:00:14 → 02:00:17] [Người nói?]** [nghe không rõ 02:00:14; cần đối chiếu] ngày xưa mình nói hiểu là ngày xưa trời mình còn chưa về học gần rồi này

<a id="S01107"></a>
**[02:00:17 → 02:00:19] [Người nói?]** [nghe không rõ 02:00:17; cần đối chiếu] là mình cũng toàn dùng cặp thôi

<a id="S01108"></a>
**[02:00:21 → 02:00:22] [Người nói?]** [nghe không rõ 02:00:21; cần đối chiếu] giống như vẫn là

<a id="S01109"></a>
**[02:00:22 → 02:00:25] [Người nói?]** [nghe không rõ 02:00:22; cần đối chiếu] sau một hồi mình thấy nó không tiện lắm

<a id="S01110"></a>
**[02:00:25 → 02:00:29] [Người nói?]** [nghe không rõ 02:00:25; cần đối chiếu] cái ba lô mình thấy đúng nhiều thứ hơn là cặp

<a id="S01111"></a>
**[02:00:31 → 02:00:36] [Người nói?]** [nghe không rõ 02:00:31; cần đối chiếu] Thế thì 2 anh em bảo phải mua một cái gì đấy mà thầy có thể ra dùng trước

<a id="S01112"></a>
**[02:00:37 → 02:00:42] [Người nói?]** [nghe không rõ 02:00:37; cần đối chiếu] Ví dụ như cái bá lô mà anh em đang thay ấy là thầy có thể bỏ kích vào trong đấy cũng được

<a id="S01113"></a>
**[02:00:42 → 02:00:46] [Người nói?]** [nghe không rõ 02:00:42; cần đối chiếu] Vừa đựng được, kể cả laptop cũng được mà đi đâu cũng có thể đi

<a id="S01114"></a>
**[02:00:46 → 02:00:49] [Người nói?]** [nghe không rõ 02:00:46; cần đối chiếu] Thì nó mới phù hợp

<a id="S01115"></a>
**[02:00:54 → 02:00:58] [Người nói?]** [nghe không rõ 02:00:54; cần đối chiếu] Nhưng mà anh em có nghĩ là nếu như có thể nổi thay như 1 trẻ

<a id="S01116"></a>
**[02:00:58 → 02:00:59] [Người nói?]** [nghe không rõ 02:00:58; cần đối chiếu] Nó cũng phải trân thủ ra

<a id="S01117"></a>
**[02:00:59 → 02:01:01] [Người nói?]** [nghe không rõ 02:00:59; cần đối chiếu] Nên không thể để được

<a id="S01118"></a>
**[02:01:20 → 02:02:05] [Người nói?]** [nghe không rõ 02:01:20; cần đối chiếu] Các bạn hãy đăng ký kênh để ủng hộ kênh của mình nhé.

<a id="S01119"></a>
**[02:02:05 → 02:02:08] [Người nói?]** [nghe không rõ 02:02:05; cần đối chiếu] Các bạn có thể thay đổi quy chế của thầy Phó với quy chế của bộ?

<a id="S01120"></a>
**[02:02:08 → 02:02:15] [Người nói?]** [nghe không rõ 02:02:08; cần đối chiếu] Chắc là có quy chế của thầy Phó.

<a id="S01121"></a>
**[02:02:16 → 02:02:18] [Người nói?]** [nghe không rõ 02:02:16; cần đối chiếu] Đúng ạ, có quy chế của thầy Phó.

<a id="S01122"></a>
**[02:02:19 → 02:02:24] [Người nói?]** [nghe không rõ 02:02:19; cần đối chiếu] Thầy Phó có khả năng sẽ rời đi, thay đổi quy chế của thầy Phó.

<a id="S01123"></a>
**[02:02:24 → 02:02:27] [Người nói?]** [nghe không rõ 02:02:24; cần đối chiếu] Không, quy chế của bộ thì khó chứ gì.

<a id="S01124"></a>
**[02:02:28 → 02:02:30] [Người nói?]** [nghe không rõ 02:02:28; cần đối chiếu] Không, quy chế của bộ thì khó chứ gì.

<a id="S01125"></a>
**[02:02:31 → 02:02:32] [Người nói?]** [nghe không rõ 02:02:31; cần đối chiếu] Không, quy chế của bộ thì khó chứ gì.

<a id="S01126"></a>
**[02:02:32 → 02:02:39] [Người nói?]** [nghe không rõ 02:02:32; cần đối chiếu] Em nghĩ là yêu cầu về tuyển sinh, nghiên cứu sinh sẽ thay đổi khá nhiều.

<a id="S01127"></a>
**[02:02:39 → 02:03:04] [Người nói?]** [nghe không rõ 02:02:39; cần đối chiếu] Hãy subscribe cho kênh La La School Để không bỏ lỡ những video hấp dẫn
