# scripts/ — เครื่องมือดูแลคู่มือ

> โฟลเดอร์นี้ไม่ได้อยู่ใน `SUMMARY.md` จึงไม่ถูกเผยแพร่บน GitBook (เป็นเครื่องมือสำหรับผู้ดูแลเท่านั้น)

## `sync_form_section.py`

ทำให้เนื้อหาส่วน **"รายละเอียดหลักสูตร" (หมวด 1–8)** ตรงกันระหว่าง 2 หน้า:

- **ต้นฉบับ (source of truth):** `curriculum-form.md`
- **ปลายทาง:** `add-curriculum.md` (ขั้นตอนที่ 3)

**วิธีใช้** (ต้องมี Python 3):

```bash
python scripts/sync_form_section.py           # sync: คัดเนื้อหาจาก curriculum-form.md ไปทับใน add-curriculum.md
python scripts/sync_form_section.py --check    # ตรวจอย่างเดียว (exit 1 ถ้าไม่ตรง) — เหมาะกับใช้ใน CI/ก่อน commit
```

**ขั้นตอนแก้เนื้อหาหมวด 1–8:** แก้ที่ `curriculum-form.md` เสมอ → รัน `python scripts/sync_form_section.py` → commit ทั้งสองไฟล์
"""
