# SPDX-License-Identifier: GPL-3.0-or-later
"""EMO Thai community UI extension for IngeTrazo (preview)."""
from PySide6.QtCore import QTimer, QSettings, Qt, QModelIndex
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QWidget, QMenu, QGroupBox,
    QAbstractButton, QLabel, QTabWidget, QDockWidget, QComboBox,
    QTreeWidget, QTableWidget, QListWidget)
import re

WORDS = {
    "File":"ไฟล์","Edit":"แก้ไข","View":"มุมมอง","Tools":"เครื่องมือ",
    "Window":"หน้าต่าง","Extensions":"ส่วนเสริม","Help":"ช่วยเหลือ",
    "Language":"ภาษา","English":"อังกฤษ","Properties":"คุณสมบัติ",
    "Browser":"ตัวจัดการโมเดล","AI":"ปัญญาประดิษฐ์","Render":"เรนเดอร์",
    "Solid Inspector":"ตรวจสอบวัตถุตัน","Entity info":"ข้อมูลวัตถุ",
    "Nothing selected":"ยังไม่ได้เลือกวัตถุ","Name":"ชื่อ",
    "Visible":"แสดง","Lock":"ล็อก","Layers":"ชั้นข้อมูล",
    "Layer":"ชั้นข้อมูล","Layer 0":"ชั้นข้อมูล 0",
    "+ Layer":"+ เพิ่มชั้นข้อมูล","Purge":"ล้างรายการที่ไม่ใช้",
    "Assign selection":"กำหนดให้วัตถุที่เลือก","Scenes":"ฉาก",
    "Scene":"ฉาก","+ Scene":"+ เพิ่มฉาก","Update":"อัปเดต",
    "Materials":"วัสดุ","Material":"วัสดุ","Library":"คลังวัสดุ",
    "In model":"ในโมเดล","Colors":"สี","Brick":"อิฐ",
    "Concrete":"คอนกรีต","Stone":"หิน","Wall":"ผนัง",
    "Wood":"ไม้","Roofing":"วัสดุมุงหลังคา",
    "Edit texture":"แก้ไขพื้นผิว","Active:":"กำลังใช้งาน:",
    "Select":"เลือก","Line":"เส้นตรง","Rectangle":"สี่เหลี่ยม",
    "Circle":"วงกลม","Arc":"ส่วนโค้ง","Move":"ย้าย",
    "Rotate":"หมุน","Scale":"ปรับขนาด","Push/Pull":"ดัน/ดึง",
    "Offset":"สร้างเส้นขนาน","Eraser":"ยางลบ",
    "Orbit":"หมุนมุมมอง","Pan":"เลื่อนมุมมอง","Zoom":"ซูม",
    "Open":"เปิด","Save":"บันทึก","Cancel":"ยกเลิก",
    "Close":"ปิด","Apply":"นำไปใช้","Search":"ค้นหา",
    "Filter":"กรอง","Texture":"พื้นผิว","Floor":"พื้น",
    "Door":"ประตู","Window":"หน้าต่าง","Glass":"กระจก",
    "Metal":"โลหะ","Fabric":"ผ้า","Tiles":"กระเบื้อง",
    "Furniture":"เฟอร์นิเจอร์","Bathroom":"ห้องน้ำ",
    "Kitchen":"ห้องครัว","Bedroom":"ห้องนอน",
    "Settings":"ตั้งค่า","Preferences":"การตั้งค่า",
    "Import":"นำเข้า","Export":"ส่งออก","Undo":"ย้อนกลับ",
    "Redo":"ทำซ้ำ","Copy":"คัดลอก","Paste":"วาง",
    "Delete":"ลบ","Hide":"ซ่อน","Show":"แสดง",
    "Double-click a scene to show it":"ดับเบิลคลิกฉากเพื่อแสดง",
    "Terrain profile":"รูปตัดภูมิประเทศ","Clear screen":"ล้างหน้าจอ",
    "Sidebar":"แถบด้านข้าง","Units...":"หน่วย...",
}
def enabled():
    return str(QSettings().value("language","en")) == "th"

def tr(value):
    if not enabled() or not isinstance(value,str):
        return value
    plain=value.replace("&","").strip()
    match=re.fullmatch(r"(.+?)\s*\((\d+)\)",plain)
    translated=WORDS.get(plain)
    if translated is None and match:
        base=WORDS.get(match.group(1))
        if base:
            translated=f"{base} ({match.group(2)})"
    if translated is None:
        return value
    return ("&" if "&" in value else "")+translated

def refresh():
    if not enabled():
        return
    app=QApplication.instance()
    if app is None:
        return
    for top in app.topLevelWidgets():
        for action in top.findChildren(QAction):
            if action.data()=="emo-thai":
                continue
            original=action.text()
            translated=tr(original)
            if translated!=original:
                action.setText(translated)
        for w in [top]+top.findChildren(QWidget):
            if isinstance(w,QGroupBox):
                old=w.title(); new=tr(old)
                if old!=new: w.setTitle(new)
            if isinstance(w,(QAbstractButton,QLabel)):
                old=w.text(); new=tr(old)
                if old!=new: w.setText(new)
            if isinstance(w,QTabWidget):
                for i in range(w.count()):
                    old=w.tabText(i); new=tr(old)
                    if old!=new: w.setTabText(i,new)
            if isinstance(w,QDockWidget):
                old=w.windowTitle(); new=tr(old)
                if old!=new: w.setWindowTitle(new)
            if isinstance(w,QComboBox):
                for i in range(w.count()):
                    old=w.itemText(i); new=tr(old)
                    if old!=new: w.setItemText(i,new)
            if isinstance(w,(QTreeWidget,QListWidget,QTableWidget)):
                model=w.model()
                if model is None: continue
                def visit(parent,depth=0):
                    if depth>12:return
                    for row in range(min(model.rowCount(parent),500)):
                        for col in range(min(model.columnCount(parent),8)):
                            idx=model.index(row,col,parent)
                            old=model.data(idx,Qt.ItemDataRole.DisplayRole)
                            if isinstance(old,str):
                                # Translate only known UI terms, not freeform model names.
                                new=tr(old)
                                if new!=old:
                                    try:model.setData(idx,new,Qt.ItemDataRole.DisplayRole)
                                    except (TypeError,RuntimeError):pass
                            if col==0 and model.hasChildren(idx):
                                visit(idx,depth+1)
                visit(QModelIndex())

def add_language(window):
    for menu in window.findChildren(QMenu):
        label=(menu.title() or "").replace("&","").strip().lower()
        if label not in ("language","ภาษา","idioma","langue","sprache"):
            continue
        if any(a.data()=="emo-thai" for a in menu.actions()):
            return
        action=QAction("ไทย (Thai)",menu)
        action.setData("emo-thai")
        action.setCheckable(True)
        action.setChecked(enabled())
        for other in menu.actions():
            group=other.actionGroup()
            if group is not None and other.isCheckable():
                group.addAction(action);break
        menu.addAction(action)
        def choose():
            QSettings().setValue("language","th")
            try:
                from core import i18n
                i18n.LANGUAGE_NAMES["th"]="ไทย (Thai)"
                i18n.set_language("th")
                i18n._catalog.update(WORDS)
            except ImportError:
                pass
            refresh()
        action.triggered.connect(choose)
        return

def setup(app):
    from core import i18n
    i18n.LANGUAGE_NAMES["th"]="ไทย (Thai)"
    if enabled():
        i18n.set_language("th")
        i18n._catalog.update(WORDS)
    window=app.window
    add_language(window)
    for menu in window.findChildren(QMenu):
        menu.aboutToShow.connect(lambda: (add_language(window),refresh()))
    timer=QTimer(window)
    timer.timeout.connect(refresh)
    timer.start(2500)
    window._emo_thai_timer=timer
    QTimer.singleShot(0,refresh)
