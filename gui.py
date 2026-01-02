import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from tkinter.scrolledtext import ScrolledText
import threading
import os
import subprocess # FR-07: 결과 폴더 팝업을 위해 추가

from file_processor import process_files # file_processor.py와 같은 레벨에 있다고 가정

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("파일명 표준화 유틸리티")
        self.root.geometry("600x500") # GUI 크기 조정
        self.root.resizable(False, False) # 창 크기 조절 비활성화

        # 상단 프레임: 소스 폴더 선택
        top_frame = tk.Frame(root, padx=10, pady=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="소스 폴더:").pack(side=tk.LEFT, padx=(0, 10))
        self.source_dir_entry = tk.Entry(top_frame, width=60)
        self.source_dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        self.browse_button = tk.Button(top_frame, text="선택", command=self.browse_source_directory)
        self.browse_button.pack(side=tk.LEFT)

        # 중단 프레임: 로그 창
        log_frame = tk.Frame(root, padx=10, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(log_frame, text="처리 로그:").pack(anchor=tk.W)
        self.log_text = ScrolledText(log_frame, wrap=tk.WORD, height=15, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # 하단 프레임: 버튼 및 진행률
        bottom_frame = tk.Frame(root, padx=10, pady=10)
        bottom_frame.pack(fill=tk.X)

        self.run_button = tk.Button(bottom_frame, text="변환 시작", command=self.start_processing, width=15, height=2)
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))

        self.open_result_button = tk.Button(bottom_frame, text="결과 폴더 열기", command=self.open_result_folder, state=tk.DISABLED, width=15, height=2)
        self.open_result_button.pack(side=tk.LEFT)

        self.progress_label = tk.Label(bottom_frame, text="진행률: 0/0 (0%)")
        self.progress_label.pack(pady=(10, 0))
        self.progress = Progressbar(bottom_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(5, 0))
        
        self.status_message_label = tk.Label(bottom_frame, text="대기 중...", anchor=tk.W)
        self.status_message_label.pack(fill=tk.X, pady=(5, 0))

        self.result_dir = "" # 결과 폴더 경로 저장용

    def browse_source_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.source_dir_entry.delete(0, tk.END)
            self.source_dir_entry.insert(0, directory)
            self.update_status_log(f"소스 폴더 선택: {directory}")

    def start_processing(self):
        source_dir = self.source_dir_entry.get()
        if not source_dir:
            messagebox.showerror("오류", "소스 폴더를 선택해주세요.")
            return

        self.run_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        self.open_result_button.config(state=tk.DISABLED)
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        self.progress['value'] = 0
        self.progress_label.config(text="진행률: 0/0 (0%)")
        self.status_message_label.config(text="처리 시작...")
        
        self.result_dir = os.path.join(source_dir, "result") # 결과 폴더 경로 미리 저장

        # 별도의 스레드에서 파일 처리 함수 실행하여 GUI가 멈추지 않도록 함
        processing_thread = threading.Thread(target=self._run_processing, args=(source_dir,))
        processing_thread.start()

    def _run_processing(self, source_dir):
        """파일 처리 로직을 실행하고 GUI를 업데이트하는 헬퍼 함수."""
        try:
            process_files(source_dir, self.update_progress, self.update_status_log)
            self.update_status_log("모든 파일 처리 완료.")
            messagebox.showinfo("완료", "파일 처리 작업이 완료되었습니다.")
            self.open_result_button.config(state=tk.NORMAL) # 처리 완료 후 결과 폴더 열기 버튼 활성화
        except Exception as e:
            self.update_status_log(f"치명적인 오류 발생: {e}")
            messagebox.showerror("오류", f"파일 처리 중 치명적인 오류가 발생했습니다: {e}")
        finally:
            self.run_button.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.NORMAL)

    def update_progress(self, current, total):
        """진행률 바와 레이블을 업데이트합니다."""
        if total > 0:
            percentage = (current / total) * 100
            self.progress['value'] = percentage
            self.progress_label.config(text=f"진행률: {current}/{total} ({percentage:.1f}%)")
        else:
            self.progress['value'] = 0
            self.progress_label.config(text="진행률: 0/0 (0%)")
        self.root.update_idletasks() # GUI 즉시 업데이트

    def update_status_log(self, message):
        """로그 창과 상태 메시지 레이블을 업데이트합니다."""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END) # 스크롤을 항상 맨 아래로
        self.log_text.config(state='disabled')
        self.status_message_label.config(text=message)
        self.root.update_idletasks() # GUI 즉시 업데이트

    def open_result_folder(self):
        """FR-07: 결과 폴더를 팝업으로 엽니다."""
        if self.result_dir and os.path.isdir(self.result_dir):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(self.result_dir)
                elif os.name == 'posix':  # macOS or Linux
                    subprocess.Popen(['xdg-open', self.result_dir]) # Linux
                elif os.name == 'darwin': # macOS
                    subprocess.Popen(['open', self.result_dir])
                else:
                    messagebox.showwarning("경고", "지원하지 않는 운영체제입니다.")
            except Exception as e:
                messagebox.showerror("오류", f"결과 폴더를 여는 데 실패했습니다: {e}")
        else:
            messagebox.showwarning("경고", "처리된 결과 폴더를 찾을 수 없습니다.")
