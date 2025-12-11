# Manim: How to Run Any Scene and Make It "Pop Up"

This is a quick reference for running Manim scenes so that a video is actually rendered and opened.

---

## 1. Activate your environment (if you use one)

From the project folder:

```bash
source manim-ce-env/bin/activate
# or whatever your env is called
```

If you don’t use a virtualenv, you can skip this.

---

## 2. General command pattern

Run this **from the project root**, where your `scenes/` (or similar) folder lives:

```bash
manim [OPTIONS] path/to/file.py SceneClassName
```

Examples:

```bash
# Low quality, fast preview, auto-open video
manim -pql scenes/demo_latex.py SimpleDemo

# High quality, auto-open video
manim -pqh scenes/demo_latex.py SimpleDemo

# If your file is in another folder
manim -pql other_folder/my_scene.py MyScene
```

If the `manim` command is **not found**, use Python to run it as a module:

```bash
python -m manim -pql scenes/demo_latex.py SimpleDemo
```

---

## 3. What the common options mean

- `-p`  = **preview**: open the rendered video automatically when done.
- `-qk` = **quality**: `l` = low, `m` = medium, `h` = high, `k` = 4K.
  - `-pql` = preview + low quality (good for testing)
  - `-pqh` = preview + high quality (nicer final video)

You can combine them however you like, e.g. `-pm` or `-pqh`.

---

## 4. Rules that must be true for any scene

- The file must contain a class that **inherits from** `Scene` (or a subclass):

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        self.play(Create(Circle()))
        self.wait()
```

- When you run Manim, the last argument must be **exactly the class name**:

```bash
manim -pql scenes/my_scene.py MyScene
```

---

## 5. Where the output video goes

- Manim creates a `media/` folder next to your project files.
- Videos are stored like this:

```text
media/videos/<python_file_name_without_.py>/<resolution>/<SceneClassName>.mp4
```

Even if the `-p` preview doesn’t open, you can always manually open the `.mp4` from this folder.
