# Replies that only state a fact, rated for character

November 14, 2026, 10:00 AM. Todd: "Find all instances of replies that are merely repeating facts and rate them on character appropriateness."

Method: a script (claude/tmp/facts.py) pulled every reply of twelve words or fewer that answers a question, 433 in all (claude/tmp/facts.txt). Claude read all 433 and rated the ones that only carry a fact. Not covered: replies to statements, and replies longer than twelve words. Rated from the question and the answer, not the full scene. 5 = only this person says it this way. 1 = anyone could, and the reader learns nothing.

## Rated 2: information only
- 3 Cal, Jo's intake: "It is in a trust." / "I am." / "I have been the trustee since October." / "It has three bedrooms, two baths and a garage." Four in a row.
- 2 Cal: "I am forty-one."
- 11 Cal: "My daughter." / "Eighteen." Clipped, where he usually answers in a full sentence.
- 12 Cal: "She has written them since 2009." Janice said 2009 a few lines before.
- 16 Cal: "Summit Road. At the top of 17."
- 17 Cal: "There are six."
- 19 Cal: "It is in Hawaii, on the Big Island." / "It is between eruptions right now." / "It last went about five hundred years ago." Guidebook answers.
- 20 Cal to Abby: "He is Jo's son. He is nine." The reader has both.
- 22 Cal: "X is Abby's mother."
- 27 Cal: "It is one hundred and fifty dollars."

## Rated 3: plain, in voice, nothing new
6 "I got it in San Jose, at a bakery in Little Portugal." / "It has healed." 8 "Janice did." 12 "I tested forty." / "I do not take many." 14 "I am waiting for Jo." 19 "She is the volcanologist." 21 "I was eleven." 22 "A present." / "It has been fourteen years." / "I mean Friday the fourteenth to Sunday the sixteenth." 25 "It takes forty minutes." 30 "It is the bathroom door from Grandma's hall." 31 Jo "His ex-wife." / "His daughter." 33 "Pancake's fine." 38 "It is a dish." / "It is mine."

## The same fact told twice
- 20: "I have been here since the milk." then "I heard everything from the milk."
- 28: "She had a shirt behind her seat." repeats Jo's line in 27.
- 32: "Who'd you call?" "Jo." and again "Who did you call?" "Jo."; "Did you thank her?" "No." and again "I did not thank her."
- "None of them.": once in 20, twice in 32.

## Rated 4 or 5: a fact that is the character (leave)
Cal's counts and clock times: "I have been here since 4:26." "four hundred and twelve times." "I stopped at one minute and fifty-two seconds." "My watch says ninety-four." "It is four minutes to five." "It was May 7." "It is three million." "It is on the desk." Jo's numbers: "Three hundred and twelve." "Ninety-one." "Thirty-nine ninety-one eighty-one." the payoff figure. Jo's dodges: "A client." "Traffic." "It was dinner." Frank: "Sao Miguel. My grandfather, in 1913."
