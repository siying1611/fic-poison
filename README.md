# Fic Poisoner

A small script that injects random, garbage words into an Ao3 fic, or any piece of HTML-formatted text.  Junk text uses HTML classes that can be hidden with CSS.

### Preparing your fic

Always keep a backup of your unpoisoned fic, in case you need to revert or make changes later.

Go to Ao3's skins page.  Either create a new work skin, or edit the skin currently being used for your fic.  Add this section of code to the skin:

```
#workskin .poison {
  display: none;
}
```

Go to your fic's edit page.  Make sure that the work skin you just edited is selected for your fic in the Associations section.  Scroll down to the Work Text section, and ensure that the HTML option is selected, *not* Rich Text.  Copy the entire work or chapter, and paste it into a text document on your computer.  Save the document somewhere you can easily find it again.

If you're copy and pasting a new work from another source, you can paste into the Rich Text editor and then switch to HTML, to allow Ao3 to automatically format your text.

### Poisoning

Run `add_poison.py` with the options listed below.  A poisoned copy will be made in the same folder as the original.

Run options:

- `filepath`: Required, the path to the file with your HTML-formatted fic.
- `-m`, `--mode`: Optional, which mode to use.  `default` mode inserts single words randomly throughout the text.  `tame` mode adds one paragraph of junk text in between each normal paragraph.
- `-c`, `--class`: Optional, name of the class to be used.  Defaults to `poison`.  Remember to update your Ao3 work skin if you change this.

### Updating/publishing your fic

Copy the text from the newly generated file back into the HTML editor.  Remember to preview your fic to make sure that everything is working correctly before updating or publishing.

You should also add an author's note letting readers know that native Ao3 downloads won't work correctly, and they should instead save the page through their browser if they want to read offline.  AI scrapers aren't likely to bother checking the author's notes for every fic they scrape, so it should be safe to explain to your readers.

#### Thanks to dolph for the word list from [their GitHub](https://github.com/dolph/dictionary)