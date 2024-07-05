export default [
  {
    id: 1,
    cards: [
      {
        type: "story",
        text: "Ah! Oh! I'm so glad you're here!",
        trustLabel: "Did something happen?",
        distrustLabel: "Hey Beejou!",
        isFlipped: false,
        image: "/images/scenario-demo-image-00.png",
      },
      {
        type: "story",
        text: "I just got an email that says Security Team Alpha detected suspicious activity using my student ID!",
        trustLabel: "Oh no…",
        distrustLabel: "Go Back",
        isFlipped: false,
        image: "beejou",
      },
      {
        type: "story",
        text: "They're gonna lock my account if I don't verify my identity... That can't be good.",
        trustLabel: "… verify?",
        distrustLabel: "Go Back",
        isFlipped: false,
        image: "beejou.jpg",
      },
      {
        type: "story",
        text: "I'm me, the one and only Beejou! Could you watch my things while I go and sort this out?",
        trustLabel: "Can I take a look at that email?",
        distrustLabel: "Go Back",
        isFlipped: false,
        image: "beejou.jpg",
      },
      {
        type: "story",
        text: `The first thing we're going to look at is the header.`,
        trustLabel: "This looks serious",
        distrustLabel: "This seems fishy",
        isFlipped: false,
        image: "beejou.jpg",
      },
      {
        type: "story",
        text: "Next, we're going to look at the body.",
        trustLabel: "This looks serious",
        distrustLabel: "This seems fishy",
        isFlipped: false,
        image: "beejou.jpg",
      },
      {
        type: "story",
        text: "What they're asking for and their signature",
        trustLabel: "This looks serious",
        distrustLabel: "This seems fishy",
        isFlipped: false,
        image: "beejou.jpg",
      },
      {
        type: "decision",
        text: "Do you trust this email and help Beejou verify her identity?",
        trustLabel: "Trust",
        distrustLabel: "Distrust",
        trustChoice: {
          consequences: { trust: -10, security: -15, gooseInfiltration: 10 },
          feedback:
            "It asks for 3 different and scanned forms of ID! Beejou heads to the library to scan her cards and you make sure her things don't move an inch while she's gone.",
        },
        distrustChoice: {
          consequences: { trust: 5, security: 10, gooseInfiltration: -5 },
          feedback:
            "It wants 3 different and scanned forms of ID! You warn Beejou that this is likely a scam. She's relieved because she actually was acting a little suspicious, but only cause she wanted to surprise you with a fresh donut from Do or Donut.",
        },
        isFlipped: false,
        image: "beejou.jpg",
      },
      {
        type: "reveal",
        text: ``,
        trustLabel: "I see",
        distrustLabel: "Got it",
        isFlipped: false,
        image: "beejou.jpg",
      },
    ],
  },
];
