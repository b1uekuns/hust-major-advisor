import pandas as pd

def get_safety_level(user_score, benchmark_score):
    """Xác định mức độ an toàn dựa trên điểm."""
    if pd.isna(benchmark_score) or benchmark_score == 0:
        return "Không có dữ liệu điểm chuẩn"
    if user_score >= benchmark_score + 1.5:
        return "Rất an toàn"
    elif user_score >= benchmark_score:
        return "An toàn"
    elif user_score >= benchmark_score - 2.5:
        return "Cân nhắc"
    elif user_score >= benchmark_score - 4.0:
        return "Thách thức"
    else:
        return "Khó"

def get_program_type(major_code):
    """Phân loại chương trình dựa trên mã ngành."""
    special_prefixes = ['-E', '-EP', 'TROY-', '-LUH', '-GU', '-NUT']
    if any(prefix in major_code for prefix in special_prefixes):
        return "Chương trình Đặc biệt (Tiên tiến, Quốc tế,...)"
    else:
        return "Chương trình Chuẩn"

def suggest_majors():
    """Hàm chính chạy hệ chuyên gia tư vấn ngành học."""
    # 1. NẠP CƠ SỞ TRI THỨC
    try:
        df = pd.read_csv('data.csv', encoding='utf-8')
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file 'data.csv'. Hãy đảm bảo bạn đã lưu file đúng chỗ.")
        return

    # 2. THU THẬP THÔNG TIN NGƯỜI DÙNG
    print("--- HỆ CHUYÊN GIA TƯ VẤN NGÀNH HỌC BÁCH KHOA HÀ NỘI (TSA) ---")
    
    while True:
        try:
            user_score = float(input("Nhập điểm thi Đánh giá tư duy của bạn (thang 100): "))
            if 0 <= user_score <= 100:
                break
            else:
                print("Điểm không hợp lệ, vui lòng nhập điểm từ 0 đến 100.")
        except ValueError:
            print("Vui lòng nhập một con số.")

    # Các từ khóa chi tiết để người dùng lựa chọn, được nhóm lại
    interest_groups = {
        "--- Nhóm Công Nghệ Thông Tin Và Toán ---": [
            "Thuật toán, Phần mềm, Lập trình",
            "AI, Machine-learning, Khoa học dữ liệu, Big-data",
            "An toàn thông tin, Cyber-security, Bảo mật mạng",
            "Phần cứng, Kiến trúc máy tính, Hệ điều hành",
            "Toán ứng dụng, Tin học, Thuật toán, Hệ thống"
            "Giáo dục, E-learning,Lập trình",
            "Thuật toán, Hệ thống, Phân tích dữ liệu, Lập trình, Quản lý"
        ],

        "--- Nhóm Vật lý ---": [
            "Vật lý ứng dụng, Quang học, laser, Nghiên cứu",
            "Năng lượng hạt nhân, Vật lý hạt nhân, Nghiên cứu",
            "Vật lý ứng dụng, Y sinh, Thiết bị y tế",
        ],

        "--- Nhóm Điện, Điện tử ---": [
            "Điện, Hệ thống điện, Thiết bị điện",
            "Tự động hóa, Robot, Hệ thống điều khiển, Lập trình PLC",
            "Điện tử, Viễn thông, Thiết kế mạch",
            "Điện, Năng lượng, Năng lượng tái tạo",
            "Y sinh, Thiết bị y tế, Xử lý tín hiệu y học",
            "Đa phương tiện, Xử lý ảnh, Thiết kế game, Truyền thông",
            "Hệ thống nhúng, Iot, Lập trình nhúng"
        ],

        "--- Nhóm Cơ khí ---": [
            "Nhiệt lạnh, Điều hòa không khí, Năng lượng",
            "Cơ khí, Điện tử, Lập trình điều khiển, Robot",
            "Cơ khí chế tạo, Thiết kế máy, Gia công CNC",
            "Oto, Động cơ, Hệ thống truyền lực, Xe điện",
            "Động cơ, Máy móc thủy lực, Khí nén",
            "Hàng không, Máy bay, Khí động lực học",
        ],

        "--- Nhóm Vật liệu ---": [
            "Vật liệu kim loại, Vật liệu học",
            "Vi điện tử, Thiết kế vi mạch, Bán dẫn, Nano",
            "Polymer, Composite, Vật liệu học",
            "Dệt may, Thời trang, Vật liệu dệt",
            "In ấn,Bao bì,Vật liệu in"
        ],

        "--- Nhóm Kinh tế ---": [
            "Kinh tế, Quản lý, Năng lượng, Chính sách",
            "Kinh tế, Quản lý, Sản xuất, Tối ưu hóa",
            "Kinh tế, Kinh doanh, Marketing, Quản trị",
            "Kinh tế, Kế toán, Kiểm toán, Tài chính",
            "Kinh tế, Tài chính, Ngân hàng, Đầu tư",
            "Kinh tế, Phân tích dữ liệu, Business-analytics",
            "Kinh tế, Logistics, Chuỗi cung ứng, Xuất nhập khẩu",

        ],

        "--- Nhóm Hóa và Khoa học sự sống ---": [
            "Sinh học, Công nghệ sinh học, Y sinh",
            "Thực phẩm, Chế biến, Dinh dưỡng",
            "Hóa học, Hóa dầu, Polymer, Sản xuất hóa chất",
            "Hóa học, Hóa phân tích, Nghiên cứu",
            "Hóa dược, Y dược, Hóa học",
            "Môi trường, Xử lý rác thải, Phát triển bền vững",
            "Môi trường, Quản lý, Tài nguyên, Chính sách"
        ],

        "--- Nhóm Ngôn ngữ và Giáo dục---": [
            "Tiếng Anh, Kỹ thuật, Biên phiên dịch",
            "Tiếng Anh, Thương mại, Biên phiên dịch",
            "Giáo dục, E-learning, Lập trình",
            "Giáo dục, Quản lý, Chính sách",
        ]
    }
    
    print("\nChọn các lĩnh vực/từ khóa bạn quan tâm (nhập số, cách nhau bởi dấu cách):")
    all_options = []
    option_index = 1
    for group_name, keywords_list in interest_groups.items():
        print(group_name)
        for keywords in keywords_list:
            print(f"  {option_index}. {keywords}")
            all_options.append(keywords)
            option_index += 1
            
    user_keywords = []
    while not user_keywords:
        try:
            choices = input("Lựa chọn của bạn: ").split()
            selected_indices = [int(c) - 1 for c in choices]
            for i in selected_indices:
                if 0 <= i < len(all_options):
                    tags = [tag.strip() for tag in all_options[i].split(',')]
                    user_keywords.extend(tags)
            
            user_keywords = list(dict.fromkeys(user_keywords))
            if not user_keywords:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
        except (ValueError, IndexError):
            print("Định dạng nhập không đúng. Vui lòng nhập các con số hợp lệ.")

    # 3. BỘ SUY DIỄN (INFERENCE ENGINE)
    results = []
    for index, row in df.iterrows():
        if not isinstance(row['ChiTietTags'], str):
            continue
        
        major_tags = [tag.strip() for tag in row['ChiTietTags'].split(',')]
        # Tính điểm phù hợp: số từ khóa của ngành khớp với sở thích của người dùng
        matched_tags = [tag for tag in user_keywords if tag in major_tags]
        interest_score = len(matched_tags)
        
        if interest_score > 0:
            safety_level = get_safety_level(user_score, row['DiemChuan2024'])
            
            if safety_level != "Khó":
                program_type = get_program_type(row['MaNganh'])
                results.append({
                    'MaNganh': row['MaNganh'],
                    'TenNganh': row['TenNganh'],
                    'LoaiChuongTrinh': program_type,
                    'DoAnToan': safety_level,
                    'DiemPhuHop': interest_score,
                    'DiemChuan2024': row['DiemChuan2024'],
                    'MatchedTags': matched_tags
                })

    # 4. TRÌNH BÀY KẾT QUẢ
    print("\n--- CÁC NGÀNH HỌC PHÙ HỢP GỢI Ý CHO BẠN ---")
    
    if not results:
        print("Rất tiếc, không tìm thấy ngành nào phù hợp với điểm số và sở thích của bạn." \
        " Hãy thử lại với các sở thích khác xem sao.")
        return

    # Sắp xếp kết quả với 3 tiêu chí
    safety_order = {"Rất an toàn": 0, "An toàn": 1, "Cân nhắc": 2, "Thách thức": 3, "Không có dữ liệu điểm chuẩn": 4}
    
    sorted_results = sorted(results, key=lambda x: (
        -x['DiemPhuHop'],
        0 if x['LoaiChuongTrinh'] == 'Chương trình Chuẩn' else 1,
        safety_order.get(x['DoAnToan'], 99),
        -x['DiemChuan2024'] if pd.notna(x['DiemChuan2024']) else 0
    ))


    for r in sorted_results:
        diem_chuan_str = f"{r['DiemChuan2024']:.2f}" if pd.notna(r['DiemChuan2024']) else "N/A"
        matched_tags_str = ", ".join(r['MatchedTags'])
        
        print(f"\nNgành: {r['TenNganh']} ({r['MaNganh']})")
        print(f"  - Loại chương trình: {r['LoaiChuongTrinh']}")
        print(f"  - Điểm chuẩn 2024: {diem_chuan_str}")
        print(f"  - Độ an toàn điểm số: {r['DoAnToan']}")
        print(f"  - Lý do phù hợp: Khớp với các sở thích của bạn về ({matched_tags_str}).")

if __name__ == "__main__":
    suggest_majors()
