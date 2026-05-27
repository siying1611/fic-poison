# `add_poison.py` — Functionality Overview

## Purpose

Inserts hidden junk text into HTML-formatted fan fiction files to make the content less useful for AI training purposes. Junk is hidden via CSS (using a configurable class name) so it is invisible to human readers but present in the raw HTML fed to scrapers/models.

---

## Command-Line Arguments

| Argument | Flag | Default | Description |
|---|---|---|---|
| `filename` | positional | — | Path to the input HTML file |
| `mode` | `-m` / `--mode` | `default` | Poisoning strategy: `tame` or `default` |
| `poison_class` | `-c` / `--class` | `poison` | CSS class name applied to junk elements |

---

## Word List

Before any poisoning, the script loads `popular.txt` (expected in the working directory), splitting it by newlines into a list of common words. These words are the source of all injected junk text.

> ⚠️ **Off-by-one bug:** `wordslen = len(words)` is used as the upper bound for `randint(0, wordslen)`. Since `randint` is inclusive on both ends, this can index one past the last element and raise an `IndexError`. It should be `wordslen - 1`.

---

## Modes

### `tame` Mode

Inserts a full paragraph of junk text **between every `</p>` tag** in the file.

**Steps:**
1. Reads the entire file into memory.
2. Splits the content on `</p>` to get a list of paragraph fragments.
3. Removes the final (empty) fragment left by the trailing `</p>`.
4. Warns the user if fewer than 4 paragraphs are found (suggesting `default` mode may be better).
5. For each paragraph fragment, appends the original `</p>` back, then injects a junk paragraph immediately after:
   ```html
   <p class="{poison_class}">{junk words...}</p>
   ```
6. The junk paragraph contains between **10 and 100** randomly selected words (chosen via `randint(10, 100)`).

---

### `default` Mode

Inserts single-word junk `<span>` elements **inline within the text** at random character intervals, while respecting HTML tag boundaries.

**Steps:**
1. Opens the file in UTF-8 text mode and reads it **one character at a time**.
2. Maintains two state variables:
   - `counting` (bool): whether the character interval counter is currently active.
   - `count` (int): characters remaining before the next junk insertion; initialized to `1`.
3. For each character read:
   - Appends it to the output string.
   - If the character is `<`, sets `counting = False` (pauses the countdown — inside an HTML tag).
   - If the character is `>`, sets `counting = True` (resumes the countdown — exited the HTML tag).
   - If `counting` is `True`, decrements `count` by 1.
   - If `count` drops to `0` or below, injects a junk span and resets `count` to a new random value:
     ```html
     <span class="{poison_class}">{single_word}</span>
     ```
     New interval: `randint(3, 30)` characters.
4. Because `count` starts at `1`, the **first junk span is inserted almost immediately** (after the first non-tag character).
5. Each junk span contains exactly **one** randomly selected word (unlike `tame` mode).

**Key property:** Junk spans are never inserted *inside* an existing HTML tag (e.g., `<p class="...">`) because the countdown is paused while `counting` is `False`.

---

## Output

The poisoned content is written to a new file in the **same directory** as the input, with `_poisoned` inserted before the `.txt` extension:

- Input: `my_fic.txt`
- Output: `my_fic_poisoned.txt`

> ⚠️ **Note:** The output filename replacement uses `.replace(".txt", "_poisoned.txt")`, which will silently produce a wrong filename if the input file does not have a `.txt` extension.

