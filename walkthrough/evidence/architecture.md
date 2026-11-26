**# ARCHITECTURE.md**



**## 1. Project Overview**



**\*\*Project:\*\* Lalibela: A Story Carved in Stone**



**This project is an AI-assisted film production pipeline that transforms a structured storyboard into a short heritage documentary about Lalibela, Ethiopia.**



**The pipeline uses AI-generated images, AI-generated narration, original AI-generated music, and FFmpeg-based video editing to produce horizontal and vertical versions of the film.**



**## 2. Pipeline Architecture**



**The production process consists of five main stages:**



**1. \*\*Storyboard validation:\*\* The storyboard is loaded from `storyboard.json` and checked against `storyboard.schema.json`. Additional checks verify shot IDs, character references, timing, prompts, narration, and subtitles.**

**2. \*\*Keyframe generation:\*\* FLUX.2 Klein 4B through Cloudflare Workers AI generates visual keyframes from storyboard prompts.**

**3. \*\*Moving-shot generation:\*\* FFmpeg applies slow camera movements, including pan and zoom effects, to the generated images.**

**4. \*\*Music and narration:\*\* AI-generated narration is produced in Amharic and English. An original AI-generated music track is prepared and mixed with narration using FFmpeg audio processing.**

**5. \*\*Final assembly:\*\* FFmpeg combines the moving shots, subtitles, narration, music, and end card into the final film.**



**## 3. Main Technologies**



**| Technology | Purpose |**

**|---|---|**

**| Python | Pipeline orchestration and automation |**

**| JSON | Storyboard data and production configuration |**

**| JSON Schema | Storyboard validation |**

**| FLUX.2 Klein 4B | AI image generation |**

**| Cloudflare Workers AI | Image-generation access |**

**| Gemini 3.8 Flash TTS | Narration generation |**

**| ACE-Step 1.5 | Original music generation |**

**| FFmpeg | Video editing, motion effects, audio mixing, and encoding |**



**## 4. Project Structure**



**```text**

**lalibela-heritage-short/**

**│**

**├── assets/**

**│   ├── audio/**

**│   │   ├── music/**

**│   │   └── narration\_script.json**

**│   ├── images/**

**│   ├── subtitles/**

**│   └── video/**

**│       └── moving\_shots/**

**│**

**├── config/**

**├── logs/**

**│   └── runs.jsonl**

**│**

**├── outputs/**

**│   ├── lalibela\_horizontal.mp4**

**│   └── lalibela\_vertical.mp4**

**│**

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

**│**

**├── storyboard.json**

**├── storyboard.schema.json**

**├── README.md**

**├── DESIGN.md**

**├── ARCHITECTURE.md**

**├── requirements.txt**

**└── .gitignore**

**```**



**## 5. Data Flow**



**`storyboard.json` is the central source of production information. It defines the shots, visual prompts, motion prompts, characters, and timeline.**



**The generated keyframes become the inputs for moving-shot creation. The narration and music are processed separately and combined during final assembly.**



**English subtitles are added during video assembly. The horizontal version is used as the source for producing the vertical version.**



**## 6. Output Formats**



**The pipeline produces:**



**- Horizontal film: 1920 × 1080 (16:9).**

**- Vertical film: 1080 × 1920 (9:16).**

**- Duration: approximately 89 seconds, including the end card.**

**- Video encoding: H.264.**

**- Audio encoding: AAC.**



**## 7. Design Decisions**



**Wan 2.2 image-to-video generation was considered as an approach for creating moving footage. For this implementation, FFmpeg-based pan and zoom effects were selected as a practical alternative because they reduced technical complexity and allowed the project to be completed within the available time.**



**The storyboard remains separate from the production scripts so that creative decisions can be updated without manually rebuilding every production asset.**

**## Audience Feedback System**



**A Python-based audience feedback application was developed using Tkinter.**



**### Main features**



**- Plays the radio cut, horizontal film, and vertical film using the computer's default video player.**

**- Collects responses to six questions about story understanding, narration, background music, cultural learning, audience preferences, and suggested improvements.**

**- Saves submissions automatically to `outputs/audience\_feedback.csv`.**

**- Generates a feedback summary showing submission counts and viewer comments.**

**- Separates participant codes beginning with `TEST` from non-test records in the summary.**



**### Technical implementation**



**- Python**

**- Tkinter for the graphical user interface**

**- CSV for feedback storage**

**- Operating-system video playback through `os.startfile()`**



**### Current testing status**



**The application was launched successfully, video playback was checked, and a sample submission was saved and displayed in the summary.**



**The sample participant `TEST001` is a software test record, not a real audience participant. Actual audience testing with three viewers remains pending. The system is intended to support the collection and analysis of genuine viewer feedback.**
