function login(event) {
    event.preventDefault();

    const url = new URL("/login", window.location.origin);
    const errorEl = document.getElementById("login-error");
    errorEl.classList.add("hidden");
    errorEl.textContent = "";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: document.getElementById("email").value,
            senha: document.getElementById("senha").value
        })
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(payload => {
                throw new Error(payload?.erro || "Falha ao logar");
            });
        }

        return res.json();
    })
    .then(data => {
        if (["ADMIN", "PROFESSOR", "ALUNO"].includes(data.tipo)) {
            window.location.href = "/dashboard";
            return;
        }

        throw new Error("Usuário inválido");
    })
    .catch(error => {
        errorEl.textContent = error.message || "Erro ao conectar com o servidor";
        errorEl.classList.remove("hidden");
    });
}
