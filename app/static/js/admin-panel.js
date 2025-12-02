const searchInput = document.getElementById("userSearch");
const resultsBox = document.getElementById("results");

const popup = document.getElementById("userPopup");
const closeBtn = document.getElementById("closePopup");

searchInput.addEventListener("input", async () => {
    const q = searchInput.value;

    if (q.length < 1) {
        resultsBox.innerHTML = "";
        return;
    }

    const res = await fetch(`/admin/search-users?q=${encodeURIComponent(q)}`);
    const data = await res.json();

    resultsBox.innerHTML = "";

    data.forEach(user => {
        const div = document.createElement("div");
        div.className = "result-item";
        div.textContent = `${user.nickname} (${user.email})`;
        div.onclick = () => openUserPopup(user);
        resultsBox.appendChild(div);
    });
});


function openUserPopup(user) {
    popup.classList.remove("hidden");

    const errorEl = document.getElementById("scoreError");
    errorEl.style.display = "none";
    errorEl.innerText = "";

    document.getElementById("popupNickname").innerHTML = `
    <a href="/players/${user.id}" class="popup-link">
        ${user.nickname}</a><span>↗</span>`;
    document.getElementById("popupEmail").textContent = user.email;
    document.getElementById("popupScore").textContent = user.score;
    document.getElementById("popupRole").textContent = user.role;

    document.getElementById("newScore").value = user.score;
    document.getElementById("saveScoreBtn").onclick = () => updateScore(user.id);
    const roleBtn = document.getElementById("promoteUserBtn");
    if (user.role === "user") {
        roleBtn.onclick = () => promoteUser(user.id);
        roleBtn.innerText = "Promote to mod";
        roleBtn.className = "btn-promote";
    }
    else if (user.role === "moderator") {
        roleBtn.onclick = () => demoteUser(user.id);
        roleBtn.innerText = "Demote to user";
        roleBtn.className = "btn-demote";
    } else if (user.role === "admin") {
        roleBtn.innerText = "Can't be demoted";
        roleBtn.className = "btn-demote";
    }

    document.getElementById("deleteUserBtn").onclick = () => {
        const isConfirmed = confirm(`Are you sure you want to delete "${user.nickname}"?\n\nThis action can not be reverted! All of his quizzes will be removed aswell.`);

        if (isConfirmed) {
            deleteUser(user.id);
        }
    };
}

closeBtn.onclick = () => popup.classList.add("hidden");


async function updateScore(id) {
    const scoreInput = document.getElementById("newScore");
    const errorEl = document.getElementById("scoreError");

    // 1. Reset chyb
    errorEl.style.display = "none";
    errorEl.innerText = "";

    const val = scoreInput.value;

    // --- VALIDACE FRONTEND ---

    // Je to vůbec číslo?
    if (val === "" || isNaN(Number(val))) {
        errorEl.innerText = "❌ You have to enter a number!";
        errorEl.style.display = "block";
        return;
    }

    // Je to CELÉ číslo?
    if (!Number.isInteger(Number(val))) {
        errorEl.innerText = "❌ You have to enter a whole number!";
        errorEl.style.display = "block";
        return; // <--- Tady se to zastaví a nepošle nic na server
    }

    // Je to kladné číslo?
    const newScore = parseInt(val);
    if (newScore < 0) {
        errorEl.innerText = "❌ Score has to be positive number!";
        errorEl.style.display = "block";
        return;
    }

    // --- ODESLÁNÍ NA BACKEND ---
    const res = await fetch(`/admin/edit-points/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ score: newScore })
    });

    // Kontrola chyby ze serveru
    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        const serverMsg = data.detail || "Server error.";

        errorEl.innerText = `❌ ${serverMsg}`;
        errorEl.style.display = "block";
        return;
    }

    // Úspěch
    showNotify("✅ Saved!", "Score has been successfully modified.");
    popup.classList.add("hidden");
    searchInput.dispatchEvent(new Event('input'));
}

async function demoteUser(id) {
    await fetch(`/admin/demote-user/${id}`, {
        method: "POST"
    });

    showNotify("🗑️ Demoted", "User has been successfully demoted to user.");
    popup.classList.add("hidden");

    searchInput.dispatchEvent(new Event('input'));
}

async function promoteUser(id) {
    await fetch(`/admin/promote-user/${id}`, {
        method: "POST"
    });

    showNotify("🗑️ Promoted", "User has been successfully promoted to moderator.");
    popup.classList.add("hidden");

    searchInput.dispatchEvent(new Event('input'));
}

async function deleteUser(id) {
    await fetch(`/admin/delete-user/${id}`, {
        method: "DELETE"
    });

    showNotify("🗑️ Deleted", "Account has been successfully deleted.");
    popup.classList.add("hidden");

    searchInput.dispatchEvent(new Event('input'));
}

function showNotify(title, message) {
    const notify = document.getElementById("notifyPopup");
    const titleEl = document.getElementById("notifyTitle");
    const msgEl = document.getElementById("notifyMessage");

    titleEl.innerHTML = title;
    msgEl.innerHTML = message;

    notify.classList.remove("hidden");

    // Animace
    notify.querySelector(".popup-content").classList.add("notify-anim");

    // Schovat po animaci
    setTimeout(() => {
        notify.classList.add("hidden");
        notify.querySelector(".popup-content").classList.remove("notify-anim");
    }, 1200);
}