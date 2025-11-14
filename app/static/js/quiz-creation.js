let qIndex = 0;

// ------------------------------
// DRAG & DROP IMAGE UPLOADER
// ------------------------------

const dropArea = document.getElementById("dropArea");
const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");

dropArea.addEventListener("click", () => imageInput.click());
dropArea.addEventListener("dragover", e => {
    e.preventDefault();
    dropArea.classList.add("dragover");
});
dropArea.addEventListener("dragleave", () => dropArea.classList.remove("dragover"));
dropArea.addEventListener("drop", e => {
    e.preventDefault();
    dropArea.classList.remove("dragover");
    imageInput.files = e.dataTransfer.files;
    showPreview();
});
imageInput.addEventListener("change", showPreview);

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

// ------------------------------
// ADD QUESTION BLOCK
// ------------------------------

function addQuestion() {
    const container = document.getElementById("questions");

    const qHTML = `
        <div class="question-card" data-index="${qIndex}">
            <h3 class="question-title">Question ${qIndex + 1}</h3>

            <input type="text" class="input-field question-text" placeholder="Question text" required>

            <div class="answers-box">
                ${[0,1,2,3].map(a => `
                    <label class="answer-row">
                        <input type="radio" name="correct_${qIndex}" value="${a}">
                        <input type="text" class="input-field answer-text" placeholder="Answer ${a+1}" required>
                    </label>
                `).join("")}
            </div>
        </div>
    `;

    container.insertAdjacentHTML("beforeend", qHTML);
    qIndex++;
}

// ------------------------------
// VALIDATION + SUBMIT
// ------------------------------

function submitQuiz() {
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();

    if (!title || !description) {
        alert("Please fill title and description.");
        return;
    }

    const questions = [];
    const cards = document.querySelectorAll(".question-card");

    if (cards.length === 0) {
        alert("Please add at least one question.");
        return;
    }

    for (let q of cards) {
        const qText = q.querySelector(".question-text").value.trim();
        if (!qText) {
            alert("Each question must have text.");
            return;
        }

        const correct = q.querySelector(`input[name="correct_${q.dataset.index}"]:checked`);
        if (!correct) {
            alert("Each question must have exactly one correct answer.");
            return;
        }

        const answers = [];
        let validAnswers = true;

        q.querySelectorAll(".answer-text").forEach((a, idx) => {
            const val = a.value.trim();
            if (!val) validAnswers = false;
            answers.push({
                text: val,
                correct: correct.value == idx ? 1 : 0
            });
        });

        if (!validAnswers) {
            alert("All 4 answers must be filled.");
            return;
        }

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