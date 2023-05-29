const chat = {
    1: {
        text: 'Hi! My name is Nordy! Nice to meet you!',
        next: 2
    },

    2: {
        text: 'How may I help you today?',
       options: [{
        text: 'What is Aspire HR India?',
        next:3
    }
]
    },
    3: {
        text: 'We advertise jobs of all types for any sector, and our team supports applicants in their search for the best job agreement, so that they can realize their work-life balance and improve their professional goals.',
        options: [
            {
                text: "<strong>OH!</strong>, nice!",
                next: 2
            },
            {
                text: "<strong>OK</strong>, I knew that",
                next: 5
            },
            {
                text: "<strong>okay</strong>, I Don't Care",
                next: 7
            }
        ]
    },
    4: {
        text: 'Awesome. This chat is still in development',
    },
    5: {
        text: 'Aah, you\'re Smart!',
        next: 6
    },
    6: {
        text: 'You should check this Out',
        options: [
            {
                text: "okay",
                url: "https://youtube.com/shorts/Obgnr9pc820?feature=share"
            }
        ]
    },

    7: {
        text: 'oh oh check this',
        options: [
            {
                text: "Please click this!",
                url: "https://youtu.be/dQw4w9WgXcQ"
            }
        ]
    }
};