const chat = {
    
    1: {
        text: 'How may I help you today?',
       options: [{
        text: 'What is Aspire Corporate Solutions?',
        next: 10
        
    
    },
    {
        text: "How do i apply for a job?",
        next: 11
    },
    {
        text: "What services do you offer?",
        next: 12
    },
    {
        text: "How do i contact you?",
        next: 13
    }


    ]
    },
    
    10: {
        text: 'Aspire Corporate Solutions was started way back in 2010 and we have grown since then. We are now a trusted and reliable name amongst the industrial spectrum in Goa, as well as other states in India. Most of our clients have been with us since inception, and we are preferred by clients due to efficient and dependable action.',
        options: [
            {
                text: "how do i apply for a job?",
                next: 11
            },
            {
                text: "What services do you offer?",
                next: 12
            },
            {
                text: "How do i contact you?",
                next: 13
            }
        ]
    },


    11: {
        text: 'Go to the job page -> select which job you want to apply for from the jobs available -> click <strong>apply for this job </strong> -> choose the whether you want to apply with cv or linkedin <br></br><br></br>  if applying through CV you must fill all the details required -> then click submit <br></br><br></br>  if applying through linkedin -> click apply with linkedin   ',
        options: [
            {
                text: "What is Aspire Corporate Solutions?",
                next: 10
            },
            {
                text: "What services do you offer?",
                next: 12
            },
            {
                text: "How do i contact you?",
                next: 13
            }
        ]
    },


    12: {
        text: 'Some of the services we offer are : <br> <strong> Recruitment & Selection </br> <br> Assessment & Training</br>  <br> Organisational Mapping & Structure </br> <br> Salary Survey</br> <br> Career Counselling</br>',
        options: [
            {
                text: "What is Aspire Corporate Solutions?",
                next: 10
            },
            {
                text: "how do i apply for a job?",
                next: 11
            },
            {
                text: "How do i contact you?",
                next: 13
            },
        ]
    },


    13: {
        text: 'You can contact us through <br></br><br> <strong>Email: </strong>  aspire.cos@gmail.com </br><br></br> <strong>Phone : </strong> 91-7030222765 \ 91-7796520001 <br></br>',
        options: [
            {
                text: 'What is Aspire Corporate Solutions?',
                next: 10
            
            },
            {
                text: "How do i apply for a job?",
                next: 11
            },
            {
                text: "What services do you offer?",
                next: 12
            },
        ]
    },

};