**# Lalibela: A Story Carved in Stone**



**An AI-generated bilingual heritage short about the rock-hewn churches of Lalibela, Ethiopia. The project demonstrates a Python-based creative AI production workflow combining AI-generated images, synthetic narration, original AI-generated music, subtitles, and FFmpeg video assembly.**



**## 1. Project overview**



**\*\*Film title:\*\* Lalibela: A Story Carved in Stone**  

**\*\*Amharic title:\*\* ላሊበላ፡ በድንጋይ የተቀረፀ ታሪክ**  

**\*\*Subject:\*\* The rock-hewn churches and living heritage of Lalibela, Ethiopia**  

**\*\*Audience:\*\* International audiences interested in Ethiopian history, culture, and heritage**  

**\*\*Languages:\*\* Amharic and English narration, with English subtitles**  

**\*\*Duration:\*\* 89 seconds, including the end card**



**The story follows fictional international visitors discovering Lalibela's remarkable rock-hewn churches with the help of an Ethiopian guide.**



**## 2. Current project status**



**- Eight-shot storyboard created and validated against a JSON Schema.**

**- Eight AI-generated keyframe images created.**

**- Selective keyframe generation with caching and retry logic implemented.**

**- Amharic and English synthetic narration generated.**

**- Original AI-generated background music produced.**

**- Narration and music mixed.**

**- English subtitles created.**

**- Eight moving-shot clips produced using FFmpeg pan-and-zoom effects.**

**- Horizontal 16:9 film assembled.**

**- Vertical 9:16 film assembled.**

**- AI-generated end card created.**

**- Technical and production documentation prepared.**



**The final film exports are available in `outputs/`.**



**\*\*Remaining work:\*\* Audience testing, final documentation updates, repository publication, and Assignment 2 submission materials.**



**## 3. Final outputs**



**| File | Description |**

**|---|---|**

**| `outputs/lalibela\_horizontal.mp4` | Horizontal 16:9 film |**

**| `outputs/lalibela\_vertical.mp4` | Vertical 9:16 film |**



**Both versions have an approximate duration of 89 seconds.**



**## 4. Technology and tools**



**- \*\*Python:\*\* Production scripts and pipeline coordination.**

**- \*\*JSON and JSON Schema:\*\* Structured storyboard and validation.**

**- \*\*Cloudflare Workers AI:\*\* FLUX.2 Klein image generation.**

**- \*\*Google Gemini API:\*\* Amharic and English text-to-speech.**

**- \*\*ACE-Step 1.5:\*\* AI-generated background music.**

**- \*\*Pillow:\*\* End-card and image processing.**

**- \*\*FFmpeg:\*\* Image animation, audio mixing, subtitles, and video assembly.**



**## 5. Project structure**



**```text**

**lalibela-heritage-short/**

**├── storyboard.json**

**├── storyboard.schema.json**

**├── requirements.txt**

**├── .gitignore**

**├── README.md**

**├── DESIGN.md**

**├── ARCHITECTURE.md**

**├── EXPERIMENTS.md**

**├── FAILURES.md**

**├── COSTS.md**

**├── ETHICS.md**

**├── config/**

**├── scripts/**

**│   ├── 01\_validate\_storyboard.py**

**│   ├── 02\_test\_gemini\_tts.py**

**│   ├── 03\_test\_amharic\_tts.py**

**│   ├── 04\_prepare\_narration.py**

**│   ├── 05\_generate\_narration.py**

**│   ├── 06\_check\_audio.py**

**│   ├── 07\_assemble\_narration\_track.py**

**│   ├── 08\_generate\_test\_image.py**

**│   ├── 09\_generate\_keyframes.py**

**│   ├── 10\_check\_images.py**

**│   ├── 11\_fix\_image\_extensions.py**

**│   ├── 12\_create\_contact\_sheet.py**

**│   ├── 13\_create\_end\_card.py**

**│   ├── 14\_create\_moving\_shots.py**

**│   └── 15\_assemble\_horizontal.py**

**├── assets/**

**│   ├── images/**

**│   ├── video/**

**│   ├── audio/**

**│   └── subtitles/**

**├── logs/**

**│   └── runs.jsonl**

**└── outputs/**

&#x20;   **├── lalibela\_horizontal.mp4**

&#x20;   **└── lalibela\_vertical.mp4**

**```**



**## 6. Installation**



**Requirements:**



**- Python 3.10 or newer.**

**- FFmpeg installed and accessible to the production scripts.**

**- API credentials for the AI services when running cloud-generation stages.**



**Create and activate a virtual environment.**



**\*\*Windows:\*\***



**```bat**

**python -m venv .venv**

**.venv\\Scripts\\activate**

**```**



**\*\*macOS/Linux:\*\***



**```bash**

**python -m venv .venv**

**source .venv/bin/activate**

**```**



**Install Python dependencies:**



**```bash**

**python -m pip install -r requirements.txt**

**```**



**Check FFmpeg:**



**```bash**

**ffmpeg -version**

**```**



**Some scripts may require the FFmpeg executable path to be configured for your operating system.**



**## 7. Environment configuration**



**Create a local `.env` file in the project root.**



**Configure the following variables using your own API credentials:**



**```text**

**CLOUDFLARE\_ACCOUNT\_ID=your\_cloudflare\_account\_id**

**CLOUDFLARE\_API\_TOKEN=your\_cloudflare\_api\_token**

**GEMINI\_API\_KEY=your\_gemini\_api\_key**

**```**



**Never commit `.env` or expose API credentials in source code, screenshots, or public logs.**



**## 8. Storyboard validation**



**Run from the project root:**



**```bash**

**python scripts/01\_validate\_storyboard.py**

**```**



**The validation checks:**



**- JSON loading and JSON Schema compliance.**

**- Shot IDs and character references.**

**- Shot timing and timeline continuity.**

**- Prompts, narration, and subtitle references.**



**A successful validation confirms that the storyboard is ready for subsequent production stages.**



**## 9. Production workflow**



**The production workflow is divided into stages:**



**1. Develop and validate the structured storyboard.**

**2. Generate and review keyframe images.**

**3. Prepare and generate narration.**

**4. Generate background music.**

**5. Assemble and inspect the narration audio.**

**6. Create moving shots using FFmpeg.**

**7. Add subtitles, music, and the end card.**

**8. Export horizontal and vertical versions.**



**The keyframe script includes selective regeneration, cache checks, and retry handling. Unchanged keyframes can be reused when their generation parameters match a successful run record.**



**The music-generation stage was performed separately using ACE-Step 1.5. The current project is a staged production workflow; a complete one-command regeneration from a clean clone is not yet implemented.**



**## 10. Experiment and run records**



**Production experiments and technical issues are documented in:**



**- `EXPERIMENTS.md`**

**- `FAILURES.md`**

**- `COSTS.md`**



**Model-generation records are stored in:**



**```text**

**logs/runs.jsonl**

**```**



**The log records model information, prompts, parameters, execution times, output files, and available cost information. Unknown or unverified costs are recorded as unavailable rather than estimated.**



**## 11. Ethics and cultural responsibility**



**The visitors and guide are fictional AI-generated characters. Synthetic narration is used rather than recordings of real people.**



**The project aims to represent Lalibela respectfully and recognizes that AI-generated images may contain architectural inaccuracies. Generated visuals should not be treated as historical evidence.**



**See `ETHICS.md` for further information about representation, AI disclosure, consent, and cultural responsibility.**



**## 12. Documentation**



**The repository includes:**



**- `DESIGN.md` — Design decisions, audience feedback, and changes.**

**- `ARCHITECTURE.md` — Pipeline architecture and data flow.**

**- `EXPERIMENTS.md` — Production experiments and observations.**

**- `FAILURES.md` — Technical challenges and solutions.**

**- `COSTS.md` — Tools and cost considerations.**

**- `ETHICS.md` — Ethical considerations and limitations.**



**## 13. Future improvements**



**- Implement a complete one-command pipeline for clean-clone regeneration.**

**- Extend caching and retry handling across all applicable production stages.**

**- Improve automated model-call logging and cost tracking.**

**- Complete audience testing and document the resulting design changes.**

**- Improve automated quality checks for generated media and final exports.**

**## Audience Feedback Application**



**The project includes a Python-based audience feedback application (`feedback\_app.py`) built with Tkinter.**



**### Features**



**- Plays the radio cut and final horizontal and vertical films.**

**- Collects viewer responses to six questions.**

**- Saves responses automatically in `outputs/audience\_feedback.csv`.**

**- Displays a summary of submissions and viewer suggestions.**

**- Distinguishes software-test records from non-test records in the summary.**



**### How to run**



**From the project root directory, activate the Python virtual environment and run:**



**```cmd**

**python feedback\_app.py**

**```**



**Select the film, enter a participant code, watch the video, answer the questions, and submit feedback.**



**The application uses Python's built-in Tkinter, CSV, and operating-system modules.**



**### Testing status**



**The application has been tested locally with a sample submission (`TEST001`). This is a software test, not actual audience feedback. Testing with at least three real viewers remains pending, and no audience-test results are claimed yet.**

