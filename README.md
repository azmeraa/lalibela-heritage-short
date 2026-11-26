# Lalibela: A Story Carved in Stone



An AI-generated bilingual heritage short about the rock-hewn churches of Lalibela, Ethiopia. The project demonstrates a Python-based creative AI production workflow combining AI-generated images, synthetic narration, original AI-generated music, subtitles, and FFmpeg video assembly.



## 1. Project overview



Film title: Lalibela: A Story Carved in Stone

Amharic title: ላሊበላ፡ በድንጋይ የተቀረፀ ታሪክ

Subject: The rock-hewn churches and living heritage of Lalibela, Ethiopia

Audience: International audiences interested in Ethiopian history, culture, and heritage

Languages: Amharic and English narration, with English subtitles

Duration: Approximately 89 seconds, including the end card



The story follows fictional international visitors discovering Lalibela's remarkable rock-hewn churches with the help of an Ethiopian guide.



## 2. Current project status



- Eight-shot storyboard created and validated against a JSON Schema.

- Eight AI-generated keyframe images created.

- Selective keyframe generation with caching and retry logic implemented.

- Amharic and English synthetic narration generated.

- Original AI-generated background music produced using ACE-Step 1.5.

- Narration and music mixed into a final audio track.

- English subtitles created.

- Eight moving-shot clips produced using FFmpeg pan-and-zoom effects.

- Horizontal 16:9 film assembled.

- Vertical 9:16 film assembled.

- AI-generated end card created.

- Radio cut produced for audience evaluation.

- Three audience feedback submissions collected.

- Technical and production documentation prepared.

- Python pipeline runner implemented for rebuilding the videos from existing production assets.

- Public GitHub repository created.



The final film exports and project report are available in `outputs/`.



## 3. Final outputs



| File | Description |

|---|---|

| `outputs/lalibela_horizontal.mp4` | Horizontal 16:9 film |

| `outputs/lalibela_vertical.mp4` | Vertical 9:16 film |

| `outputs/lalibela_radio_cut.mp4` | Radio cut with narration and background music (evaluation version) |

| `outputs/Lalibela_Final_Report.pdf` | Final project report |

| `outputs/audience_feedback.csv` | Collected audience feedback |



Both final film versions have an approximate duration of 89 seconds.



## 4. Technology and tools



- Python: Production scripts and pipeline coordination.

- JSON and JSON Schema: Structured storyboard and validation.

- Cloudflare Workers AI: FLUX.2 Klein image generation.

- Google Gemini API: Amharic and English text-to-speech.

- ACE-Step 1.5: AI-generated background music.

- Pillow: End-card and image processing.

- FFmpeg: Image animation, audio processing, subtitles, and video assembly.

- Git and GitHub: Version control and public project repository.



## 5. Project structure



```text

lalibela-heritage-short/

├── storyboard.json

├── storyboard.schema.json

├── requirements.txt

├── .env.example

├── .gitignore

├── run_pipeline.py

├── feedback_app.py

├── create_report_pdf.py

├── README.md

├── DESIGN.md

├── ARCHITECTURE.md

├── EXPERIMENTS.md

├── FAILURES.md

├── COSTS.md

├── ETHICS.md

├── FINAL_REPORT.md

├── config/

├── scripts/

│   ├── 01_validate_storyboard.py

│   ├── 02_test_gemini_tts.py

│   ├── 03_test_amharic_tts.py

│   ├── 04_prepare_narration.py

│   ├── 05_generate_narration.py

│   ├── 06_check_audio.py

│   ├── 07_assemble_narration_track.py

│   ├── 08_generate_test_image.py

│   ├── 09_generate_keyframes.py

│   ├── 10_check_images.py

│   ├── 11_fix_image_extensions.py

│   ├── 12_create_contact_sheet.py

│   ├── 13_create_end_card.py

│   ├── 14_create_moving_shots.py

│   ├── 15_assemble_horizontal.py

│   └── 15_assemble_vertical.py

├── assets/

│   ├── images/

│   ├── video/

│   ├── audio/

│   └── subtitles/

├── logs/

│   └── runs.jsonl

└── outputs/

&#x20;   ├── lalibela_horizontal.mp4

&#x20;   ├── lalibela_vertical.mp4

&#x20;   ├── lalibela_radio_cut.mp4

&#x20;   └── Lalibela_Final_Report.pdf

```



## 6. Installation



### Requirements



- Python 3.10 or newer.

- FFmpeg installed and accessible through PATH.

- API credentials for the AI services when running cloud-generation stages.



### Create a virtual environment



Windows:



```bat

python -m venv .venv

.venv\\Scripts\\activate

```



macOS/Linux:



```bash

python -m venv .venv

source .venv/bin/activate

```



### Install dependencies



```bash

python -m pip install -r requirements.txt

```



### Check FFmpeg



```bash

ffmpeg -version

```



If FFmpeg is installed but not available through PATH, configure its executable path using the `FFMPEG_PATH` environment variable.



## 7. Environment configuration



The repository includes `.env.example` as a template.



Create a local `.env` file in the project root and add your own API credentials:



```text

GEMINI_API_KEY=your_gemini_api_key

CLOUDFLARE_API_TOKEN=your_cloudflare_api_token

CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id

```



Never commit `.env` or expose API credentials in source code, screenshots, or public logs.



The `.env` file is excluded through `.gitignore`.



The existing generated images, narration, and music are included as project assets, so rebuilding the final videos does not require making new AI-generation API calls.



## 8. Storyboard validation



Run from the project root:



```bash

python scripts/01_validate_storyboard.py

```



The validation checks:



- JSON loading and JSON Schema compliance.

- Shot IDs and character references.

- Shot timing and timeline continuity.

- Prompts, narration, and subtitle references.



A successful validation confirms that the storyboard is ready for subsequent production stages.



## 9. Production workflow



The production workflow is divided into stages:



1. Develop and validate the structured storyboard.

2. Generate and review AI keyframe images.

3. Prepare and generate Amharic and English narration.

4. Generate original background music using ACE-Step 1.5.

5. Assemble and inspect narration audio.

6. Create moving shots using FFmpeg.

7. Add subtitles, background music, and the end card.

8. Export horizontal and vertical versions.



### One-command video rebuild



The project includes `run_pipeline.py`, which coordinates the video production stages using the generated assets included in the repository.



From the project root, run:



```bash

python run_pipeline.py

```



The runner:



- Validates the storyboard against its JSON Schema.

- Checks the required storyboard, keyframe, music, and audio assets.

- Prepares the English subtitles.

- Reuses the existing end-card image or creates it if missing.

- Creates or reuses the eight moving-shot clips.

- Assembles the horizontal film.

- Assembles the vertical film.



Valid existing video assets are reused to avoid unnecessary processing.



To intentionally rebuild the derived video outputs, run:



```bash

python run_pipeline.py --force

```



Important production limitation: The runner rebuilds the videos using the existing AI-generated assets. It does not automatically regenerate the AI keyframes, narration, or ACE-Step music. Music generation was performed separately using ACE-Step 1.5. The AI image and narration generation stages can be run independently when new assets are required.



The keyframe and narration generation scripts include caching and retry handling. The moving-shot and video assembly stages also reuse valid existing outputs where applicable.



FFmpeg must be installed and accessible through PATH, or configured using `FFMPEG_PATH`.



## 10. Experiment and run records



Production experiments and technical issues are documented in:



- `EXPERIMENTS.md`

- `FAILURES.md`

- `COSTS.md`



Model-generation records are stored in:



```text

logs/runs.jsonl

```



The log records model information, prompts or generation parameters, seeds where applicable, execution times, output files, status, and available cost information.



Unknown or unverified costs are recorded as unavailable rather than estimated.



## 11. Ethics and cultural responsibility



The visitors and guide are fictional AI-generated characters. Synthetic narration is used rather than recordings of real people.



The project aims to represent Lalibela respectfully and recognizes that AI-generated images may contain architectural inaccuracies. Generated visuals should not be treated as historical evidence.



The film includes an AI disclosure on its end card.



See `ETHICS.md` for further information about representation, AI disclosure, consent, and cultural responsibility.



## 12. Documentation



The repository includes:



- `DESIGN.md` — Design decisions, audience feedback, and resulting design considerations.

- `ARCHITECTURE.md` — Pipeline architecture and data flow.

- `EXPERIMENTS.md` — Production experiments and observations.

- `FAILURES.md` — Technical challenges and solutions.

- `COSTS.md` — Tools and cost considerations.

- `ETHICS.md` — Ethical considerations and limitations.

- `FINAL_REPORT.md` — Final project report and production reflections.



## 13. Future improvements



- Integrate automated AI music generation into the pipeline runner.

- Extend automated caching and retry handling across all applicable production stages.

- Improve automated model-call logging and cost tracking.

- Expand audience testing and incorporate additional viewer feedback.

- Improve automated quality checks for generated media and final exports.

- Improve visual accuracy and cultural representation through local heritage review.

- Explore more accurate AI-generated architectural imagery and multilingual subtitle options.



## 14. Audience feedback application



The project includes a Python-based audience feedback application (`feedback_app.py`) built with Tkinter.



### Features



- Plays the radio cut and final horizontal and vertical films.

- Collects viewer responses to six questions.

- Saves responses automatically in `outputs/audience_feedback.csv`.

- Displays a summary of submissions and viewer suggestions.

- Distinguishes software-test records from actual audience feedback.



### How to run



From the project root directory, activate the Python virtual environment and run:



```bash

python feedback_app.py

```



Select the film, enter a participant code, watch the video, answer the questions, and submit feedback.



The application uses Python's built-in Tkinter, CSV, and operating-system modules.



### Audience testing status



Audience feedback was collected from three participants:



- P01: Reviewed the near-final film and appreciated the bilingual Amharic and English narration and script. Suggested improving the relationship between the images and the Lalibela story, reducing subtitle size, and improving language presentation.

- P02: Reviewed the near-final film and understood the story's focus on the rock-hewn churches, living faith, Biete Giyorgis, and shared heritage. Suggested improving architectural accuracy, subtitle placement, and Amharic text rendering.

- P03: Reviewed the radio cut and understood the general story. Suggested improving narration clarity, translation flow, and considering additional language options.



P01 and P02 reviewed the near-final film, while P03 reviewed the radio cut. The three participants did not all review both versions.



The software test submission (`TEST001`) is separate from these actual audience feedback records.



The feedback and resulting design considerations are documented in `DESIGN.md` and `FINAL_REPORT.md`.



## 15. Repository



GitHub repository:

https://github.com/azmeraa/lalibela-heritage-short



The repository contains the project source code, storyboard, generated production assets, documentation, run records, and final video outputs.
