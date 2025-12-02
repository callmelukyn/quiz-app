let qIndex = 0;

const dropArea = document.getElementById("dropArea");
const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");

if (dropArea) {
    dropArea.addEventListener("click", () => imageInput.click());
    dropArea.addEventListener("dragover", e => { e.preventDefault(); dropArea.classList.add("dragover"); });
    dropArea.addEventListener("dragleave", () => dropArea.classList.remove("dragover"));
    dropArea.addEventListener("drop", e => {
        e.preventDefault();
        dropArea.classList.remove("dragover");
        imageInput.files = e.dataTransfer.files;
        showPreview();
    });
    imageInput.addEventListener("change", showPreview);
}

function showPreview() {
    const file = imageInput.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
        previewImage.src = reader.result;
        previewImage.style.display = "block";
    };
    reader.readAsDataURL(file);
}

// generate question HTML with Delete Button
function generateQuestionHTML(qIdx, qData=null) {
    const answersHTML = [0,1,2,3].map((i) => {
        const text = qData ? qData.answers[i].text : "";
        const checked = qData && qData.answers[i].correct == 1 ? "checked" : "";
        return `
            <label class="answer-row">
                <input type="radio" name="correct_${qIdx}" value="${i}" ${checked}>
                <input type="text" class="input-field answer-text" placeholder="Answer ${i+1}" value="${text}">
            </label>
        `;
    }).join("");

    const questionText = qData ? qData.text : "";

    // Vypocet cisla otazky pro zobrazeni (ne ID, ale poradi)
    const displayNum = document.querySelectorAll(".question-card").length + 1;

    return `
        <div class="question-card" data-index="${qIdx}">
            <button type="button" class="btn-delete-question" onclick="removeQuestion(this)" title="Remove Question">×</button>
            <h3 class="question-title">Question ${displayNum}</h3>

            <input type="text" class="input-field question-text" value="${questionText}" required>

            <div class="answers-box">
                ${answersHTML}
            </div>
        </div>
    `;
}

// add new question
function addQuestion(qData=null) {
    const container = document.getElementById("questions");
    container.insertAdjacentHTML("beforeend", generateQuestionHTML(qIndex, qData));
    qIndex++;
    // Pokud načítáme existující data, zajistíme správné číslování na konci
    if(!qData) renumberQuestions();
}

// Remove question logic
function removeQuestion(btn) {
    const card = btn.closest(".question-card");
    if (card) {
        card.remove();
        renumberQuestions();
    }
}

// Update "Question 1", "Question 2" titles
function renumberQuestions() {
    const cards = document.querySelectorAll(".question-card");
    cards.forEach((card, index) => {
        const title = card.querySelector(".question-title");
        if(title) {
            title.innerText = `Question ${index + 1}`;
        }
    });
}

// load existing quiz
window.addEventListener("DOMContentLoaded", () => {
    if (typeof EXISTING_QUIZ !== 'undefined' && EXISTING_QUIZ.questions) {
        EXISTING_QUIZ.questions.forEach(q => addQuestion(q));
        renumberQuestions(); // Zajistí srovnání čísel po načtení
    }
});

function submitQuiz() {
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const questions = [];

    const cards = document.querySelectorAll(".question-card");

    for (let q of cards) {
        const qText = q.querySelector(".question-text").value.trim();
        const qIdx = q.dataset.index;
        // Zde je důležité použít qIdx, protože "name" u radio inputů se nemění při mazání karet
        const correct = q.querySelector(`input[name="correct_${qIdx}"]:checked`);

        const answers = [];
        q.querySelectorAll(".answer-text").forEach((a, idx) => {
            answers.push({
                text: a.value.trim(),
                correct: (correct && correct.value == idx) ? 1 : 0
            });
        });

        questions.push({
            text: qText,
            answers: answers
        });
    }

    const payload = {
        title: title,
        description: description,
        questions: questions
    };

    document.getElementById("dataField").value = JSON.stringify(payload);
    document.getElementById("quizForm").submit();
}