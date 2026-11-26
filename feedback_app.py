
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "outputs")
FEEDBACK_FILE = os.path.join(OUTPUT_DIR, "audience_feedback.csv")

VIDEOS = {
    "Radio Cut": "lalibela_radio_cut.mp4",
    "Horizontal Film": "lalibela_horizontal.mp4",
    "Vertical Film": "lalibela_vertical.mp4"
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

questions = [
    "1. What did you understand about Lalibela from this film?",
    "2. Was the narration clear and easy to understand?",
    "3. Was the background music comfortable?",
    "4. What did you learn about Lalibela's heritage and culture?",
    "5. What did you like most?",
    "6. What would you suggest improving?"
]


class FeedbackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lalibela Heritage Short - Audience Feedback")
        self.root.geometry("900x850")

        tk.Label(
            root,
            text="Lalibela: A Story Carved in Stone",
            font=("Arial", 19, "bold")
        ).pack(pady=12)

        tk.Label(
            root,
            text="Audience Feedback and Evaluation System",
            font=("Arial", 12)
        ).pack()

        video_frame = ttk.LabelFrame(root, text="Watch the film")
        video_frame.pack(fill="x", padx=20, pady=12)

        for label in VIDEOS:
            ttk.Button(
                video_frame,
                text="Play " + label,
                command=lambda name=label: self.play_video(name)
            ).pack(side="left", padx=10, pady=12)

        self.video_choice = tk.StringVar(value="Radio Cut")

        choice_frame = ttk.LabelFrame(root, text="Which film are you reviewing?")
        choice_frame.pack(fill="x", padx=20, pady=5)

        for label in VIDEOS:
            ttk.Radiobutton(
                choice_frame, text=label,
                variable=self.video_choice, value=label
            ).pack(side="left", padx=10, pady=8)

        participant_frame = ttk.LabelFrame(root, text="Viewer information")
        participant_frame.pack(fill="x", padx=20, pady=8)

        tk.Label(
            participant_frame,
            text="Participant code (do not enter your full name):"
        ).pack(anchor="w", padx=10, pady=5)

        self.participant = tk.StringVar()

        ttk.Entry(
            participant_frame,
            textvariable=self.participant,
            width=35
        ).pack(anchor="w", padx=10, pady=5)

        self.answers = []

        for question in questions:
            frame = ttk.LabelFrame(root, text=question)
            frame.pack(fill="x", padx=20, pady=4)

            answer = tk.Text(frame, height=2, width=90, wrap="word")
            answer.pack(fill="x", padx=8, pady=4)
            self.answers.append(answer)

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=12)

        ttk.Button(
            button_frame, text="Submit Feedback",
            command=self.submit
        ).pack(side="left", padx=8)

        ttk.Button(
            button_frame, text="Clear Form",
            command=self.clear
        ).pack(side="left", padx=8)

        ttk.Button(
            button_frame, text="View Feedback Summary",
            command=self.show_summary
        ).pack(side="left", padx=8)

        tk.Label(
            root,
            text="Please provide honest feedback. Do not enter private personal information.",
            font=("Arial", 9)
        ).pack(pady=5)

    def play_video(self, name):
        video_path = os.path.join(OUTPUT_DIR, VIDEOS[name])

        if not os.path.exists(video_path):
            messagebox.showerror("Video not found", video_path)
            return

        try:
            os.startfile(video_path)
        except Exception as error:
            messagebox.showerror("Playback error", str(error))

    def submit(self):
        participant = self.participant.get().strip()
        responses = [
            answer.get("1.0", "end").strip()
            for answer in self.answers
        ]

        if not participant:
            messagebox.showwarning("Missing information",
                                   "Please enter a participant code.")
            return

        if not any(responses):
            messagebox.showwarning("Missing feedback",
                                   "Please answer at least one question.")
            return

        file_exists = os.path.exists(FEEDBACK_FILE)

        with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Date and Time", "Participant Code", "Film", *questions
                ])

            writer.writerow([
                datetime.now().isoformat(timespec="seconds"),
                participant, self.video_choice.get(), *responses
            ])

        messagebox.showinfo("Thank you", "Feedback saved successfully.")
        self.clear()

    def clear(self):
        self.participant.set("")
        for answer in self.answers:
            answer.delete("1.0", "end")

    def show_summary(self):
        if not os.path.exists(FEEDBACK_FILE):
            messagebox.showinfo("No feedback", "No feedback has been submitted yet.")
            return

        with open(FEEDBACK_FILE, "r", newline="", encoding="utf-8-sig") as file:
            rows = list(csv.DictReader(file))

        if not rows:
            messagebox.showinfo("No feedback", "The feedback file is empty.")
            return

        actual = [
            row for row in rows
            if not row.get("Participant Code", "").strip().upper().startswith("TEST")
        ]
        tests = len(rows) - len(actual)

        summary = tk.Toplevel(self.root)
        summary.title("Audience Feedback Summary")
        summary.geometry("750x650")

        tk.Label(
            summary, text="Feedback Summary",
            font=("Arial", 18, "bold")
        ).pack(pady=12)

        tk.Label(
            summary,
            text=f"Total submissions: {len(rows)}   |   "
                 f"Test records: {tests}   |   "
                 f"Non-test records: {len(actual)}",
            font=("Arial", 11)
        ).pack(pady=5)

        counts = {}
        for row in actual:
            film = row.get("Film", "Unknown")
            counts[film] = counts.get(film, 0) + 1

        tk.Label(
            summary, text="Non-test submissions by film:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=15, pady=8)

        for film, count in counts.items():
            tk.Label(
                summary, text=f"{film}: {count}"
            ).pack(anchor="w", padx=25)

        tk.Label(
            summary, text="Viewer feedback and suggestions:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=15, pady=10)

        comments = tk.Text(summary, wrap="word", width=85, height=23)
        comments.pack(fill="both", expand=True, padx=15, pady=5)

        if not actual:
            comments.insert("end", "No non-test viewer responses yet.\n")
        else:
            for index, row in enumerate(actual, start=1):
                comments.insert(
                    "end",
                    f"\nVIEWER {index} — {row.get('Film', '')}\n"
                )
                comments.insert(
                    "end",
                    f"Liked most: {row.get(questions[4], '')}\n"
                )
                comments.insert(
                    "end",
                    f"Suggested improvement: {row.get(questions[5], '')}\n"
                )
                comments.insert("end", "-" * 60 + "\n")

        comments.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = FeedbackApp(root)
    root.mainloop()
