import csv
import json

data = [
  {
    "id": 1,
    "cards": [
      {
        "type": "story",
        "text": "You're the only one at the lounge this morning. You can't wait until The Pond reopens for morning coffee!",
        "trustLabel": "Enjoy the quiet…",
        "distrustLabel": "Enjoy the quiet!",
        "isFlipped": False,
        "image": "/images/demo-lounge.png",
      },
      {
        "type": "story",
        "text": "Beejou enters anxiously: Ah! Oh! I'm so glad you're here!",
        "trustLabel": "Did something happen?",
        "distrustLabel": "Hey Beejou!",
        "isFlipped": False,
        "image": "/images/demo-lounge-beejou.png",
      },
      {
        "type": "story",
        "text": "I just got an email that says Security Team Alpha detected suspicious activity using my student ID!",
        "trustLabel": "Oh no…",
        "distrustLabel": "Go Back",
        "isFlipped": False,
        "image": "/images/demo-lounge-beejou-close.png",
      },
      {
        "type": "story",
        "text": "They're gonna lock my account if I don't verify my identity...That can't be good.",
        "trustLabel": "…verify?",
        "distrustLabel": "Go Back",
        "isFlipped": False,
        "image": "/images/demo-lounge-beejou-close.png",
      },
      {
        "type": "story",
        "text": "I'm me, the one and only Beejou! Could you watch my things while I go and sort this out?",
        "trustLabel": "Let me take a look…",
        "distrustLabel": "Go Back",
        "isFlipped": False,
        "image": "/images/demo-lounge-beejou-worried.png",
      },
      {
        "type": "story",
        "text": "The first thing we're going to look at is the header.",
        "trustLabel": "Let's keep reading…",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "/images/demo-email-subject.png",
      },
      {
        "type": "story",
        "text": "Next, we're going to look at the email's body.",
        "trustLabel": "Keep looking…",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "/images/demo-email-body.png",
      },
      {
        "type": "story",
        "text": "Finally, we're going to look at the email's call to action and signature.",
        "trustLabel": "Hmm…",
        "distrustLabel": "Hmm…",
        "isFlipped": False,
        "image": "/images/demo-email-closing.png",
      },
      {
        "type": "decision",
        "text": "Is this email legit?",
        "trustLabel": "Looks like the real deal!",
        "distrustLabel": "Something's not right!",
        "trustChoice": {
          "consequences": { "trust": -10, "security": -15, "gooseInfiltration": 10 },
          "feedback": "It asks for 3 different forms of ID! Beejou heads to the library to scan her cards and you make sure her things don't move an inch while she's gone.",
        },
        "distrustChoice": {
          "consequences": { "trust": 5, "security": 10, "gooseInfiltration": -5 },
          "feedback": "It wants 3 different forms of ID! You warn Beejou that this is likely a scam. She's relieved because she actually was acting a little suspicious, but only cause she wanted to surprise you with a fresh donut from Do or Donut.",
        },
        "isFlipped": False,
        "image": "beejou.jpg",
      },
      {
        "type": "reveal",
        "text": "",
        "trustLabel": "I see",
        "distrustLabel": "Got it",
        "isFlipped": False,
        "image": "beejou.jpg",
      },
    ],
  },
  {
    "id": 5,
    "cards": [
      {
        "type": "story",
        "text": "One of the best features of Reel Polytechnic's campus is their Pond cafeteria",
        "trustLabel": "Who else has a Pond?!",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "/images/demo-lounge.png",
      },
      {
        "type": "story",
        "text": "You read all about it in the brochure, so you're excited to experience the Advanced Salad Bar",
        "trustLabel": "Yummy toppings!",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "But you're dismayed to see it's Closed for Beautification!",
        "trustLabel": "Oh no…",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "What does that even mean? You check the college website to find out.",
        "trustLabel": "beautification?",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "You head to the Reel Polytechnic website.",
        "trustLabel": "Okay…",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "There's a blog about it! Let's read on...",
        "trustLabel": "Keep looking…",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "decision",
        "text": "Does this information look right?",
        "trustLabel": "Guess I'll wait!",
        "distrustLabel": "Maybe this is old...",
        "trustChoice": {
          "consequences": { "trust": -10, "security": -15, "gooseInfiltration": 10 },
          "feedback": "Sounds like you'll have to go somewhere else for Advanced Salad options, but the new features sound great.",
        },
        "distrustChoice": {
          "consequences": { "trust": 5, "security": 10, "gooseInfiltration": -5 },
          "feedback": "Unfortunately the doors are locked. Looks like you better be looking for refreshments elsewhere. With features like these, this will take months to complete.",
        },
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "reveal",
        "text": "",
        "trustLabel": "I see",
        "distrustLabel": "Got it",
        "isFlipped": False,
        "image": "",
      },
    ],
  },
  {
    "id": 6,
    "cards": [
      {
        "type": "story",
        "text": "You're enjoying your morning outside, daydreaming about your next visit to The Pond when it reopens.",
        "trustLabel": "Relax and wait...",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Beejou flies in, buzzing: Did you see the posters? We're hosting a Four-Armed Basketball tournament!",
        "trustLabel": "Tell me more!",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "We have to go! I used to play, back in the day, you know!",
        "trustLabel": "Of course!",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "But there's a problem... I tried to get tickets, and my card isn't working!",
        "trustLabel": "Oh no...",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Can you help me get them? Please, I don't want to miss this!",
        "trustLabel": "Let me check it out...",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Beejou sends you the website and you open it up on your phone.",
        "trustLabel": "Okay…",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Let's take a look at this webpage",
        "trustLabel": "Keep looking…",
        "distrustLabel": "Back",
      },
      {
        "type": "decision",
        "text": "Do you buy the tickets?",
        "trustLabel": "Gotta see the game!",
        "distrustLabel": "I don't like this...",
        "trustChoice": {
          "consequences": { "trust": -10, "security": -15, "gooseInfiltration": 10 },
          "feedback": "You check out and are promised the hand delivery. You're advised to stay on campus, otherwise they wont be able to find you, but no one ever arrives.",
        },
        "distrustChoice": {
          "consequences": { "trust": 5, "security": 10, "gooseInfiltration": -5 },
          "feedback": "Beejou discovers that you can just get tickets at a table by the gym and she says she'll get you a ticket as thanks since you helped her out.",
        },
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "reveal",
        "text": "",
        "trustLabel": "I see",
        "distrustLabel": "Got it",
        "isFlipped": False,
        "image": "",
      },
    ],
  },
  {
    "id": 7,
    "cards": [
      {
        "type": "story",
        "text": "You're sitting out on the grass, sipping your coffee and catching up on some reading.",
        "trustLabel": "Enjoy the moment...",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Beejou calls you: Guess what! Beeyonce is coming to campus!!",
        "trustLabel": "Really?",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "I just got an email from my Beeyonce fan community with an exclusive link to buy tickets before they go on sale to the public!",
        "trustLabel": "Sounds awesome!",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "I'm so excited, but also a little nervous...",
        "trustLabel": "Why's that?",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "It opens a link that asks for my student ID and credit card info. Do you think it's ok?",
        "trustLabel": "Let's look together.",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Take a look at the URL",
        "trustLabel": "Okay...",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Next, we're going to look at the webpage.",
        "trustLabel": "Keep looking…",
        "distrustLabel": "Back",
      },
      {
        "type": "decision",
        "text": "Should Beejou trust the site?",
        "trustLabel": "Yes! Let's get tickets!",
        "distrustLabel": "Maybe we shouldn't.",
        "trustChoice": {
          "consequences": { "trust": -10, "security": -15, "gooseInfiltration": 10 },
          "feedback": "You and Beejou get front row tickets. Beejou's so excited, she says she wont sleep for weeks.",
        },
        "distrustChoice": {
          "consequences": { "trust": 5, "security": 10, "gooseInfiltration": -5 },
          "feedback": "Sounds worrying so you decide not to go but you can't help but wonder if concert will be one of those life changing, world altering one that everyone won't stop talking about for weeks.",
        },
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "reveal",
        "text": "",
        "trustLabel": "I see",
        "distrustLabel": "Got it",
        "isFlipped": False,
        "image": "",
      },
    ],
  },
  {
    "id": 8,
    "cards": [
      {
        "type": "story",
        "text": "You're the only one at the lounge this morning. You can't wait until The Pond reopens for morning coffee!",
        "trustLabel": "Enjoy the quiet…",
        "distrustLabel": "Enjoy the quiet!",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Beejou enters anxiously: Ah! Oh! I'm so glad you're here!",
        "trustLabel": "Did something happen?",
        "distrustLabel": "Hey Beejou!",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "I just got an email that says Security Team Alpha detected suspicious activity using my student ID!",
        "trustLabel": "Oh no…",
        "distrustLabel": "Go Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "They're gonna lock my account if I don't verify my identity...That can't be good.",
        "trustLabel": "…verify?",
        "distrustLabel": "Go Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "I'm me, the one and only Beejou! Could you watch my things while I go and sort this out?",
        "trustLabel": "Let me take a look…",
        "distrustLabel": "Go Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "The first thing we're going to look at is the header.",
        "trustLabel": "Let's keep reading…",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Next, we're going to look at the email's body.",
        "trustLabel": "Keep looking…",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Finally, we're going to look at the email's call to action and signature.",
        "trustLabel": "Hmm…",
        "distrustLabel": "Hmm…",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "decision",
        "text": "Is this email legit?",
        "trustLabel": "Looks like the real deal!",
        "distrustLabel": "Something's not right!",
        "trustChoice": {
          "consequences": { "trust": -10, "security": -15, "gooseInfiltration": 10 },
          "feedback": "It asks for 3 different forms of ID! Beejou heads to the library to scan her cards and you make sure her things don't move an inch while she's gone.",
        },
        "distrustChoice": {
          "consequences": { "trust": 5, "security": 10, "gooseInfiltration": -5 },
          "feedback": "It wants 3 different forms of ID! You warn Beejou that this is likely a scam. She's relieved because she actually was acting a little suspicious, but only cause she wanted to surprise you with a fresh donut from Do or Donut.",
        },
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "reveal",
        "text": "",
        "trustLabel": "I see",
        "distrustLabel": "Got it",
        "isFlipped": False,
        "image": "",
      },
    ],
  },
  {
    "id": 9,
    "cards": [
      {
        "type": "story",
        "text": "You're checking your email in between power naps at the campus library.",
        "trustLabel": "It's so quiet…",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "There's an offer to access a plentitude of ebooks and textbooks!",
        "trustLabel": "I love ebooks!",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "It sounds like it could be a good deal...",
        "trustLabel": "Check it out!",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "First, who's sending this to me.",
        "trustLabel": "Let's see...",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Let's examine the body of the email.",
        "trustLabel": "Seems interesting.",
        "distrustLabel": "Back",
      },
      {
        "type": "story",
        "text": "Finally, let's look at the offer and the signature.",
        "trustLabel": "Sounds appealing...",
        "distrustLabel": "Back",
      },
      {
        "type": "decision",
        "text": "Do you trust this offer?",
        "trustLabel": "I want books!",
        "distrustLabel": "This isn't right!",
        "trustChoice": {
          "consequences": { "trust": -10, "security": -15, "gooseInfiltration": 10 },
          "feedback": "It's worrying when you crack open the dusty .pdf of 'Key Study Habits for Sucess.' It's just a single paged document listing out 3 study habits: 1. Studie with TV on. 2. Pcrorastinate until the last minnit. 3. Skip brekfast.",
        },
        "distrustChoice": {
          "consequences": { "trust": 5, "security": 10, "gooseInfiltration": -5 },
          "feedback": "You report it as a phishing attempt and are thanked for your report. You worry you'll have to find 10,000's of books elsewhere, but you remember you can go to the library!",
        },
        "isFlipped": False,
        "image": "",
        "overlay": {
          "image": "/images/demo-email-phishing.png",
          "text": "",
        },
      },
      {
        "type": "reveal",
        "text": "",
        "trustLabel": "I see",
        "distrustLabel": "Got it",
        "isFlipped": False,
        "image": "",
      },
    ],
  },
  {
    "id": 10,
    "cards": [
      {
        "type": "story",
        "text": "You're working late in the study lounge getting some last minute things done before you go home.",
        "trustLabel": "Gotta finish...",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "You get an email asking you participate in an official college survey about student life.",
        "trustLabel": "I have opinions...",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "You've gotten three of these this week!",
        "trustLabel": "No inbox space!",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "I guess it could be worth it to check out.",
        "trustLabel": "Let's see about this…",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Let's start by examining the email's header.",
        "trustLabel": "Let's keep reading…",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Next up, we'll focus on the email's message.",
        "trustLabel": "Keep looking…",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Finally, let's look at the email's call to action and signature.",
        "trustLabel": "Hmm…",
        "distrustLabel": "Go back.",
      },
      {
        "type": "decision",
        "text": "Is this email legit?",
        "trustLabel": "Give my feedback!",
        "distrustLabel": "They want my thoughts?",
        "trustChoice": {
          "consequences": { "trust": -10, "security": -15, "gooseInfiltration": 10 },
          "feedback": "You get a sweet $10 campus store gift card, and a follow up email gives you two more to share with your friends, or get two really small mugs.",
        },
        "distrustChoice": {
          "consequences": { "trust": 5, "security": 10, "gooseInfiltration": -5 },
          "feedback": "You receive an email thanking you for your vigilance in identifying phishing scams, but remember, phishing emails often request sensitive information, which Reel Polytechnic will never do!",
        },
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "reveal",
        "text": "",
        "trustLabel": "I see",
        "distrustLabel": "Got it",
        "isFlipped": False,
        "image": "",
      },
    ],
  },
  {
    "id": 11,
    "cards": [
      {
        "type": "story",
        "text": "Your computer's going into red alert mode!!! There's a flashing software update message for BugBuster Antivirus!",
        "trustLabel": "Check the message...",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "You're unsure whether to trust it.",
        "trustLabel": "Call for help?",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "You call the IT service desk for help. They ask you to meet them at The Pond, where they're busy angling the phish.",
        "trustLabel": "Head to The Pond.",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "One of them looks up and says: Hey there! Let's see what's going on with your computer.",
        "trustLabel": "Explain the issue.",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Ah, yes! They mentioned this update was talked about on BugBuster's blog.",
        "trustLabel": "Tell me more.",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "It says this update fixes a security bug. It's important to install it for your safety.",
        "trustLabel": "Lemmie think...",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "decision",
        "text": "Is this update legit?",
        "trustLabel": "Looks like the real deal!",
        "distrustLabel": "Something's not right!",
        "trustChoice": {
          "consequences": { "trust": -10, "security": -15, "gooseInfiltration": 10 },
          "feedback": "You decide to trust their advice and install the update. You feel secure knowing your system is protected.",
        },
        "distrustChoice": {
          "consequences": { "trust": 5, "security": 10, "gooseInfiltration": -5 },
          "feedback": "Sure, it sounds critical, but it can't actually be that critical. It can wait!",
        },
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "reveal",
        "text": "",
        "trustLabel": "I see",
        "distrustLabel": "Got it",
        "isFlipped": False,
        "image": "",
      },
    ],
  },
  {
    "id": 12,
    "cards": [
      {
        "type": "story",
        "text": "You're researching at the library and get a frantic text from Beejou.",
        "trustLabel": "What's happening?",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Beejou: AAA DONT CLIKC FOR FREE FLOPWERS!!!",
        "trustLabel": "What??",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "You rush to find Beejou. She looks desperate and worried about her computer.",
        "trustLabel": "What's wrong?",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "All I did was click a link to get free flowers and now my computer's locked!",
        "trustLabel": "Let's get help!",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "You take Beejou to the IT service team to check over her computer. They're catching phish, but they're happy to help.",
        "trustLabel": "Explain the situation.",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "(beaver 1): Oh my, this looks like ransomware!",
        "trustLabel": "What can we do?",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "(beaver 2): We can try to fix it, but Beejou you need to be careful with suspicious emails.",
        "trustLabel": "Thank you!",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "As they work on Beejou's computer, you receive a notification. It's the same email!",
        "trustLabel": "Show them.",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "(beaver 2): Since you're already here, let's walk through it together.",
        "trustLabel": "Read the email.",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "Hmm. Now, let's look at the body.",
        "trustLabel": "Okay...",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "I can see how Beejou was fooled.",
        "trustLabel": "Me too...",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "decision",
        "text": "What do you think about this offer?",
        "trustLabel": "It could be legit..",
        "distrustLabel": "So suspicious!",
        "trustChoice": {
          "consequences": { "trust": -10, "security": -15, "gooseInfiltration": 10 },
          "feedback": "Ahh! I know flowers are tempting but you should be wary about offers that sounds too good to be true.",
        },
        "distrustChoice": {
          "consequences": { "trust": 5, "security": 10, "gooseInfiltration": -5 },
          "feedback": "That's right! If an offer sounds too good to be true, it probably is!",
        },
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "reveal",
        "text": "",
        "trustLabel": "I see",
        "distrustLabel": "Got it",
        "isFlipped": False,
        "image": "",
      },
    ],
  },
  {
    "id": 13,
    "cards": [
      {
        "type": "story",
        "text": "You recently read that the Campus Cafe is trying out a new robotic coffee handler.",
        "trustLabel": "Robot coffee!",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "There's a special right now that uses AI to craft the perfect morning beverage based entirely on your mood!",
        "trustLabel": "I'm curious...",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "But, when you get your coffee, it just doesn't taste right. It doesn't seem like it's actually yours.",
        "trustLabel": "I don't trust it...",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "You call the IT support team for help. They listen to your problem.",
        "trustLabel": "Hear them out.",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "(beaver 1): Bring it to The Pond and we'll test it for you!",
        "trustLabel": "Head over there.",
        "distrustLabel": "Go back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "You arrive at The Pond, coffee in hand. They slap the water with their tails, looking excited.",
        "trustLabel": "Hand it over.",
        "distrustLabel": "Back",
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "story",
        "text": "(beaver 1): Let's take a look...",
        "trustLabel": "Watch closely.",
        "distrustLabel": "Back",
      },
      {
        "type": "decision",
        "text": "You start to suspect that they might just be aiming to get a free drink out of you.",
        "trustLabel": "Is this my mood coffee?",
        "distrustLabel": "I'll take it back!",
        "trustChoice": {
          "consequences": { "trust": -10, "security": -15, "gooseInfiltration": 10 },
          "feedback": "You watch as they all took a little sip each. It was kinda cute, so you didn't mind, but now you have to go get a new one. They thank you for your trouble.",
        },
        "distrustChoice": {
          "consequences": { "trust": 5, "security": 10, "gooseInfiltration": -5 },
          "feedback": "They just want to drink your coffee!! Even if it's wrong, you might as well drink it. You've gotta get to the gym before it closes!",
        },
        "isFlipped": False,
        "image": "",
      },
      {
        "type": "reveal",
        "text": "",
        "trustLabel": "I see",
        "distrustLabel": "Got it",
        "isFlipped": False,
        "image": "",
      },
    ],
  },
]

# Prepare the CSV file
csv_file = 'scenarios.csv'

# Define the header
header = [
    "ID", "Card Type", "Text", "Trust Label", "Distrust Label",
    "Is Flipped", "Image", "Trust Choice Consequences",
    "Trust Choice Feedback", "Distrust Choice Consequences",
    "Distrust Choice Feedback"
]

# Function to extract the data and write to CSV
def convert_to_csv(data, csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for scenario in data:
            id = scenario['id']
            for card in scenario['cards']:
                card_type = card.get('type', '')
                text = card.get('text', '')
                trust_label = card.get('trustLabel', '')
                distrust_label = card.get('distrustLabel', '')
                is_flipped = card.get('isFlipped', '')
                image = card.get('image', '')

                trust_choice_consequences = ''
                trust_choice_feedback = ''
                distrust_choice_consequences = ''
                distrust_choice_feedback = ''

                if card_type == 'decision':
                    trust_choice = card.get('trustChoice', {})
                    distrust_choice = card.get('distrustChoice', {})
                    trust_choice_consequences = json.dumps(trust_choice.get('consequences', ''))
                    trust_choice_feedback = trust_choice.get('feedback', '')
                    distrust_choice_consequences = json.dumps(distrust_choice.get('consequences', ''))
                    distrust_choice_feedback = distrust_choice.get('feedback', '')

                writer.writerow([
                    id, card_type, text, trust_label, distrust_label, is_flipped, image,
                    trust_choice_consequences, trust_choice_feedback,
                    distrust_choice_consequences, distrust_choice_feedback
                ])

# Call the function to convert JSON to CSV
convert_to_csv(data, csv_file)

print(f"Data has been successfully written to {csv_file}")
