// Formata números para exibição
function formatarNumero(valor, casasDecimais = 1) {
    return parseFloat(valor).toFixed(casasDecimais);
}

// Atualiza status do LED
function atualizarStatusLED(estado) {
    const statusElement = document.getElementById('status-led');
    if (!statusElement) return;
    if (estado === 1) {
        statusElement.innerHTML = '🟢 LED LIGADO';
        statusElement.className = 'led-status led-on';
    } else {
        statusElement.innerHTML = '🔴 LED DESLIGADO';
        statusElement.className = 'led-status led-off';
    }
}

// Verifica conexão com internet
function verificarConexao() {
    if (!navigator.onLine) {
        alert('⚠️ Sem conexão com a internet');
        return false;
    }
    return true;
}

// Log de eventos no console
function logEvento(mensagem, tipo = 'info') {
    const cores = {
        'info': '#3498db',
        'success': '#2ecc71', 
        'error': '#e74c3c',
        'warning': '#f39c12'
    };
    console.log(`%c${mensagem}`, `color: ${cores[tipo]}; font-weight: bold;`);
}

// Atualiza os valores dos sensores (Tempo Real)
function atualizarDados() {
    if (!verificarConexao()) return;

    fetch('/get_sensor_data')
        .then(res => res.json())
        .then(data => {
            if (document.getElementById('temperature-value'))
                document.getElementById('temperature-value').textContent = formatarNumero(data.temperature);
            if (document.getElementById('humidity-value'))
                document.getElementById('humidity-value').textContent = formatarNumero(data.humidity);
            
            const dataAtualizacao = new Date(data.last_update * 1000);
            if (document.getElementById('last-update'))
                document.getElementById('last-update').textContent = dataAtualizacao.toLocaleTimeString();

            logEvento(`Dados atualizados: ${data.temperature}°C, ${data.humidity}%`, 'success');
        })
        .catch(err => {
            logEvento('Erro ao atualizar dados: ' + err, 'error');
        });
}

// Publica comando LED
function publicarComandoLED(estado) {
    if (!verificarConexao()) return;
    const btnOn = document.getElementById('btn-on');
    const btnOff = document.getElementById('btn-off');
    if (btnOn) btnOn.disabled = true;
    if (btnOff) btnOff.disabled = true;

    fetch('/publish_message', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({topic: '/aula_flask/led', message: estado.toString()})
    })
    .then(res => res.json())
    .then(data => {
        atualizarStatusLED(data.led_status);
        logEvento(`Comando enviado: LED ${estado===1?'LIGADO':'DESLIGADO'}`, 'success');
    })
    .catch(err => logEvento('Erro ao publicar: ' + err, 'error'))
    .finally(() => {
        if (btnOn) btnOn.disabled = false;
        if (btnOff) btnOff.disabled = false;
    });
}
