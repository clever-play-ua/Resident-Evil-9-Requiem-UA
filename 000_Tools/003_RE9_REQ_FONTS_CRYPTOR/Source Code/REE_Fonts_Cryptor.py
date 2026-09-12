"""
RE Engine Fonts Cryptor - Python/PyQt6 GUI Port
Original by Ekey (h4x0r) / 2021
Python port with GUI + TH/EN i18n

Requirements:
    pip install PyQt6

Usage:
    python REE_Fonts_Cryptor.py
"""

import sys
import os
import struct
from typing import Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QTextEdit, QProgressBar,
    QFrame, QScrollArea, QSizePolicy, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QPalette, QFont, QDragEnterEvent, QDropEvent, QPainter


# ─────────────────────────────────────────────
#  i18n Strings
# ─────────────────────────────────────────────

STRINGS = {
    "EN": {
        "window_title":        "RE Engine Fonts Cryptor",
        "app_title":           "RE ENGINE  FONTS  CRYPTOR",
        "ver_label":           "v2.0  Python Edition",
        "lang_btn":            "🌐  ภาษาไทย",
        # Drop zone
        "drop_main":           "Drop Fonts or Folders Here",
        "drop_release":        "Release to Process!",
        "drop_sub":            "Supports: .oft  .oft.1  .otf  .ttf  .ttc  |  or click Browse",
        # Buttons
        "btn_browse_files":    "📂  Browse Files",
        "btn_browse_folder":   "📁  Browse Folder",
        "btn_output_folder":   "💾  Output Folder",
        "btn_output_tooltip":  "Optional: Choose custom output directory",
        "btn_process":         "⚡  PROCESS ALL FILES",
        "btn_clear_log":       "Clear",
        "btn_clear_all":       "Clear All",
        # Labels
        "out_auto":            "Output: Same folder as source  (auto)",
        "out_custom":          "Output: {}",
        "ext_section":         "OUTPUT EXTENSION",
        "enc_ext_label":       "Encrypt output  (plain font → game)",
        "dec_ext_label":       "Decrypt output  (game → plain font)",
        "ext_auto_enc":        "Auto  (.ext + .1)",
        "ext_auto_dec":        "Auto  (strip .1)",
        "queue_label":         "QUEUE",
        "queue_count":         "{n} file(s) queued",
        "queue_empty":         "No files queued",
        "log_label":           "LOG",
        # Status / log messages
        "status_ready":        "Ready  —  drag fonts or folders to begin",
        "status_processing":   "Processing {cur}/{total}…",
        "status_done":         "Finished: {ok} OK, {err} error(s)",
        "log_ready":           "RE Engine Fonts Cryptor ready.",
        "log_supports":        "Supports: OTF (.oft), OTF packed (.oft.1), TTF (.ttf), TTC (.ttc)",
        "log_auto_detect":     "Auto-detects encrypt / decrypt from file magic bytes.",
        "log_added":           "Added {n} file(s) to queue.",
        "log_added_folder":    "Added {n} file(s) from folder.",
        "log_no_fonts_drop":   "[WARN] No recognisable font files found in dropped items.",
        "log_no_fonts_folder": "[WARN] No font files found in selected folder.",
        "log_queue_empty":     "[WARN] Queue is empty. Add files first.",
        "log_out_folder":      "Output folder set: {}",
        "log_starting":        "\nStarting — {n} file(s)…",
        "log_done":            "\n✔ Done — {ok} success, {err} error(s).",
        # Dialogs
        "dlg_files":           "Select Font Files",
        "dlg_folder":          "Select Folder",
        "dlg_output":          "Select Output Folder",
        "dlg_filter":          "Font Files (*.oft *.oft.1 *.ttf *.otf *.ttc);;All Files (*)",
    },
    "TH": {
        "window_title":        "RE Engine Fonts Cryptor",
        "app_title":           "RE ENGINE  FONTS  CRYPTOR",
        "ver_label":           "v2.0  Python Edition",
        "lang_btn":            "🌐  English",
        # Drop zone
        "drop_main":           "วางไฟล์ฟอนต์หรือโฟลเดอร์ที่นี่",
        "drop_release":        "ปล่อยเพื่อประมวลผล!",
        "drop_sub":            "รองรับ: .oft  .oft.1  .otf  .ttf  .ttc  |  หรือกด Browse",
        # Buttons
        "btn_browse_files":    "📂  เลือกไฟล์",
        "btn_browse_folder":   "📁  เลือกโฟลเดอร์",
        "btn_output_folder":   "💾  โฟลเดอร์ปลายทาง",
        "btn_output_tooltip":  "ไม่บังคับ: เลือกโฟลเดอร์สำหรับไฟล์ผลลัพธ์",
        "btn_process":         "⚡  ประมวลผลไฟล์ทั้งหมด",
        "btn_clear_log":       "ล้างล็อก",
        "btn_clear_all":       "ล้างทั้งหมด",
        # Labels
        "out_auto":            "ผลลัพธ์: โฟลเดอร์เดียวกับต้นฉบับ  (อัตโนมัติ)",
        "out_custom":          "ผลลัพธ์: {}",
        "ext_section":         "นามสกุลไฟล์ผลลัพธ์",
        "enc_ext_label":       "เข้ารหัส  (ฟอนต์ปกติ → ไฟล์เกม)",
        "dec_ext_label":       "ถอดรหัส  (ไฟล์เกม → ฟอนต์ปกติ)",
        "ext_auto_enc":        "อัตโนมัติ  (.ext + .1)",
        "ext_auto_dec":        "อัตโนมัติ  (ตัด .1 ออก)",
        "queue_label":         "คิวไฟล์",
        "queue_count":         "{n} ไฟล์ในคิว",
        "queue_empty":         "ยังไม่มีไฟล์ในคิว",
        "log_label":           "ล็อก",
        # Status / log messages
        "status_ready":        "พร้อมใช้งาน  —  ลากไฟล์หรือโฟลเดอร์มาวาง",
        "status_processing":   "กำลังประมวลผล {cur}/{total}…",
        "status_done":         "เสร็จสิ้น: สำเร็จ {ok} ไฟล์, ผิดพลาด {err} ไฟล์",
        "log_ready":           "RE Engine Fonts Cryptor พร้อมใช้งาน",
        "log_supports":        "รองรับ: OTF (.oft), OTF แพ็ก (.oft.1), TTF (.ttf), TTC (.ttc)",
        "log_auto_detect":     "ตรวจสอบการเข้า/ถอดรหัสอัตโนมัติจาก magic bytes",
        "log_added":           "เพิ่ม {n} ไฟล์เข้าคิวแล้ว",
        "log_added_folder":    "เพิ่ม {n} ไฟล์จากโฟลเดอร์เข้าคิวแล้ว",
        "log_no_fonts_drop":   "[เตือน] ไม่พบไฟล์ฟอนต์ที่รองรับในรายการที่วาง",
        "log_no_fonts_folder": "[เตือน] ไม่พบไฟล์ฟอนต์ในโฟลเดอร์ที่เลือก",
        "log_queue_empty":     "[เตือน] คิวว่างอยู่ กรุณาเพิ่มไฟล์ก่อน",
        "log_out_folder":      "ตั้งโฟลเดอร์ปลายทาง: {}",
        "log_starting":        "\nเริ่มประมวลผล — {n} ไฟล์…",
        "log_done":            "\n✔ เสร็จสิ้น — สำเร็จ {ok} ไฟล์, ผิดพลาด {err} ไฟล์",
        # Dialogs
        "dlg_files":           "เลือกไฟล์ฟอนต์",
        "dlg_folder":          "เลือกโฟลเดอร์",
        "dlg_output":          "เลือกโฟลเดอร์ปลายทาง",
        "dlg_filter":          "ไฟล์ฟอนต์ (*.oft *.oft.1 *.ttf *.otf *.ttc);;ทุกไฟล์ (*)",
    },
}


# ─────────────────────────────────────────────
#  Core Cipher Logic
# ─────────────────────────────────────────────

MAGIC_FBOF = 0x4F464246
MAGIC_OTTO = 0x4F54544F
MAGIC_TTCF = 0x66637474
MAGIC_TT1  = 0x00000100
DELTA: int = 0xAE6E39B58A355F45


def font_cipher(data: bytearray) -> bytearray:
    seed: int = 1
    size = len(data) & 0x3F
    if size > 0:
        for _ in range(size):
            seed = (2 * seed + 1) & 0xFFFFFFFFFFFFFFFF
    part1 = (DELTA >> size) & 0xFFFFFFFFFFFFFFFF
    part2 = ((seed & DELTA) << (64 - size)) & 0xFFFFFFFFFFFFFFFF
    key: int = (part1 | part2) & 0xFFFFFFFFFFFFFFFF
    key_bytes = key.to_bytes(8, byteorder='little')
    for i in range(len(data)):
        data[i] ^= key_bytes[i % 8]
    return data


def process_file(src: str, dst: str) -> tuple[bool, str]:
    try:
        with open(src, 'rb') as f:
            raw = f.read()
    except OSError as e:
        return False, f"Cannot read file: {e}"
    if len(raw) < 4:
        return False, "File too small (< 4 bytes)"
    magic = struct.unpack_from('<I', raw, 0)[0]
    if magic == MAGIC_FBOF:
        payload = bytearray(raw[4:])
        result = bytes(font_cipher(payload))
        mode = "Decrypt"
    elif magic in (MAGIC_OTTO, MAGIC_TTCF, MAGIC_TT1):
        payload = bytearray(raw)
        ciphered = bytes(font_cipher(payload))
        result = struct.pack('<I', MAGIC_FBOF) + ciphered
        mode = "Encrypt"
    else:
        return False, f"Unknown magic 0x{magic:08X}"
    try:
        os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
        with open(dst, 'wb') as f:
            f.write(result)
    except OSError as e:
        return False, f"Cannot write output: {e}"
    size_kb = len(result) / 1024
    return True, f"[{mode}] {os.path.basename(src)}  →  {os.path.basename(dst)}  ({size_kb:.1f} KB)"


def collect_font_files(paths: list[str]) -> list[str]:
    result = []
    font_exts = {'.oft', '.ttf', '.otf', '.ttc'}
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in files:
                    fp = os.path.join(root, f)
                    if any(f.endswith(ext) for ext in font_exts) or f.endswith('.1') or _looks_like_font(fp):
                        result.append(fp)
        elif os.path.isfile(p):
            result.append(p)
    return result


def _looks_like_font(path: str) -> bool:
    try:
        with open(path, 'rb') as f:
            data = f.read(4)
        if len(data) < 4:
            return False
        return struct.unpack_from('<I', data, 0)[0] in (MAGIC_FBOF, MAGIC_OTTO, MAGIC_TTCF, MAGIC_TT1)
    except Exception:
        return False


def make_output_path(src: str, chosen_ext: Optional[str] = None) -> str:
    if chosen_ext:
        base = src
        for compound in ('.otf.1', '.ttf.1', '.ttc.1', '.oft.1', '.1'):
            if base.endswith(compound):
                base = base[:-len(compound)]
                break
        else:
            base, _ = os.path.splitext(base)
        return base + chosen_ext
    try:
        with open(src, 'rb') as f:
            raw4 = f.read(4)
        magic = struct.unpack_from('<I', raw4, 0)[0] if len(raw4) >= 4 else 0
    except Exception:
        magic = 0
    if magic == MAGIC_FBOF:
        return src[:-2] if src.endswith('.1') else (lambda s, e: s + '.dec' + e)(*os.path.splitext(src))
    return src + '.1'


# ─────────────────────────────────────────────
#  Worker Thread
# ─────────────────────────────────────────────

class WorkerThread(QThread):
    progress = pyqtSignal(int, int)
    log      = pyqtSignal(str, str)
    done     = pyqtSignal(int, int)

    def __init__(self, file_pairs: list[tuple[str, str]]):
        super().__init__()
        self.file_pairs = file_pairs

    def run(self):
        ok_count = err_count = 0
        for i, (src, dst) in enumerate(self.file_pairs):
            self.progress.emit(i + 1, len(self.file_pairs))
            success, msg = process_file(src, dst)
            if success:
                ok_count += 1
                self.log.emit(msg, 'ok')
            else:
                err_count += 1
                self.log.emit(f"[ERROR] {os.path.basename(src)}: {msg}", 'err')
        self.done.emit(ok_count, err_count)


# ─────────────────────────────────────────────
#  Drop Zone
# ─────────────────────────────────────────────

class DropZone(QFrame):
    files_dropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setMinimumHeight(155)
        self._hover = False
        self._pulse = 0.0
        self._main_text = ""
        self._release_text = ""

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)

        self.icon_lbl = QLabel("⬇")
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f = QFont(); f.setPointSize(34)
        self.icon_lbl.setFont(f)
        self.icon_lbl.setStyleSheet("color: #00D4FF;")

        self.main_lbl = QLabel()
        self.main_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_lbl.setFont(QFont("Consolas", 13, QFont.Weight.Bold))
        self.main_lbl.setStyleSheet("color: #E0E0E0;")

        self.sub_lbl = QLabel()
        self.sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub_lbl.setStyleSheet("color: #888; font-size: 11px;")

        layout.addWidget(self.icon_lbl)
        layout.addWidget(self.main_lbl)
        layout.addWidget(self.sub_lbl)

        timer = QTimer(self)
        timer.timeout.connect(self._tick)
        timer.start(50)

    def set_texts(self, main: str, sub: str, release: str):
        self._main_text = main
        self._release_text = release
        self.main_lbl.setText(main)
        self.sub_lbl.setText(sub)

    def _tick(self):
        import math
        self._pulse = (self._pulse + 0.06) % (2 * 3.14159)
        self.update()

    def paintEvent(self, event):
        import math
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pulse_a = int(30 + 20 * math.sin(self._pulse))
        p.fillRect(self.rect(), QColor(0, 212, 255, 30 if self._hover else 10))
        pen = p.pen()
        pen.setColor(QColor(0, 212, 255, 180 if self._hover else pulse_a + 60))
        pen.setWidth(2)
        pen.setStyle(Qt.PenStyle.DashLine)
        p.setPen(pen)
        p.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 12, 12)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            self._hover = True
            self.main_lbl.setText(self._release_text)
            self.main_lbl.setStyleSheet("color: #00D4FF;")
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._hover = False
        self.main_lbl.setText(self._main_text)
        self.main_lbl.setStyleSheet("color: #E0E0E0;")

    def dropEvent(self, event: QDropEvent):
        self._hover = False
        self.main_lbl.setText(self._main_text)
        self.main_lbl.setStyleSheet("color: #E0E0E0;")
        paths = [url.toLocalFile() for url in event.mimeData().urls()]
        if paths:
            self.files_dropped.emit(paths)


# ─────────────────────────────────────────────
#  File List Widget
# ─────────────────────────────────────────────

class FileListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._files: list[str] = []
        self._lang = "EN"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        header = QHBoxLayout()
        self.count_lbl = QLabel()
        self.count_lbl.setStyleSheet("color: #888; font-size: 11px;")
        self.clear_btn = QPushButton()
        self.clear_btn.setFixedHeight(22)
        self.clear_btn.setStyleSheet("""
            QPushButton { background: transparent; color: #FF6B6B;
                border: 1px solid #FF6B6B; border-radius: 4px;
                padding: 0 8px; font-size: 11px; }
            QPushButton:hover { background: rgba(255,107,107,0.15); }
        """)
        self.clear_btn.clicked.connect(self.clear_all)
        header.addWidget(self.count_lbl)
        header.addStretch()
        header.addWidget(self.clear_btn)
        layout.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(135)
        scroll.setStyleSheet("""
            QScrollArea { border: 1px solid #333; border-radius: 6px; background: #1A1A2E; }
            QScrollBar:vertical { background: #1A1A2E; width: 8px; }
            QScrollBar::handle:vertical { background: #444; border-radius: 4px; }
        """)
        self.inner = QWidget()
        self.inner_layout = QVBoxLayout(self.inner)
        self.inner_layout.setContentsMargins(6, 6, 6, 6)
        self.inner_layout.setSpacing(2)
        self.inner_layout.addStretch()
        scroll.setWidget(self.inner)
        layout.addWidget(scroll)
        self._update_count()

    def set_lang(self, lang: str):
        self._lang = lang
        self.clear_btn.setText(STRINGS[lang]["btn_clear_all"])
        self._update_count()

    def add_files(self, files: list[str]):
        existing = set(self._files)
        for f in files:
            if f not in existing:
                self._files.append(f)
                self.inner_layout.insertWidget(self.inner_layout.count() - 1, self._make_row(f))
        self._update_count()

    def _make_row(self, filepath: str) -> QWidget:
        w = QWidget()
        w.setObjectName("fr")
        w.setStyleSheet("QWidget#fr{background:rgba(0,212,255,0.05);border-radius:4px;}QWidget#fr:hover{background:rgba(0,212,255,0.12);}")
        hl = QHBoxLayout(w)
        hl.setContentsMargins(8, 2, 4, 2)
        hl.setSpacing(6)
        icon = QLabel("📄"); icon.setFixedWidth(18)
        lbl = QLabel(os.path.basename(filepath))
        lbl.setToolTip(filepath)
        lbl.setStyleSheet("color:#CCC;font-size:11px;")
        lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        rm = QPushButton("✕")
        rm.setFixedSize(18, 18)
        rm.setStyleSheet("QPushButton{background:transparent;color:#666;border:none;font-size:10px;}QPushButton:hover{color:#FF6B6B;}")
        rm.clicked.connect(lambda: self._remove(filepath, w))
        hl.addWidget(icon); hl.addWidget(lbl); hl.addWidget(rm)
        return w

    def _remove(self, filepath: str, widget: QWidget):
        if filepath in self._files:
            self._files.remove(filepath)
        widget.deleteLater()
        self._update_count()

    def clear_all(self):
        self._files.clear()
        while self.inner_layout.count() > 1:
            item = self.inner_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._update_count()

    def _update_count(self):
        s = STRINGS[self._lang]
        n = len(self._files)
        self.count_lbl.setText(
            s["queue_count"].format(n=n) if n else s["queue_empty"]
        )

    def get_files(self) -> list[str]:
        return list(self._files)


# ─────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._lang = "EN"
        self._worker: Optional[WorkerThread] = None
        self._output_dir: Optional[str] = None
        self._startup_logged = False

        self.setMinimumSize(680, 740)
        self.resize(740, 790)
        self._apply_theme()
        self._build_ui()
        self._apply_lang()

    # ── Theme ──────────────────────────────────

    def _apply_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #0D0D1A; color: #E0E0E0;
                font-family: Consolas, 'Courier New', monospace;
            }
            QLabel { color: #E0E0E0; }
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #1A1A3E,stop:1 #0F0F2A);
                color: #00D4FF; border: 1px solid #00D4FF; border-radius: 6px;
                padding: 8px 20px; font-family: Consolas,monospace; font-size: 12px; font-weight: bold;
            }
            QPushButton:hover { background: rgba(0,212,255,0.15); border-color: #00FFFF; color: #00FFFF; }
            QPushButton:pressed { background: rgba(0,212,255,0.3); }
            QPushButton:disabled { border-color: #333; color: #444; background: #111; }
            QProgressBar { background:#1A1A2E; border:1px solid #333; border-radius:5px;
                height:12px; text-align:center; color:#888; font-size:10px; }
            QProgressBar::chunk { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #00D4FF,stop:1 #0080FF); border-radius:4px; }
            QTextEdit { background:#0A0A18; border:1px solid #1E1E3A; border-radius:6px;
                color:#CCC; font-family:Consolas,monospace; font-size:11px; }
            QScrollBar:vertical { background:#0D0D1A; width:8px; border-radius:4px; }
            QScrollBar::handle:vertical { background:#333; border-radius:4px; min-height:20px; }
            QScrollBar::handle:vertical:hover { background:#00D4FF; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }
        """)

    # ── UI Build ───────────────────────────────

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(20, 14, 20, 14)
        root.setSpacing(10)

        # Header
        hdr = QHBoxLayout()
        self.title_lbl = QLabel()
        self.title_lbl.setFont(QFont("Consolas", 15, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #00D4FF; letter-spacing: 2px;")
        self.ver_lbl = QLabel()
        self.ver_lbl.setStyleSheet("color: #555; font-size: 10px;")
        self.ver_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.lang_btn = QPushButton()
        self.lang_btn.setFixedSize(115, 30)
        self.lang_btn.setStyleSheet("""
            QPushButton { background:rgba(0,212,255,0.08); color:#00D4FF;
                border:1px solid #00D4FF; border-radius:6px;
                padding:0 8px; font-size:11px; font-weight:bold; }
            QPushButton:hover { background:rgba(0,212,255,0.2); }
        """)
        self.lang_btn.clicked.connect(self._toggle_lang)
        hdr.addWidget(self.title_lbl)
        hdr.addStretch()
        hdr.addWidget(self.ver_lbl)
        hdr.addSpacing(10)
        hdr.addWidget(self.lang_btn)
        root.addLayout(hdr)
        root.addWidget(self._sep())

        # Drop zone
        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self._on_drop)
        root.addWidget(self.drop_zone)

        # Browse buttons
        btn_row = QHBoxLayout(); btn_row.setSpacing(10)
        self.browse_files_btn = QPushButton(); self.browse_files_btn.clicked.connect(self._browse_files)
        self.browse_folder_btn = QPushButton(); self.browse_folder_btn.clicked.connect(self._browse_folder)
        self.out_folder_btn = QPushButton(); self.out_folder_btn.clicked.connect(self._browse_output)
        btn_row.addWidget(self.browse_files_btn)
        btn_row.addWidget(self.browse_folder_btn)
        btn_row.addWidget(self.out_folder_btn)
        root.addLayout(btn_row)

        self.out_folder_lbl = QLabel()
        self.out_folder_lbl.setStyleSheet("color: #666; font-size: 10px;")
        root.addWidget(self.out_folder_lbl)

        # Extension selector
        root.addWidget(self._sep())
        self.ext_section_lbl = QLabel()
        self.ext_section_lbl.setStyleSheet("color: #555; font-size: 10px; letter-spacing: 2px;")
        root.addWidget(self.ext_section_lbl)

        ext_row = QHBoxLayout(); ext_row.setSpacing(16)

        enc_col = QVBoxLayout(); enc_col.setSpacing(4)
        self.enc_ext_lbl = QLabel()
        self.enc_ext_lbl.setStyleSheet("color: #888; font-size: 11px;")
        self.enc_ext_combo = QComboBox()
        self.enc_ext_combo.setStyleSheet(self._combo_style())
        enc_col.addWidget(self.enc_ext_lbl); enc_col.addWidget(self.enc_ext_combo)

        dec_col = QVBoxLayout(); dec_col.setSpacing(4)
        self.dec_ext_lbl = QLabel()
        self.dec_ext_lbl.setStyleSheet("color: #888; font-size: 11px;")
        self.dec_ext_combo = QComboBox()
        self.dec_ext_combo.setStyleSheet(self._combo_style())
        dec_col.addWidget(self.dec_ext_lbl); dec_col.addWidget(self.dec_ext_combo)

        ext_row.addLayout(enc_col); ext_row.addLayout(dec_col)
        root.addLayout(ext_row)

        # Queue
        root.addWidget(self._sep())
        self.queue_lbl = QLabel()
        self.queue_lbl.setStyleSheet("color: #555; font-size: 10px; letter-spacing: 2px;")
        root.addWidget(self.queue_lbl)
        self.file_list = FileListWidget()
        root.addWidget(self.file_list)

        # Process button
        root.addWidget(self._sep())
        self.process_btn = QPushButton()
        self.process_btn.setMinimumHeight(44)
        self.process_btn.setStyleSheet("""
            QPushButton { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #001A2E,stop:1 #001E40);
                color:#00D4FF; border:2px solid #00D4FF; border-radius:8px;
                font-size:14px; font-weight:bold; letter-spacing:1px; }
            QPushButton:hover { background:rgba(0,212,255,0.2); color:#00FFFF; border-color:#00FFFF; }
            QPushButton:disabled { border-color:#333; color:#333; background:#111; }
        """)
        self.process_btn.clicked.connect(self._run_processing)
        root.addWidget(self.process_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        root.addWidget(self.progress_bar)

        # Log
        log_hdr = QHBoxLayout()
        self.log_section_lbl = QLabel()
        self.log_section_lbl.setStyleSheet("color: #555; font-size: 10px; letter-spacing: 2px;")
        self.clear_log_btn = QPushButton()
        self.clear_log_btn.setFixedHeight(22)
        self.clear_log_btn.setFixedWidth(90)
        self.clear_log_btn.setStyleSheet("""
            QPushButton { background:transparent; color:#666; border:1px solid #333;
                border-radius:4px; font-size:10px; padding:0; }
            QPushButton:hover { color:#CCC; border-color:#666; }
        """)
        self.clear_log_btn.clicked.connect(self.log_output.clear if hasattr(self, 'log_output') else lambda: None)
        log_hdr.addWidget(self.log_section_lbl); log_hdr.addStretch(); log_hdr.addWidget(self.clear_log_btn)
        root.addLayout(log_hdr)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setMinimumHeight(125)
        root.addWidget(self.log_output)

        # Fix clear log button connection now that log_output exists
        self.clear_log_btn.clicked.disconnect()
        self.clear_log_btn.clicked.connect(self.log_output.clear)

        self.statusBar().setStyleSheet("""
            QStatusBar { background:#0A0A18; border-top:1px solid #1E1E3A; color:#666; font-size:10px; }
        """)

    # ── Language ───────────────────────────────

    def _t(self, key: str) -> str:
        return STRINGS[self._lang][key]

    def _toggle_lang(self):
        self._lang = "TH" if self._lang == "EN" else "EN"
        self._apply_lang()

    def _apply_lang(self):
        s = STRINGS[self._lang]
        self.setWindowTitle(s["window_title"])
        self.title_lbl.setText(s["app_title"])
        self.ver_lbl.setText(s["ver_label"])
        self.lang_btn.setText(s["lang_btn"])

        self.drop_zone.set_texts(s["drop_main"], s["drop_sub"], s["drop_release"])

        self.browse_files_btn.setText(s["btn_browse_files"])
        self.browse_folder_btn.setText(s["btn_browse_folder"])
        self.out_folder_btn.setText(s["btn_output_folder"])
        self.out_folder_btn.setToolTip(s["btn_output_tooltip"])
        self.process_btn.setText(s["btn_process"])
        self.clear_log_btn.setText(s["btn_clear_log"])

        self.out_folder_lbl.setText(
            s["out_custom"].format(self._output_dir) if self._output_dir else s["out_auto"]
        )

        self.ext_section_lbl.setText(s["ext_section"])
        self.enc_ext_lbl.setText(s["enc_ext_label"])
        self.dec_ext_lbl.setText(s["dec_ext_label"])

        enc_idx = self.enc_ext_combo.currentIndex()
        dec_idx = self.dec_ext_combo.currentIndex()
        self.enc_ext_combo.clear()
        self.enc_ext_combo.addItems([s["ext_auto_enc"], ".otf.1", ".ttf.1", ".ttc.1", ".oft.1"])
        self.dec_ext_combo.clear()
        self.dec_ext_combo.addItems([s["ext_auto_dec"], ".otf", ".ttf", ".ttc", ".oft"])
        self.enc_ext_combo.setCurrentIndex(max(0, enc_idx))
        self.dec_ext_combo.setCurrentIndex(max(0, dec_idx))

        self.queue_lbl.setText(s["queue_label"])
        self.log_section_lbl.setText(s["log_label"])
        self.statusBar().showMessage(s["status_ready"])

        self.file_list.set_lang(self._lang)

    # ── Helpers ────────────────────────────────

    def _sep(self) -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #1E1E3A;")
        return line

    def _combo_style(self) -> str:
        return """
            QComboBox { background:#1A1A2E; color:#00D4FF; border:1px solid #00D4FF;
                border-radius:6px; padding:5px 10px;
                font-family:Consolas,monospace; font-size:12px; min-width:160px; }
            QComboBox:hover { border-color:#00FFFF; color:#00FFFF; }
            QComboBox::drop-down { border:none; width:24px; }
            QComboBox::down-arrow { image:none; border-left:5px solid transparent;
                border-right:5px solid transparent; border-top:6px solid #00D4FF;
                width:0; height:0; margin-right:6px; }
            QComboBox QAbstractItemView { background:#0D0D1A; color:#00D4FF;
                border:1px solid #00D4FF; selection-background-color:rgba(0,212,255,0.2);
                selection-color:#00FFFF; font-family:Consolas,monospace;
                font-size:12px; padding:4px; }
        """

    def _log(self, msg: str, level: str = "info"):
        colors = {"ok": "#00FF88", "err": "#FF6B6B", "warn": "#FFD700", "info": "#888888"}
        self.log_output.append(f'<span style="color:{colors.get(level,"#CCC")};">{msg}</span>')
        sb = self.log_output.verticalScrollBar()
        sb.setValue(sb.maximum())

    # ── Slots ──────────────────────────────────

    def showEvent(self, event):
        super().showEvent(event)
        if not self._startup_logged:
            self._startup_logged = True
            s = STRINGS[self._lang]
            self._log(s["log_ready"], "info")
            self._log(s["log_supports"], "info")
            self._log(s["log_auto_detect"], "info")

    def _on_drop(self, paths: list[str]):
        files = collect_font_files(paths)
        if not files:
            self._log(self._t("log_no_fonts_drop"), "warn"); return
        self.file_list.add_files(files)
        self._log(self._t("log_added").format(n=len(files)), "info")

    def _browse_files(self):
        s = STRINGS[self._lang]
        files, _ = QFileDialog.getOpenFileNames(self, s["dlg_files"], "", s["dlg_filter"])
        if files:
            self.file_list.add_files(files)
            self._log(s["log_added"].format(n=len(files)), "info")

    def _browse_folder(self):
        s = STRINGS[self._lang]
        folder = QFileDialog.getExistingDirectory(self, s["dlg_folder"])
        if folder:
            files = collect_font_files([folder])
            if files:
                self.file_list.add_files(files)
                self._log(s["log_added_folder"].format(n=len(files)), "info")
            else:
                self._log(s["log_no_fonts_folder"], "warn")

    def _browse_output(self):
        s = STRINGS[self._lang]
        folder = QFileDialog.getExistingDirectory(self, s["dlg_output"])
        if folder:
            self._output_dir = folder
            self.out_folder_lbl.setText(s["out_custom"].format(folder))
            self.out_folder_lbl.setStyleSheet("color: #00D4FF; font-size: 10px;")
            self._log(s["log_out_folder"].format(folder), "info")

    def _run_processing(self):
        s = STRINGS[self._lang]
        files = self.file_list.get_files()
        if not files:
            self._log(s["log_queue_empty"], "warn"); return

        enc_raw = self.enc_ext_combo.currentText()
        dec_raw = self.dec_ext_combo.currentText()
        enc_ext = None if enc_raw.startswith(("Auto", "อัตโนมัติ")) else enc_raw
        dec_ext = None if dec_raw.startswith(("Auto", "อัตโนมัติ")) else dec_raw

        pairs: list[tuple[str, str]] = []
        for src in files:
            try:
                with open(src, 'rb') as f:
                    raw4 = f.read(4)
                magic = struct.unpack_from('<I', raw4, 0)[0] if len(raw4) >= 4 else 0
            except Exception:
                magic = 0
            chosen = dec_ext if magic == MAGIC_FBOF else enc_ext
            dst_name = make_output_path(src, chosen)
            dst = os.path.join(self._output_dir, os.path.basename(dst_name)) if self._output_dir else dst_name
            pairs.append((src, dst))

        for btn in (self.process_btn, self.browse_files_btn, self.browse_folder_btn):
            btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(pairs))
        self.progress_bar.setValue(0)
        self._log(s["log_starting"].format(n=len(pairs)), "info")

        self._worker = WorkerThread(pairs)
        self._worker.progress.connect(self._on_progress)
        self._worker.log.connect(lambda m, lv: self._log(m, lv))
        self._worker.done.connect(self._on_done)
        self._worker.start()

    def _on_progress(self, current: int, total: int):
        s = STRINGS[self._lang]
        self.progress_bar.setValue(current)
        self.progress_bar.setFormat(f"{current} / {total}")
        self.statusBar().showMessage(s["status_processing"].format(cur=current, total=total))

    def _on_done(self, ok: int, err: int):
        s = STRINGS[self._lang]
        for btn in (self.process_btn, self.browse_files_btn, self.browse_folder_btn):
            btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self._log(s["log_done"].format(ok=ok, err=err), "ok" if err == 0 else "warn")
        self.statusBar().showMessage(s["status_done"].format(ok=ok, err=err))
        if err == 0:
            self.file_list.clear_all()


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("REE Fonts Cryptor")
    app.setStyle("Fusion")

    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window,          QColor(13, 13, 26))
    pal.setColor(QPalette.ColorRole.WindowText,      QColor(224, 224, 224))
    pal.setColor(QPalette.ColorRole.Base,            QColor(10, 10, 24))
    pal.setColor(QPalette.ColorRole.AlternateBase,   QColor(20, 20, 40))
    pal.setColor(QPalette.ColorRole.Text,            QColor(220, 220, 220))
    pal.setColor(QPalette.ColorRole.Button,          QColor(20, 20, 45))
    pal.setColor(QPalette.ColorRole.ButtonText,      QColor(0, 212, 255))
    app.setPalette(pal)

    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
