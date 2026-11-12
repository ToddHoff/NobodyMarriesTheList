# Nobody Marries the List: the "hand flat" pass. Items for claude/review-hand-flat.md.
# Last updated: Tuesday, November 10, 2026, 10:25 PM PST
#
# Todd, November 10, 10:18 PM: "Hand flat is an aiism. Cut or replace". 10:21 PM: "yes" to a pass on the rest.
# Each item: (number, chapter file, kind, old, new, note). kind is "cut" (the word "flat" comes out and
# nothing else changes), "replace" (reworded) or "keep" (Claude would leave it; new is None).
# old is the exact text in the chapter file and occurs once in that file. APPLIED November 10, 10:39 PM (Todd: "all"); the check below now reports every old as gone.
#
# Run:  python3 review-hand-flat-items.py <manuscript folder>           checks every old against the files
#       python3 review-hand-flat-items.py <manuscript folder> --md      prints the review as markdown

ITEMS = [
    (1, "chapter-01-jo.md", "cut", "laid his hand flat on the top of my head", "laid his hand on the top of my head", "the first night, marking her height"),
    (2, "chapter-05-jo.md", "cut", "put my hand flat on his back, between the shoulders", "put my hand on his back, between the shoulders", ""),
    (3, "chapter-07-jo.md", "cut", "He had one hand flat on the oak", "He had one hand on the oak", "holding the hutch upright"),
    (4, "chapter-07-jo.md", "cut", "I put my hand flat on his chest. I told myself", "I put my hand on his chest. I told myself", "the hallway; ch 9's line points back to it"),
    (5, "chapter-08-cal.md", "cut", "laid my hand flat on top of her head", "laid my hand on top of her head", ""),
    (6, "chapter-09-jo.md", "cut", "I kept my hand flat on his chest.", "I kept my hand on his chest.", "at the kiss"),
    (7, "chapter-10-cal.md", "cut", "her hand flat on my chest, and that she had", "her hand on my chest, and that she had", ""),
    (8, "chapter-11-jo.md", "cut", "I laid my hand flat on the top of his head.", "I laid my hand on the top of his head.", "measuring Owen"),
    (9, "chapter-15-jo.md", "cut", "put my hand flat on it anyway", "put my hand on it anyway", ""),
    (10, "chapter-16-cal.md", "cut", "with one hand flat on top of her head", "with one hand on top of her head", "holding her hair in the wind"),
    (11, "chapter-17-jo.md", "replace", "You put your hand flat and leave it.", "You lay your hand on it and leave it.", "Mrs. Hollis's rule for the loving tree; the character sheet has it as \"Lay your hand on the old oak\""),
    (12, "chapter-17-jo.md", "cut", "I put my palm flat on it.", "I put my palm on it.", "related form: palm flat"),
    (13, "chapter-17-jo.md", "cut", "He put his hand flat beside mine.", "He put his hand beside mine.", ""),
    (14, "chapter-17-jo.md", "cut", "our hands still flat on the loving tree", "our hands still on the loving tree", "related form"),
    (15, "chapter-18-cal.md", "cut", "put a flat hand on his head", "put a hand on his head", "related form: flat hand"),
    (16, "chapter-18-cal.md", "cut", "She put her hand flat on my chest, where she had put it on a curb", "She put her hand on my chest, where she had put it on a curb", ""),
    (17, "chapter-18-cal.md", "cut", "and her hand flat on my chest. Her fingers", "and her hand on my chest. Her fingers", ""),
    (18, "chapter-19-jo.md", "cut", "Owen had both hands flat on the window.", "Owen had both hands on the window.", ""),
    (19, "chapter-19-jo.md", "cut", "I had my hand flat on my own chest.", "I had my hand on my own chest.", ""),
    (20, "chapter-19-jo.md", "cut", "put my hand flat on Cal's back", "put my hand on Cal's back", "at the rim"),
    (21, "chapter-20-cal.md", "replace", "I put my hand flat on the table and kept it there.", "I put my whole hand down on the table and kept it there.", "he has been tapping with one finger, so the whole hand is the point"),
    (22, "chapter-20-cal.md", "replace", "I kept my hand flat until the quarter was over.", "I kept my hand down until the quarter was over.", "goes with 21"),
    (23, "chapter-20-cal.md", "cut", "She had put her hand flat on my back and left it there.", "She had put her hand on my back and left it there.", ""),
    (24, "chapter-20-cal.md", "replace", "Jo put her flat hand out at him.", "Jo held her palm out at him.", "related form; the stop signal to Pancake before \"Stay.\""),
    (25, "chapter-20-cal.md", "cut", "Jo put her hand flat on his head. I wrote it.", "Jo put her hand on his head. I wrote it.", ""),
    (26, "chapter-21-jo.md", "cut", "I put my hand flat on his back, where it had been at the rim.", "I put my hand on his back, where it had been at the rim.", ""),
    (27, "chapter-22-cal.md", "cut", "Jo's hand flat on my back", "Jo's hand on my back", ""),
    (28, "chapter-25-jo.md", "cut", "with one hand flat on my tailgate", "with one hand on my tailgate", ""),
    (29, "chapter-26-cal.md", "replace", "Jo put her hand flat on one as she went by.", "Jo touched one as she went by.", "the next sentence is \"Then she stopped and put her hand on the next one\", so a plain cut would say \"put her hand on\" twice"),
    (30, "chapter-26-cal.md", "cut", "I put my hand flat on the rock beside her.", "I put my hand on the rock beside her.", ""),
    (31, "chapter-26-cal.md", "cut", "Then she put her hand flat on my chest, on my shirt", "Then she put her hand on my chest, on my shirt", ""),
    (32, "chapter-27-jo.md", "replace", "He put his hands flat on the seat of the chair", "He put both hands on the seat of the chair", "Frank lifting himself for the cushion"),
    (33, "chapter-27-jo.md", "keep", "Then I held a treat out on my flat hand.", None, "related form; this is how you feed a dog you are afraid of, and she was bitten"),
    (34, "chapter-27-jo.md", "replace", "put his hand flat on the back seat and then on the dash", "felt the back seat and then the dash", "he is checking how hot the car is for Pancake"),
    (35, "chapter-27-jo.md", "replace", "His hand went flat on his knee and stayed there.", "His hand went to his knee and stayed there.", "related form; the man with the phone at the fire pit"),
    (36, "chapter-27-jo.md", "cut", "put it flat on my back, between my shoulders", "put it on my back, between my shoulders", "related form"),
    (37, "chapter-27-jo.md", "cut", "Then I put my hand flat on his chest, where I'd put it on the rock.", "Then I put my hand on his chest, where I'd put it on the rock.", ""),
    (38, "chapter-28-cal.md", "cut", "I put my free hand flat on the stone.", "I put my free hand on the stone.", ""),
    (39, "chapter-28-cal.md", "cut", "with his hand flat on top of it.", "with his hand on top of it.", "Owen at the post"),
    (40, "chapter-28-cal.md", "replace", "with my hands flat on it until 10:06", "with both hands on it until 10:06", ""),
    (41, "chapter-29-jo.md", "cut", "I wanted my hand flat on his chest", "I wanted my hand on his chest", ""),
    (42, "chapter-30-cal.md", "keep", "I held my hand out flat, at about the height of her head, and waited.", None, "related form; a level hand is how you offer to measure someone"),
    (43, "chapter-30-cal.md", "cut", "I put my hand flat on the top of her head. Jo's hand had been flat on Owen's.", "I put my hand on the top of her head. Jo's hand had been on Owen's.", "two in one line"),
    (44, "chapter-31-jo.md", "cut", "I put my hand flat over the glass.", "I put my hand over the glass.", "the sea glass on its chain"),
    (45, "chapter-32-cal.md", "cut", "I put my hand flat on the hall table", "I put my hand on the hall table", ""),
    (46, "chapter-32-cal.md", "cut", "I had a hand flat on his side.", "I had a hand on his side.", "Pancake at the vet's"),
    (47, "chapter-32-cal.md", "cut", "with her hands flat on her knees", "with her hands on her knees", ""),
    (48, "chapter-33-jo.md", "cut", "on the counter and put my hand flat on it.", "on the counter and put my hand on it.", ""),
    (49, "chapter-33-jo.md", "cut", "She put her hand flat on the pad", "She put her hand on the pad", "Denise"),
    (50, "chapter-34-cal.md", "cut", "She put her hand flat on the top pad and pressed.", "She put her hand on the top pad and pressed.", "the piano under the pads"),
    (51, "chapter-34-cal.md", "cut", "with a hand flat on the top.", "with a hand on the top.", "\"Jo's flat against the face of it, guiding\" earlier in the paragraph stays; there flat is the work"),
    (52, "chapter-34-cal.md", "cut", "had their hands flat on the top of it", "had their hands on the top of it", ""),
    (53, "chapter-34-cal.md", "cut", "She put her hand flat on the paneling beside her.", "She put her hand on the paneling beside her.", ""),
    (54, "chapter-35-jo.md", "keep", "gave it to Pancake off my flat hand.", None, "related form; same reason as 33"),
    (55, "chapter-35-jo.md", "cut", "He had his hands flat on the table on either side of the card.", "He had his hands on the table on either side of the card.", ""),
    (56, "chapter-35-jo.md", "cut", "put his hand flat over it.", "put his hand over it.", "the card in his shirt pocket"),
    (57, "chapter-35-jo.md", "cut", "both my hands flat on his chest", "both my hands on his chest", ""),
    (58, "chapter-35-jo.md", "cut", "I had my hand flat on Cal's chest.", "I had my hand on Cal's chest.", "the next sentence already has \"under my palm\""),
    (59, "chapter-36-cal.md", "cut", "He put his hand flat on his stomach.", "He put his hand on his stomach.", "Owen, sick"),
    (60, "chapter-36-cal.md", "cut", "I put both hands flat on her table to keep them there.", "I put both hands on her table to keep them there.", ""),
    (61, "chapter-38-cal.md", "cut", "Stephanie put her hand flat on top of Abby's head", "Stephanie put her hand on top of Abby's head", ""),
]


def check(folder):
    import os
    bad = 0
    for n, f, kind, old, new, note in ITEMS:
        text = open(os.path.join(folder, f), encoding="utf-8").read()
        c = text.count(old)
        if c != 1:
            bad += 1
            print(f"item {n}: {f}: found {c} times: {old!r}")
    print(f"{len(ITEMS)} items, {bad} problems")
    return bad


def markdown():
    out = []
    out.append("# Nobody Marries the List: the \"hand flat\" pass")
    out.append("")
    out.append("Last updated: Tuesday, November 10, 2026, 10:25 PM PST")
    out.append("")
    out.append("Todd, November 10, 10:18 PM, on chapter 9's \"I put my hand flat on his chest\": \"Hand flat is an aiism. Cut or replace\". That one is done. At 10:21 PM he said yes to a pass on the rest. This is every other one in the book: 52 of \"hand flat\" or \"hands flat\" and 10 related forms (\"palm flat\", \"flat hand\", \"went flat\"), 61 items because two share a line. NOTHING HERE IS APPLIED. Todd picks by number.")
    out.append("")
    cuts = [i for i in ITEMS if i[2] == "cut"]
    reps = [i for i in ITEMS if i[2] == "replace"]
    keeps = [i for i in ITEMS if i[2] == "keep"]
    out.append(f"Claude's picks: {len(cuts)} plain cuts (the word \"flat\" comes out and nothing else changes), {len(reps)} rewordings where a plain cut loses something or repeats a phrase, and {len(keeps)} to keep because the flat hand is the literal point.")
    out.append("")
    out.append("## Rewordings")
    out.append("")
    for n, f, kind, old, new, note in reps:
        ch = int(f.split("-")[1])
        out.append(f"- **{n}** (ch {ch}): \"{old}\" becomes \"{new}\"" + (f" ({note})" if note else ""))
    out.append("")
    out.append("## Keep")
    out.append("")
    for n, f, kind, old, new, note in keeps:
        ch = int(f.split("-")[1])
        out.append(f"- **{n}** (ch {ch}): \"{old}\"" + (f" ({note})" if note else ""))
    out.append("")
    out.append("## Plain cuts")
    out.append("")
    for n, f, kind, old, new, note in cuts:
        ch = int(f.split("-")[1])
        out.append(f"- **{n}** (ch {ch}): \"{old}\" becomes \"{new}\"" + (f" ({note})" if note else ""))
    out.append("")
    out.append("## What the cuts leave")
    out.append("")
    out.append("Taking out \"flat\" removes the tic. The gesture under it is still frequent: a hand on his chest ten times (4, 6, 7, 16, 17, 31, 37, 41, 57, 58), a hand on a back seven times (2, 9, 20, 23, 26, 27, 36), a hand on top of a head seven times (1, 5, 8, 15, 25, 43, 61), and Cal holding a hand on a table, desk or counter to keep still six times (21, 38, 40, 45, 55, 60). The chest, the back at the rim and the head at the doorframe are planted and paid off on purpose. The six of Cal at a table are the ones to look at if the gesture still reads as repeated after this pass.")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    import sys
    if "--md" in sys.argv:
        sys.stdout.write(markdown())
    else:
        sys.exit(1 if check(sys.argv[1]) else 0)
