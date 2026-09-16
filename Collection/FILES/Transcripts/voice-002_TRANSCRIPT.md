# Voice 002 — hội thoại về AI trong an toàn thông tin, WAF mã nguồn mở và kế hoạch bảo vệ đề tài

Nguồn: [Voice 002.m4a](file:///C:/Users/Admin/Documents/Second%20Brain/%CE%A9/FILES/Recording/Voice%20002.m4a)

Thời lượng: 00:40:03. ASR: large-v3 / cuda.

Trạng thái: đã rà văn bản; chờ nghe đối chiếu. Người nói chưa được xác định nếu không có ghi chú riêng.
Bản này bảo toàn thứ tự và nội dung nhận dạng; các đoạn nghi lỗi được giữ dấu vết để nghe lại.

## Bài toán tiết kiệm token và hiệu năng cho phân tích log

<a id="S00001"></a>
**[00:00:00 → 00:00:04] [Người nói?]** Nên thế là cũng đấu tranh rồi, cũng thấy có lợi.

<a id="S00002"></a>
**[00:00:04 → 00:00:09] [Người nói?]** Cái data của em là cái gì?

<a id="S00003"></a>
**[00:00:10 → 00:00:12] [Người nói?]** Cái data em bị outdated.

<a id="S00004"></a>
**[00:00:12 → 00:00:15] [Người nói?]** Cái data của em là cũng không ra dữ liệu.

<a id="S00005"></a>
**[00:00:16 → 00:00:17] [Người nói?]** Nghĩa là kiểu để...

<a id="S00006"></a>
**[00:00:18 → 00:00:22] [Người nói?]** Nghĩa là nếu dùng AI thì nó chỉ học được khoảng 80% thôi.

<a id="S00007"></a>
**[00:00:23 → 00:00:28] [Người nói?]** Thì nó sẽ không học được 20% cái kiểu đặc biệt hơn, kiểu mẫu dài hơn hoặc là...

<a id="S00008"></a>
**[00:00:28 → 00:00:33] [Người nói?]** Nó sẽ phải yêu cầu phải đánh theo keyword, nó phải dài hơn.

<a id="S00009"></a>
**[00:00:33 → 00:00:38] [Người nói?]** Ví dụ như là bình thường các từ như SELECT sẽ đánh luôn chẳng hạn

<a id="S00010"></a>
**[00:00:38 → 00:00:41] [Người nói?]** Nhưng mà một số cụm là nó sẽ không đánh

<a id="S00011"></a>
**[00:00:41 → 00:00:45] [Người nói?]** Thì nó sẽ phải gồm nhiều một cụm nó dài hơn hơn nữa

<a id="S00012"></a>
**[00:00:45 → 00:00:46] [Người nói?]** Cái cụm mà khai thác là đưa lên

<a id="S00013"></a>
**[00:00:47 → 00:00:50] [Người nói?]** Thì bây giờ là AI nó có khả năng suy luận ra về cái đấy rồi

<a id="S00014"></a>
**[00:00:51 → 00:00:52] [Người nói?]** Hay là bây giờ mục tiêu là ngược lại

<a id="S00015"></a>
**[00:00:52 → 00:00:55] [Người nói?]** Là đằng nào AI đã làm được rồi bây giờ mình phải tạo ra một cái mô đun nhỏ

<a id="S00016"></a>
**[00:00:57 → 00:01:01] [Người nói?]** Để cho là AI không phải đưa toàn bộ tất cả các Log qua AI nữa

<a id="S00017"></a>
**[00:01:01 → 00:01:04] [Người nói?]** không nói rất tốn token đấy cả, nó rất là nặng

<a id="S00018"></a>
**[00:01:04 → 00:01:06] [Người nói?]** Token bây giờ không cần nghĩ đến làm gì

<a id="S00019"></a>
**[00:01:07 → 00:01:10] [Người nói?]** Đi đi anh, bởi vì bây giờ là gửi hơn 10 triệu request

<a id="S00020"></a>
**[00:01:10 → 00:01:13] [Người nói?]** và 10 triệu request đấy đều phải đưa

<a id="S00021"></a>
**[00:01:13 → 00:01:16] [Người nói?]** đầu tiên là sẽ đưa qua đánh checklist, đánh check keyword

<a id="S00022"></a>
**[00:01:17 → 00:01:20] [Người nói?]** rồi mới bắt đầu đưa tiếp là lúc đấy vẫn còn hơn 100 nghìn

<a id="S00023"></a>
**[00:01:20 → 00:01:23] [Người nói?]** thì nếu mà tiếp tục AI thì nó sẽ tốn rất nhiều tiền

<a id="S00024"></a>
**[00:01:23 → 00:01:27] [Người nói?]** thì bây giờ phải tạo một cái mô đun nhỏ để nó giảm hiểu cái đồng đấy trước khi đi tiếp

<a id="S00025"></a>
**[00:01:28 → 00:01:33] [Người nói?]** kiểu đưa qua một con AI đần hơn nhưng mà nhỏ hơn và chuyên biệt hơn

<a id="S00026"></a>
**[00:01:33 → 00:01:36] [Người nói?]** sau đó mới đưa con Cloud, bởi vì hầu hết giờ là chỉ có Cloud thôi

<a id="S00027"></a>
**[00:01:38 → 00:01:49] [Người nói?]** nếu mà anh dùng con 200$ cho anh, con đấy nó có con Fable

<a id="S00028"></a>
**[00:01:51 → 00:01:57] [Người nói?]** con đấy là nó được loại bỏ bớt những cái tiêu chuẩn về an toàn thông tin

<a id="S00029"></a>
**[00:01:57 → 00:02:02] [Người nói?]** [nghe không rõ 00:01:57; cần đối chiếu] Nên là nó mới kiểu tình thường là đưa payload vào là nó sẽ thưởng thực thi luôn

<a id="S00030"></a>
**[00:02:02 → 00:02:07] [Người nói?]** [nghe không rõ 00:02:02; cần đối chiếu] Còn Fable nó có mấy cái tiêu chuẩn nó khá thông minh nên là nó khả năng suy luận nó tốt

<a id="S00031"></a>
**[00:02:09 → 00:02:13] [Người nói?]** [nghe không rõ 00:02:09; cần đối chiếu] Nhưng mà con đấy ai mà đi thi Bounty là auto phải luôn

<a id="S00032"></a>
**[00:02:13 → 00:02:18] [Người nói?]** [nghe không rõ 00:02:13; cần đối chiếu] Mình mua gói 100$ thôi vì anh chỉ cần 50$ là đủ

<a id="S00033"></a>
**[00:02:18 → 00:02:21] [Người nói?]** [nghe không rõ 00:02:18; cần đối chiếu] 20$ thì hơi nhiều mà anh mới nghe nói là 20$ đấy là 20$ theo quần

<a id="S00034"></a>
**[00:02:21 → 00:02:23] [Người nói?]** [nghe không rõ 00:02:21; cần đối chiếu] Vâng đúng rồi anh

<a id="S00035"></a>
**[00:02:23 → 00:02:24] [Người nói?]** [nghe không rõ 00:02:23; cần đối chiếu] À 20$ theo 5 tiếng

<a id="S00036"></a>
**[00:02:25 → 00:02:32] [Người nói?]** bỏ bỏ luôn nếu mà anh mua không nghĩa là anh sẽ không có giới hạn tuần ai không có giới hạn theo

<a id="S00037"></a>
**[00:02:32 → 00:02:38] [Người nói?]** giờ nữa anh chỉ có dạng phần thôi thế là mấy em từ 5 đến 5 5 5 tiếng người được thành hành

<a id="S00038"></a>
**[00:02:38 → 00:02:42] [Người nói?]** với 5 tiếng đấy không dùng hết đâu không không dùng hết đây anh nếu mà anh thì bao Nếu mà anh

<a id="S00039"></a>
**[00:02:42 → 00:02:53] [Người nói?]** làm bao bác bao ti là sẽ hết bác bao ti là anh anh em là dùng là hết chắc là hết lúc đầu em tưởng

<a id="S00040"></a>
**[00:02:53 → 00:02:56] [Người nói?]** Thấy bỏ ra gần 10 triệu là anh định xài ké

<a id="S00041"></a>
**[00:02:56 → 00:03:04] [Người nói?]** Anh nghe là 200 một người dùng vẫn hết

<a id="S00042"></a>
**[00:03:04 → 00:03:06] [Người nói?]** Bởi vì là Bắc Bạc Ti

<a id="S00043"></a>
**[00:03:06 → 00:03:08] [Người nói?]** Bắc Bạc Ti là nó kiểu

<a id="S00044"></a>
**[00:03:08 → 00:03:11] [Người nói?]** Nó xà vào, nó ôm hết cả cái đồng đấy

<a id="S00045"></a>
**[00:03:12 → 00:03:13] [Người nói?]** Thì đương nhiên là

<a id="S00046"></a>
**[00:03:13 → 00:03:15] [Người nói?]** Anh ấy vẫn sẽ đưa logic vào nhưng mà không tối ưu được

<a id="S00047"></a>
**[00:03:15 → 00:03:19] [Người nói?]** Mấy em cũng không ít

<a id="S00048"></a>
**[00:03:22 → 00:03:23] [Người nói?]** Nó đang quay vào đó

<a id="S00049"></a>
**[00:03:23 → 00:03:26] [Người nói?]** Có nghĩa là

<a id="S00050"></a>
**[00:03:26 → 00:03:27] [Người nói?]** Cục thi nghìn đô

<a id="S00051"></a>
**[00:03:27 → 00:03:30] [Người nói?]** Bỏ 200 là cũng lời

<a id="S00052"></a>
**[00:03:31 → 00:03:32] [Người nói?]** 275 triệu

<a id="S00053"></a>
**[00:03:32 → 00:03:34] [Người nói?]** Là 7 triệu 8

<a id="S00054"></a>
**[00:03:34 → 00:03:35] [Người nói?]** 20 triệu nào

<a id="S00055"></a>
**[00:03:35 → 00:03:37] [Người nói?]** Thì là gần 10 triệu đi anh

<a id="S00056"></a>
**[00:03:38 → 00:03:38] [Người nói?]** 200

<a id="S00057"></a>
**[00:03:39 → 00:03:40] [Người nói?]** 211

<a id="S00058"></a>
**[00:03:40 → 00:03:41] [Người nói?]** 200

<a id="S00059"></a>
**[00:03:46 → 00:03:47] [Người nói?]** 10% ván

<a id="S00060"></a>
**[00:03:47 → 00:03:49] [Người nói?]** Anh quên

<a id="S00061"></a>
**[00:03:49 → 00:03:51] [Người nói?]** Tại vì sáng nay ngóng vừa, nhắn cho anh kìa, build vừa rồi

<a id="S00062"></a>
**[00:03:52 → 00:03:54] [Người nói?]** Vậy, thì đấy, thì bây giờ...

<a id="S00063"></a>
**[00:03:55 → 00:03:56] [Người nói?]** Từ...

## Hai hướng: mô-đun nhỏ và sinh dữ liệu cho trường hợp khó

<a id="S00064"></a>
**[00:03:57 → 00:03:59] [Người nói?]** Đúng rồi, nó thêm 10%

<a id="S00065"></a>
**[00:04:00 → 00:04:03] [Người nói?]** Thì đấy, bây giờ bài toán là tiết kiệm hiệu năng rồi

<a id="S00066"></a>
**[00:04:03 → 00:04:08] [Người nói?]** Vì gần như là cứ ném cloud với công ty một người

<a id="S00067"></a>
**[00:04:08 → 00:04:09] [Người nói?]** Nó gần như vượt trộn

<a id="S00068"></a>
**[00:04:09 → 00:04:12] [Người nói?]** Nên là bây giờ là suy ngược lại

<a id="S00069"></a>
**[00:04:13 → 00:04:14] [Người nói?]** Sử lý hai cái

<a id="S00070"></a>
**[00:04:14 → 00:04:16] [Người nói?]** Một là tạo ra một con module rất là bé

<a id="S00071"></a>
**[00:04:16 → 00:04:18] [Người nói?]** Và nó xử lý được những cái cơ bản

<a id="S00072"></a>
**[00:04:18 → 00:04:22] [Người nói?]** 2 là mình sẽ phải xử lý những cái cực kỳ khó

<a id="S00073"></a>
**[00:04:22 → 00:04:24] [Người nói?]** Nghĩa là mô hình của em phải học được

<a id="S00074"></a>
**[00:04:24 → 00:04:26] [Người nói?]** Cái cú pháp

<a id="S00075"></a>
**[00:04:26 → 00:04:27] [Người nói?]** Cái câu rất là khó

<a id="S00076"></a>
**[00:04:27 → 00:04:28] [Người nói?]** Có thật sự là tầm mô hình không?

<a id="S00077"></a>
**[00:04:29 → 00:04:29] [Người nói?]** Có chứ anh

<a id="S00078"></a>
**[00:04:30 → 00:04:31] [Người nói?]** Vì

<a id="S00079"></a>
**[00:04:32 → 00:04:37] [Người nói?]** Nhan là chỉ là xin dữ liệu

<a id="S00080"></a>
**[00:04:37 → 00:04:39] [Người nói?]** Nghĩa là bây giờ là bộ dữ liệu

<a id="S00081"></a>
**[00:04:39 → 00:04:41] [Người nói?]** Nó sẽ chỉ có 2 câu tầm công thôi

<a id="S00082"></a>
**[00:04:43 → 00:04:44] [Người nói?]** Thì nghĩa là chỉ có 2 câu tầm công thôi

<a id="S00083"></a>
**[00:04:44 → 00:04:45] [Người nói?]** Thì 2 câu tầm công đấy

<a id="S00084"></a>
**[00:04:45 → 00:04:47] [Người nói?]** Không có quá nhiều thông tin để mình học

<a id="S00085"></a>
**[00:04:47 → 00:04:49] [Người nói?]** Rồi mình sẽ sao hết tất cả lên

<a id="S00086"></a>
**[00:04:49 → 00:04:57] [Người nói?]** để cho nó cố gắng học. Ví dụ như là bây giờ em có 50 câu, trong đó chỉ có 2 câu tấn công rất là đặc biệt, rất là kiểu chuyên biệt

<a id="S00087"></a>
**[00:04:57 → 00:05:04] [Người nói?]** thì đưa vào mô hình thì nó chỉ học 48 câu còn lại, 2 câu kia nó cho rằng là thứ yếu nên nó sẽ bỏ qua.

<a id="S00088"></a>
**[00:05:04 → 00:05:11] [Người nói?]** Từ bây giờ là phải làm dầu bằng cách chỉ 2 câu đấy thôi, nhưng mà sinh ra được 50 câu rồi đưa vào thì nó sẽ chỉ tập trung vào...

## WAF mã nguồn mở: ModSecurity, Coraza, CRS và Docker

<a id="S00089"></a>
**[00:05:13 → 00:05:19] [Người nói?]** [nghe không rõ 00:05:13; cần đối chiếu] Nhưng mà hiện tại em đưa vào một tường lửa mã nguồn mở, Mode Security

<a id="S00090"></a>
**[00:05:20 → 00:05:23] [Người nói?]** [nghe không rõ 00:05:20; cần đối chiếu] Mode Security là NGX đúng không?

<a id="S00091"></a>
**[00:05:23 → 00:05:24] [Người nói?]** [nghe không rõ 00:05:23; cần đối chiếu] Dạ, NGX

<a id="S00092"></a>
**[00:05:24 → 00:05:25] [Người nói?]** [nghe không rõ 00:05:24; cần đối chiếu] Và từ giờ nó vẫn là OSI

<a id="S00093"></a>
**[00:05:25 → 00:05:30] [Người nói?]** [nghe không rõ 00:05:25; cần đối chiếu] Không, cái đấy thì em không dựng nổi, cái đấy nó dựng hơi khó

<a id="S00094"></a>
**[00:05:31 → 00:05:36] [Người nói?]** [nghe không rõ 00:05:31; cần đối chiếu] Vâng thì không, kể cả dựng Docker thì em cũng chỉ dựng được Mode Security thôi

<a id="S00095"></a>
**[00:05:39 → 00:05:45] [Người nói?]** Đang đấy nó cũng thuộc dạng trung bình, nó cũng vừa thủy khó

<a id="S00096"></a>
**[00:05:45 → 00:05:48] [Người nói?]** Em mới dựng về đấy thôi

<a id="S00097"></a>
**[00:05:48 → 00:06:01] [Người nói?]** Cora-Za, có thể dùng rule của Mod Security nhưng mà nó không có line

<a id="S00098"></a>
**[00:06:02 → 00:06:06] [Người nói?]** Em và các em có thử Cora-Za với Mod là nó phải dùng rule set chung

<a id="S00099"></a>
**[00:06:07 → 00:06:07] [Người nói?]** CRS

<a id="S00100"></a>
**[00:06:07 → 00:06:13] [Người nói?]** Còn về cơ bản là hai thằng như nhau mà thằng này được tùy chỉnh nhiều hơn

<a id="S00101"></a>
**[00:06:15 → 00:06:19] [Người nói?]** Nếu mà chuyển khai ban đầu thì dễ hơn nhưng mà nhiều cái phải setting nha

<a id="S00102"></a>
**[00:06:19 → 00:06:22] [Người nói?]** Thằng kia gọi lên phát rồi em ru cái là xong

<a id="S00103"></a>
**[00:06:23 → 00:06:26] [Người nói?]** Em mới có MDX không phải cấu hình MDX nữa

<a id="S00104"></a>
**[00:06:26 → 00:06:31] [Người nói?]** Em chưa biết anh chắc gì kì của thằng đi vào thằng Docker

<a id="S00105"></a>
**[00:06:32 → 00:06:36] [Người nói?]** Đấy thì đối với em thôi thì em chỉ cần gõ mấy code

<a id="S00106"></a>
**[00:06:36 → 00:06:44] [Người nói?]** Và thằng này thì phải custom bằng tay hơi nhiều. Như là trước thì em phải dùng lạc này, nhưng mà sau phát hiện là docker liên kết với chắc gì thì thế là thôi.

<a id="S00107"></a>
**[00:06:45 → 00:06:47] [Người nói?]** Docker là có mcp đúng không?

<a id="S00108"></a>
**[00:06:48 → 00:06:53] [Người nói?]** Đúng rồi anh. Nghĩa là cứ cái gì liên quan mcp của thằng. Cứ cái gì mcp là mắc nó đồng hoạt được.

<a id="S00109"></a>
**[00:06:53 → 00:07:00] [Người nói?]** Anh không biết cái đấy nhưng mà anh chưa dùng. Anh chưa dùng cái đấy thì anh ít dùng docker desktop lắm. Không dùng docker desktop bao giờ. Dùng cái server là chính.

## AI tools: Cloud, skill, Codex và đề tài lỗi thời

<a id="S00110"></a>
**[00:07:00 → 00:07:04] [Người nói?]** Mỗi cái là nó hơi bị quá tay nên đôi lúc em không ý thức là mình đang làm cái gì.

<a id="S00111"></a>
**[00:07:04 → 00:07:08] [Người nói?]** Nếu mà mình không theo cửa bài ai, nó là một tràn text của người đọc

<a id="S00112"></a>
**[00:07:10 → 00:07:14] [Người nói?]** Đọc xong nhưng mà vẫn chưa hiểu, có 8 câu hỏi, 10 câu hỏi để hỏi lại

<a id="S00113"></a>
**[00:07:14 → 00:07:16] [Người nói?]** Mà mình hỏi những câu hỏi xong nó lại quên cái đoạn đấy đi

<a id="S00114"></a>
**[00:07:17 → 00:07:25] [Người nói?]** Thế ờ, người ai không cần chỉ đọc sâu, nhanh, có đúng 3 tháng mà của em nó bị lỗi thời

<a id="S00115"></a>
**[00:07:26 → 00:07:28] [Người nói?]** Như của anh cũng bị lỗi thời, ngày xưa ở cái thời mà 2025

<a id="S00116"></a>
**[00:07:30 → 00:07:32] [Người nói?]** Rồi cái đề tài của anh trước thì còn

<a id="S00117"></a>
**[00:07:32 → 00:07:34] [Người nói?]** Nó sẽ là tấn công, nó sẽ bị tấn công rất là nhiều

<a id="S00118"></a>
**[00:07:34 → 00:07:37] [Người nói?]** Nhưng mà bây giờ thì hầu hết là các mô hình có cả Trails rồi

<a id="S00119"></a>
**[00:07:38 → 00:07:44] [Người nói?]** Không được, chỉ là nếu người dùng là dùng Cloud thì đề tài sẽ không có tác dụng

<a id="S00120"></a>
**[00:07:44 → 00:07:45] [Người nói?]** Nhưng mà nếu người dùng là dùng các cái

<a id="S00121"></a>
**[00:07:45 → 00:07:49] [Người nói?]** Nó là doanh nghiệp, doanh nghiệp mà tự xây LM thì nó là ok

<a id="S00122"></a>
**[00:07:49 → 00:07:56] [Người nói?]** Không, chỉ cần liên quan, chỉ cần không dùng Cloud thì đề tài nào cũng có thể được

<a id="S00123"></a>
**[00:07:56 → 00:07:57] [Người nói?]** Thằng đấy nó kiểu

<a id="S00124"></a>
**[00:07:57 → 00:08:00] [Người nói?]** Cái bản Cloud của nó là mô hình cộng với cái hát nét của nó

<a id="S00125"></a>
**[00:08:01 → 00:08:02] [Người nói?]** Thằng đấy hát nét kinh

<a id="S00126"></a>
**[00:08:02 → 00:08:09] [Người nói?]** Do cái ông Andrew NG tổ cái đấy

<a id="S00127"></a>
**[00:08:09 → 00:08:15] [Người nói?]** Thì đấy, giờ chỉ có đúng rồi

<a id="S00128"></a>
**[00:08:15 → 00:08:25] [Người nói?]** Bây giờ tôi yêu chi phí này vì là về trí đồng minh là không thể hơn được mà kiểu hơn nó cũng không tốt hơn được đấy anh

<a id="S00129"></a>
**[00:08:25 → 00:08:31] [Người nói?]** Bây giờ anh dùng nghĩa là cloud cộng với cả skill hnet, anh biết skill hnet không anh?

<a id="S00130"></a>
**[00:08:31 → 00:08:34] [Người nói?]** Nhưng mà bình thường skill là em phải viết script

<a id="S00131"></a>
**[00:08:35 → 00:08:41] [Người nói?]** Ví dụ như em muốn tải một cái video em phải viết chi tiết là script và nó sẽ phải tải, chạy câu lệnh như thế nào, thay thế từ ngữ như thế nào

<a id="S00132"></a>
**[00:08:41 → 00:08:46] [Người nói?]** Bây giờ anh chỉ cần viết ít context cho nó, nó tự động biết cần phải làm gì

<a id="S00133"></a>
**[00:08:46 → 00:08:49] [Người nói?]** Skill là một level tốt hơn của Adnet thôi

<a id="S00134"></a>
**[00:08:49 → 00:08:51] [Người nói?]** Vâng, không nghĩa là có skill và skill Adnet đi anh

<a id="S00135"></a>
**[00:08:51 → 00:08:55] [Người nói?]** Nhưng mà bây giờ thiết tải cũng không làm được rồi

<a id="S00136"></a>
**[00:08:55 → 00:08:58] [Người nói?]** Bởi vì các thằng khác là yêu cầu phải viết chi tiết xem là nó cần phải làm gì

<a id="S00137"></a>
**[00:08:58 → 00:09:02] [Người nói?]** Ừ, thế này cũng có, chỉ là nói chưa được kỹ là cloud rồi

<a id="S00138"></a>
**[00:09:02 → 00:09:07] [Người nói?]** Codec cũng có một cái dùng nó cũng ok, nhưng mà giờ mua thì phải codec thôi

<a id="S00139"></a>
**[00:09:08 → 00:09:16] [Người nói?]** Codec là thiên về người thực thi hơn

<a id="S00140"></a>
**[00:09:16 → 00:09:23] [Người nói?]** Nghĩa là nếu dùng codec để thực thi thì nó sẽ tiết kiệm token hơn, còn về xử lý thông minh thì nên dùng hàng cloud

<a id="S00141"></a>
**[00:09:23 → 00:09:27] [Người nói?]** Với đầu anh dùng codec này em cũng nghĩ là ok, nhưng mà nó có vẻ phá phát quá nhiều như là

<a id="S00142"></a>
**[00:09:27 → 00:09:31] [Người nói?]** Thấy em ví dụ là em phát một tên tên tên tên docker nó sẽ dễ hơn một tiếng

<a id="S00143"></a>
**[00:09:31 → 00:09:39] [Người nói?]** Nó không được mượt mạng và lô lông nhiều, ở kia mình cũng nói rất là nhiều

<a id="S00144"></a>
**[00:09:39 → 00:09:47] [Người nói?]** Ok, đúng thì một thằng hơi tốn tiền, hoặc thì nó sẽ gần như gặp vô hạn

<a id="S00145"></a>
**[00:09:47 → 00:09:51] [Người nói?]** Hồi đấy là anh dùng codec lúc nào cũng cũng thuộc vào rạng 200$ ý

<a id="S00146"></a>
**[00:09:52 → 00:09:55] [Người nói?]** Nên lúc đấy em cũng cảm thấy nó research khá là khỏe, vừa research vừa...

<a id="S00147"></a>
**[00:09:57 → 00:09:59] [Người nói?]** [nghe không rõ 00:09:57; cần đối chiếu] Hãy subscribe cho kênh Ghiền Mì Gõ Để không bỏ lỡ những video hấp dẫn

## Dùng AI viết slide và cách trình bày trước hội đồng

<a id="S00148"></a>
**[00:10:01 → 00:10:04] [Người nói?]** [nghe không rõ 00:10:01; cần đối chiếu] Còn với slide thì anh thấy hoạt động của đấy

<a id="S00149"></a>
**[00:10:04 → 00:10:05] [Người nói?]** [nghe không rõ 00:10:04; cần đối chiếu] Thì nó hỗ trợ kia hơn

<a id="S00150"></a>
**[00:10:06 → 00:10:08] [Người nói?]** [nghe không rõ 00:10:06; cần đối chiếu] Tạo slide, viết doc

<a id="S00151"></a>
**[00:10:09 → 00:10:11] [Người nói?]** [nghe không rõ 00:10:09; cần đối chiếu] Thôi anh hãy dùng thằng đấy để viết slide

<a id="S00152"></a>
**[00:10:11 → 00:10:12] [Người nói?]** [nghe không rõ 00:10:11; cần đối chiếu] Đấy phải nên

<a id="S00153"></a>
**[00:10:13 → 00:10:15] [Người nói?]** [nghe không rõ 00:10:13; cần đối chiếu] Đáng lẽ phải nên ngược lại nhưng mà thôi kìa

<a id="S00154"></a>
**[00:10:15 → 00:10:16] [Người nói?]** [nghe không rõ 00:10:15; cần đối chiếu] Ngược lại sao?

<a id="S00155"></a>
**[00:10:16 → 00:10:19] [Người nói?]** [nghe không rõ 00:10:16; cần đối chiếu] Nghĩa là nếu như mà anh dùng thằng

<a id="S00156"></a>
**[00:10:19 → 00:10:21] [Người nói?]** [nghe không rõ 00:10:19; cần đối chiếu] Nghĩa là thằng Cloud nó chỉ hành chạy lần đầu thôi

<a id="S00157"></a>
**[00:10:21 → 00:10:25] [Người nói?]** [nghe không rõ 00:10:21; cần đối chiếu] Còn lại những cái tinh chỉnh bé bé thì dùng thằng Codec để tính kiện

<a id="S00158"></a>
**[00:10:25 → 00:10:27] [Người nói?]** [nghe không rõ 00:10:25; cần đối chiếu] Chạy lần đầu thôi anh hãy sửa lại

<a id="S00159"></a>
**[00:10:27 → 00:10:30] [Người nói?]** Đúng rồi, anh phải sửa lại mà lúc đấy thì hãy dùng làm codec

<a id="S00160"></a>
**[00:10:30 → 00:10:32] [Người nói?]** Ờ đây, không, dưới codec thì...

<a id="S00161"></a>
**[00:10:32 → 00:10:33] [Người nói?]** Ok

<a id="S00162"></a>
**[00:10:35 → 00:10:37] [Người nói?]** Sửa lại cũng cũng thôi, cho nó với đoán của mình rồi lấy

<a id="S00163"></a>
**[00:10:38 → 00:10:43] [Người nói?]** Vì lúc đấy em thì cũng lấy slide mẫu của máy khoa thôi mà sửa thêm logo mới này

<a id="S00164"></a>
**[00:10:43 → 00:10:45] [Người nói?]** Rồi nó mới chế ra cái đồng đấy

<a id="S00165"></a>
**[00:10:46 → 00:10:48] [Người nói?]** Nhưng mà có đúng mấy cái là em...

<a id="S00166"></a>
**[00:10:49 → 00:10:53] [Người nói?]** Có đúng 4 mô hình mà em dùng AI thì các thầy dã là...

<a id="S00167"></a>
**[00:10:53 → 00:10:54] [Người nói?]** Nhiều chữ quá

<a id="S00168"></a>
**[00:10:54 → 00:10:55] [Người nói?]** Đúng rồi

<a id="S00169"></a>
**[00:10:56 → 00:11:02] [Người nói?]** Thầy họ bảo anh cũng theo, hỏi nhiều vai để bỏ phần câu hỏi luôn

<a id="S00170"></a>
**[00:11:02 → 00:11:04] [Người nói?]** Khi nào các thầy hỏi thì cứ ưa ơn

<a id="S00171"></a>
**[00:11:06 → 00:11:09] [Người nói?]** Tại vì nói cái đấy nó chỉ là cái phương phủ luật của người thầy

<a id="S00172"></a>
**[00:11:09 → 00:11:12] [Người nói?]** Chỉ là một cái mà từ đấy mình suy nghĩ ra một cái gì đấy

<a id="S00173"></a>
**[00:11:12 → 00:11:18] [Người nói?]** Thì em nghi trong nhóm là đặt vấn đề này, các nghiên cứu trước có gì này

<a id="S00174"></a>
**[00:11:18 → 00:11:24] [Người nói?]** Xong rồi xem triển khai thế nào trong cái đoạn bù hát tầm 10 phút là xong rồi

<a id="S00175"></a>
**[00:11:25 → 00:11:28] [Người nói?]** Nhưng mà nghĩ lại thì có khi cứ làm cái cách cũ hay hơn

## Kinh nghiệm bảo vệ: không hỏi được, điểm số và thư ký

<a id="S00176"></a>
**[00:11:28 → 00:11:30] [Người nói?]** Anh Hải, anh Hải công an

<a id="S00177"></a>
**[00:11:30 → 00:11:32] [Người nói?]** Anh ấy thuyết trình hết 40 phút

<a id="S00178"></a>
**[00:11:32 → 00:11:34] [Người nói?]** Xong rồi các thầy không hỏi được gì

<a id="S00179"></a>
**[00:11:34 → 00:11:36] [Người nói?]** Cho 8-6 đi về

<a id="S00180"></a>
**[00:11:36 → 00:11:37] [Người nói?]** Không hỏi đúng 1 câu

<a id="S00181"></a>
**[00:11:39 → 00:11:41] [Người nói?]** Lúc đầu lít ra là hỏi 7 câu

<a id="S00182"></a>
**[00:11:41 → 00:11:43] [Người nói?]** Nhưng mà không kịp, họ trả được đúng 1 câu

<a id="S00183"></a>
**[00:11:43 → 00:11:44] [Người nói?]** Rồi đi về

<a id="S00184"></a>
**[00:11:48 → 00:11:49] [Người nói?]** Anh ấy

<a id="S00185"></a>
**[00:11:49 → 00:11:52] [Người nói?]** Anh ấy mới cân bằng

<a id="S00186"></a>
**[00:11:52 → 00:11:53] [Người nói?]** Nhưng mà anh còn giỏi là được

<a id="S00187"></a>
**[00:11:53 → 00:11:58] [Người nói?]** Bất cứ ai cũng giỏi, trên 8 ai cũng giỏi

<a id="S00188"></a>
**[00:11:58 → 00:12:03] [Người nói?]** Không, khả năng là bạn Ngọc Anh kia sẽ khá

<a id="S00189"></a>
**[00:12:04 → 00:12:08] [Người nói?]** Bởi vì 7.5 là hơi nó kéo kinh

<a id="S00190"></a>
**[00:12:08 → 00:12:10] [Người nói?]** Đấy chắc phải chiếm 70%

<a id="S00191"></a>
**[00:12:10 → 00:12:13] [Người nói?]** Còn mấy cái điểm 8 chấm ở trên trường chỉ chiếm 0.13

<a id="S00192"></a>
**[00:12:17 → 00:12:22] [Người nói?]** Cũng do là các bạn cũng quá tự tin vì cái đề tài là khó quá

<a id="S00193"></a>
**[00:12:22 → 00:12:28] [Người nói?]** Chắc là các thầy dí cho tốc đề xuất thì các thầy nhé bác thầy

<a id="S00194"></a>
**[00:12:29 → 00:12:32] [Người nói?]** Đề xuất đề một giọng dễ bị hỏi quá

<a id="S00195"></a>
**[00:12:33 → 00:12:37] [Người nói?]** Cái đấy là chuyên việt ấy, cũng rộng như vừa rồi một chuyên việt

<a id="S00196"></a>
**[00:12:37 → 00:12:42] [Người nói?]** Và cái mà mọi người chọn là những thứ biết luật

<a id="S00197"></a>
**[00:12:42 → 00:12:47] [Người nói?]** Vâng thì thầy thắng thì ngồi thư ký thì bốn hay kia cũng càng

<a id="S00198"></a>
**[00:12:47 → 00:12:50] [Người nói?]** Thắng ngồi thư ký là chân chết rồi

<a id="S00199"></a>
**[00:12:50 → 00:12:58] [Người nói?]** không thể thắng ngồi thư ký bởi vì thầy kiểu có gì chết là thầy còn kiểu chữa cho các kiểu nói, làm nói tránh

<a id="S00200"></a>
**[00:12:59 → 00:12:59] [Người nói?]** đỡ

<a id="S00201"></a>
**[00:12:59 → 00:13:00] [Người nói?]** vâng, nói đỡ

<a id="S00202"></a>
**[00:13:00 → 00:13:03] [Người nói?]** em là thầy chung ngồi thư ký nha

<a id="S00203"></a>
**[00:13:03 → 00:13:09] [Người nói?]** thế là thầy cũng nói đỡ nên em biết là nếu mà để mấy cái thầy hay hỏi mà làm thư ký là chỉ có thể là nói đỡ

<a id="S00204"></a>
**[00:13:10 → 00:13:11] [Người nói?]** đúng là nói đỡ hơn

<a id="S00205"></a>
**[00:13:11 → 00:13:14] [Người nói?]** nhưng mà như là chủ tịch và thư ký là sẽ không đổi

<a id="S00206"></a>
**[00:13:14 → 00:13:15] [Người nói?]** còn sẽ thay đổi thủy viên

<a id="S00207"></a>
**[00:13:15 → 00:13:18] [Người nói?]** không, chỉ có chủ tịch và sẽ không đổi được

<a id="S00208"></a>
**[00:13:18 → 00:13:19] [Người nói?]** thư ký có đổi

<a id="S00209"></a>
**[00:13:19 → 00:13:20] [Người nói?]** thư ký sẽ đổi

<a id="S00210"></a>
**[00:13:21 → 00:13:26] [Người nói?]** Anh là thầy bảo vẫn ngồi đấy, nhưng thường sẽ đổi

<a id="S00211"></a>
**[00:13:29 → 00:13:35] [Người nói?]** Chỉ có chủ tịch sẽ được giữ, đổi hết

<a id="S00212"></a>
**[00:13:35 → 00:13:42] [Người nói?]** Chủ tịch yêu cầu Phó giáo sư đổi, hoặc là trên đại tá

<a id="S00213"></a>
**[00:13:42 → 00:13:50] [Người nói?]** Như thầy Tuấn Anh, thầy thảm sát nhiều quá, không thể lên Phó giáo sư được

<a id="S00214"></a>
**[00:13:50 → 00:14:05] [Người nói?]** [nghe không rõ 00:13:50; cần đối chiếu] Thầy Tuấn Anh năm... nhưng là thầy có con rồi, còn hồi 2014, thầy về thầy Thắng và phụ huynh đã đem hoa đến rồi, vẫn cho trường.

<a id="S00215"></a>
**[00:14:06 → 00:14:08] [Người nói?]** [nghe không rõ 00:14:06; cần đối chiếu] Càng đưa thầy càng kỹ.

<a id="S00216"></a>
**[00:14:09 → 00:14:14] [Người nói?]** [nghe không rõ 00:14:09; cần đối chiếu] Không, như là kiểu thầy gia đình cho trường, và giờ thầy hiền nó.

<a id="S00217"></a>
**[00:14:15 → 00:14:18] [Người nói?]** [nghe không rõ 00:14:15; cần đối chiếu] Thầy nói như thế là như thế, không ai kiểu...

<a id="S00218"></a>
**[00:14:18 → 00:14:25] [Người nói?]** Thì lúc đầu thầy Thắng thì thầy Thắng đấm em lõm hết đầu không cho em vào về tuần nghiệp, thầy thi tuần nghiệp.

<a id="S00219"></a>
**[00:14:27 → 00:14:33] [Người nói?]** Vâng, đợt thầy mới về là em năm 2, đấy kiểu vẫn hơi hơi...

<a id="S00220"></a>
**[00:14:33 → 00:14:33] [Người nói?]** Em là AT16

<a id="S00221"></a>
**[00:14:33 → 00:14:36] [Người nói?]** Em là AT16, tầm...

<a id="S00222"></a>
**[00:14:36 → 00:14:37] [Người nói?]** Tầm 5 năm là thế

<a id="S00223"></a>
**[00:14:37 → 00:14:47] [Người nói?]** Vâng, đấy là cũng bị lễ hái của thầy Tuấn Anh với cả thầy Thắng, thầy Bảo.

<a id="S00224"></a>
**[00:14:50 → 00:15:00] [Người nói?]** Thầy bảo là thầy khèo kinh hóa. Thầy cũng bình thường thôi nhưng mà nếu mà thầy có vấn đề, đúng rồi, thầy mở ra vấn đề, thầy toán hỏi kỹ hơn, thầy thắng hỏi sâu hơn, thế là chết.

<a id="S00225"></a>
**[00:15:02 → 00:15:06] [Người nói?]** Thầy có một câu hỏi đôi khi không liên quan chứ không phải là câu hỏi của người khác.

<a id="S00226"></a>
**[00:15:06 → 00:15:09] [Người nói?]** Nhưng mà nếu không trả lời kỹ chứng tỏ cái câu hỏi vấn đề là chết.

<a id="S00227"></a>
**[00:15:44 → 00:15:50] [Người nói?]** [nghe không rõ 00:15:44; cần đối chiếu] Hãy subscribe cho kênh Ghiền Mì Gõ Để không bỏ lỡ những video hấp dẫn

## Yêu cầu cống hiến sau đào tạo và góc nhìn AI pen test

<a id="S00228"></a>
**[00:15:50 → 00:15:53] [Người nói?]** Về dạng một môn hoặc là đi tiệm

<a id="S00229"></a>
**[00:15:54 → 00:15:55] [Người nói?]** Thì thầy về

<a id="S00230"></a>
**[00:15:57 → 00:15:57] [Người nói?]** Thầy

<a id="S00231"></a>
**[00:15:57 → 00:15:58] [Người nói?]** Vâng

<a id="S00232"></a>
**[00:16:00 → 00:16:02] [Người nói?]** Hơi đen vụn nga với cả là

<a id="S00233"></a>
**[00:16:03 → 00:16:04] [Người nói?]** Cry

<a id="S00234"></a>
**[00:16:05 → 00:16:07] [Người nói?]** Giống anh Hùng Anh với cả anh Mình

<a id="S00235"></a>
**[00:16:09 → 00:16:11] [Người nói?]** Rồi không thoát được

<a id="S00236"></a>
**[00:16:11 → 00:16:14] [Người nói?]** Nghĩa là mấy anh ấy là yêu cầu

<a id="S00237"></a>
**[00:16:14 → 00:16:16] [Người nói?]** Sau khi học xong rồi phải có 5 năm

<a id="S00238"></a>
**[00:16:16 → 00:16:17] [Người nói?]** Cống hiến cho học viện

<a id="S00239"></a>
**[00:16:18 → 00:16:19] [Người nói?]** Nhưng không

<a id="S00240"></a>
**[00:16:20 → 00:16:21] [Người nói?]** Nhưng mà không ai mời về

<a id="S00241"></a>
**[00:16:21 → 00:16:23] [Người nói?]** Không mời về thì không tích thời gian được

<a id="S00242"></a>
**[00:16:23 → 00:16:36] [Người nói?]** Như là kiểu anh ấy mới được tính khoảng 2-3 tháng thôi, đôi lúc đe gọi về giấy, không được tích thời gian, nhưng mà cũng không được kiểu rứt đường, cứ bị ở giữa, cứ chôn.

<a id="S00243"></a>
**[00:16:39 → 00:16:42] [Người nói?]** Đấy là đầu chiến tranh đó, chưa anh?

<a id="S00244"></a>
**[00:16:42 → 00:16:42] [Người nói?]** Dạ?

<a id="S00245"></a>
**[00:16:42 → 00:16:43] [Người nói?]** Đã được mà không anh?

<a id="S00246"></a>
**[00:16:45 → 00:16:51] [Người nói?]** Chưa, không anh ấy về được 3 năm rồi. Đợt đấy là đã bị rồi anh.

<a id="S00247"></a>
**[00:16:51 → 00:16:54] [Người nói?]** Đợt nào?

<a id="S00248"></a>
**[00:16:54 → 00:17:08] [Người nói?]** [nghe không rõ 00:16:54; cần đối chiếu] Nghĩ chắc là thêm mấy mấy năm nữa thôi vì là Nga nào cũng thắng rồi giờ phải câu, câu kiểu để Mến Úc Châu yếu cũng chưa biết được anh.

<a id="S00249"></a>
**[00:17:09 → 00:17:14] [Người nói?]** [nghe không rõ 00:17:09; cần đối chiếu] Nhưng mà làm với Gu bây giờ thì sau năm 2026 thì anh...

<a id="S00250"></a>
**[00:17:14 → 00:17:16] [Người nói?]** [nghe không rõ 00:17:14; cần đối chiếu] AI ạ.

<a id="S00251"></a>
**[00:17:16 → 00:17:23] [Người nói?]** [nghe không rõ 00:17:16; cần đối chiếu] AI nó kiểu nó sẵn sàng động vào mấy cái an toàn thông tin, an toàn thông tin nó cũng...

<a id="S00252"></a>
**[00:17:23 → 00:17:32] [Người nói?]** Anh em làm pen test được thì NLC cũng làm được. Giờ anh em pen test đi tìm bất kỳ người ai để investigate.

<a id="S00253"></a>
**[00:17:33 → 00:17:40] [Người nói?]** Thì hôm nay em cũng có nói thì anh ấy cũng có nói là bây giờ chỉ ném cái mindset là thôi, còn lại là nó sẽ chủ động.

<a id="S00254"></a>
**[00:17:41 → 00:17:44] [Người nói?]** Và cái quan trọng nhất là cái case study là cái quan trọng nhất.

<a id="S00255"></a>
**[00:17:44 → 00:18:16] [Người nói?]** Hãy subscribe cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

<a id="S00256"></a>
**[00:18:29 → 00:18:45] [Người nói?]** [nghe không rõ 00:18:29; cần đối chiếu] Hãy subscribe cho kênh lalaschool Để không bỏ lỡ những video hấp dẫn

## Phần chuyển cấp xử lý (tia 1 / tia 2) trong SOC

<a id="S00257"></a>
**[00:18:51 → 00:18:52] [Người nói?]** [nghe không rõ 00:18:51; cần đối chiếu] Để em đọc tiếp

<a id="S00258"></a>
**[00:18:54 → 00:18:55] [Người nói?]** [nghe không rõ 00:18:54; cần đối chiếu] Để em đọc tiếp

<a id="S00259"></a>
**[00:18:56 → 00:18:58] [Người nói?]** [nghe không rõ 00:18:56; cần đối chiếu] Để em đọc tiếp

<a id="S00260"></a>
**[00:18:58 → 00:19:01] [Người nói?]** [nghe không rõ 00:18:58; cần đối chiếu] Để em đọc tiếp

<a id="S00261"></a>
**[00:19:01 → 00:19:02] [Người nói?]** [nghe không rõ 00:19:01; cần đối chiếu] Để em đọc tiếp

<a id="S00262"></a>
**[00:19:02 → 00:19:02] [Người nói?]** [nghe không rõ 00:19:02; cần đối chiếu] Để em đọc tiếp

<a id="S00263"></a>
**[00:19:02 → 00:19:02] [Người nói?]** [nghe không rõ 00:19:02; cần đối chiếu] Để em đọc tiếp

<a id="S00264"></a>
**[00:19:02 → 00:19:04] [Người nói?]** [nghe không rõ 00:19:02; cần đối chiếu] Để em đọc tiếp

<a id="S00265"></a>
**[00:19:04 → 00:19:06] [Người nói?]** [nghe không rõ 00:19:04; cần đối chiếu] Để em đọc tiếp

<a id="S00266"></a>
**[00:19:06 → 00:19:08] [Người nói?]** [nghe không rõ 00:19:06; cần đối chiếu] Để em đọc tiếp

<a id="S00267"></a>
**[00:19:14 → 00:19:17] [Người nói?]** [nghe không rõ 00:19:14; cần đối chiếu] Để em đọc tiếp

<a id="S00268"></a>
**[00:19:17 → 00:19:19] [Người nói?]** [nghe không rõ 00:19:17; cần đối chiếu] Nghĩa là vứt hết tia 1 à?

<a id="S00269"></a>
**[00:19:20 → 00:19:23] [Người nói?]** [nghe không rõ 00:19:20; cần đối chiếu] Tia 1 chỉ có V5 và AI thôi

<a id="S00270"></a>
**[00:19:23 → 00:19:25] [Người nói?]** [nghe không rõ 00:19:23; cần đối chiếu] Chẳng vứt Alex nhiều

<a id="S00271"></a>
**[00:19:25 → 00:19:27] [Người nói?]** [nghe không rõ 00:19:25; cần đối chiếu] Thế thì mất hết việc

<a id="S00272"></a>
**[00:19:28 → 00:19:29] [Người nói?]** [nghe không rõ 00:19:28; cần đối chiếu] Mất được phải tiến hóa thôi

<a id="S00273"></a>
**[00:19:30 → 00:19:32] [Người nói?]** [nghe không rõ 00:19:30; cần đối chiếu] Tia 1 phải cố lên thôi như thế nào?

<a id="S00274"></a>
**[00:19:32 → 00:19:35] [Người nói?]** [nghe không rõ 00:19:32; cần đối chiếu] Tia 1 cố không được, giờ chỉ có đẩy thẳng lên tia 2 thôi

<a id="S00275"></a>
**[00:19:35 → 00:19:37] [Người nói?]** [nghe không rõ 00:19:35; cần đối chiếu] Thì đúng, nghĩa là tia 1 phải cố ăn súng tỏa

<a id="S00276"></a>
**[00:19:37 → 00:19:39] [Người nói?]** [nghe không rõ 00:19:37; cần đối chiếu] Thử lý được vấn đề đấy thì nó sẽ lên được

<a id="S00277"></a>
**[00:19:39 → 00:19:42] [Người nói?]** [nghe không rõ 00:19:39; cần đối chiếu] Chứ có tầm tia 1 lên tia 2 đâu

<a id="S00278"></a>
**[00:19:42 → 00:19:45] [Người nói?]** [nghe không rõ 00:19:42; cần đối chiếu] Vừa vào đã thành tia 2

<a id="S00279"></a>
**[00:19:46 → 00:19:47] [Người nói?]** [nghe không rõ 00:19:46; cần đối chiếu] Không có vấn đề

## SOC: alert, evidence, endpoint và làm nội bộ (MISA)

<a id="S00280"></a>
**[00:19:47 → 00:19:59] [Người nói?]** Có những ông không trực mà chỉ làm D2 thôi, tất cả các ông như thế này. Chỉ chuyên đi tùy mạng

<a id="S00281"></a>
**[00:20:00 → 00:20:03] [Người nói?]** [nghe không rõ 00:20:00; cần đối chiếu] quen của các chủ tịch xăng chủ động thôi chứ không hỗ trợ

<a id="S00282"></a>
**[00:20:04 → 00:20:10] [Người nói?]** [nghe không rõ 00:20:04; cần đối chiếu] Hỗ trợ chính là gần như bỏ gần hết

<a id="S00283"></a>
**[00:20:10 → 00:20:12] [Người nói?]** [nghe không rõ 00:20:10; cần đối chiếu] Chắc đúng như thế, mong mọi người yên tĩnh

<a id="S00284"></a>
**[00:20:13 → 00:20:19] [Người nói?]** [nghe không rõ 00:20:13; cần đối chiếu] Và cái dây chuyền mà có alert và cái tiêu chuẩn về alert này như thế nào, có AI nào, có follow như thế nào

<a id="S00285"></a>
**[00:20:19 → 00:20:23] [Người nói?]** [nghe không rõ 00:20:19; cần đối chiếu] Trước em nghe đóng cây bằng AI, đã thấy không giòn

<a id="S00286"></a>
**[00:20:23 → 00:20:28] [Người nói?]** [nghe không rõ 00:20:23; cần đối chiếu] Đóng cây này, từ cây đấy mang đi một loại loại veritip này, bổ sung trên evidence này

<a id="S00287"></a>
**[00:20:28 → 00:20:30] [Người nói?]** xong từ Evidence đấy kích xuất

<a id="S00288"></a>
**[00:20:30 → 00:20:32] [Người nói?]** quay ngược về Endpoint nhé

<a id="S00289"></a>
**[00:20:32 → 00:20:33] [Người nói?]** lấy Artifact về

<a id="S00290"></a>
**[00:20:33 → 00:20:36] [Người nói?]** lấy Analyze cái tại Artifact đấy

<a id="S00291"></a>
**[00:20:36 → 00:20:38] [Người nói?]** như là e nghe chẳng hạn kiểu kìa đấy

<a id="S00292"></a>
**[00:20:38 → 00:20:40] [Người nói?]** Vậy nhưng mà nước ngoài ai đã làm chưa mà

<a id="S00293"></a>
**[00:20:40 → 00:20:41] [Người nói?]** hay là

<a id="S00294"></a>
**[00:20:41 → 00:20:45] [Người nói?]** cũng sản phẩm hãng đang làm đấy

<a id="S00295"></a>
**[00:20:45 → 00:20:47] [Người nói?]** không kiểu nội bộ vậy anh

<a id="S00296"></a>
**[00:20:47 → 00:20:49] [Người nói?]** hay là mình vẫn phải

<a id="S00297"></a>
**[00:20:49 → 00:20:52] [Người nói?]** nghĩa là mình phải dừng đến hãng hay là kiểu mình làm nội bộ

<a id="S00298"></a>
**[00:20:52 → 00:20:53] [Người nói?]** không, mình làm nội bộ vẫn được

<a id="S00299"></a>
**[00:20:54 → 00:20:55] [Người nói?]** MISA đang làm đấy rồi

<a id="S00300"></a>
**[00:20:55 → 00:20:56] [Người nói?]** MISA hả

<a id="S00301"></a>
**[00:20:57 → 00:21:00] [Người nói?]** [nghe không rõ 00:20:57; cần đối chiếu] Misa hả? Misa, Misa là công ty Misa, Misa giấu ý

<a id="S00302"></a>
**[00:21:00 → 00:21:01] [Người nói?]** [nghe không rõ 00:21:00; cần đối chiếu] Không em biết rồi

<a id="S00303"></a>
**[00:21:03 → 00:21:05] [Người nói?]** [nghe không rõ 00:21:03; cần đối chiếu] Misa lần này đi bootcamp có tiền tiền lần đấy

<a id="S00304"></a>
**[00:21:05 → 00:21:09] [Người nói?]** [nghe không rõ 00:21:05; cần đối chiếu] Người ta không bắt đầu lên mạng, người ta không đuổi ai thì không được

<a id="S00305"></a>
**[00:21:12 → 00:21:14] [Người nói?]** [nghe không rõ 00:21:12; cần đối chiếu] Năm sau bootcamp này chắc là người ta sẽ put slide lên thôi

<a id="S00306"></a>
**[00:21:16 → 00:21:17] [Người nói?]** [nghe không rõ 00:21:16; cần đối chiếu] Bootcamp hôm nào đấy anh?

<a id="S00307"></a>
**[00:21:17 → 00:21:18] [Người nói?]** [nghe không rõ 00:21:17; cần đối chiếu] Hôm nay ngày cuối rồi

<a id="S00308"></a>
**[00:21:21 → 00:21:24] [Người nói?]** [nghe không rõ 00:21:21; cần đối chiếu] Có gì chắc là anh cho em xem, em cũng không...

## Security Bootcamp và định hướng theo thầy/chủ đề

<a id="S00309"></a>
**[00:21:28 → 00:21:33] [Người nói?]** Năm nào cũng có slide mà. Năm ngoái là bắt đầu nói về Autonomous Energy.

<a id="S00310"></a>
**[00:21:34 → 00:21:41] [Người nói?]** Có khi làm không nhanh 2 tháng ở khi nói cái của em phải lỗi thời tiết.

<a id="S00311"></a>
**[00:21:41 → 00:21:43] [Người nói?]** Thầy kêu phải tiến hóa thôi.

<a id="S00312"></a>
**[00:21:45 → 00:21:48] [Người nói?]** Công nghệ cổ kỳ luôn. Nhanh thật.

<a id="S00313"></a>
**[00:21:51 → 00:21:55] [Người nói?]** Bây giờ kiểu làm biệt tá không phải chứng minh mình hỗ trợ AI cái gì.

<a id="S00314"></a>
**[00:21:55 → 00:21:58] [Người nói?]** cái này

<a id="S00315"></a>
**[00:22:01 → 00:22:03] [Người nói?]** hình thái mới

<a id="S00316"></a>
**[00:22:21 → 00:22:23] [Người nói?]** mục tài nguyên

<a id="S00317"></a>
**[00:22:25 → 00:22:27] [Người nói?]** chắc là hiện tại thì em chưa post lên nhưng mà

<a id="S00318"></a>
**[00:22:27 → 00:22:28] [Người nói?]** hai ngôi năm thì nó có này

<a id="S00319"></a>
**[00:22:32 → 00:22:37] [Người nói?]** Facebook thì người ta sẽ nói là YouTube Bootcamp Misa

<a id="S00320"></a>
**[00:22:37 → 00:22:42] [Người nói?]** các em thấy rồi

<a id="S00321"></a>
**[00:22:42 → 00:22:46] [Người nói?]** [nghe không rõ 00:22:42; cần đối chiếu] Như thế này là giới thiệu của Securitibootcamp nhé

<a id="S00322"></a>
**[00:22:54 → 00:22:58] [Người nói?]** [nghe không rõ 00:22:54; cần đối chiếu] Từ nay đến cuối năm thì còn sự kiện kiểu đánh tập trận

<a id="S00323"></a>
**[00:22:58 → 00:22:59] [Người nói?]** [nghe không rõ 00:22:58; cần đối chiếu] Đấy gọi là gì nhé?

<a id="S00324"></a>
**[00:22:59 → 00:23:00] [Người nói?]** [nghe không rõ 00:22:59; cần đối chiếu] Đánh diễn và thực chiến

<a id="S00325"></a>
**[00:23:00 → 00:23:01] [Người nói?]** [nghe không rõ 00:23:00; cần đối chiếu] À diễn vâng

<a id="S00326"></a>
**[00:23:01 → 00:23:04] [Người nói?]** [nghe không rõ 00:23:01; cần đối chiếu] Nhưng mà nếu như Securitibootcamp thì không có cái nào nữa

<a id="S00327"></a>
**[00:23:04 → 00:23:06] [Người nói?]** [nghe không rõ 00:23:04; cần đối chiếu] Nhưng mà có thể sẽ có Smart Banking

<a id="S00328"></a>
**[00:23:06 → 00:23:10] [Người nói?]** [nghe không rõ 00:23:06; cần đối chiếu] Smart Banking thì Security là thứ yếu đi cạnh

<a id="S00329"></a>
**[00:23:10 → 00:23:12] [Người nói?]** [nghe không rõ 00:23:10; cần đối chiếu] Nó sẽ tổ chức thi đấu ở đấy

<a id="S00330"></a>
**[00:23:12 → 00:23:13] [Người nói?]** [nghe không rõ 00:23:12; cần đối chiếu] Như là nội bộ ấy

<a id="S00331"></a>
**[00:23:13 → 00:23:14] [Người nói?]** [nghe không rõ 00:23:13; cần đối chiếu] Không, các ngân hàng

<a id="S00332"></a>
**[00:23:14 → 00:23:17] [Người nói?]** [nghe không rõ 00:23:14; cần đối chiếu] Thi giữa các ngân hàng ấy

## Hội đồng, nghiên cứu sinh và hồ sơ thầy dạy

<a id="S00333"></a>
**[00:23:17 → 00:23:27] [Người nói?]** Anh vào feed anh có gặp bạn Phong hả anh?

<a id="S00334"></a>
**[00:23:28 → 00:23:29] [Người nói?]** Anh ở chỗ khác

<a id="S00335"></a>
**[00:23:29 → 00:23:30] [Người nói?]** Chỗ khác

<a id="S00336"></a>
**[00:23:30 → 00:23:31] [Người nói?]** Đặc biệt hơn

<a id="S00337"></a>
**[00:23:33 → 00:23:36] [Người nói?]** Điêu anh có được trên 4x không anh?

<a id="S00338"></a>
**[00:23:36 → 00:23:37] [Người nói?]** Trên 4x

<a id="S00339"></a>
**[00:23:38 → 00:23:41] [Người nói?]** Đến từ WinShot cũng giống mà về...

<a id="S00340"></a>
**[00:23:41 → 00:23:42] [Người nói?]** Anh...

<a id="S00341"></a>
**[00:23:43 → 00:23:43] [Người nói?]** Năm nay

<a id="S00342"></a>
**[00:23:43 → 00:23:45] [Người nói?]** Em chưa gặp, vâng rồi

<a id="S00343"></a>
**[00:23:45 → 00:23:48] [Người nói?]** Anh làm cùng anh?

<a id="S00344"></a>
**[00:23:49 → 00:23:50] [Người nói?]** Còn đây là Misa

<a id="S00345"></a>
**[00:23:50 → 00:23:51] [Người nói?]** Trường Misa

<a id="S00346"></a>
**[00:23:51 → 00:23:52] [Người nói?]** Misa

<a id="S00347"></a>
**[00:23:54 → 00:23:55] [Người nói?]** Rồi

<a id="S00348"></a>
**[00:23:55 → 00:23:57] [Người nói?]** Ai xem thức AI

<a id="S00349"></a>
**[00:23:57 → 00:23:59] [Người nói?]** No, nó mất defense

<a id="S00350"></a>
**[00:24:01 → 00:24:03] [Người nói?]** [nghe không rõ 00:24:01; cần đối chiếu] Nó không nếp việc đâu

<a id="S00351"></a>
**[00:24:03 → 00:24:05] [Người nói?]** [nghe không rõ 00:24:03; cần đối chiếu] Không, đương nhiên là không nhanh

<a id="S00352"></a>
**[00:24:05 → 00:24:09] [Người nói?]** [nghe không rõ 00:24:05; cần đối chiếu] Và cái đề tài của thêm không nhanh là cũng ngon ngoẻo

<a id="S00353"></a>
**[00:24:10 → 00:24:11] [Người nói?]** [nghe không rõ 00:24:10; cần đối chiếu] Ừ, nên nhanh

<a id="S00354"></a>
**[00:24:12 → 00:24:15] [Người nói?]** [nghe không rõ 00:24:12; cần đối chiếu] Nhưng mà đối với người nghiên cứu thì nhanh chậm nó khốn nha lắm

<a id="S00355"></a>
**[00:24:15 → 00:24:16] [Người nói?]** [nghe không rõ 00:24:15; cần đối chiếu] Giờ thì có rồi

<a id="S00356"></a>
**[00:24:16 → 00:24:21] [Người nói?]** [nghe không rõ 00:24:16; cần đối chiếu] Không, đối với người nghiên cứu thì không nhanh thì sẽ vẫn có cách khác để người ta làm

<a id="S00357"></a>
**[00:24:21 → 00:24:24] [Người nói?]** [nghe không rõ 00:24:21; cần đối chiếu] Tức là người ta không phải là người nghiên cứu chỉ hôm nay thôi

<a id="S00358"></a>
**[00:24:24 → 00:24:26] [Người nói?]** [nghe không rõ 00:24:24; cần đối chiếu] Người ta nghiên cứu là người ta tiếp tục chuyển đổi chủ đề

<a id="S00359"></a>
**[00:24:26 → 00:24:27] [Người nói?]** [nghe không rõ 00:24:26; cần đối chiếu] Người khác thì người ta vẫn không thể

<a id="S00360"></a>
**[00:24:28 → 00:24:31] [Người nói?]** Chuyển đổi chủ đề cũng hơi khó

<a id="S00361"></a>
**[00:24:31 → 00:24:35] [Người nói?]** Không nhưng mà chuyển đổi chủ đề phải theo thầy nữa

<a id="S00362"></a>
**[00:24:35 → 00:24:36] [Người nói?]** Bởi vì là

<a id="S00363"></a>
**[00:24:38 → 00:24:39] [Người nói?]** Khi nào em lên tiến sĩ

<a id="S00364"></a>
**[00:24:40 → 00:24:42] [Người nói?]** À khi nào em lên phó giáo sư em mới được quyền tự chủ

<a id="S00365"></a>
**[00:24:43 → 00:24:46] [Người nói?]** Còn thầy Phạm Duy Trung là thầy đang theo một thầy

<a id="S00366"></a>
**[00:24:46 → 00:24:48] [Người nói?]** Đây là thầy Bùi Thu Lâm ở thiên trường

<a id="S00367"></a>
**[00:24:48 → 00:24:50] [Người nói?]** Thầy à

<a id="S00368"></a>
**[00:24:53 → 00:24:54] [Người nói?]** Thầy mà dạy mình môn

<a id="S00369"></a>
**[00:24:54 → 00:24:55] [Người nói?]** Học máy

<a id="S00370"></a>
**[00:24:55 → 00:24:56] [Người nói?]** Học máy đấy

<a id="S00371"></a>
**[00:24:56 → 00:25:00] [Người nói?]** Thì thấy bị hồ sơ bị bỏ vấn đề

<a id="S00372"></a>
**[00:25:00 → 00:25:02] [Người nói?]** Nên là không lên được

<a id="S00373"></a>
**[00:25:03 → 00:25:06] [Người nói?]** Còn trước là thấy là bên trường quân sự

<a id="S00374"></a>
**[00:25:06 → 00:25:07] [Người nói?]** Vâng

<a id="S00375"></a>
**[00:25:07 → 00:25:08] [Người nói?]** À đấy biết cắt

<a id="S00376"></a>
**[00:25:08 → 00:25:10] [Người nói?]** Vâng đúng rồi

<a id="S00377"></a>
**[00:25:10 → 00:25:14] [Người nói?]** Thấy trước là cũng kiểu sắp lên

<a id="S00378"></a>
**[00:25:14 → 00:25:16] [Người nói?]** Không biết

<a id="S00379"></a>
**[00:25:18 → 00:25:19] [Người nói?]** Cũng sắp lên phó

<a id="S00380"></a>
**[00:25:19 → 00:25:20] [Người nói?]** À cũng lên phó hiệu trưởng

<a id="S00381"></a>
**[00:25:20 → 00:25:24] [Người nói?]** Nhưng mà bị cái liên quan tới mở lớp

<a id="S00382"></a>
**[00:25:24 → 00:25:26] [Người nói?]** Mở lớp dạy thêm thì không được tính là

<a id="S00383"></a>
**[00:25:26 → 00:25:28] [Người nói?]** Đó là kiểu tiền khô

<a id="S00384"></a>
**[00:25:28 → 00:25:32] [Người nói?]** Anh không biết vụ đấy nhưng mà anh chỉ biết là một tục tạm mà không trở nên

<a id="S00385"></a>
**[00:25:32 → 00:25:36] [Người nói?]** Đấy thì bị cái đấy thôi bởi vì mỗi lớp dạy thêm ngoài, dạy thu tiền

<a id="S00386"></a>
**[00:25:36 → 00:25:41] [Người nói?]** Và hồi đấy thì cứ nghĩ là phải dạy để dạy từ tấm lòng của thầy là khô xong

<a id="S00387"></a>
**[00:25:41 → 00:25:44] [Người nói?]** Thế là gọi là dòng tiền không minh bạch, dính

<a id="S00388"></a>
**[00:25:46 → 00:25:47] [Người nói?]** Và thầy thích rất đến cái đấy

<a id="S00389"></a>
**[00:25:47 → 00:25:49] [Người nói?]** Vâng, thầy cũng thích

<a id="S00390"></a>
**[00:25:49 → 00:25:49] [Người nói?]** Nhẹ nhàng, nhẹ nhàng

<a id="S00391"></a>
**[00:25:50 → 00:25:53] [Người nói?]** Thì cái đấy bị uống hồ sơ thế là thầy bị kẹt

<a id="S00392"></a>
**[00:25:53 → 00:25:56] [Người nói?]** Ờ, hiện tại thầy cũng theo thầy đấy

## Tiến độ đề tài của anh và khả năng bảo vệ sớm

<a id="S00393"></a>
**[00:25:57 → 00:26:04] [Người nói?]** Nhất là bình thường là cứ thứ bảy hàng tuần là sẽ có một buổi giữa các nghiên cứu sinh thì em được ngồi ké

<a id="S00394"></a>
**[00:26:05 → 00:26:07] [Người nói?]** Vì kiểu em ghi tên mấy vào

<a id="S00395"></a>
**[00:26:08 → 00:26:13] [Người nói?]** Tức là em mới tự tin là ít nhất là đề tài em nhắc nhắn trên tám vì thấy mà không ok em không bao giờ ra bảo vệ

<a id="S00396"></a>
**[00:26:14 → 00:26:19] [Người nói?]** Về em bảo vệ muộn thì mãi thấy ok không thì có khi nhanh hơn nhiều

<a id="S00397"></a>
**[00:26:21 → 00:26:25] [Người nói?]** Cái đề tài này của anh lâu lâu anh ngó vào một tí, không có nhiều thời gian được

<a id="S00398"></a>
**[00:26:26 → 00:26:29] [Người nói?]** Cũng may là em nghĩ là giai đoạn của anh ngó kịp

<a id="S00399"></a>
**[00:26:30 → 00:26:30] [Người nói?]** Đúng đấy

<a id="S00400"></a>
**[00:26:30 → 00:26:32] [Người nói?]** Vì là mới thông báo 2 tuần

<a id="S00401"></a>
**[00:26:33 → 00:26:37] [Người nói?]** Anh dự trù công việc lâu từ trước rồi, chỉ là anh không ngó vào kịp

<a id="S00402"></a>
**[00:26:38 → 00:26:40] [Người nói?]** Lên đề cương thì lên đề cương trước 1 tuần thôi

<a id="S00403"></a>
**[00:26:40 → 00:26:47] [Người nói?]** Thế cũng may em vừa mới nhắn tin cho anh Hải lớp trưởng là khả năng sẽ bảo vệ sớm

<a id="S00404"></a>
**[00:26:47 → 00:26:49] [Người nói?]** Bởi vì thầy hiệu phó sắp phải luân chuyển công tác

<a id="S00405"></a>
**[00:26:49 → 00:26:53] [Người nói?]** 2 hôm sau đã nhận tin là 12 đảng chí bảo vệ

<a id="S00406"></a>
**[00:27:00 → 00:27:06] [Người nói?]** Bình thường là phải nộp, gửi các thầy, tạm biệt rồi sửa lại một lần nữa, rồi gửi lại lần cuối.

<a id="S00407"></a>
**[00:27:07 → 00:27:15] [Người nói?]** Cái này cô ý anh có thể cắt hết đoạn AI đi, nhưng mà bỏ qua hết thì rất là may mắn.

<a id="S00408"></a>
**[00:27:16 → 00:27:18] [Người nói?]** Đỡ bao nhiêu bước làm nhẹ cũng được.

<a id="S00409"></a>
**[00:27:21 → 00:27:22] [Người nói?]** Chưa sẵn sàng bảo vệ.

<a id="S00410"></a>
**[00:27:22 → 00:27:27] [Người nói?]** Không sao, anh thấy cái quy mô thì anh cũng biết là nó rất là dễ.

<a id="S00411"></a>
**[00:27:28 → 00:27:30] [Người nói?]** Sáng anh có đi dạo một vòng hay hình thế?

<a id="S00412"></a>
**[00:27:31 → 00:27:35] [Người nói?]** Chắc là chết mỗi một người thôi

<a id="S00413"></a>
**[00:27:35 → 00:27:38] [Người nói?]** Em cảm giác là mình không nên chọn đề tài

<a id="S00414"></a>
**[00:27:40 → 00:27:42] [Người nói?]** Nghĩa là em biết là chuyên biệt rồi

<a id="S00415"></a>
**[00:27:42 → 00:27:43] [Người nói?]** Nhưng mà nó quá rộng để hỏi

<a id="S00416"></a>
**[00:27:43 → 00:27:46] [Người nói?]** Rộng là không người cũng biết

<a id="S00417"></a>
**[00:27:46 → 00:27:50] [Người nói?]** Nếu mà đi theo thầy mà không tự tin thì tự tìm một cái

<a id="S00418"></a>
**[00:27:52 → 00:27:55] [Người nói?]** Nếu mà em tự vẽ ra đường thì sẽ không ai bắt vẽ em cả

<a id="S00419"></a>
**[00:27:55 → 00:27:56] [Người nói?]** Em đi theo đường người khác thì...

<a id="S00420"></a>
**[00:28:01 → 00:28:03] [Người nói?]** Đi theo người khác thì phải tâm trí hơn

<a id="S00421"></a>
**[00:28:04 → 00:28:05] [Người nói?]** Mình bị thú động hay tự động?

<a id="S00422"></a>
**[00:28:10 → 00:28:19] [Người nói?]** [nghe không rõ 00:28:10; cần đối chiếu] hello hello đang đang đang ok ok ok

## Autonomous, forensics và threat intelligence

<a id="S00423"></a>
**[00:28:27 → 00:28:33] [Người nói?]** [nghe không rõ 00:28:27; cần đối chiếu] ngoài cái autonomous còn giờ còn có cái gì bên LOC cần phải biết không anh

<a id="S00424"></a>
**[00:28:33 → 00:28:45] [Người nói?]** [nghe không rõ 00:28:33; cần đối chiếu] đấy autonomous đấy là chỉ bên LOC thôi còn bản forensic và internet response đúng không

<a id="S00425"></a>
**[00:28:45 → 00:28:47] [Người nói?]** [nghe không rõ 00:28:45; cần đối chiếu] còn nhiều hay như nào anh

<a id="S00426"></a>
**[00:28:47 → 00:28:49] [Người nói?]** [nghe không rõ 00:28:47; cần đối chiếu] ý là có những mảng khác nữa mà

<a id="S00427"></a>
**[00:28:49 → 00:28:54] [Người nói?]** [nghe không rõ 00:28:49; cần đối chiếu] vâng thì em đang quan tâm đến khách intelligent hơn

<a id="S00428"></a>
**[00:28:54 → 00:28:56] [Người nói?]** [nghe không rõ 00:28:54; cần đối chiếu] khách intelligent mà có AI á

<a id="S00429"></a>
**[00:28:56 → 00:28:57] [Người nói?]** [nghe không rõ 00:28:56; cần đối chiếu] có chứ anh

<a id="S00430"></a>
**[00:28:57 → 00:29:02] [Người nói?]** [nghe không rõ 00:28:57; cần đối chiếu] có ừ không ý là anh đang muốn hỏi em em muốn có AI trong đấy hay là như nào

<a id="S00431"></a>
**[00:29:02 → 00:29:02] [Người nói?]** [nghe không rõ 00:29:02; cần đối chiếu] ừ đúng rồi anh

<a id="S00432"></a>
**[00:29:02 → 00:29:07] [Người nói?]** Mục tiêu của em là khi bảo vệ thì sẽ làm 2 cái

<a id="S00433"></a>
**[00:29:07 → 00:29:11] [Người nói?]** Một là thêm cái keyword để cho thằng tượng lửa nó quét mạnh hơn

<a id="S00434"></a>
**[00:29:11 → 00:29:16] [Người nói?]** Hai là sẽ ném một thằng AI vào giữa thằng tượng lửa với cả thằng AI chính

<a id="S00435"></a>
**[00:29:16 → 00:29:20] [Người nói?]** Một con mô đun nhỏ hơn để giảm thiểu cho ví dụ thằng Cloud ở hạng nó rất là khỏe

<a id="S00436"></a>
**[00:29:20 → 00:29:21] [Người nói?]** Nó sẽ sàng lọc thêm

<a id="S00437"></a>
**[00:29:21 → 00:29:23] [Người nói?]** Thì sẽ là kiểu bảo vệ băng

<a id="S00438"></a>
**[00:29:25 → 00:29:28] [Người nói?]** Thì sau đó thì nó phải dựa trên một bộ TI chứ anh

<a id="S00439"></a>
**[00:29:28 → 00:29:31] [Người nói?]** Cái con mô đun bé của em là nó phải dựa trên TI

<a id="S00440"></a>
**[00:29:32 → 00:29:35] [Người nói?]** Đồng ý, đồng ý. Ok đây, nhưng mà CoTi đâu cần phải AI.

<a id="S00441"></a>
**[00:29:36 → 00:29:46] [Người nói?]** Con TI đấy nó chỉ ghi một vài cái câu lệnh, ví dụ như là một câu tấn công mới nhất chẳng hạn.

<a id="S00442"></a>
**[00:29:46 → 00:29:51] [Người nói?]** Như vừa mới tấn công ngân hàng VIP chẳng hạn, thì khả năng sẽ tấn công ngân hàng MB.

<a id="S00443"></a>
**[00:29:51 → 00:29:53] [Người nói?]** Thì mới thu thập được một hai câu thôi.

<a id="S00444"></a>
**[00:29:53 → 00:29:57] [Người nói?]** Mà muốn đưa vào mô hình AI thì phải nhân dọng nó cực kỳ nhiều lên.

<a id="S00445"></a>
**[00:29:57 → 00:30:00] [Người nói?]** mình không thể ctrl c ctrl v được

<a id="S00446"></a>
**[00:30:00 → 00:30:01] [Người nói?]** bởi vì nó chỉ giảm học đúng một mẫu

<a id="S00447"></a>
**[00:30:01 → 00:30:03] [Người nói?]** cái thật không thể đổi mẫu liên tục

<a id="S00448"></a>
**[00:30:03 → 00:30:06] [Người nói?]** cái này cũng như là ngoài tầm của TI rồi, cái này vẫn là GAN thôi

<a id="S00449"></a>
**[00:30:06 → 00:30:12] [Người nói?]** không nhưng mà ý là đầu tiên là có TI, giờ phải làm đến nào mà GAN nó phải học được, thì hút đấy mới nhân

<a id="S00450"></a>
**[00:30:12 → 00:30:16] [Người nói?]** thế thì thử mấy cái project open source kiểu MISC ấy

<a id="S00451"></a>
**[00:30:16 → 00:30:18] [Người nói?]** để nó chỉ là môi trường của TI thôi

<a id="S00452"></a>
**[00:30:19 → 00:30:19] [Người nói?]** môi trường của TI

<a id="S00453"></a>
**[00:30:19 → 00:30:23] [Người nói?]** tức là nó là một cái pool để em lấy nguồn nước ngoài

<a id="S00454"></a>
**[00:30:24 → 00:30:24] [Người nói?]** MISC

<a id="S00455"></a>
**[00:30:28 → 00:30:36] [Người nói?]** [nghe không rõ 00:30:28; cần đối chiếu] nguồn tên rồi thì cái nó nó chỉ là một cái ôm xuống cho em kéo ra những nguồn cộng đồng về và

<a id="S00456"></a>
**[00:30:36 → 00:30:44] [Người nói?]** [nghe không rõ 00:30:36; cần đối chiếu] đấy sẽ nuôi được cái đấy để em phát triển ra nhân nhân dưới lên nhưng mà anh không không biết cái

<a id="S00457"></a>
**[00:30:44 → 00:30:50] [Người nói?]** [nghe không rõ 00:30:44; cần đối chiếu] gần gan tự thi ai như thế nào thì không anh nhanh anh cứ hiểu chỉ đơn giản anh biết là nó sẽ hết rồi

<a id="S00458"></a>
**[00:30:50 → 00:30:58] [Người nói?]** [nghe không rõ 00:30:50; cần đối chiếu] với ý là cái MSP hay là những cái nguồn TI khác, CTI thì nó chỉ có nguồn thầu hết là các IOC

<a id="S00459"></a>
**[00:30:59 → 00:31:06] [Người nói?]** [nghe không rõ 00:30:59; cần đối chiếu] Đa số là thế, IP, Domain hoặc là Pilot mấy cái đấy đều là IOC

<a id="S00460"></a>
**[00:31:06 → 00:31:10] [Người nói?]** [nghe không rõ 00:31:06; cần đối chiếu] thì IP và Domain anh không biết nó gen ra kiểu gì, còn Pilot thì may là có thể

<a id="S00461"></a>
**[00:31:13 → 00:31:18] [Người nói?]** [nghe không rõ 00:31:13; cần đối chiếu] Nói thật ra IP với cả thường bị đánh chặn

<a id="S00462"></a>
**[00:31:18 → 00:31:20] [Người nói?]** [nghe không rõ 00:31:18; cần đối chiếu] những cái này là cái specific nhất

<a id="S00463"></a>
**[00:31:21 → 00:31:22] [Người nói?]** [nghe không rõ 00:31:21; cần đối chiếu] không thường hai cái đấy là bỏ qua

<a id="S00464"></a>
**[00:31:22 → 00:31:24] [Người nói?]** [nghe không rõ 00:31:22; cần đối chiếu] cái đó là hash

<a id="S00465"></a>
**[00:31:24 → 00:31:25] [Người nói?]** [nghe không rõ 00:31:24; cần đối chiếu] hash với cả

<a id="S00466"></a>
**[00:31:25 → 00:31:28] [Người nói?]** [nghe không rõ 00:31:25; cần đối chiếu] hash với cả gì hash nhỉ

<a id="S00467"></a>
**[00:31:28 → 00:31:28] [Người nói?]** [nghe không rõ 00:31:28; cần đối chiếu] imhash

<a id="S00468"></a>
**[00:31:29 → 00:31:32] [Người nói?]** [nghe không rõ 00:31:29; cần đối chiếu] imhash là một phần

<a id="S00469"></a>
**[00:31:32 → 00:31:34] [Người nói?]** [nghe không rõ 00:31:32; cần đối chiếu] tức là để theo dõi nhiều họ một lúc ấy

<a id="S00470"></a>
**[00:31:34 → 00:31:35] [Người nói?]** [nghe không rõ 00:31:34; cần đối chiếu] thì người ta đem được imhash

<a id="S00471"></a>
**[00:31:35 → 00:31:38] [Người nói?]** [nghe không rõ 00:31:35; cần đối chiếu] một loại hash của những cái có liên quan đến cái hash này

<a id="S00472"></a>
**[00:31:38 → 00:31:41] [Người nói?]** [nghe không rõ 00:31:38; cần đối chiếu] ví dụ là binary này import

<a id="S00473"></a>
**[00:31:41 → 00:31:41] [Người nói?]** [nghe không rõ 00:31:41; cần đối chiếu] những thư kiện nào ấy

<a id="S00474"></a>
**[00:31:42 → 00:31:44] [Người nói?]** [nghe không rõ 00:31:42; cần đối chiếu] imhash nó sẽ chỉ dưới cái phần chung đấy thôi

<a id="S00475"></a>
**[00:31:45 → 00:31:47] [Người nói?]** [nghe không rõ 00:31:45; cần đối chiếu] nhưng mà nếu mà em tải

<a id="S00476"></a>
**[00:31:48 → 00:31:54] [Người nói?]** [nghe không rõ 00:31:48; cần đối chiếu] Nhằm tải mấy cái thư viện, một vài cái thư viện, và người chung thì nó sẽ đánh vào

<a id="S00477"></a>
**[00:31:54 → 00:31:59] [Người nói?]** [nghe không rõ 00:31:54; cần đối chiếu] Nó sẽ tính ra là cái in-house và có thể biết là họ này với họ này có liên quan đến nhau không, có chung một mẹ hay không, kiểu gì đấy

<a id="S00478"></a>
**[00:32:03 → 00:32:11] [Người nói?]** [nghe không rõ 00:32:03; cần đối chiếu] IOC có nhiều kiểu lắm, em phải lựa xem là IOC nào có thể dạy gan được, IOC nào có thể dùng tận dụng, rồi mới tính tiếp được

<a id="S00479"></a>
**[00:32:12 → 00:32:13] [Người nói?]** [nghe không rõ 00:32:12; cần đối chiếu] Đấy là nếu nó hướng dưới ai

## Tấn công web (XSS, SQLi) và ràng buộc ngữ pháp khi sinh GAN

<a id="S00480"></a>
**[00:32:13 → 00:32:27] [Người nói?]** Còn ở Core 6 thì nó sẽ phải unpack và tìm tác tích của mỗi cái Artifact ấy

<a id="S00481"></a>
**[00:32:28 → 00:32:32] [Người nói?]** Ví dụ là Manware gì đấy, cái đấy phức tạp hơn nữa

<a id="S00482"></a>
**[00:32:32 → 00:32:34] [Người nói?]** Cái đấy thì em không làm được

<a id="S00483"></a>
**[00:32:34 → 00:32:38] [Người nói?]** Cái đấy thì hơi sâu về phần Assignment

<a id="S00484"></a>
**[00:32:38 → 00:32:39] [Người nói?]** Ừ

<a id="S00485"></a>
**[00:32:39 → 00:32:44] [Người nói?]** Đấy thì Adem lại chưa được làm được thôi

<a id="S00486"></a>
**[00:32:44 → 00:32:46] [Người nói?]** Em chỉ làm cái bề kiểu nông nông

<a id="S00487"></a>
**[00:32:47 → 00:32:49] [Người nói?]** Tập trung vào mấy cái tầng thông web

<a id="S00488"></a>
**[00:32:50 → 00:32:53] [Người nói?]** [nghe không rõ 00:32:50; cần đối chiếu] Em chỉ tập trung vào mấy cái tính công web trước

<a id="S00489"></a>
**[00:32:54 → 00:32:56] [Người nói?]** [nghe không rõ 00:32:54; cần đối chiếu] XSS, SVL là 2 cái

<a id="S00490"></a>
**[00:32:56 → 00:32:59] [Người nói?]** [nghe không rõ 00:32:56; cần đối chiếu] Em hãy đi từ các nguồn CVE

<a id="S00491"></a>
**[00:33:01 → 00:33:05] [Người nói?]** [nghe không rõ 00:33:01; cần đối chiếu] CVE sẽ để lại exploit code để tạo ra GAN

<a id="S00492"></a>
**[00:33:05 → 00:33:09] [Người nói?]** [nghe không rõ 00:33:05; cần đối chiếu] Em cũng làm yêu thương đấy nhưng mà

<a id="S00493"></a>
**[00:33:09 → 00:33:12] [Người nói?]** [nghe không rõ 00:33:09; cần đối chiếu] Bên đấy nó kiểu đặc thù quá

<a id="S00494"></a>
**[00:33:13 → 00:33:16] [Người nói?]** [nghe không rõ 00:33:13; cần đối chiếu] Các CVE không thể liên hệ với nhau được

<a id="S00495"></a>
**[00:33:22 → 00:33:36] [Người nói?]** Nhưng mà các biến thể này nó không có tính liên kết với nhau anh, bởi vì là mỗi một câu là phải có ngữ pháp riêng ý anh, ví dụ như là học kiểu 10 ngữ pháp là em cũng chưa làm được, nó rất dễ bị trồng trèo ý anh.

<a id="S00496"></a>
**[00:33:39 → 00:33:45] [Người nói?]** Nó dễ bị vô nghĩa, nó chỉ đơn giản là ghép với nhau như Lego vậy anh

<a id="S00497"></a>
**[00:33:45 → 00:33:47] [Người nói?]** Kiểu anh có cái tàu Lego anh tháo ra

<a id="S00498"></a>
**[00:33:49 → 00:33:55] [Người nói?]** Thế nên là kể cả là nó có độc nhất thì ít nhất phải có các tính liên kết

<a id="S00499"></a>
**[00:33:55 → 00:33:57] [Người nói?]** Nó kiểu phải có ngũ pháp

<a id="S00500"></a>
**[00:33:57 → 00:33:58] [Người nói?]** Như SQL

<a id="S00501"></a>
**[00:33:59 → 00:34:02] [Người nói?]** Vâng, hiện tại SQL, XSS là 2 cái mà dễ nhất rồi

<a id="S00502"></a>
**[00:34:02 → 00:34:06] [Người nói?]** Còn tấn công như kiểu là đi đốt vào mấy cái kia là khó quá

<a id="S00503"></a>
**[00:34:06 → 00:34:09] [Người nói?]** Mấy cái kia là kiểu gây nhiễu

<a id="S00504"></a>
**[00:34:09 → 00:34:10] [Người nói?]** Thế là nó dùng đủ mọi cái

<a id="S00505"></a>
**[00:34:20 → 00:34:24] [Người nói?]** Thế thắng là làm cái khác

<a id="S00506"></a>
**[00:34:24 → 00:34:26] [Người nói?]** Thế thắng là làm liên quan tới

<a id="S00507"></a>
**[00:34:26 → 00:34:27] [Người nói?]** Phần mềm

<a id="S00508"></a>
**[00:34:27 → 00:34:29] [Người nói?]** Cái của thầy thắng

<a id="S00509"></a>
**[00:34:31 → 00:34:33] [Người nói?]** Cái thắng sẽ

<a id="S00510"></a>
**[00:34:33 → 00:34:35] [Người nói?]** Công kinh hơn

<a id="S00511"></a>
**[00:34:37 → 00:34:38] [Người nói?]** Thắng như là có nghiên cứu cả UAV mà

<a id="S00512"></a>
**[00:34:39 → 00:34:41] [Người nói?]** Thầy Thắng giờ chắc là không làm được gì nữa

<a id="S00513"></a>
**[00:34:41 → 00:34:42] [Người nói?]** Thầy phải gồng ghê quá

<a id="S00514"></a>
**[00:34:43 → 00:34:47] [Người nói?]** Bây giờ đang sát nhập 2 cơ sở vào

<a id="S00515"></a>
**[00:34:48 → 00:34:49] [Người nói?]** Lên lại văn phòng

<a id="S00516"></a>
**[00:34:49 → 00:34:50] [Người nói?]** Sao đến rồi?

<a id="S00517"></a>
**[00:34:51 → 00:34:52] [Người nói?]** Học báo cuối rồi

<a id="S00518"></a>
**[00:34:55 → 00:34:56] [Người nói?]** Học báo đến 5h

<a id="S00519"></a>
**[00:34:56 → 00:34:57] [Người nói?]** Học báo đến 5h

<a id="S00520"></a>
**[00:34:59 → 00:35:00] [Người nói?]** Ý là hết tên ảnh

<a id="S00521"></a>
**[00:35:09 → 00:39:13] [Người nói?]** Mặt giỏi của anh

<a id="S00522"></a>
**[00:39:17 → 00:39:18] [Người nói?]** Với người ít duy nhất đây

<a id="S00523"></a>
**[00:39:18 → 00:39:21] [Người nói?]** Cái gì là góng phát là cả 1 lớp

<a id="S00524"></a>
**[00:39:21 → 00:39:23] [Người nói?]** Không muốn nhắc về tình

<a id="S00525"></a>
**[00:39:24 → 00:39:29] [Người nói?]** [nghe không rõ 00:39:24; cần đối chiếu] Hãy subscribe cho kênh La La School Để không bỏ lỡ những video hấp dẫn
