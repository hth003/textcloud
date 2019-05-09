# Text Cloud

1. Describe at least three functions in your program that work well and have a potential to be reused in other similar programs; imagine and describe the tasks for which they could be useful. What program features are you proud of? List them and briefly discuss why. 
• crawlWeb(seed,maxDepth): The crawlWeb function work perfectly. It can retrieve information from any website, navigate to other websit and crawl the website fast based on depth. They can be used to make search engine. 
• removePunc(content): Because it can remove punctuation and space of a string, it is more effective that the split() function. This function can be used to split any paragraph into word 
• displayCloud(sortedList): This is the function I am most proud of because it constructs a 3D visual “tornado” text cloud. Because the word with most appearances appears at the bottom of the tornado and then it move. Beside text, we can assign the position to other objects such as 
images. It creates interesting way of represent information. 
Figure 1: My textCloud representation 
2. If some parts of the program are not working properly, mention them and the inputs for which they don't work. If the program does not fully meet the Project's specifications, again, name those places and explain why. 
• The stemming part are not working properly because it miss many cases. For example, “great” become “greate”. There might be many other cases that I haven't though of. 
• The program will not work if the text file is empty and or if it contains only punctuation symbol. 
• The program might crash if the seed page have a link to itself and the depth is set at a very big number (just a guess) 
3. Discuss at least three possible improvements to your project. Given more time, what features would you like to add to the program? 
Improvement I would want to make: 
Improvement 1: Make a dictionary of stemming special cases 
There are many special words that do not follow stemming rule. To solve this, I need to develop a dictionary of special cases. 
Improvement 2: Use a better stemming algorithm: 
- Count how many vowel-consonant combination (vc) after the first syllable in the word to know the word's basic structure (ccc → c, vvv → v) For example: vc = 0: eve, be vc = 1: man, toy, trouble vc = 2: troubles - Add more cases: for example, add e after “at” only when m>1, add e if it the word have form of cvc - Add more rules: for example: application => apply 
