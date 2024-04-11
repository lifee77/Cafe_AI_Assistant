const questionContainer = document.getElementById('question-container');
const recommendationDiv = document.getElementById('recommendation');
let currentQuestionId = "1"; // Start with the first question

// ... (fetchQuestion - unchanged) ...

async function handleAnswer(question, selectedOption) {
  try {
    const response = await fetch(`http://localhost:5000/questions/${currentQuestionId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ answer: selectedOption }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const nextQuestion = await response.json();

    if (nextQuestion.message) { // Recommendation time!
      const userAnswers = []/* Gather all answers so far */
      const recommendations = await getRecommendation(userAnswers);  
      displayRecommendations(recommendations); 
    } else {
      currentQuestionId = nextQuestion.id;
      displayQuestion(nextQuestion); 
    }

  } catch (error) {
    console.error("Error handling answer:", error);
    displayErrorMessage(error.message);
  }
}

async function getRecommendation(userAnswers) {
  try {
    const response = await fetch('http://localhost:5001/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ answers: userAnswers })
    });

    if (!response.ok) {
      throw new Error('Could not get recommendation from Prolog');
    }

    return await response.json();

  } catch (error) {
    console.error("Error getting recommendation:", error);
    displayErrorMessage("Error communicating with recommendation system");
  }
}

function displayRecommendations(recommendations) {
  // ... (Implement dynamic display based on your Prolog output) ...
}

function displayErrorMessage(message) {
  // ... (Implement a way to show error messages to the user) ...
}

fetchQuestion(currentQuestionId); // Start the quiz 
