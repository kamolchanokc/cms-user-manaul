# -*- coding: utf-8 -*-
"""Sync the "รายละเอียดหลักสูตร" (หมวด 1–8) section between the two manual pages.

Source of truth : curriculum-form.md   (หน้าฉบับผู้จัดทำ — curate ละเอียดสุด)
Target          : add-curriculum.md    (ขั้นตอนที่ 3 ของหน้า "5. การเพิ่มหลักสูตรใหม่")

สคริปต์นี้จะคัดเนื้อหาตั้งแต่ย่อหน้าอินโทร ("กรอกข้อมูลรายละเอียดหลักสูตรผ่าน 8 หมวดหมู่หลัก")
ไปจนจบไฟล์ curriculum-form.md แล้วเอาไปแทนที่บล็อกเดียวกันใน add-curriculum.md
(ระหว่างอินโทร กับหัวข้อ "## ขั้นตอนที่ 4 — การส่งหลักสูตรเข้าสู่กระบวนการอนุมัติ")
โดยหัวข้อ "## ขั้นตอนที่ 3", ขั้นตอนที่ 4 และ 5 ของ add-curriculum.md จะไม่ถูกแตะ

การใช้งาน (รันจากที่ไหนก็ได้ — ใช้ path แบบ relative กับตัวสคริปต์):
    python scripts/sync_form_section.py           # sync (เขียนทับ add-curriculum.md)
    python scripts/sync_form_section.py --check    # ตรวจอย่างเดียว ไม่เขียน (exit 1 ถ้าไม่ตรง)

หมายเหตุ: แก้เนื้อหาหมวด 1–8 ที่ curriculum-form.md เสมอ แล้วรันสคริปต์นี้เพื่อ push ไป add-curriculum.md
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORM = os.path.join(REPO, "curriculum-form.md")
ADD = os.path.join(REPO, "add-curriculum.md")

# จุดเริ่มของบล็อกเนื้อหา (เหมือนกันทั้งสองไฟล์)
BODY_START = "กรอกข้อมูลรายละเอียดหลักสูตรผ่าน 8 หมวดหมู่หลัก"
# จุดสิ้นสุดใน add-curriculum.md (หัวข้อถัดไป ที่ต้องคงไว้)
ADD_END = "## ขั้นตอนที่ 4 — การส่งหลักสูตรเข้าสู่กระบวนการอนุมัติ"


def extract_form_body(form_text):
    i = form_text.find(BODY_START)
    if i == -1:
        raise SystemExit(f"[error] ไม่พบจุดเริ่มบล็อกใน curriculum-form.md: {BODY_START!r}")
    return form_text[i:].rstrip()


def extract_add_body(add_text):
    a1 = add_text.find(BODY_START)
    a2 = add_text.find(ADD_END)
    if a1 == -1:
        raise SystemExit(f"[error] ไม่พบจุดเริ่มบล็อกใน add-curriculum.md: {BODY_START!r}")
    if a2 == -1:
        raise SystemExit(f"[error] ไม่พบหัวข้อสิ้นสุดใน add-curriculum.md: {ADD_END!r}")
    if a1 >= a2:
        raise SystemExit("[error] ลำดับ anchor ใน add-curriculum.md ไม่ถูกต้อง")
    return a1, a2


def main():
    check_only = "--check" in sys.argv[1:]

    form_text = open(FORM, encoding="utf-8").read()
    add_text = open(ADD, encoding="utf-8").read()

    form_body = extract_form_body(form_text)
    a1, a2 = extract_add_body(add_text)
    current_add_body = add_text[a1:a2].rstrip()

    if current_add_body == form_body:
        print("[ok] สองไฟล์ตรงกันอยู่แล้ว (in sync)")
        return 0

    if check_only:
        print("[out-of-sync] add-curriculum.md ไม่ตรงกับ curriculum-form.md — รันโดยไม่ใส่ --check เพื่อ sync")
        return 1

    new_add = add_text[:a1] + form_body + "\n\n" + add_text[a2:]
    open(ADD, "w", encoding="utf-8").write(new_add)
    print(f"[synced] อัปเดต add-curriculum.md แล้ว ({len(form_body)} ตัวอักษร) จาก curriculum-form.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
