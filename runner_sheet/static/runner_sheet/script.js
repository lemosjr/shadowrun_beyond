/* ARQUIVO: script.js
   OBJETIVO: Controla toda a interatividade (Cliques, Rolagens e Comunicação com o Servidor).
   
   NOTA PARA A EQUIPE:
   Sempre que modificarem este arquivo, lembrem de ir no 'ficha.html'
   e alterar a linha do script para aumentar a versão (Ex: script.js?v=6).
   Se não fizerem isso, o navegador do usuário vai continuar usando a versão velha (Cache).
*/

// --- 1. VARIÁVEIS GLOBAIS ---
// Guardam o estado atual da ficha na memória do navegador.
let danoFisicoAtual = 0;
let danoStunAtual = 0;
let personagemId = 0;

// --- 2. INICIALIZAÇÃO (Assim que a página carrega) ---
document.addEventListener("DOMContentLoaded", () => {
    // Busca os dados escondidos na tag <body> do HTML
    const bodyData = document.body.dataset;
    
    // Converte os textos do HTML para números do Javascript
    personagemId = bodyData.id;
    danoFisicoAtual = parseInt(bodyData.fisico || 0);
    danoStunAtual = parseInt(bodyData.stun || 0);

    // Pinta os quadradinhos de dano iniciais
    renderizarDano();
});

// --- 3. SISTEMA DE DANO (Vitalidade) ---

function renderizarDano() {
    // Loop para pintar Caixas Físicas
    document.querySelectorAll('.box-fisico').forEach(box => {
        const idx = parseInt(box.dataset.index);
        // Se o índice da caixa for menor que o dano atual, pinta de vermelho
        if (idx <= danoFisicoAtual) box.classList.add('filled');
        else box.classList.remove('filled');
    });

    // Loop para pintar Caixas de Stun
    document.querySelectorAll('.box-stun').forEach(box => {
        const idx = parseInt(box.dataset.index);
        if (idx <= danoStunAtual) box.classList.add('filled');
        else box.classList.remove('filled');
    });
}

async function setDano(tipo, valor) {
    // 1. Atualiza visualmente na hora (Feedback instantâneo pro usuário)
    if (tipo === 'fisico') danoFisicoAtual = valor;
    if (tipo === 'stun') danoStunAtual = valor;
    renderizarDano();

    // 2. Salva no Banco de Dados em segundo plano (AJAX/Fetch)
    try {
        // Bate na rota definida em urls.py: path('api/dano/...')
        await fetch(`/api/dano/${personagemId}/${tipo}/${valor}/`);
        console.log(`>> Servidor sincronizado: Dano ${tipo} = ${valor}`);
    } catch (error) {
        console.error("Falha ao salvar dano:", error);
        logNoConsole("ERRO DE CONEXÃO: Dano não salvo no servidor!", true);
    }
}

// --- 4. SISTEMA DE ROLAGENS (Perícias e Armas) ---

async function rolarDados(periciaId, nomeArma = null) {
    // Prepara a mensagem de log
    let msgInicial = ">> Iniciando sub-rotina de dados...";
    let corMsg = "#666"; // Cinza padrão

    if (nomeArma) {
        msgInicial = `>> ENGAJANDO ALVO COM: [${nomeArma}]...`;
        corMsg = "#ff3333"; // Vermelho alerta
    }
    
    logNoConsole(msgInicial, false, corMsg);

    try {
        // Chama a API do Django
        const response = await fetch(`/api/rolar/${periciaId}/`);
        
        if (!response.ok) throw new Error("Erro na API (Verifique o servidor)");
        
        const data = await response.json();

        // Define a cor do resultado (Verde = Sucesso, Vermelho = Falha/Glitch)
        let classeResultado = data.hits > 0 ? 'log-success' : 'log-fail';
        if (data.glitch) classeResultado = 'log-fail';

        // Título do resultado (Mostra nome da arma se houver)
        const tituloTeste = nomeArma ? `${nomeArma} (via ${data.teste})` : data.teste;

        // Monta o HTML do Log
        const html = `
            <div class="log-entry">
                <div>
                    <strong>${tituloTeste}</strong>: 
                    <span class="${classeResultado}">HITS: ${data.hits} (${data.mensagem})</span>
                </div>
                <div class="dice-results">[Pool: ${data.pool_total}] :: [${data.resultados.join(', ')}]</div>
            </div>
        `;
        
        adicionarAoLog(html);

    } catch (error) {
        console.error(error);
        logNoConsole(">> FATAL ERROR: Falha na conexão com Matrix.", true);
    }
}

// --- 5. ROLAGEM DE ATRIBUTO PURO ---

async function rolarAtributo(attrId, nomeAttr) {
    logNoConsole(`>> TESTE DE ATRIBUTO: [${nomeAttr}]...`, false, "#ffff00"); // Amarelo

    try {
        const response = await fetch(`/api/rolar_atributo/${attrId}/`);
        const data = await response.json();
        
        let classeResultado = data.hits > 0 ? 'log-success' : 'log-fail';
        if (data.glitch) classeResultado = 'log-fail';

        const html = `
            <div class="log-entry">
                <div>
                    <strong>${data.teste}</strong>: 
                    <span class="${classeResultado}">HITS: ${data.hits} (${data.mensagem})</span>
                </div>
                <div class="dice-results">[Pool: ${data.pool_total}] :: [${data.resultados.join(', ')}]</div>
            </div>
        `;
        
        adicionarAoLog(html);
        
    } catch (e) {
        console.error(e);
        logNoConsole(">> ERRO DE CONEXÃO.", true);
    }
}

// --- 6. HELPERS (Funções Auxiliares) ---

function adicionarAoLog(htmlContent) {
    const consoleContent = document.getElementById('console-content');
    if (!consoleContent) return; // Segurança caso o HTML mude

    consoleContent.innerHTML += htmlContent;
    consoleContent.scrollTop = consoleContent.scrollHeight; // Rola pra baixo automaticamente

    // Se o console estiver fechado (minimizado), abre ele automaticamente para mostrar o resultado
    const consoleMain = document.getElementById('console-log');
    if(consoleMain && consoleMain.classList.contains('collapsed')) {
        toggleConsole();
    }
}

function logNoConsole(msg, isError, color=null) {
    let style = "";
    if (color) style = `style="color:${color}"`;
    if (isError) style = `style="color:#f00; font-weight:bold"`;
    
    adicionarAoLog(`<div ${style}>${msg}</div>`);
}

// --- 7. UI: CONSOLE RETRÁTIL ---
// Função chamada pelo botão [ MAXIMIZAR / MINIMIZAR ] no HTML
function toggleConsole() {
    const consoleDiv = document.getElementById('console-log');
    const btn = document.getElementById('btn-toggle-console');
    
    // Adiciona/Remove a classe CSS que esconde o corpo do console
    consoleDiv.classList.toggle('collapsed');

    // Troca o texto do botão
    if (consoleDiv.classList.contains('collapsed')) {
        btn.innerText = '[ MAXIMIZAR ]';
    } else {
        btn.innerText = '[ MINIMIZAR ]';
    }
}