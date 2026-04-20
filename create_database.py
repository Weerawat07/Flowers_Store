import sqlite3
from datetime import datetime

# สร้างการเชื่อมต่อกับฐานข้อมูล flowers_store.db
conn = sqlite3.connect('flowers_store.db')
cursor = conn.cursor()

print("=" * 60)
print("สร้างฐานข้อมูล Flowers Store")
print("=" * 60)

# ลบตารางเก่า (ถ้ามี) เพื่อให้สร้างใหม่
cursor.execute('DROP TABLE IF EXISTS Flowers')
cursor.execute('DROP TABLE IF EXISTS Categories')

# ============================================================
# สร้างตาราง Categories (ตารางรอง)
# ============================================================
cursor.execute('''
    CREATE TABLE Categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(100) NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("\n✓ สร้างตาราง Categories สำเร็จ")

# ============================================================
# สร้างตาราง Flowers (ตารางหลัก)
# ============================================================
cursor.execute('''
    CREATE TABLE Flowers (
        flower_id INTEGER PRIMARY KEY AUTOINCREMENT,
        flower_name VARCHAR(100) NOT NULL,
        category_id INTEGER NOT NULL,
        price DECIMAL(8, 2) NOT NULL,
        stock INTEGER DEFAULT 0,
        description TEXT,
        color VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES Categories(category_id)
    )
''')
print("✓ สร้างตาราง Flowers สำเร็จ")

# ============================================================
# เพิ่มข้อมูลตัวอย่างในตาราง Categories
# ============================================================
categories_data = [
    ('ดอกไม้สดใจร่วมสุข', 'ดอกไม้สดใจทั่วไป ใช้ในโอกาส ต่าง ๆ'),
    ('ดอกไม้วัสดุและใบไม้', 'วัสดุแต่งช่อดอกไม้ ใบไม้เสริมสวยงาม'),
    ('ดอกไม้แห้ง', 'ดอกไม้แห้งทนทาน สำหรับตกแต่งระยะยาว'),
    ('ดอกไม้ดื่มน้ำ', 'ดอกไม้ที่เหมาะสำหรับการตั้งตนไว้ในน้ำ'),
]

cursor.executemany(
    'INSERT INTO Categories (category_name, description) VALUES (?, ?)',
    categories_data
)
print("✓ เพิ่มข้อมูลตัวอย่าง Categories แล้ว (4 รายการ)")

# ============================================================
# เพิ่มข้อมูลตัวอย่างในตาราง Flowers
# ============================================================
flowers_data = [
    ('กุหลาบแดง', 1, 150.00, 50, 'กุหลาบแดงสดใจขนาดกลาง', 'แดง'),
    ('ทิวลิปสีชมพู', 1, 120.00, 35, 'ทิวลิปสีชมพูสวยงามจากเนเธอร์แลนด์', 'ชมพู'),
    ('ดอกแสนดาสีม่วง', 2, 80.00, 60, 'ดอกแสนดาสีม่วงเอกเทศ', 'ม่วง'),
    ('ดอกไม้แห้งสาขาสีขาว', 3, 200.00, 25, 'วัสดุแต่งช่อดอกไม้สีขาวสวยงาม', 'ขาว'),
    ('ดอกบุปผาสีเหลือง', 4, 90.00, 45, 'ดอกบุปผาสีเหลืองสดใจและสดชื่น', 'เหลือง'),
]

cursor.executemany(
    '''INSERT INTO Flowers (flower_name, category_id, price, stock, description, color) 
       VALUES (?, ?, ?, ?, ?, ?)''',
    flowers_data
)
print("✓ เพิ่มข้อมูลตัวอย่าง Flowers แล้ว (5 รายการ)")

# บันทึกการเปลี่ยนแปลง
conn.commit()

# ============================================================
# แสดงข้อมูลที่สร้างขึ้น
# ============================================================
print("\n" + "=" * 60)
print("ข้อมูลในตาราง Categories:")
print("=" * 60)
cursor.execute('SELECT * FROM Categories')
categories = cursor.fetchall()
for cat in categories:
    print(f"ID: {cat[0]}, ชื่อ: {cat[1]}, คำอธิบาย: {cat[2]}")

print("\n" + "=" * 60)
print("ข้อมูลในตาราง Flowers:")
print("=" * 60)
cursor.execute('''
    SELECT f.flower_id, f.flower_name, c.category_name, f.price, 
           f.stock, f.color 
    FROM Flowers f 
    JOIN Categories c ON f.category_id = c.category_id
''')
flowers = cursor.fetchall()
for flower in flowers:
    print(f"ID: {flower[0]}, ชื่อ: {flower[1]}, หมวดหมู่: {flower[2]}, "
          f"ราคา: {flower[3]} บาท, คงเหลือ: {flower[4]} ชิ้น, สี: {flower[5]}")

# ปิดการเชื่อมต่อ
conn.close()

print("\n" + "=" * 60)
print("✓ สร้างฐานข้อมูล flowers_store.db สำเร็จ!")
print("=" * 60)
