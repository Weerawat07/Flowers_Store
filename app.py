import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# ============================================================
# กำหนดเส้นทางฐานข้อมูลให้ใช้ได้ทั้ง Windows และ PythonAnywhere
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'flowers_store.db')

def get_db_connection():
    """สร้างการเชื่อมต่อกับฐานข้อมูล SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================
# Route: หน้าแรก - แสดงสินค้าทั้งหมด
# ============================================================
@app.route('/')
def index():
    """แสดงหน้าแรกพร้อมรายการดอกไม้"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # ดึงข้อมูลดอกไม้พร้อมชื่อหมวดหมู่
    cursor.execute('''
        SELECT f.flower_id, f.flower_name, c.category_name, f.price, 
               f.stock, f.color, f.description, f.category_id
        FROM Flowers f 
        JOIN Categories c ON f.category_id = c.category_id
        ORDER BY f.flower_id DESC
    ''')
    flowers = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', flowers=flowers, page='home')

# ============================================================
# Route: หมวดหมู่ - แสดงและจัดการหมวดหมู่
# ============================================================
@app.route('/categories')
def categories():
    """แสดงหน้าจัดการหมวดหมู่"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Categories ORDER BY category_id DESC')
    categories = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', categories=categories, page='categories')

# ============================================================
# Route: เพิ่มดอกไม้ใหม่
# ============================================================
@app.route('/add-flower', methods=['GET', 'POST'])
def add_flower():
    """เพิ่มดอกไม้ใหม่"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Categories ORDER BY category_name')
    categories = cursor.fetchall()
    conn.close()
    
    if request.method == 'POST':
        flower_name = request.form['flower_name']
        category_id = request.form['category_id']
        price = request.form['price']
        stock = request.form['stock']
        color = request.form['color']
        description = request.form['description']
        
        # ตรวจสอบว่ากรอกข้อมูลครบ
        if not all([flower_name, category_id, price, stock, color]):
            flash('⚠️ กรุณากรอกข้อมูลทั้งหมด', 'error')
            return redirect(url_for('add_flower'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Flowers (flower_name, category_id, price, stock, color, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (flower_name, category_id, price, stock, color, description))
        conn.commit()
        conn.close()
        
        flash('✅ เพิ่มดอกไม้ใหม่สำเร็จ!', 'success')
        return redirect(url_for('index'))
    
    return render_template('index.html', categories=categories, page='add_flower')

# ============================================================
# Route: แก้ไขดอกไม้
# ============================================================
@app.route('/edit-flower/<int:flower_id>', methods=['GET', 'POST'])
def edit_flower(flower_id):
    """แก้ไขข้อมูลดอกไม้"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        flower_name = request.form['flower_name']
        category_id = request.form['category_id']
        price = request.form['price']
        stock = request.form['stock']
        color = request.form['color']
        description = request.form['description']
        
        if not all([flower_name, category_id, price, stock, color]):
            flash('⚠️ กรุณากรอกข้อมูลทั้งหมด', 'error')
            return redirect(url_for('edit_flower', flower_id=flower_id))
        
        cursor.execute('''
            UPDATE Flowers 
            SET flower_name=?, category_id=?, price=?, stock=?, color=?, description=?
            WHERE flower_id=?
        ''', (flower_name, category_id, price, stock, color, description, flower_id))
        conn.commit()
        conn.close()
        
        flash('✅ แก้ไขดอกไม้สำเร็จ!', 'success')
        return redirect(url_for('index'))
    
    # GET request - แสดงฟอร์มแก้ไข
    cursor.execute('SELECT * FROM Flowers WHERE flower_id=?', (flower_id,))
    flower = cursor.fetchone()
    
    cursor.execute('SELECT * FROM Categories ORDER BY category_name')
    categories = cursor.fetchall()
    conn.close()
    
    if not flower:
        flash('❌ ไม่พบดอกไม้ที่ต้องการแก้ไข', 'error')
        return redirect(url_for('index'))
    
    return render_template('index.html', flower=flower, categories=categories, page='edit_flower')

# ============================================================
# Route: ลบดอกไม้
# ============================================================
@app.route('/delete-flower/<int:flower_id>', methods=['POST'])
def delete_flower(flower_id):
    """ลบข้อมูลดอกไม้"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Flowers WHERE flower_id=?', (flower_id,))
    conn.commit()
    conn.close()
    
    flash('✅ ลบดอกไม้สำเร็จ!', 'success')
    return redirect(url_for('index'))

# ============================================================
# Route: เพิ่มหมวดหมู่ใหม่
# ============================================================
@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    """เพิ่มหมวดหมู่ใหม่"""
    if request.method == 'POST':
        category_name = request.form['category_name']
        description = request.form['description']
        
        if not category_name:
            flash('⚠️ กรุณากรอกชื่อหมวดหมู่', 'error')
            return redirect(url_for('add_category'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Categories (category_name, description)
            VALUES (?, ?)
        ''', (category_name, description))
        conn.commit()
        conn.close()
        
        flash('✅ เพิ่มหมวดหมู่ใหม่สำเร็จ!', 'success')
        return redirect(url_for('categories'))
    
    return render_template('index.html', page='add_category')

# ============================================================
# Route: แก้ไขหมวดหมู่
# ============================================================
@app.route('/edit-category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    """แก้ไขข้อมูลหมวดหมู่"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        category_name = request.form['category_name']
        description = request.form['description']
        
        if not category_name:
            flash('⚠️ กรุณากรอกชื่อหมวดหมู่', 'error')
            return redirect(url_for('edit_category', category_id=category_id))
        
        cursor.execute('''
            UPDATE Categories 
            SET category_name=?, description=?
            WHERE category_id=?
        ''', (category_name, description, category_id))
        conn.commit()
        conn.close()
        
        flash('✅ แก้ไขหมวดหมู่สำเร็จ!', 'success')
        return redirect(url_for('categories'))
    
    # GET request - แสดงฟอร์มแก้ไข
    cursor.execute('SELECT * FROM Categories WHERE category_id=?', (category_id,))
    category = cursor.fetchone()
    conn.close()
    
    if not category:
        flash('❌ ไม่พบหมวดหมู่ที่ต้องการแก้ไข', 'error')
        return redirect(url_for('categories'))
    
    return render_template('index.html', category=category, page='edit_category')

# ============================================================
# Route: ลบหมวดหมู่
# ============================================================
@app.route('/delete-category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    """ลบข้อมูลหมวดหมู่"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # ตรวจสอบว่ามีดอกไม้ใช้หมวดหมู่นี้หรือไม่
    cursor.execute('SELECT COUNT(*) as count FROM Flowers WHERE category_id=?', (category_id,))
    result = cursor.fetchone()
    
    if result['count'] > 0:
        flash('❌ ไม่สามารถลบหมวดหมู่ได้ เพราะมีดอกไม้ใช้หมวดหมู่นี้อยู่', 'error')
    else:
        cursor.execute('DELETE FROM Categories WHERE category_id=?', (category_id,))
        conn.commit()
        flash('✅ ลบหมวดหมู่สำเร็จ!', 'success')
    
    conn.close()
    return redirect(url_for('categories'))

# ============================================================
# เรียกใช้ Flask App
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("🌸 Ohm-Flower Store Management System")
    print("=" * 60)
    print("✓ ฐานข้อมูล: flowers_store.db")
    print("✓ เว็บไซต์: http://localhost:5000")
    print("✓ พิมพ์ Ctrl+C เพื่อหยุดเซิร์ฟเวอร์")
    print("=" * 60)
    app.run(debug=True)
