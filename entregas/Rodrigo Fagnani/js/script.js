const profissionaisMock = [
    { id: 1, nome: "João Silva", iniciais: "JS", categoria: "Elétrica", descricao: "Instalações elétricas residenciais e comerciais.", avaliacao: "4,8", avaliacoes: 120 },
    { id: 2, nome: "Carlos Souza", iniciais: "CS", categoria: "Elétrica", descricao: "Manutenção, tomadas e iluminação.", avaliacao: "4,7", avaliacoes: 86 },
    { id: 3, nome: "Marcos Oliveira", iniciais: "MO", categoria: "Elétrica", descricao: "Projetos e manutenção elétrica.", avaliacao: "4,9", avaliacoes: 154 },
    { id: 4, nome: "Ana Costa", iniciais: "AC", categoria: "Hidráulica", descricao: "Reparos hidráulicos, torneiras e encanamentos.", avaliacao: "4,9", avaliacoes: 92 },
    { id: 5, nome: "Paula Mendes", iniciais: "PM", categoria: "Limpeza", descricao: "Limpeza residencial detalhada e organização.", avaliacao: "4,8", avaliacoes: 73 },
    { id: 6, nome: "Lucas Almeida", iniciais: "LA", categoria: "Informática", descricao: "Suporte para computadores, redes e instalação.", avaliacao: "4,7", avaliacoes: 61 },
    { id: 7, nome: "Fernanda Rocha", iniciais: "FR", categoria: "Pintura", descricao: "Pintura de ambientes internos e acabamento.", avaliacao: "5,0", avaliacoes: 48 },
    { id: 8, nome: "Roberto Lima", iniciais: "RL", categoria: "Reparos", descricao: "Montagem de móveis e pequenos consertos.", avaliacao: "4,6", avaliacoes: 55 }
];

let favoritos = [];
let usuario = null;

function emailValido(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function semAcentos(texto) {
    return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function criarCardHTML(profissional) {
    const favorito = favoritos.includes(profissional.id);

    return `
        <article class="professional-card">
            <div class="professional-avatar" aria-hidden="true">${profissional.iniciais}</div>
            <div class="professional-content">
                <span class="tag">${profissional.categoria}</span>
                <h3>${profissional.nome}</h3>
                <p>${profissional.descricao}</p>
                <div class="rating">
                    <span aria-hidden="true">★★★★★</span>
                    <strong>${profissional.avaliacao}</strong>
                    <span>(${profissional.avaliacoes} avaliações)</span>
                </div>
                <button class="button button-outline button-full" type="button" data-favorito="${profissional.id}">
                    ${favorito ? "Remover dos favoritos" : "Adicionar aos favoritos"}
                </button>
            </div>
        </article>
    `;
}

function mostrarProfissionais(termo = "") {
    const lista = document.querySelector("#lista-profissionais");
    const mensagem = document.querySelector("#resultado-busca");
    const listaFavoritos = document.querySelector("#lista-favoritos");
    const areaFavoritos = document.querySelector("#favoritos-container");

    if (!lista || !mensagem || !listaFavoritos || !areaFavoritos) {
        return;
    }

    const resultados = profissionaisMock.filter((profissional) => {
        const texto = semAcentos(`${profissional.nome} ${profissional.categoria} ${profissional.descricao}`);
        return texto.toLowerCase().includes(semAcentos(termo.trim()).toLowerCase());
    });

    lista.innerHTML = resultados.map(criarCardHTML).join("");

    if (resultados.length === 0) {
        mensagem.textContent = "Nenhum profissional encontrado.";
    } else {
        mensagem.textContent = `${resultados.length} profissional(is) encontrado(s).`;
    }

    const profissionaisFavoritos = profissionaisMock.filter((profissional) =>
        favoritos.includes(profissional.id)
    );
    listaFavoritos.innerHTML = profissionaisFavoritos.map(criarCardHTML).join("");
    areaFavoritos.hidden = profissionaisFavoritos.length === 0;
}

const formularioBusca = document.querySelector("#form-busca");
const campoBusca = document.querySelector("#busca");

if (formularioBusca && campoBusca) {
    formularioBusca.addEventListener("submit", (event) => {
        event.preventDefault();
        mostrarProfissionais(campoBusca.value);
    });

    campoBusca.addEventListener("input", () => {
        mostrarProfissionais(campoBusca.value);
    });

    mostrarProfissionais();
}

const categorias = document.querySelectorAll(".category-card");

categorias.forEach((categoria) => {
    categoria.addEventListener("click", (event) => {
        const campo = document.querySelector("#busca");
        const titulo = categoria.querySelector(".category-title");

        if (!campo || !titulo) {
            return;
        }

        event.preventDefault();
        campo.value = titulo.textContent;
        mostrarProfissionais(campo.value);
        const secaoProfissionais = document.querySelector("#profissionais");

        if (secaoProfissionais) {
            secaoProfissionais.scrollIntoView({ behavior: "smooth" });
        }
    });
});

const listaProfissionais = document.querySelector("#lista-profissionais");
const listaFavoritos = document.querySelector("#lista-favoritos");

function alternarFavorito(event) {
    const botao = event.target.closest("[data-favorito]");

    if (!botao) {
        return;
    }

    const id = Number(botao.dataset.favorito);

    if (favoritos.includes(id)) {
        favoritos = favoritos.filter((favorito) => favorito !== id);
    } else {
        favoritos.push(id);
    }

    mostrarProfissionais(campoBusca.value);
}

if (listaProfissionais) {
    listaProfissionais.addEventListener("click", alternarFavorito);
}

if (listaFavoritos) {
    listaFavoritos.addEventListener("click", alternarFavorito);
}

const formularioLogin = document.querySelector("#login-form");

if (formularioLogin) {
    formularioLogin.addEventListener("submit", (event) => {
        event.preventDefault();

        const email = document.querySelector("#email");
        const senha = document.querySelector("#senha");
        const erroEmail = document.querySelector("#email-error");
        const erroSenha = document.querySelector("#senha-error");

        erroEmail.textContent = "";
        erroSenha.textContent = "";

        if (!email.value.trim()) {
            erroEmail.textContent = "Informe seu e-mail.";
        } else if (!emailValido(email.value.trim())) {
            erroEmail.textContent = "Digite um e-mail válido.";
        }

        if (!senha.value.trim()) {
            erroSenha.textContent = "Informe sua senha.";
        } else if (senha.value.length < 8) {
            erroSenha.textContent = "A senha deve ter pelo menos 8 caracteres.";
        }

        if (erroEmail.textContent || erroSenha.textContent) {
            return;
        }

        window.location.href = "dashboard.html";
    });
}

const formularioPerfil = document.querySelector("#perfil-form");
const resumoPerfil = document.querySelector("#account-summary");

if (formularioPerfil && resumoPerfil) {
    formularioPerfil.addEventListener("submit", (event) => {
        event.preventDefault();

        const nome = document.querySelector("#nome");
        const email = document.querySelector("#email");
        const senha = document.querySelector("#senha");
        const confirmarSenha = document.querySelector("#confirmar-senha");
        const erroNome = document.querySelector("#nome-error");
        const erroEmail = document.querySelector("#email-error");
        const erroSenha = document.querySelector("#senha-error");
        const erroConfirmarSenha = document.querySelector("#confirmar-senha-error");

        erroNome.textContent = "";
        erroEmail.textContent = "";
        erroSenha.textContent = "";
        erroConfirmarSenha.textContent = "";

        if (!nome.value.trim()) {
            erroNome.textContent = "Informe seu nome.";
        }

        if (!email.value.trim()) {
            erroEmail.textContent = "Informe seu e-mail.";
        } else if (!emailValido(email.value.trim())) {
            erroEmail.textContent = "Digite um e-mail válido.";
        }

        if (!senha.value.trim()) {
            erroSenha.textContent = "Informe sua senha.";
        } else if (senha.value.length < 8) {
            erroSenha.textContent = "A senha deve ter pelo menos 8 caracteres.";
        }

        if (!confirmarSenha.value.trim()) {
            erroConfirmarSenha.textContent = "Confirme sua senha.";
        } else if (confirmarSenha.value !== senha.value) {
            erroConfirmarSenha.textContent = "As senhas não coincidem.";
        }

        if (erroNome.textContent || erroEmail.textContent || erroSenha.textContent || erroConfirmarSenha.textContent) {
            return;
        }

        usuario = { nome: nome.value.trim(), email: email.value.trim() };
        document.querySelector("#profile-name").textContent = usuario.nome;
        document.querySelector("#profile-email").textContent = usuario.email;
        formularioPerfil.hidden = true;
        resumoPerfil.hidden = false;
    });

    const botaoEditar = document.querySelector("#edit-profile");

    if (botaoEditar) {
        botaoEditar.addEventListener("click", () => {
            document.querySelector("#nome").value = usuario.nome;
            document.querySelector("#email").value = usuario.email;
            document.querySelector("#senha").value = "";
            document.querySelector("#confirmar-senha").value = "";
            resumoPerfil.hidden = true;
            formularioPerfil.hidden = false;
        });
    }
}
