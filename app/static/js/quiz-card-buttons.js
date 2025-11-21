document.addEventListener("DOMContentLoaded", () => {

    // Zastaví kliknutí na kartu (aby neotevíralo quiz)
    document.querySelectorAll(".btn-promote, .btn-delete").forEach(btn => {
        btn.addEventListener("click", e => {
            e.preventDefault();
            e.stopPropagation();
        });
    });

    // EDIT tlačítko
    document.querySelectorAll(".btn-promote").forEach(btn => {
        btn.addEventListener("click", () => {
            const id = btn.dataset.id;
            window.location.href = `edit/${id}`;
        });
    });

    // DELETE tlačítko
    document.querySelectorAll(".btn-delete").forEach(btn => {
        btn.addEventListener("click", () => {
            const id = btn.dataset.id;

            // volitelně potvrzení
            if (confirm("Do you really wish to delete this quiz?")) {
                window.location.href = `delete/${id}`;
            }
        });
    });

});