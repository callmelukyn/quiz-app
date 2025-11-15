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
        roleBtn.innerText = "Promote to mod";
        roleBtn.className = "btn-promote";
        roleBtn.onclick = () => promoteUser(user.id);
    }
    else if (user.role === "moderator") {
        roleBtn.innerText = "Demote to user";
        roleBtn.className = "btn-demote";
        roleBtn.onclick = () => demoteUser(user.id);
    }

    document.getElementById("deleteUserBtn").onclick = () => deleteUser(user.id);
}

closeBtn.onclick = () => popup.classList.add("hidden");


async function updateScore(id) {
    const newScore = document.getElementById("newScore").value;

    await fetch(`/admin/edit-points/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ score: newScore })
    });

    showNotify("✅ Updated!", "Score has been successfully updated.");
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