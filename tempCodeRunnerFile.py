import pyodbc

server = 'DESKTOP-91K319E\\WINCC'  # Escape backslash
driver = 'ODBC Driver 17 for SQL Server'
conn_string = f'DRIVER={{{driver}}};SERVER={server};Trusted_Connection=yes;'

def Connect_db(database=None):
    try:
        if database:
            conn_string_with_db = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
            conn = pyodbc.connect(conn_string_with_db, autocommit=True)
        else:
            conn = pyodbc.connect(conn_string, autocommit=True)
        print('Kết nối thành công')
        return conn
    except Exception as e:
        print(f'Lỗi kết nối: {e}')
        return None
    
def Create_database(conn, database):
    cursor = conn.cursor()
    try:
        cursor.execute(f'CREATE DATABASE {database}')  # Tạo cơ sở dữ liệu
        print(f'Database "{database}" đã được tạo.')
    except Exception as e:
        print(f'Lỗi tạo cơ sở dữ liệu: {e}')
    finally:
        cursor.close()

def Create_table(conn, table):
    cursor = conn.cursor()
    try:
        cursor.execute(f'''
            CREATE TABLE {table} (
                MaCongViec INT PRIMARY KEY,
                TieuDe NVARCHAR(50) NOT NULL,
                MoTa NVARCHAR(100) DEFAULT 'Pending',
                NgayBatDau DATETIME,
                NgayKetThuc DATETIME,
                TrangThai NVARCHAR(50) DEFAULT 'Done',
                CHECK (TrangThai IN ('Done', 'Not Done'))
            )
        ''')  # Tạo bảng
        print(f'Bảng "{table}" đã được tạo.')
    except Exception as e:
        print(f'Lỗi tạo bảng: {e}')
    finally:
        cursor.close()

def Insert(conn, table, MaCongViec, TieuDe, MoTa, NgayBatDau, NgayKetThuc, TrangThai):
    cursor = conn.cursor()
    try:
        cursor.execute(f'''
            INSERT INTO {table} (MaCongViec, TieuDe, MoTa, NgayBatDau, NgayKetThuc, TrangThai)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (MaCongViec, TieuDe, MoTa, NgayBatDau, NgayKetThuc, TrangThai))  # Chèn dữ liệu
        print("Công việc đã được thêm.")
    except Exception as e:
        print(f'Lỗi chèn dữ liệu: {e}')
    finally:
        cursor.close()

def List_column(conn, table):
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM {table}')  # Lấy tất cả bản ghi
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]}, Tiêu đề: {row[1]}, Mô tả: {row[2]}, Ngày bắt đầu: {row[3]}, Ngày kết thúc: {row[4]}, Trạng thái: {row[5]}")
    except Exception as e:
        print(f'Lỗi truy vấn: {e}')
    finally:
        cursor.close()
        
def Update_column(conn, table, MaCongViec, new_TieuDe, new_MoTa, new_NgayBatDau, new_NgayKetThuc, new_TrangThai):
    cursor = conn.cursor()
    try:
        cursor.execute(f'''
            UPDATE {table}
            SET
                TieuDe = ?,
                MoTa = ?,
                NgayBatDau = ?,
                NgayKetThuc = ?,
                TrangThai = ?
            WHERE MaCongViec = ?
        ''', (new_TieuDe, new_MoTa, new_NgayBatDau, new_NgayKetThuc, new_TrangThai, MaCongViec))  # Cập nhật công việc
        print("Trạng thái công việc đã được cập nhật.")
    except Exception as e:
        print(f'Lỗi cập nhật: {e}')
    finally:
        cursor.close()

def delete_column(conn, table, MaCongViec):
    cursor = conn.cursor()
    try:
        cursor.execute(f'''
            DELETE FROM {table}
            WHERE MaCongViec = ?
        ''', (MaCongViec,))  # Xóa công việc
        print("Công việc đã được xóa.")
    except Exception as e:
        print(f'Lỗi xóa dữ liệu: {e}')
    finally:
        cursor.close()

def main():
    conn = Connect_db()  # Kết nối đến SQL Server
    if conn is None:
        return

    database = input('Nhập tên Database: ')
    Create_database(conn, database)  # Tạo cơ sở dữ liệu
    conn.close()  # Đóng kết nối tạm thời

    # Kết nối đến cơ sở dữ liệu vừa tạo
    conn = Connect_db(database)
    if conn is None:
        return

    table = input('Nhập tên Bảng: ')
    Create_table(conn, table)  # Tạo bảng

    while True:
        print("\nQuản lý To-Do List")
        print("1. Thêm công việc mới")
        print("2. Liệt kê tất cả công việc")
        print("3. Cập nhật trạng thái công việc")
        print("4. Xóa công việc")
        print("5. Thoát")

        choice = int(input('Nhập: '))
        if choice == 1:
            MaCongViec = int(input('Nhập mã công việc: '))
            TieuDe = input('Nhập tiêu đề: ')
            MoTa = input('Nhập mô tả: ')
            NgayBatDau = input('Nhập ngày bắt đầu (YYYY-MM-DD): ')
            NgayKetThuc = input('Nhập ngày kết thúc (YYYY-MM-DD): ')
            TrangThai = input('Nhập trạng thái (Done/Not Done): ')
            Insert(conn, table, MaCongViec, TieuDe, MoTa, NgayBatDau, NgayKetThuc, TrangThai)
        elif choice == 2:
            List_column(conn, table)
        elif choice == 3:
            MaCongViec = int(input('Nhập mã công việc cần cập nhật: '))
            new_TieuDe = input('Nhập tiêu đề mới: ')
            new_MoTa = input('Nhập mô tả mới: ')
            new_NgayBatDau = input('Nhập ngày bắt đầu mới (YYYY-MM-DD): ')
            new_NgayKetThuc = input('Nhập ngày kết thúc mới (YYYY-MM-DD): ')
            new_TrangThai = input('Nhập trạng thái mới (Done/Not Done): ')
            Update_column(conn, table, MaCongViec, new_TieuDe, new_MoTa, new_NgayBatDau, new_NgayKetThuc, new_TrangThai)
        elif choice == 4:
            MaCongViec = int(input('Nhập mã công việc cần xóa: '))
            delete_column(conn, table, MaCongViec)
        elif choice == 5:
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ! Vui lòng thử lại.")

    conn.close()  # Đóng kết nối khi kết thúc

if __name__ == "__main__":
    main()
