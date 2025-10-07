const start = document.getElementById("start");
const quiz = document.getElementById("quiz");
const questionEl = document.getElementById("question");
const qImg = document.getElementById("qImg");
const choices = {
    A: document.getElementById("A"),
    B: document.getElementById("B"),
    C: document.getElementById("C"),
    D: document.getElementById("D")
};
const counterEl = document.getElementById("counter");
const timeGauge = document.getElementById("timeGauge");
const progressEl = document.getElementById("progress");
const scoreDiv = document.getElementById("scoreContainer");

const questions = [
    {
        question: "Что такое JavaScript?",
        imgSrc: "/static/img/img.png",
        choiceA: "A) Язык разметки для веб-страниц",
        choiceB: "B) ЯП для создания интерактивных элементов на веб-страницах",
        choiceC: "C) Система управления базами данных",
        choiceD: "D) Операционная система",
        correct: "B"
    },
    {
        question: "Как объявить переменную в JavaScript с помощью ключевого слова?",
        imgSrc: "https://via.placeholder.com/120/4caf50/FFFFFF?text=LET",
        choiceA: "A) variable x = 5;",
        choiceB: "B) var x = 5;",
        choiceC: "C) let x = 5;",
        choiceD: "D) dim x = 5;",
        correct: "C"
    },
    {
        question: "Что такое функция в JavaScript?",
        imgSrc: "https://via.placeholder.com/120/ff9800/FFFFFF?text=FUNC",
        choiceA: "A) Специальный объект для хранения данных",
        choiceB: "B) Блок кода, который можно вызвать многократно",
        choiceC: "C) Тип данных для хранения чисел",
        choiceD: "D) Способ объявления переменной",
        correct: "B"
    },
    {
        question: "Как написать условие if в JavaScript?",
        imgSrc: "https://via.placeholder.com/120/f44336/FFFFFF?text=IF",
        choiceA: "A) if x > 0 { ... }",
        choiceB: "B) if (x > 0) { ... }",
        choiceC: "C) if x > 0 then { ... }",
        choiceD: "D) condition (x > 0) { ... }",
        correct: "B"
    },
    {
        question: "Что такое массив в JavaScript?",
        imgSrc: "https://via.placeholder.com/120/9c27b0/FFFFFF?text=ARR",
        choiceA: "A) Объект, содержащий упорядоченные данные",
        choiceB: "B) Тип данных для хранения чисел",
        choiceC: "C) Способ объявления функции",
        choiceD: "D) Специальный оператор",
        correct: "A"
    },
    {
        question: "Какой оператор используется для сравнения на равенство в JavaScript?",
        imgSrc: "https://via.placeholder.com/120/00bcd4/FFFFFF?text==",
        choiceA: "A) =",
        choiceB: "B) ==",
        choiceC: "C) ===",
        choiceD: "D) =!=",
        correct: "B"
    },
    {
        question: "Как добавить новый элемент в массив в JavaScript?",
        imgSrc: "https://via.placeholder.com/120/8bc34a/FFFFFF?text=PUSH",
        choiceA: "A) array.add(element);",
        choiceB: "B) array.push(element);",
        choiceC: "C) array.insert(element);",
        choiceD: "D) array.append(element);",
        correct: "B"
    },
    {
        question: "Что делает оператор + в JavaScript?",
        imgSrc: "https://via.placeholder.com/120/ff5722/FFFFFF?text=+",
        choiceA: "A) Складывает числа или объединяет строки",
        choiceB: "B) Умножает числа",
        choiceC: "C) Делит числа",
        choiceD: "D) Вычитает числа",
        correct: "A"
    },
    {
        question: "Как объявить функцию в JavaScript?",
        imgSrc: "https://via.placeholder.com/120/607d8b/FFFFFF?text=FUNC",
        choiceA: "A) function myFunction() { }",
        choiceB: "B) def myFunction() { }",
        choiceC: "C) func myFunction() { }",
        choiceD: "D) define myFunction() { }",
        correct: "A"
    },
    {
        question: "Какой метод используется для вывода информации в консоль в JavaScript?",
        imgSrc: "https://via.placeholder.com/120/795548/FFFFFF?text=LOG",
        choiceA: "A) print()",
        choiceB: "B) console.log()",
        choiceC: "C) alert()",
        choiceD: "D) show()",
        correct: "B"
    }
];

const totalQuestions = questions.length;
let currentQuestion = 0;
let score = 0;
let count = 0;
const questionTime = 300; // 5 минут = 300 сек
let timer;

start.addEventListener("click", () => {
    start.style.display = "none";
    quiz.style.display = "block";
    renderProgress();
    loadQuestion();
    startTimer();
});

function loadQuestion() {
    const q = questions[currentQuestion];
    questionEl.innerHTML = `<p>${q.question}</p>`;
    qImg.innerHTML = `<img src="${q.imgSrc}" alt="Иконка вопроса">`;
    choices.A.textContent = q.choiceA;
    choices.B.textContent = q.choiceB;
    choices.C.textContent = q.choiceC;
    choices.D.textContent = q.choiceD;
    count = 0;
}

function renderProgress() {
    progressEl.innerHTML = "";
    for (let i = 0; i < totalQuestions; i++) {
        const dot = document.createElement("div");
        dot.className = "prog";
        dot.id = `prog-${i}`;
        progressEl.appendChild(dot);
    }
}

function startTimer() {
    clearInterval(timer);
    timer = setInterval(() => {
        if (count >= questionTime) {
            handleTimeUp();
            return;
        }
        count++;
        const remaining = questionTime - count;
        counterEl.textContent = remaining;
        const percent = (remaining / questionTime) * 100;
        timeGauge.style.width = `${percent}%`;
    }, 1000);
}

function handleTimeUp() {
    markAnswer(false);
    nextQuestion();
}

function checkAnswer(answer) {
    clearInterval(timer);
    const isCorrect = answer === questions[currentQuestion].correct;
    markAnswer(isCorrect);
    setTimeout(nextQuestion, 1200);
}

function markAnswer(isCorrect) {
    const progDot = document.getElementById(`prog-${currentQuestion}`);
    if (isCorrect) {
        score++;
        progDot.classList.add("correct");
    } else {
        progDot.classList.add("wrong");
    }
}

function nextQuestion() {
    currentQuestion++;
    if (currentQuestion < totalQuestions) {
        loadQuestion();
        startTimer();
    } else {
        showScore();
    }
}

function showScore() {
    quiz.style.display = "none";
    const percent = Math.round((score / totalQuestions) * 100);
    let imgSrc;
    if (percent >= 80) imgSrc = "https://via.placeholder.com/120/4caf50/FFFFFF?text=5";
    else if (percent >= 60) imgSrc = "https://via.placeholder.com/120/8bc34a/FFFFFF?text=4";
    else if (percent >= 40) imgSrc = "https://via.placeholder.com/120/ff9800/FFFFFF?text=3";
    else if (percent >= 20) imgSrc = "https://via.placeholder.com/120/ff5722/FFFFFF?text=2";
    else imgSrc = "https://via.placeholder.com/120/f44336/FFFFFF?text=1";

    scoreDiv.innerHTML = `
        <img src="${imgSrc}" alt="Оценка">
        <p>${percent}%</p>
      `;
    scoreDiv.style.display = "block";
}
