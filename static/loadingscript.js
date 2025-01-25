
const factsText = document.getElementById("facts");


document.addEventListener("DOMContentLoaded", function() {
    console.log(factsText); // Check if factsText is correctly identified

    const facts = ["Phishing is the most common form of cyber crime, with an estimated 3.4 billion spam emails sent every day.",
                "The use of stolen credentials is the most common cause of data breaches.",
                "Google blocks around 100 million phishing emails daily.",
                "Over 48% of emails sent in 2022 were spam.",
                "Over a fifth of phishing emails originate from Russia.",
                "83% of UK businesses that suffered a cyber attack in 2022 reported the attack type as phishing.",
                "The average cost of a data breach against an organisation is more than $4 million.",
                "One whaling attack costs a business $47 million.",
                "Spear phishing emails are the most popular targeted attack vector"
            ];

    function loadingFacts(){
        const index = Math.floor(Math.random() * facts.length);
        factsText.textContent = facts[index];
        setTimeout(loadingFacts, 6000);
    }

    loadingFacts();
});

