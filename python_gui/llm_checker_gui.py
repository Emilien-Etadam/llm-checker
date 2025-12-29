"""
LLM Checker GUI - Standalone Windows Application
Detects hardware and recommends optimal Ollama models
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
from hardware_detector import HardwareDetector
from model_scorer import ModelScorer
from model_database import get_popular_models


class LLMCheckerGUI:
    """Main GUI application for LLM Checker"""

    def __init__(self, root):
        self.root = root
        self.root.title("LLM Checker - Ollama Model Recommender")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Initialize backend
        self.detector = HardwareDetector()
        self.scorer = ModelScorer()
        self.hardware = None
        self.recommendations = []

        # Color scheme
        self.bg_color = "#f0f0f0"
        self.header_bg = "#2c3e50"
        self.header_fg = "#ffffff"
        self.accent_color = "#3498db"

        self.root.configure(bg=self.bg_color)

        # Setup UI
        self.create_widgets()

        # Auto-detect on startup
        self.root.after(500, self.run_detection)

    def create_widgets(self):
        """Create all GUI widgets"""

        # Header
        header_frame = tk.Frame(self.root, bg=self.header_bg, height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🚀 LLM Checker - Ollama Model Recommender",
            font=("Arial", 18, "bold"),
            bg=self.header_bg,
            fg=self.header_fg
        )
        title_label.pack(pady=20)

        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Hardware Info Section
        hw_frame = tk.LabelFrame(
            main_container,
            text="💻 Hardware Detected",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        hw_frame.pack(fill=tk.X, pady=(0, 10))

        self.hw_text = scrolledtext.ScrolledText(
            hw_frame,
            height=6,
            font=("Consolas", 9),
            bg="#ffffff",
            fg="#000000",
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.hw_text.pack(fill=tk.X)

        # Recommendations Section
        rec_frame = tk.LabelFrame(
            main_container,
            text="⭐ Top 5 Recommended Models",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            padx=10,
            pady=10
        )
        rec_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.rec_text = scrolledtext.ScrolledText(
            rec_frame,
            font=("Consolas", 9),
            bg="#ffffff",
            fg="#000000",
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.rec_text.pack(fill=tk.BOTH, expand=True)

        # Control Panel
        control_frame = tk.Frame(main_container, bg=self.bg_color)
        control_frame.pack(fill=tk.X)

        # Use case selector
        use_case_label = tk.Label(
            control_frame,
            text="Use Case:",
            font=("Arial", 10),
            bg=self.bg_color
        )
        use_case_label.pack(side=tk.LEFT, padx=(0, 5))

        self.use_case_var = tk.StringVar(value="general")
        use_case_combo = ttk.Combobox(
            control_frame,
            textvariable=self.use_case_var,
            values=["general", "coding", "reasoning", "chat", "creative", "fast", "quality"],
            state="readonly",
            width=12,
            font=("Arial", 9)
        )
        use_case_combo.pack(side=tk.LEFT, padx=(0, 15))
        use_case_combo.bind("<<ComboboxSelected>>", lambda e: self.run_detection())

        # Refresh button
        self.refresh_btn = tk.Button(
            control_frame,
            text="🔄 Refresh Detection",
            command=self.run_detection,
            font=("Arial", 10, "bold"),
            bg=self.accent_color,
            fg="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(
            control_frame,
            text="Ready",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="#555555"
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # Footer
        footer_label = tk.Label(
            self.root,
            text="Made with Python • Powered by Ollama",
            font=("Arial", 8),
            bg=self.bg_color,
            fg="#888888"
        )
        footer_label.pack(side=tk.BOTTOM, pady=5)

    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def run_detection(self):
        """Run hardware detection and model scoring in background thread"""
        # Disable button during detection
        self.refresh_btn.config(state=tk.DISABLED)
        self.update_status("Detecting hardware...")

        # Run in thread to avoid freezing GUI
        thread = threading.Thread(target=self._detect_and_score, daemon=True)
        thread.start()

    def _detect_and_score(self):
        """Worker function for detection and scoring"""
        try:
            # Clear cache to force fresh detection
            self.detector.cache = None

            # Detect hardware
            self.hardware = self.detector.detect()

            # Update GUI with hardware info
            self.root.after(0, self.display_hardware_info)

            # Get use case
            use_case = self.use_case_var.get()

            # Score models
            self.root.after(0, lambda: self.update_status(f"Scoring models for {use_case}..."))
            models = get_popular_models()
            self.recommendations = self.scorer.score_models(
                models,
                self.hardware,
                use_case=use_case,
                limit=5
            )

            # Update GUI with recommendations
            self.root.after(0, self.display_recommendations)

            # Done
            self.root.after(0, lambda: self.update_status(f"✅ Found {len(self.recommendations)} compatible models"))

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("Detection Error", error_msg))
            self.root.after(0, lambda: self.update_status("❌ Detection failed"))

        finally:
            # Re-enable button
            self.root.after(0, lambda: self.refresh_btn.config(state=tk.NORMAL))

    def display_hardware_info(self):
        """Display hardware information"""
        if not self.hardware:
            return

        summary = self.hardware['summary']
        backend = self.hardware['backend']
        cpu = self.hardware['cpu']
        mem = self.hardware['memory']

        # Build display text
        lines = []
        lines.append(f"═══════════════════════════════════════════════════════════════")
        lines.append(f"Hardware Summary")
        lines.append(f"═══════════════════════════════════════════════════════════════")
        lines.append(f"System: {summary['description']}")
        lines.append(f"Tier: {self.hardware['tier']}")
        lines.append(f"Backend: {backend['name']} ({backend['type']})")
        lines.append(f"Max Model Size: {summary['max_model_size_gb']:.1f} GB")
        lines.append(f"Speed Coefficient: {summary['speed_coefficient']:.0f}")
        lines.append(f"")
        lines.append(f"CPU: {cpu['brand']}")
        lines.append(f"  Cores: {cpu['cores_physical']} physical, {cpu['cores_logical']} logical")
        lines.append(f"  SIMD: {cpu['simd']}")
        lines.append(f"")
        lines.append(f"Memory: {mem['total_gb']:.1f} GB total, {mem['available_gb']:.1f} GB available")

        if backend['type'] in ['cuda', 'rocm', 'intel']:
            lines.append(f"")
            lines.append(f"GPU: {backend['gpu_name']}")
            lines.append(f"  VRAM: {backend['vram_gb']:.1f} GB")

        # Update text widget
        self.hw_text.config(state=tk.NORMAL)
        self.hw_text.delete(1.0, tk.END)
        self.hw_text.insert(1.0, "\n".join(lines))
        self.hw_text.config(state=tk.DISABLED)

    def display_recommendations(self):
        """Display model recommendations"""
        if not self.recommendations:
            self.rec_text.config(state=tk.NORMAL)
            self.rec_text.delete(1.0, tk.END)
            self.rec_text.insert(1.0, "No compatible models found.\n\nYour system may have limited resources.")
            self.rec_text.config(state=tk.DISABLED)
            return

        # Build display text
        lines = []
        lines.append(f"═══════════════════════════════════════════════════════════════")
        lines.append(f"Top 5 Models for '{self.use_case_var.get()}' Use Case")
        lines.append(f"═══════════════════════════════════════════════════════════════\n")

        for i, rec in enumerate(self.recommendations, 1):
            model = rec['model']
            scores = rec['scores']

            lines.append(f"{i}. {model['name']}")
            lines.append(f"   ───────────────────────────────────────────────────────────")
            lines.append(f"   Family: {model['family']} | Params: {model['params_b']:.1f}B | Size: {model['size_gb']:.1f} GB")
            lines.append(f"   Quantization: {model['quantization']} | Context: {model['context_length']:,} tokens")
            lines.append(f"")
            lines.append(f"   📊 Scores:")
            lines.append(f"      • Overall: {scores['final']:.0f}/100 ⭐")
            lines.append(f"      • Quality: {scores['quality']:.0f}/100")
            lines.append(f"      • Speed: {scores['speed']:.0f}/100 (~{rec['estimated_tps']:.1f} tokens/sec)")
            lines.append(f"      • Fit: {scores['fit']:.0f}/100")
            lines.append(f"      • Context: {scores['context']:.0f}/100")
            lines.append(f"")
            lines.append(f"   💻 To install:")
            lines.append(f"      ollama pull {model['name']}")
            lines.append(f"")

        lines.append(f"═══════════════════════════════════════════════════════════════")
        lines.append(f"💡 Tip: Run 'ollama pull <model-name>' to download any model")
        lines.append(f"    Visit https://ollama.ai for more information")

        # Update text widget
        self.rec_text.config(state=tk.NORMAL)
        self.rec_text.delete(1.0, tk.END)
        self.rec_text.insert(1.0, "\n".join(lines))
        self.rec_text.config(state=tk.DISABLED)


def main():
    """Main entry point"""
    try:
        root = tk.Tk()
        app = LLMCheckerGUI(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
