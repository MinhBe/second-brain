# Voice 018 — làm rõ ứng dụng, bằng chứng và nền tảng của đề tài GAN

Nguồn: [Voice 018.m4a](file:///C:/Users/Admin/Documents/Collection/Data/Recording/Voice%20018.m4a)

Thời lượng: 01:20:19. ASR: large-v3 / cuda.

Trạng thái: đã rà văn bản; chờ nghe đối chiếu. Người nói chưa được xác định nếu không có ghi chú riêng.
Bản này bảo toàn thứ tự và nội dung nhận dạng; các đoạn nghi lỗi được giữ dấu vết để nghe lại.

## Đề tài làm gì và các giả định dữ liệu từ đâu

<a id="S00001"></a>
**[00:00:00 → 00:00:07] [Người nói?]** không dùng thuật toán của ai đây anh thì trên này mày thấy tao thấy cái tiêu đề của mày là khác mà

<a id="S00002"></a>
**[00:00:07 → 00:00:16] [Người nói?]** đây anh thì là làm mấy cái thằng còn lại gan gồm gì đấy vâng thì gan nó là cái lộn gì gan là thuật

<a id="S00003"></a>
**[00:00:16 → 00:00:22] [Người nói?]** toán của ai đây anh nghĩa là bình thường thì sẽ là kiểu copy paste các cái câu lệnh lên thì bây giờ

<a id="S00004"></a>
**[00:00:22 → 00:00:30] [Người nói?]** là em sẽ chọn lấy những cái keyword mà quan trọng để có thể tập trung vào đó mà sinh ra dữ liệu

<a id="S00005"></a>
**[00:00:30 → 00:00:32] [Người nói?]** [ASR cần nghe lại] để kiểu làm mới bộ dữ liệu lên thôi anh

<a id="S00006"></a>
**[00:00:32 → 00:00:37] [Người nói?]** [ASR cần nghe lại] nghĩa là một phương pháp mà kiểu nó sinh dữ liệu nó thông minh hơn

<a id="S00007"></a>
**[00:00:37 → 00:00:42] [Người nói?]** [ASR cần nghe lại] thì về cơ bản là nó sẽ vượt trội hơn các phương án truyền thống chỉ đơn giản là copy paste

<a id="S00008"></a>
**[00:00:42 → 00:00:45] [Người nói?]** [ASR cần nghe lại] thì hiện tại thì là

<a id="S00009"></a>
**[00:00:45 → 00:00:46] [Người nói?]** [ASR cần nghe lại] copy paste vào đâu?

<a id="S00010"></a>
**[00:00:47 → 00:00:50] [Người nói?]** [ASR cần nghe lại] bây giờ có 70 câu thì đẩy lên thành hơn

<a id="S00011"></a>
**[00:00:50 → 00:00:52] [Người nói?]** [ASR cần nghe lại] 70 câu thì mẹ à

<a id="S00012"></a>
**[00:00:52 → 00:00:57] [Người nói?]** [ASR cần nghe lại] nó block thì mấy trăm nghìn

<a id="S00013"></a>
**[00:00:57 → 00:01:01] [Người nói?]** [ASR cần nghe lại] có nghĩa là kiểu trong AI thì nó sẽ cần một lượng lớn dữ liệu ý ạ

<a id="S00014"></a>
**[00:01:01 → 00:01:07] [Người nói?]** Ừ, bây giờ payload mày search bừa trên mạng cũng phải mấy chục nghìn câu

<a id="S00015"></a>
**[00:01:07 → 00:01:11] [Người nói?]** Nhưng mà payload mà khai thác nội bộ của công ty cơ anh

<a id="S00016"></a>
**[00:01:11 → 00:01:11] [Người nói?]** Nghĩa là

<a id="S00017"></a>
**[00:01:11 → 00:01:19] [Người nói?]** Công ty nào nó chẳng như nhau, database nào thì nó ứng với query đấy chứ còn của công ty thì

<a id="S00018"></a>
**[00:01:19 → 00:01:27] [Người nói?]** [nghe không rõ 00:01:19; cần đối chiếu] Em tưởng là mixconfig thì kiểu công ty sẽ mixconfig riêng để kiểu có sự độc nhất để chẳng bị tấn công

<a id="S00019"></a>
**[00:01:27 → 00:01:30] [Người nói?]** [nghe không rõ 00:01:27; cần đối chiếu] Thế mày có hiểu FP audio đâu mà mày phải viết

<a id="S00020"></a>
**[00:01:30 → 00:01:36] [Người nói?]** Bây giờ ý là mày cần tao chỉ cho mày cái gì

<a id="S00021"></a>
**[00:01:36 → 00:01:39] [Người nói?]** Nhờ cái đấy để mày viết ra cái gì thì mày hỏi cái đấy

<a id="S00022"></a>
**[00:01:39 → 00:01:41] [Người nói?]** Chứ còn bây giờ nói là

<a id="S00023"></a>
**[00:01:41 → 00:01:43] [Người nói?]** Không viết thì chắc là chưa

<a id="S00024"></a>
**[00:01:43 → 00:01:46] [Người nói?]** Bởi vì là em còn sau này mày về phải xem lại

<a id="S00025"></a>
**[00:01:46 → 00:01:49] [Người nói?]** Vì là em cũng chưa ý thức được là

<a id="S00026"></a>
**[00:01:49 → 00:01:53] [Người nói?]** Một cuộc tấn công kiểu chỉ bước scanning đầu

<a id="S00027"></a>
**[00:01:53 → 00:01:55] [Người nói?]** Để xem lỗi ở một hệ cơ sở điểm

<a id="S00028"></a>
**[00:01:55 → 00:01:57] [Người nói?]** Thế ý là bây giờ ví dụ

<a id="S00029"></a>
**[00:01:57 → 00:01:59] [Người nói?]** Mày tạo ra cái này để làm gì

<a id="S00030"></a>
**[00:01:59 → 00:02:00] [Người nói?]** Tạo này

<a id="S00031"></a>
**[00:02:03 → 00:02:05] [Người nói?]** Thì các công ty sẽ không phải đưa

<a id="S00032"></a>
**[00:02:05 → 00:02:07] [Người nói?]** Phải lưu tải dữ liệu về nữa

<a id="S00033"></a>
**[00:02:07 → 00:02:09] [Người nói?]** Mà chỉ cần dữ liệu nội bộ thôi

<a id="S00034"></a>
**[00:02:09 → 00:02:11] [Người nói?]** Thì không cần phải tải thêm gì nữa

<a id="S00035"></a>
**[00:02:11 → 00:02:13] [Người nói?]** Ví dụ như bình thường chỉ có

<a id="S00036"></a>
**[00:02:13 → 00:02:15] [Người nói?]** Kiểu 60-70 mẫu

<a id="S00037"></a>
**[00:02:15 → 00:02:16] [Người nói?]** Là pen test tạo ra

<a id="S00038"></a>
**[00:02:16 → 00:02:18] [Người nói?]** Sao này chỉ có 60-70 mẫu nhỉ

<a id="S00039"></a>
**[00:02:18 → 00:02:21] [Người nói?]** Tại sao này chỉ có 60-70 mẫu

<a id="S00040"></a>
**[00:02:21 → 00:02:22] [Người nói?]** Em đang hiểu là

<a id="S00041"></a>
**[00:02:22 → 00:02:24] [Người nói?]** Ví dụ như là nếu như anh làm

<a id="S00042"></a>
**[00:02:24 → 00:02:26] [Người nói?]** Thì anh sẽ thử kiểm thử nội bộ

<a id="S00043"></a>
**[00:02:26 → 00:02:29] [Người nói?]** Thì anh sẽ chỉ tạo ra được một lượng

<a id="S00044"></a>
**[00:02:29 → 00:02:34] [Người nói?]** [nghe không rõ 00:02:29; cần đối chiếu] tầm 1% so với tổng những lượng payload bình thường mà công ty đang có

<a id="S00045"></a>
**[00:02:34 → 00:02:36] [Người nói?]** thì bây giờ làm nào đi?

<a id="S00046"></a>
**[00:02:36 → 00:02:37] [Người nói?]** tao vẫn không hiểu

<a id="S00047"></a>
**[00:02:37 → 00:02:40] [Người nói?]** tại vì cái trên mạng thiếu đéo như vậy

<a id="S00048"></a>
**[00:02:40 → 00:02:43] [Người nói?]** sau này cứ 60-70 mẫu là sao?

<a id="S00049"></a>
**[00:02:43 → 00:02:46] [Người nói?]** cái trên mạng thì được coi là kiểu dữ liệu cộng đồng

<a id="S00050"></a>
**[00:02:46 → 00:02:49] [Người nói?]** thì thường những câu lệnh đấy là đã bị chặn hết rồi

<a id="S00051"></a>
**[00:02:49 → 00:02:51] [Người nói?]** ai chặn?

<a id="S00052"></a>
**[00:02:51 → 00:02:55] [Người nói?]** [nghe không rõ 00:02:51; cần đối chiếu] các cái con Warp

<a id="S00053"></a>
**[00:02:55 → 00:02:58] [Người nói?]** hoặc nó sẽ tải bộ Threat Intelligence về

<a id="S00054"></a>
**[00:02:58 → 00:03:03] [Người nói?]** về và nó sẽ chủ động chặn các cái cái tấn công đấy. Ừ. Thì

<a id="S00055"></a>
**[00:03:03 → 00:03:07] [Người nói?]** bây giờ là có những cái mà tấn công đặc thù hơn ví dụ như là

<a id="S00056"></a>
**[00:03:07 → 00:03:11] [Người nói?]** nó không chặn hết được. Cái của mày thì tao thấy có đặc thù

<a id="S00057"></a>
**[00:03:11 → 00:03:14] [Người nói?]** gì đâu. Vì đang em đang hướng như thế. Thì hiện tại là mới

<a id="S00058"></a>
**[00:03:14 → 00:03:18] [Người nói?]** chứng minh là phương pháp của em thì ổn định hơn phương pháp

<a id="S00059"></a>
**[00:03:18 → 00:03:23] [Người nói?]** thì bây giờ là sẽ cần phải làm với các tất cả các tấn công

<a id="S00060"></a>
**[00:03:23 → 00:03:29] [Người nói?]** khác. Nhưng mà sao này sáu mươi bảy mươi lâu nhỉ? Thì

<a id="S00061"></a>
**[00:03:29 → 00:03:34] [Người nói?]** sau đấy nó sinh thì nó mới học được chứ

<a id="S00062"></a>
**[00:03:34 → 00:03:38] [Người nói?]** thì nó thấy giống dạng nào thì nó mới học

<a id="S00063"></a>
**[00:03:38 → 00:03:40] [Người nói?]** nó detect là cái dạng đấy

<a id="S00064"></a>
**[00:03:40 → 00:03:44] [Người nói?]** ý em là kiểu kể cả là lấy hết các mẫu ấy à

<a id="S00065"></a>
**[00:03:44 → 00:03:46] [Người nói?]** thì so với các mẫu người dùng thông thường

<a id="S00066"></a>
**[00:03:46 → 00:03:51] [Người nói?]** [nghe không rõ 00:03:46; cần đối chiếu] thì nó chỉ chiếm tầm khoảng dưới 10% đầu xuống

<a id="S00067"></a>
**[00:03:51 → 00:03:53] [Người nói?]** 10% ở đâu? thông số chỗ nào ra?

<a id="S00068"></a>
**[00:03:54 → 00:03:54] [Người nói?]** dạ

<a id="S00069"></a>
**[00:03:54 → 00:03:55] [Người nói?]** thông số ở đâu?

<a id="S00070"></a>
**[00:03:55 → 00:03:58] [Người nói?]** các payload bình thường của người dùng ấy anh

<a id="S00071"></a>
**[00:03:58 → 00:03:58] [Người nói?]** là sao?

<a id="S00072"></a>
**[00:03:58 → 00:04:01] [Người nói?]** nghĩa là một ngày thì

<a id="S00073"></a>
**[00:04:01 → 00:04:04] [Người nói?]** bây lốt thông thường người dùng thì liên quan đéo đến tấn công nhỉ?

<a id="S00074"></a>
**[00:04:04 → 00:04:07] [Người nói?]** nghĩa là các cái truy vấn bình thường của người dùng về cơ sở dữ liệu

<a id="S00075"></a>
**[00:04:07 → 00:04:12] [Người nói?]** [nghe không rõ 00:04:07; cần đối chiếu] thì so với lượng bây lốt tấn công thì là sẽ ít hơn hẳn

<a id="S00076"></a>
**[00:04:12 → 00:04:14] [Người nói?]** ừ, thì liên quan đéo gì?

<a id="S00077"></a>
**[00:04:15 → 00:04:17] [Người nói?]** bây giờ mình đang cẩn trận tấn công mà

<a id="S00078"></a>
**[00:04:17 → 00:04:22] [Người nói?]** những thằng tấn công thì nó sẽ lấy hết, nó sẽ lấy chỉ mỗi dữ liệu người dùng

<a id="S00079"></a>
**[00:04:22 → 00:04:27] [Người nói?]** mà thằng học máy thì nó sẽ không, lúc đầu nó sẽ không biết đâu là tấn công

<a id="S00080"></a>
**[00:04:27 → 00:04:29] [Người nói?]** mình truyền vào ạ?

<a id="S00081"></a>
**[00:04:29 → 00:04:30] [Người nói?]** Vâng kể cả sau đấy ạ

<a id="S00082"></a>
**[00:04:30 → 00:04:32] [Người nói?]** Kể cả sau đấy là như nào

<a id="S00083"></a>
**[00:04:34 → 00:04:35] [Người nói?]** Nghĩa là khi mà đưa vào mô hình

<a id="S00084"></a>
**[00:04:35 → 00:04:37] [Người nói?]** Thì không để đưa thuật tấn công được

<a id="S00085"></a>
**[00:04:37 → 00:04:40] [Người nói?]** Phải đưa cả mẫu bình thường để nó biết đâu là mẫu cần chặn

<a id="S00086"></a>
**[00:04:40 → 00:04:41] [Người nói?]** Và đâu là mẫu có thể bỏ qua

<a id="S00087"></a>
**[00:04:43 → 00:04:45] [Người nói?]** Thì xe có những mẫu mà nó

<a id="S00088"></a>
**[00:04:46 → 00:04:48] [Người nói?]** Mẫu nào là mẫu cần bỏ qua

<a id="S00089"></a>
**[00:04:48 → 00:04:49] [Người nói?]** Nó

<a id="S00090"></a>
**[00:04:50 → 00:04:51] [Người nói?]** Ông này chả hiểu đéo

<a id="S00091"></a>
**[00:04:52 → 00:04:53] [Người nói?]** Ví dụ nha

<a id="S00092"></a>
**[00:04:53 → 00:04:55] [Người nói?]** Ví dụ nó thực thi trong

<a id="S00093"></a>
**[00:04:56 → 00:04:56] [Người nói?]** DB đúng không

<a id="S00094"></a>
**[00:04:57 → 00:04:59] [Người nói?]** Thì cái thằng nó cần check là

<a id="S00095"></a>
**[00:04:59 → 00:05:00] [Người nói?]** Cái thằng

<a id="S00096"></a>
**[00:05:01 → 00:05:04] [Người nói?]** thằng nào đòi thực thi

<a id="S00097"></a>
**[00:05:06 → 00:05:07] [Người nói?]** bình thường

<a id="S00098"></a>
**[00:05:07 → 00:05:09] [Người nói?]** thằng web thực thi đúng không

<a id="S00099"></a>
**[00:05:09 → 00:05:12] [Người nói?]** thì ông web đấy

<a id="S00100"></a>
**[00:05:12 → 00:05:14] [Người nói?]** thực thi là từ chức năng nào

<a id="S00101"></a>
**[00:05:14 → 00:05:16] [Người nói?]** ví dụ

<a id="S00102"></a>
**[00:05:16 → 00:05:18] [Người nói?]** như tên người dùng chẳng hạn

<a id="S00103"></a>
**[00:05:19 → 00:05:21] [Người nói?]** tên người dùng nó thực thi cái gì

<a id="S00104"></a>
**[00:05:21 → 00:05:25] [Người nói?]** nó sẽ query cái gì để nó ra

<a id="S00105"></a>
**[00:05:25 → 00:05:25] [Người nói?]** cái tên người dùng đó

<a id="S00106"></a>
**[00:05:25 → 00:05:32] [Người nói?]** mày đang chặn cái gì tao chưa hiểu

<a id="S00107"></a>
**[00:05:32 → 00:05:35] [Người nói?]** mày đang muốn sinh ra

<a id="S00108"></a>
**[00:05:35 → 00:05:37] [Người nói?]** để nhiều

<a id="S00109"></a>
**[00:05:37 → 00:05:38] [Người nói?]** cái payload đúng không

<a id="S00110"></a>
**[00:05:38 → 00:05:44] [Người nói?]** Vâng và dựa vào những cái để chặn những thằng bên ngoài thì vâng nhưng mà các em đang thấy là

<a id="S00111"></a>
**[00:05:44 → 00:05:52] [Người nói?]** khi bình thường là người ta cũng đã làm hết rồi kiểu không dùng nghĩa là mấy các cái câu ờ các

<a id="S00112"></a>
**[00:05:52 → 00:06:02] [Người nói?]** cái câu tấn công là cũng đã được lên rồi để có gì mọi người đem về làm kiểu bộ trạng riêng ý ạ ừ

<a id="S00113"></a>
**[00:06:02 → 00:06:08] [Người nói?]** thì nên là bây giờ ít nhất là vệ sinh là có khả năng học được những mẫu cao cấp hơn vượt lên

<a id="S00114"></a>
**[00:06:08 → 00:06:17] [Người nói?]** Các mẫu mã nguồn mở như thế này có những mẫu mà có khả năng tự ẩn ẩn ẩn đi các cái mục đích

<a id="S00115"></a>
**[00:06:17 → 00:06:25] [Người nói?]** [nghe không rõ 00:06:17; cần đối chiếu] này kiểu có những cái ký quát đặc biệt hơn để vượt qua được từng lửa thông thường là cái gì

<a id="S00116"></a>
**[00:06:25 → 00:06:39] [Người nói?]** đây có cái đi phương sinh em em để mới biết cái gợi ý cái đấy thì chỉ có chất lượng chỉ có từng

## Chất lượng mẫu và bằng chứng thực nghiệm

<a id="S00117"></a>
**[00:06:42 → 00:06:47] [Người nói?]** Đấy, thì thường dữ liệu nó sinh ra nó sẽ bị lẫn

<a id="S00118"></a>
**[00:06:47 → 00:06:49] [Người nói?]** Bây giờ cố gắng tinh chỉnh

<a id="S00119"></a>
**[00:06:52 → 00:06:53] [Người nói?]** Mấy cô này khai thác được rồi

<a id="S00120"></a>
**[00:06:54 → 00:06:57] [Người nói?]** Mấy cô này nếu như đưa vào mô hình mà không có phòng thủ gì

<a id="S00121"></a>
**[00:06:57 → 00:07:01] [Người nói?]** Vẫn khai thác được rồi, không dùng tường rửa gì

<a id="S00122"></a>
**[00:07:01 → 00:07:06] [Người nói?]** Em phải tưởng là nó không có khả năng vì nó bị chặn hết

<a id="S00123"></a>
**[00:07:06 → 00:07:08] [Người nói?]** Chặn cái gì?

<a id="S00124"></a>
**[00:07:08 → 00:07:10] [Người nói?]** Đây, bên này là kiểu đưa vào tường rửa

<a id="S00125"></a>
**[00:07:10 → 00:07:11] [Người nói?]** Nó bắt ru thì nó chặn luôn

<a id="S00126"></a>
**[00:07:18 → 00:07:19] [Người nói?]** Còn tao khẳng định luôn

<a id="S00127"></a>
**[00:07:19 → 00:07:21] [Người nói?]** Mấy cái máy sinh ra chắc chắn là vẫn bị chặn

<a id="S00128"></a>
**[00:07:23 → 00:07:32] [Người nói?]** [nghe không rõ 00:07:23; cần đối chiếu] Đối với mày vượt được đấy, nếu mà mày làm 1 con F5, 1 con quát vào, mày cho 1 con quát vào, mày thử chạy thử xem, chứng minh đi.

<a id="S00129"></a>
**[00:07:35 → 00:07:38] [Người nói?]** Thế ví dụ mày dùng con AI mày sinh ra được đúng không?

<a id="S00130"></a>
**[00:07:38 → 00:07:45] [Người nói?]** Mày sinh được thì mày phải bypass được con đấy, mày phải bypass được cái bộ chặn đấy.

<a id="S00131"></a>
**[00:07:46 → 00:07:49] [Người nói?]** Tại vì mày bảo là mày đặc biệt hơn chúng nó mà.

<a id="S00132"></a>
**[00:07:50 → 00:07:55] [Người nói?]** Mày bảo đặc biệt hơn thì những cái bộ mà sinh ra mà con này có, thì thằng khác không có đúng không?

<a id="S00133"></a>
**[00:07:55 → 00:08:02] [Người nói?]** đúng không ạ thì mày phiêu vào những thằng khác thì thằng khác nó phải khai thác được chỉ phiêu

<a id="S00134"></a>
**[00:08:02 → 00:08:07] [Người nói?]** vào con của mày thì con của mày mới chặn được thôi còn tất cả con khác nó đều phiêu qua hiểu chưa

<a id="S00135"></a>
**[00:08:08 → 00:08:16] [Người nói?]** Vâng cái đấy hợp ý anh cái đấy đúng em nhầm cái ý là cái đấy thì em có ý thức được thì em có làm cái

<a id="S00136"></a>
**[00:08:16 → 00:08:22] [Người nói?]** đấy rồi làm cái gì mày làm cái gì mày kể tao nghe mày làm cái gì ở mức các bạn nói nghĩa là em đưa

<a id="S00137"></a>
**[00:08:22 → 00:08:29] [Người nói?]** đưa vào nghĩa là sau mô hình con mô hình của em sau khi mà học được bộ dữ liệu mới thì chặn được

<a id="S00138"></a>
**[00:08:29 → 00:08:38] [Người nói?]** [nghe không rõ 00:08:29; cần đối chiếu] Còn nếu mà dùng các cái ru máu nguồn mở thì là 60 70 câu gì không Cái đấy là con một security

<a id="S00139"></a>
**[00:08:40 → 00:08:50] [Người nói?]** [nghe không rõ 00:08:40; cần đối chiếu] 2022 bộ bộ ru xe một security 2022 máu nguồn mở trên mạng thôi thì là con con đấy thì chặn chặn

<a id="S00140"></a>
**[00:08:50 → 00:08:52] [Người nói?]** Thì em dùng

<a id="S00141"></a>
**[00:08:56 → 00:08:58] [Người nói?]** Thì đầu tiên là chứng minh là hơn được

<a id="S00142"></a>
**[00:08:59 → 00:08:59] [Người nói?]** Ruset trước rồi

<a id="S00143"></a>
**[00:09:08 → 00:09:10] [Người nói?]** [nghe không rõ 00:09:08; cần đối chiếu] Không được dùng bộ 2026 anh

<a id="S00144"></a>
**[00:09:10 → 00:09:11] [Người nói?]** Bởi vì là chưa ai làm

<a id="S00145"></a>
**[00:09:11 → 00:09:14] [Người nói?]** Thì là mọi người chỉ dùng bộ 2022

<a id="S00146"></a>
**[00:09:14 → 00:09:16] [Người nói?]** Nên phải dựa vào đấy để chứng minh là

<a id="S00147"></a>
**[00:09:16 → 00:09:17] [Người nói?]** Mình có cải thiện

<a id="S00148"></a>
**[00:09:17 → 00:09:20] [Người nói?]** Đương nhiên là cải thiện thì so với bây giờ

<a id="S00149"></a>
**[00:09:20 → 00:09:21] [Người nói?]** Là nó bị lỗi thờ

<a id="S00150"></a>
**[00:09:21 → 00:09:24] [Người nói?]** nhưng mà vẫn phải chứng minh là có cải thiện trước đã.

<a id="S00151"></a>
**[00:09:24 → 00:09:33] [Người nói?]** Mày chứng minh được là bây giờ nếu mà cho vào trong cái rule set của mày thì

<a id="S00152"></a>
**[00:09:33 → 00:09:35] [Người nói?]** cho vào cái mode thì nó khai thác được.

<a id="S00153"></a>
**[00:09:36 → 00:09:38] [Người nói?]** Đâu, cái khai thác được đâu, chụp ảnh thôi.

<a id="S00154"></a>
**[00:09:38 → 00:09:40] [Người nói?]** Thì đấy, ở trong cái quyển của em nhưng mà...

<a id="S00155"></a>
**[00:09:40 → 00:09:41] [Người nói?]** Đây, quyển của mày đây.

<a id="S00156"></a>
**[00:09:41 → 00:09:44] [Người nói?]** Thì nó chỉ đưa thủ số chặn thôi anh, còn...

<a id="S00157"></a>
**[00:09:44 → 00:09:45] [Người nói?]** Như nào, như nào?

<a id="S00158"></a>
**[00:09:45 → 00:09:47] [Người nói?]** Đây thì mấy cái câu mà anh đang nhìn đây anh.

<a id="S00159"></a>
**[00:09:47 → 00:09:48] [Người nói?]** Là nó chặn?

<a id="S00160"></a>
**[00:09:48 → 00:09:51] [Người nói?]** Vâng, là nó chặn còn...

<a id="S00161"></a>
**[00:09:51 → 00:09:52] [Người nói?]** Câu của mày đâu, câu của mày thì nó không chặn đâu.

<a id="S00162"></a>
**[00:09:52 → 00:09:58] [Người nói?]** [nghe không rõ 00:09:52; cần đối chiếu] Đang không để trong quyển với gạch kia nhưng mà chỉ có tầm hơn 7

<a id="S00163"></a>
**[00:10:00 → 00:10:04] [Người nói?]** [nghe không rõ 00:10:00; cần đối chiếu] bảy tầm mấy phần trăm là không bị chạm rồi anh nhưng mà mẫu đâu phải không

<a id="S00164"></a>
**[00:10:04 → 00:10:11] [Người nói?]** chạm đâu không được rồi em không đưa ở đây ạ Thế cái quyển của mày gì kia nó chỉ có thông số

<a id="S00165"></a>
**[00:10:11 → 00:10:18] [Người nói?]** đâu số đâu là mày chỉ ghi là bao nhiêu phần trăm á Vâng thế là ông đéo làm à vậy không làm anh không

<a id="S00166"></a>
**[00:10:18 → 00:10:23] [Người nói?]** Thế không có hình à? Ông nào mà nói không có hình á?

<a id="S00167"></a>
**[00:10:23 → 00:10:25] [Người nói?]** Như này hình gì anh?

<a id="S00168"></a>
**[00:10:25 → 00:10:30] [Người nói?]** Ôi địt mẹ, thằng nào nó cho mày tát cái thạc sĩ nó cũng vãi lồn thật

<a id="S00169"></a>
**[00:10:30 → 00:10:36] [Người nói?]** Không, em, các thầy chỉ quan tâm là mô hình AI thôi chứ không quan tâm thực tế nào

<a id="S00170"></a>
**[00:10:36 → 00:10:38] [Người nói?]** Thì bây giờ là em mới quan tâm thực tế

<a id="S00171"></a>
**[00:10:38 → 00:10:43] [Người nói?]** Còn hầu hết cả mô hình của em chỉ là toàn kiểu vẽ kiến trúc các kiểu thôi

<a id="S00172"></a>
**[00:10:43 → 00:10:45] [Người nói?]** Cái đấy...

<a id="S00173"></a>
**[00:10:47 → 00:10:49] [Người nói?]** Cái đấy trên mạng đầy, bị bệ hả?

<a id="S00174"></a>
**[00:10:49 → 00:10:51] [Người nói?]** Không, không, cái của em thì không có

<a id="S00175"></a>
**[00:10:51 → 00:10:54] [Người nói?]** Cái của em chỉ có 6 người làm thôi

<a id="S00176"></a>
**[00:10:54 → 00:10:56] [Người nói?]** Em cải thiện hơn người ta 1 tí

<a id="S00177"></a>
**[00:10:56 → 00:10:57] [Người nói?]** Chết

<a id="S00178"></a>
**[00:11:00 → 00:11:05] [Người nói?]** Đâu thông thố đâu

<a id="S00179"></a>
**[00:11:05 → 00:11:06] [Người nói?]** Được à

<a id="S00180"></a>
**[00:11:06 → 00:11:07] [Người nói?]** Cho xem thông thố nào

<a id="S00181"></a>
**[00:11:07 → 00:11:08] [Người nói?]** Đấy không

<a id="S00182"></a>
**[00:11:08 → 00:11:10] [Người nói?]** Đây cái đoạn tùng lửa bay

<a id="S00183"></a>
**[00:11:10 → 00:11:11] [Người nói?]** Bay gút

<a id="S00184"></a>
**[00:11:11 → 00:11:14] [Người nói?]** Đây đây gì

<a id="S00185"></a>
**[00:11:14 → 00:11:15] [Người nói?]** Thông

<a id="S00186"></a>
**[00:11:15 → 00:11:16] [Người nói?]** À đúng rồi

<a id="S00187"></a>
**[00:11:16 → 00:11:17] [Người nói?]** Làm sao

<a id="S00188"></a>
**[00:11:17 → 00:11:18] [Người nói?]** Đây đây

<a id="S00189"></a>
**[00:11:18 → 00:11:21] [Người nói?]** Thông thố nó như thế nào

<a id="S00190"></a>
**[00:11:21 → 00:11:22] [Người nói?]** Đây là cái cột mà

<a id="S00191"></a>
**[00:11:23 → 00:11:24] [Người nói?]** Thì bị chặn

<a id="S00192"></a>
**[00:11:24 → 00:11:25] [Người nói?]** Bị chặn là sao

<a id="S00193"></a>
**[00:11:25 → 00:11:25] [Người nói?]** Nghĩa là

<a id="S00194"></a>
**[00:11:25 → 00:11:27] [Người nói?]** Pilot nó bắt được

<a id="S00195"></a>
**[00:11:27 → 00:11:28] [Người nói?]** Là dạng tấn công

<a id="S00196"></a>
**[00:11:28 → 00:11:28] [Người nói?]** Thì nó

<a id="S00197"></a>
**[00:11:28 → 00:11:30] [Người nói?]** Không cho qua được anh

<a id="S00198"></a>
**[00:11:30 → 00:11:31] [Người nói?]** Nghĩa là kiểu

<a id="S00199"></a>
**[00:11:31 → 00:11:32] [Người nói?]** [nghe không rõ 00:11:31; cần đối chiếu] Đưa qua bộ rưu xét

<a id="S00200"></a>
**[00:11:32 → 00:11:33] [Người nói?]** [nghe không rõ 00:11:32; cần đối chiếu] Rồi bộ rưu xét

<a id="S00201"></a>
**[00:11:33 → 00:11:34] [Người nói?]** Nhận định đâu là tấn công

<a id="S00202"></a>
**[00:11:34 → 00:11:35] [Người nói?]** [ASR cần nghe lại] không phải tấn công đâu, không phải tấn công nha anh

<a id="S00203"></a>
**[00:11:35 → 00:11:38] [Người nói?]** [ASR cần nghe lại] thì là phương pháp cơ bản

<a id="S00204"></a>
**[00:11:38 → 00:11:41] [Người nói?]** [ASR cần nghe lại] thì đây là các dạng tấn công

<a id="S00205"></a>
**[00:11:41 → 00:11:43] [Người nói?]** [ASR cần nghe lại] thì chỉ có là

<a id="S00206"></a>
**[00:11:44 → 00:11:46] [Người nói?]** [ASR cần nghe lại] cái thằng Time với cả thằng Union

<a id="S00207"></a>
**[00:11:46 → 00:11:47] [Người nói?]** [ASR cần nghe lại] thì thực ra là em sinh

<a id="S00208"></a>
**[00:11:47 → 00:11:49] [Người nói?]** [ASR cần nghe lại] linh tinh quá nên là nó không nhận ra nó có phải

<a id="S00209"></a>
**[00:11:49 → 00:11:50] [Người nói?]** [ASR cần nghe lại] payload không thì nó cho qua

<a id="S00210"></a>
**[00:11:50 → 00:11:53] [Người nói?]** [ASR cần nghe lại] còn chỉ tập trung vào đúng 2 cái này thì là

<a id="S00211"></a>
**[00:11:53 → 00:11:54] [Người nói?]** [ASR cần nghe lại] thế có nghĩa là ông không tấn công như gì?

<a id="S00212"></a>
**[00:11:54 → 00:11:57] [Người nói?]** [ASR cần nghe lại] vâng 2 cái này thì gần như là giác vứt đi

<a id="S00213"></a>
**[00:11:57 → 00:11:58] [Người nói?]** [ASR cần nghe lại] chỉ tập trung vào 2 cái bên trên thôi anh

<a id="S00214"></a>
**[00:11:58 → 00:12:00] [Người nói?]** [ASR cần nghe lại] thế mày tấn công qua cái gì?

<a id="S00215"></a>
**[00:12:00 → 00:12:03] [Người nói?]** [nghe không rõ 00:12:00; cần đối chiếu] thì không tấn công qua chỉ đưa qua bộ reset để check thôi anh

<a id="S00216"></a>
**[00:12:05 → 00:12:15] [Người nói?]** đấy là yêu cầu đấy yêu cầu bài luận đi phải làm đúng yêu cầu yêu cầu cái lồng cái bài này mày

<a id="S00217"></a>
**[00:12:15 → 00:12:19] [Người nói?]** chứng minh được cái gì không thấy chả chứng minh được cái gì không chỉ chứng minh là phương pháp

<a id="S00218"></a>
**[00:12:19 → 00:12:28] [Người nói?]** [nghe không rõ 00:12:19; cần đối chiếu] si quần gan ưu việt hơn phương pháp mốt thế là đã là đủ đổ rồi anh còn thực tế không thì bây giờ em

<a id="S00219"></a>
**[00:12:28 → 00:12:35] [Người nói?]** em mới cần anh có thêm từ khóa để làm vì là cái của em nó chỉ là mô hình lý thuyết thôi

<a id="S00220"></a>
**[00:12:35 → 00:12:37] [Người nói?]** giờ phải đưa vào thực tế

<a id="S00221"></a>
**[00:12:37 → 00:12:43] [Người nói?]** thật điệt, tao thấy nó điếu thực tế kì nào luôn

<a id="S00222"></a>
**[00:12:46 → 00:12:48] [Người nói?]** bây giờ ví dụ nha

<a id="S00223"></a>
**[00:12:51 → 00:13:00] [Người nói?]** bây giờ ông nếu mà ông muốn thực tế thì ông phải gọi là có một cái file word đúng không ạ

<a id="S00224"></a>
**[00:13:00 → 00:13:07] [Người nói?]** và ông tự tạo một cái file word của ông sinh bằng cái key của ông

<a id="S00225"></a>
**[00:13:07 → 00:13:11] [Người nói?]** và ông lấy một cái Firewall cũng như thế

<a id="S00226"></a>
**[00:13:11 → 00:13:13] [Người nói?]** nhưng mà xinh bằng key của thằng Public

<a id="S00227"></a>
**[00:13:13 → 00:13:15] [Người nói?]** được chưa

<a id="S00228"></a>
**[00:13:16 → 00:13:16] [Người nói?]** rồi

<a id="S00229"></a>
**[00:13:18 → 00:13:20] [Người nói?]** xong là ông tấn công bằng

<a id="S00230"></a>
**[00:13:20 → 00:13:22] [Người nói?]** những cái Payload

<a id="S00231"></a>
**[00:13:22 → 00:13:25] [Người nói?]** mà ông nghĩ là nó bypass được

<a id="S00232"></a>
**[00:13:25 → 00:13:28] [Người nói?]** vào những cái Rubik's Cube kia

<a id="S00233"></a>
**[00:13:28 → 00:13:29] [Người nói?]** xem là nó

<a id="S00234"></a>
**[00:13:30 → 00:13:31] [Người nói?]** có bị chặn không

## Làm rõ câu hỏi về AI trong công việc

<a id="S00235"></a>
**[00:13:35 → 00:13:36] [Người nói?]** cái đấy thì là

<a id="S00236"></a>
**[00:13:36 → 00:13:38] [Người nói?]** định hướng em sẽ làm cho lần kế tiếp rồi

<a id="S00237"></a>
**[00:13:38 → 00:13:41] [Người nói?]** nhưng mà em đang

<a id="S00238"></a>
**[00:13:41 → 00:13:43] [Người nói?]** hôm nay em đang muốn hỏi là cách anh dùng AI

<a id="S00239"></a>
**[00:13:43 → 00:13:53] [Người nói?]** là những cái dữ liệu mà ai sinh ra ấy hoặc là anh dùng ai để nó hỗ trợ cái công đoạn nào còn cái anh

<a id="S00240"></a>
**[00:13:53 → 00:13:59] [Người nói?]** cái anh kể là đây sẽ là lần là ý là yêu cầu tiếp theo em cần phải làm cái lần thạc sĩ này chỉ là

<a id="S00241"></a>
**[00:13:59 → 00:14:05] [Người nói?]** [nghe không rõ 00:13:59; cần đối chiếu] coi như là đề xuất là thằng sinh quân chỉ đơn giản là một luật toán của khẳng vượt trội hơn

<a id="S00242"></a>
**[00:14:05 → 00:14:12] [Người nói?]** hơn với các thuật toán truyền thống. Thuật toán truyền thống là cái SMOTE mà em nói đi anh.

<a id="S00243"></a>
**[00:14:13 → 00:14:20] [Người nói?]** SMOTE thì nó làm gì? Nó sẽ nội suy nghĩa là nó cứ ghép ghép từ thôi. Đầu tiên là nó chọn những cái

<a id="S00244"></a>
**[00:14:20 → 00:14:25] [Người nói?]** keyword mà xuất hiện nhiều. Ví dụ như là trong một câu mà nó có các từ như kiểu select hoặc là

<a id="S00245"></a>
**[00:14:27 → 00:14:32] [Người nói?]** benchmark thì nó có thể xuất hiện nhiều. Nó nghĩ là đây là những từ key. Sau đó nó sẽ cố gắng sao

<a id="S00246"></a>
**[00:14:32 → 00:14:40] [Người nói?]** [nghe không rõ 00:14:32; cần đối chiếu] đào hết cái đồng đề lên rồi đưa qua một bộ lọc chính là bộ reset của thằng nó bộ reset của một

<a id="S00247"></a>
**[00:14:40 → 00:14:45] [Người nói?]** thằng tường lửa Nếu mà nó bị chặn và bị coi là tấn công và kiểu có giải thích thì nó sẽ coi như

<a id="S00248"></a>
**[00:14:45 → 00:14:51] [Người nói?]** đấy là một câu Payload chuẩn thì nó sẽ làm dầu bộ dữ liệu lên kiểu đấy nó kiểu xếp hình kiểm tra có

<a id="S00249"></a>
**[00:14:51 → 00:14:57] [Người nói?]** phải tấn công không Nếu như đúng thì nó sẽ làm dầu cái đồng đề lên này bằng những cái câu lệnh đã bị

<a id="S00250"></a>
**[00:14:57 → 00:15:03] [Người nói?]** bị chặn có có có dấu hiệu có khả năng bị chặn thì mục tiêu của họ chỉ đơn giản là có rất ít dữ liệu

<a id="S00251"></a>
**[00:15:03 → 00:15:09] [Người nói?]** giờ làm nào mà học thật kỳ cái đồng dữ liệu đấy kiểu học học về đây thì đấy là phương pháp cũ thì

<a id="S00252"></a>
**[00:15:09 → 00:15:15] [Người nói?]** chủ đích của bọn nó là khiến cho mô hình kiểu những cái công ty nào mà nghèo nghèo mà không có khả năng

<a id="S00253"></a>
**[00:15:15 → 00:15:23] [Người nói?]** thuê các cái tường lửa xị hoặc là các cái chức năng xị thì sẽ phải dùng cách đấy thì em vẫn dùng

<a id="S00254"></a>
**[00:15:24 → 00:15:30] [Người nói?]** [ASR cần nghe lại] Vâng thì bởi vì là các cái công ty đấy phải sử dụng tương lựa đều bằng phương pháp SMOTE

<a id="S00255"></a>
**[00:15:30 → 00:15:40] [Người nói?]** [ASR cần nghe lại] Thì em đề xuất là thêm, vẫn dùng SMOTE nhưng mà kẹp thêm cái câu lệnh của em vào để có thể là đảm bảo là có thể học hết tất cả các cái

<a id="S00256"></a>
**[00:15:41 → 00:15:43] [Người nói?]** [ASR cần nghe lại] Nhầm cái thuật toán của em

<a id="S00257"></a>
**[00:15:46 → 00:15:53] [Người nói?]** [ASR cần nghe lại] Nó sẽ kẹp song song với thằng SMOTE, một thằng là học tủ, một thằng là học những cái tấn công nó đặc biệt hơn

<a id="S00258"></a>
**[00:15:53 → 00:15:56] [Người nói?]** Bởi vì thường là kể cả là đưa khoảng

<a id="S00259"></a>
**[00:15:56 → 00:15:57] [Người nói?]** Đặc biệt hơn chỗ nào

<a id="S00260"></a>
**[00:15:59 → 00:16:00] [Người nói?]** Ví dụ như

<a id="S00261"></a>
**[00:16:00 → 00:16:01] [Người nói?]** Có nghĩa là nó tự sinh ra

<a id="S00262"></a>
**[00:16:01 → 00:16:02] [Người nói?]** Vâng, những cái câu

<a id="S00263"></a>
**[00:16:02 → 00:16:06] [Người nói?]** [nghe không rõ 00:16:02; cần đối chiếu] Ví dụ như mà một câu khai thác mà trên 200 ký tự

<a id="S00264"></a>
**[00:16:06 → 00:16:09] [Người nói?]** [nghe không rõ 00:16:06; cần đối chiếu] Nằm giữa những câu khai thác mà từ tầm 60-70 ký tự

<a id="S00265"></a>
**[00:16:09 → 00:16:11] [Người nói?]** [nghe không rõ 00:16:09; cần đối chiếu] Thì những câu 200 ký tự sẽ bị loại ngay lập tức

<a id="S00266"></a>
**[00:16:11 → 00:16:15] [Người nói?]** Bởi vì nó quá dài và nó quá đặc biệt so với những câu bình thường

<a id="S00267"></a>
**[00:16:16 → 00:16:19] [Người nói?]** Thì bây giờ là em sẽ cố gắng học mấy cái câu mà có cái

<a id="S00268"></a>
**[00:16:20 → 00:16:21] [Người nói?]** Kiểu thông số khác biệt như thế

<a id="S00269"></a>
**[00:16:21 → 00:16:27] [Người nói?]** [nghe không rõ 00:16:21; cần đối chiếu] Thì trong mô hình mà ở trên cargo hoặc là các cái bộ dữ liệu công khai

<a id="S00270"></a>
**[00:16:28 → 00:16:31] [Người nói?]** [nghe không rõ 00:16:28; cần đối chiếu] Thì những cái bộ dữ liệu đấy nó rơi vào khoảng tầm 10% thôi

<a id="S00271"></a>
**[00:16:31 → 00:16:34] [Người nói?]** Nhưng mà thường là vừa vào phát là nó sẽ bị loại ngay lập tức

<a id="S00272"></a>
**[00:16:34 → 00:16:39] [Người nói?]** Bởi vì nó quá là kiểu nhọn, nó kiểu một mũi nhọn ý

<a id="S00273"></a>
**[00:16:39 → 00:16:40] [Người nói?]** Học cái đấy nó không được tác dụng gì mà

<a id="S00274"></a>
**[00:16:42 → 00:16:45] [Người nói?]** Người ta chỉ quan tâm là kiểu chung chung để đảm bảo là

<a id="S00275"></a>
**[00:16:45 → 00:16:48] [Người nói?]** Ít nhất là chặn có thể chặn tối đa không phải chặn cái mẫu như thế

<a id="S00276"></a>
**[00:16:48 → 00:16:52] [Người nói?]** Thế bây giờ mày muốn hỏi ta là bình thường ta sẽ dùng cái gì?

<a id="S00277"></a>
**[00:16:52 → 00:16:56] [Người nói?]** Nghĩa là em cũng nhận thấy là kiểu cái này nó hơi bánh vẽ

<a id="S00278"></a>
**[00:16:56 → 00:17:01] [Người nói?]** Vì thực tế là cũng tường lửa bây giờ là cũng rất tiên tiến

<a id="S00279"></a>
**[00:17:01 → 00:17:03] [Người nói?]** [nghe không rõ 00:17:01; cần đối chiếu] Và cũng chặn gần như là 99% rồi

<a id="S00280"></a>
**[00:17:03 → 00:17:06] [Người nói?]** Cùng lắm là sẽ phải là mình tự custom

<a id="S00281"></a>
**[00:17:06 → 00:17:08] [Người nói?]** Nghĩa là anh phải chủ động kiểu khai thác

<a id="S00282"></a>
**[00:17:08 → 00:17:10] [Người nói?]** Khai thác dần khai thác dần rồi bắt đầu hiểu là

<a id="S00283"></a>
**[00:17:10 → 00:17:13] [Người nói?]** Đằng sau mô hình nó như thế nào và có khả năng lô hổng là gì

<a id="S00284"></a>
**[00:17:13 → 00:17:16] [Người nói?]** Thì lúc đấy mới cần nêm kiểu con người vào

<a id="S00285"></a>
**[00:17:16 → 00:17:18] [Người nói?]** Thì lúc đấy mới biết là mô hình sẽ bị làm sao

<a id="S00286"></a>
**[00:17:18 → 00:17:21] [Người nói?]** Chứ không thể là ném mấy cái đống tech này vào được

<a id="S00287"></a>
**[00:17:22 → 00:17:25] [Người nói?]** mong là một cái thành công thì thực tế là nó không còn nữa rồi

<a id="S00288"></a>
**[00:17:25 → 00:17:29] [Người nói?]** thì bây giờ là biến từ mõm thành thực tế rồi anh

<a id="S00289"></a>
**[00:17:29 → 00:17:32] [Người nói?]** còn lúc lúc làm là em cũng thấy

<a id="S00290"></a>
**[00:17:32 → 00:17:36] [Người nói?]** cũng thấy là nó hơi lý thuyết rồi

<a id="S00291"></a>
**[00:17:36 → 00:17:39] [Người nói?]** thì bây giờ là có hai cái

<a id="S00292"></a>
**[00:17:39 → 00:17:43] [Người nói?]** thì như vần cái câu nhất thì anh cũng trả rồi là

<a id="S00293"></a>
**[00:17:43 → 00:17:44] [Người nói?]** cái của em là nói về thực tế

<a id="S00294"></a>
**[00:17:44 → 00:17:48] [Người nói?]** giờ em đang muốn hiểu là nếu anh dùng AI để hỗ trợ

<a id="S00295"></a>
**[00:17:48 → 00:17:49] [Người nói?]** cho việc khai thác tấn công

<a id="S00296"></a>
**[00:17:49 → 00:17:52] [Người nói?]** thì anh sẽ sử dụng như thế nào vậy anh

<a id="S00297"></a>
**[00:17:53 → 00:17:59] [Người nói?]** Chứ không thể là kiểu chỉ sinh rồi ném hết tất cả vào để xem mô hình xem thằng nào vượt thì dùng

<a id="S00298"></a>
**[00:17:59 → 00:18:00] [Người nói?]** Em nghĩ thế nó...

<a id="S00299"></a>
**[00:18:00 → 00:18:02] [Người nói?]** AI giờ nó dùng như con người

<a id="S00300"></a>
**[00:18:02 → 00:18:09] [Người nói?]** Có nghĩa là nó tìm một cái phần trăm như bình thường mà mày bảo nó check hành vi đấy

<a id="S00301"></a>
**[00:18:09 → 00:18:14] [Người nói?]** Chỉ check nó sẽ check như thế nào ấy

<a id="S00302"></a>
**[00:18:14 → 00:18:16] [Người nói?]** À thử không cô đề sai quá

<a id="S00303"></a>
**[00:18:16 → 00:18:17] [Người nói?]** Ví dụ nha

<a id="S00304"></a>
**[00:18:17 → 00:18:18] [Người nói?]** Vâng

<a id="S00305"></a>
**[00:18:18 → 00:18:22] [Người nói?]** Ví dụ nó chặn nhưng mà nó chặn thiếu đi

<a id="S00306"></a>
**[00:18:27 → 00:18:28] [Người nói?]** Vâng

<a id="S00307"></a>
**[00:18:28 → 00:18:32] [Người nói?]** Các ký tự đặc biệt chẳng hạn, có hiểu không?

<a id="S00308"></a>
**[00:18:32 → 00:18:35] [Người nói?]** Có, cái câu SELECT mà anh nói đúng không anh?

<a id="S00309"></a>
**[00:18:35 → 00:18:37] [Người nói?]** Ờ, cái ký tự đặc biệt này là gì?

<a id="S00310"></a>
**[00:18:38 → 00:18:42] [Người nói?]** Ký tự đặc biệt thì là kiểu các ký tự encoder kiểu phần trăm hai mươi hoặc là

<a id="S00311"></a>
**[00:18:43 → 00:18:47] [Người nói?]** Các ký tự kiểu để ẩn cái câu lệnh truy vấn thật đi anh

<a id="S00312"></a>
**[00:18:47 → 00:18:53] [Người nói?]** Ờ, ký tự đặc biệt, ví dụ encode hoặc là hack đi chẳng hạn đúng không?

<a id="S00313"></a>
**[00:18:53 → 00:18:53] [Người nói?]** Vâng

<a id="S00314"></a>
**[00:18:53 → 00:18:59] [Người nói?]** Thì nó xem là cái web đấy nó chặn những cái gì, nó sẽ thử từng cái một

<a id="S00315"></a>
**[00:18:59 → 00:19:05] [Người nói?]** bây giờ nó sẽ thử select bị chặn đúng không ạ

<a id="S00316"></a>
**[00:19:06 → 00:19:13] [Người nói?]** thì nó thử select, nó thử tất cả những cái gì mà để nó phân tích hành vi

<a id="S00317"></a>
**[00:19:13 → 00:19:18] [Người nói?]** để nó biết được tại vì mình black box mà mình đâu có biết là suộc nó như thế nào

<a id="S00318"></a>
**[00:19:18 → 00:19:26] [Người nói?]** chứ nếu mà biết suộc với cả con watt nó chặn cái gì thì nó không phải thử đúng không ạ

<a id="S00319"></a>
**[00:19:26 → 00:19:30] [Người nói?]** bây giờ nó sẽ những cái payload có sẵn rồi

<a id="S00320"></a>
**[00:19:31 → 00:19:34] [Người nói?]** sql thì nó cũng hiểu là cái db đây sử dụng thế nào rồi

<a id="S00321"></a>
**[00:19:35 → 00:19:44] [Người nói?]** thì nó làm như con người nó tìm một cái phần trăm đấy, không chẳng được gì.

<a id="S00322"></a>
**[00:19:45 → 00:19:51] [Người nói?]** Nhưng mà thế nghĩa là, nghĩa là cái của em là về mặt lý thuyết là vẫn khả thi,

<a id="S00323"></a>
**[00:19:51 → 00:19:57] [Người nói?]** nghĩa là kiểu tạo ra hơn hàng trăm hàng nghìn câu lệnh, và đạo sử cái bộ kia nó không có.

## Dữ liệu sinh được đưa vào đâu

<a id="S00324"></a>
**[00:19:57 → 00:19:59] [Người nói?]** Cái đấy nó, mày đút vào đâu? Tao đang hỏi là cái

<a id="S00325"></a>
**[00:20:00 → 00:20:02] [Người nói?]** hàng trăm hàng nghìn câu lệnh của mày nó đút vào đâu ấy?

<a id="S00326"></a>
**[00:20:02 → 00:20:06] [Người nói?]** Đút qua website kiểu tấn công website mạng chứ anh

<a id="S00327"></a>
**[00:20:08 → 00:20:10] [Người nói?]** Mày đang là phía ngăn chặn cơ mà

<a id="S00328"></a>
**[00:20:11 → 00:20:15] [Người nói?]** Không thì bây giờ là cái tấn công của em phải có tác dụng thì mới đưa vào trong bộ dữ liệu chứ anh

<a id="S00329"></a>
**[00:20:15 → 00:20:18] [Người nói?]** Thế bây giờ nếu mà kiểu chỉ đơn giản là

<a id="S00330"></a>
**[00:20:18 → 00:20:20] [Người nói?]** À cái thằng đéo hiểu

<a id="S00331"></a>
**[00:20:20 → 00:20:23] [Người nói?]** Thế bây giờ mày đã chứng minh nó có hiệu nghiệm đâu

<a id="S00332"></a>
**[00:20:23 → 00:20:24] [Người nói?]** Tao đang nói ở cái này thôi

<a id="S00333"></a>
**[00:20:24 → 00:20:25] [Người nói?]** Vâng

<a id="S00334"></a>
**[00:20:26 → 00:20:28] [Người nói?]** Thì bây giờ là em đang

<a id="S00335"></a>
**[00:20:36 → 00:20:49] [Người nói?]** bây giờ là cái này là nó chỉ chứng minh là cái xinh này hơn cái bình thường thì ta đang hỏi là

<a id="S00336"></a>
**[00:20:49 → 00:20:57] [Người nói?]** cái xinh này này nó sinh ra xong nó nhét vào đâu sinh ra xong nhét vào cơ sở kiểu bộ dữ liệu tấn

<a id="S00337"></a>
**[00:20:57 → 00:21:03] [Người nói?]** [ASR cần nghe lại] bộ dữ liệu tấn công anh để bộ dữ liệu tấn công lưu ở cái gì lưu hiện tại thì là sẽ nghĩa là dùng

<a id="S00338"></a>
**[00:21:03 → 00:21:08] [Người nói?]** [ASR cần nghe lại] con học máy nó lại học lại cái đồng đấy để nhận biết các cái học máy là máy chặn bằng ai à học

<a id="S00339"></a>
**[00:21:08 → 00:21:14] [Người nói?]** [ASR cần nghe lại] máy không nghĩa là chạy bằng thuật toán của ai không phải chạy bằng ai ai nó sẽ dùng một vài

<a id="S00340"></a>
**[00:21:14 → 00:21:24] [Người nói?]** [nghe không rõ 00:21:14; cần đối chiếu] thuật toán để nó học mấy cái này còn cái mẹ thằng này hiểu câu hỏi rồi có nghĩa là nha anh quát đúng

<a id="S00341"></a>
**[00:21:24 → 00:21:27] [Người nói?]** nó phải dựa vào những cái câu lệnh đấy

<a id="S00342"></a>
**[00:21:27 → 00:21:30] [Người nói?]** và khi thằng người dùng truyền cái câu lệnh đấy vào

<a id="S00343"></a>
**[00:21:31 → 00:21:35] [Người nói?]** nó sẽ phải lấy cái data từ những cái câu lệnh mà nó đã có sẵn rồi

<a id="S00344"></a>
**[00:21:35 → 00:21:38] [Người nói?]** nó check với cả câu lệnh thằng người dùng nó truyền vào

<a id="S00345"></a>
**[00:21:38 → 00:21:42] [Người nói?]** xem có đạt điểm bao nhiêu điểm không

<a id="S00346"></a>
**[00:21:42 → 00:21:48] [Người nói?]** [nghe không rõ 00:21:42; cần đối chiếu] ví dụ nó dính 5 điểm là bị cảnh báo hoặc là dính 3 điểm thì nó không bị cảnh báo

<a id="S00347"></a>
**[00:21:48 → 00:21:52] [Người nói?]** ví dụ thế, ngày xưa tao học web là nó sẽ là như thế

<a id="S00348"></a>
**[00:21:52 → 00:21:56] [Người nói?]** có nghĩa là nó sẽ tính điểm xem câu lệnh này có điểm nó có bị nguy hiểm không

<a id="S00349"></a>
**[00:21:56 → 00:21:59] [Người nói?]** ví dụ thế nhá

<a id="S00350"></a>
**[00:21:59 → 00:22:03] [Người nói?]** thì cái số lượng cái câu đấy

<a id="S00351"></a>
**[00:22:03 → 00:22:04] [Người nói?]** nó phải lưu vào một cái chỗ nào đấy

<a id="S00352"></a>
**[00:22:06 → 00:22:08] [Người nói?]** để khi mà lúc nó đánh giá

<a id="S00353"></a>
**[00:22:08 → 00:22:10] [Người nói?]** thì nó có cái cơ sở để nó đánh giá câu lệnh

<a id="S00354"></a>
**[00:22:10 → 00:22:11] [Người nói?]** chuyển vào

<a id="S00355"></a>
**[00:22:12 → 00:22:14] [Người nói?]** thế thì mẹ ta hỏi cái này mày sinh ra

<a id="S00356"></a>
**[00:22:14 → 00:22:15] [Người nói?]** mày đút vào đâu

<a id="S00357"></a>
**[00:22:15 → 00:22:17] [Người nói?]** [nghe không rõ 00:22:15; cần đối chiếu] em không đút vào cái của thằng WAP

<a id="S00358"></a>
**[00:22:17 → 00:22:19] [Người nói?]** mà đút vào cái bộ

<a id="S00359"></a>
**[00:22:19 → 00:22:21] [Người nói?]** mà thằng AI sẽ dùng để nó học lên

<a id="S00360"></a>
**[00:22:21 → 00:22:23] [Người nói?]** bố mình hiểu rồi

<a id="S00361"></a>
**[00:22:24 → 00:22:33] [Người nói?]** [ASR cần nghe lại] Cũng nghĩa là sẽ có hai cái, một là thằng tường lửa nó chặn theo kì, hai là thằng AI là nó chặn thì là nó cứ, nó giống kiểu thằng Cloud ấy anh.

<a id="S00362"></a>
**[00:22:33 → 00:22:34] [Người nói?]** [ASR cần nghe lại] Thằng AI nó chặn cái gì?

<a id="S00363"></a>
**[00:22:35 → 00:22:35] [Người nói?]** [ASR cần nghe lại] Vâng anh.

<a id="S00364"></a>
**[00:22:35 → 00:22:40] [Người nói?]** [ASR cần nghe lại] Mẹ tao bảo thằng AI nó chặn từ nãy rồi, cứ bộ sinh bộ sinh cái lồn gì, đéo hiểu quá.

<a id="S00365"></a>
**[00:22:40 → 00:22:50] [Người nói?]** [nghe không rõ 00:22:40; cần đối chiếu] Có nghĩa là khi mày vào thì sẽ có một con AI nó chặn, bây giờ mày đang dùng AI để chặn, quay loát với những thằng ở ngoài.

<a id="S00366"></a>
**[00:22:50 → 00:22:50] [Người nói?]** [ASR cần nghe lại] Rồi.

<a id="S00367"></a>
**[00:22:51 → 00:22:51] [Người nói?]** [ASR cần nghe lại] Đúng chưa?

<a id="S00368"></a>
**[00:22:51 → 00:22:52] [Người nói?]** [ASR cần nghe lại] Đúng anh, vâng.

<a id="S00369"></a>
**[00:22:54 → 00:23:00] [Người nói?]** đấy có nghĩa là mày cứ thằng ở ngoài nó cứ cho vào bao nhiêu câu lệnh

<a id="S00370"></a>
**[00:23:00 → 00:23:04] [Người nói?]** xong là nó tự trộn trong đấy lên, nó tự suy luận, nó tự học

<a id="S00371"></a>
**[00:23:04 → 00:23:08] [Người nói?]** để nó biết là khi thằng kia nó chuyển những câu lệnh như thế nào vào thì nó chặn cái đấy gì

<a id="S00372"></a>
**[00:23:09 → 00:23:11] [Người nói?]** thì những thằng khác là nó chưa dùng AI

<a id="S00373"></a>
**[00:23:13 → 00:23:15] [Người nói?]** còn của mày hơn chúng nó là mày dùng AI cái gì

<a id="S00374"></a>
**[00:23:16 → 00:23:18] [Người nói?]** thì thế thôi

<a id="S00375"></a>
**[00:23:22 → 00:23:24] [Người nói?]** không, cho anh anh hiểu thế nó có gì hơn

<a id="S00376"></a>
**[00:23:26 → 00:23:27] [Người nói?]** cứ nãy giờ em nói thì tao anh tự

<a id="S00377"></a>
**[00:23:27 → 00:23:33] [Người nói?]** Thế bây giờ ý mày hỏi là bây giờ tao dùng AI để làm thế nào để tấn công con AI của máy hay gì?

<a id="S00378"></a>
**[00:23:34 → 00:23:36] [Người nói?]** Anh dùng AI trong công việc nó như thế nào vậy anh?

<a id="S00379"></a>
**[00:23:36 → 00:23:39] [Người nói?]** Công việc thì cứ bảo nó làm thôi

<a id="S00380"></a>
**[00:23:40 → 00:23:45] [Người nói?]** Nhưng mà nếu mà kiểu như thế thì vì anh có chuyện là anh là chuyên viên cộng cấp đấy anh

<a id="S00381"></a>
**[00:23:45 → 00:23:53] [Người nói?]** Nhưng mà ý là chính xác là cái luồng công việc riêng của anh ấy anh thì anh sẽ phải khai thác thế nào

<a id="S00382"></a>
**[00:23:54 → 00:23:58] [Người nói?]** Nếu không thì ai dùng AI nó cũng thành chuyên viên tấn công được

<a id="S00383"></a>
**[00:23:58 → 00:24:01] [Người nói?]** [ASR cần nghe lại] ta thấy ai dùng AI thành chuyên nghiệp chấm trộm được mà

<a id="S00384"></a>
**[00:24:01 → 00:24:04] [Người nói?]** [ASR cần nghe lại] không, nó còn phải kiểu dựa theo mindset với cả là

<a id="S00385"></a>
**[00:24:04 → 00:24:07] [Người nói?]** [ASR cần nghe lại] cái kinh nghiệm cá nhân của anh nữa chứ anh

<a id="S00386"></a>
**[00:24:07 → 00:24:12] [Người nói?]** [ASR cần nghe lại] thì mindset thì bây giờ nó vẫn là thử và sai thôi chứ có gì đâu

<a id="S00387"></a>
**[00:24:12 → 00:24:15] [Người nói?]** [ASR cần nghe lại] ví dụ bây giờ bảo tấn công SQL á

<a id="S00388"></a>
**[00:24:15 → 00:24:18] [Người nói?]** [ASR cần nghe lại] thì còn AI nó đã học tất cả các loại tấn công

<a id="S00389"></a>
**[00:24:18 → 00:24:21] [Người nói?]** [nghe không rõ 00:24:18; cần đối chiếu] các loại tấn quát các thứ có thể truyền lại được rồi

<a id="S00390"></a>
**[00:24:22 → 00:24:25] [Người nói?]** [ASR cần nghe lại] bây giờ nó thử hành vi thôi

<a id="S00391"></a>
**[00:24:26 → 00:24:29] [Người nói?]** [nghe không rõ 00:24:26; cần đối chiếu] hành vi của con quát xem nó có bypass được không

<a id="S00392"></a>
**[00:24:30 → 00:24:33] [Người nói?]** Còn cái web của máy chạm này thì con AI nó chỉ

<a id="S00393"></a>
**[00:24:34 → 00:24:39] [Người nói?]** Thế bây giờ mày muốn hỏi kiểu sử dụng AI như thế nào

<a id="S00394"></a>
**[00:24:40 → 00:24:45] [Người nói?]** Nó rộng, biết cái gì đó, dùng cái gì hay như nào

<a id="S00395"></a>
**[00:24:46 → 00:24:50] [Người nói?]** Thế nếu như mà không phải Blackbox thì rao nghĩa là anh kiểm thử từ bên trong nhé

<a id="S00396"></a>
**[00:24:50 → 00:24:55] [Người nói?]** Anh đã được biết rồi và lead ra các kiểu gần như mình đã biết trước đáp án rồi

<a id="S00397"></a>
**[00:24:55 → 00:24:58] [Người nói?]** Và bây giờ phải lead ra là mô hình tùy vào những vấn đề gì

<a id="S00398"></a>
**[00:24:58 → 00:25:05] [Người nói?]** Có biết con là trong môi trường bình thường hay là có môi trường AI của mày?

<a id="S00399"></a>
**[00:25:06 → 00:25:07] [Người nói?]** Môi trường công việc bình thường thôi anh

<a id="S00400"></a>
**[00:25:07 → 00:25:12] [Người nói?]** Nghĩa là ví dụ như là một công ty nó khá tự tin về khả năng bảo vệ của mình

<a id="S00401"></a>
**[00:25:12 → 00:25:16] [Người nói?]** Và thuê anh là coi như anh biết luôn cả mã nguồn

<a id="S00402"></a>
**[00:25:16 → 00:25:21] [Người nói?]** Để có thể phá thêm để đảm bảo là cái attack surface nó gần có thể, ít nhất có thể

<a id="S00403"></a>
**[00:25:23 → 00:25:29] [Người nói?]** Thì anh sẽ làm gì thì kiểu em nghĩ là lúc đấy là chỉ có những cái nó rất đặc thù thì mới có khả năng vượt qua

<a id="S00404"></a>
**[00:25:29 → 00:25:33] [Người nói?]** Đúng rồi, bây giờ mình đã có ví dụ mã nguồn đúng không?

<a id="S00405"></a>
**[00:25:33 → 00:25:34] [Người nói?]** Vâng

<a id="S00406"></a>
**[00:25:34 → 00:25:41] [Người nói?]** Thì bây giờ con AI nó sẽ phân tích là trong cái mã nguồn này nó sẽ có những payload nào bị dính, được chưa?

<a id="S00407"></a>
**[00:25:41 → 00:25:43] [Người nói?]** Rồi, phân tích rồi

<a id="S00408"></a>
**[00:25:43 → 00:25:44] [Người nói?]** Hiểu không?

<a id="S00409"></a>
**[00:25:44 → 00:25:44] [Người nói?]** Có

<a id="S00410"></a>
**[00:25:44 → 00:25:52] [Người nói?]** Có nghĩa là khi mà nó review cái mã nguồn đấy, nó sẽ phân tích ra được là những payload nào sẽ dính

<a id="S00411"></a>
**[00:25:52 → 00:25:53] [Người nói?]** Rồi

<a id="S00412"></a>
**[00:25:54 → 00:25:57] [Người nói?]** Nó ghen ra những payload đã dính được chưa?

<a id="S00413"></a>
**[00:25:57 → 00:26:05] [Người nói?]** [nghe không rõ 00:25:57; cần đối chiếu] và nếu ở ngoài nó có 1 con quáp nữa thì nó sẽ chế cháo cây loại đi theo các cách off circuit mà nó đã biết

<a id="S00414"></a>
**[00:26:05 → 00:26:07] [Người nói?]** [nghe không rõ 00:26:05; cần đối chiếu] chế cháo theo cách off circuit

<a id="S00415"></a>
**[00:26:08 → 00:26:10] [Người nói?]** em biết là cái đó làm ẩn

<a id="S00416"></a>
**[00:26:10 → 00:26:12] [Người nói?]** em đang làm theo hướng này đấy

<a id="S00417"></a>
**[00:26:13 → 00:26:21] [Người nói?]** nó ẩn những cái mà mình chế cháo đi để truyền vào và câu lệnh nó vẫn giữ nguyên không thay đổi

<a id="S00418"></a>
**[00:26:21 → 00:26:24] [Người nói?]** con ở trong nó vẫn hiểu được

<a id="S00419"></a>
**[00:26:24 → 00:26:26] [Người nói?]** [nghe không rõ 00:26:24; cần đối chiếu] và cái con quáp nó không hiểu

<a id="S00420"></a>
**[00:26:29 → 00:26:37] [Người nói?]** con AI mày làm xong ấy thì nó vẫn phải dựa vào một cái con gì đấy để nó bắt những cái đấy nó bắt

<a id="S00421"></a>
**[00:26:37 → 00:26:46] [Người nói?]** những cái mà mày gen ra hay là mày dùng công nghệ gì mà con AI nó bắt được luôn anh cứ hiểu là em

<a id="S00422"></a>
**[00:26:46 → 00:26:52] [Người nói?]** kiểu em có một cái câu lệnh và câu lệnh đấy sẽ đi qua con cloud trước để nó tự đánh giá nếu như mà

<a id="S00423"></a>
**[00:26:52 → 00:26:59] [Người nói?]** [nghe không rõ 00:26:52; cần đối chiếu] có nguy hiểm thì nó sẽ cho bỏ qua thì nếu nhưng mà nếu như câu lệnh này nó quá tinh vi thế thì ok

## Tốc độ xử lý và tính khả thi

<a id="S00424"></a>
**[00:26:59 → 00:27:05] [Người nói?]** [ASR cần nghe lại] Ok, nhưng mà làm sao để Cloud nó xử lý được dữ liệu như thế, ví dụ

<a id="S00425"></a>
**[00:27:05 → 00:27:09] [Người nói?]** [ASR cần nghe lại] Luộc, nghĩa là kiểu nhiều quá hay như thế nào

<a id="S00426"></a>
**[00:27:09 → 00:27:15] [Người nói?]** [ASR cần nghe lại] Ví dụ ta là một thằng hacker, nó bắn cả triệu request

<a id="S00427"></a>
**[00:27:16 → 00:27:16] [Người nói?]** [ASR cần nghe lại] Đúng rồi

<a id="S00428"></a>
**[00:27:16 → 00:27:18] [Người nói?]** [ASR cần nghe lại] Đúng chưa

<a id="S00429"></a>
**[00:27:18 → 00:27:24] [Người nói?]** [ASR cần nghe lại] Và cũng có hàng triệu thằng hacker khác, nó bắn cả triệu request

<a id="S00430"></a>
**[00:27:24 → 00:27:27] [Người nói?]** [ASR cần nghe lại] Thì làm sao thằng đấy nó nói được

<a id="S00431"></a>
**[00:27:27 → 00:27:32] [Người nói?]** [ASR cần nghe lại] Thế thì mình sẽ có những cái con AI nội bộ kiểu tự train từ đầu

<a id="S00432"></a>
**[00:27:32 → 00:27:34] [Người nói?]** [ASR cần nghe lại] Nghĩa là kiểu Cloud cho riêng mình

<a id="S00433"></a>
**[00:27:34 → 00:27:38] [Người nói?]** Tao đéo nói về cái vấn đề là con cloud nó xử lý được hay không

<a id="S00434"></a>
**[00:27:39 → 00:27:43] [Người nói?]** Mà là ví dụ cả khách hàng, cả người dùng

<a id="S00435"></a>
**[00:27:43 → 00:27:46] [Người nói?]** Như làm sao mà tất cả đều qua con cloud được

<a id="S00436"></a>
**[00:27:46 → 00:27:50] [Người nói?]** Ví dụ qua như thế thì cái tốc độ của website nó như thế nào

<a id="S00437"></a>
**[00:27:50 → 00:27:52] [Người nói?]** Rồi, hiểu

<a id="S00438"></a>
**[00:27:52 → 00:27:53] [Người nói?]** Hiểu không?

<a id="S00439"></a>
**[00:27:53 → 00:27:53] [Người nói?]** Vâng

<a id="S00440"></a>
**[00:27:53 → 00:27:57] [Người nói?]** Ví dụ như con tường nửa nhá

<a id="S00441"></a>
**[00:27:57 → 00:27:59] [Người nói?]** Con web này hà

<a id="S00442"></a>
**[00:27:59 → 00:28:04] [Người nói?]** Thì nó chỉ cần matching với cái gì đấy

<a id="S00443"></a>
**[00:28:04 → 00:28:07] [Người nói?]** Chỉ cần truyền câu lệnh vào matching với cái gì

<a id="S00444"></a>
**[00:28:07 → 00:28:15] [Người nói?]** thì là như kiểu là câu lệnh đến sớt luôn thì matching cái là nó loại nó sử lý rất nhanh thì

<a id="S00445"></a>
**[00:28:15 → 00:28:25] [Người nói?]** con ai mày xử lý là bao lâu một request hiểu không bao lâu một request thì nó sẽ hệ thống

<a id="S00446"></a>
**[00:28:25 → 00:28:34] [Người nói?]** vẫn hoạt động bình thường mà vẫn an toàn chứ nếu tất cả cho con AI thì nó sẽ bị vấn đề gì về lại

<a id="S00447"></a>
**[00:28:34 → 00:28:47] [Người nói?]** hỏi con AI xem xem nó có khả thi không còn giống bình thường luồng hoạt động thì mày muốn hỏi luồng

<a id="S00448"></a>
**[00:28:47 → 00:28:53] [Người nói?]** hoạt động về cái gì bây giờ mày bảo anh cứ dùng ai trong công việc như thế nào thì ai dùng nhiều cái

<a id="S00449"></a>
**[00:28:54 → 00:29:02] [Người nói?]** làm sao mà kể hết được em nghe nói anh mua luôn gói cao nhất mà chỉ có một mình mình dùng ấy thì

<a id="S00450"></a>
**[00:29:02 → 00:29:09] [Người nói?]** sao anh phải em tưởng là anh phải đầu tư lớn đấy anh phải làm gì nó cũng một lực lượng tên luôn ừ

<a id="S00451"></a>
**[00:29:09 → 00:29:18] [Người nói?]** [nghe không rõ 00:29:09; cần đối chiếu] bất quả ti thôi bất quả ti mà cũng dùng hết có dùng hết rồi mày hay là khiếu khiếu vẫn khiếu

<a id="S00452"></a>
**[00:29:18 → 00:29:29] [Người nói?]** [nghe không rõ 00:29:18; cần đối chiếu] ừ con đấy nhiều vậy nhiều nhưng vẫn không đủ bất kiểu gì mà hết được tận cái con 200

<a id="S00453"></a>
**[00:29:29 → 00:29:40] [Người nói?]** [nghe không rõ 00:29:29; cần đối chiếu] xe à 400 xe bây giờ mày làm một tay ghép thì mày có biết là nó làm những cái gì không ví dụ

<a id="S00454"></a>
**[00:29:42 → 00:29:52] [Người nói?]** nghĩa là phải làm như cái gì Ví dụ nếu mà mày tấn công thì lúc đấy là mình sẽ scan

<a id="S00455"></a>
**[00:29:52 → 00:29:59] [Người nói?]** in cách là đưa hàng loạt câu vào để xem là bằng tưởng em ít nhất là cũng nghĩa

<a id="S00456"></a>
**[00:30:00 → 00:30:05] [Người nói?]** Nghĩa là ý em là kiểu mình sẽ đưa vào rất nhiều câu lệnh thì ở mỗi câu lệnh nó sẽ trả về một cái

<a id="S00457"></a>
**[00:30:05 → 00:30:10] [Người nói?]** một cái dấu hiệu gì đó để mình bắt đầu suy luận ra xem là đằng sau nó sẽ hệ thống ở trong như nào

<a id="S00458"></a>
**[00:30:10 → 00:30:20] [Người nói?]** thế thì cái suy luận đấy thì nó dùng cái gì suy luận thì các cái dấu hiệu mình AI tổng hợp lại và mình

<a id="S00459"></a>
**[00:30:20 → 00:30:27] [Người nói?]** sẽ là người suy luận nó chỉ tổng hợp lại cái dấu hiệu thôi Đấy là cách mà em thấy là khả thi nhất

<a id="S00460"></a>
**[00:30:27 → 00:30:31] [Người nói?]** [ASR cần nghe lại] bởi vì AI nó thường nó không suy luận tốt về cái đấy

<a id="S00461"></a>
**[00:30:34 → 00:30:37] [Người nói?]** [ASR cần nghe lại] Nghĩa là nó sẽ suy luận theo kiểu ý tưởng số đông

<a id="S00462"></a>
**[00:30:37 → 00:30:39] [Người nói?]** [ASR cần nghe lại] nếu như số đông nó đúng từ đầu thì cái đấy sẽ đúng

<a id="S00463"></a>
**[00:30:42 → 00:30:44] [Người nói?]** [ASR cần nghe lại] AI bây giờ nó suy luận hết

<a id="S00464"></a>
**[00:30:44 → 00:30:47] [Người nói?]** [ASR cần nghe lại] Nhưng cái đấy là cái dùng token đấy

<a id="S00465"></a>
**[00:30:47 → 00:30:52] [Người nói?]** [ASR cần nghe lại] Bây giờ nó sẽ là như một thằng người bình thường

<a id="S00466"></a>
**[00:30:52 → 00:30:55] [Người nói?]** [ASR cần nghe lại] nhưng mà mình sẽ chuyển mindset của mình vào cho nó thôi

<a id="S00467"></a>
**[00:30:57 → 00:30:58] [Người nói?]** [ASR cần nghe lại] Hiểu không?

<a id="S00468"></a>
**[00:30:58 → 00:31:02] [Người nói?]** [ASR cần nghe lại] Có nghĩa là bây giờ ta đã biết là ví dụ

<a id="S00469"></a>
**[00:31:03 → 00:31:04] [Người nói?]** [ASR cần nghe lại] chỗ này là cái chỗ chuyển vào đúng không?

<a id="S00470"></a>
**[00:31:04 → 00:31:07] [Người nói?]** nó sẽ từ lì con ra cái chỗ đấy cho truyền vào

<a id="S00471"></a>
**[00:31:07 → 00:31:10] [Người nói?]** và tính khả thi của nó là truyền cái gì vào

<a id="S00472"></a>
**[00:31:10 → 00:31:13] [Người nói?]** truyền cái gì vào thì nó lại thử

<a id="S00473"></a>
**[00:31:13 → 00:31:16] [Người nói?]** nó sẽ thử và nó sẽ tự suy đoạn tiếp

<a id="S00474"></a>
**[00:31:17 → 00:31:19] [Người nói?]** chỗ này truyền nó bị sao

<a id="S00475"></a>
**[00:31:20 → 00:31:24] [Người nói?]** thế những cái đấy thì những cái suy nghĩ của nó tốn tốc cân đấy

<a id="S00476"></a>
**[00:31:27 → 00:31:27] [Người nói?]** hiểu không

<a id="S00477"></a>
**[00:31:28 → 00:31:30] [Người nói?]** và lượng kiến thức của nó nhiều

<a id="S00478"></a>
**[00:31:31 → 00:31:33] [Người nói?]** con AI nó sẽ cover hết lượng kiến thức

<a id="S00479"></a>
**[00:31:36 → 00:31:37] [Người nói?]** mình chỉ hiểu luôn thôi

<a id="S00480"></a>
**[00:31:37 → 00:31:43] [Người nói?]** còn lại là nó sẽ làm hết

<a id="S00481"></a>
**[00:31:43 → 00:31:48] [Người nói?]** Còn cái hỗ trợ của mày thì tao thấy là

<a id="S00482"></a>
**[00:31:51 → 00:31:51] [Người nói?]** Nghề

<a id="S00483"></a>
**[00:31:52 → 00:31:54] [Người nói?]** Nếu mà có một con AI ở ngoài

<a id="S00484"></a>
**[00:31:54 → 00:31:55] [Người nói?]** Mà dùng được vào trong

<a id="S00485"></a>
**[00:31:55 → 00:31:57] [Người nói?]** Cái web này thì đúng là

<a id="S00486"></a>
**[00:31:57 → 00:31:58] [Người nói?]** Nó ok

<a id="S00487"></a>
**[00:31:58 → 00:32:01] [Người nói?]** Nếu mà mày dùng AI để chạm thì đề tài ok

<a id="S00488"></a>
**[00:32:04 → 00:32:05] [Người nói?]** Dùng AI chứ không phải dùng

<a id="S00489"></a>
**[00:32:05 → 00:32:06] [Người nói?]** Thuật toán nhá

<a id="S00490"></a>
**[00:32:07 → 00:32:08] [Người nói?]** Thuật toán ý

<a id="S00491"></a>
**[00:32:08 → 00:32:10] [Người nói?]** Thuật toán thì cũng không có gì kỳ quốc

<a id="S00492"></a>
**[00:32:11 → 00:32:13] [Người nói?]** Đúng rồi, dùng thuật toán ý

<a id="S00493"></a>
**[00:32:13 → 00:32:14] [Người nói?]** Thì mày sinh ra những cái gì đúng không

<a id="S00494"></a>
**[00:32:15 → 00:32:15] [Người nói?]** Sinh ra

<a id="S00495"></a>
**[00:32:15 → 00:32:21] [Người nói?]** sinh ra nhưng mà nó cũng chỉ sinh ra gọi là những cái ký vuốt đấy thôi xong là con quá vẫn phải làm

<a id="S00496"></a>
**[00:32:21 → 00:32:37] [Người nói?]** nhiệm vụ con quá hiểu chưa Còn con ai nó không làm gì nó chỉ học thôi hiểu chưa đây nhé mày bảo

<a id="S00497"></a>
**[00:32:37 → 00:32:49] [Người nói?]** là cái gì cho xin dữ liệu không sinh ra dữ liệu đi vào đâu tao vừa hỏi mày đấy sinh dữ liệu thì

<a id="S00498"></a>
**[00:32:49 → 00:32:55] [Người nói?]** [nghe không rõ 00:32:49; cần đối chiếu] vẫn phải đẩy vào cái chỗ con quát để con quát khi mà mình mình truyền cái gì vào thì con quát

<a id="S00499"></a>
**[00:32:55 → 00:33:02] [Người nói?]** nó nhận thấy những cái dữ liệu tấn công thì nó mới ngăn chặn hiểu chưa thì đây là máy vẫn là dùng con

<a id="S00500"></a>
**[00:33:02 → 00:33:12] [Người nói?]** [nghe không rõ 00:33:02; cần đối chiếu] WAP thôi chứ mà chưa dùng AI khi dùng AI là nó phải suy luận suy luận trên từng câu tấn công này

<a id="S00501"></a>
**[00:33:12 → 00:33:13] [Người nói?]** [ASR cần nghe lại] Vâng ạ

<a id="S00502"></a>
**[00:33:13 → 00:33:14] [Người nói?]** [ASR cần nghe lại] Nhưng mà...

<a id="S00503"></a>
**[00:33:14 → 00:33:17] [Người nói?]** [ASR cần nghe lại] Thôi thì để em tự tìm hiểu

<a id="S00504"></a>
**[00:33:17 → 00:33:21] [Người nói?]** [ASR cần nghe lại] Con web thì nó cũng đã detect gần như hết đánh án rồi

<a id="S00505"></a>
**[00:33:24 → 00:33:24] [Người nói?]** [ASR cần nghe lại] Hiểu không?

<a id="S00506"></a>
**[00:33:24 → 00:33:27] [Người nói?]** [ASR cần nghe lại] Mày làm nào mà thiết kế cho con AI nó suy loạn ấy

<a id="S00507"></a>
**[00:33:28 → 00:33:29] [Người nói?]** [ASR cần nghe lại] Thì cái đấy ok

<a id="S00508"></a>
**[00:33:29 → 00:33:30] [Người nói?]** [ASR cần nghe lại] Cái đề tài đấy tao thấy được

<a id="S00509"></a>
**[00:33:32 → 00:33:33] [Người nói?]** [ASR cần nghe lại] Hiểu không?

<a id="S00510"></a>
**[00:33:33 → 00:33:36] [Người nói?]** [ASR cần nghe lại] Chứ còn nếu mà sinh mô hình tấn công

<a id="S00511"></a>
**[00:33:36 → 00:33:37] [Người nói?]** [ASR cần nghe lại] Mô hình tấn công này

<a id="S00512"></a>
**[00:33:37 → 00:33:41] [Người nói?]** [ASR cần nghe lại] Con AI ở ngoài thì nó cũng sinh mô hình tấn công mẹ thôi

<a id="S00513"></a>
**[00:33:42 → 00:33:44] [Người nói?]** [ASR cần nghe lại] Cần gì phải làm đề án

<a id="S00514"></a>
**[00:33:44 → 00:33:45] [Người nói?]** [ASR cần nghe lại] Cần gì phải viết báo

<a id="S00515"></a>
**[00:33:45 → 00:33:49] [Người nói?]** Biết báo là phải những thằng chuyên lạc bây giờ

<a id="S00516"></a>
**[00:33:50 → 00:33:57] [Người nói?]** Có nghĩa là sử dụng AI phân tích được mấy thằng kia nó như vào nhưng mà nó phải nhanh

<a id="S00517"></a>
**[00:33:57 → 00:34:00] [Người nói?]** Dùng một module bé thôi của con AI

<a id="S00518"></a>
**[00:34:00 → 00:34:04] [Người nói?]** Có nghĩa là một con AI nó sẽ phân tích nhiều thứ

<a id="S00519"></a>
**[00:34:04 → 00:34:07] [Người nói?]** Phải phân tích nhiều thứ hoặc đây chỉ cho nó phân tích SQL thôi

<a id="S00520"></a>
**[00:34:09 → 00:34:15] [Người nói?]** [nghe không rõ 00:34:09; cần đối chiếu] Và một câu lệnh truyền vào tối ưu cho nó là sử lý trong 0.001 giây thôi

<a id="S00521"></a>
**[00:34:15 → 00:34:20] [Người nói?]** [nghe không rõ 00:34:15; cần đối chiếu] Ví dụ thế thì nó sử lý một nghìn request chỉ trong một giây

<a id="S00522"></a>
**[00:34:20 → 00:34:24] [Người nói?]** [nghe không rõ 00:34:20; cần đối chiếu] 1 triệu request, kiểu 10 giây là nó xử lý xong

<a id="S00523"></a>
**[00:34:24 → 00:34:26] [Người nói?]** có nghĩa là hệ thống không ảnh hưởng gì quá lớn

<a id="S00524"></a>
**[00:34:26 → 00:34:27] [Người nói?]** ví dụ thế đúng không

<a id="S00525"></a>
**[00:34:28 → 00:34:29] [Người nói?]** đấy là ý tưởng

<a id="S00526"></a>
**[00:34:29 → 00:34:34] [Người nói?]** [nghe không rõ 00:34:29; cần đối chiếu] còn cái sinh này thì nó vẫn dựa vào con quát của nó bắt này

<a id="S00527"></a>
**[00:34:34 → 00:34:36] [Người nói?]** tại vì mày sinh ra những cái dữ liệu

<a id="S00528"></a>
**[00:34:36 → 00:34:37] [Người nói?]** nó mới hơn, đúng không

<a id="S00529"></a>
**[00:34:38 → 00:34:39] [Người nói?]** sinh ra dữ liệu mới hơn

<a id="S00530"></a>
**[00:34:39 → 00:34:42] [Người nói?]** [nghe không rõ 00:34:39; cần đối chiếu] và những con quát trước và hệ thống chung chung

<a id="S00531"></a>
**[00:34:42 → 00:34:47] [Người nói?]** chưa có, thì có nghĩa là bây giờ

<a id="S00532"></a>
**[00:34:48 → 00:34:49] [Người nói?]** cái này

<a id="S00533"></a>
**[00:34:49 → 00:34:51] [Người nói?]** mày vứt cho con cloud

<a id="S00534"></a>
**[00:34:51 → 00:34:54] [Người nói?]** một cái file tầm khoảng 100.000

<a id="S00535"></a>
**[00:34:54 → 00:34:55] [Người nói?]** cái payload

<a id="S00536"></a>
**[00:34:55 → 00:35:04] [Người nói?]** [nghe không rõ 00:34:55; cần đối chiếu] Bảo là sinh như tao dữ liệu ra là con AI tự sinh, con cơ lao tự sinh, 5 phút là xong.

<a id="S00537"></a>
**[00:35:05 → 00:35:06] [Người nói?]** Cả cái đề án của mày luôn.

<a id="S00538"></a>
**[00:35:06 → 00:35:15] [Người nói?]** Cơ lao bây giờ nó mạnh, nó hãy chứa làm gì được tích hợp với một cái mức gì đấy của nó.

<a id="S00539"></a>
**[00:35:16 → 00:35:21] [Người nói?]** Nó học, xong rồi nó sinh ra kiểu gì mà nó chặn được.

<a id="S00540"></a>
**[00:35:21 → 00:35:25] [Người nói?]** Sử lý, vấn đề sử lý nó nhanh và nó vẫn thông minh.

<a id="S00541"></a>
**[00:35:27 → 00:35:30] [Người nói?]** Còn cái này là vẫn theo kỳ, ta thấy là vẫn theo kỳ.

<a id="S00542"></a>
**[00:35:30 → 00:35:35] [Người nói?]** [nghe không rõ 00:35:30; cần đối chiếu] Mày vứt vào trong con warp để nó tự... gọi là cái gì nhỉ?

<a id="S00543"></a>
**[00:35:36 → 00:35:37] [Người nói?]** Tự detect cái gì?

<a id="S00544"></a>
**[00:35:38 → 00:35:38] [Người nói?]** Rue set

<a id="S00545"></a>
**[00:35:38 → 00:35:40] [Người nói?]** Rue set bao nhiêu phần trăm thôi

<a id="S00546"></a>
**[00:35:40 → 00:35:43] [Người nói?]** [nghe không rõ 00:35:40; cần đối chiếu] Một khác gì nó vẫn dùng con warp đâu

<a id="S00547"></a>
**[00:35:43 → 00:35:48] [Người nói?]** Chứ con AI nó có nghĩ cái đoạn set đi đâu

<a id="S00548"></a>
**[00:35:48 → 00:35:49] [Người nói?]** Hiểu không?

## Hướng ứng dụng và các giả định còn tranh luận

<a id="S00549"></a>
**[00:35:51 → 00:35:53] [Người nói?]** Đấy bây giờ hướng tương lai của mày muốn làm gì?

<a id="S00550"></a>
**[00:35:54 → 00:35:55] [Người nói?]** Vậy là...

<a id="S00551"></a>
**[00:35:55 → 00:35:56] [Người nói?]** Vẫn là con này thôi

<a id="S00552"></a>
**[00:35:56 → 00:35:57] [Người nói?]** Vâng, nhưng mà...

<a id="S00553"></a>
**[00:35:58 → 00:36:00] [Người nói?]** [nghe không rõ 00:35:58; cần đối chiếu] Cả warp, sau khi mà vượt qua được warp

<a id="S00554"></a>
**[00:36:00 → 00:36:02] [Người nói?]** Chỗ này của em thì mới đến con AI mà anh

<a id="S00555"></a>
**[00:36:02 → 00:36:03] [Người nói?]** Chẳng thích thường em

<a id="S00556"></a>
**[00:36:03 → 00:36:09] [Người nói?]** Thế bây giờ cái hướng lớn nhất thì mày cứ làm theo ý của mày ban đầu thì có nghĩa là

<a id="S00557"></a>
**[00:36:09 → 00:36:14] [Người nói?]** Khi mà con này sinh ra thì nó chặn đến những cái mà con bình thường cũng có chặn được

<a id="S00558"></a>
**[00:36:14 → 00:36:16] [Người nói?]** Thế là được

<a id="S00559"></a>
**[00:36:16 → 00:36:19] [Người nói?]** Thế thôi mày lấy một cái Google Public rồi mày ghi vào

<a id="S00560"></a>
**[00:36:23 → 00:36:24] [Người nói?]** Và gọi là

<a id="S00561"></a>
**[00:36:24 → 00:36:30] [Người nói?]** Có nghĩa là khi mà thằng khác nó cho những cái câu lệnh mới vào

<a id="S00562"></a>
**[00:36:30 → 00:36:31] [Người nói?]** Thì con này nó sẽ tự học được đúng không ạ?

<a id="S00563"></a>
**[00:36:32 → 00:36:33] [Người nói?]** Đúng rồi

<a id="S00564"></a>
**[00:36:33 → 00:36:39] [Người nói?]** Nó hơn cái là nó phải tự học được chứ không cần thằng người dùng nó gì nữa

<a id="S00565"></a>
**[00:36:39 → 00:36:41] [Người nói?]** Thằng người dùng nó loại

<a id="S00566"></a>
**[00:36:42 → 00:36:45] [Người nói?]** Nó phải tự nhận biết xem có phải đáng để đưa vào không

<a id="S00567"></a>
**[00:36:45 → 00:36:50] [Người nói?]** Đúng như thế thì nó sẽ là ưu việt hơn thì nó đúng

<a id="S00568"></a>
**[00:36:50 → 00:36:53] [Người nói?]** Có nghĩa là những thằng bình thường là nó sẽ phải bị tấn công

<a id="S00569"></a>
**[00:36:55 → 00:36:57] [Người nói?]** Nó bị tấn công rồi thì nó mới biết

<a id="S00570"></a>
**[00:36:57 → 00:37:03] [Người nói?]** Có nghĩa là nó bị tấn công rồi thì nó mới xét cái đu là nếu mà gặp cái này thì phải chặn cho tao đúng không

<a id="S00571"></a>
**[00:37:03 → 00:37:09] [Người nói?]** nhưng mà dùng con của em thì chưa cần bị tấn công

<a id="S00572"></a>
**[00:37:09 → 00:37:11] [Người nói?]** có nguy cơ bị tấn công

<a id="S00573"></a>
**[00:37:11 → 00:37:16] [Người nói?]** nó nhìn ra như thế là nó đã tự biết là nó sinh ra như thế để nó chặn cho em đồ

<a id="S00574"></a>
**[00:37:16 → 00:37:19] [Người nói?]** đó, thế là cái tính thực tế và ưu việt hơn của nó

<a id="S00575"></a>
**[00:37:21 → 00:37:22] [Người nói?]** ok chưa?

<a id="S00576"></a>
**[00:37:22 → 00:37:24] [Người nói?]** ok, vâng, không hiểu

<a id="S00577"></a>
**[00:37:24 → 00:37:33] [Người nói?]** không biết người ta, người ta đang không biết là cái hôm này nói với thầy

<a id="S00578"></a>
**[00:37:37 → 00:37:44] [Người nói?]** [ASR cần nghe lại] Nói về thầy đi. Đấy chỉ chứng minh là cái thằng thuật toán của em nó hơn rồi các thuật toán thông thường ở đây.

<a id="S00579"></a>
**[00:37:45 → 00:37:51] [Người nói?]** [ASR cần nghe lại] Các thuật toán thông thường thì đánh vào kinh phí vì cái phương pháp kia nó nhanh gọn, nó không phải quá tổ kỳ.

<a id="S00580"></a>
**[00:37:51 → 00:37:56] [Người nói?]** [ASR cần nghe lại] Cần một file Python khoảng mấy MB là nó chạy được rồi.

<a id="S00581"></a>
**[00:37:56 → 00:38:03] [Người nói?]** [nghe không rõ 00:37:56; cần đối chiếu] Cái của em thì phải sinh ra một cái con mô đun nhỏ, nó tầm khoảng một ghi, nó sẽ xử lý những cái nâng cao hơn.

<a id="S00582"></a>
**[00:38:04 → 00:38:11] [Người nói?]** [nghe không rõ 00:38:04; cần đối chiếu] Thì là em có thuyết trình là chỉ cần 2 con kết hợp lại thì có thể bao quát được rộng hơn nữa thôi

<a id="S00583"></a>
**[00:38:12 → 00:38:15] [Người nói?]** Thì chỗ đấy là đủ để đố thạc sĩ hả anh?

<a id="S00584"></a>
**[00:38:15 → 00:38:20] [Người nói?]** Có nghĩa là hôm thuyết trình thì mà cái thuyết trình là gọi là thuyết trình

<a id="S00585"></a>
**[00:38:22 → 00:38:28] [Người nói?]** [nghe không rõ 00:38:22; cần đối chiếu] Là sẽ có 1 con quát bình thường và 1 phát Python chứa các cái ru

<a id="S00586"></a>
**[00:38:31 → 00:38:32] [Người nói?]** Ru thì không đủ

<a id="S00587"></a>
**[00:38:33 → 00:38:42] [Người nói?]** [ASR cần nghe lại] dữ không đủ dữ liệu dữ liệu các cái ru cộng đồng cũng chưa đủ chưa đủ báo khoát thì phải kẹt thêm

<a id="S00588"></a>
**[00:38:42 → 00:38:49] [Người nói?]** [ASR cần nghe lại] là sẽ phải sinh ra dữ liệu tấn công nhé mình bị tấn công rồi nó sẽ có cái dữ liệu đấy và bình thường là

<a id="S00589"></a>
**[00:38:49 → 00:38:57] [Người nói?]** [ASR cần nghe lại] sẽ sử dụng cái phương pháp của em để kiểu nhân bản nó lên để khiến cho cái lượng dữ liệu này nó nó dày

<a id="S00590"></a>
**[00:38:57 → 00:39:02] [Người nói?]** [nghe không rõ 00:38:57; cần đối chiếu] thì lúc đấy là Sengaru Set nó bao quát cái đồng đấy

<a id="S00591"></a>
**[00:39:02 → 00:39:05] [Người nói?]** [ASR cần nghe lại] nhưng mà set có những cái mẫu là kể cả có làm nhiều lên

<a id="S00592"></a>
**[00:39:05 → 00:39:09] [Người nói?]** [ASR cần nghe lại] bởi vì nó quá phức tạp, kiểu số lượng ký tự quá dài

<a id="S00593"></a>
**[00:39:09 → 00:39:12] [Người nói?]** [ASR cần nghe lại] thì là mô hình thường nó sẽ chủ động chặn để học nó

<a id="S00594"></a>
**[00:39:13 → 00:39:15] [Người nói?]** [nghe không rõ 00:39:13; cần đối chiếu] chỉ học những cái mà nó bao quát thôi

<a id="S00595"></a>
**[00:39:16 → 00:39:19] [Người nói?]** [ASR cần nghe lại] thì giờ sẽ là những cái mẫu đấy sẽ đưa qua con của em

<a id="S00596"></a>
**[00:39:19 → 00:39:23] [Người nói?]** [ASR cần nghe lại] để đảm bảo là thằng học không không thằng nào bị bỏ hết

<a id="S00597"></a>
**[00:39:23 → 00:39:28] [Người nói?]** [ASR cần nghe lại] đấy là hướng, gần như là hướng

<a id="S00598"></a>
**[00:39:28 → 00:39:31] [Người nói?]** Bởi vì là đoạn sau cũng vấn đề nhưng mà đấy là hướng của em

<a id="S00599"></a>
**[00:39:31 → 00:39:36] [Người nói?]** Thì em có thuyết trình thì có thể đấy là ý tưởng cũng hợp lệ cho bác

<a id="S00600"></a>
**[00:39:40 → 00:39:43] [Người nói?]** Thì bây giờ là muốn viết báo thì phải biến cái đống ý tưởng này

<a id="S00601"></a>
**[00:39:44 → 00:39:48] [Người nói?]** Thành ý nhất là phải có thực tế và phải đăng lên trên mạng để kiểm chứng

<a id="S00602"></a>
**[00:39:48 → 00:39:50] [Người nói?]** Thế nên là em nghĩ

<a id="S00603"></a>
**[00:39:50 → 00:39:51] [Người nói?]** Thực tế đi, thực tế đi

<a id="S00604"></a>
**[00:39:53 → 00:39:57] [Người nói?]** Thì lúc mà em làm em thấy cũng hơi bị bánh vẽ rồi

<a id="S00605"></a>
**[00:39:57 → 00:40:00] [Người nói?]** nên là hôm nay cần phải gặp anh để

<a id="S00606"></a>
**[00:40:00 → 00:40:04] [Người nói?]** biết là thực tế nhiều đề tài em là so với anh thì anh nghe nào

<a id="S00607"></a>
**[00:40:05 → 00:40:10] [Người nói?]** biết là hướng cần phải làm lại nếu mà làm cách cũ thì khả năng là trượt hơi cao

## Hiểu luồng WAF, SQL và học qua lab

<a id="S00608"></a>
**[00:40:13 → 00:40:17] [Người nói?]** nói chung mày làm thế nào để, nói chung mày thì hiểu

<a id="S00609"></a>
**[00:40:19 → 00:40:24] [Người nói?]** [nghe không rõ 00:40:19; cần đối chiếu] tự nhiên là mày sẽ hiểu cái cách mà con quát nó hoạt động như thế nào

<a id="S00610"></a>
**[00:40:24 → 00:40:27] [Người nói?]** bình thường nó chặn như thế nào và mày tối ưu nó là cái gì

<a id="S00611"></a>
**[00:40:29 → 00:40:36] [Người nói?]** [nghe không rõ 00:40:29; cần đối chiếu] có hiểu con quát nó chặn như nào không em nó chặn theo ký quất kiểu hoặc là bộ ru từ trước nó đưa vào

<a id="S00612"></a>
**[00:40:36 → 00:40:43] [Người nói?]** [ASR cần nghe lại] rồi tôi biết là nó chặn như thế rồi chặn ký quất nhưng mà mình phải hiểu là nó xử lý nó như thế nào

<a id="S00613"></a>
**[00:40:44 → 00:40:55] [Người nói?]** [ASR cần nghe lại] để mình nhét con ai ai vào để nó xử lý để nó khác đéo ai cho biết nó chặn theo những từ hay là những

<a id="S00614"></a>
**[00:40:55 → 00:41:07] [Người nói?]** [nghe không rõ 00:40:55; cần đối chiếu] Như câu lận như thế nào đấy, nguy hiểm như thế nào, nhưng mà nó chẳng như thế nào là cái cách hoạt động ấy, cái cách hoạt động của cái quát nó như thế nào ấy, thì mày phải biết là cái luồng nó như thế nào.

<a id="S00615"></a>
**[00:41:08 → 00:41:09] [Người nói?]** Mày có kể được không?

<a id="S00616"></a>
**[00:41:10 → 00:41:11] [Người nói?]** Không.

<a id="S00617"></a>
**[00:41:12 → 00:41:22] [Người nói?]** [nghe không rõ 00:41:12; cần đối chiếu] Thế thì mày phải hiểu đi đã, mày phải hiểu con quát nó hoạt động như thế nào, mày phải hiểu được nó như thế nào thì mày mới tối ưu và cải tiến hơn được chứ.

<a id="S00618"></a>
**[00:41:23 → 00:41:24] [Người nói?]** Đó, đúng rồi.

<a id="S00619"></a>
**[00:41:24 → 00:41:25] [Người nói?]** Đó, thế đó.

<a id="S00620"></a>
**[00:41:36 → 00:41:42] [Người nói?]** Thế nếu như bây giờ thì bình thường là code select nó chặn. Nhưng bây giờ là mình off UK

<a id="S00621"></a>
**[00:41:42 → 00:41:47] [Người nói?]** cái code select đấy đi kiểu em ví dụ vậy thì nó sẽ là một cụm dài dặn dặn ra nữa. Thì bây giờ

<a id="S00622"></a>
**[00:41:47 → 00:41:53] [Người nói?]** bây giờ em sẽ cố gắng là bê cái cụm ấy chặn luôn cái cụm như thế thì có khả thiêu

<a id="S00623"></a>
**[00:41:56 → 00:42:03] [Người nói?]** nghĩa là nghĩa là bây giờ là có một câu select thì câu select rất là dài thì nó thấy chữ select nó chặn

<a id="S00624"></a>
**[00:42:03 → 00:42:09] [Người nói?]** nhưng mà mình obfuscate có thể là hack nó lên chẳng hạn thì từ câu select cầm khoảng 6 ký

<a id="S00625"></a>
**[00:42:09 → 00:42:16] [Người nói?]** dự đấy thì nó biến thành một cụm rất là dài các câu được hack thì có thể là tương lửa nó bỏ qua cái này

<a id="S00626"></a>
**[00:42:16 → 00:42:19] [Người nói?]** Thì em sẽ cố gắng là bê nguyên cái cụm đấy vào

<a id="S00627"></a>
**[00:42:20 → 00:42:21] [Người nói?]** Thấy là chọn

<a id="S00628"></a>
**[00:42:23 → 00:42:25] [Người nói?]** Ví dụ là

<a id="S00629"></a>
**[00:42:28 → 00:42:29] [Người nói?]** Cái hack đấy làm sao

<a id="S00630"></a>
**[00:42:29 → 00:42:30] [Người nói?]** Con ở trong nó hiểu được

<a id="S00631"></a>
**[00:42:31 → 00:42:32] [Người nói?]** Hiểu không

<a id="S00632"></a>
**[00:42:33 → 00:42:36] [Người nói?]** Cái server của mày làm sao tự nhiên cái hack đó

<a id="S00633"></a>
**[00:42:37 → 00:42:38] [Người nói?]** [nghe không rõ 00:42:37; cần đối chiếu] Để nó off-cache

<a id="S00634"></a>
**[00:42:41 → 00:42:41] [Người nói?]** Con DB

<a id="S00635"></a>
**[00:42:42 → 00:42:43] [Người nói?]** Sao nó hiểu hack

<a id="S00636"></a>
**[00:42:43 → 00:42:45] [Người nói?]** Câu select thì

<a id="S00637"></a>
**[00:42:46 → 00:42:48] [Người nói?]** Tao nghĩ là chả chuyển được cái gì đó

<a id="S00638"></a>
**[00:42:50 → 00:42:50] [Người nói?]** Select là select

<a id="S00639"></a>
**[00:42:50 → 00:42:52] [Người nói?]** [nghe không rõ 00:42:50; cần đối chiếu] không hiểu mình có phụ kết được gì hết

<a id="S00640"></a>
**[00:42:55 → 00:43:01] [Người nói?]** [nghe không rõ 00:42:55; cần đối chiếu] Nó chỉ có phụ kết được thành các chữ S

<a id="S00641"></a>
**[00:43:01 → 00:43:03] [Người nói?]** [ASR cần nghe lại] xong rồi nó cách cách ngay cách

<a id="S00642"></a>
**[00:43:03 → 00:43:06] [Người nói?]** [ASR cần nghe lại] xong sao thăng gì đấy

<a id="S00643"></a>
**[00:43:06 → 00:43:08] [Người nói?]** [ASR cần nghe lại] xong chữ L

<a id="S00644"></a>
**[00:43:09 → 00:43:10] [Người nói?]** [ASR cần nghe lại] xong các thứ

<a id="S00645"></a>
**[00:43:10 → 00:43:11] [Người nói?]** [ASR cần nghe lại] đúng như nó tách ra

<a id="S00646"></a>
**[00:43:12 → 00:43:16] [Người nói?]** [ASR cần nghe lại] hoặc là hệ thống của mày nó hiểu một cái character gì đấy

<a id="S00647"></a>
**[00:43:16 → 00:43:18] [Người nói?]** [ASR cần nghe lại] nó hiểu ký tự cha

<a id="S00648"></a>
**[00:43:18 → 00:43:21] [Người nói?]** [ASR cần nghe lại] nó tự chuyển đổi từ con server sang

<a id="S00649"></a>
**[00:43:21 → 00:43:54] [Người nói?]** [nghe không rõ 00:43:21; cần đối chiếu] Mày cũng hiểu con server nó làm cái gì, cây của nó là gì, thì mấy dí vào được là nó off-focus bằng cách nào, hiểu SQL nữa, nó làm cái gì, làm đề tài của SQL, không biết SQL, không biết ấy thì làm sao mà dìu bằng.

<a id="S00650"></a>
**[00:43:54 → 00:44:06] [Người nói?]** [nghe không rõ 00:43:54; cần đối chiếu] Như thế này mới sẽ nói nguyên cơ chứ chẳng có ít được quay được

<a id="S00651"></a>
**[00:44:07 → 00:44:08] [Người nói?]** Hôm nay...

<a id="S00652"></a>
**[00:44:08 → 00:44:10] [Người nói?]** Mày về tìm hiểu lại đi đã

<a id="S00653"></a>
**[00:44:10 → 00:44:13] [Người nói?]** Tìm hiểu xong bác vào đoạn cái nào nhé

<a id="S00654"></a>
**[00:44:13 → 00:44:13] [Người nói?]** Rồi

<a id="S00655"></a>
**[00:44:13 → 00:44:15] [Người nói?]** Rồi xong SQL là gì

<a id="S00656"></a>
**[00:44:16 → 00:44:21] [Người nói?]** [nghe không rõ 00:44:16; cần đối chiếu] Thực thi tại sao cái ốc phụ kết lấy mà ghi lại với câu hỏi thứ 3

<a id="S00657"></a>
**[00:44:23 → 00:44:26] [Người nói?]** Rồi hôm sau mày sẽ gặp một buổi khác

<a id="S00658"></a>
**[00:44:26 → 00:44:31] [Người nói?]** Nếu mày đang chưa hiểu một cái gì về SQL thì làm sao mà có thể tìm hiểu

<a id="S00659"></a>
**[00:44:44 → 00:44:57] [Người nói?]** [nghe không rõ 00:44:44; cần đối chiếu] anh em nói lại anh nói lại không cách quá phải đẹp hạt động với từng quay đoát này nhá

<a id="S00660"></a>
**[00:45:18 → 00:45:39] [Người nói?]** [nghe không rõ 00:45:18; cần đối chiếu] Các bạn hãy đăng ký kênh để ủng hộ kênh của mình nhé.

<a id="S00661"></a>
**[00:45:47 → 00:45:50] [Người nói?]** Có, nhưng mà chỉ hiểu đúng 4 dạng cơ bản, đấy thôi.

<a id="S00662"></a>
**[00:45:54 → 00:45:57] [Người nói?]** Tưởng còn mấy dạng kiểu con con thôi.

<a id="S00663"></a>
**[00:46:09 → 00:46:16] [Người nói?]** [nghe không rõ 00:46:09; cần đối chiếu] Aaron là cố gắng sinh ra các cái thông báo lỗi để xem là mô hình nó đang bị lỗ họng ở đâu.

<a id="S00664"></a>
**[00:46:16 → 00:46:17] [Người nói?]** Time thì sẽ là

<a id="S00665"></a>
**[00:46:17 → 00:46:18] [Người nói?]** Được

<a id="S00666"></a>
**[00:46:20 → 00:46:21] [Người nói?]** [nghe không rõ 00:46:20; cần đối chiếu] Erot Bay đúng không?

<a id="S00667"></a>
**[00:46:21 → 00:46:22] [Người nói?]** Vâng, đúng rồi

<a id="S00668"></a>
**[00:46:23 → 00:46:25] [Người nói?]** [nghe không rõ 00:46:23; cần đối chiếu] Erot Bay thì nó sinh ra

<a id="S00669"></a>
**[00:46:25 → 00:46:27] [Người nói?]** [nghe không rõ 00:46:25; cần đối chiếu] Cái Erot thì sao?

<a id="S00670"></a>
**[00:46:27 → 00:46:30] [Người nói?]** [nghe không rõ 00:46:27; cần đối chiếu] Sao FQL nó phai thác bằng kiểu gì?

<a id="S00671"></a>
**[00:46:30 → 00:46:32] [Người nói?]** Thì khi mà mình cố tình

<a id="S00672"></a>
**[00:46:32 → 00:46:34] [Người nói?]** Chuyển lỗi vào thì mô hình nó sẽ phải

<a id="S00673"></a>
**[00:46:34 → 00:46:36] [Người nói?]** Hiển thị một cái dấu hiệu gì đó

<a id="S00674"></a>
**[00:46:37 → 00:46:38] [Người nói?]** Và nếu như mà

<a id="S00675"></a>
**[00:46:38 → 00:46:40] [Người nói?]** Nó hiển thị, nó bị hiện ra ngoài

<a id="S00676"></a>
**[00:46:40 → 00:46:41] [Người nói?]** Một cái dấu hiệu mà mình có thể nhận ra

<a id="S00677"></a>
**[00:46:41 → 00:46:44] [Người nói?]** Thì mình có thể suy đoạn là có khả năng

<a id="S00678"></a>
**[00:46:44 → 00:46:46] [Người nói?]** Là nó đã không pass được

<a id="S00679"></a>
**[00:46:46 → 00:46:47] [Người nói?]** Được cái đấy và bị lộ ra thôi

<a id="S00680"></a>
**[00:46:52 → 00:46:53] [Người nói?]** Lộ dấu hiệu

<a id="S00681"></a>
**[00:46:54 → 00:46:56] [Người nói?]** Lộ dấu hiệu thì khai thác kiểu gì

<a id="S00682"></a>
**[00:47:00 → 00:47:02] [Người nói?]** [nghe không rõ 00:47:00; cần đối chiếu] E-Route Bay

<a id="S00683"></a>
**[00:47:02 → 00:47:03] [Người nói?]** Khai thác kiểu gì

<a id="S00684"></a>
**[00:47:03 → 00:47:05] [Người nói?]** Từng loại đấy khai thác kiểu gì

<a id="S00685"></a>
**[00:47:10 → 00:47:12] [Người nói?]** [nghe không rõ 00:47:10; cần đối chiếu] SVL thì từng loại khai thác này

<a id="S00686"></a>
**[00:47:12 → 00:47:14] [Người nói?]** Từng loại khai thác đấy nó khai thác như thế nào

<a id="S00687"></a>
**[00:47:14 → 00:47:16] [Người nói?]** Mày phải hiểu cách nó hoạt động

<a id="S00688"></a>
**[00:47:16 → 00:47:18] [Người nói?]** Mày mới chặn được

<a id="S00689"></a>
**[00:47:18 → 00:47:19] [Người nói?]** Mày không hiểu cách hoạt động

<a id="S00690"></a>
**[00:47:19 → 00:47:20] [Người nói?]** Mày mới chặn được gì

<a id="S00691"></a>
**[00:47:25 → 00:47:26] [Người nói?]** Thêm là tại sao

<a id="S00692"></a>
**[00:47:26 → 00:47:38] [Người nói?]** [nghe không rõ 00:47:26; cần đối chiếu] tìm kiếm sao cái phụ kết đấy Tại sao cái phụ kết đấy nó lại bài bát được ví dụ nó chặn câu lệnh

<a id="S00693"></a>
**[00:47:38 → 00:47:58] [Người nói?]** [nghe không rõ 00:47:38; cần đối chiếu] bình thường không Tại sao phụ kết thì nó lại vào được nó không cháy được chưa rồi đó xong lúc đấy

<a id="S00694"></a>
**[00:47:58 → 00:48:03] [Người nói?]** bây giờ mình đã hiểu hết được nguồn của những cái đấy nó hoạt động rồi bắt đầu mình nhắc cho

<a id="S00695"></a>
**[00:48:03 → 00:48:11] [Người nói?]** con ai của mày là con ai của mày nhét vào đoạn nào thì tùy thuộc đúng không rồi cái gan của mày

<a id="S00696"></a>
**[00:48:12 → 00:48:20] [Người nói?]** nhét vào đâu được rồi tao vẫn chưa thấy mày giải thích gì kiểu nó xinh chỗ nào nó ấy ở đâu

<a id="S00697"></a>
**[00:48:20 → 00:48:34] [Người nói?]** vâng hôm nay em biết là nhiều cái phải làm rõ kiểu mô hình của thằng này chả hiểu gì đây là toàn

<a id="S00698"></a>
**[00:48:35 → 00:48:41] [Người nói?]** Vâng, cái của em là thiên về thuật toán trước, còn bây giờ mới là lúc mà thiên về thực tế.

<a id="S00699"></a>
**[00:48:44 → 00:48:49] [Người nói?]** Để tại thạc sĩ chỉ cần đề xuất một ý tưởng thôi anh, bao nhiêu là vẫn đi độ rồi.

<a id="S00700"></a>
**[00:48:57 → 00:49:04] [Người nói?]** Thế là sau hôm qua nói chuyện với anh Minh là anh Minh cũng nghĩ lại thôi, không học thạc sĩ, an toàn, làm quản lý còn hơn.

<a id="S00701"></a>
**[00:49:11 → 00:49:15] [Người nói?]** Tổng quan của SPL đây, phân ngoại, không phải phân công đâu.

<a id="S00702"></a>
**[00:49:27 → 00:49:28] [Người nói?]** yêu cầu mới của bộ

<a id="S00703"></a>
**[00:49:28 → 00:49:58] [Người nói?]** nó thì biết nhưng mà nếu mà hỏi xem là nó bypass mà khai thác ở đây thì không

<a id="S00704"></a>
**[00:49:58 → 00:49:59] [Người nói?]** [ASR cần nghe lại] nó hoạt động

<a id="S00705"></a>
**[00:50:00 → 00:50:10] [Người nói?]** mình sẽ dùng o, o thì sẽ gồm một câu lệnh luôn đúng ở phía trước và o sẽ là câu lệnh mình khai thác

<a id="S00706"></a>
**[00:50:10 → 00:50:14] [Người nói?]** mình sẽ cố gắng nhét cái câu lệnh đấy thông qua cái toán tử đấy đấy

<a id="S00707"></a>
**[00:50:16 → 00:50:22] [Người nói?]** để có thể chuyển câu lệnh khai thác của mình vào do là ở trong o thì chuyển một về đúng

<a id="S00708"></a>
**[00:50:22 → 00:50:24] [Người nói?]** thì nó sẽ thực hiện với còn lại

<a id="S00709"></a>
**[00:50:27 → 00:50:36] [Người nói?]** [ASR cần nghe lại] thì chỉ hiểu là Boolean chỉ đơn giản là đưa một câu lệnh khai thác vào câu toán tử để có thể ép nó khai thác

<a id="S00710"></a>
**[00:50:36 → 00:50:37] [Người nói?]** [ASR cần nghe lại] Khai thác cái gì?

<a id="S00711"></a>
**[00:50:41 → 00:50:46] [Người nói?]** [ASR cần nghe lại] Có thể khai thác kiểu dữ liệu bảng hoặc là có những user nào ấy

<a id="S00712"></a>
**[00:50:46 → 00:50:50] [Người nói?]** [ASR cần nghe lại] Ừ, thì nó khai thác như thế nào? Giải thích như thế nào?

<a id="S00713"></a>
**[00:50:51 → 00:50:57] [Người nói?]** Mình sẽ đưa những câu lệnh truy vấn mà quyền của mình không đủ và đưa vào thông qua các cái toán từ đấy.

<a id="S00714"></a>
**[00:51:00 → 00:51:01] [Người nói?]** Quyền không đủ thì sao?

<a id="S00715"></a>
**[00:51:01 → 00:51:06] [Người nói?]** Em đang chờ ý thư của anh đi nào.

<a id="S00716"></a>
**[00:51:06 → 00:51:09] [Người nói?]** Đi, xem có khai thác được gì.

<a id="S00717"></a>
**[00:51:09 → 00:51:10] [Người nói?]** Về làm lab ngay.

<a id="S00718"></a>
**[00:51:11 → 00:51:13] [Người nói?]** [nghe không rõ 00:51:11; cần đối chiếu] Về làm lab ngay xem FVL khai thác được gì.

<a id="S00719"></a>
**[00:51:13 → 00:51:23] [Người nói?]** không hiểu mấy cái bài kiểu mấy cái láp trên mạng nhiều lắm

<a id="S00720"></a>
**[00:51:23 → 00:51:34] [Người nói?]** [nghe không rõ 00:51:23; cần đối chiếu] kiểu kép bm, bwap, không hiểu trong khách mạng kiểu gì

<a id="S00721"></a>
**[00:51:34 → 00:51:43] [Người nói?]** ví dụ như kiểu là cái no này đúng không

<a id="S00722"></a>
**[00:51:43 → 00:51:51] [Người nói?]** đúng không có nghĩa là ví dụ mày có một câu truy vấn đằng trước là đúng nó hiểu câu truy vấn đằng

<a id="S00723"></a>
**[00:51:51 → 00:52:00] [Người nói?]** trước đấy nó ở đâu không đúng thì chỉ cần kiểu toán tử một bằng một là nó đã coi như là luôn đúng rồi

<a id="S00724"></a>
**[00:52:00 → 00:52:08] [Người nói?]** để làm cái lần đấy hiểu ạ để nghĩa là lệnh o chỉ cần một trong hai cái đúng là nó sẽ thực thi ạ

<a id="S00725"></a>
**[00:52:08 → 00:52:18] [Người nói?]** vâng đúng rồi em chưa hiểu câu hỏi của anh có nghĩa là bây giờ mày dùng cái n o ở trong khai thác đúng

<a id="S00726"></a>
**[00:52:18 → 00:52:24] [Người nói?]** Đúng rồi, nghe bảo là có một câu đằng trước và phần khái hạng đằng sau

<a id="S00727"></a>
**[00:52:24 → 00:52:24] [Người nói?]** Ừ

<a id="S00728"></a>
**[00:52:26 → 00:52:29] [Người nói?]** Thì nếu như mà câu đằng trước đúng, nghĩa là cái toán tử O đúng

<a id="S00729"></a>
**[00:52:29 → 00:52:32] [Người nói?]** Thì sẽ thực hiện cái câu lệnh tấn công của mình

<a id="S00730"></a>
**[00:52:32 → 00:52:35] [Người nói?]** Câu đằng trước lúc đéo là cho đúng, biết tại sao không?

<a id="S00731"></a>
**[00:52:35 → 00:52:42] [Người nói?]** Do toán tử, nhưng mà ý em là chưa ý thức được là

<a id="S00732"></a>
**[00:52:42 → 00:52:43] [Người nói?]** Toán tử cái gì trời ơi

<a id="S00733"></a>
**[00:52:43 → 00:52:46] [Người nói?]** O là chỉ cần một trong hai vệt đúng anh

<a id="S00734"></a>
**[00:52:46 → 00:52:49] [Người nói?]** Cái bế đằng trước nó sai kiểu gì?

<a id="S00735"></a>
**[00:52:49 → 00:52:54] [Người nói?]** Hôm nay có đang hiểu cấu trúc của câu truy vấn không?

<a id="S00736"></a>
**[00:52:54 → 00:52:57] [Người nói?]** Hôm nay đéo hiểu cấu trúc của câu truy vấn

<a id="S00737"></a>
**[00:52:57 → 00:52:58] [Người nói?]** Em mới về tìm hiểu ký ức

<a id="S00738"></a>
**[00:53:01 → 00:53:03] [Người nói?]** Nghĩa là khi mà mày input vào đâu đấy

<a id="S00739"></a>
**[00:53:04 → 00:53:08] [Người nói?]** Mày sẽ có như kiểu là

<a id="S00740"></a>
**[00:53:08 → 00:53:09] [Người nói?]** Select A

<a id="S00741"></a>
**[00:53:10 → 00:53:12] [Người nói?]** Bằng mở ngoặc nhận đầu vào

<a id="S00742"></a>
**[00:53:12 → 00:53:13] [Người nói?]** Là của mình

<a id="S00743"></a>
**[00:53:13 → 00:53:15] [Người nói?]** Hiểu không

<a id="S00744"></a>
**[00:53:21 → 00:53:23] [Người nói?]** Mày không nghĩ là

<a id="S00745"></a>
**[00:53:23 → 00:53:25] [Người nói?]** Nói em bị hổng đến nước nhiều thế

<a id="S00746"></a>
**[00:53:25 → 00:53:27] [Người nói?]** Mày không biết cái gì đâu mà hổng

<a id="S00747"></a>
**[00:53:27 → 00:53:28] [Người nói?]** Mày hổng hết

<a id="S00748"></a>
**[00:53:31 → 00:53:33] [Người nói?]** Mày đang béo hiểu câu truy vấn này

<a id="S00749"></a>
**[00:53:33 → 00:53:34] [Người nói?]** Mày đang chưa biết

<a id="S00750"></a>
**[00:53:34 → 00:53:36] [Người nói?]** [nghe không rõ 00:53:34; cần đối chiếu] STL là cái gì

<a id="S00751"></a>
**[00:53:37 → 00:53:40] [Người nói?]** Mày đang bị hỏng cái này á, hỏng cái này rất nặng

<a id="S00752"></a>
**[00:53:41 → 00:53:42] [Người nói?]** Mày không hiểu chứ vẫn là gì

<a id="S00753"></a>
**[00:53:42 → 00:53:47] [Người nói?]** Ví dụ mày select

<a id="S00754"></a>
**[00:53:48 → 00:53:49] [Người nói?]** select name

<a id="S00755"></a>
**[00:53:50 → 00:53:51] [Người nói?]** rồi

<a id="S00756"></a>
**[00:53:52 → 00:53:54] [Người nói?]** form từ đâu đấy đúng không?

<a id="S00757"></a>
**[00:53:54 → 00:53:54] [Người nói?]** vâng

<a id="S00758"></a>
**[00:53:55 → 00:53:56] [Người nói?]** [nghe không rõ 00:53:55; cần đối chiếu] từ một cái đảng á

<a id="S00759"></a>
**[00:53:57 → 00:54:04] [Người nói?]** xong là mày sẽ so sánh cái select đấy

<a id="S00760"></a>
**[00:54:04 → 00:54:07] [Người nói?]** bằng một cái tên gì đấy mà mày chuyển vào

<a id="S00761"></a>
**[00:54:07 → 00:54:13] [Người nói?]** thì cái câu select ở đằng trước ấy

<a id="S00762"></a>
**[00:54:13 → 00:54:17] [Người nói?]** cái câu select đằng trước mà tao bảo

<a id="S00763"></a>
**[00:54:17 → 00:54:19] [Người nói?]** xong là có một cái tên chuyển vào đằng sau này này

<a id="S00764"></a>
**[00:54:19 → 00:54:26] [Người nói?]** [nghe không rõ 00:54:19; cần đối chiếu] Câu truy vấn này, câu truy vấn đằng trước này là câu truy vấn của hệ thống, là của những thằng cốt, hiểu chưa?

<a id="S00765"></a>
**[00:54:27 → 00:54:31] [Người nói?]** [nghe không rõ 00:54:27; cần đối chiếu] Nên lúc nào nó cũng đúng hết, mình chỉ chuyển vào cái đằng sau thôi.

<a id="S00766"></a>
**[00:54:33 → 00:54:36] [Người nói?]** Chuyển vào đằng sau để sử dụng, khai thác câu lệnh hệ thống này?

<a id="S00767"></a>
**[00:54:38 → 00:54:38] [Người nói?]** Vâng.

<a id="S00768"></a>
**[00:54:39 → 00:54:46] [Người nói?]** Rồi. Không, cái đấy em không cho em hiểu kỹ lưỡi về xem.

<a id="S00769"></a>
**[00:54:46 → 00:54:50] [Người nói?]** Em chưa hiểu cấu trúc của câu truy vấn về học, cấu trúc của câu truy vấn học.

<a id="S00770"></a>
**[00:54:50 → 00:54:56] [Người nói?]** [nghe không rõ 00:54:50; cần đối chiếu] học hiểu cái này hiểu cái quát thì mày mới bắt đầu làm cái này

<a id="S00771"></a>
**[00:54:56 → 00:55:01] [Người nói?]** mày chả hiểu gì mà hỏi tao, tao chán chả buồn mỏi, nói có hiểu gì đâu

<a id="S00772"></a>
**[00:55:02 → 00:55:11] [Người nói?]** [nghe không rõ 00:55:02; cần đối chiếu] đây, đề tài của mày tên là nghiên cứu mô hình gan cho sinh dữ liệu cẩn thận STL

<a id="S00773"></a>
**[00:55:11 → 00:55:18] [Người nói?]** [nghe không rõ 00:55:11; cần đối chiếu] thì phải hiểu STL, phải nâng cao phát triển dựa trên học máy đúng không?

<a id="S00774"></a>
**[00:55:18 → 00:55:31] [Người nói?]** Cái đề tài này là sử dụng mô hình gan

<a id="S00775"></a>
**[00:55:32 → 00:55:32] [Người nói?]** Ừ thì đúng

<a id="S00776"></a>
**[00:55:32 → 00:55:34] [Người nói?]** Mà nghiên cứu đúng mô hình gan thật

<a id="S00777"></a>
**[00:55:40 → 00:55:42] [Người nói?]** Ừ thì mày nghiên cứu mô hình gan là ok

<a id="S00778"></a>
**[00:55:44 → 00:55:46] [Người nói?]** Tại vì đề tài đó là nghiên cứu mô hình gan

<a id="S00779"></a>
**[00:55:46 → 00:55:49] [Người nói?]** Nó đeo liên quan gì với tấn công nhỉ

<a id="S00780"></a>
**[00:55:51 → 00:55:51] [Người nói?]** Vâng

<a id="S00781"></a>
**[00:55:53 → 00:56:04] [Người nói?]** Mày đánh tàu mày đeo bác đồng hành

<a id="S00782"></a>
**[00:56:04 → 00:56:05] [Người nói?]** À thì

<a id="S00783"></a>
**[00:56:07 → 00:56:08] [Người nói?]** Sĩ đồn gì

## Chuyện hội đồng được kể lại — chưa xác minh

<a id="S00784"></a>
**[00:56:14 → 00:56:16] [Người nói?]** [nghe không rõ 00:56:14; cần đối chiếu] Thầy Lãi Minh Tuấn ở trường mình không anh

<a id="S00785"></a>
**[00:56:16 → 00:56:20] [Người nói?]** Ông ấy là phản biện ngồi

<a id="S00786"></a>
**[00:56:20 → 00:56:23] [Người nói?]** Bố em cho thầy nghỉ luôn

<a id="S00787"></a>
**[00:56:23 → 00:56:25] [Người nói?]** Hôm nay thầy không đi

<a id="S00788"></a>
**[00:56:25 → 00:56:28] [Người nói?]** [nghe không rõ 00:56:25; cần đối chiếu] Là người nhất SQL là không hỏi

<a id="S00789"></a>
**[00:56:28 → 00:56:29] [Người nói?]** [nghe không rõ 00:56:28; cần đối chiếu] Thế là mới tát

<a id="S00790"></a>
**[00:56:29 → 00:56:37] [Người nói?]** [nghe không rõ 00:56:29; cần đối chiếu] Tại có 2 người không nhận phong bì

<a id="S00791"></a>
**[00:56:37 → 00:56:39] [Người nói?]** [nghe không rõ 00:56:37; cần đối chiếu] Thế là thầy đi luôn

<a id="S00792"></a>
**[00:56:39 → 00:56:41] [Người nói?]** [nghe không rõ 00:56:39; cần đối chiếu] Tự nhiên hôm nay thầy nghỉ

<a id="S00793"></a>
**[00:56:41 → 00:56:41] [Người nói?]** [nghe không rõ 00:56:41; cần đối chiếu] Vì việc gia đình

<a id="S00794"></a>
**[00:56:44 → 00:56:45] [Người nói?]** [nghe không rõ 00:56:44; cần đối chiếu] Thầy và 1 thầy nữa

<a id="S00795"></a>
**[00:56:45 → 00:56:46] [Người nói?]** [nghe không rõ 00:56:45; cần đối chiếu] Và thầy thầy kia

<a id="S00796"></a>
**[00:56:48 → 00:56:51] [Người nói?]** [nghe không rõ 00:56:48; cần đối chiếu] Mỗi đồng có 4-5 thầy

<a id="S00797"></a>
**[00:56:51 → 00:56:53] [Người nói?]** [nghe không rõ 00:56:51; cần đối chiếu] 1 thư ký, 2 phản biện

<a id="S00798"></a>
**[00:56:53 → 00:56:55] [Người nói?]** [nghe không rõ 00:56:53; cần đối chiếu] Và 2 thầy chủ trì hội đồng

<a id="S00799"></a>
**[00:56:56 → 00:56:57] [Người nói?]** [nghe không rõ 00:56:56; cần đối chiếu] 5 thầy

<a id="S00800"></a>
**[00:56:59 → 00:57:01] [Người nói?]** [nghe không rõ 00:56:59; cần đối chiếu] Nhưng mà một ông là bên chủ trì hội đồng

<a id="S00801"></a>
**[00:57:01 → 00:57:02] [Người nói?]** [nghe không rõ 00:57:01; cần đối chiếu] Nên là không lo

<a id="S00802"></a>
**[00:57:04 → 00:57:05] [Người nói?]** [nghe không rõ 00:57:04; cần đối chiếu] Giờ kiểu quản lý được anh

<a id="S00803"></a>
**[00:57:05 → 00:57:07] [Người nói?]** [nghe không rõ 00:57:05; cần đối chiếu] Thầy đấy là liêm

<a id="S00804"></a>
**[00:57:07 → 00:57:09] [Người nói?]** [nghe không rõ 00:57:07; cần đối chiếu] Kiểu không thích kiểu cái đấy rồi

<a id="S00805"></a>
**[00:57:09 → 00:57:10] [Người nói?]** [nghe không rõ 00:57:09; cần đối chiếu] Thì không sao

<a id="S00806"></a>
**[00:57:10 → 00:57:11] [Người nói?]** [nghe không rõ 00:57:10; cần đối chiếu] Cũng quen rồi

<a id="S00807"></a>
**[00:57:11 → 00:57:13] [Người nói?]** [nghe không rõ 00:57:11; cần đối chiếu] Và thầy Tuấn

<a id="S00808"></a>
**[00:57:16 → 00:57:17] [Người nói?]** [nghe không rõ 00:57:16; cần đối chiếu] Thầy Tuấn nghĩ

<a id="S00809"></a>
**[00:57:17 → 00:57:19] [Người nói?]** [nghe không rõ 00:57:17; cần đối chiếu] Thầy chỉ cần gửi câu hỏi thôi

<a id="S00810"></a>
**[00:57:19 → 00:57:21] [Người nói?]** [nghe không rõ 00:57:19; cần đối chiếu] Còn trò thì cứ ngồi vẫn đáp

## Hạn chế đánh giá và tính hữu ích

<a id="S00811"></a>
**[00:57:21 → 00:57:24] [Người nói?]** Hai câu thầy là hỏi phát là chết luôn

<a id="S00812"></a>
**[00:57:24 → 00:57:25] [Người nói?]** Em phải thừa nhận em chưa làm

<a id="S00813"></a>
**[00:57:25 → 00:57:34] [Người nói?]** [ASR cần nghe lại] Câu là cái này, cái dữ liệu này sinh ra thì ok, phần trăm ok rồi nhưng mà thực tế có dùng tấn công nổi không?

<a id="S00814"></a>
**[00:57:34 → 00:57:38] [Người nói?]** [ASR cần nghe lại] Em phải thừa nhận thẳng là mới sinh ra kiểu nhiễu.

<a id="S00815"></a>
**[00:57:38 → 00:57:44] [Người nói?]** [ASR cần nghe lại] Nhưng mà mấy cái mà vừa vừa được tường lửa chẳng qua là tường lửa nghĩ là nó không làm được gì cho đời, nó phải cho qua.

<a id="S00816"></a>
**[00:57:44 → 00:57:48] [Người nói?]** [ASR cần nghe lại] Chứ không phải là cho qua bởi vì nó có khả năng thái thác và ẩn bình.

<a id="S00817"></a>
**[00:57:50 → 00:58:03] [Người nói?]** Câu 2 là em dựa trên, nghĩa là mô hình học máy này thì dựa trên một cái bộ rule của SQL

<a id="S00818"></a>
**[00:58:04 → 00:58:10] [Người nói?]** Xong rồi dùng chính cái bộ rule đấy để kiểm tra xem dữ liệu nó có phải là SQL không kiểu đúng kiểu tự đạp bóng, tự thổi cò

<a id="S00819"></a>
**[00:58:10 → 00:58:16] [Người nói?]** Theo ông chỉ ra cái cũng phải thừa nhận là có lỗi trong thiết kế, đúng 2 câu là chết luôn

<a id="S00820"></a>
**[00:58:17 → 00:58:23] [Người nói?]** [nghe không rõ 00:58:17; cần đối chiếu] là kiểu mô hình có xu hướng tự đạp bóng tự hỏi có ý nghĩa là thằng đánh giá dựa trên một bộ

<a id="S00821"></a>
**[00:58:23 → 00:58:38] [Người nói?]** [nghe không rõ 00:58:23; cần đối chiếu] không nghe đây đây đừng ạ em tốt rồi hai thầy thì hỏi sao thầy nhắn tin cho mày thầy hỏi không em

<a id="S00822"></a>
**[00:58:39 → 00:58:45] [Người nói?]** [nghe không rõ 00:58:39; cần đối chiếu] hô câu của thầy khó quá em em phải viết em phải nốt lại xong rồi đưa vào chết gì thì cùng ra gì

<a id="S00823"></a>
**[00:58:52 → 00:59:08] [Người nói?]** [nghe không rõ 00:58:52; cần đối chiếu] Câu số 2, nếu hàm thưởng và hàm đánh giá đều dựa trên Keyword, Motif, Detect, Sở, Xây dựng

<a id="S00824"></a>
**[00:59:13 → 00:59:21] [Người nói?]** [nghe không rõ 00:59:13; cần đối chiếu] chuẩn mẹ đẹp mẹ ông bảo cứ 60 luôn 60 luôn bây giờ hỏi là chết

<a id="S00825"></a>
**[00:59:23 → 00:59:54] [Người nói?]** [nghe không rõ 00:59:23; cần đối chiếu] Các bạn nhớ đăng ký kênh để ủng hộ kênh của mình nhé.

<a id="S00826"></a>
**[00:59:57 → 00:59:59] [Người nói?]** [nghe không rõ 00:59:57; cần đối chiếu] Hẹn gặp lại các bạn trong những video tiếp theo.

<a id="S00827"></a>
**[01:00:00 → 01:00:14] [Người nói?]** [ASR cần nghe lại] Bây giờ mày về mày cần cải thiện cái đế đa, nếu không sẽ không bùi pháp

<a id="S00828"></a>
**[01:00:15 → 01:00:17] [Người nói?]** [ASR cần nghe lại] Vâng, mày phải hiểu đùa

<a id="S00829"></a>
**[01:00:18 → 01:00:22] [Người nói?]** [ASR cần nghe lại] Tại vì tao không học cái gan này, người ta không quan tâm

<a id="S00830"></a>
**[01:00:22 → 01:00:25] [Người nói?]** [ASR cần nghe lại] Tao quan tâm là cái tính hữu thức của nó là như thế nào

<a id="S00831"></a>
**[01:00:28 → 01:00:31] [Người nói?]** [ASR cần nghe lại] Tại các thầy đọc một lần, các thầy hiểu cái bùi này được

<a id="S00832"></a>
**[01:00:31 → 01:00:36] [Người nói?]** [ASR cần nghe lại] Mày chỉ thuyết trình trong khoảng bao nhiêu phút, một tiếng

<a id="S00833"></a>
**[01:00:36 → 01:00:42] [Người nói?]** Để các thầy hiểu được là cái đề án của em nó làm được cái gì, nó giúp ích được cái gì

<a id="S00834"></a>
**[01:00:42 → 01:00:42] [Người nói?]** Rồi

<a id="S00835"></a>
**[01:00:42 → 01:00:43] [Người nói?]** Và tao cũng chỉ cần hiểu cái đấy thôi

<a id="S00836"></a>
**[01:00:44 → 01:00:46] [Người nói?]** Tao như là các thầy của mày, trấn biển của mày

<a id="S00837"></a>
**[01:00:46 → 01:00:51] [Người nói?]** Chỉ cần hiểu là cái mô hình này của em nó có ứng dụng gì cho đời

<a id="S00838"></a>
**[01:00:51 → 01:00:53] [Người nói?]** Nó có giúp gì được cho đời không

<a id="S00839"></a>
**[01:00:55 → 01:00:58] [Người nói?]** Chứ thầy cũng địt cần hiểu là thằng gan này nó làm cái gì

<a id="S00840"></a>
**[01:00:59 → 01:01:05] [Người nói?]** Thầy chỉ biết là ví dụ mày là thằng gan này hơn cái thằng bình thường trong đời này là cái gì

<a id="S00841"></a>
**[01:01:05 → 01:01:06] [Người nói?]** Hiểu chưa

<a id="S00842"></a>
**[01:01:07 → 01:01:14] [Người nói?]** có nghĩa là đấy bây giờ mày hiểu được mình xong về sau mình ra này trình bày lại sao

<a id="S00843"></a>
**[01:01:15 → 01:01:23] [Người nói?]** khi mà hiểu rồi thì mày biết là con gan này nó sẽ áp dụng ở đâu hoặc là mày có thể tích hợp một con AI vào để mày làm lên tiến sĩ

<a id="S00844"></a>
**[01:01:24 → 01:01:25] [Người nói?]** hiểu chưa? hiểu

<a id="S00845"></a>
**[01:01:25 → 01:01:30] [Người nói?]** [nghe không rõ 01:01:25; cần đối chiếu] lên tiến sĩ là mày sẽ làm to hơn đúng không? ngoài SVL ra mày sẽ làm thêm

<a id="S00846"></a>
**[01:01:30 → 01:01:31] [Người nói?]** gần như là tất

<a id="S00847"></a>
**[01:01:31 → 01:01:32] [Người nói?]** ừ gần như là tất

<a id="S00848"></a>
**[01:01:32 → 01:01:34] [Người nói?]** dạng payload là gồm hết

<a id="S00849"></a>
**[01:01:34 → 01:01:38] [Người nói?]** Rằng này đang là dạng mà nó dễ nhất rồi

<a id="S00850"></a>
**[01:01:39 → 01:01:40] [Người nói?]** Thì mày phải hiểu là

<a id="S00851"></a>
**[01:01:42 → 01:01:43] [Người nói?]** Tại sao con AI nó lại

<a id="S00852"></a>
**[01:01:44 → 01:01:45] [Người nói?]** Làm được những cái

<a id="S00853"></a>
**[01:01:45 → 01:01:46] [Người nói?]** Mà nó học

<a id="S00854"></a>
**[01:01:47 → 01:01:49] [Người nói?]** Chứ còn mấy thứ này

<a id="S00855"></a>
**[01:01:50 → 01:01:51] [Người nói?]** [nghe không rõ 01:01:50; cần đối chiếu] Thì quát nó chặn hết rồi

<a id="S00856"></a>
**[01:01:52 → 01:01:53] [Người nói?]** Chả cần AI được

<a id="S00857"></a>
**[01:01:55 → 01:01:56] [Người nói?]** Cái rule tự sinh

<a id="S00858"></a>
**[01:01:57 → 01:01:59] [Người nói?]** Bây giờ làm nào để bái bát

<a id="S00859"></a>
**[01:01:59 → 01:02:00] [Người nói?]** Mấy cái rule đấy thì dễ vãi loàn

<a id="S00860"></a>
**[01:02:02 → 01:02:03] [Người nói?]** Bây giờ nếu mà nó thực tế

<a id="S00861"></a>
**[01:02:03 → 01:02:04] [Người nói?]** Thì phải là

<a id="S00862"></a>
**[01:02:04 → 01:02:06] [Người nói?]** Bất kỳ một thằng nào

<a id="S00863"></a>
**[01:02:06 → 01:02:14] [Người nói?]** Ví dụ mình thử trên một hệ thống thật chẳng hạn, mà mình bypass được thì nó luôn ok.

<a id="S00864"></a>
**[01:02:18 → 01:02:24] [Người nói?]** Ví dụ bây giờ mình đi mình test, ví dụ là được cho phép của hệ thống của trường,

<a id="S00865"></a>
**[01:02:24 → 01:02:32] [Người nói?]** [nghe không rõ 01:02:24; cần đối chiếu] ví dụ trường nó quát rồi, em đã chứng minh được trên khu vực của trường là như thế này, như thế này.

<a id="S00866"></a>
**[01:02:32 → 01:02:37] [Người nói?]** [ASR cần nghe lại] bài phát biệt bằng các cây lát tự sinh của em, chiếc chiếc.

<a id="S00867"></a>
**[01:02:38 → 01:02:41] [Người nói?]** [ASR cần nghe lại] Thế thì nói như là impact kỳ cực.

<a id="S00868"></a>
**[01:02:41 → 01:02:44] [Người nói?]** [ASR cần nghe lại] Mấy cái này, gu mày tự nghĩ, gu mày biết rồi.

<a id="S00869"></a>
**[01:02:45 → 01:02:50] [Người nói?]** [ASR cần nghe lại] Xong rồi bây giờ mày bảo con AI là sinh cho tao mấy cái cây lát, vượt được cái gu này.

<a id="S00870"></a>
**[01:02:51 → 01:02:58] [Người nói?]** [ASR cần nghe lại] Xong rồi mày gán cho cái con mốt thứ 2 của mày, đứng ở trên đá bóng thì vừa quay ra.

<a id="S00871"></a>
**[01:03:15 → 01:03:19] [Người nói?]** đúng kiểu tệ hơn quá

<a id="S00872"></a>
**[01:03:21 → 01:03:33] [Người nói?]** [ASR cần nghe lại] bây giờ mình phải kiểm tra xem để AI sinh đúng, sinh đúng, đối với một tí thực tế và hiểu mấy cái

<a id="S00873"></a>
**[01:03:35 → 01:03:44] [Người nói?]** [nghe không rõ 01:03:35; cần đối chiếu] WAP sử dụng như thế nào. Thì lúc đấy mình tư duy thì mình nghĩ ra những cái mà để nó thực tế bây

<a id="S00874"></a>
**[01:03:44 → 01:03:50] [Người nói?]** [ASR cần nghe lại] giờ còn không hiểu thì cũng sao mà mình nghĩ ra được. Tại vì tao nghĩ là tất cả những cái trên đầu

## Giải thích cơ chế GAN — nhiều thuật ngữ chưa rõ

<a id="S00875"></a>
**[01:04:01 → 01:04:10] [Người nói?]** phần thuật toán thì phải tự cây viết không hiểu không có ai giải thích không được toán thì bắt

<a id="S00876"></a>
**[01:04:10 → 01:04:15] [Người nói?]** buộc phải đọc bài báo thì mình mới dựng y hệt được rồi có đúng phần duy nhất mà phải làm thì

<a id="S00877"></a>
**[01:04:15 → 01:04:23] [Người nói?]** thì bắt buộc phải đọc thầy phải bắt buộc phải yêu cầu chứng minh từ đầu còn các phần khác là

<a id="S00878"></a>
**[01:04:23 → 01:04:34] [Người nói?]** [nghe không rõ 01:04:23; cần đối chiếu] phải tự làm tự để ai Zen trong đó có phần là Zen liên quan tới mấy cái đặc tính của sql.exe có nghĩa

<a id="S00879"></a>
**[01:04:34 → 01:04:44] [Người nói?]** là mày hiểu tương tận với thằng gan này rồi thì mỗi môi mục tiêu của gan đấy là nó sẽ nhận vào là

<a id="S00880"></a>
**[01:04:44 → 01:04:52] [Người nói?]** là một bộ dữ liệu nó sẽ sinh ra rất nhiều dữ liệu sinh kiểu gì nó sinh bởi thuật toán lan

<a id="S00881"></a>
**[01:04:52 → 01:04:59] [Người nói?]** [nghe không rõ 01:04:52; cần đối chiếu] chuyển ngược nghĩa là khi mà cái câu lệnh nó nó sẽ đi qua rất nhiều lớp mỗi lớp nó chỉ học đúng một

<a id="S00882"></a>
**[01:04:59 → 01:05:18] [Người nói?]** [nghe không rõ 01:04:59; cần đối chiếu] cái đặc điểm thôi thì sau khi mà nó có khoảng cho nó vào rất nhiều câu lệnh của nó sẽ sử dụng thuật

<a id="S00883"></a>
**[01:05:19 → 01:05:26] [Người nói?]** [nghe không rõ 01:05:19; cần đối chiếu] sở toán logistic để có thể là tính cái ra điện nó đi ngược quay trở lại mà ở ban đầu nha sau khi

<a id="S00884"></a>
**[01:05:26 → 01:05:32] [Người nói?]** [nghe không rõ 01:05:26; cần đối chiếu] sinh hợp một dữ liệu được nói thế nào thì cái ra điện này nó làm thế nào để nó suy ngược lại nó tính

<a id="S00885"></a>
**[01:05:32 → 01:05:42] [Người nói?]** [nghe không rõ 01:05:32; cần đối chiếu] logistik thì mục tiêu thì đúng là kiểu đưa đưa cái cái đưa các cái cụm giá trị đó là toán logistik

<a id="S00886"></a>
**[01:05:42 → 01:05:45] [Người nói?]** [nghe không rõ 01:05:42; cần đối chiếu] Nếu như mà giá trị đấy về 0

<a id="S00887"></a>
**[01:05:45 → 01:05:47] [Người nói?]** [nghe không rõ 01:05:45; cần đối chiếu] Thì là đang có khả năng đi ngược về ban đầu

<a id="S00888"></a>
**[01:05:47 → 01:05:48] [Người nói?]** Thì nó sẽ

<a id="S00889"></a>
**[01:05:52 → 01:05:55] [Người nói?]** Thế ý là nó đi ngược về 0 rồi

<a id="S00890"></a>
**[01:05:55 → 01:05:57] [Người nói?]** Là nó tính như thế nào

<a id="S00891"></a>
**[01:05:57 → 01:05:58] [Người nói?]** Cách thức tính của nó

<a id="S00892"></a>
**[01:05:59 → 01:06:00] [Người nói?]** Tính thì có một

<a id="S00893"></a>
**[01:06:01 → 01:06:03] [Người nói?]** Một hàm mất mát để có thể

<a id="S00894"></a>
**[01:06:03 → 01:06:05] [Người nói?]** Thay số vào để tính

<a id="S00895"></a>
**[01:06:06 → 01:06:08] [Người nói?]** Ví dụ một câu lệnh nó thay số về gì

<a id="S00896"></a>
**[01:06:08 → 01:06:11] [Người nói?]** Không một câu lệnh sẽ đi qua mấy cái lớp mà em bảo

<a id="S00897"></a>
**[01:06:11 → 01:06:12] [Người nói?]** Để nó chuyển thành các dạng số học

<a id="S00898"></a>
**[01:06:12 → 01:06:14] [Người nói?]** Thì lúc đấy mô hình mới hiểu được

<a id="S00899"></a>
**[01:06:14 → 01:06:18] [Người nói?]** Thế thôi em về xem lại cách giải thích

<a id="S00900"></a>
**[01:06:19 → 01:06:20] [Người nói?]** Số học

<a id="S00901"></a>
**[01:06:20 → 01:06:23] [Người nói?]** Đấy mày mà hiểu với thằng gan

<a id="S00902"></a>
**[01:06:23 → 01:06:25] [Người nói?]** Nó làm gì cho tao

<a id="S00903"></a>
**[01:06:25 → 01:06:28] [Người nói?]** Gan thì chỉ là

<a id="S00904"></a>
**[01:06:28 → 01:06:30] [Người nói?]** Một thằng là thằng đánh giá

<a id="S00905"></a>
**[01:06:30 → 01:06:31] [Người nói?]** Một thằng là thằng sinh

<a id="S00906"></a>
**[01:06:31 → 01:06:33] [Người nói?]** Thằng sinh sẽ cố gắng sinh nhiều dưới đất có thể

<a id="S00907"></a>
**[01:06:33 → 01:06:35] [Người nói?]** Thằng đánh giá thì sẽ cố gắng nhận biết

<a id="S00908"></a>
**[01:06:35 → 01:06:36] [Người nói?]** Sinh là địch mà nó xáo trộn lên à

<a id="S00909"></a>
**[01:06:37 → 01:06:38] [Người nói?]** Đúng rồi gần như là xáo trộn lên

<a id="S00910"></a>
**[01:06:38 → 01:06:41] [Người nói?]** Không đúng nghĩa là nó xáo trộn lên

<a id="S00911"></a>
**[01:06:42 → 01:06:44] [Người nói?]** Cứ cho một đống từ vào

<a id="S00912"></a>
**[01:06:44 → 01:06:46] [Người nói?]** Xong nó đang đung nó nhảy loạn lên

<a id="S00913"></a>
**[01:06:46 → 01:06:48] [Người nói?]** Không đúng nghĩa thôi

<a id="S00914"></a>
**[01:06:48 → 01:06:50] [Người nói?]** Sao anh không nói cái từ đầu nhỉ

<a id="S00915"></a>
**[01:06:50 → 01:06:51] [Người nói?]** Nó có ý nghĩa bùi gì

<a id="S00916"></a>
**[01:06:51 → 01:06:53] [Người nói?]** như thế mới có thằng đánh giá

<a id="S00917"></a>
**[01:06:53 → 01:06:57] [Người nói?]** thằng đánh giá là nó sẽ dựa vào các dấu hiệu từ bộ dữ liệu gốc

<a id="S00918"></a>
**[01:06:57 → 01:07:01] [Người nói?]** đánh giá xem thằng nào là thằng giả

<a id="S00919"></a>
**[01:07:01 → 01:07:04] [Người nói?]** và thằng nào là thằng có thể là thật

<a id="S00920"></a>
**[01:07:04 → 01:07:07] [Người nói?]** thì những cái thằng random thì nó sẽ bị loại gần hết

<a id="S00921"></a>
**[01:07:07 → 01:07:10] [Người nói?]** chỉ có những cái thằng may mắn random được mấy cái keyword chuẩn

<a id="S00922"></a>
**[01:07:10 → 01:07:13] [Người nói?]** kiểu may mắn ghép ra từ select được thành công chẳng hạn

<a id="S00923"></a>
**[01:07:13 → 01:07:17] [Người nói?]** thì nó sẽ giữ lại và nó cứ xoay dần xoay dần thôi anh

<a id="S00924"></a>
**[01:07:17 → 01:07:21] [Người nói?]** random tất cả sắp xếp lần lượt từ hướng cuối

<a id="S00925"></a>
**[01:07:21 → 01:07:24] [Người nói?]** bao nhiêu từ sắp xếp từ lấy từ

<a id="S00926"></a>
**[01:07:25 → 01:07:38] [Người nói?]** đúng rồi anh nói bắt đầu nhờ cái đoạn đúng rồi không phải đúng nghĩa kiểu tạo ra một loạt các

<a id="S00927"></a>
**[01:07:38 → 01:07:45] [Người nói?]** cái kính tự linh ta linh tinh không theo thứ tự gì cả thì sẽ thằng kia nó sẽ bắt đầu mới lọc dần

<a id="S00928"></a>
**[01:07:45 → 01:07:51] [Người nói?]** lọc dần không Nhưng mà cái thằng cái thằng cái thằng đánh giá nó sẽ lọc dần rất nhiều

<a id="S00929"></a>
**[01:07:51 → 01:08:01] [Người nói?]** nhiều sao lại để nó ra đừng tất cả các chữ gì nói nhé Nếu là kiểu random dịch từ select cái từ con

<a id="S00930"></a>
**[01:08:01 → 01:08:09] [Người nói?]** thôi Ví dụ nó sắp thành select con hoặc là con select ấy thôi mày đây là sắp xếp cả những ký

<a id="S00931"></a>
**[01:08:09 → 01:08:15] [Người nói?]** tự vớ vẩn đúng không anh thì em thấy mới trong cái kết quả của em mới có mấy cái ký tự rất là

<a id="S00932"></a>
**[01:08:15 → 01:08:29] [Người nói?]** dài mà nó không có ý nghĩa bởi vì là nó không học hết quay lại không nhưng mà cái thằng kia

<a id="S00933"></a>
**[01:08:29 → 01:08:36] [Người nói?]** thế là nó khả năng đánh giá được thì bắt đầu mới thành hình được này rồi đến bước tiếp theo là thằng

<a id="S00934"></a>
**[01:08:36 → 01:08:43] [Người nói?]** này nó dựa vào cái gì để nó ra một câu lệnh mà đúng thì bình thường là nó nó chỉ biết là đâu

<a id="S00935"></a>
**[01:08:43 → 01:08:49] [Người nói?]** là dữ liệu sinh ra hoặc đâu là đâu là dữ liệu tạo ra đâu là dữ liệu từ bộ dữ liệu đây nó kiểu

<a id="S00936"></a>
**[01:08:49 → 01:08:56] [Người nói?]** chỉ đánh giá xem thằng nào kiểu hàng giả hàng giả thật cái bộ dữ liệu là cái lộn gì là cái

<a id="S00937"></a>
**[01:08:56 → 01:09:04] [Người nói?]** cái mày nhập vào đúng không anh thế làm sao để nó sinh ra những cái câu lệnh mà nó biết là xem

<a id="S00938"></a>
**[01:09:04 → 01:09:16] [Người nói?]** sẽ phù hợp nó đánh giá với bộ dữ liệu đúng không đánh giá kiểu gì đây ví dụ đây là bộ dữ liệu được

<a id="S00939"></a>
**[01:09:16 → 01:09:24] [Người nói?]** chưa rồi thế cái thằng mà nó sinh ra đâu thằng sinh ra đâu đây thằng sinh ra đây anh ạ đây đâu

<a id="S00940"></a>
**[01:09:24 → 01:09:31] [Người nói?]** sinh ra đâu nghĩa là dữ liệu sinh ra cuối cùng nó sẽ trông như thế này anh nó biết rồi thế làm

<a id="S00941"></a>
**[01:09:31 → 01:09:34] [Người nói?]** nó làm sao để nó biết là cái câu lệnh truy vấn nó sẽ sinh ra thế này

<a id="S00942"></a>
**[01:09:34 → 01:09:38] [Người nói?]** nó dựa ở đâu để nó sắp được như thế này để nó chọn ra

<a id="S00943"></a>
**[01:09:38 → 01:09:41] [Người nói?]** cái thằng đánh giá nó sẽ chặn và nó...

<a id="S00944"></a>
**[01:09:41 → 01:09:42] [Người nói?]** đánh giá bằng cái gì?

<a id="S00945"></a>
**[01:09:42 → 01:09:44] [Người nói?]** đánh giá bằng một hàm

<a id="S00946"></a>
**[01:09:44 → 01:09:47] [Người nói?]** nó sẽ đánh giá được kiểu web ấy anh, bao nhiêu điểm

<a id="S00947"></a>
**[01:09:47 → 01:09:49] [Người nói?]** nếu mà dưới điểm chuẩn là nó cho lại luôn

<a id="S00948"></a>
**[01:09:49 → 01:09:51] [Người nói?]** còn những cái thằng nào mà được đánh điểm

<a id="S00949"></a>
**[01:09:51 → 01:09:53] [Người nói?]** nó sẽ nói...

<a id="S00950"></a>
**[01:09:53 → 01:09:53] [Người nói?]** đánh điểm dựa vào cái gì?

<a id="S00951"></a>
**[01:09:54 → 01:09:55] [Người nói?]** cũng dựa vào cái hàm bất mát đấy

<a id="S00952"></a>
**[01:09:55 → 01:09:59] [Người nói?]** một cái hàm mà nó sẽ đưa cái kiểu so sánh

<a id="S00953"></a>
**[01:10:00 → 01:10:04] [Người nói?]** là cái dữ liệu mà được sinh ra dữ liệu gốc thì nó được bao nhiêu điểm

<a id="S00954"></a>
**[01:10:04 → 01:10:13] [Người nói?]** [nghe không rõ 01:10:04; cần đối chiếu] mày phải hiểu nó so sánh bằng cái gì nó so sánh bằng một thuật toán cái thuật toán đấy sẽ đưa

<a id="S00955"></a>
**[01:10:13 → 01:10:22] [Người nói?]** [nghe không rõ 01:10:13; cần đối chiếu] thuật toán hoạt động thế nào lần đấy sẽ là đưa các cái ký tự của hai đưa ký tự của bộ dữ liệu mình

<a id="S00956"></a>
**[01:10:22 → 01:10:30] [Người nói?]** [nghe không rõ 01:10:22; cần đối chiếu] mình đưa vào chuyển đổi thành một cái một cái một cái chuỗi hàm tính toán sau là sau khi mình được

<a id="S00957"></a>
**[01:10:30 → 01:10:39] [Người nói?]** [nghe không rõ 01:10:30; cần đối chiếu] chuyển thành hát một cái phương trình hơn anh một phương trình mà có rất nhiều x mỗi x sẽ là một cái

<a id="S00958"></a>
**[01:10:39 → 01:10:58] [Người nói?]** [nghe không rõ 01:10:39; cần đối chiếu] lây ở và em còn nói phần này em phải học lại cách giải vì em cũng chỉ biết nói cho ví dụ ví dụ cái

<a id="S00959"></a>
**[01:11:00 → 01:11:04] [Người nói?]** thì cái câu lệnh này nó sẽ có cái cấu trúc, được chưa?

<a id="S00960"></a>
**[01:11:05 → 01:11:12] [Người nói?]** Cấu trúc là select này, like này, vớ vẩn vớ vẩn này, random các thứ này, được chưa?

<a id="S00961"></a>
**[01:11:14 → 01:11:17] [Người nói?]** Thì cái câu ban đầu ví dụ nó như thế này

<a id="S00962"></a>
**[01:11:18 → 01:11:23] [Người nói?]** thì cái câu sinh ra nó sẽ dựa vào cái cấu trúc như kiểu là cấu trúc của những câu ban đầu

<a id="S00963"></a>
**[01:11:23 → 01:11:30] [Người nói?]** để nó xác định xem cái câu về sau nó có phù hợp với cái cấu trúc đấy không, được chưa?

<a id="S00964"></a>
**[01:11:31 → 01:11:34] [Người nói?]** Thì cái cách thức nó xác định cái cấu trúc đấy là cái gì

<a id="S00965"></a>
**[01:11:34 → 01:11:40] [Người nói?]** Thì cái hàm đấy mày phải hiểu tương tận cái hàm

<a id="S00966"></a>
**[01:11:40 → 01:11:42] [Người nói?]** Anh nói thế thì em hiểu câu hỏi của anh rồi

<a id="S00967"></a>
**[01:11:42 → 01:11:45] [Người nói?]** Thì cái phương pháp cũ nó không học được cấu trúc

<a id="S00968"></a>
**[01:11:46 → 01:11:47] [Người nói?]** Phương pháp của em thì mới học được

<a id="S00969"></a>
**[01:11:47 → 01:11:49] [Người nói?]** Nó sẽ chia cái câu payload đấy

<a id="S00970"></a>
**[01:11:49 → 01:11:51] [Người nói?]** Phương pháp cũ nằm đéo cấu trúc

<a id="S00971"></a>
**[01:11:51 → 01:11:52] [Người nói?]** Phương pháp cũ là nó

<a id="S00972"></a>
**[01:11:52 → 01:11:55] [Người nói?]** Phương pháp random mà anh hỏi là gan đi anh

<a id="S00973"></a>
**[01:11:55 → 01:11:56] [Người nói?]** [nghe không rõ 01:11:55; cần đối chiếu] Gan thì nó không học được cấu trúc

<a id="S00974"></a>
**[01:11:56 → 01:11:58] [Người nói?]** [nghe không rõ 01:11:56; cần đối chiếu] Nó chỉ đơn giản là random liên tục thôi

<a id="S00975"></a>
**[01:11:58 → 01:12:00] [Người nói?]** Cái thằng cải tiến của em là sẽ chia

<a id="S00976"></a>
**[01:12:00 → 01:12:02] [Người nói?]** Thế mày đang làm về gan mà cải tiến cái lồn gì

<a id="S00977"></a>
**[01:12:02 → 01:12:05] [Người nói?]** Có phiên bản gan và gan gốc

<a id="S00978"></a>
**[01:12:05 → 01:12:09] [Người nói?]** [ASR cần nghe lại] hoặc dựa vào đấy để chứng minh là mình ưu việt hơn, còn gan của em gọi là sequengan

<a id="S00979"></a>
**[01:12:10 → 01:12:16] [Người nói?]** [nghe không rõ 01:12:10; cần đối chiếu] một một cái thằng gan khác thì sẽ chia cái câu lệnh đấy thành 20 phần hoặc là 40 phần mình tự đưa đầu vào

<a id="S00980"></a>
**[01:12:16 → 01:12:23] [Người nói?]** [nghe không rõ 01:12:16; cần đối chiếu] sau đó là mỗi cái cụm đấy thì có thể ghép từ các cái câu kiểu có thể 1 câu hoặc là 2 câu thì tùy

<a id="S00981"></a>
**[01:12:23 → 01:12:30] [Người nói?]** [nghe không rõ 01:12:23; cần đối chiếu] nói chung là trong cái khuôn 40 ký tự đấy đi mà nhét vào sau đó là mới đưa vào trong cái mô hình

<a id="S00982"></a>
**[01:12:30 → 01:12:31] [Người nói?]** nó sẽ đánh điểm

<a id="S00983"></a>
**[01:12:31 → 01:12:34] [Người nói?]** thì nếu như cái cụ nào mà được coi là

<a id="S00984"></a>
**[01:12:35 → 01:12:36] [Người nói?]** điểm cao nhất

<a id="S00985"></a>
**[01:12:36 → 01:12:38] [Người nói?]** thì nó sẽ ví dụ như ở vị số 1

<a id="S00986"></a>
**[01:12:38 → 01:12:40] [Người nói?]** là từ select có điểm cao nhất

<a id="S00987"></a>
**[01:12:40 → 01:12:42] [Người nói?]** thì nó sẽ ưu tiên là luôn luôn bắt đầu

<a id="S00988"></a>
**[01:12:42 → 01:12:43] [Người nói?]** với câu lệnh select

<a id="S00989"></a>
**[01:12:43 → 01:12:45] [Người nói?]** và nó bắt đầu sinh ra một hàng loại các câu

<a id="S00990"></a>
**[01:12:45 → 01:12:47] [Người nói?]** với từng vị trí

<a id="S00991"></a>
**[01:12:47 → 01:12:50] [Người nói?]** có 40 vị trí thì sẽ xem là top 1

<a id="S00992"></a>
**[01:12:50 → 01:12:51] [Người nói?]** sẽ là vị trí gì, top 2 vị trí, top 3 vị trí

<a id="S00993"></a>
**[01:12:51 → 01:12:53] [Người nói?]** thì bắt đầu xáo lên

<a id="S00994"></a>
**[01:12:53 → 01:12:55] [Người nói?]** thì đấy là hàng của em

<a id="S00995"></a>
**[01:13:04 → 01:13:07] [Người nói?]** Thì cái hàm đấy là có một vấn đề

<a id="S00996"></a>
**[01:13:07 → 01:13:10] [Người nói?]** Là nếu như mà nó phân chia bị đần

<a id="S00997"></a>
**[01:13:10 → 01:13:13] [Người nói?]** Ví dụ như là có những câu mà 200 ký tự

<a id="S00998"></a>
**[01:13:13 → 01:13:15] [Người nói?]** [nghe không rõ 01:13:13; cần đối chiếu] 222, đúng rồi, 222 câu

<a id="S00999"></a>
**[01:13:15 → 01:13:17] [Người nói?]** Nhưng mà chỉ cho có đúng 40 khuôn

<a id="S01000"></a>
**[01:13:17 → 01:13:20] [Người nói?]** Và đôi lúc là nó sẽ bị chia thiếu

<a id="S01001"></a>
**[01:13:20 → 01:13:22] [Người nói?]** Hoặc là kiểu dồn hết tất cả vào khuôn cuối

<a id="S01002"></a>
**[01:13:22 → 01:13:24] [Người nói?]** Thành ra là nó không học được

<a id="S01003"></a>
**[01:13:24 → 01:13:26] [Người nói?]** Hoặc là có đúng 40 khuôn

<a id="S01004"></a>
**[01:13:26 → 01:13:28] [Người nói?]** Nhưng mà câu truyền nó chỉ có 30 khuôn

<a id="S01005"></a>
**[01:13:28 → 01:13:29] [Người nói?]** Ai học?

<a id="S01006"></a>
**[01:13:29 → 01:13:31] [Người nói?]** Thực toán của em ạ.

<a id="S01007"></a>
**[01:13:31 → 01:13:33] [Người nói?]** Nó sẽ tự học ạ?

<a id="S01008"></a>
**[01:13:33 → 01:13:37] [Người nói?]** Vâng, nó học theo thực toán, kiểu biến đổi thành số vậy anh. Chứ không phải là để con này này làm.

<a id="S01009"></a>
**[01:13:37 → 01:13:50] [Người nói?]** Là tìm sắc xuất để cái từ này, à nghĩa là ở vị số 1 thì câu select nó sẽ có sắc xuất thành công là bao nhiêu.

<a id="S01010"></a>
**[01:13:50 → 01:13:58] [Người nói?]** [nghe không rõ 01:13:50; cần đối chiếu] Ví dụ như nó là có sắc xuất thành công 40% thì chứng tỏ là nên bắt đầu câu lệnh bằng câu select thì có khả năng có dấu hiệu SQL.

<a id="S01011"></a>
**[01:13:59 → 01:14:02] [Người nói?]** Tính sắc xuất thành công kiểu bùi gì? Nó phải dựa vào cái gì chứ?

<a id="S01012"></a>
**[01:14:02 → 01:14:04] [Người nói?]** nó dựa vào hàm sắc xuất

<a id="S01013"></a>
**[01:14:04 → 01:14:05] [Người nói?]** hàm sắc xuất

<a id="S01014"></a>
**[01:14:08 → 01:14:08] [Người nói?]** [nghe không rõ 01:14:08; cần đối chiếu] 1T Caclo

<a id="S01015"></a>
**[01:14:08 → 01:14:12] [Người nói?]** nó đúng kiểu hàm sắc xuất

<a id="S01016"></a>
**[01:14:12 → 01:14:14] [Người nói?]** nghĩa là nếu như A sinh ra

<a id="S01017"></a>
**[01:14:14 → 01:14:16] [Người nói?]** thì tỷ lệ của B sinh ra bao nhiêu

<a id="S01018"></a>
**[01:14:16 → 01:14:18] [Người nói?]** gieo 1 con súc sắc

<a id="S01019"></a>
**[01:14:21 → 01:14:22] [Người nói?]** kiểu gieo 1 con súc sắc

<a id="S01020"></a>
**[01:14:22 → 01:14:25] [Người nói?]** ra 1 mặt là 2

<a id="S01021"></a>
**[01:14:25 → 01:14:27] [Người nói?]** thì sắc xuất để có thể tổng

<a id="S01022"></a>
**[01:14:27 → 01:14:29] [Người nói?]** 2 mặt là 7

<a id="S01023"></a>
**[01:14:29 → 01:14:30] [Người nói?]** thì là bao nhiêu phần trăm

<a id="S01024"></a>
**[01:14:30 → 01:14:37] [Người nói?]** em không tính sắc xuất khai thác được

<a id="S01025"></a>
**[01:14:37 → 01:14:40] [Người nói?]** [ASR cần nghe lại] Để có thể tính cái góc đó thì phải đưa vào tường lửa lúc đấy mới check được

<a id="S01026"></a>
**[01:14:40 → 01:14:44] [Người nói?]** [nghe không rõ 01:14:40; cần đối chiếu] Còn khi mà em làm em chỉ quan tâm là nó có ra được hình thủ SQLS không

<a id="S01027"></a>
**[01:14:44 → 01:14:46] [Người nói?]** [ASR cần nghe lại] Thì gặp dính câu của thầy Tuấn

<a id="S01028"></a>
**[01:14:46 → 01:14:48] [Người nói?]** [ASR cần nghe lại] Nên là mai hôm đấy thầy không đi

<a id="S01029"></a>
**[01:14:51 → 01:14:58] [Người nói?]** [ASR cần nghe lại] Nói chung là đây gan đây đúng không?

<a id="S01030"></a>
**[01:14:58 → 01:15:00] [Người nói?]** [ASR cần nghe lại] Cái mô hình của mày đây đúng không?

<a id="S01031"></a>
**[01:15:00 → 01:15:01] [Người nói?]** [ASR cần nghe lại] Mô hình của em là mô hình

<a id="S01032"></a>
**[01:15:01 → 01:15:04] [Người nói?]** [ASR cần nghe lại] Đây ạ?

<a id="S01033"></a>
**[01:15:04 → 01:15:07] [Người nói?]** [ASR cần nghe lại] À đây đấy đúng rồi đúng rồi

<a id="S01034"></a>
**[01:15:07 → 01:15:10] [Người nói?]** [ASR cần nghe lại] Cái dữ liệu thực tế sinh ra nó thể trông như thế

<a id="S01035"></a>
**[01:15:11 → 01:15:17] [Người nói?]** [ASR cần nghe lại] Như là trông rất là rác mà ít ra nó đỡ hơn mấy cái đằng sau

<a id="S01036"></a>
**[01:15:17 → 01:15:30] [Người nói?]** Thì mới cần buổi hôm nay anh ở dưới em, em cũng biết là mô hình em cũng bánh vẽ, nếu mà nộp lên hội thảo toàn quốc người ta cũng cười vào mặt sau.

<a id="S01037"></a>
**[01:15:30 → 01:15:44] [Người nói?]** Anh thấy mày đang chưa hiểu lắm nên...

<a id="S01038"></a>
**[01:15:46 → 01:15:49] [Người nói?]** [nghe không rõ 01:15:46; cần đối chiếu] Gan bản gốc này thì nó thua cái gì?

<a id="S01039"></a>
**[01:15:49 → 01:15:55] [Người nói?]** [nghe không rõ 01:15:49; cần đối chiếu] Gan bản gốc là nó cố định ở con số 20, mà payload thì thường rất là dài.

<a id="S01040"></a>
**[01:15:56 → 01:15:59] [Người nói?]** [nghe không rõ 01:15:56; cần đối chiếu] Nên là nó có cái xu hướng là dồn hết tất cả vào cái khay cuối cùng.

<a id="S01041"></a>
**[01:16:00 → 01:16:03] [Người nói?]** Và nó bị thiếu một vài cái nữa qua cái thuật toán này.

<a id="S01042"></a>
**[01:16:03 → 01:16:06] [Người nói?]** [nghe không rõ 01:16:03; cần đối chiếu] Số gan màn gốc nó xinh có ngắn thế này được không?

<a id="S01043"></a>
**[01:16:06 → 01:16:09] [Người nói?]** Vâng, bởi vì cái thằng đánh giá nó đánh mạnh quá

<a id="S01044"></a>
**[01:16:09 → 01:16:13] [Người nói?]** Thành ra nó chỉ cần phát hiện là cái câu lệnh này vượt qua cái

<a id="S01045"></a>
**[01:16:13 → 01:16:16] [Người nói?]** Nó chỉ quan tâm là gen giống hệt cái câu lệnh cũ này

<a id="S01046"></a>
**[01:16:16 → 01:16:17] [Người nói?]** Đúng

<a id="S01047"></a>
**[01:16:17 → 01:16:18] [Người nói?]** Nó

<a id="S01048"></a>
**[01:16:19 → 01:16:24] [Người nói?]** Thế nếu mà câu gan của mày mới nó chỉ xuất hiện như thế nào?

<a id="S01049"></a>
**[01:16:24 → 01:16:24] [Người nói?]** Vâng, cũng nó chỉ xuất hiện như thế này

<a id="S01050"></a>
**[01:16:24 → 01:16:27] [Người nói?]** Bởi vì là cái thằng kia mấy cái dấu hiệu đặc biệt

<a id="S01051"></a>
**[01:16:27 → 01:16:29] [Người nói?]** Là nó không học nổi

<a id="S01052"></a>
**[01:16:30 → 01:16:33] [Người nói?]** Nhưng mà nó lại học được đúng một cái câu lệnh mà chắc chắn là thành công

<a id="S01053"></a>
**[01:16:33 → 01:16:35] [Người nói?]** thì nó chỉ quan tâm đến cái câu lệnh đấy thôi

<a id="S01054"></a>
**[01:16:35 → 01:16:37] [Người nói?]** nó chỉ sinh ra giống hiện đủ cái câu lệnh

<a id="S01055"></a>
**[01:16:37 → 01:16:40] [Người nói?]** ví dụ nó nhìn thấy

<a id="S01056"></a>
**[01:16:40 → 01:16:42] [Người nói?]** phải em cái nó chặn mẹ luôn

<a id="S01057"></a>
**[01:16:42 → 01:16:44] [Người nói?]** thì cái câu đằng sau

<a id="S01058"></a>
**[01:16:44 → 01:16:46] [Người nói?]** vô nghĩa hay có gì đó

<a id="S01059"></a>
**[01:16:46 → 01:16:48] [Người nói?]** thì tao thấy thằng gan bản gốc

<a id="S01060"></a>
**[01:16:49 → 01:16:50] [Người nói?]** mày cắt đéo rồi

<a id="S01061"></a>
**[01:16:50 → 01:16:52] [Người nói?]** [nghe không rõ 01:16:50; cần đối chiếu] 0.1 u liền

<a id="S01062"></a>
**[01:16:52 → 01:16:54] [Người nói?]** nó chặn mẹ luôn

<a id="S01063"></a>
**[01:16:54 → 01:16:56] [Người nói?]** câu này hơn cái đầu bùi

<a id="S01064"></a>
**[01:16:56 → 01:16:58] [Người nói?]** cái đấy nó dài hơn

<a id="S01065"></a>
**[01:16:59 → 01:17:00] [Người nói?]** dài hơn thì được cái gì

<a id="S01066"></a>
**[01:17:01 → 01:17:02] [Người nói?]** phải u liền nó chặn luôn

<a id="S01067"></a>
**[01:17:02 → 01:17:09] [Người nói?]** [nghe không rõ 01:17:02; cần đối chiếu] Cái cuốn của tao, tao chỉ cần nó u điền, tao chặn luôn. Chưa cần giải. Hiểu chưa?

<a id="S01068"></a>
**[01:17:10 → 01:17:10] [Người nói?]** [ASR cần nghe lại] Rồi.

## Trình bày đơn giản và đo phần hơn

<a id="S01069"></a>
**[01:17:11 → 01:17:18] [Người nói?]** [ASR cần nghe lại] Cái gì mới có buổi hôm nay? Không biết thực tế là làm kẻ test nó lại trông ổn định không?

<a id="S01070"></a>
**[01:17:19 → 01:17:23] [Người nói?]** [ASR cần nghe lại] Cứ đi học thôi. 4 năm cơ mà. 4 năm thì không học được tiền test à.

<a id="S01071"></a>
**[01:17:23 → 01:17:25] [Người nói?]** [ASR cần nghe lại] 4 năm không học thì ghét đi học à.

<a id="S01072"></a>
**[01:17:27 → 01:17:28] [Người nói?]** [ASR cần nghe lại] Đi học đi. Đi học đi.

<a id="S01073"></a>
**[01:17:29 → 01:17:30] [Người nói?]** [ASR cần nghe lại] Ngồi giải thích đi.

<a id="S01074"></a>
**[01:17:31 → 01:17:33] [Người nói?]** [ASR cần nghe lại] Nghe cái đề tài gần tiếng giữa mà ngồi.

<a id="S01075"></a>
**[01:17:34 → 01:17:37] [Người nói?]** [ASR cần nghe lại] Đéo hiểu được cái đề tài này làm lộn thì tao thấy là nó chưa ok đâu.

<a id="S01076"></a>
**[01:17:39 → 01:17:41] [Người nói?]** Bây giờ mày phải nói nó thật là dễ hiểu rồi đó

<a id="S01077"></a>
**[01:17:42 → 01:17:43] [Người nói?]** Người bình thường không hiểu được

<a id="S01078"></a>
**[01:17:44 → 01:17:45] [Người nói?]** Đừng có học thuật lên

<a id="S01079"></a>
**[01:17:46 → 01:17:48] [Người nói?]** Học thuật lên chả hiểu nó

<a id="S01080"></a>
**[01:17:48 → 01:17:49] [Người nói?]** Nó không giúp ích cho cái gì được

<a id="S01081"></a>
**[01:17:49 → 01:17:53] [Người nói?]** Mày nói đơn giản thôi

<a id="S01082"></a>
**[01:17:53 → 01:17:55] [Người nói?]** Lấy ví dụ đơn giản thôi

<a id="S01083"></a>
**[01:17:58 → 01:18:01] [Người nói?]** Cái gan của mày hơn cái gì

<a id="S01084"></a>
**[01:18:01 → 01:18:02] [Người nói?]** Thuật là nơi giờ

<a id="S01085"></a>
**[01:18:03 → 01:18:03] [Người nói?]** Gạch đầu dòng ra

<a id="S01086"></a>
**[01:18:03 → 01:18:07] [Người nói?]** Cái tính ứng dụng của nó

<a id="S01087"></a>
**[01:18:08 → 01:18:09] [Người nói?]** Chứ còn đéo một thằng nào

<a id="S01088"></a>
**[01:18:11 → 01:18:13] [Người nói?]** Mày cần làm cái gì

<a id="S01089"></a>
**[01:18:13 → 01:18:15] [Người nói?]** thì làm ra cái gì là mày phải bắt buộc phải hiểu rồi

<a id="S01090"></a>
**[01:18:15 → 01:18:18] [Người nói?]** còn để cho người khác hiểu được

<a id="S01091"></a>
**[01:18:18 → 01:18:21] [Người nói?]** thì mày phải đơn giản hóa nó đi

<a id="S01092"></a>
**[01:18:21 → 01:18:23] [Người nói?]** có nghĩa là mày rất hiểu rồi

<a id="S01093"></a>
**[01:18:23 → 01:18:24] [Người nói?]** thì mày mới đơn giản hóa được

<a id="S01094"></a>
**[01:18:26 → 01:18:30] [Người nói?]** thế mình nói là đang vang vông vần thể

<a id="S01095"></a>
**[01:18:32 → 01:18:33] [Người nói?]** tao chưa hiểu

<a id="S01096"></a>
**[01:18:33 → 01:18:36] [Người nói?]** chưa hiểu cái thằng gan nó hơn cái gì

<a id="S01097"></a>
**[01:18:37 → 01:18:40] [Người nói?]** ví dụ thằng kia nó sinh bị ngắn quá

<a id="S01098"></a>
**[01:18:40 → 01:18:41] [Người nói?]** đúng không?

<a id="S01099"></a>
**[01:18:41 → 01:18:41] [Người nói?]** vâng

<a id="S01100"></a>
**[01:18:42 → 01:18:44] [Người nói?]** và thằng gan kia nó sinh nhiều hơn

<a id="S01101"></a>
**[01:18:45 → 01:18:45] [Người nói?]** [ASR cần nghe lại] dài hơn

<a id="S01102"></a>
**[01:18:45 → 01:18:48] [Người nói?]** [ASR cần nghe lại] thế tại sao nó phải sinh dài hơn

<a id="S01103"></a>
**[01:18:51 → 01:18:52] [Người nói?]** [ASR cần nghe lại] nếu mà sinh ngắn quá

<a id="S01104"></a>
**[01:18:52 → 01:18:55] [Người nói?]** [ASR cần nghe lại] chứng tỏ là mô hình của em

<a id="S01105"></a>
**[01:18:55 → 01:18:56] [Người nói?]** [ASR cần nghe lại] chỉ tập trung vào những mẫu mà chắc chắn thành công

<a id="S01106"></a>
**[01:18:58 → 01:18:59] [Người nói?]** [ASR cần nghe lại] thì nếu mà chỉ đơn giản là

<a id="S01107"></a>
**[01:18:59 → 01:19:00] [Người nói?]** [ASR cần nghe lại] tập trung vào mẫu chắc chắn thành công

<a id="S01108"></a>
**[01:19:00 → 01:19:03] [Người nói?]** [ASR cần nghe lại] thì sẽ bỏ xót toàn bộ tất cả các mẫu mà có nguy cơ bị tấn công

<a id="S01109"></a>
**[01:19:03 → 01:19:06] [Người nói?]** [ASR cần nghe lại] cái đầu nó giống nhau mà

<a id="S01110"></a>
**[01:19:07 → 01:19:09] [Người nói?]** [ASR cần nghe lại] vâng, cái đầu giống nhau

<a id="S01111"></a>
**[01:19:09 → 01:19:10] [Người nói?]** [ASR cần nghe lại] đầu giống nhau thì nó chặn rồi

<a id="S01112"></a>
**[01:19:12 → 01:19:13] [Người nói?]** [ASR cần nghe lại] ông phải so sánh được là

<a id="S01113"></a>
**[01:19:13 → 01:19:15] [Người nói?]** [ASR cần nghe lại] cái mẫu chắc chắn thành công của

<a id="S01114"></a>
**[01:19:15 → 01:19:23] [Người nói?]** [nghe không rõ 01:19:15; cần đối chiếu] của cái mẫu không chưa chắc là thành công ấy thì nó bị trùng cướp với cả cái chắc chắn thành công

<a id="S01115"></a>
**[01:19:23 → 01:19:31] [Người nói?]** [nghe không rõ 01:19:23; cần đối chiếu] như là bao nhiêu phần trăm và ông tối ưu hơn nó là bao nhiêu phần trăm hiểu chưa Đấy thì em chưa

<a id="S01116"></a>
**[01:19:31 → 01:19:41] [Người nói?]** [nghe không rõ 01:19:31; cần đối chiếu] mày hơn người ta cái gì mày cũng nói là được thì đối với ai mà biết xin câu giải hơn xin câu giải

<a id="S01117"></a>
**[01:19:41 → 01:19:48] [Người nói?]** có hiệu quả không hiểu chưa Ví dụ cái đầu nó ra giống nhau rồi thì thằng này nó cũng chặn mà có

<a id="S01118"></a>
**[01:19:48 → 01:19:54] [Người nói?]** [nghe không rõ 01:19:48; cần đối chiếu] phải mỗi thằng dài của mày nó chặn đâu hai cái đầu ví dụ nó đều là U niền thì thằng kia nó có U

<a id="S01119"></a>
**[01:19:54 → 01:20:00] [Người nói?]** niền nó cũng chặn rồi thì là sinh cái đằng sau nó không quan tâm thì có nghĩa

<a id="S01120"></a>
**[01:20:00 → 01:20:02] [Người nói?]** là cái câu lệnh dài của mày, nó gặp thì nó chặn đúng không?

<a id="S01121"></a>
**[01:20:03 → 01:20:06] [Người nói?]** Nhưng mà bên này nó cũng là câu lệnh dài ngắn thôi, nhưng mà nó gặp thì nó vẫn chặn.

<a id="S01122"></a>
**[01:20:07 → 01:20:09] [Người nói?]** Kể cả thằng kia không khuyên truyền câu lệnh dài của mày.

<a id="S01123"></a>
**[01:20:10 → 01:20:13] [Người nói?]** Nó hiểu cái buổi. Về học đi.

<a id="S01124"></a>
**[01:20:13 → 01:20:17] [Người nói?]** Vâng. Nhờ anh ạ.
