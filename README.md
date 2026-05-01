# DS310.Q11 - Ứng dụng mô hình học sâu trong phân loại đa nhãn và tóm tắt văn bản


##  Giới thiệu
Nghiên cứu này tập trung ứng dụng các mô hình học sâu cho hai bài toán quan trọng trong Xử lý Ngôn ngữ Tự nhiên: phân loại văn bản và tóm tắt văn bản. 
Dự án tiến hành so sánh hiệu quả của các phương pháp học máy truyền thống, mô hình ngôn ngữ tiền huấn luyện và mô hình ngôn ngữ lớn dựa trên các độ đo đánh giá tiêu chuẩn.

## Mục tiêu


## Tập dữ liệu
* Dữ liệu được thu thập từ trang web ScienceDaily, một nguồn báo chí khoa học phổ biến bằng tiếng Anh.
* Bộ dữ liệu phản ánh nội dung và ngữ cảnh thực tế với tính đa dạng về các chủ đề như sức khỏe, khoa học tự nhiên, công nghệ và đời sống.
* Các trường dữ liệu chính bao gồm: `title` (Tiêu đề bài báo), `abstract` (Phần tóm tắt ngắn gọn), `full_story` (Nội dung đầy đủ), `related_topics` (Các chủ đề liên quan), và `topic` (Chủ đề chính).
* Tập dữ liệu được thiết kế phục vụ cho bài toán phân loại đơn nhãn, đa nhãn và tóm tắt văn bản.

## ⚙️ Phương pháp thực hiện
* **Tóm tắt văn bản:** Sử dụng mô hình sinh văn bản dựa trên kiến trúc Transformer bao gồm BART và PEGASUS (tiến hành tinh chỉnh) cùng với mô hình ngôn ngữ lớn Qwen2.5 (zero-shot và few-shot). Đầu vào là toàn bộ nội dung bài viết (`full_story`) và đầu ra mục tiêu là bản tóm tắt (`abstract`).
* **Phân loại đơn nhãn:** Sử dụng Logistic Regression kết hợp đặc trưng TF-IDF và tinh chỉnh mô hình BERT. Bài toán lấy đầu vào là toàn bộ nội dung bài viết (`full_story`).
* **Phân loại đa nhãn:** Tinh chỉnh các mô hình ngôn ngữ tiền huấn luyện RoBERTa và DeBERTa. Đầu vào cho mô hình cũng là toàn bộ nội dung bài viết (`full_story`).

## Kết quả thực nghiệm
### 1. Tóm tắt văn bản
* Mô hình BART (fine-tuned) đạt kết quả cao nhất trên tất cả các độ đo, với ROUGE-1 đạt 60.29 và ROUGE-L đạt 53.92.
* [BART thể hiện khả năng bảo toàn thông tin và độ bao phủ tốt, phù hợp cho các yêu cầu tóm tắt đáng tin cậy.
* Mô hình Qwen2.5 cho thấy ưu thế về khả năng nén và khái quát hóa nội dung theo hướng trừu tượng cao hơn.
* Phân tích cho thấy cả hai nhóm mô hình đều kiểm soát tốt hiện tượng hallucination với tỷ lệ mâu thuẫn (Contradiction) thấp.

### 2. Phân loại văn bản
* **Đơn nhãn:** Mô hình BERT vượt trội hơn Logistic Regression với độ chính xác đạt 51% so với 47%. Tuy nhiên, kết quả này bị giới hạn do tính chất phức tạp của dữ liệu báo chí khoa học, nơi một bài viết thường xuyên đề cập đến nhiều khía cạnh.
* **Đa nhãn:** Cả hai mô hình RoBERTa và DeBERTa đều đạt hiệu năng cao với Micro-F1 và Macro-F1 xấp xỉ 0.89. Điều này minh chứng các kiến trúc Transformer hiện đại hoàn toàn đủ khả năng xử lý tốt sự phức tạp và đa dạng về chủ đề của dữ liệu báo chí khoa học.
