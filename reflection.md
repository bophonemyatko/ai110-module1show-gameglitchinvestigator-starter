# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
    It worked well. Nothing seems out of place. But the attempt left didn't get deduceted for the first time. 
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
    The hint was saying opposite. The first attempt didn't get recorded.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Changing lower and higher and I verified by actually playing the game. 
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
AI didn't suggest anything misleading. However, sometimes when I ask AI to fix a bug, it doesn't fix other part of the code that also gets affected by the bug. So I have to play the game again and ask AI to add/edit a specific part again. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I test the specific bug that I fixed in the live application
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I ran the out of range test and it showed that it passed
- Did AI help you design or understand any tests? How?
Test created by AI are fairly readable or it's easy to understand all the test. 

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
The secret number kept changing because it was at the top of the code outside of all session state guard.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit "reruns" is basically telling the computer to rerun the app by reading the whole code file again to make sure your new changes get applied to the web application. Session state store the previous data before the rerun so that after rerun the scores, etc. stays the same. 
- What change did you make that finally gave the game a stable secret number?
use if statement to check first so that the secret number is only generated once per game
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  Commiting every time after editing
- What is one thing you would do differently next time you work with AI on a coding task?
Make sure to write down or make notes of bugs so that I don't forget
- In one or two sentences, describe how this project changed the way you think about AI generated code.
We have to be specific when asking AI to do something or it will just assume and execute it. 
