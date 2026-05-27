Read the procedures under the logic branch elif mode == "default". From my understanding, it is doing the following:

1. Read byte by byte for from the file referred to by the variable `filename`
2. It adds span of junk at random intervals determined by `count = randint(3, 30)`.
3. The random junk added has the format of `f"<span class=\"{poison_class}\">{junk}</span>"`

Let me know if I missed anything.

---

Next I want to work with you to generalize the function to not just english writing, but also chinese writings.

First of all, build a function like this:

`def is_chinese(text:str): -> bool`: Given a text file, detect whether it is in Chinese or not (specifically).

---

Next, write a Standalone function which takes in a string. It keeps everything enclosed by `<` and `>` intact, but adds random characters (junk) at random intervals in the text. The junk should be in Chinese if the input string is detected as Chinese, and in English otherwise. The function should return the modified string.

---

Now I switch to the new environment `fic_poison_test`. Write a pytest module to test the function `add_poison`, using the input `fanfic_sample_eng.txt` and input arguments `mode="default"` and `poison_class="poison"`. The test should check that the output string contains the expected junk format, and that the junk is in English.